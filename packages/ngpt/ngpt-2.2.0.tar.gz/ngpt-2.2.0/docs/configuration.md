# Configuration Guide

nGPT uses a flexible configuration system that supports multiple profiles for different API providers and models. This guide explains how to configure and manage your nGPT settings.

## Configuration File Location

nGPT stores its configuration in a JSON file located at:

- **Linux**: `~/.config/ngpt/ngpt.conf` or `$XDG_CONFIG_HOME/ngpt/ngpt.conf`
- **macOS**: `~/Library/Application Support/ngpt/ngpt.conf`
- **Windows**: `%APPDATA%\ngpt\ngpt.conf`

## Configuration Structure

The configuration file uses a JSON list format that allows you to store multiple configurations. Each configuration entry is a JSON object with the following fields:

```json
[
  {
    "api_key": "your-openai-api-key-here",
    "base_url": "https://api.openai.com/v1/",
    "provider": "OpenAI",
    "model": "gpt-4o"
  },
  {
    "api_key": "your-groq-api-key-here",
    "base_url": "https://api.groq.com/openai/v1/",
    "provider": "Groq",
    "model": "llama3-70b-8192"
  },
  {
    "api_key": "your-optional-ollama-key",
    "base_url": "http://localhost:11434/v1/",
    "provider": "Ollama-Local",
    "model": "llama3"
  }
]
```

### Configuration Fields

- **api_key**: Your API key for the service
- **base_url**: The base URL for the API endpoint
- **provider**: A human-readable name for the provider (used for display purposes)
- **model**: The default model to use with this configuration

## Managing Configurations Programmatically

You can manipulate configurations programmatically using the configuration module:

```python
from ngpt.config import load_config, get_config_path, get_config_dir

# Get the directory where configs are stored
config_dir = get_config_dir()

# Get the path to the config file
config_path = get_config_path()

# Load a specific configuration (default is index 0)
config = load_config(config_index=0)

# Use the configuration
print(f"Using {config['provider']} with model {config['model']}")
```

## Configuration Priority

nGPT determines configuration values in the following order (highest priority first):

1. **Command-line arguments**: When specified directly with `--api-key`, `--base-url`, `--model`, etc.
2. **Environment variables**: 
   - `OPENAI_API_KEY` 
   - `OPENAI_BASE_URL`
   - `OPENAI_MODEL`
3. **Configuration file**: Selected configuration (by default, index 0)
4. **Default values**: Fall back to built-in defaults

## Interactive Configuration

You can configure nGPT interactively using the CLI:

```bash
# Add a new configuration
ngpt --config

# Edit an existing configuration at index 1
ngpt --config --config-index 1

# Remove a configuration at index 2
ngpt --config --remove --config-index 2
```

The interactive configuration will prompt you for values and guide you through the process.

## Command-Line Configuration

You can also set configuration options directly via command-line arguments:

```bash
# Use specific API key, base URL, and model for a single command
ngpt --api-key "your-key" --base-url "https://api.example.com/v1/" --model "custom-model" "Your prompt here"

# Select a specific configuration by index
ngpt --config-index 2 "Your prompt here"

# Control response generation parameters
ngpt --temperature 0.8 --top_p 0.95 --max_length 300 "Write a creative story"
```

## Environment Variables

You can set the following environment variables to override configuration:

```bash
# Set API key
export OPENAI_API_KEY="your-api-key"

# Set base URL
export OPENAI_BASE_URL="https://api.alternative.com/v1/"

# Set model
export OPENAI_MODEL="alternative-model"
```

These will take precedence over values in the configuration file but can be overridden by command-line arguments.

## Checking Current Configuration

To see your current configuration:

```bash
# Show active configuration
ngpt --show-config

# Show all configurations
ngpt --show-config --all
```

## Examples

### Using Multiple Providers

The multiple configuration support allows you to easily switch between different providers:

```bash
# Use OpenAI (config at index 0)
ngpt --config-index 0 "Tell me about quantum computing"

# Use Groq (config at index 1)
ngpt --config-index 1 "Tell me about quantum computing"

# Use local Ollama (config at index 2)
ngpt --config-index 2 "Tell me about quantum computing"
```

### Programmatically Loading Configurations

In your Python code, you can load and use different configurations:

```python
from ngpt import NGPTClient, load_config

# Load OpenAI configuration
openai_config = load_config(config_index=0)
openai_client = NGPTClient(**openai_config)

# Load Groq configuration
groq_config = load_config(config_index=1)
groq_client = NGPTClient(**groq_config)

# Use the clients
openai_response = openai_client.chat("Hello from OpenAI")
groq_response = groq_client.chat("Hello from Groq")
```

For more details on using the library, see the [Library Usage](usage/library_usage.md) guide. 