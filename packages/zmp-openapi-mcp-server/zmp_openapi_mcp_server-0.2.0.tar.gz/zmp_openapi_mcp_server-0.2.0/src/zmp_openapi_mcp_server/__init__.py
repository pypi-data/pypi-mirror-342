"""This is the MCP server for the ZMP OpenAPI."""

import logging
import logging.config

# for stdio
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S",
#     handlers=[logging.StreamHandler()],
# )

# for sse
logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

logging.getLogger("httpcore.http11").setLevel(logging.INFO)
logging.getLogger("zmp_openapi_helper.openapi.zmpapi_models").setLevel(logging.INFO)
logging.getLogger("zmp_openapi_toolkit.toolkits.toolkit").setLevel(logging.INFO)
logging.getLogger("zmp_openapi_mcp_server.openapi_mcp_server").setLevel(logging.DEBUG)
