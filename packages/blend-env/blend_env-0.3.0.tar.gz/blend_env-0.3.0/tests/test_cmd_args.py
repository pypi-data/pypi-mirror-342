import sys
from pathlib import Path

import pytest

from blend_env import (
    _parse_env_file_from_args,
    _parse_local_only_from_args,
    _parse_secret_key_from_args,
    _parse_show_secrets_from_args,
    load_env,
)


@pytest.fixture
def mock_sys_argv(monkeypatch):
    """Fixture to restore sys.argv after test."""
    original_argv = sys.argv.copy()
    yield monkeypatch
    monkeypatch.setattr(sys, "argv", original_argv)


def test_parse_env_file_equal_syntax(mock_sys_argv):
    """Test parsing --env-file=value syntax."""
    mock_sys_argv.setattr(sys, "argv", ["program", "--env-file=custom.env", "other"])
    assert _parse_env_file_from_args() == Path("custom.env")


def test_parse_env_file_space_syntax(mock_sys_argv):
    """Test parsing --env-file value syntax."""
    mock_sys_argv.setattr(sys, "argv", ["program", "--env-file", "custom.env", "other"])
    assert _parse_env_file_from_args() == Path("custom.env")


def test_parse_env_file_missing(mock_sys_argv):
    """Test parsing when --env-file is not present."""
    mock_sys_argv.setattr(sys, "argv", ["program", "other"])
    assert _parse_env_file_from_args() is None


def test_parse_show_secrets(mock_sys_argv):
    """Test parsing --show-secrets flag."""
    mock_sys_argv.setattr(sys, "argv", ["program", "--show-secrets", "other"])
    assert _parse_show_secrets_from_args() is True


def test_parse_show_secrets_missing(mock_sys_argv):
    """Test parsing when --show-secrets is not present."""
    mock_sys_argv.setattr(sys, "argv", ["program", "other"])
    assert _parse_show_secrets_from_args() is False


def test_parse_secret_key_equal_syntax(mock_sys_argv):
    """Test parsing --secret-key=value syntax."""
    mock_sys_argv.setattr(sys, "argv", ["program", "--secret-key=mysecretkey", "other"])
    assert _parse_secret_key_from_args() == "mysecretkey"


def test_parse_secret_key_space_syntax(mock_sys_argv):
    """Test parsing --secret-key value syntax."""
    mock_sys_argv.setattr(sys, "argv", ["program", "--secret-key", "mysecretkey", "other"])
    assert _parse_secret_key_from_args() == "mysecretkey"


def test_parse_secret_key_missing(mock_sys_argv):
    """Test parsing when --secret-key is not present."""
    mock_sys_argv.setattr(sys, "argv", ["program", "other"])
    assert _parse_secret_key_from_args() is None


def test_parse_local_only(mock_sys_argv):
    """Test parsing --local-only flag."""
    mock_sys_argv.setattr(sys, "argv", ["program", "--local-only", "other"])
    assert _parse_local_only_from_args() is True


def test_parse_local_only_missing(mock_sys_argv):
    """Test parsing when --local-only is not present."""
    mock_sys_argv.setattr(sys, "argv", ["program", "other"])
    assert _parse_local_only_from_args() is False


def test_load_env_with_cmd_args(mock_sys_argv, tmp_path, monkeypatch):
    """Test load_env with command-line arguments."""
    # Create a test .env file
    test_env = tmp_path / "test.env"
    test_env.write_text("TEST_VAR=test_value")

    # Set up command-line arguments
    mock_sys_argv.setattr(
        sys,
        "argv",
        ["program", f"--env-file={test_env}", "--show-secrets", "--local-only"],
    )

    # Change to a directory without .env to ensure our param works
    monkeypatch.chdir(tmp_path)

    # Load environment
    env = load_env()

    # Verify the environment was loaded from the specified file
    assert "TEST_VAR" in env
    assert env["TEST_VAR"] == "test_value"
