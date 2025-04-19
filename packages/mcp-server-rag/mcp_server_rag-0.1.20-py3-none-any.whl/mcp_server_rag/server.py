import asyncio
import os
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Any

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import logging
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.shared.exceptions import McpError
from mcp.server.stdio import stdio_server

@dataclass
class SearchResult:
    document_number: int
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    relevance: str = "Unknown"
    distance_score: float = 0.0

    def to_text(self) -> str:
        metadata_formatted = "\n".join([f"{key}: {value}" for key, value in self.metadata.items()])
        return f"""
Document Number: {self.document_number}
Relevance: {self.relevance}
Distance Score: {self.distance_score:.4f} # Format distance

Metadata:
{metadata_formatted}

Content:
{self.content}
        """

    def to_prompt_result(self) -> types.GetPromptResult:
        return types.GetPromptResult(
            description=f"Search Result: Document #{self.document_number}",
            messages=[
                types.PromptMessage(
                    role="user", content=types.TextContent(type="text", text=self.to_text())
                )
            ],
        )

    def to_tool_result(self) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        return [types.TextContent(type="text", text=self.to_text())]

@dataclass
class SearchResponse:
    status: str
    query: str
    results: List[SearchResult] = field(default_factory=list)
    message: Optional[str] = None

    def to_text(self) -> str:
        if self.status != "success":
            return f"Status: {self.status}\nMessage: {self.message or 'No additional information'}"

        result_texts = [result.to_text() for result in self.results]
        separator = "\n\n" + "-" * 50 + "\n\n"

        return f"""
Search Results for: {self.query}
Status: {self.status}
Number of Results: {len(self.results)}
Message: {self.message or "Success"}

{separator.join(result_texts)}
        """

    def to_prompt_result(self) -> types.GetPromptResult:
        return types.GetPromptResult(
            description=f"Search Results for: {self.query}",
            messages=[
                types.PromptMessage(
                    role="user", content=types.TextContent(type="text", text=self.to_text())
                )
            ],
        )

    def to_tool_result(self) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        # Returns the formatted text of the whole search response
        return [types.TextContent(type="text", text=self.to_text())]


@dataclass
class ServerConfig:
    """Configuration for the RAG system that can be controlled through environment variables.
    
    Attributes:
        persist_dir: Directory where ChromaDB will store its data
        embedding_model_name: Path or name of the Sentence Transformer model
        n_results: Default number of results to return from searches
    """
    persist_dir: str = os.getenv('RAG_PERSIST_DIR', str(Path.home() / "Documents/chroma_db_mpnet"))
    embedding_model_name: Optional[str] = os.getenv('RAG_EMBEDDING_MODEL', None)
    n_results: int = int(os.getenv('RAG_N_RESULTS', "5"))


class GlobalState:
    """Container for global state with proper typing"""
    def __init__(self):
        self.embedding_model: Optional[SentenceTransformer] = None
        self.chroma_client: Optional[chromadb.PersistentClient] = None
        self.collections: Dict[str, chromadb.Collection] = {}
        self.config: ServerConfig = ServerConfig()

state = GlobalState()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [%(funcName)s] - %(message)s')
logger = logging.getLogger(__name__)

def initialize_services():
    """Asynchronously set up our core services: embedding model and vector database."""
    global state
    try:
        # Ensure data directory exists
        os.makedirs(state.config.persist_dir, exist_ok=True)

        # Eagerly load the embedding model
        if state.embedding_model is None:
            # Ensure embedding_model_name has a default if not set by env var
            model_name = state.config.embedding_model_name or "all-mpnet-base-v2" # Defaulting to the model used in chunker
            logger.info(f"Initializing embedding model: {model_name}")
            state.embedding_model = SentenceTransformer(model_name)
            logger.info("Embedding model initialized.")
        else:
             logger.info("Embedding model already initialized.")

        # Eagerly initialize the ChromaDB client
        if state.chroma_client is None:
            logger.info(f"Initializing ChromaDB client at path: {state.config.persist_dir}")
            state.chroma_client = chromadb.PersistentClient(
                path=state.config.persist_dir,
                settings=Settings(anonymized_telemetry=False) # Consider other Chroma settings if needed
            )
            logger.info("ChromaDB client initialized.")
        else:
            logger.info("ChromaDB client already initialized.")

    except Exception as e:
        logger.error(f"Initialization failed: {e}", exc_info=True)
        raise McpError(f"Core service initialization failed: {e}")

async def retrieve_context(query: str, collection_name: str) -> List[SearchResult]:
    """
    Performs context retrieval using pre-initialized services.
    Returns a list of SearchResult objects or raises an exception on failure.
    """
    global state
    if not state.embedding_model or not state.chroma_client:
        logger.error("Attempted to retrieve context before services were initialized.")
        raise RuntimeError("Services not initialized. Server startup might have failed.")

    try:
        # Get or create the collection if not already cached
        collection: Optional[chromadb.Collection] = state.collections.get(collection_name)
        if collection is None:
            logger.info(f"Collection '{collection_name}' not in cache. Getting or creating...")
            collection = state.chroma_client.get_or_create_collection(collection_name)
            state.collections[collection_name] = collection
            logger.info(f"Collection '{collection_name}' initialized and cached.")

        # Generate query embedding
        # Ensure embedding is List[float] for ChromaDB
        logger.debug(f"Generating embedding for query: '{query[:50]}...'")
        # Generate embedding as NumPy array
        query_embedding_np = state.embedding_model.encode([query], convert_to_numpy=True)
        # Convert to list (Chroma expects list of embeddings, even if just one)
        query_embedding_list = query_embedding_np.tolist()
        logger.debug("Embedding generated and converted to list.")
        
        # Perform vector search
        logger.debug(f"Querying collection '{collection_name}' with {state.config.n_results} results.")
        results = collection.query(
            query_embeddings=query_embedding_list, # Pass the list of lists
            n_results=state.config.n_results,
            include=['documents', 'metadatas', 'distances']
        )
        logger.debug(f"Query completed. Found results: {'Yes' if results and results.get('ids') and results['ids'][0] else 'No'}")


        # Process results
        search_results = []
        # Check if results are valid and contain data
        if results and results.get('ids') and results['ids'][0]:
            ids = results['ids'][0]
            documents = results.get('documents', [[]])[0]
            metadatas = results.get('metadatas', [[]])[0]
            distances = results.get('distances', [[]])[0]

            if not (len(ids) == len(documents) == len(metadatas) == len(distances)):
                 logger.warning("ChromaDB query result lists have inconsistent lengths.")
                 # Handle potential inconsistency, e.g., take the minimum length

            num_results_found = len(ids)
            for i in range(num_results_found):
                distance = distances[i]
                # Determine relevance based on distance (tune thresholds as needed)
                if distance < 0.5:
                    relevance = "High"
                elif distance < 0.8:
                    relevance = "Medium"
                else:
                    relevance = "Low"

                search_results.append(
                    SearchResult(
                        document_number=i + 1,
                        content=documents[i],
                        metadata=metadatas[i] or {},
                        relevance=relevance,
                        distance_score=distance
                    )
                )

        if not search_results:
             logger.warning(f"No relevant documents found for query: '{query[:50]}...' in collection: '{collection_name}'")

        return search_results

    except Exception as e:
        logger.error(f"Error retrieving context for query '{query[:50]}...' in collection '{collection_name}': {e}", exc_info=True)
        raise

async def get_collection_info(collection_name: str) -> str:
    """Gets information about a specific collection."""
    global state
    if not state.chroma_client:
        logger.error("Attempted to get collection info before ChromaDB client was initialized.")
        return json.dumps({"status": "error", "message": "ChromaDB client not initialized"})

    try:
        collection = state.chroma_client.get_collection(collection_name)
        doc_count = collection.count()
        logger.info(f"Retrieved info for collection '{collection_name}'. Count: {doc_count}")
        return json.dumps({
            "status": "success",
            "collection_name": collection_name,
            "document_count": doc_count,
            "persist_directory": state.config.persist_dir,
            "embedding_model": state.config.embedding_model_name or "all-mpnet-base-v2",
        }, indent=2)
    except Exception as e:
        logger.warning(f"Could not get info for collection '{collection_name}': {e}", exc_info=True)
        return json.dumps({
            "status": "error",
            "collection_name": collection_name,
            "message": f"Could not retrieve info or collection does not exist: {str(e)}"
        }, indent=2)

async def serve() -> None:
    server = Server("RAG System") # Updated name

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name="retrieve_liv_context",
                description="Search for documents relevant to a query in the 'liv-rag' collection.",
                inputSchema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}
            ),
            types.Tool(
                name="retrieve_ken_context",
                description="Search for documents relevant to a query in the 'ken-rag' collection.",
                inputSchema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}
            ),
            types.Tool(
                name="retrieve_ufa_context",
                description="Search for documents relevant to a query in the 'ufa-rag' collection.",
                inputSchema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}
            ),
        ]

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: Optional[dict] = None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:

        logger.info(f"Handling tool call: {name} with arguments: {arguments}")
        retrieve_collection_mapping = {
            "retrieve_liv_context": "liv-rag",
            "retrieve_ken_context": "ken-rag",
            "retrieve_ufa_context": "ufa-rag",
            "retrieve_sap_comm_context": "sap-comm-rag"
        }
        # Map tool names to collection names for collection info tools
        collection_info_mapping = {
            "get_liv_collection_info": "liv-rag",
            "get_ken_collection_info": "ken-rag",
            "get_ufa_collection_info": "ufa-rag",
            "get_sap_comm_collection_info": "sap-comm-rag"
        }

        if name in retrieve_collection_mapping:
            if not arguments or not arguments.get("query"):
                logger.error("Missing or empty 'query' argument for retrieval tool.")
                raise ValueError("Missing or empty 'query' argument.")

            collection_name = retrieve_collection_mapping[name]
            query = arguments["query"]

            try:
                results: List[SearchResult] = await retrieve_context(query, collection_name)

                search_response = SearchResponse(
                    status="success" if results else "no_results",
                    query=query,
                    results=results,
                    message="Retrieved successfully." if results else "No relevant documents found."
                )

                logger.info(f"Returning {len(results)} results for tool call '{name}'.")
                return search_response.to_tool_result()

            except Exception as e:
                # Log the full error and return a user-friendly error via MCP
                logger.error(f"Error executing retrieval tool '{name}': {e}", exc_info=True)
                raise ValueError(f"Failed to execute retrieval tool '{name}': An internal error occurred.")
        elif name in collection_info_mapping:
            collection_name = collection_info_mapping[name]
            return await get_collection_info(collection_name)
        else:
             logger.error(f"Unknown tool called: {name}")
             raise ValueError(f"Unknown tool: {name}")

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)