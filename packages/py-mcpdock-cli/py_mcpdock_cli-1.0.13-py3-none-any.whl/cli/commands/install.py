import click
import json
import asyncio
from typing import Dict, Any, Optional

from rich import print as rprint
from rich.console import Console
from rich.spinner import Spinner

from ..utils.logger import verbose, info, debug, error, warning
from ..registry import resolve_package
from ..utils.runtime import ensure_uv_installed, ensure_bun_installed, check_and_notify_remote_server
from ..utils.config import choose_connection, collect_config_values, get_server_name, format_server_config, format_config_values
from ..config.client_config import read_config, write_config
from ..types.registry import ConfiguredServer, ClientConfig


async def validate_config_values(
    connection: Any,
    existing_values: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Validates config values without prompting for user input.
    Only checks if required values are present.

    Args:
        connection: Connection details containing schema
        existing_values: Existing config values to validate

    Returns:
        Dictionary with validated config values

    Raises:
        ValueError: If required configuration values are missing
    """
    schema = connection.configSchema or {}
    env = schema.env if schema else {}
    if not env:
        return {}

    # Use existing values or empty dict
    config_values = existing_values or {}

    # Get list of required env variables
    required = set(schema.required if schema else [])

    # Check if all required env variables are provided
    missing_required = []
    for key in required:
        if key not in config_values or config_values[key] is None:
            missing_required.append(key)

    # Raise error if any required env variables are missing
    if missing_required:
        missing_fields = ", ".join(missing_required)
        raise ValueError(f"Missing required configuration values: {missing_fields}")

    # Format and return the validated config
    return format_config_values(connection, config_values)


async def install_mcp_server(
    package_identifier: str,
    target_client: Optional[str] = None,
    initial_config: Optional[Dict[str, Any]] = None,
    api_key: Optional[str] = None
) -> None:
    """
    Installs and configures an AI server package for a specified client.

    Args:
        package_identifier: The fully qualified name of the AI server package
        target_client: The AI client to configure the server for
        initial_config: Optional pre-defined configuration values
        api_key: Optional API key for fetching saved configurations
    """
    target_client = target_client or "claude"  # Default to Claude if no client specified
    verbose(f"Initiating installation of {package_identifier} for {target_client}")

    console = Console()

    # Create and start spinner for package resolution
    with console.status(f"Resolving {package_identifier}...", spinner="dots") as status:
        try:
            # Resolve the package (fetch server metadata)
            verbose(f"Resolving package: {package_identifier}")
            server_data = await resolve_package(package_identifier)
            verbose(f"Package resolved successfully: {server_data.qualifiedName}")

            # Choose the appropriate connection type
            verbose("Choosing connection type...")
            connection = choose_connection(server_data)
            verbose(f"Selected connection type: {connection.type}")

            # Check for required runtimes and install if needed
            # Commented out as these are specific to JS environment
            # await ensure_uv_installed(connection)
            # await ensure_bun_installed(connection)

            # Inform users of remote server installation if applicable
            is_remote = check_and_notify_remote_server(server_data)
            if is_remote:
                verbose("Remote server detected, notification displayed")

            # Get the validated config values, no prompting
            status.update(f"Validating configuration for {package_identifier}...")
            collected_config_values = await validate_config_values(connection, initial_config)

            # Determine if we need to pass config flag
            config_flag_needed = initial_config is not None

            verbose(f"Config values validated: {json.dumps(collected_config_values, indent=2)}")
            verbose(f"Using config flag: {config_flag_needed}")

            # Format the server configuration
            verbose("Formatting server configuration...")
            server_config = format_server_config(
                package_identifier,
                collected_config_values,
                api_key,
                config_flag_needed,
            )
            verbose(f"Formatted server config: {json.dumps(server_config.__dict__, indent=2)}")

            # Read existing config from client
            status.update(f"Installing for {target_client}...")
            verbose(f"Reading configuration for client: {target_client}")
            client_config = read_config(target_client)

            # Get normalized server name to use as key
            server_name = get_server_name(package_identifier)
            verbose(f"Normalized server ID: {server_name}")

            # Update client configuration with new server
            verbose("Updating client configuration...")
            if not isinstance(client_config.mcpServers, dict):
                # Initialize if needed
                client_config.mcpServers = {}

            # Add the new server config
            client_config.mcpServers[server_name] = server_config

            # Write updated configuration
            verbose("Writing updated configuration...")
            write_config(client_config, target_client)
            verbose("Configuration successfully written")

            rprint(f"[green]{package_identifier} successfully installed for {target_client}[/green]")

            # No prompt for client restart
            verbose("Installation completed successfully")

        except Exception as e:
            verbose(f"Installation error: {str(e)}")
            rprint(f"[red]Failed to install {package_identifier}[/red]")
            rprint(f"[red]Error: {str(e)}[/red]")
            raise


@click.command("install")
@click.argument("mcp_server", type=click.STRING)
@click.option("--client", type=click.STRING, help="Specify the target AI client")
@click.option("--env", "env_json", type=click.STRING, help="Provide configuration as JSON (bypasses interactive prompts)")
@click.option("--api-key", type=click.STRING, help="Provide an API key for fetching saved configurations")
def install(mcp_server: str, client: Optional[str], env_json: Optional[str], api_key: Optional[str]):
    """Install an AI mcp-server with optional configuration."""
    click.echo(f"Attempting to install {mcp_server}...")
    user_config = None
    if env_json:
        try:
            user_config = json.loads(env_json)
            click.echo(f"Using provided config: {user_config}")
        except json.JSONDecodeError as e:
            click.echo(f"Error: Invalid JSON provided for --config: {e}", err=True)
            return

    try:
        # Run the async installation process
        asyncio.run(install_mcp_server(mcp_server, client, user_config, api_key))
    except Exception as e:
        click.echo(f"Installation failed: {str(e)}", err=True)
        return 1
