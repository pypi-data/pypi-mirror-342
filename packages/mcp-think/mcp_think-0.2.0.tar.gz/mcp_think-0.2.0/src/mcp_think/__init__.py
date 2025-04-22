"""MCP Think - A Model Context Protocol server for the think tool."""

from .__about__ import __version__
from .server import main, think, mcp

__all__ = ["__version__", "main", "think", "mcp"]