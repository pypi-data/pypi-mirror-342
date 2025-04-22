# FlowAI

G'day! FlowAI is your mate for automating development tasks using LLMs. It's a ripper CLI tool that helps you write better commit messages, pull requests, and code reviews.

## Quick Start

```bash
# Install FlowAI
pipx install glagos-flowai

# Set up your config (you'll need API keys)
flowai --init

# Use predefined commands (easiest way)
flowai --command staged-commit-message  # For staged changes
flowai --command pull-request           # For pull request description
flowai --command code-review           # For code review

# Or use manual mode with prompt files
git diff -w --staged | flowai --prompt-file ~/flowai-prompts/prompt-commit-message.txt
git log main..HEAD | flowai --prompt-file ~/flowai-prompts/prompt-pull-request.txt
git diff -w main..HEAD | flowai --prompt-file ~/flowai-prompts/prompt-code-review.txt
```

## Required API Keys

You'll need at least one of these environment variables set:
- OpenAI: `OPENAI_API_KEY` (get it from https://platform.openai.com/api-keys)
- Anthropic: `ANTHROPIC_API_KEY` (get it from https://console.anthropic.com/settings/keys)
- Groq: `GROQ_API_KEY` (get it from https://console.groq.com/keys)
- Google: `GOOGLE_API_KEY` (get it from https://makersuite.google.com/app/apikey)
- Ollama: No key needed, but install from https://ollama.com

## Common Commands

### Git Workflow

```bash
# Using predefined commands (recommended)
flowai --command staged-commit-message  # Generate commit message for staged changes
flowai --command code-review           # Review code changes
flowai --command pull-request          # Create pull request description (will prompt for base branch)

# Using manual mode with prompt files
git diff -w --staged | flowai --prompt-file ~/flowai-prompts/prompt-commit-message.txt
git diff -w main..HEAD | flowai --prompt-file ~/flowai-prompts/prompt-code-review.txt
git log main..HEAD | flowai --prompt-file ~/flowai-prompts/prompt-pull-request.txt
```

### Predefined Commands

FlowAI comes with several predefined commands that make it easy to perform common tasks:

- `staged-commit-message`: Generate commit message for staged changes
- `main-commit-message`: Generate commit message for all changes
- `pull-request`: Create pull request description (prompts for base branch)
- `staged-code-review`: Review staged changes
- `code-review`: Review all changes

These commands are defined in `~/flowai-prompts/prompt-index.txt` and automatically handle running the right git commands and using the appropriate prompt files.

```bash
# List available commands
cat ~/flowai-prompts/prompt-index.txt

# Use a command
flowai --command pull-request
# When prompted: Input branch name (example: main, dev, staging, etc): main
```

### Model Selection

```bash
# List available models
flowai --list-models

# Use a specific model
flowai --model openai:gpt-4 "Your prompt here"
flowai --model anthropic:claude-3-opus-20240229 "Your prompt here"
flowai --model groq:mixtral-8x7b-32768 "Your prompt here"
flowai --model google:gemini-pro "Your prompt here"
flowai --model ollama:codellama "Your prompt here"
```

### Context Options

```bash
# Use a file as context
flowai --context-file error.log "Analyze this error"

# Use command output as context
flowai --context-shell-command "git diff" "Review these changes"

# Use clipboard content as context
flowai --context-from-clipboard "Summarize this"
```

## Advanced Features

### Custom Prompts

Create your own prompt templates in `~/flowai-prompts/`. See [Creating Custom Prompts](docs/creating-prompts.md) for details.

```bash
# Select a prompt file interactively
flowai --select-prompt-file

# Use a custom prompt file
flowai --prompt-file ~/flowai-prompts/my-custom-prompt.txt
```

### Custom Commands

You can create your own commands by adding them to `~/flowai-prompts/prompt-index.txt`. The file uses a CSV format with four columns:

```csv
label,description,context_command,prompt_file
```

- `label`: The command name (used with --command)
- `description`: A brief description of what the command does
- `context_command`: The shell command to run for context (can include user prompts in [brackets])
- `prompt_file`: Path to the prompt file to use

When adding commands, make sure to:
1. Quote any fields containing special characters (commas, brackets, etc.)
2. Use double quotes (") for quoting fields
3. Escape any double quotes within fields by doubling them ("")

Example of adding a custom command:
```csv
# Add this line to ~/flowai-prompts/prompt-index.txt
"blame-lines","Find who changed specific lines","git blame -L [Enter line range (e.g. 10,20)] [Enter file path]","~/flowai-prompts/my-blame-prompt.txt"
```

Then use it like:
```bash
flowai --command blame-lines
# You'll be prompted for:
# Enter line range (e.g. 10,20): 15,25
# Enter file path: src/main.py
```

### Configuration

```bash
# Check current settings
flowai --status

# Reconfigure FlowAI
flowai --init

# Toggle streaming output
flowai --stream "Watch the response in real-time"
flowai --no-stream "Wait for complete response"
```

FlowAI automatically detects when it has been updated to a new version and will:
1. Notify you about the version change
2. Update configuration and templates automatically
3. Preserve your existing settings (API keys, model preferences)

This ensures you always have the latest templates and documentation while keeping your personal configuration intact.

### Output Formatting

```bash
# Default markdown output
flowai "Format this nicely"

# Plain text output
flowai --no-markdown "Keep it simple"
```

## Troubleshooting

1. **Missing API Keys**
   - Run `flowai --init` to see which providers need API keys
   - Check the provider URLs above to get your keys
   - Add keys to your environment variables

2. **Model Issues**
   - Run `flowai --list-models` to see available models
   - Check if your chosen provider is properly configured
   - Verify your API key has access to the model

3. **Command Not Found**
   - Make sure `pipx` is installed
   - Try reinstalling: `pipx reinstall glagos-flowai`
   - Check your PATH environment variable

4. **Platform Compatibility**
   - Some commands have platform-specific versions (e.g., for Windows vs Unix)
   - FlowAI automatically selects the right version for your platform
   - If you see shell command errors, check if the command needs a platform-specific version
   - See [Commands](docs/commands.md) for details about platform-specific commands

## Contributing

We'd love your help! Here's how you can contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

We especially need help with:
- Adding new LLM providers
- Creating useful prompt templates
- Writing unit tests
- Improving documentation

## License

MIT License - See LICENSE file for details