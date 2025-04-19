# MCP Think

A Model Context Protocol (MCP) server implementing the "think" tool for improving Claude's and other LLMs' complex reasoning capabilities.

## Overview

This MCP server implements the "think" tool as described in Anthropic's [blog post](https://www.anthropic.com/engineering/claude-think-tool), which provides Claude with a dedicated space for structured thinking during complex problem-solving tasks. The think tool has been shown to significantly improve performance in complex tasks requiring policy adherence and reasoning in long chains of tool calls.

## Features

- **Structured Thinking Space**: Provides LLMs with a dedicated place to break down complex problems
- **Thought History**: Maintains a log of all thoughts with timestamps for reference
- **Multiple Transport Support**: Works with both stdio and SSE transports

## Installation

Install from PyPI:

```bash
pip install mcp-think
```

Or install from source:

```bash
git clone https://github.com/ddkang1/mcp-think.git
cd mcp-think
pip install -e .
```

## Usage

You can run the MCP server directly:

```bash
mcp-think
```

By default, it uses stdio transport. To use SSE transport:

```bash
mcp-think --sse
```

You can also specify host and port for SSE transport:

```bash
mcp-think --sse --host 127.0.0.1 --port 3001
```

## Configuration

To use this tool with Claude in Windsurf, add the following configuration to your MCP config file:

```json
"think": {
    "command": "/home/xxx/.local/bin/mcp-think",
    "args": [],
    "type": "stdio",
    "pollingInterval": 30000,
    "startupTimeout": 30000,
    "restartOnFailure": true
}
```

The `command` field should point to the directory where you installed the python package using pip.

## Available Tools

The MCP server provides the following tool:

- **think**: Record a thought with a timestamp

## Development

### Installation for Development

```bash
git clone https://github.com/ddkang1/mcp-think.git
cd mcp-think
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Style

This project uses Black for formatting, isort for import sorting, and flake8 for linting:

```bash
black src tests
isort src tests
flake8 src tests
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a history of changes to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.