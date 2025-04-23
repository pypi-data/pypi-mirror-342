# MCP Development Tools Setup Guide

## Prerequisites

- Python 3.x
- UV package installer
- Claude Desktop (for integration)

## Installation

1. Install UV (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Install dependencies using UV:
```bash
uv add requirement.txt
uv add "mcp[cli]"
```

## Usage

### Running MCP Command
To execute the MCP command using UV:
```bash
uv run mcp
```

### Running MCP Inspector
To start the MCP inspector:
```bash
mcp dev server.py
```

## Claude Desktop Integration

### Basic Installation
Install your server in Claude Desktop:
```bash
mcp install server.py
```

### Advanced Installation Options

#### Custom Server Name
To install with a custom name:
```bash
mcp install server.py --name "My Analytics Server"
```

#### Environment Variables
There are two ways to configure environment variables:

1. Direct specification:
```bash
mcp install server.py -v API_KEY=abc123 -v DB_URL=postgres://...
```

2. Using an environment file:
```bash
mcp install server.py -f .env
```

## Additional Resources

For more detailed information about MCP tools and their usage, please refer to the official documentation.