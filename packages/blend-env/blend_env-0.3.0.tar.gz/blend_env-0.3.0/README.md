# blend-env v0.3.0

**Blend-env** is a lightweight Python utility that blends:

- A global env file from `~/.config/blend-env/.env`
- A secrets file `.secrets` or `.secrets.enc`
- A project-level `.env` file

Mimics `python-dotenv` but with global config and encryption built in.

GitHub: [github.com/weholt/blend-env](https://github.com/weholt/blend-env)

Current Version: 0.3.0

---

## Features

- Merges environment from global, secret, and project `.env` files
- Secrets are included by default, can be excluded if desired
- Local overrides global and secrets
- `.secrets` can be encrypted to `.secrets.enc`
- CLI support with preview/export
- Shell completions
- Alias support: `foo__alias = bar,baz` duplicates `foo` under those names
- Dict-like object with `.get()` method with support for default values
- Support for custom environment files with `--env-file` option
- Automatic command-line argument parsing when used as a library
- Secure encryption for sensitive secrets
- Global environment variable management via CLI
- Support for debug logging via --debug flag or BLEND_ENV_DEBUG=1

---

## Install

```bash
uv pip install blend-env
```

## Usage

### CLI

```bash
# Initialize the global configuration directory
blend-env init

# Check the package version (the --version flag is not available)
blend-env version

# Preview environment variables without applying them
blend-env run --preview

# Use a custom env file
blend-env run --env-file custom.env

# Install shell completions
blend-env install-completions zsh

# Export environment variables in shell format
blend-env run --export --shell-format

# For CLI commands that don't include secrets by default
blend-env run --show-secrets

# Blend environment variables into os.environ
blend-env run --blend-in-os

# Set a global environment variable
blend-env global --set "API_URL=https://api.example.com"

# Retrieve a global environment variable
blend-env global --get API_URL

# List all global environment variables
blend-env global --list

# Set a local environment variable
blend-env local-env --set "DEBUG=true"

# Retrieve a local environment variable
blend-env local-env --get DEBUG

# List all local environment variables
blend-env local-env --list

# Use a custom env file with local-env
blend-env local-env --set "PORT=8080" --env-file "dev.env"
```

### Python API

```python
from pathlib import Path
from blend_env import load_env

# Load and apply environment variables (includes secrets by default)
env = load_env()

# Access variables with dictionary access
value = env["MY_VAR"]

# Use get() with default values
debug = env.get("DEBUG", "false")
port = env.get("PORT", "8000")

# Use a custom environment file
env = load_env(env_file=Path("custom.env"))

# Exclude secrets from the environment
env = load_env(include_secrets=False)

# Blend environment variables into os.environ
env = load_env(blend_in_os=True)
```

## Managing Global Environment Variables

Blend-env provides a `global` command to manage variables in the global environment file at `~/.config/blend-env/.env`:

### Setting Variables

To add or update a global variable:

```bash
blend-env global --set "API_URL=https://api.example.com"
```

This sets the variable in your global configuration, making it available to all your projects.

### Getting Variables

To retrieve values from the global environment:

```bash
# Get a specific variable
blend-env global --get API_URL

# Get variables matching a pattern
blend-env global --get "API_*"
```

### Listing All Variables

To list all variables in your global environment:

```bash
blend-env global --list
```

## Managing Local Environment Variables

Blend-env provides a `local-env` command to manage variables in the local `.env` file in your current directory:

### Setting Variables

To add or update a local variable:

```bash
blend-env local-env --set "DEBUG=true"
```

If the `.env` file doesn't exist, it will be created automatically.

### Getting Variables

To retrieve values from the local environment:

```bash
# Get a specific variable
blend-env local-env --get DEBUG

# Get variables matching a pattern
blend-env local-env --get "DB_*"
```

### Listing All Variables

To list all variables in your local environment:

```bash
blend-env local-env --list
```

### Using a Custom Environment File

You can specify a different environment file with the `--env-file` option:

```bash
# Set a variable in a custom environment file
blend-env local-env --set "PORT=8080" --env-file "dev.env"

# List variables from a custom environment file
blend-env local-env --list --env-file "dev.env"
```

## Working with Encrypted Secrets

Blend-env provides secure encryption for sensitive secrets like API keys and passwords. 

### Initialize the Configuration

First, initialize the blend-env configuration which creates necessary directories and encryption keys:

```bash
blend-env init
```

This creates a configuration at `~/.config/blend-env/` with:
- `.key` - Encryption key (automatically generated)
- `.env` - Global environment variables
- `.secrets` - Plaintext secrets (create and populate this yourself)
- `.secrets.enc` - Encrypted secrets (generated from plaintext)

### Create and Encrypt Secrets

1. Create a plaintext `.secrets` file:

```bash
echo "API_KEY=your_secret_key" >> ~/.config/blend-env/.secrets
echo "DB_PASSWORD=your_password" >> ~/.config/blend-env/.secrets
```

2. Encrypt your secrets:

```bash
blend-env run --encrypt-secrets
```

3. Access your encrypted secrets:

```bash
# In the CLI, you still need --show-secrets flag with certain commands
blend-env run --show-secrets
blend-env run --preview --show-secrets

# In Python code, secrets are included by default
from blend_env import load_env
env = load_env()
api_key = env["API_KEY"]
```

### Using Encrypted Secrets in Code

```python
from blend_env import load_env

# Load environment with secrets included (default behavior)
env = load_env()

# OR to explicitly exclude secrets 
env = load_env(include_secrets=False)

# Access your secure secret when secrets are included
api_key = env["API_KEY"]
```

### Using a Custom Secret Key

You can specify a custom secret key instead of using the auto-generated one:

```bash
# CLI approach
blend-env run --show-secrets --secret-key="your-secret-key"

# In Python
from blend_env import load_env
env = load_env(secret_key="your-secret-key")
```

## Command-line Arguments When Used as a Library

When you import blend-env in your own application, it automatically recognizes certain command-line arguments:

```bash
# In your application
python your_app.py --env-file=production.env
```

This allows users of your application to specify which environment file to use without any additional code.

Supported command-line arguments:

- `--env-file=file.env` or `--env-file file.env`: Specify a custom environment file
- `--show-secrets`: For the CLI commands that don't include secrets by default (secrets are included by default in the Python API)
- `--local-only`: Only use local environment files (ignore global configuration)
- `--secret-key=key` or `--secret-key key`: Provide a key to decrypt encrypted secrets
- `--debug`: Enable debug logging
- `--blend-in-os`: Update the system's environment variables (os.environ)
- `--include-system-env`: Include system environment variables as a fallback layer

See the [examples directory](examples/) for more details.

## Versioning

blend-env follows semantic versioning:

- Current version: 0.3.0
- Install specific version: `uv pip install blend-env==0.3.0`
- Check version in code: `from blend_env import __version__`

## License

GPL-3.0-or-later — © Thomas Weholt

## Creator

**Thomas Weholt**  
- Website: [weholt.org](https://weholt.org)
- Email: thomas@weholt.org
- GitHub: [github.com/weholt](https://github.com/weholt)

## CLI Command Reference

### Managing Environment Variables

Blend-env provides commands for managing three types of environment variables:

1. **Global variables** - stored in `~/.config/blend-env/.env`
2. **Local variables** - stored in the current directory's `.env` file
3. **Secret variables** - stored in `~/.config/blend-env/.secrets` (encrypted to `.secrets.enc`)

#### Global Variables

```bash
# Set a global variable
blend-env global set "API_URL=https://api.example.com"

# Get a specific global variable 
blend-env global get API_URL

# Get global variables matching a pattern
blend-env global get "DB_*"

# List all global variables
blend-env global list
```

#### Local Variables

```bash
# Set a local variable
blend-env local set "DEBUG=true"

# Get a specific local variable
blend-env local get DEBUG

# Get local variables matching a pattern
blend-env local get "TEST_*"

# List all local variables
blend-env local list

# Work with a custom env file
blend-env local set "PORT=8080" --env-file dev.env
blend-env local get PORT --env-file dev.env
blend-env local list --env-file dev.env
```

#### Secret Variables

```bash
# Set a secret variable (will be encrypted automatically)
blend-env secrets set "API_KEY=super-secret-value"

# Get a specific secret variable
blend-env secrets get API_KEY

# Get secret variables matching a pattern
blend-env secrets get "PASSWORD_*"

# List secret variables (values are masked by default)
blend-env secrets list

# List secret variables showing actual values
blend-env secrets list --show-values
```

### Other Common Commands

```bash
# Initialize the blend-env environment
blend-env init

# Check package version
blend-env version

# Preview all merged variables
blend-env run --preview

# Show variables in a tabular format
blend-env show

# Execute a command with the environment variables applied
blend-env run-command python your_script.py

# Install shell completions
blend-env install-completions-cmd bash
```

### Environment Access with the `get()` Method

When using the Python API, the `env.get()` method works like a standard dictionary's `get()` method, returning the default value if the key is not found:

```python
from blend_env import load_env

env = load_env()

# Access with fallback default
debug_mode = env.get("DEBUG", "false")  # Returns "false" if DEBUG is not set
port = env.get("PORT", "8080")          # Returns "8080" if PORT is not set
```

#### Fallback Behavior

By default, `env.get()` **does not** automatically fall back to checking `os.environ`. However, you can control whether the system environment variables are included in your environment:

```python
# To start with os.environ variables (they will be overridden by .env files)
env = load_env(clean=False)  # Include system environment variables

# To apply loaded variables to os.environ
env = load_env(blend_in_os=True)  # Updates os.environ with all loaded variables
```

When using `clean=False`, the environment is initialized with the current system environment variables. These can then be overridden by global and local .env files. This gives you a full fallback chain:

1. Local .env files (highest priority)
2. Global .env files and secrets
3. System environment variables (when `clean=False`)
4. Default values provided to `get()` method (lowest priority)

When using `blend_in_os=True`, the environment variables are added to `os.environ`, making them available to child processes and through `os.environ.get()`.

#### Command-line Options

You can also control these behaviors through command-line flags:

```bash
# Include system environment variables
python your_script.py --include-system-env

# Apply variables to os.environ
python your_script.py --blend-in-os
```

## Configuration Variables

Blend-env recognizes special configuration variables that can control its behavior. These can be set in system environment, `.env` files, or through API parameters.

### Special Environment Variables

You can set these variables in your `.env` files to control blend-env behavior:

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `BLEND_ENV_INCLUDE_SECRETS` | Whether to include secrets in the merged environment | `True` | `BLEND_ENV_INCLUDE_SECRETS=false` |
| `BLEND_ENV_INCLUDE_SYSTEM_ENV` | Whether to include system environment variables as fallback | `False` | `BLEND_ENV_INCLUDE_SYSTEM_ENV=true` |
| `BLEND_ENV_LOCAL_ONLY` | Whether to only use local .env files (ignore global) | `False` | `BLEND_ENV_LOCAL_ONLY=true` |
| `BLEND_ENV_BLEND_IN_OS` | Whether to update the system environment with loaded variables | `False` | `BLEND_ENV_BLEND_IN_OS=true` |
| `BLEND_ENV_DEBUG` | Enable debug logging | `False` | `BLEND_ENV_DEBUG=true` |

### Usage in Global and Local Config

These variables can be set in both global and local `.env` files, with local settings overriding global ones:

```
# ~/.config/blend-env/.env (global)
BLEND_ENV_INCLUDE_SECRETS=true
BLEND_ENV_DEBUG=true

# ./.env (local, overrides global)
BLEND_ENV_INCLUDE_SECRETS=false
```

### Precedence

Configuration is determined in the following order (highest priority first):

1. Parameters passed directly to `load_env()` in code
2. Command-line flags (e.g., `--include-system-env`)
3. Variables in local `.env` file
4. Variables in global `.env` file
5. System environment variables (e.g., `BLEND_ENV_DEBUG=1`)

### Command-line Flags

For convenience, these configuration variables can also be set through command-line flags:

| Flag | Equivalent Environment Variable |
|------|--------------------------------|
| `--show-secrets` | `BLEND_ENV_INCLUDE_SECRETS=true` |
| `--include-system-env` | `BLEND_ENV_INCLUDE_SYSTEM_ENV=true` |
| `--local-only` | `BLEND_ENV_LOCAL_ONLY=true` |
| `--blend-in-os` | `BLEND_ENV_BLEND_IN_OS=true` |
| `--debug` | `BLEND_ENV_DEBUG=true` |