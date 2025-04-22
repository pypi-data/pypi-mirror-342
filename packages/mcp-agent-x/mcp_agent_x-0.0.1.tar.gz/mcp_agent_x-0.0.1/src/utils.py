"""
Utility functions for working with MCP.
"""

from typing import Any

from mcp_use import MCPClient


def extend_mcp_client():
    """
    Extend the MCPClient class with additional methods needed for our application.
    This should be called before using MCPClient.
    """
    # Only add the method if it doesn't already exist
    if not hasattr(MCPClient, "get_tools"):

        def get_tools(self) -> list[dict[str, Any]]:
            """
            Get all available tools from all registered MCP servers.

            Returns:
                List of tool definitions with server information added.
            """
            all_tools = []

            # Go through each server
            for server_name, server in self.servers.items():
                # Check if the server is connected and has tool definitions
                if hasattr(server, "tool_definitions") and server.tool_definitions:
                    # Add tools from this server with server name
                    for tool in server.tool_definitions:
                        # Create a copy of the tool and add server information
                        tool_copy = tool.copy()
                        tool_copy["server"] = server_name
                        all_tools.append(tool_copy)

            return all_tools

        # Add the method to the class
        MCPClient.get_tools = get_tools
