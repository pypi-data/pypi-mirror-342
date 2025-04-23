# __init__.py
from .yuanqiserver import mcp

def main():
    """MCP YaunQi Server - HTTP call YaunQi API for MCP"""
    mcp.run()

if __name__ == "__main__":
    main()
