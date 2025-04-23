"""
Entry point for running the boring-news-mcp server
"""

from .client import mcp

def main():
    """Run the MCP server"""
    mcp.run()

if __name__ == "__main__":
    main() 