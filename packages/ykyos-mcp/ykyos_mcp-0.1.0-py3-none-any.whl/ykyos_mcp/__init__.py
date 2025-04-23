"""
YkyosMCP - A Model Context Protocol server for URL processing and image extraction
"""

__version__ = "0.1.0"

from .server import mcp

def main():
    """
    Entry point for the MCP server.
    This function is called when the package is run via the command line.
    """
    print("Starting YKY's MCP Server for URL Processing and Image Extraction...")
    mcp.run()

if __name__ == "__main__":
    main()