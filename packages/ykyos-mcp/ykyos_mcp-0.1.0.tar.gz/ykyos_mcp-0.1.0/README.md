# YkyosMCP

A Model Context Protocol (MCP) server that processes URLs and extracts images.

## Features

This MCP server provides three main tools:

1. **fetch_markdown**: Takes a URL and returns its content as markdown by prepending https://r.jina.ai/
2. **extract_images**: Takes markdown content and extracts all image URLs
3. **download_images**: Takes a list of image URLs and downloads them to a specified directory

## Installation

```bash
pip install ykyos-mcp
```

## Usage with Claude Desktop

Add the following configuration to your Claude Desktop settings:

```json
{
  "mcpServers": {
    "YkeyMCP": {
      "isActive": true,
      "command": "uvx",
      "args": [
        "ykyos-mcp"
      ],
      "env": {
        "DOWNLOAD_BASE_PATH": "/path/to/download/directory"
      }
    }
  }
}
```

Replace `/path/to/download/directory` with the directory where you want to save downloaded images.

## Development

To set up for development:

```bash
# Clone the repository
git clone https://github.com/your-username/ykyos-mcp.git
cd ykyos-mcp

# Install in development mode
pip install -e .
```

## License

MIT License