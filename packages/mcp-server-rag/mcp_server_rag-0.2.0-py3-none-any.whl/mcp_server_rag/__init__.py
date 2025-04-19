import click
from .server import serve

@click.command()
def main() -> None:
    """RAG MCP Server - RAG functionality for LLM"""
    import asyncio

    asyncio.run(serve())

if __name__ == "__main__":
    main()
