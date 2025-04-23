from pathlib import Path

import pytest

from blend_env import load_env


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


def test_include_secrets_default_is_true(mock_home):
    """Test that the default value of include_secrets is True."""
    mock_home_dir, mock_config_dir = mock_home
    mock_config_dir.mkdir(parents=True, exist_ok=True)

    # Create a secret file
    secrets_file = mock_config_dir / ".secrets"
    secrets_file.write_text("TEST_SECRET=secret_value")

    # Load environment without explicitly setting include_secrets
    env = load_env()

    # Verify the secret is included by default
    assert "TEST_SECRET" in env
    assert env["TEST_SECRET"] == "secret_value"

    # For comparison, explicitly set include_secrets=False
    env_no_secrets = load_env(include_secrets=False)

    # Verify the secret is not included when include_secrets=False
    assert "TEST_SECRET" not in env_no_secrets
