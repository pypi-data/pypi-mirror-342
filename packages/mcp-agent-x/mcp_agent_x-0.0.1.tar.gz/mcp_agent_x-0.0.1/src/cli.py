"""
Command-line interface for MCPx application.
"""

import asyncio
import os
import subprocess
import sys

import click

from mcpx.config import (
    CONFIG_DIR,
    CONFIG_FILE,
    DEFAULTS_DIR,
    SYSTEM_PROMPT_FILE,
    Config,
    ensure_config_exists,
)
from mcpx.main import start_repl


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    """MCPx - MCP Agent REPL interface for AI agents."""
    if ctx.invoked_subcommand is None:
        # If no subcommand provided, run the REPL by default
        ctx.invoke(run)


@main.command()
def run():
    """Start the MCPx REPL interface."""
    # Ensure config exists before starting
    ensure_config_exists()
    # Start the REPL interface
    asyncio.run(start_repl())


@main.command()
@click.option(
    "--force",
    is_flag=True,
    help="Force overwrite of existing configuration with defaults",
)
def init(force):
    """Initialize or reinitialize the MCPx configuration with defaults."""
    click.echo("Initializing MCPx application...")

    # Create config directories if they don't exist
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    # Reset the config file
    if force or not CONFIG_FILE.exists():
        default_config = DEFAULTS_DIR / "config.json"
        import shutil

        shutil.copy(default_config, CONFIG_FILE)
        click.echo(f"✅ Created default configuration at: {CONFIG_FILE}")
    else:
        click.echo(
            f"ℹ️ Config file already exists at: {CONFIG_FILE} (use --force to overwrite)"
        )

    # Reset the system prompt file
    if force or not SYSTEM_PROMPT_FILE.exists():
        default_prompt = DEFAULTS_DIR / "system_prompt.md"
        import shutil

        shutil.copy(default_prompt, SYSTEM_PROMPT_FILE)
        click.echo(f"✅ Created default system prompt at: {SYSTEM_PROMPT_FILE}")
    else:
        click.echo(
            f"ℹ️ System prompt already exists at: {SYSTEM_PROMPT_FILE} (use --force to overwrite)"
        )

    click.echo(
        "\nInitialization complete. You can now run 'mcpx run' to start the application."
    )


@main.command()
def config():
    """Open the config directory in your file explorer."""
    ensure_config_exists()

    try:
        # Platform-specific directory opening commands
        if sys.platform == "win32":
            os.startfile(CONFIG_DIR)
        elif sys.platform == "darwin":
            subprocess.run(["open", CONFIG_DIR], check=True)
        else:  # Linux and other platforms
            subprocess.run(["xdg-open", CONFIG_DIR], check=True)
        click.echo(f"Opened config directory: {CONFIG_DIR}")
    except Exception as e:
        click.echo(f"Failed to open config directory: {e}")
        click.echo(f"You can manually open: {CONFIG_DIR}")


@main.command()
def edit():
    """Edit the configuration file directly."""
    ensure_config_exists()

    # Try to use the default editor from environment
    editor = os.environ.get("EDITOR", "")

    if not editor:
        # Try to find vim or nano as fallback editors
        editor = _find_fallback_editor()

    if editor:
        try:
            subprocess.run([editor, CONFIG_FILE], check=False)
        except Exception as e:
            click.echo(f"Failed to open with editor: {e}")
            click.echo(f"You can manually edit: {CONFIG_FILE}")
    else:
        # If no editor is found, just show the path
        click.echo(f"No editor found. You can manually edit: {CONFIG_FILE}")


@main.command()
def prompt():
    """Edit the system prompt file directly."""
    ensure_config_exists()

    # Try to use the default editor from environment
    editor = os.environ.get("EDITOR", "")

    if not editor:
        # Try to find vim or nano as fallback editors
        editor = _find_fallback_editor()

    if editor:
        try:
            subprocess.run([editor, SYSTEM_PROMPT_FILE], check=False)
            click.echo("System prompt updated. Changes will take effect on next start.")
        except Exception as e:
            click.echo(f"Failed to open with editor: {e}")
            click.echo(f"You can manually edit: {SYSTEM_PROMPT_FILE}")
    else:
        # If no editor is found, just show the path
        click.echo(f"No editor found. You can manually edit: {SYSTEM_PROMPT_FILE}")


@main.group()
def provider():
    """Manage LLM providers and settings."""
    pass


@provider.command("list")
def list_providers():
    """List all available LLM providers."""
    config = Config.from_file()

    click.echo("\nAvailable LLM Providers:")
    click.echo("------------------------")

    # Get all providers - built-in first
    click.echo("Built-in Providers:")
    for provider in ["google"]:
        if provider == config.llm_provider:
            click.echo(f"* {provider} (current)")
        else:
            click.echo(f"  {provider}")

    # Then show custom providers from config
    if config.custom_providers:
        click.echo("\nCustom Providers:")
        for provider_name in config.custom_providers:
            if provider_name == config.llm_provider:
                click.echo(f"* {provider_name} (current)")
            else:
                click.echo(f"  {provider_name}")

    click.echo("\nUse 'mcpx provider show <name>' to see details of a provider")
    click.echo("Use 'mcpx provider use <name>' to switch to a different provider")
    click.echo("Use 'mcpx provider add <name>' to add a new custom provider")


@provider.command("show")
@click.argument("name")
def show_provider(name):
    """Show details of a specific provider."""
    config = Config.from_file()

    # Handle built-in providers
    if name == "google":
        click.echo("\nGoogle Provider (built-in)")
        click.echo("------------------------")
        click.echo(f"Model: {config.llm_model}")
        click.echo("API Key: Uses GOOGLE_API_KEY environment variable")
        return

    # Get provider config
    provider_config = config.get_provider_config(name)

    if not provider_config:
        click.echo(f"Provider '{name}' not found")
        return

    click.echo(f"\nProvider: {name}")
    click.echo("------------------------")
    click.echo(f"Base URL: {provider_config.base_url}")

    # Don't show actual API key, but whether it's set
    api_key = "Set" if provider_config.api_key else "Not set"
    click.echo(f"API Key: {api_key}")

    click.echo(f"Header: {provider_config.header_name}")
    click.echo(f"Header Prefix: {provider_config.header_prefix}")

    # Show any extra options
    if provider_config.extra_options:
        click.echo("\nAdditional Options:")
        for key, value in provider_config.extra_options.items():
            click.echo(f"  {key}: {value}")


@provider.command("use")
@click.argument("name")
def use_provider(name):
    """Switch to a different provider."""
    config = Config.from_file()

    if config.set_provider(name):
        config.save()
        click.echo(f"Switched to provider: {name}")
    else:
        click.echo(f"Provider '{name}' not found")


@provider.command("add")
@click.argument("name")
@click.option("--base-url", prompt="Base URL for the API", help="Base URL for the API")
@click.option("--model", prompt="Model name", help="Model name to use")
@click.option("--api-key", prompt="API Key", help="API Key")
@click.option("--header-name", default="x-api-key", help="Header name for the API key")
@click.option("--header-prefix", default="", help="Header prefix for the API key")
def add_provider(name, base_url, model, api_key, header_name, header_prefix):
    """Add a new LLM provider."""
    config = Config.from_file()

    # Check if provider already exists
    if name in config.list_all_providers():
        click.echo(f"Provider '{name}' already exists")
        return

    # Add the provider
    config.add_custom_provider(
        name=name,
        base_url=base_url,
        api_key=api_key,
        header_name=header_name,
        header_prefix=header_prefix,
    )

    # Set the model
    config.llm_model = model

    # Save the config
    config.save()

    click.echo(f"Added new provider: {name}")
    click.echo(f"You can now use it with: mcpx provider use {name}")


def _find_fallback_editor():
    """Find a fallback editor if EDITOR is not set."""
    # List of editors to try in order of preference
    editors = ["vim", "nano"]

    for editor in editors:
        try:
            # Check if the editor is available in the system
            result = subprocess.run(
                ["which", editor] if sys.platform != "win32" else ["where", editor],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0:
                click.echo(f"Using {editor} as the default editor")
                return editor
        except Exception:
            pass

    return None


if __name__ == "__main__":
    main()
