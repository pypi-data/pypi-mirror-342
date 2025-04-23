from pathlib import Path

import pytest
from typer.testing import CliRunner

from blend_env.cli import global_env
from blend_env.scaffold import get_global_env_path


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

    return mock_home_dir, mock_config_dir


@pytest.fixture
def typer_runner():
    """Create a CLI runner for testing."""
    return CliRunner()


def test_global_set_new_var(typer_runner, mock_home):
    """Test setting a new global variable."""
    mock_home_dir, mock_config_dir = mock_home
    mock_config_dir.mkdir(parents=True, exist_ok=True)

    # Run the set command 
    result = typer_runner.invoke(global_env, "set TEST_VAR=test_value")
    assert "Set global variable: TEST_VAR=test_value" in result.output

    # Verify the file was created with the variable
    global_env_file = get_global_env_path()
    assert global_env_file.exists()
    content = global_env_file.read_text()
    assert "TEST_VAR=test_value" in content


def test_global_update_existing_var(typer_runner, mock_home):
    """Test updating an existing global variable."""
    mock_home_dir, mock_config_dir = mock_home
    mock_config_dir.mkdir(parents=True, exist_ok=True)

    # Create the global .env file with an existing variable
    global_env_file = get_global_env_path()
    global_env_file.parent.mkdir(parents=True, exist_ok=True)
    global_env_file.write_text("EXISTING_VAR=old_value\nTEST_VAR=initial_value\n")

    # Run the set command to update a variable
    result = typer_runner.invoke(global_env, "set TEST_VAR=new_value")
    assert "Set global variable: TEST_VAR=new_value" in result.output

    # Verify the file was updated correctly
    content = global_env_file.read_text()
    assert "TEST_VAR=new_value" in content
    assert "EXISTING_VAR=old_value" in content  # Other variables should remain


def test_global_get_existing_var(typer_runner, mock_home):
    """Test getting an existing global variable."""
    mock_home_dir, mock_config_dir = mock_home
    mock_config_dir.mkdir(parents=True, exist_ok=True)

    # Create the global .env file with a variable
    global_env_file = get_global_env_path()
    global_env_file.parent.mkdir(parents=True, exist_ok=True)
    global_env_file.write_text("TEST_VAR=test_value\nANOTHER_VAR=another_value\n")

    # Run the get command
    result = typer_runner.invoke(global_env, "get TEST_VAR")
    # Check that both key and value are in the output
    assert "TEST_VAR" in result.output
    assert "test_value" in result.output


def test_global_get_nonexistent_var(typer_runner, mock_home):
    """Test getting a non-existent global variable."""
    mock_home_dir, mock_config_dir = mock_home
    mock_config_dir.mkdir(parents=True, exist_ok=True)

    # Create an empty global .env file
    global_env_file = get_global_env_path()
    global_env_file.parent.mkdir(parents=True, exist_ok=True)
    global_env_file.touch()

    # Run the get command for a non-existent variable
    result = typer_runner.invoke(global_env, "get NONEXISTENT_VAR")
    assert "No global variable found matching: NONEXISTENT_VAR" in result.output


def test_global_list_vars(typer_runner, mock_home):
    """Test listing all global variables."""
    mock_home_dir, mock_config_dir = mock_home
    mock_config_dir.mkdir(parents=True, exist_ok=True)

    # Create the global .env file with multiple variables
    global_env_file = get_global_env_path()
    global_env_file.parent.mkdir(parents=True, exist_ok=True)
    global_env_file.write_text("AAA=value1\nBBB=value2\nCCC=value3\n")

    # Run the list command
    result = typer_runner.invoke(global_env, "list")
    # Check for presence of the environment variables in the output
    assert "Global" in result.output
    assert "Environment" in result.output  
    assert "Variables" in result.output
    assert "AAA" in result.output
    assert "value1" in result.output
    assert "BBB" in result.output
    assert "value2" in result.output
    assert "CCC" in result.output
    assert "value3" in result.output


def test_global_pattern_match(typer_runner, mock_home):
    """Test getting variables that match a pattern."""
    mock_home_dir, mock_config_dir = mock_home
    mock_config_dir.mkdir(parents=True, exist_ok=True)

    # Create the global .env file with variables matching a pattern
    global_env_file = get_global_env_path()
    global_env_file.parent.mkdir(parents=True, exist_ok=True)
    global_env_file.write_text("PREFIX_AAA=value1\nPREFIX_BBB=value2\nOTHER=value3\n")

    # Run the get command with a pattern
    result = typer_runner.invoke(global_env, "get PREFIX_*")
    # Check for keys and values in the table output 
    assert "PREFIX_AAA" in result.output
    assert "PREFIX_BBB" in result.output
    assert "value1" in result.output
    assert "value2" in result.output
    assert "OTHER" not in result.output


def test_global_invalid_set_format(typer_runner, mock_home):
    """Test setting a variable with invalid format."""
    mock_home_dir, mock_config_dir = mock_home
    mock_config_dir.mkdir(parents=True, exist_ok=True)

    # Run the set command with invalid format
    result = typer_runner.invoke(global_env, "set INVALID_FORMAT")
    assert "Invalid format" in result.output
    assert "Use KEY=VALUE" in result.output


def test_global_empty_key(typer_runner, mock_home):
    """Test setting a variable with an empty key."""
    mock_home_dir, mock_config_dir = mock_home
    mock_config_dir.mkdir(parents=True, exist_ok=True)

    # Run the set command with an empty key
    result = typer_runner.invoke(global_env, "set =value")
    assert "Empty key is not allowed" in result.output


def test_global_no_options(typer_runner, mock_home):
    """Test running global command without options."""
    mock_home_dir, mock_config_dir = mock_home
    mock_config_dir.mkdir(parents=True, exist_ok=True)

    # Run the command without options
    result = typer_runner.invoke(global_env)
    assert "Usage:" in result.output
