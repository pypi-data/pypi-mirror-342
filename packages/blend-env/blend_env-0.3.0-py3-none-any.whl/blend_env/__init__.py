import logging
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, Optional

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("blend-env")

# Check if debug mode is enabled via environment variable
if os.environ.get("BLEND_ENV_DEBUG") == "1":
    logger.setLevel(logging.DEBUG)
    logger.debug("Debug logging enabled via BLEND_ENV_DEBUG environment variable")

from .crypto import decrypt, encrypt, get_or_create_key
from .export import expand_aliases, export_env
from .loader import EnvDict, merge_env
from .scaffold import (
    get_encrypted_secrets_path,
    get_global_env_path,
    get_global_secrets_path,
)


def _parse_env_file_from_args() -> Optional[Path]:
    """Parse --env-file argument from sys.argv if present.

    Returns:
        Optional[Path]: Path to env file specified with --env-file or None
    """
    # Look for --env-file in the command line arguments
    arg_pattern = re.compile(r"--env-file[=\s](.+?)(?:\s|$)")

    for i, arg in enumerate(sys.argv):
        # Check for --env-file=value pattern
        if arg.startswith("--env-file="):
            match = arg_pattern.match(arg)
            if match:
                return Path(match.group(1))

        # Check for --env-file value pattern (separate arguments)
        elif arg == "--env-file" and i + 1 < len(sys.argv):
            return Path(sys.argv[i + 1])

    # No --env-file argument found
    return None


def _parse_secret_key_from_args() -> Optional[str]:
    """Parse --secret-key argument from sys.argv if present.

    Returns:
        Optional[str]: Secret key specified with --secret-key or None
    """
    # Look for --secret-key in the command line arguments
    arg_pattern = re.compile(r"--secret-key[=\s](.+?)(?:\s|$)")

    for i, arg in enumerate(sys.argv):
        # Check for --secret-key=value pattern
        if arg.startswith("--secret-key="):
            match = arg_pattern.match(arg)
            if match:
                return match.group(1)

        # Check for --secret-key value pattern (separate arguments)
        elif arg == "--secret-key" and i + 1 < len(sys.argv):
            return sys.argv[i + 1]

    # No --secret-key argument found
    return None


def _parse_local_only_from_args() -> bool:
    """Check if --local-only flag is present in sys.argv.

    Returns:
        bool: True if --local-only is found, False otherwise
    """
    return "--local-only" in sys.argv


def _parse_blend_in_os_from_args() -> bool:
    """Check if --blend-in-os flag is present in sys.argv.

    Returns:
        bool: True if --blend-in-os is found, False otherwise
    """
    return "--blend-in-os" in sys.argv


def _parse_debug_from_args() -> bool:
    """Check if --debug flag is present in sys.argv.

    Returns:
        bool: True if --debug is found, False otherwise
    """
    return "--debug" in sys.argv


def _parse_include_system_env_from_args() -> bool:
    """Check if --include-system-env flag is present in sys.argv.

    Returns:
        bool: True if --include-system-env is found, False otherwise
    """
    return "--include-system-env" in sys.argv


def load_env(
    global_path: Optional[Path] = None,
    local_path: Optional[Path] = None,
    secrets_path: Optional[Path] = None,
    encrypted_secrets_path: Optional[Path] = None,
    include_secrets: bool = True,
    local_only: bool = False,
    env_file: Optional[Path] = None,  # Parameter for custom .env file
    secret_key: Optional[str] = None,  # Parameter to provide decryption key
    blend_in_os: bool = False,  # Parameter to control whether to blend in os.environ
    debug: bool = False,  # New parameter for debug logging
    clean: bool = True,  # Whether to start with a clean environment or include system env vars
) -> EnvDict:
    """Load and merge environment variables from different sources.

    Args:
        global_path: Path to global .env file (default: ~/.config/blend-env/.env)
        local_path: Path to local .env file (default: ./.env)
        secrets_path: Path to plaintext secrets file (default: ~/.config/blend-env/.secrets)
        encrypted_secrets_path: Path to encrypted secrets file (default: ~/.config/blend-env/.secrets.enc)
        include_secrets: Whether to include secrets in the output (default: True)
        local_only: Whether to only use local environment variables
        env_file: Path to a custom .env file (prioritized over local_path)
        secret_key: Key to decrypt secrets
        blend_in_os: Whether to blend the environment variables into os.environ
        debug: Whether to enable debug logging
        clean: Whether to start with a clean environment (True) or include system environment variables (False)

    Returns:
        EnvDict: Merged environment variables as a dict-like object with get method
    """
    try:
        # Check for debug mode
        if debug or _parse_debug_from_args():
            logger.setLevel(logging.DEBUG)
            logger.debug("Debug logging enabled via parameter or --debug flag")

        # Check for --env-file in command line arguments if not explicitly provided
        if env_file is None:
            cmd_env_file = _parse_env_file_from_args()
            if cmd_env_file is not None:
                env_file = cmd_env_file
                logger.debug(f"Using env file from command line: {env_file}")

        # Check for --show-secrets flag
        if not include_secrets:
            include_secrets = _parse_show_secrets_from_args()
            if include_secrets:
                logger.debug("Including secrets from command line flag")

        # Check for --secret-key parameter
        if not secret_key and include_secrets:
            cmd_secret_key = _parse_secret_key_from_args()
            if cmd_secret_key is not None:
                secret_key = cmd_secret_key
                logger.debug("Using secret key from command line")

        # Check for --local-only flag
        if not local_only:
            local_only = _parse_local_only_from_args()
            if local_only:
                logger.debug("Using local-only mode from command line flag")

        # Check for --blend-in-os flag
        if not blend_in_os:
            blend_in_os = _parse_blend_in_os_from_args()
            if blend_in_os:
                logger.debug("Blending variables into os.environ from command line flag")

        # Check for --include-system-env flag
        if clean:  # Only check if clean is True (default)
            include_system_env = _parse_include_system_env_from_args()
            if include_system_env:
                clean = False
                logger.debug("Including system environment variables from command line flag")

        # Get default paths if not provided
        if not global_path and not local_only:
            global_path = get_global_env_path()
            if not global_path.exists():
                global_path = None
                logger.debug("Global path does not exist")
            else:
                logger.debug(f"Using global path: {global_path}")

        # If env_file is specified, use it instead of the default local .env
        if env_file:
            local_path = env_file
            logger.debug(f"Using env file as local path: {local_path}")
        elif not local_path:  # Only set local_path if not explicitly provided
            local_env = Path(".env")
            if local_env.exists():
                local_path = local_env
                logger.debug(f"Using default local path: {local_path}")

        if not secrets_path and not local_only and include_secrets:
            secrets_path = get_global_secrets_path()
            if not secrets_path.exists():
                secrets_path = None
                logger.debug("Secrets path does not exist")
            else:
                logger.debug(f"Using secrets path: {secrets_path}")

        if not encrypted_secrets_path and not local_only and include_secrets:
            encrypted_secrets_path = get_encrypted_secrets_path()
            if not encrypted_secrets_path.exists():
                encrypted_secrets_path = None
                logger.debug("Encrypted secrets path does not exist")
            else:
                logger.debug(f"Using encrypted secrets path: {encrypted_secrets_path}")

        # Call merge_env with paths and options
        merged_env = merge_env(
            global_path=str(global_path) if global_path else None,
            local_path=str(local_path) if local_path else None,
            secrets_path=str(secrets_path) if secrets_path else None,
            encrypted_secrets_path=(str(encrypted_secrets_path) if encrypted_secrets_path else None),
            include_secrets=include_secrets,
            local_only=local_only,
            secret_key=secret_key,
            clean=clean,
        )

        # Apply to os.environ if blend_in_os is True
        if blend_in_os:
            logger.debug("Applying variables to os.environ")
            for key, value in merged_env.items():
                if value is not None:
                    os.environ[key] = str(value)
                    logger.debug(f"Set os.environ[{key}]")
                elif key in os.environ:
                    del os.environ[key]
                    logger.debug(f"Deleted os.environ[{key}]")

        return merged_env
    except Exception as e:
        logger.error(f"Error during environment processing: {e}")
        raise


# Also parse --show-secrets flag for convenience
def _parse_show_secrets_from_args() -> bool:
    """Check if --show-secrets flag is present in sys.argv.

    Returns:
        bool: True if --show-secrets is found, False otherwise
    """
    return "--show-secrets" in sys.argv


__version__ = "0.3.0"
__all__ = [
    "load_env",
    "merge_env",
    "encrypt",
    "decrypt",
    "get_or_create_key",
    "export_env",
]

# The following functions should not be part of the public API
# They are exposed here for testing purposes only
_all_internal = [
    "_parse_env_file_from_args",
    "_parse_show_secrets_from_args",
    "_parse_secret_key_from_args",
    "_parse_local_only_from_args",
    "_parse_blend_in_os_from_args",
    "_parse_include_system_env_from_args",
]
