import base64
import os
from pathlib import Path

import pytest
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Import load_env to test integration
from blend_env import load_env

# Import functions to test from the crypto module
from blend_env.crypto import decrypt, encrypt, get_or_create_key


# Use the mock_home fixture defined in test_merge_env.py (or redefine if needed)
# Make sure the mock_home fixture also patches blend_env.crypto.KEY_PATH
@pytest.fixture
def mock_home(tmp_path, monkeypatch):
    mock_home_dir = tmp_path / "home" / "testuser"
    mock_home_dir.mkdir(parents=True)
    monkeypatch.setattr(Path, "home", lambda: mock_home_dir)

    mock_config_dir = mock_home_dir / ".config" / "blend-env"
    # No need to mkdir here, get_or_create_key should do it
    monkeypatch.setattr("blend_env.loader.DEFAULT_CONFIG_DIR", mock_config_dir)
    monkeypatch.setattr("blend_env.crypto.KEY_PATH", mock_config_dir / ".key")
    monkeypatch.setattr("blend_env.scaffold.CONFIG_DIR", mock_config_dir)
    return mock_home_dir, mock_config_dir


def test_get_or_create_key_creates_new(mock_home):
    """Test that a new key is created, saved, and returned if none exists."""
    mock_home_dir, mock_config_dir = mock_home
    key_path = mock_config_dir / ".key"

    assert not key_path.exists()
    key = get_or_create_key()
    assert isinstance(key, bytes)
    assert len(key) == 32  # AES-256 key length
    assert key_path.exists()
    assert key_path.stat().st_mode & 0o777 == 0o600  # Check permissions

    # Verify content can be decoded
    saved_key_b64 = key_path.read_text().strip()
    decoded_key = base64.urlsafe_b64decode(saved_key_b64)
    assert decoded_key == key


def test_get_or_create_key_reads_existing(mock_home):
    """Test that an existing key is read correctly."""
    mock_home_dir, mock_config_dir = mock_home
    key_path = mock_config_dir / ".key"
    mock_config_dir.mkdir(parents=True, exist_ok=True)  # Ensure dir exists

    # Create a dummy key file
    dummy_key = AESGCM.generate_key(bit_length=256)
    key_path.write_text(base64.urlsafe_b64encode(dummy_key).decode())
    key_path.chmod(0o600)

    read_key = get_or_create_key()
    assert read_key == dummy_key


def test_get_or_create_key_invalid_content(mock_home):
    """Test handling of invalid base64 content in the key file."""
    mock_home_dir, mock_config_dir = mock_home
    key_path = mock_config_dir / ".key"
    mock_config_dir.mkdir(parents=True, exist_ok=True)
    key_path.write_text("this is not base64")

    with pytest.raises(ValueError, match="Invalid key file content"):
        get_or_create_key()


def test_encrypt_decrypt_roundtrip(mock_home):
    """Test that encrypting and then decrypting returns the original content."""
    mock_home_dir, mock_config_dir = mock_home
    # Ensure a key exists
    get_or_create_key()

    original_content = "SECRET_KEY=my_super_secret_value\nANOTHER_SECRET=12345"
    encrypted_data = encrypt(original_content)
    assert isinstance(encrypted_data, bytes)
    assert len(encrypted_data) > len(original_content)  # Nonce + ciphertext + tag

    decrypted_content = decrypt(encrypted_data)
    assert decrypted_content == original_content


def test_decrypt_with_override_key(mock_home):
    """Test decryption using an explicitly provided override key."""
    mock_home_dir, mock_config_dir = mock_home
    # Generate a key but don't save it to the default path
    override_key = AESGCM.generate_key(bit_length=256)

    # Create data with one key
    content = "SOME_DATA=test"
    encrypted_data = encrypt(content)  # Uses default key mechanism

    # Try to decrypt with a different key - should fail
    with pytest.raises((InvalidTag, ValueError, RuntimeError), match="Decryption failed"):
        decrypt(encrypted_data, override_key=override_key)


def test_decrypt_invalid_data_too_short(mock_home):
    """Test decryption failure with data too short to be valid."""
    mock_home_dir, mock_config_dir = mock_home
    get_or_create_key()  # Ensure key exists
    invalid_data = b"short"
    with pytest.raises(ValueError, match="Invalid encrypted data: too short"):
        decrypt(invalid_data)


def test_decrypt_invalid_tag(mock_home):
    """Test decryption failure with corrupted data (invalid tag)."""
    mock_home_dir, mock_config_dir = mock_home
    get_or_create_key()
    original_content = "data=value"
    encrypted_data = encrypt(original_content)

    # Tamper with the ciphertext (e.g., flip a bit in the tag part)
    tampered_data = bytearray(encrypted_data)
    tampered_data[-1] = tampered_data[-1] ^ 1  # Flip last bit
    tampered_data = bytes(tampered_data)

    with pytest.raises((InvalidTag, ValueError), match="Decryption failed"):
        decrypt(tampered_data)


def test_load_env_with_encrypted_secrets(mock_home):
    """Test load_env integration with encrypted secrets file."""
    mock_home_dir, mock_config_dir = mock_home
    mock_config_dir.mkdir(parents=True, exist_ok=True)
    key_path = mock_config_dir / ".key"
    enc_secrets_path = mock_config_dir / ".secrets.enc"

    # 1. Generate key
    key = get_or_create_key()
    assert key_path.exists()
    key_b64 = base64.urlsafe_b64encode(key).decode()  # Convert key to base64 for API

    # 2. Create secrets content and encrypt it
    secrets_content = "ENC_SECRET=encrypted_val\nCOMMON_VAR=enc_common"
    encrypted_data = encrypt(secrets_content)
    enc_secrets_path.write_bytes(encrypted_data)

    # 3. Test load_env without --show-secrets
    merged_no_secrets = load_env(include_secrets=False)
    assert "ENC_SECRET" not in merged_no_secrets
    assert "COMMON_VAR" not in merged_no_secrets

    # 4. Test load_env with --show-secrets and key
    merged_with_secrets = load_env(include_secrets=True, secret_key=key_b64)
    assert "ENC_SECRET" in merged_with_secrets
    assert merged_with_secrets["ENC_SECRET"] == "encrypted_val"
    assert "COMMON_VAR" in merged_with_secrets
    assert merged_with_secrets["COMMON_VAR"] == "enc_common"


def test_load_env_encrypted_secrets_override_key(mock_home):
    """Test load_env with encrypted secrets using BLENDENV_SECRET_KEY override."""
    mock_home_dir, mock_config_dir = mock_home
    mock_config_dir.mkdir(parents=True, exist_ok=True)
    enc_secrets_path = mock_config_dir / ".secrets.enc"

    # 1. Generate a specific key for override
    override_key = AESGCM.generate_key(bit_length=256)
    override_key_b64 = base64.urlsafe_b64encode(override_key).decode()

    # 2. Encrypt secrets content *using the override key*
    secrets_content = "OVERRIDE_SECRET=override_val"
    aesgcm = AESGCM(override_key)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, secrets_content.encode(), None)
    encrypted_with_override = nonce + ct
    enc_secrets_path.write_bytes(encrypted_with_override)

    # 3. Set the environment variable
    os.environ["BLENDENV_SECRET_KEY"] = override_key_b64

    # 4. Test load_env with --show-secrets
    merged_with_secrets = load_env(include_secrets=True, secret_key=override_key_b64)

    # Only check this one key, don't require exact match of entire dict
    assert "OVERRIDE_SECRET" in merged_with_secrets
    assert merged_with_secrets["OVERRIDE_SECRET"] == "override_val"


def test_load_env_encrypted_secrets_wrong_key(mock_home, capsys):
    """Test load_env failure when default key doesn't match encrypted file."""
    mock_home_dir, mock_config_dir = mock_home
    mock_config_dir.mkdir(parents=True, exist_ok=True)
    enc_secrets_path = mock_config_dir / ".secrets.enc"

    # Ensure no leaking variables
    if "BLENDENV_SECRET_KEY" in os.environ:
        del os.environ["BLENDENV_SECRET_KEY"]

    # 1. Generate a specific key and encrypt with it
    wrong_key = AESGCM.generate_key(bit_length=256)
    secrets_content = "CANT_DECRYPT=nope"
    aesgcm = AESGCM(wrong_key)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, secrets_content.encode(), None)
    encrypted_with_wrong_key = nonce + ct
    enc_secrets_path.write_bytes(encrypted_with_wrong_key)

    # 2. Generate the default key (which will be different)
    default_key = get_or_create_key()
    default_key_b64 = base64.urlsafe_b64encode(default_key).decode()

    # 3. Test load_env - should gracefully fail decryption but still return any other
    # environment variables that were loaded
    merged = load_env(include_secrets=True, secret_key=default_key_b64)

    # Should not have decrypted the secret
    assert "CANT_DECRYPT" not in merged
    captured = capsys.readouterr()
    assert "Decryption" in captured.err or "Decryption" in captured.out
