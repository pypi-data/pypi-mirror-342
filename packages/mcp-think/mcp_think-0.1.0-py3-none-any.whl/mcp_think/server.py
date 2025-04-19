#!/usr/bin/env python3
"""MCP server implementation for the think tool."""

import sys
import datetime
import argparse
from typing import Any
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from mcp.server.sse import SseServerTransport
from starlette.requests import Request
from starlette.routing import Mount, Route
from mcp.server import Server
import uvicorn

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
        "--sse",
        action="store_true",
        help="Run the server with SSE transport rather than STDIO (default: False)",
    )
    parser.add_argument(
        "--host", default=None, help="Host to bind to (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port", type=int, default=None, help="Port to listen on (default: 3001)"
    )
    args = parser.parse_args()

    if not args.sse and (args.host or args.port):
        parser.error("Host and port arguments are only valid when using SSE transport.")
        sys.exit(1)

    print(f"Starting Think MCP Server...")
    
    if args.sse:
        starlette_app = create_starlette_app(mcp_server, debug=True)
        uvicorn.run(
            starlette_app,
            host=args.host if args.host else "127.0.0.1",
            port=args.port if args.port else 8000,
        )
    else:
        mcp.run()


if __name__ == "__main__":
    main()