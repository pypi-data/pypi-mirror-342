"""
MCPx - MCP Agent REPL interface implementation.
"""

__version__ = "0.1.0"

from mcpx.config import CONFIG_DIR, CONFIG_FILE, DATA_DIR
from mcpx.main import main, start_repl
from mcpx.repl import AgentREPL

__all__ = ["CONFIG_DIR", "CONFIG_FILE", "DATA_DIR", "main", "start_repl", "AgentREPL"]
