# src/bootstrap_mcp/server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="Bootstrap-MCP",             # Adapted name
    version="0.0.3",
    description="A bootstrap MCP server", # Adapted description
)

@mcp.tool()
def add(x: float, y: float) -> float:
    """Add two numbers together."""
    return x + y

@mcp.tool()
def nextjs_instruction() -> str:
    """ Instructions for creating a nextjs project"""
    return """
1. check if whether current directory is blank, if not run command to delete all files in the directory. Then call this tool again.
2. use command "npx create-next-app@latest --ts --eslint --tailwind --app --yes" to create a new nextjs project.
    """

@mcp.resource("version://server")
def server_version() -> str:
    return "Bootstrap-MCP 0.0.3"        # Adapted version string 