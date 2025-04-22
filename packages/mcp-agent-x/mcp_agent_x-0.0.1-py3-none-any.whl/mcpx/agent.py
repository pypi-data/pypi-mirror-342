"""
Extended MCP Agent implementation with additional tool introspection capabilities.
"""

import sys
from typing import Any

from langchain_core.messages import BaseMessage
from mcp_use import MCPAgent


class ExtendedMCPAgent(MCPAgent):
    """Extended MCP Agent with better tool introspection."""

    def __init__(
        self,
        llm,
        client=None,
        memory_enabled=True,
        system_prompt: str | None = None,
        max_steps: int = 10,
        **kwargs,
    ):
        """Initialize the extended MCP agent."""
        # Save parameters we'll need later
        self.system_prompt = system_prompt
        self._max_steps = max_steps

        # Initialize parent
        super().__init__(
            llm=llm, client=client, memory_enabled=memory_enabled, **kwargs
        )

        # Initialize internal state
        self._initialized = False
        self._tools_cache = {}
        self._tool_schemas_cache = {}

    async def ensure_initialized(self):
        """Make sure the agent is initialized. Safe to call multiple times."""
        if not self._initialized:
            await self.initialize()
            self._initialized = True

    async def initialize(self):
        """Initialize the MCP agent, connecting to servers and preparing tools."""
        try:
            # Call parent initialize
            await super().initialize()

            # Configure underlying agent if accessible
            if hasattr(self, "_agent") and self._agent is not None:
                self._agent.max_iterations = self._max_steps

            self._initialized = True

            # Pre-cache available tools if possible
            try:
                await self.get_available_tools(force_refresh=True)
            except Exception as e:
                print(f"Warning: Could not pre-cache tools: {e}", file=sys.stderr)
        except Exception as e:
            print(f"Error initializing agent: {e}", file=sys.stderr)
            import traceback

            print(traceback.format_exc(), file=sys.stderr)
            raise

    async def run(self, query: str, chat_history: list[BaseMessage] | None = None):
        """Run a query against the LLM with the given chat history."""
        # Ensure agent is initialized
        await self.ensure_initialized()

        # Validate the query
        if not query or not query.strip():
            raise ValueError("Cannot process empty query")

        # Validate chat history to avoid empty messages
        if chat_history:
            chat_history = [
                msg
                for msg in chat_history
                if hasattr(msg, "content") and msg.content and msg.content.strip()
            ]

        # Call parent run method
        try:
            return await super().run(query, chat_history)
        except Exception as e:
            print(f"Error in agent run: {str(e)}")
            raise

    async def get_available_tools(
        self, force_refresh: bool = False
    ) -> dict[str, list[str]]:
        """Get all available tools grouped by server."""
        # Ensure agent is initialized
        await self.ensure_initialized()

        # Return cached results if available and not forced to refresh
        if self._tools_cache and not force_refresh:
            return self._tools_cache

        # Create a new cache
        tools_by_server = {}

        # Access the client
        client = self.get_client()

        if client and hasattr(client, "servers"):
            # Iterate through all servers
            for server_name, server in client.servers.items():
                try:
                    # Try to access tools
                    tools = None
                    if hasattr(server, "tools") and server.tools:
                        tools = server.tools
                    elif hasattr(server, "_tools") and server._tools:
                        tools = server._tools

                    # If we found tools, add them to our result
                    if tools:
                        tools_by_server[server_name] = list(tools.keys())
                except Exception as e:
                    print(
                        f"Warning: Error accessing tools for server {server_name}: {e}",
                        file=sys.stderr,
                    )

        # Cache the results
        self._tools_cache = tools_by_server
        return tools_by_server

    async def get_tool_schema(
        self, server_name: str, tool_name: str
    ) -> dict[str, Any] | None:
        """Get the schema for a specific tool."""
        # Ensure agent is initialized
        await self.ensure_initialized()

        # Check cache first
        cache_key = f"{server_name}:{tool_name}"
        if cache_key in self._tool_schemas_cache:
            return self._tool_schemas_cache[cache_key]

        # Access the client
        client = self.get_client()

        # Try to get the tool schema
        schema = None
        if client and hasattr(client, "servers"):
            server = client.servers.get(server_name)
            if server:
                # Try different ways to access the tool and its schema
                if (
                    hasattr(server, "tools")
                    and server.tools
                    and tool_name in server.tools
                ):
                    tool = server.tools[tool_name]
                    if hasattr(tool, "schema"):
                        schema = tool.schema
                    elif hasattr(tool, "_schema"):
                        schema = tool._schema
                # Try alternative _tools attribute
                elif (
                    hasattr(server, "_tools")
                    and server._tools
                    and tool_name in server._tools
                ):
                    tool = server._tools[tool_name]
                    if hasattr(tool, "schema"):
                        schema = tool.schema
                    elif hasattr(tool, "_schema"):
                        schema = tool._schema

        # Cache the result
        self._tool_schemas_cache[cache_key] = schema
        return schema

    def get_client(self):
        """Get the MCP client instance, if available."""
        if hasattr(self, "_agent") and hasattr(self._agent, "client"):
            return self._agent.client
        return getattr(self, "client", None) or getattr(self, "_mcp_client_ref", None)

    async def close(self):
        """Close the agent and release resources."""
        # Clear caches
        self._tools_cache = {}
        self._tool_schemas_cache = {}
        self._initialized = False

        # Call parent close
        await super().close()
