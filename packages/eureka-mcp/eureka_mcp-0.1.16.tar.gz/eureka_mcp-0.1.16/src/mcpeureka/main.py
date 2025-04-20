"""Main entry point for MCP Eureka Server."""

import logging
import sys
from typing import Dict, Optional, Any

import requests
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Spring Cloud Eureka server discovery and management")

__version__ = "0.1.16"

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    stream=sys.stderr)
logger = logging.getLogger("mcpeureka")


@mcp.tool()
async def just_get_version():
    """
    Get the version of the MCP protocol being used. currently: 0.1.15
    
    Returns:
        str: The version of the MCP protocol.
    """
    return __version__


@mcp.tool()
async def get_all_services(eureka_url: str, username: str, password: str) -> Dict[str, Any]:
    """
    Get a list of all registered services from Eureka server.
    
    Args:
        eureka_url: URL of the Eureka server (e.g., http://localhost:8761)
        username: username for authentication
        password: password for authentication
    
    Returns:
        Dictionary containing all registered services
    """
    try:
        url = f"{eureka_url.rstrip('/')}/eureka/apps"
        headers = {"Accept": "application/json"}

        if username and password:
            response = requests.get(url, headers=headers, auth=(username, password))
        else:
            response = requests.get(url, headers=headers)

        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def get_service_instances(eureka_url: str, app_id: str, username: str, password: str) -> Dict[str, Any]:
    """
    Get all instances of a specific service from Eureka server.
    
    Args:
        eureka_url: URL of the Eureka server (e.g., http://localhost:8761)
        app_id: The application ID/name
        username: username for authentication
        password: password for authentication
    
    Returns:
        Dictionary containing service instances
    """
    try:
        url = f"{eureka_url.rstrip('/')}/eureka/apps/{app_id}"
        headers = {"Accept": "application/json"}

        if username and password:
            response = requests.get(url, headers=headers, auth=(username, password))
        else:
            response = requests.get(url, headers=headers)

        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def get_instance_details(eureka_url: str, app_id: str, instance_id: str, username: str, password: str) -> \
        Dict[str, Any]:
    """
    Get details of a specific instance from Eureka server.
    
    Args:
        eureka_url: URL of the Eureka server (e.g., http://localhost:8761)
        app_id: The application ID/name
        instance_id: The instance ID (hostname or EC2 instance ID)
        username: username for authentication
        password: password for authentication
    
    Returns:
        Dictionary containing instance details
    """
    try:
        url = f"{eureka_url.rstrip('/')}/eureka/apps/{app_id}/{instance_id}"
        headers = {"Accept": "application/json"}

        if username and password:
            response = requests.get(url, headers=headers, auth=(username, password))
        else:
            response = requests.get(url, headers=headers)

        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def change_instance_status(
        eureka_url: str,
        app_id: str,
        instance_id: str,
        status: str,
        username: str,
        password: str,
) -> Dict[str, Any]:
    """
    Change the status of an instance in Eureka server.
    
    Args:
        eureka_url: URL of the Eureka server (e.g., http://localhost:8761)
        app_id: The application ID/name
        instance_id: The instance ID (hostname or EC2 instance ID)
        status: New status (UP, DOWN, OUT_OF_SERVICE, etc.)
        username: username for authentication
        password: password for authentication
    
    Returns:
        Dictionary with status change result
    """
    try:
        url = f"{eureka_url.rstrip('/')}/eureka/apps/{app_id}/{instance_id}/status?value={status}"

        if username and password:
            response = requests.put(url, auth=(username, password))
        else:
            response = requests.put(url)

        if response.status_code == 200:
            return {"status": "success", "message": f"Instance status changed to {status} successfully"}
        else:
            return {"status": "error", "message": f"Failed to change status: {response.text}",
                    "code": response.status_code}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_instances_by_vip(
        eureka_url: str,
        vip_address: str,
        username: Optional[str] = None,
        password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get all instances registered with a specific VIP address.
    
    Args:
        eureka_url: URL of the Eureka server (e.g., http://localhost:8761)
        vip_address: The VIP address
        username: username for authentication
        password: password for authentication
    
    Returns:
        Dictionary containing instances with the specified VIP address
    """
    try:
        url = f"{eureka_url.rstrip('/')}/eureka/vips/{vip_address}"
        headers = {"Accept": "application/json"}

        if username and password:
            response = requests.get(url, headers=headers, auth=(username, password))
        else:
            response = requests.get(url, headers=headers)

        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def main():
    """Run the MCP Description server when called directly."""
    print("Starting eureka MCP Server...")
    mcp.run()  # The FastMCP API doesn't accept host and port parameters


if __name__ == "__main__":
    main()
