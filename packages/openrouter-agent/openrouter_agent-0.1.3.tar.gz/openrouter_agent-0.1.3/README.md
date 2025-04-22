# OpenRouter Agent for Pydantic AI

A Python library that extends the Pydantic AI framework to support OpenRouter models.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Configuring Your API Key via Environment Variable](#configuring-your-api-key-via-environment-variable)
  - [Method 1: Using a `.env` File (Recommended for Projects)](#method-1-using-a-env-file-recommended-for-projects)
  - [Method 2: Setting Temporarily in Your Terminal Session](#method-2-setting-temporarily-in-your-terminal-session)
- [Usage](#usage)
  - [Command Line Interface](#command-line-interface)
  - [Python API Example](#python-api-example)
  - [Custom Configuration](#custom-configuration)
- [Class Reference](#class-reference)
  - [OpenRouterModel](#openroutermodel)
  - [OpenRouterAgent](#openrouteragent)
- [Environment Variables](#environment-variables)
- [Available Models](#available-models)
- [License](#license)

## Overview

This package provides integration between [Pydantic AI](https://github.com/pydantic-ai/pydantic-ai) and [OpenRouter](https://openrouter.ai/), allowing you to use any model available on OpenRouter with the Pydantic AI framework. The implementation leverages the OpenAI-compatible API provided by OpenRouter.

## Installation

```bash
# Install from the repository in editable mode to make changes
pip install -e .

# Or you can install through PyPi
pip install openrouter-agent
```

You'll also need to set up your OpenRouter API key. You can either:

1. Set the `OPENROUTER_API_KEY` environment variable
2. Pass the API key directly when initializing the agent

## Configuring Your API Key via Environment Variable

Using an environment variable (`OPENROUTER_API_KEY`) is the recommended way to provide your API key securely. Here’s how you can set it:

### Method 1: Using a `.env` File (Recommended for Projects)

This method keeps your key associated with your project without hardcoding it.

1. **Create or Copy:** In your project's main directory, create a file named `.env`. If your project includes a `.env-sample` or `.env.example` file, you can copy it to `.env`.
2. **Add Your Key:** Open the `.env` file and add the following line, replacing `your_actual_api_key` with the key you generated on [OpenRouter Keys](https://openrouter.ai/settings/keys):

   ```dotenv
   OPENROUTER_API_KEY=your_actual_api_key
   ```

3. **Load the Variable:** For your Python code to access this variable, you usually need a library like `python-dotenv`. Install it (`pip install python-dotenv`) and load it early in your script:

   ```python
   from dotenv import load_dotenv
   load_dotenv()
   # Now os.getenv("OPENROUTER_API_KEY") or libraries that check env vars will find it.
   ```

   _(Note: Some frameworks or tools might load `.env` files automatically.)_

### Method 2: Setting Temporarily in Your Terminal Session

This is useful for quick tests but needs to be done every time you open a new terminal session.

1. **Get Your Key:** Copy your API key from [OpenRouter Keys](https://openrouter.ai/settings/keys).
2. **Run the Command:** Execute the command specific to your terminal, replacing `your_actual_api_key` with your key:

   - **Linux, macOS, Git Bash (or other sh-like shells):**

     ```bash
     export OPENROUTER_API_KEY='your_actual_api_key'
     ```

   - **Windows Command Prompt (cmd.exe):**

     ```cmd
     set OPENROUTER_API_KEY=your_actual_api_key
     ```

   - **Windows PowerShell:**

     ```powershell
     $env:OPENROUTER_API_KEY = 'your_actual_api_key'
     ```

3. **Run Your Code:** Now you can run your Python script or the `openrouter-agent` CLI command from the _same_ terminal window.

**Important:** Avoid committing your `.env` file (if it contains secrets) to version control like Git. Add `.env` to your `.gitignore` file.

## Usage

### Command Line Interface

The package includes a command-line interface (CLI) that allows you to generate and execute shell commands:

```bash
# Install the package with CLI support
pip install .

# Generate a command without executing it (copies to clipboard)
openrouter-agent query "show me all .txt files in the current directory"

# Generate and execute a command
openrouter-agent execute "show me all .txt files in the current directory"
```

Or run directly with Python:

```bash
# Generate a command without executing it (copies to clipboard)
python src/cli.py query "show me all .txt files in the current directory"

# Generate and execute a command
python src/cli.py execute "show me all .txt files in the current directory"
```

### Python API Example

```python
from openrouter_agent import Agent

# Initialize with default settings (uses openrouter/quasar-alpha model)
agent = Agent()

# Run a simple completion
result = agent.run("What is the capital of France?")
print(result)
```

You can also import the specific classes if needed:

```python
from openrouter_agent import OpenRouterAgent, OpenRouterModel
```

### Custom Configuration

```python
from openrouter_agent import Agent

# Initialize with custom settings
agent = Agent(
    agent_name="explanation_agent",
    system_prompt="You are a helpful assistant that explains complex topics in simple terms.",
    openrouter_model_name="anthropic/claude-3-opus-20240229",
    temp=0.7,
    max_result_retries=5,
    openrouter_api_key="your-api-key-here"  # Or use environment variable
)

# Use the agent
result = agent.run_sync("Explain quantum computing in simple terms.")
print(result.data)
```

## Class Reference

### OpenRouterModel

The `OpenRouterModel` class inherits from `OpenAIModel` and configures it to work with OpenRouter:

```python
OpenRouterModel(
    openrouter_model_name: str = "openrouter/quasar-alpha",
    openrouter_url: str = "https://openrouter.ai/api/v1",
    openrouter_api_key: Optional[str] = os.getenv("OPENROUTER_API_KEY")
)
```

### OpenRouterAgent

The `OpenRouterAgent` class inherits from Pydantic AI's `Agent` class and uses `OpenRouterModel` for completions:

```python
OpenRouterAgent(
    agent_name: str = uuid.uuid4().hex,  # Auto-generates a UUID if not provided
    openrouter_model_name: str = "openrouter/quasar-alpha",
    temp: float = 0.1,
    max_result_retries: int = 10,
    openrouter_url: str = "https://openrouter.ai/api/v1",
    openrouter_api_key: Optional[str] = os.getenv("OPENROUTER_API_KEY"),
    instrument: bool = True,
    **kwargs: Any  # Additional arguments passed to the Agent constructor
)
```

## Environment Variables

- `OPENROUTER_API_KEY`: Your OpenRouter API key

## Available Models

You can use any model available on OpenRouter by specifying its identifier in the `openrouter_model_name` parameter. Some popular free options include:

**Note**: You must use a model that supports tools to use the cli application, the following free models all do.

- `openrouter/quasar-alpha` (default)
- `google/gemini-2.5-pro-exp-03-25:free`
- `google/gemini-2.0-flash-exp:free`
- `google/gemini-flash-1.5-8b-exp`
- `mistralai/mistral-small-3.1-24b-instruct:free`

Check the [OpenRouter documentation](https://openrouter.ai/docs) for a complete list of available models.

## License

[MIT](LICENSE)
