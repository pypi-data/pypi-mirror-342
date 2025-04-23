"""Main entry point for MCP Nacos Config."""

import logging
import sys
from typing import Dict, Any

import nacos
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Nacos Config server discovery and management")

__version__ = "0.1.15"

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    stream=sys.stderr)
logger = logging.getLogger("mcpnacos_config")


@mcp.tool()
async def just_get_version():
    """
    Get the version of the MCP protocol being used. currently:0.1.14
    
    Returns:
        str: The version of the MCP protocol.
    """
    return __version__


@mcp.tool()
async def get_config(
        server_url: str,
        username: str,
        password: str,
        namespace_id: str,
        data_id: str,
        group: str,
) -> Dict[str, Any]:
    """
    Get configuration from Nacos server.
    
    Retrieves a single configuration item from Nacos server based on the provided
    data ID, group, and namespace.
    
    Args:
        server_url (str): URL of the Nacos server (e.g., http://localhost:8848)
        username (str): Username for authentication with Nacos server
        password (str): Password for authentication with Nacos server
        namespace_id (str): The namespace ID to fetch configuration from (use empty string for default namespace)
        data_id (str): The data ID of the configuration to retrieve
        group (str): The group of the configuration (default: DEFAULT_GROUP)
    
    Returns:
        Dict[str, Any]: Dictionary containing either:
            - On success: {"content": <configuration_content>, "status": 200}
            - On failure: {"error": "Configuration not found", "status": 404} or {"error": <exception_message>}
    """
    try:
        # Create Nacos client with namespace
        client = nacos.NacosClient(server_url, namespace=namespace_id, username=username, password=password)

        # Get config from Nacos
        content = client.get_config(data_id, group)

        if content is None:
            return {"error": "Configuration not found", "status": 404}

        return {"content": content, "status": 200}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def get_configs(
        server_url: str,
        username: str,
        password: str,
        namespace_id: str,
        group: str = None,
        page_no: int = 1,
        page_size: int = 10,
) -> Dict[str, Any]:
    """
    Get multiple configurations from Nacos server based on namespace and optional group.
    
    Args:
        server_url (str): URL of the Nacos server (e.g., http://localhost:8848)
        username (str): Username for authentication with Nacos server
        password (str): Password for authentication with Nacos server
        namespace_id (str): The namespace ID to fetch configurations from
        group (str, optional): The group of configurations to filter by. If None, 
                               returns configurations from all groups. Default is None.
        page_no (int, optional): Page number for pagination. Default is 1.
        page_size (int, optional): Number of configurations to return per page. Default is 1000.
    
    Returns:
        Dict[str, Any]: Dictionary containing either:
            - On success: {"content": <configuration_data>, "status": 200}
            - On failure: {"error": <error_message>, "status": 404} or {"error": <exception_message>}
    """
    try:
        # Create Nacos client with namespace
        client = nacos.NacosClient(server_url, namespace=namespace_id, username=username, password=password)

        # Get configs from Nacos with optional group filter
        args: dict[str, Any] = {
            "page_no": page_no,
            "page_size": page_size,
        }
        if group:
            args["group"] = group
        content = client.get_configs(**args)

        if content is None:
            return {"error": "Configuration not found", "status": 404}

        return {"content": content, "status": 200}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def publish_config(
        server_url: str,
        data_id: str,
        group: str,
        content: str,
        username: str,
        password: str,
        namespace_id: str = "",
        type: str = "text"
) -> Dict[str, Any]:
    """
    Publish (create or update) configuration to Nacos server.
    
    ⚠️ CAUTION: This operation will create a new configuration or overwrite
    an existing one. Use with caution as it may impact services using this configuration.
    
    Args:
        server_url: URL of the Nacos server (e.g., http://localhost:8848)
        data_id: The data ID of the configuration
        group: The group of the configuration
        content: The content of the configuration
        namespace_id: The namespace ID (default: empty string)
        username: Username for authentication
        password: Password for authentication
        type: Configuration type (default: text, can be: text, json, xml, yaml, html, properties)
    
    Returns:
        Dictionary with status of operation
    """
    try:
        # Create Nacos client with namespace
        client = nacos.NacosClient(server_url, namespace=namespace_id, username=username, password=password)

        # Set content type in metadata if specified
        if type and type != "text":
            # Set options to include content type in the request
            client.set_options(content_type=type)

        # Publish config to Nacos
        result = client.publish_config(data_id, group, content)

        if result:
            return {"success": True, "message": "Configuration published successfully"}
        else:
            return {"success": False, "message": "Failed to publish configuration"}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def remove_config(
        server_url: str,
        data_id: str,
        group: str,
        username: str,
        password: str,
        namespace_id: str = ""
) -> Dict[str, Any]:
    """
    Remove configuration from Nacos server.
    
    ⚠️ CAUTION: This operation will permanently delete the configuration.
    Use with extreme caution as it may impact services using this configuration.
    
    Args:
        server_url: URL of the Nacos server (e.g., http://localhost:8848)
        data_id: The data ID of the configuration
        group: The group of the configuration
        namespace_id: The namespace ID (default: empty string)
        username: Username for authentication
        password: Password for authentication
    
    Returns:
        Dictionary with status of operation
    """
    try:
        # Create Nacos client with namespace
        client = nacos.NacosClient(server_url, namespace=namespace_id, username=username, password=password)

        # Remove config from Nacos
        result = client.remove_config(data_id, group)

        if result:
            return {"success": True, "message": "Configuration removed successfully"}
        else:
            return {"success": False, "message": "Failed to remove configuration"}
    except Exception as e:
        return {"error": str(e)}


def main():
    """Run the MCP Nacos Config server when called directly."""
    print(f"Starting Nacos Config MCP Server for version {__version__}...")
    mcp.run()


if __name__ == "__main__":
    main()
