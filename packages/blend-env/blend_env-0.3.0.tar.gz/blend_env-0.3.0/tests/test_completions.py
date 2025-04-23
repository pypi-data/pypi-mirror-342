from pathlib import Path

import pytest

from blend_env.completion import (
    END_MARKER,
    START_MARKER,
    _get_shell_config_path,
    install_completion,
)


# Use the mock_home fixture
@pytest.fixture
def mock_home(tmp_path, monkeypatch):
    mock_home_dir = tmp_path / "home" / "testuser"
    mock_home_dir.mkdir(parents=True)
    monkeypatch.setattr(Path, "home", lambda: mock_home_dir)
    # Mock ZDOTDIR environment variable for zsh test
    monkeypatch.setenv("ZDOTDIR", str(mock_home_dir / ".config" / "zsh_custom"))
    return mock_home_dir


def test_get_shell_config_path_bash(mock_home):
    """Test finding the bash config path."""
    path = _get_shell_config_path("bash")
    assert path == mock_home / ".bashrc"


def test_get_shell_config_path_zsh_default(mock_home, monkeypatch):
    """Test finding the zsh config path when ZDOTDIR is not set."""
    monkeypatch.delenv("ZDOTDIR", raising=False)  # Ensure ZDOTDIR is not set
    path = _get_shell_config_path("zsh")
    assert path == mock_home / ".zshrc"


def test_get_shell_config_path_zsh_zdotdir(mock_home):
    """Test finding the zsh config path when ZDOTDIR is set."""
    # ZDOTDIR is set by the mock_home fixture in this case
    zdotdir_path = mock_home / ".config" / "zsh_custom"
    zdotdir_path.mkdir(parents=True, exist_ok=True)  # Ensure dir exists
    path = _get_shell_config_path("zsh")
    assert path == zdotdir_path / ".zshrc"


def test_get_shell_config_path_fish(mock_home):
    """Test finding the fish config path."""
    path = _get_shell_config_path("fish")
    assert path == mock_home / ".config/fish/config.fish"


def test_get_shell_config_path_unsupported(mock_home):
    """Test returning None for an unsupported shell."""
    path = _get_shell_config_path("csh")
    assert path is None


@pytest.mark.parametrize("shell", ["bash", "zsh", "fish"])
def test_install_completion_new_file(mock_home, shell, capsys):
    """Test installing completion when the config file doesn't exist."""
    config_path = _get_shell_config_path(shell)
    assert not config_path.exists()  # Verify it doesn't exist initially

    install_completion(shell)
    captured = capsys.readouterr()

    assert config_path.exists()
    content = config_path.read_text()
    assert START_MARKER in content
    assert END_MARKER in content
    assert f"_BLEND_ENV_COMPLETE={shell}_source" in content
    assert f"Completion installed for {shell}" in captured.out
    assert "Please restart your shell" in captured.out


@pytest.mark.parametrize("shell", ["bash", "zsh", "fish"])
def test_install_completion_append_to_existing(mock_home, shell, capsys):
    """Test installing completion appends to an existing config file."""
    config_path = _get_shell_config_path(shell)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    initial_content = f"# Existing {shell} config\nexport MYVAR=value\n"
    config_path.write_text(initial_content)

    install_completion(shell)
    captured = capsys.readouterr()

    content = config_path.read_text()
    assert content.startswith(initial_content)  # Check it appended
    assert START_MARKER in content
    assert END_MARKER in content
    assert f"_BLEND_ENV_COMPLETE={shell}_source" in content
    assert f"Completion installed for {shell}" in captured.out


@pytest.mark.parametrize("shell", ["bash", "zsh", "fish"])
def test_install_completion_already_installed(mock_home, shell, capsys):
    """Test installing completion when the block already exists."""
    config_path = _get_shell_config_path(shell)
    config_path.parent.mkdir(parents=True, exist_ok=True)

    completion_line = {
        "zsh": 'eval "$(_BLEND_ENV_COMPLETE=zsh_source blendenv)"',
        "bash": 'eval "$(_BLEND_ENV_COMPLETE=bash_source blendenv)"',
        "fish": "eval (env _BLEND_ENV_COMPLETE=fish_source blendenv)",
    }[shell]
    existing_content = f"# Existing stuff\n{START_MARKER}\n{completion_line}\n{END_MARKER}\n# More stuff\n"
    config_path.write_text(existing_content)

    install_completion(shell)
    captured = capsys.readouterr()

    # Content should not change
    assert config_path.read_text() == existing_content
    assert "Completion already installed" in captured.out
    # Should not print the "restart shell" message again
    assert "Please restart your shell" not in captured.out


def test_install_completion_unsupported_shell(mock_home, capsys):
    """Test attempting to install for an unsupported shell."""
    with pytest.raises(SystemExit) as excinfo:
        install_completion("tcsh")

    captured = capsys.readouterr()
    assert excinfo.value.code == 1
    assert "Error: Unsupported shell 'tcsh'" in captured.out


def test_install_completion_write_error(mock_home, monkeypatch, capsys):
    """Test handling of OS errors during file writing."""
    shell = "bash"
    config_path = _get_shell_config_path(shell)

    def mock_write_text_fail(*args, **kwargs):
        raise OSError("Permission denied")

    monkeypatch.setattr(Path, "write_text", mock_write_text_fail)
    monkeypatch.setattr(Path, "exists", lambda self: False)
    monkeypatch.setattr(Path, "read_text", lambda self: "")
    monkeypatch.setattr(Path, "mkdir", lambda self, parents=False, exist_ok=False: None)

    with pytest.raises(SystemExit) as excinfo:
        install_completion(shell)

    captured = capsys.readouterr()
    assert excinfo.value.code == 1
    assert "Error: Could not write to" in captured.err
    assert "Permission denied" in captured.err
