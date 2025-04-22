import signal
import sys
from datetime import datetime

from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from mcp_use import MCPAgent
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import FileHistory
from rich.box import DOUBLE
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

from mcpx.config import CONFIG_FILE, HISTORY_FILE, load_history, save_history

# ASCII art logo for the welcome screen
MCPX_LOGO = """
"""


class ToolUsageCallbackHandler(BaseCallbackHandler):
    """Callback handler for streaming tool usage in real-time."""

    def __init__(self, console):
        """Initialize with a Rich console."""
        self.console = console
        self.current_tool = None
        self.tool_count = 0
        self.verbose = True  # Can be toggled on/off

    def on_tool_start(self, serialized, input_str, **kwargs):
        """Called when a tool starts running."""
        self.tool_count += 1
        tool_name = serialized.get("name", "unknown_tool")
        self.current_tool = tool_name

        # Format the input more nicely
        truncated_input = input_str
        if len(input_str) > 60:
            truncated_input = input_str[:57] + "..."

        # Show tool usage with count
        self.console.print(
            f"[dim cyan]> Tool #{self.tool_count}: [bold]{tool_name}[/bold][/dim cyan]"
        )
        self.console.print(f"[dim]  Input: {truncated_input}[/dim]")

    def on_tool_end(self, output, **kwargs):
        """Called when a tool ends running."""
        if self.current_tool:
            # Format output - show a condensed version
            if isinstance(output, str) and len(output) > 60:
                preview = output[:57] + "..."
                self.console.print(f"[dim green]  Result: {preview}[/dim green]")
            elif output:
                self.console.print("[dim green]  Completed[/dim green]")
            else:
                self.console.print("[dim yellow]  No output[/dim yellow]")

            self.current_tool = None

    def on_tool_error(self, error, **kwargs):
        """Called when a tool errors."""
        if self.current_tool:
            error_msg = str(error)
            if len(error_msg) > 60:
                error_msg = error_msg[:57] + "..."
            self.console.print(f"[dim red]  Error: {error_msg}[/dim red]")
            self.current_tool = None

    def on_chain_start(self, serialized, inputs, **kwargs):
        """Log chain starts."""
        if not self.verbose:
            return

        if "name" in serialized:
            chain_name = serialized["name"]
            if "agent" in chain_name.lower():
                self.console.print("[dim]Starting agent reasoning process...[/dim]")

    def on_chain_end(self, outputs, **kwargs):
        """Log chain ends."""
        if self.tool_count > 0:
            self.console.print(
                f"[dim]Agent used {self.tool_count} tools to answer[/dim]"
            )
            self.tool_count = 0

    def on_agent_action(self, action, **kwargs):
        """Called when agent decides on an action."""
        if not self.verbose:
            return

        try:
            # Try to extract and show the agent's reasoning
            if hasattr(action, "log"):
                thought = action.log
                if thought and len(thought) > 10:
                    # Show a brief version of the agent's thought process
                    preview = thought[:80] + "..." if len(thought) > 80 else thought
                    self.console.print(f"[dim]Reasoning: {preview}[/dim]")
        except Exception:
            # Silently ignore any errors in the callback
            pass

    def on_llm_start(self, serialized, prompts, **kwargs):
        """Called when an LLM starts processing."""
        if not self.verbose:
            return

        if "name" in serialized and self.tool_count == 0:
            # Only show this for the first LLM call, not subsequent ones
            self.console.print("[dim]Thinking...[/dim]")

    def on_llm_end(self, response, **kwargs):
        """Called when an LLM finishes processing."""
        # No output needed here to avoid cluttering the display


class ChatCommandCompleter(Completer):
    """Completer for chat commands."""

    def __init__(self):
        """Initialize the completer with available commands."""
        self.commands = [
            "/clear",  # Clear conversation history
            "/help",  # Show help information
            "/tools",  # List available MCP tools
            "/fix",  # Fix corrupted conversation history
            "/init",  # Re-initialize agent
        ]

    def get_completions(self, document, complete_event):
        """Get completions for the current document."""
        # Only complete at the start of the line
        text = document.text
        if text.startswith("/"):
            for command in self.commands:
                if command.startswith(text):
                    yield Completion(
                        command,
                        start_position=-len(text),
                        display=command,
                        display_meta="Chat command",
                    )


class AgentREPL:
    def __init__(
        self, agent: MCPAgent, system_prompt: str = None, session_id: str = "default"
    ):
        self.agent = agent
        self.system_prompt = system_prompt
        self.console = Console()
        self.session_id = session_id

        # Set up file-based history for persistent command history
        self.history = FileHistory(
            str(HISTORY_FILE.parent / f"{session_id}_commands.txt")
        )

        # Create command completer
        self.command_completer = ChatCommandCompleter()

        # Create session with history and autocomplete
        self.session = PromptSession(
            history=self.history,
            completer=self.command_completer,
            auto_suggest=AutoSuggestFromHistory(),
            complete_while_typing=True,
        )

        # Set system prompt if provided
        if system_prompt:
            self.agent.set_system_message(system_prompt)

        # Set up signal handler for graceful exit
        signal.signal(signal.SIGINT, self._signal_handler)

        # Load previous messages if available
        self.messages = []
        self._load_conversation()

    def _signal_handler(self, sig, frame):
        self._save_conversation()  # Save before exiting
        self.console.print("\n[bold red]Exiting agent session...[/bold red]")
        sys.exit(0)

    def _get_tools_count(self):
        """Get a count of available tools."""
        try:
            tools = []

            # Try different paths to access the tools
            if hasattr(self.agent, "get_tools"):
                tools = self.agent.get_tools()
            elif hasattr(self.agent._agent, "tools"):
                tools = self.agent._agent.tools
            elif hasattr(self.agent._agent, "_tools"):
                tools = self.agent._agent._tools

            return len(tools)
        except Exception:
            return "?"

    def _get_enabled_servers(self):
        """Get a list of enabled MCP servers."""
        try:
            # Try to access the servers from the agent
            if hasattr(self.agent, "_client") and hasattr(
                self.agent._client, "servers"
            ):
                return list(self.agent._client.servers.keys())
            elif (
                hasattr(self.agent, "_agent")
                and hasattr(self.agent._agent, "client")
                and hasattr(self.agent._agent.client, "servers")
            ):
                return list(self.agent._agent.client.servers.keys())
            else:
                # Fall back to the default Playwright server if we can't get the actual list
                return ["playwright"]
        except Exception:
            return ["unknown"]

    def _display_welcome(self):
        """Display a BBS-style welcome screen."""
        # Clear the screen for a clean start
        self.console.clear()

        # Print the logo
        # self.console.print(f"[bold magenta]{MCPX_LOGO}[/bold magenta]")

        # Current timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Create main info table
        table = Table(box=DOUBLE, expand=False, show_header=False)
        table.add_column("Item", style="cyan")
        table.add_column("Value", style="green")

        # Add system info
        table.add_row("System Time", current_time)
        table.add_row("Session ID", self.session_id)
        table.add_row("Config Path", str(CONFIG_FILE))

        # Get the number of previous messages
        message_count = len(self.messages) // 2 if self.messages else 0
        table.add_row("History", f"{message_count} previous messages")

        # Add enabled servers and tools info
        servers = self._get_enabled_servers()
        tool_count = self._get_tools_count()

        table.add_row("Enabled Servers", ", ".join(servers))
        table.add_row("Available Tools", str(tool_count))

        # Display the info panel
        self.console.print(
            Panel(
                table,
                title="[bold yellow]MCPx Agent Terminal[/bold yellow]",
                subtitle="[italic]Model Context Protocol Agent Interface[/italic]",
            )
        )

        # Show minimal command help as a single line
        self.console.print(
            "[dim]Commands: [/dim][cyan]/help[/cyan] [dim]|[/dim] [cyan]/tools[/cyan] [dim]|[/dim] [cyan]clear[/cyan] [dim]|[/dim] [cyan]/fix[/cyan] [dim]|[/dim] [cyan]exit[/cyan]"
        )

        # Show message if history was loaded
        if self.messages and len(self.messages) > 1:
            self.console.print(
                f"[dim]Loaded {message_count} messages from previous conversation[/dim]"
            )

        # Final separator before starting the conversation
        self.console.print("[dim]" + "─" * self.console.width + "[/dim]")

    def _load_conversation(self):
        """Load conversation history from persistent storage."""
        try:
            history_data = load_history()
            conversations = history_data.get("conversations", {})

            # Clear any existing messages
            self.messages = []

            # Handle both dictionary and list formats for backward compatibility
            if isinstance(conversations, dict) and self.session_id in conversations:
                # Convert the loaded messages back to appropriate message types
                loaded_msgs = conversations[self.session_id]

                for msg in loaded_msgs:
                    # Skip messages with empty content
                    if not msg.get("content") or not msg.get("content").strip():
                        continue

                    if msg["type"] == "system":
                        self.messages.append(SystemMessage(content=msg["content"]))
                    elif msg["type"] == "human":
                        self.messages.append(HumanMessage(content=msg["content"]))
                    elif msg["type"] == "ai":
                        self.messages.append(AIMessage(content=msg["content"]))
            elif isinstance(conversations, list) and len(conversations) > 0:
                # Legacy format - initialize with the first conversation
                for msg in conversations:
                    # Skip messages with empty content
                    if not msg.get("content") or not msg.get("content").strip():
                        continue

                    if msg["type"] == "system":
                        self.messages.append(SystemMessage(content=msg["content"]))
                    elif msg["type"] == "human":
                        self.messages.append(HumanMessage(content=msg["content"]))
                    elif msg["type"] == "ai":
                        self.messages.append(AIMessage(content=msg["content"]))

            # If no messages or only system, add system message
            if not self.messages and self.system_prompt:
                self.messages.append(SystemMessage(content=self.system_prompt))
        except Exception:
            # Initialize with system message only
            self.messages = []
            if self.system_prompt:
                self.messages.append(SystemMessage(content=self.system_prompt))

    def _save_conversation(self):
        """Save conversation history to persistent storage."""
        try:
            # Convert messages to serializable format
            serialized_msgs = []
            for msg in self.messages:
                # Skip messages with empty content
                if (
                    not hasattr(msg, "content")
                    or not msg.content
                    or not msg.content.strip()
                ):
                    continue

                if isinstance(msg, SystemMessage):
                    serialized_msgs.append({"type": "system", "content": msg.content})
                elif isinstance(msg, HumanMessage):
                    serialized_msgs.append({"type": "human", "content": msg.content})
                elif isinstance(msg, AIMessage):
                    serialized_msgs.append({"type": "ai", "content": msg.content})

            # Load existing history, update it, and save
            history_data = load_history()

            # Ensure conversations is a dictionary
            if "conversations" not in history_data or not isinstance(
                history_data["conversations"], dict
            ):
                history_data["conversations"] = {}

            # Save the current conversation
            history_data["conversations"][self.session_id] = serialized_msgs
            save_history(history_data)
        except Exception as e:
            self.console.print(
                f"[yellow]Warning: Could not save conversation history: {e}[/yellow]"
            )
            import traceback

            self.console.print(f"[dim]{traceback.format_exc()}[/dim]")

    def _clear_conversation(self):
        """Clear the current conversation history, keeping only the system message."""
        # Store the system message if it exists
        system_message = None
        for msg in self.messages:
            if isinstance(msg, SystemMessage):
                system_message = msg
                break

        # Clear messages and add back system message if it exists
        self.messages = []
        if system_message:
            self.messages.append(system_message)

        # Save the cleared conversation
        self._save_conversation()

        # Show success message in minimal style
        self.console.print("[green]Conversation history cleared[/green]")

    def _show_help(self):
        """Show help information about available commands."""
        self.console.print("[bold]Available Commands:[/bold]")
        self.console.print()
        self.console.print(
            "  [cyan]clear[/cyan], [cyan]cls[/cyan]   - Clear the screen (preserves conversation)"
        )
        self.console.print("  [cyan]/clear[/cyan]       - Clear conversation history")
        self.console.print("  [cyan]/help[/cyan]        - Show this help information")
        self.console.print("  [cyan]/tools[/cyan]       - List available MCP tools")
        self.console.print(
            "  [cyan]/fix[/cyan]         - Fix corrupted conversation history"
        )
        self.console.print(
            "  [cyan]/init[/cyan]        - Re-initialize the agent and MCP servers"
        )
        self.console.print(
            "  [cyan]exit[/cyan], [cyan]quit[/cyan]  - Exit the application"
        )

        # Show detailed help for specific commands
        if hasattr(self.agent, "initialize") and callable(self.agent.initialize):
            self.console.print()
            self.console.print("[bold yellow]Command Details:[/bold yellow]")
            self.console.print(
                "[cyan]/init[/cyan] - Reconnects to MCP servers and refreshes available tools."
            )
            self.console.print(
                "        Use this if tools stop working or if you've started new MCP servers."
            )

    def _list_tools(self):
        """List all available MCP tools from the agent."""
        self.console.print("[bold]Scanning for tools...[/bold]")

        try:
            # Check if agent is initialized
            if not hasattr(self.agent, "_agent") or not self.agent._agent:
                self.console.print("[yellow]Agent not properly initialized[/yellow]")
                self.console.print(
                    "See error messages above for troubleshooting steps."
                )
                return

            # Try to access tools through different potential paths
            tools = []
            tool_access_method = None

            # Option 1: Check if the agent has a get_tools method
            if hasattr(self.agent, "get_tools"):
                try:
                    tools = self.agent.get_tools()
                    tool_access_method = "agent.get_tools()"
                except Exception as e:
                    self.console.print(
                        f"[yellow]Tried agent.get_tools() but: {str(e)}[/yellow]"
                    )

            # Option 2: Check if _agent.tools exists (LangChain structure)
            if not tools and hasattr(self.agent._agent, "tools"):
                tools = self.agent._agent.tools
                tool_access_method = "agent._agent.tools"

            # Option 3: Check for _tools attribute
            if not tools and hasattr(self.agent._agent, "_tools"):
                tools = self.agent._agent._tools
                tool_access_method = "agent._agent._tools"

            # Option 4: Check if client exists and has get_tools method
            if (
                not tools
                and hasattr(self.agent._agent, "client")
                and hasattr(self.agent._agent.client, "get_tools")
            ):
                try:
                    tools = self.agent._agent.client.get_tools()
                    tool_access_method = "agent._agent.client.get_tools()"
                except Exception as e:
                    self.console.print(
                        f"[yellow]Tried agent._agent.client.get_tools() but: {str(e)}[/yellow]"
                    )

            # Option 5: Check for client attribute at agent level
            if (
                not tools
                and hasattr(self.agent, "client")
                and hasattr(self.agent.client, "get_tools")
            ):
                try:
                    tools = self.agent.client.get_tools()
                    tool_access_method = "agent.client.get_tools()"
                except Exception as e:
                    self.console.print(
                        f"[yellow]Tried agent.client.get_tools() but: {str(e)}[/yellow]"
                    )

            # Option 6: Look for _client attribute
            if (
                not tools
                and hasattr(self.agent, "_client")
                and hasattr(self.agent._client, "get_tools")
            ):
                try:
                    tools = self.agent._client.get_tools()
                    tool_access_method = "agent._client.get_tools()"
                except Exception as e:
                    self.console.print(
                        f"[yellow]Tried agent._client.get_tools() but: {str(e)}[/yellow]"
                    )

            # Option 7: Check if _agent itself might be an agent with tools
            if not tools and hasattr(self.agent._agent, "get_tools"):
                try:
                    tools = self.agent._agent.get_tools()
                    tool_access_method = "agent._agent.get_tools()"
                except Exception as e:
                    self.console.print(
                        f"[yellow]Tried agent._agent.get_tools() but: {str(e)}[/yellow]"
                    )

            if not tools:
                # If we couldn't get tools directly
                self.console.print(
                    "[yellow]No tools found. Try asking 'what tools do you have access to?'[/yellow]"
                )
                return

            # Process tools
            tool_count = len(tools)

            # Create a clean table with DOUBLE box style
            tools_table = Table(box=DOUBLE, expand=False)
            tools_table.add_column("Tool", style="cyan")
            tools_table.add_column("Description", style="green")

            # Get all tools with their descriptions
            tool_data = []
            for tool in tools:
                try:
                    # Get tool name and description
                    if hasattr(tool, "name"):
                        name = tool.name
                        description = getattr(tool, "description", "No description")
                    elif isinstance(tool, dict):
                        name = tool.get("name", "Unknown")
                        description = tool.get("description", "No description")
                    else:
                        name = str(tool)
                        description = "No description"

                    # Truncate overly long descriptions
                    if isinstance(description, str) and len(description) > 60:
                        description = description[:57] + "..."

                    tool_data.append((name, description))
                except Exception as e:
                    # Skip tools that can't be processed
                    self.console.print(f"[yellow]Skipped tool: {str(e)}[/yellow]")

            if not tool_data:
                self.console.print(
                    "[yellow]Found tools data but couldn't process any tool information[/yellow]"
                )
                self.console.print(
                    "[yellow]Try asking 'what tools do you have access to?' instead[/yellow]"
                )
                return

            # Sort tools alphabetically for easier scanning
            for name, description in sorted(tool_data, key=lambda x: x[0]):
                tools_table.add_row(name, description)

            # Display the table in a panel
            self.console.print(
                Panel(
                    tools_table,
                    title=f"[bold yellow]Available Tools ({tool_count})[/bold yellow]",
                    subtitle=f"[italic]Via {tool_access_method}[/italic]",
                )
            )

        except Exception as e:
            self.console.print(f"[red]Error accessing tools:[/red] {str(e)}")
            self.console.print(
                "[yellow]Try asking 'what tools do you have access to?' instead[/yellow]"
            )

    def _fix_conversation(self):
        """Fix the current conversation history by removing empty or invalid messages."""
        original_count = len(self.messages)

        # Filter out invalid messages
        fixed_messages = []
        for msg in self.messages:
            if hasattr(msg, "content") and msg.content and msg.content.strip():
                fixed_messages.append(msg)

        # Ensure we have at least a system message
        if not fixed_messages and self.system_prompt:
            fixed_messages.append(SystemMessage(content=self.system_prompt))

        # Replace the messages list
        self.messages = fixed_messages

        # Save the fixed conversation
        self._save_conversation()

        # Report the results in minimal style
        removed_count = original_count - len(self.messages)
        if removed_count > 0:
            self.console.print(
                f"[green]Fixed: Removed {removed_count} empty messages[/green]"
            )
        else:
            self.console.print("[green]No issues found in conversation history[/green]")

    async def _reinitialize_agent(self):
        """Re-initialize the agent by closing and initializing it again."""
        try:
            # First, close the agent to clean up resources
            await self.agent.close()

            # Re-initialize the agent
            await self.agent.initialize()

            # Re-register our callback handler for tool streaming
            if hasattr(self, "tool_callback"):
                tool_callback = self.tool_callback

                # Try multiple ways to register our callback with the agent
                # Method 1: Direct callbacks attribute
                if hasattr(self.agent, "_agent") and hasattr(
                    self.agent._agent, "callbacks"
                ):
                    if self.agent._agent.callbacks is None:
                        self.agent._agent.callbacks = [tool_callback]
                    else:
                        self.agent._agent.callbacks.append(tool_callback)

                # Method 2: Via callback_manager
                if (
                    hasattr(self.agent, "_agent")
                    and hasattr(self.agent._agent, "callback_manager")
                    and hasattr(self.agent._agent.callback_manager, "add_handler")
                ):
                    self.agent._agent.callback_manager.add_handler(tool_callback)

                # Method 3: At the agent level
                if hasattr(self.agent, "callbacks"):
                    if self.agent.callbacks is None:
                        self.agent.callbacks = [tool_callback]
                    else:
                        self.agent.callbacks.append(tool_callback)

            self.console.print("[green]Agent re-initialized successfully[/green]")

            # Display active MCP servers
            enabled_servers = self._get_enabled_servers()
            if enabled_servers:
                servers_str = ", ".join(enabled_servers)
                self.console.print(
                    f"[dim]Connected to MCP servers: {servers_str}[/dim]"
                )

                # Try to get tool count
                tool_count = self._get_tools_count()
                if tool_count > 0:
                    self.console.print(f"[dim]Found {tool_count} available tools[/dim]")

        except Exception as e:
            self.console.print(
                f"[bold red]Error re-initializing agent:[/bold red] {str(e)}"
            )
            self.console.print("\n[yellow]Troubleshooting tips:[/yellow]")
            self.console.print(
                "1. Make sure Node.js is installed (required for Playwright)"
            )
            self.console.print("2. Check your internet connection")
            self.console.print(
                "3. Ensure your API keys are correctly set in your .env file"
            )
            self.console.print(
                "4. Try running 'npx @playwright/mcp@latest' manually to see if there are any Playwright-specific errors"
            )
            self.console.print(
                "\n[yellow]Agent will continue in limited mode (some features may not work)[/yellow]\n"
            )

    def _handle_command(self, command: str) -> bool:
        """Handle a chat command.

        Returns:
            bool: True if a command was handled, False otherwise.
        """
        if command.startswith("/clear"):
            self._clear_conversation()
            return True
        elif command.startswith("/help"):
            self._show_help()
            return True
        elif command.startswith("/tools"):
            self._list_tools()
            return True
        elif command.startswith("/fix"):
            self._fix_conversation()
            return True
        elif command.startswith("/init"):
            # Re-initialize the agent - display message but actual re-initialization
            # will happen in an async context
            self.console.print(
                "[yellow]Re-initializing agent and MCP servers...[/yellow]"
            )
            # We return False here to let the REPL loop handle this command specially
            return False
        return False

    async def _handle_async_command(self, command: str) -> bool:
        """Handle an async chat command.

        Returns:
            bool: True if a command was handled, False otherwise.
        """
        if command.startswith("/init"):
            # Re-initialize the agent
            await self._reinitialize_agent()
            return True
        return False

    def _clear_screen(self):
        """Clear the terminal screen without affecting conversation history."""
        self.console.clear()
        # Print a minimal header to show we're still in the same session
        self.console.print("[dim]" + "─" * self.console.width + "[/dim]")

    async def run(self):
        """Start the REPL loop"""
        # Initialize the agent
        try:
            self.console.print(
                "[yellow]Initializing agent and starting MCP servers...[/yellow]"
            )
            await self.agent.initialize()

            # Create our custom callback handler for tool streaming
            tool_callback = ToolUsageCallbackHandler(self.console)

            # Try multiple ways to register our callback with the agent
            # Method 1: Direct callbacks attribute
            if hasattr(self.agent, "_agent") and hasattr(
                self.agent._agent, "callbacks"
            ):
                if self.agent._agent.callbacks is None:
                    self.agent._agent.callbacks = [tool_callback]
                else:
                    self.agent._agent.callbacks.append(tool_callback)

            # Method 2: Via callback_manager
            if (
                hasattr(self.agent, "_agent")
                and hasattr(self.agent._agent, "callback_manager")
                and hasattr(self.agent._agent.callback_manager, "add_handler")
            ):
                self.agent._agent.callback_manager.add_handler(tool_callback)

            # Method 3: At the agent level
            if hasattr(self.agent, "callbacks"):
                if self.agent.callbacks is None:
                    self.agent.callbacks = [tool_callback]
                else:
                    self.agent.callbacks.append(tool_callback)

            # Store the callback for later use
            self.tool_callback = tool_callback

            self.console.print("[green]Agent initialized successfully[/green]")
        except Exception as e:
            self.console.print(
                f"[bold red]Error initializing agent:[/bold red] {str(e)}"
            )
            self.console.print("\n[yellow]Troubleshooting tips:[/yellow]")
            self.console.print(
                "1. Make sure Node.js is installed (required for Playwright)"
            )
            self.console.print("2. Check your internet connection")
            self.console.print(
                "3. Ensure GOOGLE_API_KEY is correctly set in your .env file"
            )
            self.console.print(
                "4. Try running 'npx @playwright/mcp@latest' manually to see if there are any Playwright-specific errors"
            )
            self.console.print(
                "\n[yellow]Agent will continue in limited mode (some features may not work)[/yellow]\n"
            )
            # Don't exit - we'll handle missing agent components in the command handlers

        # Display welcome message
        self._display_welcome()

        # Initialize message history with system message if present
        if not self.messages and self.system_prompt:
            self.messages.append(SystemMessage(content=self.system_prompt))

        # REPL loop
        while True:
            try:
                # Get user input with minimalist TTY-style prompt
                user_input = await self.session.prompt_async(
                    HTML("<b><style fg='green'>> </style></b>")
                )

                # Check if user wants to exit
                if user_input.lower() in ("exit", "quit"):
                    self._save_conversation()  # Save before exiting
                    self.console.print("[bold red]Exiting...[/bold red]")
                    # Simple exit without animation
                    break

                # Check for screen clear commands
                if user_input.lower() in ("clear", "cls"):
                    self._clear_screen()
                    continue

                # Check if input is a command
                if user_input.startswith("/"):
                    handled = self._handle_command(user_input)

                    # Handle special case for async commands
                    if not handled and user_input.startswith("/init"):
                        # Handle async command
                        await self._handle_async_command(user_input)
                        # Add consistent spacing after command output
                        self.console.print("\n")
                        continue
                    elif handled:
                        # Add consistent spacing after command output
                        self.console.print("\n")
                        continue

                # Skip empty inputs
                if not user_input.strip():
                    self.console.print("[yellow]Empty input[/yellow]")
                    self.console.print("\n")
                    continue

                # Add user message to messages
                user_message = HumanMessage(content=user_input)
                self.messages.append(user_message)

                # Add consistent spacing before thinking indicator
                self.console.print()

                # Show minimal thinking indicator - keep this status indicator
                # but now our callback will also show tool usage alongside it
                with self.console.status("[yellow]thinking[/yellow]"):
                    # Filter out any empty messages to prevent API errors
                    valid_messages = [
                        msg
                        for msg in self.messages
                        if hasattr(msg, "content")
                        and msg.content
                        and msg.content.strip()
                    ]

                    # Make sure we at least have a system message
                    if not valid_messages and self.system_prompt:
                        valid_messages = [SystemMessage(content=self.system_prompt)]

                    try:
                        # Check if agent was properly initialized
                        if (
                            not hasattr(self.agent, "_agent")
                            or self.agent._agent is None
                        ):
                            raise RuntimeError(
                                "Agent not properly initialized. Try restarting the application."
                            )

                        # Reset tool counter for this new run
                        if hasattr(self, "tool_callback"):
                            self.tool_callback.tool_count = 0

                        # Use a direct call to the LLM rather than the agent.run method
                        # This will trigger our callback as tools are used
                        result = await self.agent._agent.run(
                            query=user_input,
                            chat_history=valid_messages,  # Pass only valid messages
                        )

                        # Strip trailing whitespace and newlines for consistent formatting
                        result = result.rstrip()

                        # Add AI response to messages
                        ai_message = AIMessage(content=result)
                        self.messages.append(ai_message)
                    except Exception as e:
                        raise e

                # Display the result with a minimal TTY-style prefix with consistent spacing
                self.console.print("[bold cyan]x[/bold cyan] ", end="")
                self.console.print(Markdown(result))

                # Add exactly one blank line after the assistant's response
                self.console.print("\n")

                # Save conversation after each interaction
                self._save_conversation()

            except Exception as e:
                error_str = str(e)

                # Handle specific error cases with more minimal messages
                if "empty text parameter" in error_str or "empty content" in error_str:
                    self.console.print(
                        "[red]Error:[/red] Empty message content. Try [cyan]/fix[/cyan]"
                    )
                elif "rate limit" in error_str.lower():
                    self.console.print(
                        "[red]Error:[/red] API rate limit exceeded. Wait a moment."
                    )
                elif (
                    "api key" in error_str.lower()
                    or "authentication" in error_str.lower()
                ):
                    self.console.print(
                        "[red]API Error:[/red] Check your API key in .env file."
                    )
                elif (
                    "network" in error_str.lower()
                    or "connection" in error_str.lower()
                    or "timeout" in error_str.lower()
                ):
                    self.console.print(
                        "[red]Network Error:[/red] Check your internet connection."
                    )
                else:
                    # Generic error handling
                    self.console.print(f"[red]Error:[/red] {error_str}")

                # Add consistent spacing after error
                self.console.print("\n")

        # Clean up resources
        await self.agent.close()
