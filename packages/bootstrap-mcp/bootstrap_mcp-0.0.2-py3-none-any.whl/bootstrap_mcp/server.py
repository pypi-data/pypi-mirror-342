# src/bootstrap_mcp/server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="Bootstrap-MCP",             # Adapted name
    version="0.0.2",
    description="A bootstrap MCP server", # Adapted description
)

@mcp.tool()
def add(x: float, y: float) -> float:
    """Add two numbers together."""
    return x + y

@mcp.resource("version://server")
def server_version() -> str:
    return "Bootstrap-MCP 0.0.2"        # Adapted version string 