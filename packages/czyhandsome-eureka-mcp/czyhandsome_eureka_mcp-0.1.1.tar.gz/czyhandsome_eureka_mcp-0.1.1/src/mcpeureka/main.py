"""Main entry point for MCP Eureka Server."""

from typing import Dict, Optional, Any

import requests
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Spring Cloud Eureka server discovery and management")


def get_mcp_version():
    """Return the MCP protocol version being used."""
    return "0.1.0"


@mcp.tool()
async def get_all_services(eureka_url: str, auth: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Get a list of all registered services from Eureka server.
    
    Args:
        eureka_url: URL of the Eureka server (e.g., http://localhost:8761)
        auth: Optional authentication dictionary containing 'username' and 'password'
    
    Returns:
        Dictionary containing all registered services
    """
    try:
        url = f"{eureka_url.rstrip('/')}/eureka/apps"
        headers = {"Accept": "application/json"}

        if auth:
            response = requests.get(url, headers=headers, auth=(auth.get("username", ""), auth.get("password", "")))
        else:
            response = requests.get(url, headers=headers)

        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def get_service_instances(eureka_url: str, app_id: str, auth: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Get all instances of a specific service from Eureka server.
    
    Args:
        eureka_url: URL of the Eureka server (e.g., http://localhost:8761)
        app_id: The application ID/name
        auth: Optional authentication dictionary containing 'username' and 'password'
    
    Returns:
        Dictionary containing service instances
    """
    try:
        url = f"{eureka_url.rstrip('/')}/eureka/apps/{app_id}"
        headers = {"Accept": "application/json"}

        if auth:
            response = requests.get(url, headers=headers, auth=(auth.get("username", ""), auth.get("password", "")))
        else:
            response = requests.get(url, headers=headers)

        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def get_instance_details(eureka_url: str, app_id: str, instance_id: str, auth: Optional[Dict[str, str]] = None) -> \
        Dict[str, Any]:
    """
    Get details of a specific instance from Eureka server.
    
    Args:
        eureka_url: URL of the Eureka server (e.g., http://localhost:8761)
        app_id: The application ID/name
        instance_id: The instance ID (hostname or EC2 instance ID)
        auth: Optional authentication dictionary containing 'username' and 'password'
    
    Returns:
        Dictionary containing instance details
    """
    try:
        url = f"{eureka_url.rstrip('/')}/eureka/apps/{app_id}/{instance_id}"
        headers = {"Accept": "application/json"}

        if auth:
            response = requests.get(url, headers=headers, auth=(auth.get("username", ""), auth.get("password", "")))
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
        auth: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Change the status of an instance in Eureka server.
    
    Args:
        eureka_url: URL of the Eureka server (e.g., http://localhost:8761)
        app_id: The application ID/name
        instance_id: The instance ID (hostname or EC2 instance ID)
        status: New status (UP, DOWN, OUT_OF_SERVICE, etc.)
        auth: Optional authentication dictionary containing 'username' and 'password'
    
    Returns:
        Dictionary with status change result
    """
    try:
        url = f"{eureka_url.rstrip('/')}/eureka/apps/{app_id}/{instance_id}/status?value={status}"

        if auth:
            response = requests.put(url, auth=(auth.get("username", ""), auth.get("password", "")))
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
        auth: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Get all instances registered with a specific VIP address.
    
    Args:
        eureka_url: URL of the Eureka server (e.g., http://localhost:8761)
        vip_address: The VIP address
        auth: Optional authentication dictionary containing 'username' and 'password'
    
    Returns:
        Dictionary containing instances with the specified VIP address
    """
    try:
        url = f"{eureka_url.rstrip('/')}/eureka/vips/{vip_address}"
        headers = {"Accept": "application/json"}

        if auth:
            response = requests.get(url, headers=headers, auth=(auth.get("username", ""), auth.get("password", "")))
        else:
            response = requests.get(url, headers=headers)

        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def main():
    """Run the MCP Eureka Server."""
    print(f"Starting MCP Eureka Server with protocol version {get_mcp_version()}")
    mcp.run()
    return 0


if __name__ == "__main__":
    exit(main())
