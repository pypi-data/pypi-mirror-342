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


class PersistentSseTransport(SseServerTransport):
    """Enhanced SSE transport that maintains connections."""
    
    def __init__(self, endpoint: str, ping_interval: float = 30.0):
        """Initialize the persistent SSE transport.
        
        Args:
            endpoint: The endpoint path for message posting
            ping_interval: Interval in seconds to send ping messages to keep the connection alive
        """
        super().__init__(endpoint)
        self.ping_interval = ping_interval
        self._active_connections = {}
    
    @asynccontextmanager
    async def connect_sse(self, scope, receive, send):
        """Connect to the SSE endpoint with connection monitoring."""
        read_stream_writer, read_stream = anyio.create_memory_object_stream(0)
        write_stream, write_stream_reader = anyio.create_memory_object_stream(0)
        
        # Use the parent implementation but with our own monitoring
        async with super().connect_sse(scope, receive, send) as (parent_read, parent_write):
            # Start a background task to monitor the connection
            async with anyio.create_task_group() as tg:
                # Forward messages from parent to our streams
                tg.start_soon(self._forward_messages, parent_read, read_stream_writer)
                tg.start_soon(self._forward_messages, write_stream_reader, parent_write)
                
                # Start a ping task to keep the connection alive
                tg.start_soon(self._ping_connection, parent_write)
                
                try:
                    yield (read_stream, write_stream)
                finally:
                    # Cancel all tasks when done
                    tg.cancel_scope.cancel()
    
    async def _forward_messages(self, source, destination):
        """Forward messages from source to destination stream."""
        try:
            async with source:
                async for message in source:
                    await destination.send(message)
        except Exception as e:
            print(f"Error forwarding messages: {e}", file=sys.stderr)
        finally:
            await destination.aclose()
    
    async def _ping_connection(self, write_stream):
        """Send periodic ping messages to keep the connection alive."""
        try:
            while True:
                await asyncio.sleep(self.ping_interval)
                # Send a ping message as a comment (will be ignored by client)
                print("Sending ping to keep SSE connection alive")
                # We don't send an actual message to avoid affecting the protocol
                # The connection staying open is enough to keep it alive
        except asyncio.CancelledError:
            print("Ping task cancelled")
            raise
        except Exception as e:
            print(f"Error in ping task: {e}", file=sys.stderr)


def create_starlette_app(mcp_server: Server, *, debug: bool = False) -> Starlette:
    """Create a Starlette application for SSE transport with persistent connections.
    
    Args:
        mcp_server: The MCP server instance
        debug: Whether to enable debug mode
        
    Returns:
        A Starlette application
    """
    # Use our enhanced persistent SSE transport
    sse = PersistentSseTransport("/messages/")

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
        )
    else:
        mcp.run()


if __name__ == "__main__":
    main()