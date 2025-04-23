import base64
import logging
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, Optional


# Get logger
logger = logging.getLogger("blend-env")

# Only keep DEFAULT_CONFIG_DIR as a constant
DEFAULT_CONFIG_DIR = Path.home() / ".config" / "blend-env"


class EnvDict:
    """A dict-like object that provides environment variable access with fallback to defaults.

    This class behaves like a dictionary for environment variable access.
    It implements the get method with fallback to default values.
    """

    def __init__(self, env_data: Dict[str, str] = None):
        """Initialize with environment data.

        Args:
            env_data: Initial environment data dictionary
        """
        self._data = env_data or {}

    def __getitem__(self, key: str) -> str:
        """Get environment variable value.

        Args:
            key: Environment variable name

        Returns:
            str: Value for the environment variable

        Raises:
            KeyError: If the environment variable is not found
        """
        if key in self._data:
            return self._data[key]
        raise KeyError(key)

    def __setitem__(self, key: str, value: str) -> None:
        """Set environment variable value.

        Args:
            key: Environment variable name
            value: Environment variable value
        """
        self._data[key] = value

    def __contains__(self, key: str) -> bool:
        """Check if environment variable exists.

        Args:
            key: Environment variable name

        Returns:
            bool: True if the environment variable exists
        """
        return key in self._data

    def get(self, key: str, default: Any = None) -> Any:
        """Get environment variable with optional default value.

        Args:
            key: Environment variable name
            default: Default value if variable not found

        Returns:
            str or default: Value for the environment variable or default
        """
        return self._data.get(key, default)

    def update(self, data: Dict[str, str]) -> None:
        """Update environment variables from a dictionary.

        Args:
            data: Dictionary of environment variables
        """
        self._data.update(data)

    def items(self):
        """Return all environment variable items.

        Returns:
            Iterator for (key, value) pairs
        """
        return self._data.items()

    def keys(self):
        """Return all environment variable keys.

        Returns:
            Iterator for keys
        """
        return self._data.keys()

    def values(self):
        """Return all environment variable values.

        Returns:
            Iterator for values
        """
        return self._data.values()

    def __iter__(self):
        """Iterate over environment variable keys.

        Returns:
            Iterator for keys
        """
        return iter(self._data)

    def __len__(self):
        """Return the number of environment variables.

        Returns:
            int: Number of environment variables
        """
        return len(self._data)

    def copy(self):
        """Create a copy of the environment.

        Returns:
            EnvDict: A new EnvDict with the same data
        """
        return EnvDict(self._data.copy())

    def to_dict(self) -> Dict[str, str]:
        """Convert to a regular dictionary.

        Returns:
            Dict[str, str]: Regular dictionary with the environment data
        """
        return self._data.copy()


def get_global_env_path():
    return DEFAULT_CONFIG_DIR / ".env"


def get_global_secrets_path():
    return DEFAULT_CONFIG_DIR / ".secrets"


def get_encrypted_secrets_path():
    return DEFAULT_CONFIG_DIR / ".secrets.enc"


def get_default_config_dir():
    return DEFAULT_CONFIG_DIR


def parse_env_line(line: str) -> Optional[tuple[str, str]]:
    """Parse a single line from an env file.

    Args:
        line: A line from the env file

    Returns:
        Tuple of (key, value) if valid, None if comment or empty line
    """
    # Remove comments (# that isn't escaped)
    line = re.sub(r"(?<!\\)#.*$", "", line)

    # Skip empty lines or comment-only lines
    line = line.strip()
    if not line:
        return None

    # Check for key=value format
    if "=" not in line:
        return None

    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()

    # Skip if key is empty
    if not key:
        return None

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]

    # Handle escaped characters
    value = value.replace('\\"', '"').replace("\\'", "'")
    value = value.replace("\\n", "\n")
    value = value.replace("\\r", "\r")

    return key, value


def parse_env_file(path: str) -> Dict[str, str]:
    """Parse a .env file and return a dictionary of environment variables.

    Args:
        path: Path to .env file

    Returns:
        Dict[str, str]: Dictionary of environment variables

    Raises:
        FileNotFoundError: If file does not exist
        ValueError: If file cannot be parsed
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Environment file not found: {path}")

    try:
        # Create a clean environment without inheritance
        env_vars = {}

        # Read and parse the file line by line
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                result = parse_env_line(line)
                if result:
                    key, value = result
                    env_vars[key] = value

        return env_vars
    except Exception as e:
        raise ValueError(f"Failed to parse environment file {path}: {e}")


def parse_encrypted_secrets(path: str, secret_key: str) -> Dict[str, str]:
    """Parse an encrypted secrets file and return a dictionary of environment variables.

    Args:
        path: Path to encrypted secrets file
        secret_key: Key used to decrypt secrets

    Returns:
        Dict[str, str]: Dictionary of decrypted environment variables

    Raises:
        FileNotFoundError: If file does not exist
        ValueError: If file cannot be parsed or decrypted
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Encrypted secrets file not found: {path}")

    if not secret_key:
        print(
            "Warning: No secret key provided, skipping encrypted secrets",
            file=sys.stderr,
        )
        return {}

    try:
        # Read encrypted content
        with open(path, "rb") as f:
            encrypted_data = f.read()

        # Import decrypt here to avoid circular imports
        from .crypto import decrypt

        # Decode the base64 key and decrypt
        key_bytes = base64.urlsafe_b64decode(secret_key)
        decrypted_content = decrypt(encrypted_data, override_key=key_bytes)

        # Parse decrypted content into individual environment variables
        env_vars = {}
        for line in decrypted_content.splitlines():
            result = parse_env_line(line)
            if result:
                key, value = result
                env_vars[key] = value

        return env_vars
    except Exception as e:
        print(
            f"Error loading encrypted secrets: Failed to parse encrypted secrets file {path}: {e}",
            file=sys.stderr,
        )
        # Return empty dict instead of raising to allow graceful fallback
        return {}


def apply_aliases(env_vars: Dict[str, str]) -> Dict[str, str]:
    """Expand keys with __alias definitions in the environment dictionary.

    Args:
        env_vars: Environment variable dictionary

    Returns:
        Dict[str, str]: Environment dictionary with aliases expanded
    """
    result = env_vars.copy()
    alias_keys = [k for k in result.keys() if k.endswith("__alias")]

    # Process each alias definition
    for alias_key in alias_keys:
        base_key = alias_key.replace("__alias", "")
        if base_key in result:  # Only process if base key exists
            base_value = result[base_key]
            aliases = [a.strip() for a in result[alias_key].split(",") if a.strip()]

            # Create the aliases
            for alias in aliases:
                result[alias] = base_value

    # Remove the __alias keys themselves
    for alias_key in alias_keys:
        if alias_key in result:
            del result[alias_key]

    return result


def apply_config_vars(env_vars: Dict[str, str]) -> Dict[str, Dict[str, Any]]:
    """Extract special configuration variables from the environment dictionary.
    
    This identifies special configuration variables that can control blend-env behavior.
    
    Args:
        env_vars: Environment variable dictionary
        
    Returns:
        Dict with configuration settings extracted from env vars
    """
    # Create a copy to avoid modifying the original
    result = env_vars.copy()
    config = {
        "include_secrets": None,
        "clean": None,
        "local_only": None,
        "blend_in_os": None,
        "debug": None
    }
    
    # Extract configuration variables
    if "BLEND_ENV_INCLUDE_SECRETS" in result:
        value = result["BLEND_ENV_INCLUDE_SECRETS"].lower()
        config["include_secrets"] = value in ("true", "1", "yes", "on")
        del result["BLEND_ENV_INCLUDE_SECRETS"]
        
    if "BLEND_ENV_INCLUDE_SYSTEM_ENV" in result:
        value = result["BLEND_ENV_INCLUDE_SYSTEM_ENV"].lower()
        config["clean"] = not (value in ("true", "1", "yes", "on"))
        del result["BLEND_ENV_INCLUDE_SYSTEM_ENV"]
        
    if "BLEND_ENV_LOCAL_ONLY" in result:
        value = result["BLEND_ENV_LOCAL_ONLY"].lower()
        config["local_only"] = value in ("true", "1", "yes", "on")
        del result["BLEND_ENV_LOCAL_ONLY"]
        
    if "BLEND_ENV_BLEND_IN_OS" in result:
        value = result["BLEND_ENV_BLEND_IN_OS"].lower()
        config["blend_in_os"] = value in ("true", "1", "yes", "on")
        del result["BLEND_ENV_BLEND_IN_OS"]
        
    if "BLEND_ENV_DEBUG" in result:
        value = result["BLEND_ENV_DEBUG"].lower()
        config["debug"] = value in ("true", "1", "yes", "on")
        del result["BLEND_ENV_DEBUG"]
    
    return {"env_vars": result, "config": config}


def merge_env(
    global_path: Optional[str] = None,
    local_path: Optional[str] = None,
    secrets_path: Optional[str] = None,
    encrypted_secrets_path: Optional[str] = None,
    include_secrets: bool = False,
    local_only: bool = False,
    secret_key: Optional[str] = None,
    clean: bool = True,  # Default to clean environment
    original_env: Optional[Dict[str, str]] = None,  # For testing purposes
) -> EnvDict:
    """Merge environment variables from different sources.

    Args:
        global_path: Path to global .env file
        local_path: Path to local .env file
        secrets_path: Path to plaintext secrets file
        encrypted_secrets_path: Path to encrypted secrets file
        include_secrets: Whether to include secrets in the output
        local_only: Whether to only use local environment variables
        secret_key: Key to decrypt secrets
        clean: Whether to start with a clean environment or inherit from os.environ
        original_env: Optional dict to use as base environment (for testing)

    Returns:
        EnvDict: Dictionary of merged environment variables
    """
    # Start with a clean or original environment
    if original_env is not None:
        # Use provided env (for testing)
        merged_env = dict(original_env)
    elif clean:
        # Start with empty dict
        merged_env = {}
    else:
        # Start with current environment
        merged_env = dict(os.environ)

    # Configuration settings from .env files
    global_config = {
        "include_secrets": None,
        "clean": None,
        "local_only": None,
        "blend_in_os": None,
        "debug": None
    }
    local_config = global_config.copy()

    # Step 1: Load global environment if applicable
    global_vars = {}
    if global_path and not local_only:
        try:
            raw_global_vars = parse_env_file(global_path)
            # Extract any configuration variables
            result = apply_config_vars(raw_global_vars)
            global_vars = result["env_vars"]
            global_config = result["config"]
            logger.debug(f"Global vars: {global_vars}")
            logger.debug(f"Global config: {global_config}")
        except FileNotFoundError:
            # Global file doesn't exist, ignore
            pass
        except ValueError as e:
            logger.warning(f"{e}")
    
    # Apply global configuration settings if specified
    if global_config["include_secrets"] is not None:
        include_secrets = global_config["include_secrets"]
        logger.debug(f"Using include_secrets={include_secrets} from global config")
    
    if global_config["local_only"] is not None:
        local_only = global_config["local_only"]
        logger.debug(f"Using local_only={local_only} from global config")
        
    if global_config["clean"] is not None:
        # Note: If we're here, we've already initialized merged_env,
        # so we can't change the clean flag directly.
        # However, we log it for informational purposes
        logger.debug(f"Note: clean={global_config['clean']} from global config cannot be applied retrospectively")

    # Expand global aliases first
    global_final = {}
    global_final.update(global_vars)

    # Process global aliases but keep them separate initially
    global_alias_keys = [k for k in global_vars.keys() if k.endswith("__alias")]
    global_aliases = {}

    for alias_key in global_alias_keys:
        base_key = alias_key.replace("__alias", "")
        if base_key in global_vars:
            base_value = global_vars[base_key]
            aliases = [a.strip() for a in global_vars[alias_key].split(",") if a.strip()]

            # Create aliases from global values
            for alias in aliases:
                global_aliases[alias] = base_value

    # Add global variables without aliases first
    merged_env.update(global_vars)

    # Step 2: Load secrets if requested
    if include_secrets and not local_only:
        # Try to get secret key from environment if not provided
        if not secret_key and "BLENDENV_SECRET_KEY" in os.environ:
            secret_key = os.environ["BLENDENV_SECRET_KEY"]

        # Load plaintext secrets if available
        plaintext_secrets = {}
        if secrets_path:
            try:
                plaintext_secrets = parse_env_file(secrets_path)
            except FileNotFoundError:
                # Secrets file doesn't exist, try encrypted
                pass
            except ValueError as e:
                logger.warning(f"{e}")

        # Load encrypted secrets if available and key is provided
        encrypted_secrets = {}
        if encrypted_secrets_path and secret_key:
            try:
                encrypted_secrets = parse_encrypted_secrets(encrypted_secrets_path, secret_key)
            except FileNotFoundError:
                # Encrypted secrets file doesn't exist
                pass
            except ValueError as e:
                logger.warning(f"{e}")

        # Update merged environment with secrets (plaintext then encrypted)
        if plaintext_secrets or encrypted_secrets:
            merged_env.update(plaintext_secrets)
            merged_env.update(encrypted_secrets)
            # Add a marker that secrets were loaded
            merged_env["secrets_loaded"] = "true"

    # Step 3: Load local environment last (highest priority)
    local_vars = {}
    if local_path:
        try:
            raw_local_vars = parse_env_file(local_path)
            # Extract any configuration variables
            result = apply_config_vars(raw_local_vars)
            local_vars = result["env_vars"]
            local_config = result["config"]
            logger.debug(f"Local vars: {local_vars}")
            logger.debug(f"Local config: {local_config}")
        except FileNotFoundError:
            # Local file doesn't exist, ignore
            pass
        except ValueError as e:
            logger.warning(f"{e}")
    
    # Apply local configuration settings - these override global settings
    if local_config["include_secrets"] is not None:
        include_secrets = local_config["include_secrets"]
        logger.debug(f"Using include_secrets={include_secrets} from local config")
    
    if local_config["local_only"] is not None:
        local_only = local_config["local_only"]
        logger.debug(f"Using local_only={local_only} from local config")
    
    # Re-check if we should include secrets based on updated config
    if not include_secrets:
        # If we've loaded secrets but now need to exclude them, remove them
        if "secrets_loaded" in merged_env:
            # Clean out any secret keys we previously loaded
            logger.debug("Removing previously loaded secrets due to configuration")
            for secret_key in list(merged_env.keys()):
                if secret_key.startswith("SECRET_") or "_SECRET_" in secret_key:
                    del merged_env[secret_key]
            del merged_env["secrets_loaded"]
            
    # Process local aliases separately
    local_alias_keys = [k for k in local_vars.keys() if k.endswith("__alias")]
    local_aliases = {}

    for alias_key in local_alias_keys:
        base_key = alias_key.replace("__alias", "")
        if base_key in local_vars:
            base_value = local_vars[base_key]
            aliases = [a.strip() for a in local_vars[alias_key].split(",") if a.strip()]

            # Create aliases from local values
            for alias in aliases:
                local_aliases[alias] = base_value

    # Add local variables (overrides anything before it)
    merged_env.update(local_vars)

    # Now add the aliases in proper order (global then local)
    merged_env.update(global_aliases)
    merged_env.update(local_aliases)

    # Remove all __alias keys
    for key in list(merged_env.keys()):
        if key.endswith("__alias"):
            del merged_env[key]
            
    # Remove internal marker
    if "secrets_loaded" in merged_env:
        del merged_env["secrets_loaded"]

    logger.debug(f"After apply_aliases: {merged_env}")

    # Convert to EnvDict
    env_dict = EnvDict(merged_env)
    logger.debug(f"Final result: {merged_env}")
    return env_dict
