import anyio
from typing import Any
import mcp.types as types
from mcp.server.lowlevel import Server

# Handle SSE transport directly without using asyncio.run()
import uvicorn
from uvicorn.config import Config

# Create Starlette app synchronously
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from mcp.server.stdio import stdio_server

def create_server(agent, name="mcp-simple-prompt"):
    """Create and return an MCP server instance."""
    app = Server(name)
    available_agents = [agent.agent_name]
    
    
    @app.call_tool()
    async def fetch_tool(
        name: str, arguments: dict
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        if name not in available_agents:
            raise ValueError(f"Tool '{name}' not found")
        if "user_input" not in arguments:
            raise ValueError("Missing required argument 'user_input'")
        response = agent.predict(**arguments)
        print(response)
        if response.get('chat_history') and isinstance(response['chat_history'], list):
            return [types.TextContent(type="text", text=response['chat_history'][-1].get('content'))]
        return NameError("No messages found in response")

    @app.list_tools()
    async def list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name=agent.agent_name,
                description=agent.description,
                inputSchema=agent.pydantic_model.schema()
            )
        ]
        
    return app


def run(agent: Any, server=None, transport="stdio", host='0.0.0.0', port=8000):
    """Run the MCP server."""
    app = server or create_server(agent, agent.agent_name)
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
        # Run with uvicorn directly
        config = Config(
            app=starlette_app,
            host=host,
            port=port,
            timeout_graceful_shutdown=5,
        )
        server = uvicorn.Server(config)
        server.run()
    elif transport == "stdio":
        async def arun():
            async with stdio_server() as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )
        anyio.run(arun)
    else:
        raise ValueError(f"Unsupported transport: {transport}")