import argparse
import logging

from mcp.server.fastmcp import FastMCP

from .tools import instance_info, resource_info

# logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class MCPServerCloudSearch:
    def __init__(self):
        self.name = "MCPServerCloudSearch"
        self.mcp = FastMCP(self.name)
        self._register_tools()

    def _register_tools(self):
        """Register tools to the mcp server."""
        resource_info.register_tools(self.mcp)
        instance_info.register_tools(self.mcp)


def main():
    parser = argparse.ArgumentParser(description="Run the MCP Server CloudSearch")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["sse", "stdio"],
        default="stdio",
        help="Transport protocol to use (sse or stdio)",
    )
    args = parser.parse_args()

    logger.info("Starting MCP Server CloudSearch with %s transport", args.transport)
    server = MCPServerCloudSearch()
    server.mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()
