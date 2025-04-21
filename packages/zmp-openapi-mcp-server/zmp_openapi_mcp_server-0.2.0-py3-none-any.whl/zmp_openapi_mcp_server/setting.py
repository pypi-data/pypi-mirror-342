"""Base settings for MCP and Gateway."""


from pydantic_settings import BaseSettings, SettingsConfigDict
from zmp_openapi_helper import AuthenticationType

from zmp_openapi_mcp_server.openapi_mcp_server import TransportType


class McpSettings(BaseSettings):
    """Settings for MCP."""

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_prefix="MCP_", env_file=".env", extra="allow"
    )
    transport_type: TransportType = TransportType.SSE
    port: int
    server_name: str
    tool_spec_base_path: str
    tool_spec_file_name: str
class GatewaySettings(BaseSettings):
    """Settings for Gateway."""

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_prefix="GW_", env_file=".env", extra="allow"
    )
    endpoint: str
    auth_type: AuthenticationType
    custom_auth_header_key: str | None = None
    custom_auth_header_value: str | None = None
    bearer_token: str | None = None
    basic_auth_username: str | None = None
    basic_auth_password: str | None = None
    timeout: int = 30
    backend_sever_names: str

    @property
    def backend_severs_list(self) -> list[str]:
        """Split the backend_sever_names string by comma and strip whitespace."""
        if self.backend_sever_names is None:
            raise ValueError("backend_sever_names is empty")
        return [sever.strip() for sever in self.backend_sever_names.split(",")]
