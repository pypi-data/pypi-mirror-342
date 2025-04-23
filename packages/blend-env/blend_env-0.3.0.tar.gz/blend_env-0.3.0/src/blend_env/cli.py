import logging
import re
import subprocess
from pathlib import Path
from typing import Optional, List, Dict

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import print as rprint
from rich.progress import Progress, SpinnerColumn, TextColumn

from . import load_env

# Use relative imports for sibling modules within the package
from .completion import install_completion
from .crypto import KEY_PATH, encrypt
from .export import export_env
from .loader import DEFAULT_CONFIG_DIR, parse_env_file
from .scaffold import (
    get_encrypted_secrets_path,
    get_global_env_path,
    get_global_secrets_path,
    init_blendenv,
)

# Get logger
logger = logging.getLogger("blend-env")

# Create rich console for fancy output
console = Console()

# Create a Typer app
app = typer.Typer(
    help="Blend-env: Merge global and local .env files seamlessly.",
    add_completion=False,
)

# Create CLI alias for test compatibility
cli = app

# Create subcommands
global_app = typer.Typer(help="Manage global environment variables")
local_app = typer.Typer(help="Manage local environment variables")
secrets_app = typer.Typer(help="Manage secret environment variables")

# Create aliases for test compatibility
global_env = global_app
local_env = local_app
secrets = secrets_app

# Register subcommands
app.add_typer(global_app, name="global")
app.add_typer(local_app, name="local")
app.add_typer(secrets_app, name="secrets")


def get_default_config_dir():
    """Get the default configuration directory."""
    return DEFAULT_CONFIG_DIR


# Common state for the app (similar to Click's context)
class State:
    debug: bool = False


state = State()


def log_debug(message: str):
    """Log debug message if debug mode is enabled"""
    if state.debug:
        logger.debug(message)


def print_success(message: str):
    """Print a success message with visual styling"""
    rprint(Panel.fit(f"[bold green]✓[/bold green] {message}", border_style="green"))


def print_error(message: str):
    """Print an error message with visual styling"""
    rprint(Panel.fit(f"[bold red]✗[/bold red] {message}", border_style="red"))


def print_info(message: str):
    """Print an information message with visual styling"""
    rprint(Panel.fit(f"[bold blue]ℹ[/bold blue] {message}", border_style="blue"))


def print_warning(message: str):
    """Print a warning message with visual styling"""
    rprint(Panel.fit(f"[bold yellow]⚠[/bold yellow] {message}", border_style="yellow"))


def format_key_value(key: str, value: str, mask: bool = False) -> Text:
    """Format a key-value pair with colors"""
    text = Text()
    text.append(key, style="bold cyan")
    text.append("=")
    if mask:
        text.append("*****", style="dim")
    else:
        text.append(value, style="green")
    return text


def show_env_table(data: Dict[str, str], title: str, mask_values: bool = False):
    """Display environment variables in a rich table"""
    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="green")

    for k, v in sorted(data.items()):
        table.add_row(k, "*****" if mask_values else v)

    console.print(table)


@app.callback()
def main(
    debug: bool = typer.Option(False, "--debug", help="Enable debug logging")
):
    """
    Blend-env: Merge global and local .env files seamlessly.

    Manages environment variables by merging a global configuration
    (~/.config/blend-env/.env), optional secrets (~/.config/blend-env/.secrets
    or .secrets.enc), and a project-specific .env file.
    """
    # Store debug flag
    state.debug = debug

    if debug:
        logger.setLevel(logging.DEBUG)
        log_debug("Debug logging enabled via --debug flag")


@global_app.command("set")
def global_set(kv_pair: str = typer.Argument(..., help="Environment variable (key=value)")):
    """Set a global environment variable (key=value)"""
    global_path = get_global_env_path()

    # Create the global config directory if it doesn't exist
    global_path.parent.mkdir(parents=True, exist_ok=True)

    # Create the global .env file if it doesn't exist
    if not global_path.exists():
        global_path.touch()

    if "=" not in kv_pair:
        print_error("Invalid format. Use KEY=VALUE")
        raise typer.Exit(1)

    key, value = kv_pair.split("=", 1)
    key = key.strip()
    value = value.strip()

    if not key:
        print_error("Empty key is not allowed")
        raise typer.Exit(1)

    # Read existing environment variables
    try:
        env_vars = parse_env_file(str(global_path))
    except Exception:
        env_vars = {}

    # Update or add the new variable
    env_vars[key] = value

    # Write back to the global file
    with open(global_path, "w") as f:
        for k, v in sorted(env_vars.items()):
            f.write(f"{k}={v}\n")

    print_success(f"Set global variable: {key}={value}")


@global_app.command("get")
def global_get(key: str = typer.Argument(..., help="Key to retrieve (supports wildcards with *)")):
    """Get global environment variables by key (supports wildcards)"""
    global_path = get_global_env_path()

    if not key:
        print_error("Empty key is not allowed")
        raise typer.Exit(1)

    # Read existing environment variables
    try:
        env_vars = parse_env_file(str(global_path))
    except Exception as e:
        print_error(f"Error reading global environment file: {e}")
        raise typer.Exit(1)

    # Find and print variables matching the key
    found = {}
    for k, v in env_vars.items():
        if k == key or (re.search(key, k) if "*" in key else False):
            found[k] = v

    if not found:
        print_warning(f"No global variable found matching: {key}")
        raise typer.Exit(1)

    show_env_table(found, "Global Environment Variables")


@global_app.command("list")
def global_list():
    """List all global environment variables"""
    global_path = get_global_env_path()

    # Read existing environment variables
    try:
        env_vars = parse_env_file(str(global_path))
    except Exception as e:
        print_error(f"Error reading global environment file: {e}")
        raise typer.Exit(1)

    if not env_vars:
        print_info("No global environment variables found.")
    else:
        show_env_table(env_vars, "Global Environment Variables")


@local_app.command("set")
def local_set(
    kv_pair: str = typer.Argument(..., help="Environment variable (key=value)"),
    env_file: Optional[Path] = typer.Option(None, "--env-file", help="Path to a custom .env file"),
):
    """Set a local environment variable (key=value)"""
    # Determine the local path
    local_path = Path(env_file) if env_file else Path(".env")

    # Get the display path (just the filename or basename)
    display_path = local_path.name

    # Create the local .env file if it doesn't exist
    if not local_path.exists():
        local_path.touch()
        log_debug(f"Created new local environment file at {local_path}")

    if "=" not in kv_pair:
        print_error("Invalid format. Use KEY=VALUE")
        raise typer.Exit(1)

    key, value = kv_pair.split("=", 1)
    key = key.strip()
    value = value.strip()

    if not key:
        print_error("Empty key is not allowed")
        raise typer.Exit(1)

    # Read existing environment variables
    try:
        env_vars = parse_env_file(str(local_path)) if local_path.exists() else {}
    except Exception:
        env_vars = {}

    # Update or add the new variable
    env_vars[key] = value

    # Write back to the local file
    with open(local_path, "w") as f:
        for k, v in sorted(env_vars.items()):
            f.write(f"{k}={v}\n")

    print_success(f"Set local variable: {key}={value} in {display_path}")


@local_app.command("get")
def local_get(
    key: str = typer.Argument(..., help="Key to retrieve (supports wildcards with *)"),
    env_file: Optional[Path] = typer.Option(None, "--env-file", help="Path to a custom .env file"),
):
    """Get local environment variables by key (supports wildcards)"""
    # Determine the local path
    local_path = Path(env_file) if env_file else Path(".env")

    # Get the display path (just the filename or basename)
    display_path = local_path.name

    if not key:
        print_error("Empty key is not allowed")
        raise typer.Exit(1)

    # Check if the local env file exists
    if not local_path.exists():
        print_error(f"Local environment file not found at {display_path}")
        raise typer.Exit(1)

    # Read existing environment variables
    try:
        env_vars = parse_env_file(str(local_path))
    except Exception as e:
        print_error(f"Error reading local environment file: {e}")
        raise typer.Exit(1)

    # Find and print variables matching the key
    found = {}
    for k, v in env_vars.items():
        if k == key or (re.search(key, k) if "*" in key else False):
            found[k] = v

    if not found:
        print_warning(f"No local variable found matching: {key}")
        raise typer.Exit(1)

    show_env_table(found, f"Local Environment Variables [{display_path}]")


@local_app.command("list")
def local_list(env_file: Optional[Path] = typer.Option(None, "--env-file", help="Path to a custom .env file")):
    """List all local environment variables"""
    # Determine the local path
    local_path = Path(env_file) if env_file else Path(".env")

    # Get the display path (just the filename or basename)
    display_path = local_path.name

    # Check if the local env file exists
    if not local_path.exists():
        print_error(f"Local environment file not found at {display_path}")
        raise typer.Exit(1)

    # Read existing environment variables
    try:
        env_vars = parse_env_file(str(local_path))
    except Exception as e:
        print_error(f"Error reading local environment file: {e}")
        raise typer.Exit(1)

    if not env_vars:
        print_info(f"No local environment variables found in {display_path}")
    else:
        show_env_table(env_vars, f"Local Environment Variables [{display_path}]")


@secrets_app.command("set")
def secrets_set(
    kv_pair: str = typer.Argument(..., help="Secret variable (key=value)"),
    secret_key: Optional[str] = typer.Option(None, help="Key to decrypt secrets (uses .key file by default)"),
):
    """Set a secret environment variable (key=value)"""
    secrets_path = get_global_secrets_path()
    encrypted_secrets_path = get_encrypted_secrets_path()

    # Create the global config directory if it doesn't exist
    secrets_path.parent.mkdir(parents=True, exist_ok=True)

    # Create the secrets file if it doesn't exist
    if not secrets_path.exists():
        secrets_path.touch()
        # Set secure permissions
        secrets_path.chmod(0o600)

    if "=" not in kv_pair:
        print_error("Invalid format. Use KEY=VALUE")
        raise typer.Exit(1)

    key_name, value = kv_pair.split("=", 1)
    key_name = key_name.strip()
    value = value.strip()

    if not key_name:
        print_error("Empty key is not allowed")
        raise typer.Exit(1)

    # Read existing secrets
    try:
        secrets_vars = parse_env_file(str(secrets_path))
    except Exception:
        secrets_vars = {}

    # Update or add the new secret
    secrets_vars[key_name] = value

    # Write back to the secrets file
    with open(secrets_path, "w") as f:
        for k, v in sorted(secrets_vars.items()):
            f.write(f"{k}={v}\n")

    # Encrypt the updated secrets file
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]Encrypting secrets...[/bold blue]"),
            transient=True,
        ) as progress:
            progress.add_task("encrypt", total=None)
            secrets_content = secrets_path.read_text()
            encrypted_data = encrypt(secrets_content, secret_key)
            encrypted_secrets_path.write_bytes(encrypted_data)

        print_success(f"Set secret variable: {key_name}=*****")
        print_info(f"Secrets file encrypted to {encrypted_secrets_path}")
    except Exception as e:
        print_error(f"Error encrypting secrets: {e}")
        raise typer.Exit(1)


@secrets_app.command("get")
def secrets_get(
    key: str = typer.Argument(..., help="Key to retrieve (supports wildcards with *)"),
    secret_key: Optional[str] = typer.Option(None, help="Key to decrypt secrets (uses .key file by default)"),
):
    """Get secret environment variables by key (supports wildcards)"""
    secrets_path = get_global_secrets_path()

    if not key:
        print_error("Empty key is not allowed")
        raise typer.Exit(1)

    # Read existing secrets
    try:
        secrets_vars = parse_env_file(str(secrets_path))
    except Exception as e:
        print_error(f"Error reading secrets file: {e}")
        raise typer.Exit(1)

    # Find and print secrets matching the key
    found = {}
    for k, v in secrets_vars.items():
        if k == key or (re.search(key, k) if "*" in key else False):
            found[k] = v

    if not found:
        print_warning(f"No secret variable found matching: {key}")
        raise typer.Exit(1)

    show_env_table(found, "Secret Environment Variables")


@secrets_app.command("list")
def secrets_list(show_values: bool = typer.Option(False, "--show-values", help="Show actual secret values")):
    """List all secret environment variables"""
    secrets_path = get_global_secrets_path()

    # Read existing secrets
    try:
        secrets_vars = parse_env_file(str(secrets_path))
    except Exception as e:
        print_error(f"Error reading secrets file: {e}")
        raise typer.Exit(1)

    if not secrets_vars:
        print_info("No secret environment variables found.")
    else:
        show_env_table(secrets_vars, "Secret Environment Variables", mask_values=not show_values)


@app.command()
def run(
    global_path: Optional[Path] = typer.Option(None, help="Path to the global .env file (overrides default)."),
    local_path: Optional[Path] = typer.Option(None, help="Path to the project's .env file (overrides default './.env')."),
    env_file: Optional[Path] = typer.Option(None, help="Path to a custom .env file (overrides --local-path)."),
    secrets_path: Optional[Path] = typer.Option(None, help="Path to the plaintext secrets file (overrides default)."),
    secret_key: Optional[str] = typer.Option(None, help="Key to decrypt secrets."),
    preview: bool = typer.Option(False, "--preview", help="Preview the merged environment variables without applying them."),
    export_flag: bool = typer.Option(False, "--export", help="Print the merged environment variables to stdout in .env format."),
    show_secrets: bool = typer.Option(False, "--show-secrets", help="Include secrets (.secrets or decrypted .secrets.enc) in the merge/preview/export."),
    encrypt_secrets: bool = typer.Option(False, "--encrypt-secrets", help="Encrypt the plaintext secrets file into .secrets.enc."),
    shell_format: bool = typer.Option(False, "--shell-format", help='Output in shell export format (export KEY="value").'),
    blend_in_os: bool = typer.Option(False, "--blend-in-os", help="Blend the environment variables into os.environ."),
):
    """Merges and optionally applies/previews/exports environment variables."""
    # Get default paths
    default_global_path = get_global_env_path()
    default_secrets_path = get_global_secrets_path()
    default_encrypted_secrets_path = get_encrypted_secrets_path()

    # Handle encryption request first
    if encrypt_secrets:
        try:
            # Use provided secrets path or default
            plain_secrets_path = secrets_path or default_secrets_path
            if not plain_secrets_path.exists():
                print_error(f"Plaintext secrets file not found at {plain_secrets_path}")
                raise typer.Exit(1)

            # Check if key exists
            if not KEY_PATH.exists():
                print_error(f"Encryption key not found at {KEY_PATH}")
                raise typer.Exit(1)

            with Progress(
                SpinnerColumn(),
                TextColumn(f"[bold blue]Encrypting {plain_secrets_path}...[/bold blue]"),
                transient=True,
            ) as progress:
                progress.add_task("encrypt", total=None)
                # Read plaintext secrets
                secrets_content = plain_secrets_path.read_text()
                # Encrypt the content
                encrypted_data = encrypt(secrets_content)
                # Write to encrypted file
                default_encrypted_secrets_path.write_bytes(encrypted_data)

            print_success(f"Successfully encrypted secrets to {default_encrypted_secrets_path}")

            # If only encrypting, exit here
            if not preview and not export_flag:
                return

        except Exception as e:
            print_error(f"Error during secrets encryption: {e}")
            raise typer.Exit(1)

    # Handle export request
    if export_flag:
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]Exporting environment variables...[/bold blue]"),
                transient=True,
            ) as progress:
                progress.add_task("export", total=None)
                result = export_env(
                    global_path=global_path,
                    local_path=local_path,
                    secrets_path=secrets_path,
                    encrypted_secrets_path=default_encrypted_secrets_path,
                    include_secrets=show_secrets,
                    shell_format=shell_format,
                    env_file=env_file,
                    secret_key=secret_key,
                )

            console.print(result, style="bright_green")
            return
        except Exception as e:
            print_error(f"Error during environment export: {e}")
            raise typer.Exit(1)

    # Default action: Load and display environment variables
    try:
        global_path = global_path or default_global_path

        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]Loading environment variables...[/bold blue]"),
            transient=True,
        ) as progress:
            progress.add_task("load", total=None)
            # Load environment using the load_env function
            merged = load_env(
                global_path=global_path,
                local_path=local_path,
                secrets_path=secrets_path,
                encrypted_secrets_path=default_encrypted_secrets_path,
                include_secrets=show_secrets,
                env_file=env_file,
                secret_key=secret_key,
                blend_in_os=blend_in_os,
                debug=state.debug,
            )

        # If preview flag is set, print the variables
        if preview:
            if merged:
                console.print(
                    Panel.fit(
                        "\n".join([format_key_value(k, v if v is not None else "") for k, v in merged.items()]),
                        title="[bold]Merged Environment Variables (Preview)[/bold]",
                        border_style="cyan",
                    )
                )
            else:
                print_warning("No environment variables loaded or merged.")
        else:
            print_success("Environment variables loaded and applied.")
            if show_secrets:
                print_info("Included secrets.")

            if blend_in_os:
                print_info("Environment variables blended into os.environ.")
            else:
                print_info("Use 'blend-env run-command' to execute commands with these variables.")

            # Log the messages as well
            logger.info("Environment variables loaded and applied.")
            if show_secrets:
                logger.info("Included secrets.")

            if blend_in_os:
                logger.info("Environment variables blended into os.environ.")
            else:
                logger.info("Use 'blend-env run-command' to execute commands with these variables.")

    except Exception as e:
        print_error(f"Error during environment processing: {e}")
        logger.error(f"Error during environment processing: {e}")
        raise typer.Exit(1)


@app.command()
def show(
    env_file: Optional[Path] = typer.Option(None, "--env-file", help="Specify a custom .env file (instead of default .env)."),
    global_dir: Optional[Path] = typer.Option(DEFAULT_CONFIG_DIR, "--global-dir", help="Specify a different global directory for .env files."),
    secret_key: Optional[str] = typer.Option(None, "--secret-key", help="Key to decrypt secrets."),
    blend_in_os: bool = typer.Option(False, "--blend-in-os", help="Blend the environment variables into os.environ."),
    show_secrets: bool = typer.Option(False, "--show-secrets", help="Include secret variables in the output."),
):
    """Show the merged environment variables in a colorful display."""
    global_path = Path(global_dir) / ".env"  # Look for .env file in the global directory

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Loading environment variables...[/bold blue]"),
        transient=True,
    ) as progress:
        progress.add_task("load", total=None)
        # Use load_env directly
        merged_vars = load_env(
            global_path=global_path,
            env_file=Path(env_file) if env_file else None,
            secret_key=secret_key,
            blend_in_os=blend_in_os,
            include_secrets=show_secrets,
            debug=state.debug,
        )

    if not merged_vars:
        print_warning("No environment variables found or merged.")
        return

    # Create a table instead of panel for better display
    table = Table(title="Merged Environment Variables", show_header=True, header_style="bold magenta")
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="green")

    for k, v in sorted(merged_vars.items()):
        table.add_row(k, str(v) if v is not None else "")

    console.print(table)


@app.command()
def run_command(
    command: List[str] = typer.Argument(..., help="Command to execute"),
    env_file: Optional[Path] = typer.Option(None, "--env-file", help="Specify a custom .env file (instead of default .env)."),
    secret_key: Optional[str] = typer.Option(None, "--secret-key", help="Key to decrypt secrets."),
    blend_in_os: bool = typer.Option(False, "--blend-in-os", help="Blend the environment variables into os.environ."),
    show_secrets: bool = typer.Option(False, "--show-secrets", help="Include secret variables in the environment."),
):
    """Run a command with the merged environment variables."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Preparing environment...[/bold blue]"),
        transient=True,
    ) as progress:
        progress.add_task("prepare", total=None)
        # Merge the environment variables using load_env
        merged_env = load_env(
            env_file=Path(env_file) if env_file else None, secret_key=secret_key, blend_in_os=blend_in_os, include_secrets=show_secrets, debug=state.debug
        )

    # Prepare the command to be executed
    cmd = [str(arg) for arg in command]
    cmd_display = " ".join(cmd)

    print_info(f"Running command: [bold]{cmd_display}[/bold]")

    # Execute the command in a subshell with the merged environment
    result = subprocess.run(cmd, env=merged_env.to_dict())

    # Show result
    if result.returncode == 0:
        print_success(f"Command completed successfully (exit code: {result.returncode})")
    else:
        print_error(f"Command failed with exit code: {result.returncode}")

    # Exit with the same code as the executed command
    raise typer.Exit(result.returncode)


@app.command()
def install_completions_cmd(shell: str = typer.Argument(..., help="Shell to install completions for (bash, zsh, fish)")):
    """Install shell tab completions for blend-env."""
    supported_shells = ["bash", "zsh", "fish"]
    if shell not in supported_shells:
        print_error(f"Unsupported shell: {shell}. Supported shells: {', '.join(supported_shells)}")
        raise typer.Exit(1)

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn(f"[bold blue]Installing completions for {shell}...[/bold blue]"),
            transient=True,
        ) as progress:
            progress.add_task("install", total=None)
            install_completion(shell)
    except SystemExit as e:
        # Let install_completion handle its own exit messages and codes
        raise typer.Exit(e.code)
    except Exception as e:
        print_error(f"Failed to install completions: {e}")
        raise typer.Exit(1)


@app.command()
def init():
    """Generate the default ~/.config/blend-env structure and files."""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]Initializing blend-env configuration...[/bold blue]"),
            transient=True,
        ) as progress:
            progress.add_task("init", total=None)
            init_blendenv()
    except SystemExit as e:
        raise typer.Exit(e.code)
    except Exception as e:
        print_error(f"Failed to initialize configuration: {e}")
        raise typer.Exit(1)


@app.command("version")
def version_cmd():
    """Show the version of the blend-env package."""
    from . import __version__
    console.print(f"[bold]blend-env[/bold] version: [cyan]{__version__}[/cyan]")
    raise typer.Exit()


# Entry point for the script when run directly (e.g., python -m blend_env.cli)
# Also used by the console script defined in pyproject.toml
def main():
    """Entry point for the CLI application."""
    # Execute the Typer application
    app()


if __name__ == "__main__":
    main()
