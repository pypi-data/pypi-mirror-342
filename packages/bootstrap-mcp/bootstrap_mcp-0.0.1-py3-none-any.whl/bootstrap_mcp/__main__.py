# src/bootstrap_mcp/__main__.py
import asyncio
from mcp.server.stdio import stdio_server
from .server import mcp  # Adapted import

def cli() -> None:
    async def _run():
        async with stdio_server() as (reader, writer):
            await mcp.run(reader, writer, mcp.create_initialization_options())
    asyncio.run(_run()) 