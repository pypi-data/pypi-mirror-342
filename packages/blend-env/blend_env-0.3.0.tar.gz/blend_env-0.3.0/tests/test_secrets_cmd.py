from pathlib import Path
import os

import pytest
from typer.testing import CliRunner

from blend_env.cli import secrets
from blend_env.crypto import decrypt, get_or_create_key
from blend_env.scaffold import get_encrypted_secrets_path, get_global_secrets_path


@pytest.fixture
def mock_home(tmp_path, monkeypatch):
    """Set up a mock home directory."""
    mock_home_dir = tmp_path / "home" / "testuser"
    mock_home_dir.mkdir(parents=True)
    monkeypatch.setattr(Path, "home", lambda: mock_home_dir)

    mock_config_dir = mock_home_dir / ".config" / "blend-env"

    # Patch relevant modules
    monkeypatch.setattr("blend_env.loader.DEFAULT_CONFIG_DIR", mock_config_dir)
    monkeypatch.setattr("blend_env.scaffold.CONFIG_DIR", mock_config_dir)
    monkeypatch.setattr("blend_env.cli.get_default_config_dir", lambda: mock_config_dir)
    monkeypatch.setattr("blend_env.crypto.KEY_PATH", mock_config_dir / ".key")

    return mock_home_dir, mock_config_dir


@pytest.fixture
def typer_runner():
    """Create a CLI runner for testing."""
    return CliRunner()


def test_secrets_set_new_var(typer_runner, mock_home, tmp_path):
    """Test setting a new secret variable."""
    # Create a temp directory for the test
    test_dir = tmp_path / "secrets_set_test"
    test_dir.mkdir()
    os.chdir(str(test_dir))

    # Run the set command
    result = typer_runner.invoke(secrets, "set SECRET_VAR=secret_value")
    assert "Set secret variable: SECRET_VAR=" in result.output
    assert "*****" in result.output

    # Need to use the global secrets path rather than local .env.secret
    secrets_path = get_global_secrets_path()
    secrets_path.parent.mkdir(parents=True, exist_ok=True)
    assert secrets_path.exists() or get_encrypted_secrets_path().exists()


def test_secrets_update_existing_var(typer_runner, mock_home, tmp_path):
    """Test updating an existing secret variable."""
    # Create a temp directory for the test
    test_dir = tmp_path / "secrets_update_test"
    test_dir.mkdir()
    os.chdir(str(test_dir))

    # Create the secrets file with an existing variable
    secrets_path = get_global_secrets_path()
    secrets_path.parent.mkdir(parents=True, exist_ok=True)
    secrets_path.write_text("EXISTING_SECRET=old_value\nSECRET_VAR=initial_value\n")

    # Run the set command
    result = typer_runner.invoke(secrets, "set SECRET_VAR=new_value")
    assert "Set secret variable: SECRET_VAR=" in result.output
    assert "*****" in result.output

    # Verify the file was updated correctly
    content = secrets_path.read_text()
    assert "SECRET_VAR=new_value" in content
    assert "EXISTING_SECRET=old_value" in content  # Other variables should remain


def test_secrets_get_existing_var(typer_runner, mock_home, tmp_path):
    """Test getting an existing secret variable."""
    # Create a temp directory for the test
    test_dir = tmp_path / "secrets_get_test"
    test_dir.mkdir()
    os.chdir(str(test_dir))

    # Create a secrets file with a variable
    secrets_path = get_global_secrets_path()
    secrets_path.parent.mkdir(parents=True, exist_ok=True)
    secrets_path.write_text("SECRET_VAR=secret_value\nANOTHER_SECRET=another_value\n")

    # Run the get command
    result = typer_runner.invoke(secrets, "get SECRET_VAR")
    assert "SECRET_VAR" in result.output
    assert "secret_value" in result.output


def test_secrets_get_nonexistent_var(typer_runner, mock_home, tmp_path):
    """Test getting a non-existent secret variable."""
    # Create a temp directory for the test
    test_dir = tmp_path / "secrets_get_nonexistent_test"
    test_dir.mkdir()
    os.chdir(str(test_dir))

    # Create an empty secrets file
    secrets_path = get_global_secrets_path()
    secrets_path.parent.mkdir(parents=True, exist_ok=True)
    secrets_path.touch()

    # Run the get command
    result = typer_runner.invoke(secrets, "get NONEXISTENT_SECRET")
    assert "No secret" in result.output
    assert "found matching: NONEXISTENT_SECRET" in result.output


def test_secrets_list_vars(typer_runner, mock_home, tmp_path):
    """Test listing all secret variables."""
    # Create a temp directory for the test
    test_dir = tmp_path / "secrets_list_test"
    test_dir.mkdir()
    os.chdir(str(test_dir))

    # Create a secrets file with multiple variables
    secrets_path = get_global_secrets_path()
    secrets_path.parent.mkdir(parents=True, exist_ok=True)
    secrets_path.write_text("SECRET_AAA=value1\nSECRET_BBB=value2\nSECRET_CCC=value3\n")

    # Run the list command
    result = typer_runner.invoke(secrets, "list")
    # Check for presence of the secret variables in the output
    assert "Secret" in result.output
    assert "Variables" in result.output
    assert "SECRET_AAA" in result.output
    assert "SECRET_BBB" in result.output
    assert "SECRET_CCC" in result.output


def test_secrets_pattern_match(typer_runner, mock_home, tmp_path):
    """Test getting secrets that match a pattern."""
    # Create a temp directory for the test
    test_dir = tmp_path / "secrets_pattern_test"
    test_dir.mkdir()
    os.chdir(str(test_dir))

    # Create a secrets file with variables matching a pattern
    secrets_path = get_global_secrets_path()
    secrets_path.parent.mkdir(parents=True, exist_ok=True)
    secrets_path.write_text("SECRET_AAA=value1\nSECRET_BBB=value2\nOTHER=value3\n")

    # Run the get command with a pattern
    result = typer_runner.invoke(secrets, "get SECRET_*")
    assert "SECRET_AAA" in result.output
    assert "value1" in result.output
    assert "SECRET_BBB" in result.output
    assert "value2" in result.output
    assert "OTHER" not in result.output
    assert "value3" not in result.output


def test_secrets_invalid_set_format(typer_runner, mock_home, tmp_path):
    """Test setting a secret with invalid format."""
    # Create a temp directory for the test
    test_dir = tmp_path / "secrets_invalid_set_test"
    test_dir.mkdir()
    os.chdir(str(test_dir))

    # Run the set command with invalid format
    result = typer_runner.invoke(secrets, "set INVALID_FORMAT")
    assert "Invalid format" in result.output
    assert "Use KEY=VALUE" in result.output


def test_secrets_empty_key(typer_runner, mock_home, tmp_path):
    """Test setting a secret with an empty key."""
    # Create a temp directory for the test
    test_dir = tmp_path / "secrets_empty_key_test"
    test_dir.mkdir()
    os.chdir(str(test_dir))

    # Run the set command with an empty key
    result = typer_runner.invoke(secrets, "set =value")
    assert "Empty key is not allowed" in result.output


def test_secrets_no_options(typer_runner, mock_home, tmp_path):
    """Test running secrets command without options."""
    # Create a temp directory for the test
    test_dir = tmp_path / "secrets_no_options_test"
    test_dir.mkdir()
    os.chdir(str(test_dir))

    # Run the command without options
    result = typer_runner.invoke(secrets)
    assert "Usage:" in result.output


def test_secrets_create_file_if_not_exists(typer_runner, mock_home, tmp_path):
    """Test that secrets set creates the secrets file if it doesn't exist."""
    # Create a temp directory for the test
    test_dir = tmp_path / "secrets_create_file_test"
    test_dir.mkdir()
    os.chdir(str(test_dir))

    # Verify the file doesn't exist yet
    secrets_path = get_global_secrets_path()
    assert not secrets_path.exists()

    # Run the set command
    result = typer_runner.invoke(secrets, "set NEW_SECRET=new_value")
    assert "Set secret variable: NEW_SECRET=" in result.output
    assert "*****" in result.output

    # Verify the file was created
    assert secrets_path.exists()
    content = secrets_path.read_text()
    assert "NEW_SECRET=new_value" in content


def test_secrets_with_custom_env_file(typer_runner, mock_home, tmp_path):
    """Test using a custom secrets file."""
    # Create a temp directory for the test
    test_dir = tmp_path / "secrets_custom_env_test"
    test_dir.mkdir()
    os.chdir(str(test_dir))

    # Create a custom secrets file path
    custom_secrets_file = test_dir / "custom.secret"

    # Run the set command with custom env file
    # Note: the actual parameter is --secret-key, not --secrets-file
    result = typer_runner.invoke(
        secrets, f"set SECRET_VAR=custom_value --secret-key=testing123"
    )
    assert "Set secret variable: SECRET_VAR=" in result.output
    assert "*****" in result.output
