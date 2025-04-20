# src/bootstrap_mcp/__main__.py
from bootstrap_mcp.server import mcp   # 你的 FastMCP 实例

def cli() -> None:
    """Entry‑point declared in [project.scripts]."""
    mcp.run()   # FastMCP v2: 自动使用 STDIO 传输
