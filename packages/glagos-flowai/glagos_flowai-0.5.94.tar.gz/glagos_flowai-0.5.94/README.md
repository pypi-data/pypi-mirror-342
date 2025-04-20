# FlowAI

FlowAI is a Python-based CLI tool that helps developers streamline their development workflow by automating common tasks using LLMs (Language Learning Models).

## Features

- Generate detailed commit messages from git diffs
- Create comprehensive pull request descriptions
- Perform automated code reviews
- Interactive chat mode with streaming support
- Support for multiple LLM providers:
  - OpenAI
  - Anthropic
  - Groq
  - Gemini
  - Ollama
- Cross-platform compatibility (Windows, Mac, Linux)
- Markdown rendering in terminal
- Streaming responses for real-time feedback
- Configurable output formatting per command

## Command System

FlowAI uses a powerful command system to automate common tasks. Commands are defined in `~/flowai-prompts/prompt-index.txt` and can be customized to your needs.

### Command Features
- Pre-configured context gathering
- Template-based prompts
- Interactive user input
- Platform-specific variants (Windows/Unix)
- Configurable output formatting:
  - `markdown` - Rich formatted output (default)
  - `raw` - Plain text output (ideal for commit messages, PR descriptions)

### Example Commands
```bash
# Generate a commit message for staged changes (raw output)
flowai --command staged-commit-message

# Review code changes (markdown formatted)
flowai --command staged-code-review

# Create PR description (raw output)
flowai --command pull-request
```

## Chat Mode Features

FlowAI's chat mode is a powerful way to interact with the AI assistant. You can:

1. Start a direct chat session:
```bash
flowai --chat
```

2. Turn any command into a chat session by adding `--chat`:
```bash
# Start with a code review and continue chatting about it
flowai --command staged-code-review --chat

# Generate a commit message and discuss it
flowai --command staged-commit-message --chat

# Create a PR description and refine it through chat
flowai --command pull-request --chat
```

When using `--chat` with a command, FlowAI will:
1. Execute the command normally first
2. Use the command's output as context for a new chat session
3. Allow you to discuss, refine, or ask questions about the output
4. Keep the original context (e.g., git diff, code changes) available for reference

### Chat Features
- Stream mode toggle (`/stream`, `/stream on`, `/stream off`)
- Token usage tracking
- Real-time response streaming
- Command system for common operations
- Chat history persistence
- Markdown rendering
- Loading indicators with timing information

### Chat Commands
- `/help` - Show available commands
- `/quit` - Exit chat mode
- `/clear` - Clear chat history
- `/stream` - Toggle stream mode
- `/stream on` - Enable stream mode
- `/stream off` - Disable stream mode

## Known Issues

We are actively working on fixing several issues in the chat mode:
- Ctrl+C handling may not work correctly in some scenarios
- Status display (tokens and stream mode) may not show correctly in some terminals
- Double "Generating response..." message may appear
- Some formatting issues with streamed responses
- Terminal compatibility issues with certain commands

Please check our [TODO.md](TODO.md) file for a complete list of issues being tracked.

## Installation

```bash
pip install flowai
```

## Configuration

Run the initial setup:
```bash
flowai --init
```

This will guide you through:
1. Setting up API keys
2. Choosing your default model
3. Configuring stream mode preferences

## Usage

### Basic Commands
```bash
# Start chat mode
flowai --chat

# pipe output into flowai as context
git diff | flowai "summarise these changes in 1 paragraph"

# ask any question
flowai "how do i do a git rebase? Is it dangerous? Be concise"

# Generate commit message for staged changes (raw output)
flowai --command staged-commit-message

# Review staged changes (markdown formatted)
flowai --command staged-code-review

# Get help (markdown formatted)
flowai --command help

# Get specific help on any flowai feature
flowai --command help "how do i create a custom command that will work in windows and unix style platforms?"
```

### Output Formatting
Commands can be configured to output in either markdown or raw format:
- Markdown format: Rich text with formatting, ideal for reviews and documentation
- Raw format: Plain text, perfect for commit messages and PR descriptions

You can:
1. Set format per command in `prompt-index.txt`
2. Override with `--no-markdown` flag
3. Default to markdown if not specified

### Chat Commands
- `/help` - Show available commands
- `/quit` - Exit chat mode
- `/clear` - Clear chat history
- `/stream` - Toggle stream mode
- `/stream on` - Enable stream mode
- `/stream off` - Disable stream mode

## Contributing

Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License

MIT License - see [LICENSE](LICENSE) for details