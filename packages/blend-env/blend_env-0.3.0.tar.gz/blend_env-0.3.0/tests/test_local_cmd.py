import os

import pytest
from typer.testing import CliRunner

from blend_env.cli import local_env


def test_local_set_new_var(typer_runner, mock_home, tmp_path):
    """Test setting a new local variable."""
    # Create a temp directory for the test
    test_dir = tmp_path / "local_set_test"
    test_dir.mkdir()
    os.chdir(str(test_dir))

    # Run the set command
    result = typer_runner.invoke(local_env, "set TEST_VAR=test_value")
    assert "Set local variable: TEST_VAR=test_value" in result.output

    # Verify the file was created with the variable
    local_env_file = test_dir / ".env"
    assert local_env_file.exists()
    content = local_env_file.read_text()
    assert "TEST_VAR=test_value" in content


def test_local_update_existing_var(typer_runner, mock_home, tmp_path):
    """Test updating an existing local variable."""
    # Create a temp directory for the test
    test_dir = tmp_path / "local_update_test"
    test_dir.mkdir()
    os.chdir(str(test_dir))

    # Create a local .env file with an existing variable
    local_env_file = test_dir / ".env"
    local_env_file.write_text("EXISTING_VAR=old_value\nTEST_VAR=initial_value\n")

    # Run the set command
    result = typer_runner.invoke(local_env, "set TEST_VAR=new_value")
    assert "Set local variable: TEST_VAR=new_value" in result.output

    # Verify the file was updated correctly
    content = local_env_file.read_text()
    assert "TEST_VAR=new_value" in content
    assert "EXISTING_VAR=old_value" in content  # Other variables should remain


def test_local_get_existing_var(typer_runner, mock_home, tmp_path):
    """Test getting an existing local variable."""
    # Create a temp directory for the test
    test_dir = tmp_path / "local_get_test"
    test_dir.mkdir()
    os.chdir(str(test_dir))

    # Create a local .env file with a variable
    local_env_file = test_dir / ".env"
    local_env_file.write_text("TEST_VAR=test_value\nANOTHER_VAR=another_value\n")

    # Run the get command
    result = typer_runner.invoke(local_env, "get TEST_VAR")
    # Check that both key and value are in the output
    assert "TEST_VAR" in result.output
    assert "test_value" in result.output


def test_local_get_nonexistent_var(typer_runner, mock_home, tmp_path):
    """Test getting a non-existent local variable."""
    # Create a temp directory for the test
    test_dir = tmp_path / "local_get_nonexistent_test"
    test_dir.mkdir()
    os.chdir(str(test_dir))

    # Create an empty local .env file
    local_env_file = test_dir / ".env"
    local_env_file.touch()

    # Run the get command
    result = typer_runner.invoke(local_env, "get NONEXISTENT_VAR")
    assert "No local variable found matching: NONEXISTENT_VAR" in result.output


def test_local_list_vars(typer_runner, mock_home, tmp_path):
    """Test listing all local variables."""
    # Create a temp directory for the test
    test_dir = tmp_path / "local_list_test"
    test_dir.mkdir()
    os.chdir(str(test_dir))

    # Create a local .env file with multiple variables
    local_env_file = test_dir / ".env"
    local_env_file.write_text("AAA=value1\nBBB=value2\nCCC=value3\n")

    # Run the list command
    result = typer_runner.invoke(local_env, "list")
    # Check for presence of the environment variables in the output
    assert "Local" in result.output
    assert "Environment" in result.output  
    assert "Variables" in result.output
    assert "AAA" in result.output
    assert "value1" in result.output
    assert "BBB" in result.output
    assert "value2" in result.output
    assert "CCC" in result.output
    assert "value3" in result.output


def test_local_pattern_match(typer_runner, mock_home, tmp_path):
    """Test getting variables that match a pattern."""
    # Create a temp directory for the test
    test_dir = tmp_path / "local_pattern_test"
    test_dir.mkdir()
    os.chdir(str(test_dir))

    # Create a local .env file with variables matching a pattern
    local_env_file = test_dir / ".env"
    local_env_file.write_text("PREFIX_AAA=value1\nPREFIX_BBB=value2\nOTHER=value3\n")

    # Run the get command with a pattern
    result = typer_runner.invoke(local_env, "get PREFIX_*")
    # Check for keys and values in the table output
    assert "PREFIX_AAA" in result.output
    assert "PREFIX_BBB" in result.output
    assert "value1" in result.output
    assert "value2" in result.output
    assert "OTHER" not in result.output


def test_local_invalid_set_format(typer_runner, mock_home, tmp_path):
    """Test setting a variable with invalid format."""
    # Create a temp directory for the test
    test_dir = tmp_path / "local_invalid_set_test"
    test_dir.mkdir()
    os.chdir(str(test_dir))

    # Run the set command with invalid format
    result = typer_runner.invoke(local_env, "set INVALID_FORMAT")
    assert "Invalid format" in result.output
    assert "Use KEY=VALUE" in result.output


def test_local_empty_key(typer_runner, mock_home, tmp_path):
    """Test setting a variable with an empty key."""
    # Create a temp directory for the test
    test_dir = tmp_path / "local_empty_key_test"
    test_dir.mkdir()
    os.chdir(str(test_dir))

    # Run the set command with an empty key
    result = typer_runner.invoke(local_env, "set =value")
    assert "Empty key is not allowed" in result.output


def test_local_no_options(typer_runner, mock_home, tmp_path):
    """Test running local command without options."""
    # Create a temp directory for the test
    test_dir = tmp_path / "local_no_options_test"
    test_dir.mkdir()
    os.chdir(str(test_dir))

    # Run the command without options
    result = typer_runner.invoke(local_env)
    assert "Usage:" in result.output


def test_local_create_file_if_not_exists(typer_runner, mock_home, tmp_path):
    """Test that local set creates the .env file if it doesn't exist."""
    # Create a temp directory for the test
    test_dir = tmp_path / "local_create_file_test"
    test_dir.mkdir()
    os.chdir(str(test_dir))

    # Verify the file doesn't exist yet
    local_env_file = test_dir / ".env"
    assert not local_env_file.exists()

    # Run the set command
    result = typer_runner.invoke(local_env, "set NEW_VAR=new_value")
    assert "Set local variable: NEW_VAR=new_value" in result.output

    # Verify the file was created
    assert local_env_file.exists()
    content = local_env_file.read_text()
    assert "NEW_VAR=new_value" in content


def test_local_with_custom_env_file(typer_runner, mock_home, tmp_path):
    """Test using a custom env file."""
    # Create a temp directory for the test
    test_dir = tmp_path / "local_custom_env_test"
    test_dir.mkdir()
    os.chdir(str(test_dir))

    # Create a custom env file path
    custom_env_file = test_dir / "custom.env"

    # Run the set command with custom env file
    result = typer_runner.invoke(
        local_env, f"set TEST_VAR=custom_value --env-file {custom_env_file}"
    )
    assert "Set local variable: TEST_VAR=custom_value" in result.output

    # Verify the custom file was created
    assert custom_env_file.exists()
    content = custom_env_file.read_text()
    assert "TEST_VAR=custom_value" in content

    # Test getting the variable from the custom file
    result = typer_runner.invoke(
        local_env, f"get TEST_VAR --env-file {custom_env_file}"
    )
    # Check that both key and value are in the output
    assert "TEST_VAR" in result.output
    assert "custom_value" in result.output
