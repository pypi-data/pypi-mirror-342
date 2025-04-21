"""This is a mcp server."""

import logging
from pathlib import Path

import click
from zmp_openapi_helper import MixedAPISpecConfig, ZmpAPIWrapper

from zmp_openapi_mcp_server.openapi_mcp_server import OpenAPIMCPServer

logger = logging.getLogger(__name__)


@click.command()
@click.option("--transport", type=click.Choice(["stdio", "sse"]), default="sse", help="Transport type",)
@click.option("--port", default=9999, help="Port to listen on for SSE")
@click.option("--server-name", type=str, required=True, help="Server name")
@click.option("--endpoint", type=str, required=True, help="Gateway endpoint for openapi")
@click.option("--auth-type", type=click.Choice(["Custom", "Bearer", "Basic", "None"]), default="Custom", help="Authentication type")
@click.option("--custom-auth-header-key", type=str, required=False, help="Custom auth header key. e.g. X-Access-Key")
@click.option("--custom-auth-header-value", type=str, required=False, help="Custom auth header value")
@click.option("--bearer-token", type=str, required=False, help="Bearer token")
@click.option("--basic-auth-username", type=str, required=False, help="Basic auth username")
@click.option("--basic-auth-password", type=str, required=False, help="Basic auth password")
@click.option("--timeout", type=int, required=False, default=30, help="Timeout")
@click.option("--tool-spec-base-path", type=click.Path(exists=True), required=True, help="Path to the tool spec base path",)
@click.option("--tool-spec-file-name", type=str, required=True, help="Tool spec file name")
@click.option("--backend-severs", type=str, required=False, help="Backend servers")
def main(
    transport: str,
    port: int,
    server_name: str,
    endpoint: str,
    auth_type: str,
    custom_auth_header_key: str,
    custom_auth_header_value: str,
    bearer_token: str,
    basic_auth_username: str,
    basic_auth_password: str,
    timeout: int,
    tool_spec_base_path: str,
    tool_spec_file_name: str,
    backend_severs: str,
):
    """Run the MCP server."""
    base_path = Path(tool_spec_base_path)
    tool_spec_file_path = base_path / tool_spec_file_name
    if not tool_spec_file_path.exists():
        raise ValueError(f"Tool spec file not found: {tool_spec_file_path}")

    try:
        mixed_api_spec_config = MixedAPISpecConfig.from_mixed_spec_file(
            file_path=tool_spec_file_path
        )
    except Exception as e:
        raise ValueError(f"Failed to load OpenAPI spec file: {e}")

    zmp_api_wrapper = ZmpAPIWrapper(
        endpoint,
        auth_type=auth_type,
        custom_auth_header_key=custom_auth_header_key,
        custom_auth_header_value=custom_auth_header_value,
        bearer_token=bearer_token,
        username=basic_auth_username,
        password=basic_auth_password,
        timeout=timeout,
        mixed_api_spec_config=mixed_api_spec_config,
    )

    zmp_mcp_server = OpenAPIMCPServer(
        name=server_name,
        transport_type=transport,
        port=port,
        zmp_openapi_helper=zmp_api_wrapper,
    )

    zmp_mcp_server.run()
    
    return 0
