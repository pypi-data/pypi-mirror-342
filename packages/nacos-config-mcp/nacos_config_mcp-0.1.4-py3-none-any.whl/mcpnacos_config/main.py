"""Main entry point for MCP Nacos Config."""

import logging
import sys
from typing import Dict, Any, Optional, List

import requests
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Nacos Config server discovery and management")

__version__ = "0.1.4"

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    stream=sys.stderr)
logger = logging.getLogger("mcpnacos_config")


@mcp.tool()
async def just_get_version():
    """
    Get the version of the MCP protocol being used. currently:0.1.4
    
    Returns:
        str: The version of the MCP protocol.
    """
    return __version__


@mcp.tool()
async def list_namespaces(server_url: str, username: Optional[str] = None, password: Optional[str] = None) -> Dict[str, Any]:
    """
    List all namespaces in the Nacos server.
    
    Args:
        server_url: URL of the Nacos server (e.g., http://localhost:8848)
        username: Username for authentication (optional)
        password: Password for authentication (optional)
    
    Returns:
        Dictionary containing the list of namespaces
    """
    try:
        url = f"{server_url.rstrip('/')}/nacos/v1/console/namespaces"
        
        if username and password:
            response = requests.get(url, auth=(username, password))
        else:
            response = requests.get(url)
        
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def get_config(
    server_url: str, 
    data_id: str,
    group: str = "DEFAULT_GROUP",
    namespace_id: str = "",
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get configuration from Nacos server.
    
    Args:
        server_url: URL of the Nacos server (e.g., http://localhost:8848)
        data_id: The data ID of the configuration
        group: The group of the configuration (default: DEFAULT_GROUP)
        namespace_id: The namespace ID (optional)
        username: Username for authentication (optional)
        password: Password for authentication (optional)
    
    Returns:
        Dictionary containing the configuration content or error
    """
    try:
        url = f"{server_url.rstrip('/')}/nacos/v1/cs/configs"
        params = {
            "dataId": data_id,
            "group": group,
        }
        
        if namespace_id:
            params["tenant"] = namespace_id
        
        if username and password:
            response = requests.get(url, params=params, auth=(username, password))
        else:
            response = requests.get(url, params=params)
        
        if response.status_code == 404:
            return {"error": "Configuration not found", "status": 404}
        
        response.raise_for_status()
        return {"content": response.text, "status": response.status_code}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def publish_config(
    server_url: str, 
    data_id: str,
    group: str,
    content: str,
    namespace_id: str = "",
    username: Optional[str] = None,
    password: Optional[str] = None,
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
        namespace_id: The namespace ID (optional)
        username: Username for authentication (optional)
        password: Password for authentication (optional)
        type: Configuration type (default: text, can be: text, json, xml, yaml, html, properties)
    
    Returns:
        Dictionary with status of operation
    """
    try:
        url = f"{server_url.rstrip('/')}/nacos/v1/cs/configs"
        data = {
            "dataId": data_id,
            "group": group,
            "content": content,
            "type": type
        }
        
        if namespace_id:
            data["tenant"] = namespace_id
        
        if username and password:
            response = requests.post(url, data=data, auth=(username, password))
        else:
            response = requests.post(url, data=data)
        
        response.raise_for_status()
        
        # Nacos returns "true" or "false" as a string
        if response.text.lower() == "true":
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
    namespace_id: str = "",
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Remove configuration from Nacos server.
    
    ⚠️ CAUTION: This operation will permanently delete the configuration.
    Use with extreme caution as it may impact services using this configuration.
    
    Args:
        server_url: URL of the Nacos server (e.g., http://localhost:8848)
        data_id: The data ID of the configuration
        group: The group of the configuration
        namespace_id: The namespace ID (optional)
        username: Username for authentication (optional)
        password: Password for authentication (optional)
    
    Returns:
        Dictionary with status of operation
    """
    try:
        url = f"{server_url.rstrip('/')}/nacos/v1/cs/configs"
        params = {
            "dataId": data_id,
            "group": group,
        }
        
        if namespace_id:
            params["tenant"] = namespace_id
        
        if username and password:
            response = requests.delete(url, params=params, auth=(username, password))
        else:
            response = requests.delete(url, params=params)
        
        response.raise_for_status()
        
        # Nacos returns "true" or "false" as a string
        if response.text.lower() == "true":
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