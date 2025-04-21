"""OpenAPI MCP Server."""

import logging
from enum import Enum
from typing import List

import anyio
import uvicorn
from mcp.server.lowlevel import Server
from mcp.server.sse import SseServerTransport
from mcp.server.stdio import stdio_server
from mcp.types import FileUrl, GetPromptResult, Prompt, Resource, TextContent, Tool
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from zmp_openapi_helper import ZmpAPIWrapper

logger = logging.getLogger(__name__)


class TransportType(str, Enum):
    """Transport type for MCP and Gateway."""

    SSE = "sse"
    STDIO = "stdio"


class OpenAPIMCPServer:
    """OpenAPI MCP Server."""

    def __init__(
        self,
        name: str = "zmp-openapi-mcp-server",
        transport_type: TransportType = TransportType.SSE,
        port: int = 9999,
        zmp_openapi_helper: ZmpAPIWrapper = None,
    ):
        """Initialize the server."""
        self.name = name
        self.port = port
        self.transport_type = transport_type
        self.zmp_openapi_helper = zmp_openapi_helper
        self.operations = (
            self.zmp_openapi_helper.get_operations() if zmp_openapi_helper else None
        )
        self.app = Server(self.name)
        self._initialize_app()

    def _initialize_app(self):
        """Initialize the app."""

        @self.app.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            """Call the tool with the given name and arguments from llm."""
            logger.debug("-" * 100)
            logger.debug(f"::: tool name: {name}")
            logger.debug("::: arguments:")
            for key, value in arguments.items():
                logger.debug(f"\t{key}: {value}")
            logger.debug("-" * 100)

            operation = next((op for op in self.operations if op.name == name), None)
            if operation is None:
                # raise ValueError(f"Unknown tool: {name}")
                logger.error(f"Unknown tool: {name}")
                return [TextContent(type="text", text=f"Error: Unknown tool: {name}")]

            path_params = (
                operation.path_params(**arguments) if operation.path_params else None
            )
            query_params = (
                operation.query_params(**arguments) if operation.query_params else None
            )
            request_body = (
                operation.request_body(**arguments) if operation.request_body else None
            )

            logger.debug(f"path_params: {path_params}")
            logger.debug(f"query_params: {query_params}")
            logger.debug(f"request_body: {request_body}")

            try:
                result = self.zmp_openapi_helper.run(
                    operation.method,
                    operation.path,
                    path_params=path_params,
                    query_params=query_params,
                    request_body=request_body,
                )

                return [TextContent(type="text", text=f"result: {result}")]
            except Exception as e:
                logger.error(f"Error: {e}")
                return [TextContent(type="text", text=f"Error: {e}")]

        @self.app.list_tools()
        async def list_tools() -> list[Tool]:
            """List all the tools available."""
            tools: List[Tool] = []
            for operation in self.operations:
                tool: Tool = Tool(
                    name=operation.name,
                    description=operation.description,
                    inputSchema=operation.args_schema.model_json_schema(),
                )
                tools.append(tool)

                logger.debug("-" * 100)
                logger.debug(f"::: tool: {tool.name}\n{tool.inputSchema}")

            return tools

        @self.app.list_prompts()
        async def list_prompts() -> list[Prompt]:
            """List all the prompts available."""
            prompts: List[Prompt] = []
            return prompts

        @self.app.get_prompt()
        async def get_prompt(
            name: str, arguments: dict[str, str] | None = None
        ) -> GetPromptResult:
            """Get the prompt with the given name and arguments."""
            return None

        @self.app.list_resources()
        async def list_resources() -> list[Resource]:
            """List all the resources available."""
            resources: List[Resource] = []
            return resources

        @self.app.read_resource()
        async def read_resource(uri: FileUrl) -> str | bytes:
            """Read the resource with the given URI."""
            return None

    def run(self):
        """Run the server."""
        if self.transport_type == TransportType.SSE:
            sse = SseServerTransport("/messages/")

            async def handle_sse(request):
                logger.info(f"::: SSE connection established - request: {request}")
                async with sse.connect_sse(
                    request.scope, request.receive, request._send
                ) as streams:
                    await self.app.run(
                        streams[0], streams[1], self.app.create_initialization_options()
                    )

            starlette_app = Starlette(
                debug=True,
                routes=[
                    Route("/sse", endpoint=handle_sse),
                    Mount("/messages/", app=sse.handle_post_message),
                ],
            )

            uvicorn.run(starlette_app, host="0.0.0.0", port=self.port)
        else:
            async def arun():
                async with stdio_server() as streams:
                    await self.app.run(
                        streams[0], streams[1], self.app.create_initialization_options()
                    )

            anyio.run(arun)
