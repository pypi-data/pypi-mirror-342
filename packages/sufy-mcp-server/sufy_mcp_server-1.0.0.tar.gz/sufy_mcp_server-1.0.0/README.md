# Sufy MCP Server

[Chinese Documentation](README_zh.md) | [English Documentation](README.md)

## Overview

The Model Context Protocol (MCP) Server built on Sufy products allows users to access Sufy services through this MCP Server within the context of AI large model clients.

## Environment Requirements

• Python 3.12 or higher
• uv package manager

If you haven't installed uv yet, you can install it with the following command:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Usage in Cline

Steps:

1. Install the Cline plugin in VSCode (the Cline icon will appear in the sidebar after installation)
2. Configure the Large Model
3. Configure Sufy MCP
    1. Click the Cline icon to enter the plugin interface and select the MCP Server module
    2. Choose "Installed", click "Advanced MCP Settings", and configure using the following template:
   ```json
   {
     "mcpServers": {
       "Sufy": {
         "command": "uvx",
         "args": [
           "sufy-mcp-server"
         ],
         "env": {
           "SUFY_ACCESS_KEY": "YOUR_ACCESS_KEY",
           "SUFY_SECRET_KEY": "YOUR_SECRET_KEY",
           "SUFY_REGION_NAME": "YOUR_REGION_NAME",
           "SUFY_ENDPOINT_URL": "YOUR_ENDPOINT_URL",
           "SUFY_BUCKETS": "YOUR_BUCKET_A,YOUR_BUCKET_B"
        },
         "disabled": false
       }
     }
   }
   ```
    3. Toggle the connection switch for Sufy MCP Server to establish connection
4. Create a chat window in Cline to interact with AI using sufy-mcp-server. Example prompts:
    ◦ List Sufy resource information
    ◦ List all Buckets in Sufy
    ◦ List files in Sufy's xxx Bucket
    ◦ Read content of yyy file in Sufy's xxx Bucket
    ◦ Resize image yyy in Sufy's xxx Bucket by 20%

Note: When creating an MCP Server in Cline, you can directly use the above configuration.

## Development

1. Clone the repository:
```bash
git clone git@github.com:sufy/sufy-mcp-server.git
cd sufy-mcp-server
```

2. Create and activate virtual environment:
```bash
uv venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
uv pip install -e .
```

4. Configuration

Copy environment template:
```bash
cp .env.example .env
```

Edit `.env` file with these parameters:
```bash
# S3/Sufy credentials
SUFY_ACCESS_KEY=your_access_key
SUFY_SECRET_KEY=your_secret_key

# Region info
SUFY_REGION_NAME=your_region
SUFY_ENDPOINT_URL=endpoint_url # eg:https://s3.your_region.sufycs.com

# Configure buckets (comma-separated, max 20 recommended)
SUFY_BUCKETS=bucket1,bucket2,bucket3
```

For feature extensions:
1. Create a new business package directory under `core` (e.g., storage)
2. Implement features in the package directory
3. Register tools/resources via `load()` function in the package's `__init__.py`
4. Call the load function in `core/__init__.py` to complete registration

Directory structure:
```shell
core
├── __init__.py # Load business tools/resources
└── storage # Storage service
    ├── __init__.py # Load storage tools/resources
    ├── resource.py # Storage resources
    ├── storage.py # Storage utilities
    └── tools.py # Storage tools
```

## Testing

### Using Model Control Protocol Inspector

Recommended tool: [Model Control Protocol Inspector](https://github.com/modelcontextprotocol/inspector)

```shell
# Requires node v22.4.0
npx @modelcontextprotocol/inspector uv --directory . run sufy-mcp-server
```

### Local MCP Server Examples

1. Start in stdio mode (default):
```bash
uv --directory . run sufy-mcp-server
```

2. Start in SSE mode (for web applications):
```bash
uv --directory . run sufy-mcp-server --transport sse --port 8000
```