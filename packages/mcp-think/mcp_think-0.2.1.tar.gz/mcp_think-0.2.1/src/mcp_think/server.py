#!/usr/bin/env python3
"""MCP server implementation for the think tool."""

import sys
import datetime
import argparse
import asyncio
from typing import Any
from contextlib import asynccontextmanager
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from mcp.server.sse import SseServerTransport
from starlette.requests import Request
from starlette.routing import Mount, Route
from mcp.server import Server
import uvicorn
import anyio
from anyio.streams.memory import MemoryObjectReceiveStream, MemoryObjectSendStream

# Initialize FastMCP server
mcp = FastMCP("think")

# Store the thoughts for logging purposes
thoughts_log = []

@mcp.tool()
async def think(thought: str) -> str:
    """Use the tool to think about something. It will not obtain new information or make any changes, but just log the thought. Use it when complex reasoning or brainstorming is needed. For example, if you explore the repo and discover the source of a bug, call this tool to brainstorm several unique ways of fixing the bug, and assess which change(s) are likely to be simplest and most effective. Alternatively, if you receive some test results, call this tool to brainstorm ways to fix the failing tests.

    Args:
        thought: Your thoughts.
    """
    # Log the thought with a timestamp
    timestamp = datetime.datetime.now().isoformat()
    thoughts_log.append({
        "timestamp": timestamp,
        "thought": thought
    })
    
    # Return a confirmation
    return thought

def create_starlette_app(mcp_server: Server, *, debug: bool = False) -> Starlette:
    """Create a Starlette application for SSE transport with persistent connections.
    
    Args:
        mcp_server: The MCP server instance
        debug: Whether to enable debug mode
        
    Returns:
        A Starlette application
    """
    # Use our enhanced persistent SSE transport
    sse = SseServerTransport("/messages/")

    async def handle_sse(request: Request) -> None:
        async with sse.connect_sse(
            request.scope,
            request.receive,
            request._send,
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )

    return Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )


def main():
    mcp_server = mcp._mcp_server

    parser = argparse.ArgumentParser(description="Run MCP Think server")

    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="sse",
        help="Transport protocol to use (stdio or sse, default: sse)",
    )
    parser.add_argument(
        "--host", default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="Port to listen on (default: 8000)"
    )
    args = parser.parse_args()

    if args.transport != "sse" and (args.host != "0.0.0.0" or args.port != 8000):
        parser.error("Host and port arguments are only valid when using SSE transport.")
        sys.exit(1)

    print(f"Starting Think MCP Server with {args.transport} transport...")
    
    if args.transport == "sse":
        starlette_app = create_starlette_app(mcp_server, debug=True)
        uvicorn.run(
            starlette_app,
            host=args.host,
            port=args.port,
            timeout_keep_alive=120,  # Increase keep-alive timeout (default is 5s)
            h11_max_incomplete_event_size=0,  # No limit on event size
        )
    else:
        mcp.run()


if __name__ == "__main__":
    main()