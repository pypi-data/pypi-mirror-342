"""
ECS MCP Server.

This server provides MCP tools to interact with ECS OpenAPI.
"""

import argparse
import traceback

import anyio
import uvicorn
from mcp import types
from mcp.server.lowlevel import Server
from mcp.server.sse import SseServerTransport
from mcp.server.stdio import stdio_server
from starlette.applications import Starlette
from starlette.routing import Mount, Route

from .common.logs import LOG
from .tools import TOOL_REGISTRY, event, get_tool_function, instance, is_tool_registered, region


app = Server("ecs")


@app.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name=info["name"],
            description=info["description"],
            inputSchema=info["model"].model_json_schema(),
        )
        for info in TOOL_REGISTRY.values()
    ]


@app.call_tool()
async def call_tool(name: str, args: dict) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    if not is_tool_registered(name):
        return [types.TextContent(
            type="text",
            text="Tool not found"
        )]

    try:
        tool_info = TOOL_REGISTRY[name]
        model_class = tool_info["model"]

        try:
            validated_args = model_class(**args)
            LOG.info(f"Validated args: {validated_args.model_dump()}")
        except Exception as e:
            LOG.error(f"Parameter validation error: {str(e)}")
            return [types.TextContent(
                type="text",
                text=f"Parameter validation error: {str(e)}"
            )]

        tool_function = get_tool_function(name)
        result = await tool_function(validated_args.model_dump())
        return result

    except Exception as e:
        LOG.error(f"Exception: {traceback.format_exc()}")
        return [types.TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]


def serve(transport: str):
    if transport == "sse":
        sse = SseServerTransport("/messages/")

        async def handle_sse(request):
            async with sse.connect_sse(
                request.scope, request.receive, request._send
            ) as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )

        starlette_app = Starlette(
            debug=True,
            routes=[
                Route("/sse", endpoint=handle_sse),
                Mount("/messages/", app=sse.handle_post_message),
            ],
        )

        uvicorn.run(starlette_app, host="0.0.0.0", port=8000)

    else:
        async def arun():
            async with stdio_server() as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )

        anyio.run(arun)


def main():
    parser = argparse.ArgumentParser(description="Run the ECS MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["sse", "stdio"],
        default="stdio",
        help="Transport protocol to use (sse or stdio)",
    )

    args = parser.parse_args()
    LOG.info(f"Starting ECS MCP Server with {args.transport} transport")

    serve(args.transport)


if __name__ == "__main__":
    main()
