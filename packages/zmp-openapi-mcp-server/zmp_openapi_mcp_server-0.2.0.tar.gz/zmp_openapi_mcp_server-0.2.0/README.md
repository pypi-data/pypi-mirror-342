# MCP Inspector CLI for lowlevel server
```bash
$ npx @modelcontextprotocol/inspector uv --directory /Users/kks/IdeaProjects/aiops/zmp-openapi-mcp-server run zmp-openapi-mcp-server --transport stdio --endpoint https://api.ags.cloudzcp.net --access-key xxx --spec-path /Users/kks/IdeaProjects/aiops/zmp-openapi-mcp-server/openapi/zmp_mixed_api_spec.json
```

# fastmcp cli command
```bash
$ mcp dev src/zmp_openapi_mcp_server/fastmcp/zcp_alert_manager.py
$ mcp run src/zmp_openapi_mcp_server/fastmcp/zcp_alert_manager.py -t sse
$ mcp install src/zmp_openapi_mcp_server/fastmcp/zcp_alert_manager.py --name alert-manager --with zmp-openapi-toolkit,pyyaml
```

# How to run the lowlevel.server
## sse
```bash
zmp-openapi-mcp-server --port 9999 --transport sse -e https://api.ags.cloudzcp.net -s xxx -p /Users/kks/IdeaProjects/aiops/zmp-openapi-mcp-server/openapi/zmp_mixed_api_spec.json
```

## stdio
first install the zmp-openapi-mcp-server
```bash
pip install zmp-openapi-mcp-server
```

then configure the mcp server into the mcp host like claude desktop or cursor
```json
{
  "mcpServers": {
    "zmp-openapi-mcp-server": {
      "command": "python3",
      "args": [
        "-m",
        "zmp_openapi_mcp_server",
        "--transport",
        "stdio",
        "--endpoint",
        "https://api.ags.cloudzcp.net",
        "--access-key",
        "xxxxx",
        "--spec-path",
        "/Users/kks/IdeaProjects/aiops/zmp-openapi-mcp-server/openapi/zmp_mixed_api_spec.json"
      ]
    }
  }
}
```


# backup the claude desktop mcp conf
```json
{
  "mcpServers": {
    "zmp-openapi-mcp-server": {
      "command": "python3",
      "args": [
        "-m",
        "zmp_openapi_mcp_server",
        "--transport",
        "stdio",
        "--endpoint",
        "https://api.ags.cloudzcp.net",
        "--access-key",
        "xxxx",
        "--spec-path",
        "/Users/kks/IdeaProjects/aiops/zmp-openapi-mcp-server/openapi/zmp_mixed_api_spec.json"
      ]
    },
    "tavily-mcp": {
      "command": "npx",
      "args": ["-y", "tavily-mcp@0.1.4"],
      "env": {
        "TAVILY_API_KEY": "xxxxx"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/kks/Desktop"
      ]
    }
  }
}
 ```