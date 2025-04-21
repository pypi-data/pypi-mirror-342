"""This is a container main."""

import logging
from pathlib import Path

from zmp_openapi_helper import MixedAPISpecConfig, ZmpAPIWrapper

from zmp_openapi_mcp_server.openapi_mcp_server import OpenAPIMCPServer
from zmp_openapi_mcp_server.setting import GatewaySettings, McpSettings

logger = logging.getLogger(__name__)

def run():
    """Run the MCP server."""
    mcp_settings = McpSettings()
    gateway_settings = GatewaySettings()

    backend_servers = gateway_settings.backend_severs_list
    for backend_server in backend_servers:
        logger.info(f"Processing backend server: {backend_server}")
        # TODO
        # 1st, get the openapi spec file from the persistent database
        # 2nd, save the openapi spec file to the local file system
        # 3rd, get the mixed api spec file from the persistent database
        # 4th, update the mixed api spec file with the openapi spec file path
        # 5th, save the mixed api spec file to the local file system

    # TODO: remove this after implementing the persistent database
    base_path = Path(mcp_settings.tool_spec_base_path)
    tool_spec_file_path = base_path / mcp_settings.tool_spec_file_name

    if not tool_spec_file_path.exists():
        raise ValueError(f"Tool spec file not found: {tool_spec_file_path}")

    try:
        mixed_api_spec_config = MixedAPISpecConfig.from_mixed_spec_file(
            file_path=tool_spec_file_path
        )
    except Exception as e:
        raise ValueError(f"Failed to load OpenAPI spec file: {e}")

    zmp_openapi_wrapper = ZmpAPIWrapper(
        gateway_settings.endpoint,
        auth_type=gateway_settings.auth_type,
        custom_auth_header_key=gateway_settings.custom_auth_header_key or None,
        custom_auth_header_value=gateway_settings.custom_auth_header_value or None,
        bearer_token=gateway_settings.bearer_token or None,
        username=gateway_settings.basic_auth_username or None,
        password=gateway_settings.basic_auth_password or None,
        timeout=gateway_settings.timeout,
        mixed_api_spec_config=mixed_api_spec_config,
    )

    zmp_mcp_server = OpenAPIMCPServer(
        transport_type=mcp_settings.transport_type,
        name=mcp_settings.server_name,
        port=mcp_settings.port,
        zmp_openapi_helper=zmp_openapi_wrapper,
    )

    zmp_mcp_server.run()


if __name__ == "__main__":
    run()
