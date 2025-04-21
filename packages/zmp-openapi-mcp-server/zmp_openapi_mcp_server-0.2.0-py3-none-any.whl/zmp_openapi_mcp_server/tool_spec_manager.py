"""Tool spec manager."""

# TODO: implement the tool spec manager
class ToolSpecManager:
    """Tool spec manager."""

    def __init__(
        self,
        tool_spec_base_path: str,
        mcp_server_name: str,
        backend_sever_names: list[str],
    ):
        """Initialize the tool spec manager."""
        self.tool_spec_base_path = tool_spec_base_path
        self.mcp_server_name = mcp_server_name
        self.backend_sever_names = backend_sever_names


