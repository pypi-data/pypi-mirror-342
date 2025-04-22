from .mcp_dispatch_service import mcp

def main():
    """启动MCP派车服务"""
    mcp.run(transport="stdio")

__version__ = "0.1.0" 