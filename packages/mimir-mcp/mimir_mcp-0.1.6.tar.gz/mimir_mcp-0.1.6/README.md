# Mimir MCP

[![PyPI Version](https://img.shields.io/pypi/v/mimir-mcp?style=for-the-badge&color=%230094FF)](https://pypi.org/project/mimir-mcp/)

MCP (Model Context Protocol) server for Mimir AI with authenticated API support.

## Installation

You can install the package directly from PyPI:

```bash
pip install mimir-mcp
```

Alternatively, you can clone the repository and install the package locally:

```bash
# Clone the repository
git clone https://github.com/trymimirai/mimir-mcp.git
cd mimir-mcp

# Install the package
pip install -e .
```

## Configuration

This MCP uses our [official Mimir API library](https://github.com/trymimirai/mimir-api) under the hood, and thus requires configuration for the API base URL and authentication key. These can be provided in 2 different ways:

1. **Environment Variables** (prioritized):

   - `MIMIR_API_URL`: The base URL for the API (optional, default: "https://dev.trymimir.ai/api")
   - `MIMIR_API_KEY`: Your API authentication key

2. **Configuration File** (used when environment variables are missing):
   Create a file at `~/.mimir/config.json` with the following structure:

   ```json
   {
     "api_url": "https://dev.trymimir.ai/api",
     "api_key": "your-api-key-here"
   }
   ```

   > **Note:** If an environment variable is set, it will take precedence over the corresponding value in the config file. The config file is only read if at least one of the required values is not set as an environment variable.

### Claude Desktop Configuration

To use with Claude desktop, update your Claude configuration file (typically at `%APPDATA%\Claude\claude_desktop_config.json` on Windows) to include the environment variables:

```json
{
  "mcpServers": {
    "Mimir": {
      "command": "mimir-mcp",
      "env": {
        "MIMIR_API_URL": "https://dev.trymimir.ai/api",
        "MIMIR_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

## Usage

Once installed, you can run the MCP server directly:

```bash
mimir-mcp
```

Or configure it in Claude desktop as described above.
