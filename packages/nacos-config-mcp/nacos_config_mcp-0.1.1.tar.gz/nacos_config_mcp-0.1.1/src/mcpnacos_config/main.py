"""Main entry point for MCP Nacos Config."""

import logging
import sys
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Nacos Config server discovery and management")

__version__ = "0.1.1"

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    stream=sys.stderr)
logger = logging.getLogger("mcpnacos_config")


@mcp.tool()
async def just_get_version():
    """
    Get the version of the MCP protocol being used. currently:0.1.1
    
    Returns:
        str: The version of the MCP protocol.
    """
    return __version__


def main():
    """Run the MCP Nacos Config server when called directly."""
    print("Starting Nacos Config MCP Server...")
    mcp.run()


if __name__ == "__main__":
    main() 