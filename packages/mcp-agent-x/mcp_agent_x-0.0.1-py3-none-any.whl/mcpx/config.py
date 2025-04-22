"""
Configuration management for MCPx application.
"""

import json
import shutil
from pathlib import Path
from typing import Any

from platformdirs import user_config_dir, user_data_dir

# Configuration directories and files
APP_NAME = "mcp-agent-x"
APP_AUTHOR = "mcpx"

# Main configuration paths
CONFIG_DIR = Path(user_config_dir(APP_NAME, APP_AUTHOR))
DATA_DIR = Path(user_data_dir(APP_NAME, APP_AUTHOR))
CONFIG_FILE = CONFIG_DIR / "config.json"
SYSTEM_PROMPT_FILE = CONFIG_DIR / "system_prompt.md"
HISTORY_FILE = DATA_DIR / "history.json"
DEFAULTS_DIR = Path(__file__).parent / "defaults"


class LLMProviderConfig:
    """Configuration for a LLM provider."""

    def __init__(self, provider_data: dict[str, Any]):
        """Initialize with provider configuration data.

        Args:
            provider_data: Provider configuration dictionary
        """
        self.base_url = provider_data.get("base_url", "")
        self.api_key = provider_data.get("api_key", "")
        self.header_name = provider_data.get("header_name", "Authorization")
        self.header_prefix = provider_data.get("header_prefix", "Bearer ")
        self.extra_options = {
            k: v
            for k, v in provider_data.items()
            if k not in ["base_url", "api_key", "header_name", "header_prefix"]
        }

    def get_headers(self) -> dict[str, str]:
        """Get the headers for API calls.

        Returns:
            Dictionary of headers
        """
        if not self.api_key:
            return {}

        return {self.header_name: f"{self.header_prefix}{self.api_key}"}

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary.

        Returns:
            Dictionary representation
        """
        return {
            "base_url": self.base_url,
            "api_key": self.api_key,
            "header_name": self.header_name,
            "header_prefix": self.header_prefix,
            **self.extra_options,
        }


class Config:
    """Configuration class for MCPx application."""

    def __init__(self, config_data: dict[str, Any]):
        """Initialize with configuration data.

        Args:
            config_data: Configuration dictionary loaded from JSON
        """
        self.config_data = config_data

        # Extract common settings
        agent_config = config_data.get("agent", {})
        self.max_steps = agent_config.get("max_steps", 10)
        self.memory_enabled = agent_config.get("memory_enabled", True)

        # Extract conversation settings
        conversation_config = config_data.get("conversation", {})
        self.save_conversations = conversation_config.get("save", True)
        self.conversation_dir = conversation_config.get(
            "directory", str(DATA_DIR / "conversations")
        )

        # Extract UI settings
        ui_config = config_data.get("ui", {})
        self.show_thinking = ui_config.get("show_thinking", True)
        self.display_mode = ui_config.get("display_mode", "markdown")

        # LLM configuration
        self.llm_config = config_data.get("llm", {})
        self.llm_provider = self.llm_config.get("provider", "google")
        self.llm_model = self.llm_config.get("model", "gemini-2.0-flash")

        # Parse custom providers
        self.custom_providers = {}
        for provider_name, provider_data in self.llm_config.get(
            "custom_providers", {}
        ).items():
            self.custom_providers[provider_name] = LLMProviderConfig(provider_data)

        # MCP servers configuration
        self.mcp_servers = config_data.get("mcpServers", {})

    def get_provider_config(
        self, provider_name: str | None = None
    ) -> LLMProviderConfig | None:
        """Get the configuration for a provider.

        Args:
            provider_name: Name of the provider, defaults to the current provider

        Returns:
            Provider configuration or None if not found
        """
        if provider_name is None:
            provider_name = self.llm_provider

        return self.custom_providers.get(provider_name)

    def set_provider(self, provider_name: str) -> bool:
        """Set the current provider.

        Args:
            provider_name: Name of the provider

        Returns:
            True if successful, False if provider not found
        """
        if provider_name in self.custom_providers or provider_name in [
            "google",
            "openai",
            "anthropic",
        ]:
            self.llm_provider = provider_name
            self.config_data["llm"]["provider"] = provider_name
            return True
        return False

    def add_custom_provider(
        self,
        name: str,
        base_url: str,
        api_key: str,
        header_name: str = "x-api-key",
        header_prefix: str = "",
    ) -> LLMProviderConfig:
        """Add a new custom provider.

        Args:
            name: Name of the provider
            base_url: Base URL for API calls
            api_key: API key
            header_name: Name of the header for the API key
            header_prefix: Prefix for the API key in the header

        Returns:
            The created provider configuration
        """
        provider_data = {
            "base_url": base_url,
            "api_key": api_key,
            "header_name": header_name,
            "header_prefix": header_prefix,
        }

        provider_config = LLMProviderConfig(provider_data)
        self.custom_providers[name] = provider_config

        # Update config data
        if "custom_providers" not in self.config_data["llm"]:
            self.config_data["llm"]["custom_providers"] = {}

        self.config_data["llm"]["custom_providers"][name] = provider_data

        return provider_config

    def list_all_providers(self) -> list[str]:
        """List all available providers.

        Returns:
            List of provider names
        """
        # Standard providers
        providers = ["google", "openai", "anthropic"]

        # Add custom providers
        for name in self.custom_providers:
            if name not in providers:
                providers.append(name)

        return providers

    @classmethod
    def from_file(cls, path: Path | None = None) -> "Config":
        """Load configuration from a file.

        Args:
            path: Path to the configuration file, defaults to CONFIG_FILE

        Returns:
            Config object populated with the configuration data
        """
        if path is None:
            path = CONFIG_FILE

        ensure_config_exists()

        try:
            with open(path) as f:
                config_data = json.load(f)
                return cls(config_data)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading config file: {e}")
            # Return default config
            with open(DEFAULTS_DIR / "config.json") as f:
                config_data = json.load(f)
                return cls(config_data)

    def save(self, path: Path | None = None) -> None:
        """Save the configuration to a file.

        Args:
            path: Path to save the configuration file, defaults to CONFIG_FILE
        """
        if path is None:
            path = CONFIG_FILE

        try:
            with open(path, "w") as f:
                json.dump(self.config_data, f, indent=2)
        except Exception as e:
            print(f"Error saving configuration: {e}")


def ensure_config_exists():
    """Ensure the configuration directory and files exist."""
    # Create config directory if it doesn't exist
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Ensure the parent directories of all config files exist
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    SYSTEM_PROMPT_FILE.parent.mkdir(parents=True, exist_ok=True)
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Check if config file exists, if not copy the default
    if not CONFIG_FILE.exists():
        default_config = DEFAULTS_DIR / "config.json"
        shutil.copy(default_config, CONFIG_FILE)
        print(f"Created default configuration at: {CONFIG_FILE}")

    # Check if system prompt file exists, if not copy the default
    if not SYSTEM_PROMPT_FILE.exists():
        default_prompt = DEFAULTS_DIR / "system_prompt.md"
        try:
            shutil.copy(default_prompt, SYSTEM_PROMPT_FILE)
            print(f"Created default system prompt at: {SYSTEM_PROMPT_FILE}")
        except FileNotFoundError as e:
            # If default prompt file doesn't exist (e.g., in tests), create an empty one
            with open(SYSTEM_PROMPT_FILE, "w") as f:
                f.write("Default system prompt")
            print(
                f"Created empty system prompt at: {SYSTEM_PROMPT_FILE} (default not found: {e})"
            )

    # Ensure history file exists (empty if new)
    if not HISTORY_FILE.exists():
        with open(HISTORY_FILE, "w") as f:
            json.dump({"conversations": {}}, f)


def load_config():
    """Load configuration from file."""
    ensure_config_exists()

    try:
        with open(CONFIG_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading config file: {e}")
        # Return default config
        with open(DEFAULTS_DIR / "config.json") as f:
            return json.load(f)


def load_system_prompt():
    """Load system prompt from file."""
    ensure_config_exists()

    try:
        with open(SYSTEM_PROMPT_FILE) as f:
            system_prompt = f.read().strip()
            return system_prompt
    except (OSError, FileNotFoundError) as e:
        print(f"Error loading system prompt file: {e}")
        # Return default prompt
        with open(DEFAULTS_DIR / "system_prompt.md") as f:
            return f.read().strip()


def save_history(history_data):
    """Save conversation history to file."""
    ensure_config_exists()

    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(history_data, f, indent=2)
    except Exception as e:
        print(f"Error saving history: {e}")


def load_history():
    """Load conversation history from file."""
    ensure_config_exists()

    try:
        with open(HISTORY_FILE) as f:
            data = json.load(f)

            # Validate the structure
            if not isinstance(data, dict) or not isinstance(
                data.get("conversations", {}), dict | list
            ):
                raise ValueError("Invalid history file format")

            return data
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"Error loading history file: {e}")
        # Backup the corrupted file if it exists
        if HISTORY_FILE.exists():
            backup_file = HISTORY_FILE.with_suffix(".json.bak")
            try:
                shutil.copy(HISTORY_FILE, backup_file)
                print(f"Backed up corrupted history file to {backup_file}")
            except Exception as backup_error:
                print(f"Failed to back up history file: {backup_error}")

        # Create a new history file
        with open(HISTORY_FILE, "w") as f:
            default_data = {"conversations": {}}
            json.dump(default_data, f, indent=2)
            print("Reset history file")

        return default_data
