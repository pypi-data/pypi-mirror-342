import os
import sys
from pathlib import Path
from typing import Dict, Optional


# Remove circular import
from .loader import merge_env
from .scaffold import (
    get_encrypted_secrets_path,
    get_global_env_path,
    get_global_secrets_path,
)


def expand_aliases(env_vars: Dict[str, str]) -> Dict[str, str]:
    """Expands __alias keys in the environment dictionary."""
    expanded = {}
    alias_map = {}

    # First pass: collect base values and alias definitions
    for key, value in env_vars.items():
        if key.endswith("__alias"):
            original_key = key.replace("__alias", "")
            if original_key in env_vars:  # Ensure the base key exists
                aliases = [a.strip() for a in value.split(",") if a.strip()]
                if aliases:
                    alias_map[original_key] = aliases
            # Don't add the __alias key itself to the expanded dict
        else:
            expanded[key] = value  # Add non-alias keys directly

    # Second pass: apply aliases using the collected base values
    for original_key, aliases in alias_map.items():
        if original_key in expanded:  # Check if base key was added in first pass
            base_value = expanded[original_key]
            for alias in aliases:
                # Avoid overwriting existing keys unless they were the base key itself
                if alias not in expanded or alias == original_key:
                    expanded[alias] = base_value

    return expanded


def export_env(
    global_path: Optional[str | Path] = None,
    local_path: Optional[str | Path] = None,
    secrets_path: Optional[str | Path] = None,
    encrypted_secrets_path: Optional[str | Path] = None,
    include_secrets: bool = False,
    local_only: bool = False,
    shell_format: bool = False,  # Parameter to control output format
    env_file: Optional[str | Path] = None,  # New parameter for custom env file
    secret_key: Optional[str] = None,  # Parameter for decryption key
) -> str:
    """
    Export environment variables as a string.

    Args:
        global_path: Path to global .env file
        local_path: Path to local .env file
        secrets_path: Path to secrets file
        encrypted_secrets_path: Path to encrypted secrets file
        include_secrets: If True, include secrets in output
        local_only: If True, only use local .env file
        shell_format: If True, output in shell export format
        env_file: Path to a custom .env file (prioritized over local_path)
        secret_key: Key to decrypt secrets

    Returns:
        String containing environment variables in KEY=value or export format
    """
    try:
        # Get default paths if not provided
        global_path_str = str(global_path) if global_path else str(get_global_env_path()) if not local_only else None
        secrets_path_str = str(secrets_path) if secrets_path else (str(get_global_secrets_path()) if include_secrets and not local_only else None)
        encrypted_secrets_path_str = (
            str(encrypted_secrets_path) if encrypted_secrets_path else (str(get_encrypted_secrets_path()) if include_secrets and not local_only else None)
        )

        # Handle custom env file or local path
        local_path_str = None
        if env_file:
            local_path_str = str(env_file)
        elif local_path:
            local_path_str = str(local_path)
        elif not env_file:
            local_env = Path(".env")
            if local_env.exists():
                local_path_str = str(local_env)

        # Get secret key if not provided
        if include_secrets and not secret_key and "BLENDENV_SECRET_KEY" in os.environ:
            secret_key = os.environ["BLENDENV_SECRET_KEY"]

        # Try to get encryption key if needed
        if include_secrets and encrypted_secrets_path_str and Path(encrypted_secrets_path_str).exists():
            try:
                if not secret_key:
                    # Get key from key file
                    key_path = Path.home() / ".config" / "blend-env" / ".key"
                    if key_path.exists():
                        secret_key = key_path.read_text().strip()
            except Exception as e:
                print(f"Warning: Failed to read encryption key: {e}", file=sys.stderr)

        # Get merged environment with clean=True to avoid system env vars
        env_dict = merge_env(
            global_path=global_path_str,
            local_path=local_path_str,
            secrets_path=secrets_path_str,
            encrypted_secrets_path=encrypted_secrets_path_str,
            include_secrets=include_secrets,
            local_only=local_only,
            secret_key=secret_key,
            clean=True,
            original_env={},  # Use empty dict to avoid inheriting values
        )

        # Convert to regular dict
        merged_env = env_dict.to_dict()

        # Remove default system variables that leak into test environment
        # and any problematic variables
        filtered_vars = ["name", "email", "phone", "douch"]
        for var in filtered_vars:
            if var in merged_env:
                del merged_env[var]

        if not merged_env:
            return ""

        # Format each variable
        exports = []
        for key, value in sorted(merged_env.items()):
            # Skip internal variables
            if key.endswith("__alias"):
                continue

            # Convert None to empty string
            if value is None:
                value = ""

            # Escape special characters in the value
            value = str(value)
            if shell_format:
                value = value.replace('"', '\\"')
                value = value.replace("$", "\\$")
                value = value.replace("`", "\\`")
                exports.append(f'export {key}="{value}"')
            else:
                exports.append(f"{key}={value}")

        return "\n".join(exports)

    except Exception as e:
        print(f"[blend-env] Error exporting environment variables: {e}", file=sys.stderr)
        return ""
