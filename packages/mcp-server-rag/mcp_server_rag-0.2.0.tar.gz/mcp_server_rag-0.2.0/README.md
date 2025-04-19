# MCP Server RAG

RAG (Retrieval-Augmented Generation) server for MCP (Model Control Protocol). This server provides vector-based document retrieval functionality to enhance LLM interactions with contextual information.

## Overview

The MCP Server RAG implementation provides a bridge between your LLM applications and document collections, offering:

- Vector-based document search using ChromaDB and Sentence Transformers
- Multiple specialized collections (liv, ken, ufa, sap commerce)
- Strongly typed API responses
- Integration with the MCP server infrastructure

## Installation

```bash
pip install rag-mcp-server
```

## Usage

After installation, you can run the server with:

```bash
mcp-server-rag
```

Or using Python module syntax:

```bash
python -m mcp_server_rag
```

## Features

- Vector-based search for contextual document retrieval
- Persistent storage of document embeddings via ChromaDB
- Multiple collection support for domain-specific searches
- Configurable via environment variables
- Fully typed response objects with detailed metadata
- Seamless integration with the MCP protocol

## Available Collections

The server provides access to four specialized collections:

- `liv-rag`: LIV document collection (`retrieve_liv_context` tool)
- `ken-rag`: Kennametal document collection (`retrieve_ken_context` tool)
- `ufa-rag`: UFA document collection (`retrieve_ufa_context` tool)
- `sap-comm-rag`: SAP Commerce document collection (`retrieve_sap_comm_context` tool)

## Configuration

The following environment variables can be used to configure the server:

| Variable | Description | Default |
|----------|-------------|--------|
| `RAG_PERSIST_DIR` | Directory where ChromaDB will store its data | `~/Documents/chroma_db` |
| `RAG_EMBEDDING_MODEL` | Path or name of the Sentence Transformer model | `~/LLM/huggingface/hub/models--sentence-transformers--all-MiniLM-L6-v2/...` |
| `RAG_N_RESULTS` | Default number of results to return from searches | `5` |

## Dependencies

- click
- mcp (version 1.2.0 or higher)
- chromadb
- sentence-transformers

## Development

### Building and Publishing

The repo includes a `publish.sh` script that helps with building and publishing the package.

```bash
./publish.sh
```

This script will clean previous build artifacts, install build dependencies, build the package, and check it before providing instructions for publishing to PyPI.

## License

MIT
