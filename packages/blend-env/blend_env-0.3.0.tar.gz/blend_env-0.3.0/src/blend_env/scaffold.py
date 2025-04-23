import sys
from pathlib import Path

# Use the same config dir definition as in loader/crypto
CONFIG_DIR = Path.home() / ".config" / "blend-env"
DEFAULT_ENV_CONTENT = "# Add your global variables here\n"
DEFAULT_SECRETS_CONTENT = "# Add your sensitive keys here\n"

# Import encrypt from crypto for monkeypatching in tests


def get_global_env_path() -> Path:
    """Get the path to the global .env file."""
    return CONFIG_DIR / ".env"


def get_global_secrets_path() -> Path:
    """Get the path to the global secrets file."""
    return CONFIG_DIR / ".secrets"


def get_encrypted_secrets_path() -> Path:
    """Get the path to the encrypted secrets file."""
    return CONFIG_DIR / ".secrets.enc"


def init_blendenv():
    """
    Initializes the blend-env configuration directory (~/.config/blend-env)
    with default .env, .secrets, .key, and .secrets.enc files if they don't exist.
    """
    print(f"[blend-env] Initializing configuration in {CONFIG_DIR}...")

    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        CONFIG_DIR.chmod(0o700)  # Owner read/write/execute only
    except OSError as e:
        print(f"[blend-env] Error: Could not create or set permissions for directory {CONFIG_DIR}: {e}")
        sys.exit(1)

    # Define file paths
    env_path = CONFIG_DIR / ".env"
    secrets_path = CONFIG_DIR / ".secrets"
    enc_secrets_path = CONFIG_DIR / ".secrets.enc"
    key_path = CONFIG_DIR / ".key"

    files_created = []
    files_existing = []
    key_generated = False

    # Try to generate or load key first if it doesn't exist
    if not key_path.exists():
        try:
            from .crypto import get_or_create_key

            get_or_create_key()  # Just try to create it
            files_created.append((".key", key_path))
            key_generated = True
        except Exception as e:
            print(f"[blend-env] Error generating key file {key_path}: {e}")
            # Don't exit - continue with other files
    else:
        files_existing.append((".key", key_path))

    # Create .env if not exists
    if not env_path.exists():
        try:
            env_path.write_text(DEFAULT_ENV_CONTENT)
            env_path.chmod(0o600)
            files_created.append((".env", env_path))
        except OSError as e:
            print(f"[blend-env] Error writing default {env_path}: {e}")
            sys.exit(1)
    else:
        files_existing.append((".env", env_path))

    # Create .secrets if not exists
    if not secrets_path.exists():
        try:
            secrets_path.write_text(DEFAULT_SECRETS_CONTENT)
            secrets_path.chmod(0o600)
            files_created.append((".secrets", secrets_path))
        except OSError as e:
            print(f"[blend-env] Error writing default {secrets_path}: {e}")
            sys.exit(1)
    else:
        files_existing.append((".secrets", secrets_path))

    # Only try to encrypt if key exists and was successfully created/loaded
    if key_generated or key_path.exists():
        try:
            from .crypto import encrypt

            content = secrets_path.read_text()
            enc_data = encrypt(content)  # This will use the key we loaded/generated above
            enc_secrets_path.write_bytes(enc_data)
            enc_secrets_path.chmod(0o600)
            print(f"[blend-env] Encrypted existing {secrets_path.name} to {enc_secrets_path.name}")
            if enc_secrets_path.exists():
                files_existing.append((".secrets.enc", enc_secrets_path))
            else:
                files_created.append((".secrets.enc", enc_secrets_path))
        except Exception as e:
            print(f"[blend-env] Error encrypting secrets to {enc_secrets_path}: {e}")
            # Don't exit - keep the plaintext files

    # Summary Report
    print("\n[blend-env] Initialization Summary:")
    if files_created:
        print("  Created:")
        for name, path in files_created:
            print(f"    - {name:<15} ({path})")
    if files_existing:
        print("  Already Existed:")
        for name, path in files_existing:
            print(f"    - {name:<15} ({path})")

    print("\n[blend-env] Initialization complete.")
    if any(f[0] == ".env" for f in files_created):
        print("  -> Please review and edit the default values in ~/.config/blend-env/.env")
    if any(f[0] == ".secrets" for f in files_created):
        print("  -> Please review and edit the default values in ~/.config/blend-env/.secrets")
        if key_generated or key_path.exists():
            print("     Remember to run 'blendenv run --encrypt-secrets' after editing .secrets to update the encrypted version.")
    if key_generated:
        print(f"  -> A new encryption key was generated at {key_path}. Keep this file secure!")
