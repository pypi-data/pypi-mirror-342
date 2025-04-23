"""
Setup script for backward compatibility with older pip versions.
"""
from setuptools import setup

if __name__ == "__main__":
    setup(
        name="ykyos-mcp",
        version="0.1.0",
        description="MCP Server for URL Processing and Image Extraction",
        author="YKY",
        author_email="info@ykyos.com",
        packages=["ykyos_mcp"],
        install_requires=[
            "mcp>=1.4.0",
            "aiohttp>=3.8.0",
            "aiofiles>=0.8.0"
        ]
    )