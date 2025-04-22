import asyncio

from dotenv import load_dotenv
from langchain_core.language_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from mcp_use import MCPClient

from mcpx.agent import ExtendedMCPAgent
from mcpx.config import Config, load_system_prompt


def create_llm_from_config(config: Config) -> BaseChatModel:
    """Create an LLM based on the configuration.

    Args:
        config: Config object containing LLM settings

    Returns:
        A configured LLM instance

    Raises:
        ValueError: If the provider is not supported
    """
    provider = config.llm_provider

    # Handle standard providers
    if provider == "google":
        return ChatGoogleGenerativeAI(model=config.llm_model)
    elif provider == "openai":
        # Get OpenAI provider config
        provider_config = config.get_provider_config("openai")
        if not provider_config:
            raise ValueError("OpenAI provider configuration not found")

        # Create OpenAI chat model
        return ChatOpenAI(
            model=config.llm_model,
            openai_api_key=provider_config.api_key,
            openai_api_base=(
                provider_config.base_url if provider_config.base_url else None
            ),
        )
    elif provider == "anthropic":
        # We would need to add the anthropic package import
        raise ValueError("Anthropic provider not yet implemented")
    elif provider in config.custom_providers:
        # Handle custom providers - this would require a more generic approach
        # and potentially custom implementations
        raise ValueError(f"Custom provider '{provider}' not yet implemented")
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")


async def start_repl(session_id=None):
    """Start the REPL interface with the given session ID."""
    # Load environment variables
    load_dotenv()

    # Generate a session ID if not provided
    if session_id is None:
        session_id = "default"

    # Load configuration and system prompt
    config = Config.from_file()
    system_prompt = load_system_prompt()

    # Create MCPClient from configuration dictionary
    client = MCPClient.from_dict({"mcpServers": config.mcp_servers})
    print(f"Initialized MCPClient with servers: {', '.join(config.mcp_servers.keys())}")

    try:
        # Create LLM based on config
        llm = create_llm_from_config(config)

        # Create agent with the client and configured settings
        agent = ExtendedMCPAgent(
            llm=llm,
            client=client,
            memory_enabled=config.memory_enabled,
            system_prompt=system_prompt,
            max_steps=config.max_steps,
        )
        print(
            f"Agent configured with max_steps={config.max_steps}, memory_enabled={config.memory_enabled}"
        )

        # Create and start the REPL interface
        from mcpx.repl import AgentREPL

        repl = AgentREPL(agent, system_prompt)
        await repl.run()
    except ValueError as e:
        print(f"Error starting REPL: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback

        print(traceback.format_exc())


async def main():
    """Legacy main function for backward compatibility."""
    await start_repl()


if __name__ == "__main__":
    asyncio.run(main())
