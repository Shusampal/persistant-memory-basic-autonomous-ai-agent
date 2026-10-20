from fastmcp import Client
from pathlib import Path


async def connect():
    """
    Connect to the MCP Server.
    """

    client = Client(Path("mcp_config/server.py"))

    await client.__aenter__()

    return client


async def disconnect(client):
    """
    Close the MCP connection.
    """

    await client.__aexit__(
        None,
        None,
        None
    )


async def discover_tools(client):
    """
    Retrieve all tools from the server.
    """

    tools = await client.list_tools()

    return tools


async def execute_tool(
    client,
    tool_name,
    arguments={}
):
    """
    Execute a tool.
    """

    result = await client.call_tool(
        tool_name,
        arguments
    )

    return str(result)
