import asyncio
import json
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.shared.exceptions import McpError

# ──────────────────────────────────────────────────────────────────────────
# Logging
# ──────────────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s [%(funcName)s] %(message)s")
logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────────────────
# Chroma memory limit (default 768 MB)
# ──────────────────────────────────────────────────────────────────────────
DEFAULT_CHROMA_LIMIT = 768 * 1024 ** 2  # 768 MB
CHROMA_MEM_LIMIT_BYTES: int = int(os.getenv("CHROMA_MEM_LIMIT_BYTES", DEFAULT_CHROMA_LIMIT))

# ──────────────────────────────────────────────────────────────────────────
# Typed helpers
# ──────────────────────────────────────────────────────────────────────────
# ──────────────────────────────────────────────────────────────────────────
# Typed helpers (unchanged)
# ──────────────────────────────────────────────────────────────────────────
class SearchResult(types.BaseModel):
    document_number: int
    content: str
    metadata: Dict[str, Any]
    relevance: str
    distance_score: float = 0.0

    def to_text(self) -> str:
        meta_block = "\n".join(f"{k}: {v}" for k, v in self.metadata.items())
        return (
            f"Document Number: {self.document_number}\n"
            f"Relevance: {self.relevance}\n"
            f"Distance Score: {self.distance_score:.4f}\n\n"
            f"Metadata:\n{meta_block}\n\nContent:\n{self.content}"
        )

    def to_tool_result(self) -> List[types.TextContent]:
        return [types.TextContent(type="text", text=self.to_text())]


@dataclass
class SearchResponse:
    status: str
    query: str
    results: List[SearchResult] = field(default_factory=list)
    message: Optional[str] = None

    def to_tool_result(self) -> List[types.TextContent]:
        if self.status != "success":
            return [types.TextContent(type="text", text=f"Status: {self.status}\nMessage: {self.message}")]

        sep = "\n" + "-" * 60 + "\n"
        body = sep.join(r.to_text() for r in self.results)
        header = (
            f"Search Results for: {self.query}\nStatus: {self.status}\n"
            f"Results: {len(self.results)}\n{sep}"
        )
        return [types.TextContent(type="text", text=header + body)]

# ──────────────────────────────────────────────────────────────────────────
# Config + state
# ──────────────────────────────────────────────────────────────────────────
@dataclass
class ServerConfig:
    """Configuration for the RAG system that can be controlled through environment variables.
    
    Attributes:
        persist_dir: Directory where ChromaDB will store its data
        embedding_model_name: Path or name of the Sentence Transformer model
        n_results: Default number of results to return from searches
    """
    persist_dir: str = os.getenv("RAG_PERSIST_DIR", str(Path.home() / "Documents/chroma_db_mpnet"))
    embedding_model_name: Optional[str] = os.getenv("RAG_EMBEDDING_MODEL", None)
    n_results: int = int(os.getenv("RAG_N_RESULTS", "5"))


class GlobalState:
    """Container for global state with proper typing"""
    def __init__(self) -> None:
        self.embedding_model: Optional[SentenceTransformer] = None
        self.chroma_client: Optional[chromadb.PersistentClient] = None
        self.config: ServerConfig = ServerConfig()

state = GlobalState()

# ──────────────────────────────────────────────────────────────────────────
# Helper functions
# ──────────────────────────────────────────────────────────────────────────

def _ensure_chroma_client() -> chromadb.PersistentClient:
    if state.chroma_client is None:
        logger.info(f"Initializing ChromaDB client at path: {state.config.persist_dir}")
        logger.info("Chroma client (LRU, limit %s bytes)", CHROMA_MEM_LIMIT_BYTES)
        state.chroma_client = chromadb.PersistentClient(
            path=state.config.persist_dir,
            settings=Settings(
                anonymized_telemetry=False,
                chroma_segment_cache_policy="LRU",
                chroma_memory_limit_bytes=CHROMA_MEM_LIMIT_BYTES,
            ),
        )
        logger.info("Chroma client initialized.")
    return state.chroma_client


def _get_collection(name: str) -> chromadb.Collection:
    return _ensure_chroma_client().get_or_create_collection(name)

def initialize_services() -> None:
    """Load the embedding model and prepare the Chroma client."""
    try:
        # Ensure data directory exists
        os.makedirs(state.config.persist_dir, exist_ok=True)

        if state.embedding_model is None:
            # Ensure embedding_model_name has a default if not set by env var
            model_name = state.config.embedding_model_name or "all-mpnet-base-v2" # Defaulting to the model used in chunker
            logger.info(f"Initializing embedding model: {model_name}")
            state.embedding_model = SentenceTransformer(model_name)
            logger.info("Embedding model initialized.")

        _ensure_chroma_client()  # make sure client exists

    except Exception as exc:
        logger.critical("Initialisation failed: %s", exc, exc_info=True)
        raise McpError("Core service initialisation failed")

async def _vector_search(query: str, collection_name: str) -> List[SearchResult]:
    """
    Performs context retrieval using pre-initialized services.
    Returns a list of SearchResult objects or raises an exception on failure.
    """
    if state.embedding_model is None:
        logger.error("Attempted to retrieve context before services were initialized.")
        raise RuntimeError("Services not initialized. Server startup might have failed.")

    collection = _get_collection(collection_name)
    logger.debug(f"Generating embedding for query: '{query[:50]}...'")
    embed = state.embedding_model.encode([query], convert_to_numpy=True).tolist()
    logger.debug("Embedding generated and converted to list.")

    logger.debug(f"Querying collection '{collection_name}' with {state.config.n_results} results.")
    results = collection.query(
        query_embeddings=embed,
        n_results=state.config.n_results,
        include=["documents", "metadatas", "distances"],
    )

    logger.debug(f"Query completed. Found results: {'Yes' if results and results.get('ids') and results['ids'][0] else 'No'}")

    if not results or not results.get("ids") or not results["ids"][0]:
        return []

    search_results = []

    ids = results['ids'][0]
    documents = results.get('documents', [[]])[0]
    metadatas = results.get('metadatas', [[]])[0]
    distances = results.get('distances', [[]])[0]

    if not (len(ids) == len(documents) == len(metadatas) == len(distances)):
         logger.warning("ChromaDB query result lists have inconsistent lengths.")

    num_results_found = len(ids)
    for i in range(num_results_found):
        distance = distances[i]
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

async def _get_collection_info(name: str) -> List[types.TextContent]:
    col = _get_collection(name)
    count = col.count()
    info = (
        f"collection_name: {name}\ndocument_count: {count}\npersist_directory: {state.config.persist_dir}\n"
        f"embedding_model: {state.config.embedding_model_name or 'all-mpnet-base-v2'}"
    )
    return [types.TextContent(type="text", text=info)]

async def serve() -> None:
    server = Server("RAG System")
    """Main entry point for the RAG server."""
    logger.info("Starting RAG server initialization...")
    try:
        initialize_services()
        logger.info("Core services initialized successfully.")
    except Exception as e:
         logger.critical(f"Fatal error during server initialization: {e}", exc_info=True)
         return

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
                results: List[SearchResult] = await _vector_search(query, collection_name)

                search_response = SearchResponse(
                    status="success" if results else "no_results",
                    query=query,
                    results=results,
                    message="Retrieved successfully." if results else "No relevant documents found."
                )

                logger.info(f"Returning {len(results)} results for tool call '{name}'.")
                return search_response.to_tool_result()

            except Exception as e:
                logger.error(f"Error executing retrieval tool '{name}': {e}", exc_info=True)
                raise ValueError(f"Failed to execute retrieval tool '{name}': An internal error occurred.")
        elif name in collection_info_mapping:
            collection_name = collection_info_mapping[name]
            return await _get_collection_info(collection_name)
        else:
             logger.error(f"Unknown tool called: {name}")
             raise ValueError(f"Unknown tool: {name}")

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)