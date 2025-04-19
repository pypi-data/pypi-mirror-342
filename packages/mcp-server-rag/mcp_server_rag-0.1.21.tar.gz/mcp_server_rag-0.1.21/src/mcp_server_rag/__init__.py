import click
from .server import serve, initialize_services

@click.command()
def main() -> None:
    """RAG MCP Server - RAG functionality for LLM"""
    import asyncio
    import logging
    """Main entry point for the RAG server."""
    logger.info("Starting RAG server initialization...")
    try:
        initialize_services()
        logger.info("Core services initialized successfully.")
    except Exception as e:
         logger.critical(f"Fatal error during server initialization: {e}", exc_info=True)
         return

    asyncio.run(serve())

if __name__ == "__main__":
    main()
