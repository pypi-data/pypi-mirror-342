import os
import sys
from pathlib import Path
from typing import Optional

# Marker comments to identify lines added by blendenv
START_MARKER = "# BEGIN blendenv completion"
END_MARKER = "# END blendenv completion"


def _get_shell_config_path(shell: str) -> Optional[Path]:
    """Determines the configuration file path for the given shell."""
    home = Path.home()
    shell_name = Path(shell).name  # Extract shell name if full path is given

    if shell_name == "zsh":
        # Check ZDOTDIR first, default to ~/.zshrc
        zdotdir = os.environ.get("ZDOTDIR")
        if zdotdir:
            return Path(zdotdir) / ".zshrc"  # No mkdir - let install_completion handle it
        return home / ".zshrc"
    elif shell_name == "bash":
        return home / ".bashrc"
    elif shell_name == "fish":
        return home / ".config/fish/config.fish"
    else:
        print(f"Error: Unsupported shell '{shell}'", file=sys.stdout)
        return None


def install_completion(shell: str):
    """Installs shell completion script lines into the appropriate config file."""
    profile_path = _get_shell_config_path(shell)
    if not profile_path:
        sys.exit(1)

    # Define the completion command based on the shell (Typer uses different env vars than Click)
    completion_lines = {
        "zsh": f'eval "$(_BLEND_ENV_COMPLETE=zsh_source blend-env)"',
        "bash": f'eval "$(_BLEND_ENV_COMPLETE=bash_source blend-env)"',
        "fish": f"eval (env _BLEND_ENV_COMPLETE=fish_source blend-env)",
    }

    line_to_add = completion_lines.get(Path(shell).name)
    if not line_to_add:
        print(f"[blend-env] Error: Could not determine completion command for shell '{shell}'.", file=sys.stderr)
        sys.exit(1)

    full_block = f"\n{START_MARKER}\n{line_to_add}\n{END_MARKER}\n"

    # Read existing content first
    try:
        content = profile_path.read_text() if profile_path.exists() else ""
    except OSError as e:
        print(f"[blend-env] Error: Could not read {profile_path}: {e}", file=sys.stderr)
        sys.exit(1)

    # Check if block already exists
    if START_MARKER in content and END_MARKER in content:
        print(f"[blend-env] Completion already installed in {profile_path}.")
        return

    # Prepare new content
    if not content.endswith("\n"):
        content += "\n"
    content += full_block

    # Create directory and write file
    try:
        try:
            profile_path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print(f"[blend-env] Error: Could not create directory for {profile_path}: {e}", file=sys.stderr)
            sys.exit(1)

        try:
            # For testing, we need to handle both write_text and open failures
            profile_path.write_text(content)
            profile_path.chmod(0o644)  # Make readable
        except OSError as e:
            print(f"[blend-env] Error: Could not write to {profile_path}: {e}", file=sys.stderr)
            sys.exit(1)

        print(f"Completion installed for {shell} in {profile_path}")
        print("Please restart your shell or source the file (e.g., 'source ~/.zshrc') for changes to take effect.")
    except Exception as e:
        print(f"[blend-env] Error: {e}", file=sys.stderr)
        sys.exit(1)
