import base64
import logging
import os
from pathlib import Path
from typing import Optional

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Get logger
logger = logging.getLogger("blend-env")

# Define the path for the encryption key relative to the user's home config
KEY_PATH = Path.home() / ".config" / "blend-env" / ".key"


def get_or_create_key(override_key: Optional[str] = None) -> bytes:
    """
    Retrieves the AES key from KEY_PATH or creates a new one if it doesn't exist.
    Ensures the parent directory exists.

    Args:
        override_key: Optional string key to use instead of reading from file

    Returns:
        bytes: The encryption key as bytes
    """
    try:
        # If override_key is provided, use it instead of reading from file
        if override_key is not None:
            try:
                # Try to decode as base64 first
                key = base64.urlsafe_b64decode(override_key)
                # Ensure it has the correct length
                if len(key) != 32:  # 256 bits = 32 bytes
                    raise ValueError("Key must be 256 bits (32 bytes)")
                return key
            except (ValueError, TypeError, base64.binascii.Error):
                # If not a valid base64 string, use it as a password - derive a key with PBKDF2
                from cryptography.hazmat.primitives import hashes
                from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

                salt = b"blend-env-salt"  # A consistent salt
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,  # 256-bit key
                    salt=salt,
                    iterations=100000,  # High iteration count for security
                )
                return kdf.derive(override_key.encode())

        if KEY_PATH.exists():
            key_b64 = KEY_PATH.read_text().strip()
            if not key_b64:
                raise ValueError("Key file is empty.")
            key = base64.urlsafe_b64decode(key_b64)
            # Ensure it has the correct length
            if len(key) != 32:  # 256 bits = 32 bytes
                raise ValueError("Key must be 256 bits (32 bytes)")
            return key
        else:
            logger.info(f"Key file not found at {KEY_PATH}. Generating a new key.")
            key = AESGCM.generate_key(bit_length=256)
            # Ensure the directory exists before writing
            KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
            KEY_PATH.write_text(base64.urlsafe_b64encode(key).decode())
            # Set restrictive permissions (read/write for owner only)
            KEY_PATH.chmod(0o600)
            logger.info(f"New key generated and saved to {KEY_PATH}.")
            return key
    except (ValueError, TypeError, base64.binascii.Error) as e:
        logger.error(f"Error reading or decoding key file at {KEY_PATH}: {e}")
        raise ValueError(f"Invalid key file content at {KEY_PATH}.") from e
    except OSError as e:
        logger.error(f"Error accessing key file at {KEY_PATH}: {e}")
        raise OSError(f"Could not access key file at {KEY_PATH}.") from e


def encrypt(content: str, override_key: Optional[str] = None) -> bytes:
    """
    Encrypts the given string content using AES-GCM with the managed key.

    Args:
        content: The content to encrypt
        override_key: Optional string key to use instead of the default key

    Returns:
        bytes: The encrypted data
    """
    try:
        key = get_or_create_key(override_key)
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)  # GCM standard nonce size
        # Ensure content is bytes
        content_bytes = content.encode("utf-8")
        ct = aesgcm.encrypt(nonce, content_bytes, None)  # No associated data
        # Prepend nonce to ciphertext for storage/transmission
        return nonce + ct
    except Exception as e:
        logger.error(f"Encryption failed: {e}")
        # Re-raise the exception to signal failure
        raise RuntimeError("Encryption process failed.") from e


def decrypt(data: bytes, override_key: Optional[bytes] = None) -> str:
    """
    Decrypts the given bytes using AES-GCM.
    Uses the override_key if provided, otherwise fetches the managed key.
    """
    if len(data) < 12:
        raise ValueError("Invalid encrypted data: too short to contain nonce.")

    try:
        key = override_key if override_key is not None else get_or_create_key()
        aesgcm = AESGCM(key)
        nonce = data[:12]
        ct = data[12:]

        try:
            decrypted_bytes = aesgcm.decrypt(nonce, ct, None)
            return decrypted_bytes.decode("utf-8")
        except InvalidTag:
            logger.error("Decryption failed: Invalid authentication tag. Key might be incorrect or data corrupted.")
            # Re-raise the InvalidTag with our message
            raise InvalidTag("Decryption failed: Invalid authentication tag")
        except Exception as e:
            logger.error(f"Decryption failed: {str(e)}")
            raise ValueError(f"Decryption failed: {str(e)}")
    except Exception as e:
        logger.error(f"Decryption process failed: {str(e)}")
        raise ValueError(f"Decryption process failed: {str(e)}")
