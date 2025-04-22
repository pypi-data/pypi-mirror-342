# LightMCP

A lightweight Python-based wrapper around MCP (Model Context Protocol) tools.

## Installation

```bash
pip install lightmcp
```

## Usage

```python
from lightmcp import add

# Load and start a Notion tasks query tool
tool = add("notion.query_tasks")
server_info = tool.run()

# Load and start a GitHub issues tool
github_tool = add("github.list_issues")
github_server = github_tool.run()

# When done, stop the servers
tool.stop()
github_tool.stop()
```

## Why LightMCP?

### Token and Latency Savings

Traditional MCP servers often bundle numerous tools, resources, and prompts that you may never use. This leads to:

- Increased token usage when communicating with LLMs
- Higher latency due to loading unnecessary components
- Larger memory footprint in your applications

LightMCP solves these problems by creating isolated micro-servers for each tool. You only instantiate and load the specific tools you need, resulting in:

- Reduced token consumption
- Lower latency for tool operations
- Minimal resource usage

### Focused Tool Architecture

Each tool in LightMCP is wrapped in a self-contained FastMCP server. This means:

- No bloat or extra load
- Only the exact functionality your agent needs
- Clean separation between tools

### Framework Compatibility

LightMCP is designed to work seamlessly with leading agent frameworks:

- LangGraph
- CrewAI
- Agno
- And more...

## CLI Usage

LightMCP includes a command-line interface for managing tools:

```bash
# Add a new tool to the registry
lightmcp add-tool "custom.tool" "path/to/tool.py"

# List all available tools
lightmcp list-tools

# Remove a tool from the registry
lightmcp remove-tool "custom.tool"
```

## Features

- One-line setup for MCP tools
- Zero unnecessary prompts/resources
- FastMCP-based isolated micro-servers
- Full compatibility with agent frameworks
- CLI for tool management

## License

MIT