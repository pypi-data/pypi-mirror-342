import typer
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.live import Live
from rich.table import Table
import questionary
from questionary import Choice
from typing import Optional, Dict, Any
import time
import sys
import re
import select
from difflib import get_close_matches
import shutil
from pathlib import Path
import os
if os.name == 'nt':  # Windows
    import msvcrt
import subprocess
import pyperclip
import importlib.resources as pkg_resources
from importlib.resources import files, as_file
import importlib.metadata
import traceback
import csv
from markdown_it import MarkdownIt

from .config_manager import ConfigManager
from .llm_connector import LLMConnector
from .chat_manager import ChatManager
import flowai  # Import the package to access resources

app = typer.Typer(add_completion=False)
console = Console()

# Initialize markdown parser
md_parser = MarkdownIt("commonmark", {"breaks": True})

from flowai import __version__

# Global dictionary for provider URLs
provider_urls = {
    "gemini": "https://ai.google.dev/gemini-api/docs/api-key",
    "anthropic": "https://docs.anthropic.com/en/api/getting-started",
    "openai": "https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key",
    "groq": "https://console.groq.com/docs/api-keys",
    "ollama": "https://www.ollama.com"
}

def get_available_models(config):
    available_models = {}
    llm_connector = None
    try:
        llm_connector = LLMConnector(config)

        for provider in ["openai", "anthropic", "groq", "gemini", "ollama"]:
            try:
                models = llm_connector.get_available_models(provider)
                # Skip test models in listings
                if models and "Error fetching models" not in models[0] and provider != "test":
                    available_models[provider] = [f"{provider}/{model}" for model in models]
                elif provider == "ollama" and "Error fetching models" in models[0]:
                    console.print(f"[yellow]Ollama is not installed. Go to {provider_urls['ollama']} to install it.[/yellow]")
                elif "No API key set" in models[0]:
                    console.print(f"[yellow]No API key detected for {provider}. See {provider_urls[provider]} to set one.[/yellow]")
                elif "Error fetching models" in models[0]:
                    console.print(f"[red]Error fetching models for {provider}[/red]")
            except Exception as e:
                print(f"\nError while fetching {provider} models:", file=sys.stderr)
                traceback.print_exc()

    except Exception as e:
        print("\nError initializing LLM connector:", file=sys.stderr)
        traceback.print_exc()

    return available_models

def check_version():
    """Check if the installed version matches the config version and trigger updates if needed."""
    config_dir = Path.home() / ".config" / "flowai"
    version_file = config_dir / "VERSION"
    current_version = __version__

    try:
        needs_update = False
        if not version_file.exists():
            console.print("\n[bold yellow]First time running this version of FlowAI![/bold yellow]")
            console.print("[yellow]Setting up templates and documentation...[/yellow]\n")
            needs_update = True
        else:
            with open(version_file, 'r') as f:
                installed_version = f.read().strip()

            if installed_version != current_version:
                console.print(f"\n[bold yellow]FlowAI has been updated from v{installed_version} to v{current_version}![/bold yellow]")
                console.print("[yellow]Updating templates and documentation...[/yellow]\n")
                needs_update = True

        return needs_update
    except Exception as e:
        console.print(f"[yellow]Warning: Could not check version: {str(e)}[/yellow]")
        return False

def update_files():
    """Update template and documentation files without changing configuration."""
    config_dir = Path.home() / ".config" / "flowai"
    prompts_dir = Path.home() / "flowai-prompts"
    docs_dir = config_dir / "docs"

    for directory in [prompts_dir, config_dir, docs_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    # Copy prompt files from the package resources
    prompt_files = ["prompt-commit-message.txt", "prompt-pull-request.txt", "prompt-code-review.txt", "prompt-index.txt", "prompt-help.txt"]
    for prompt_file in prompt_files:
        try:
            with pkg_resources.as_file(pkg_resources.files('flowai.prompts') / prompt_file) as prompt_path:
                shutil.copy(prompt_path, prompts_dir / prompt_file)
        except Exception as e:
            console.print(f"[yellow]Warning: Could not copy {prompt_file}: {str(e)}[/yellow]")

    # Copy documentation files
    try:
        docs_path = pkg_resources.files('flowai.docs')
        for doc_file in [p for p in docs_path.iterdir() if p.name.endswith('.md')]:
            with pkg_resources.as_file(doc_file) as doc_path:
                shutil.copy(doc_path, docs_dir / doc_path.name)
    except Exception as e:
        console.print(f"[yellow]Warning: Could not copy documentation files: {str(e)}[/yellow]")

    # Update version file
    try:
        with open(config_dir / "VERSION", 'w') as f:
            f.write(__version__)
    except Exception as e:
        console.print(f"[yellow]Warning: Could not write version file: {str(e)}[/yellow]")

    console.print(f"\n[bold green]Template files copied to {prompts_dir}[/bold green]")
    console.print(f"[bold green]Documentation files copied to {docs_dir}[/bold green]")

def init_config():
    """Full initialization including model selection and file updates."""
    config_manager = ConfigManager()
    config = config_manager.load_config()

    # Ensure all necessary keys are present with default values
    default_config = {
        'default_model': 'openai/gpt-3.5-turbo',
        'openai_api_key': '',
        'anthropic_api_key': '',
        'groq_api_key': '',
        'google_api_key': '',
        'ollama_base_url': 'http://localhost:11434',
        'stream_mode': 'true'
    }

    for key, value in default_config.items():
        if key not in config['DEFAULT']:
            config['DEFAULT'][key] = value

    current_model = config['DEFAULT']['default_model']
    current_stream_mode = config.getboolean('DEFAULT', 'stream_mode')

    console.print(Panel.fit(
        f"[bold green]Welcome to FlowAI {__version__}![/bold green]\n\n"
        "flowai is a CLI tool for multi-agent LLM tasks. It allows you to interact with "
        "various Language Models from different providers and NOT manage complex, multi-step tasks.\n\n"
        f"[bold blue]Current configuration:[/bold blue]\n"
        f"Model: [yellow]{current_model}[/yellow]\n"
        f"Stream mode: [yellow]{'On' if current_stream_mode else 'Off'}[/yellow]"
    ))

    available_models = get_available_models(config)

    # Prepare choices for providers with valid API keys
    provider_choices = []
    for provider, models in available_models.items():
        if models and models[0] not in [f"{provider}/No API key set", "Error fetching models"]:
            provider_choices.append(Choice(provider, value=provider))
        elif models[0] == f"{provider}/No API key set":
            console.print(f"[yellow]No API key detected for {provider}. See {provider_urls[provider]} to set one.[/yellow]")
        elif models[0] == "Error fetching models":
            console.print(f"[yellow]Error fetching models for {provider}. Please check your configuration.[/yellow]")

    if not provider_choices:
        console.print("[bold red]No models available. Please set at least one API key and try again.[/bold red]")
        for provider, url in provider_urls.items():
            console.print(f"[yellow]For {provider}, visit: {url}[/yellow]")
        return

    # First level: Select provider
    selected_provider = questionary.select(
        "Select a provider:",
        choices=provider_choices
    ).ask()

    if not selected_provider:
        console.print("[bold red]No provider selected. Exiting configuration.[/bold red]")
        return

    # Second level: Select model from the chosen provider
    model_choices = [model.split('/', 1)[1] for model in available_models[selected_provider]]
    current_model = config['DEFAULT']['default_model']
    current_model_name = current_model.split('/', 1)[1] if '/' in current_model else current_model

    selected_model = questionary.select(
        f"Select a model from {selected_provider}:",
        choices=model_choices,
        default=current_model_name if current_model_name in model_choices else model_choices[0]
    ).ask()

    if not selected_model:
        console.print("[bold red]No model selected. Exiting configuration.[/bold red]")
        return

    # When setting the default model
    default_model = f"{selected_provider}/{selected_model}"

    console.print(f"\n[bold green]Selected model: {default_model}[/bold green]")

    stream_mode = questionary.confirm("Enable stream mode by default?", default=config.getboolean('DEFAULT', 'stream_mode')).ask()

    # Update the config
    config['DEFAULT'] = {
        'default_model': default_model,
        'stream_mode': str(stream_mode).lower(),
        'openai_api_key': config.get('DEFAULT', 'openai_api_key', fallback=''),
        'anthropic_api_key': config.get('DEFAULT', 'anthropic_api_key', fallback=''),
        'groq_api_key': config.get('DEFAULT', 'groq_api_key', fallback=''),
        'google_api_key': config.get('DEFAULT', 'google_api_key', fallback=''),
        'ollama_base_url': config.get('DEFAULT', 'ollama_base_url', fallback='http://localhost:11434')
    }
    config_manager.save_config(config)
    console.print(f"\n[bold green]Configuration updated![/bold green]")

    console.print(f"Your config file is located at: {config_manager.config_file}")
    console.print("You can update these values by editing the file or by running 'flowai --init' again.")

    # Update files after configuration
    update_files()

def is_input_available():
    if os.name == 'nt':  # Windows
        return msvcrt.kbhit()
    else:  # Unix-based systems (Mac, Linux)
        return select.select([sys.stdin], [], [], 0.0)[0]

def generate_status_table(elapsed_time):
    table = Table.grid(padding=(0, 1))
    table.add_row(
        "[bold green]Generating response...",
        f"[bold blue]Elapsed time: {elapsed_time:.3f}s"
    )
    return table

def parse_prompt_index():
    """Parse the prompt index file using proper CSV parsing to handle commas in values."""
    prompts_dir = Path.home() / "flowai-prompts"
    index_file = prompts_dir / "prompt-index.txt"

    if not index_file.exists():
        raise ValueError("Prompt index file not found. Please run 'flowai --init' to set up the prompts directory.")

    commands = {}
    with open(index_file, 'r') as f:
        # Use csv module to properly handle commas within fields
        reader = csv.DictReader(f)
        for row in reader:
            label = row['label']
            # Handle platform-specific commands
            if ':' in label:
                platform, cmd = label.split(':', 1)
                # Check for valid platform prefixes
                if platform not in ['win', 'unix']:
                    console.print(f"[yellow]Warning: Invalid platform prefix '{platform}' in command '{label}'. Valid prefixes are 'win:' and 'unix:'.[/yellow]")
                    continue
                # Skip if not for current platform
                if platform == 'win' and os.name != 'nt':
                    continue
                if platform == 'unix' and os.name == 'nt':
                    continue
                # Store without platform prefix
                label = cmd

            # Replace ~ with actual home directory in prompt file path
            prompt_file = row['prompt_file'].replace('~', str(Path.home()))

            # Replace ~ with %USERPROFILE% in context command for Windows
            context_command = row['context_command']
            if os.name == 'nt':
                context_command = context_command.replace('~', '%USERPROFILE%')
            else:
                context_command = context_command.replace('~', str(Path.home()))

            # Get format value if it exists, validate it
            format_value = row.get('format', '').lower()
            if format_value and format_value not in ['raw', 'markdown']:
                console.print(f"[yellow]Warning: Invalid format value '{format_value}' in command '{label}'. Valid values are 'raw' or 'markdown'.[/yellow]")
                format_value = ''

            # Get user_input value if it exists
            user_input = row.get('user_input', '').strip()

            commands[label] = {
                'description': row['description'],
                'context_command': context_command,
                'prompt_file': prompt_file,
                'format': format_value,
                'user_input': user_input
            }
    return commands

def handle_user_prompts(command_str):
    """Extract user prompts from command string and get user input."""
    prompt_pattern = r'\[(.*?)\]'
    matches = re.finditer(prompt_pattern, command_str)

    for match in matches:
        prompt_text = match.group(1)
        user_input = questionary.text(f"{prompt_text}: ").ask()
        if user_input is None:
            raise typer.Abort()
        command_str = command_str.replace(f"[{prompt_text}]", user_input)

    # Show the command that will be run
    if command_str:
        console.print(f"\n[bold blue]Running command:[/bold blue] [cyan]{command_str}[/cyan]\n")

    return command_str

def display_available_commands():
    """Display available commands in a user-friendly way using Rich."""
    try:
        commands = parse_prompt_index()

        console.print("\n[bold green]G'day! Here are the available FlowAI commands:[/bold green]\n")

        table = Table(show_header=True, header_style="bold blue", show_lines=True)
        # Set column widths: command (25%), description (35%), context (40%)
        table.add_column("Command", style="yellow", ratio=1)
        table.add_column("Description", style="white", ratio=2)
        table.add_column("Context Source", style="cyan", ratio=3)

        for cmd, info in commands.items():
            context_source = info['context_command']
            if '[' in context_source:
                # Use Rich's markup for highlighting
                context_source = re.sub(r'\[(.*?)\]', r'[yellow]\[\1][/yellow]', context_source)

            table.add_row(cmd, info['description'], context_source)

        console.print(table)
        console.print("\n[bold green]To use a command:[/bold green]")
        console.print("  flowai --command [purple]<command-name>[/purple]")
        console.print("\n[bold green]Example:[/bold green]")
        console.print("  flowai --command pull-request")
        console.print("\n[italic]Note: [yellow]Yellow[/yellow] highlights in Context Source indicate where you'll be prompted for input[/italic]\n")

    except Exception as e:
        if "Prompt index file not found" in str(e):
            console.print("[bold yellow]No commands available. Run 'flowai --init' to set up command templates.[/bold yellow]")
        else:
            raise e

def list_commands_callback(ctx: typer.Context, param: typer.CallbackParam, value: str) -> Optional[str]:
    """Callback to handle --command with no value"""
    if value is None:
        display_available_commands()
        raise typer.Exit()
    return value

def first_run_onboarding(config_manager: ConfigManager):
    """Handle first-time user onboarding with a friendly introduction and setup guidance."""
    config = config_manager.load_config()

    welcome_md = f"""# Welcome to FlowAI! 🚀

G'day! Thanks for trying out FlowAI, your AI-powered development assistant.

## What is FlowAI?

FlowAI helps you automate common development tasks using AI, such as:
- Generating detailed commit messages from your changes
- Creating comprehensive pull request descriptions
- Performing automated code reviews
- And much more!

## Getting Started

FlowAI supports multiple AI providers:
| Provider | Status | API Key Link |
|----------|---------|--------------|"""

    # Check which providers have API keys
    has_api_keys = False
    provider_status = []

    for provider, url in provider_urls.items():
        key = f"{provider}_api_key".upper()  # Environment variables are uppercase
        if provider == "ollama":
            status = "✅ No key needed" if shutil.which("ollama") else "❌ Not installed"
        else:
            # Check both config and environment variables
            has_key = bool(config.get('DEFAULT', key.lower(), fallback='')) or bool(os.environ.get(key, ''))
            status = "✅ Configured" if has_key else "❌ Not configured"
            has_api_keys = has_api_keys or has_key

        provider_status.append(f"| {provider.capitalize()} | {status} | {url} |")

    welcome_md += "\n" + "\n".join(provider_status)

    if not has_api_keys:
        welcome_md += """

## Next Steps

1. Set up at least one API key from the providers above
2. Set the API key as an environment variable:
   ```bash
   # For OpenAI
   export OPENAI_API_KEY=your_key_here

   # For Anthropic
   export ANTHROPIC_API_KEY=your_key_here

   # For Groq
   export GROQ_API_KEY=your_key_here

   # For Gemini
   export GOOGLE_API_KEY=your_key_here

   # For Ollama
   # Just install from ollama.com
   ```
3. Run `flowai --init` to configure your preferred model

## Getting Help

- Run `flowai --command help` to get help with any topic
- Run `flowai --command list` to see available commands
- Visit our documentation at https://github.com/glagol-space/flowai
"""
    else:
        welcome_md += """

Great! You already have some API keys configured. Let's set up your preferred model.
"""

    # Display the welcome message
    console.print(Markdown(welcome_md))

    if has_api_keys:
        # If they have API keys, run the init process
        console.print("\n[yellow]Running initial setup...[/yellow]")
        init_config()
    else:
        # Just update files without running init
        update_files()
        console.print("\n[yellow]Run 'flowai --init' after setting up your API keys to complete the setup.[/yellow]")

def get_shell():
    """Get the user's shell with fallbacks for containers and minimal environments."""
    # Windows doesn't use this function
    if os.name == 'nt':
        return 'cmd.exe'

    # Try environment variables in order of preference
    if 'BASH' in os.environ and os.path.exists(os.environ['BASH']):
        return os.environ['BASH']

    if 'SHELL' in os.environ and os.path.exists(os.environ['SHELL']):
        return os.environ['SHELL']

    # Common shell paths to try
    shell_paths = [
        # Mac-specific paths
        '/usr/local/bin/bash',
        '/opt/homebrew/bin/bash',
        # Standard Unix paths
        '/bin/bash',
        '/usr/bin/bash',
        '/bin/sh',
        '/usr/bin/sh'
    ]

    # Try each shell in order
    for shell in shell_paths:
        if os.path.exists(shell):
            return shell

    # If we get here, we're in real trouble
    raise ValueError("No valid shell found. Please ensure bash or sh is installed in one of these locations: " + ", ".join(shell_paths))

def handle_chat_mode(llm_connector: LLMConnector, initial_context: Optional[Dict[str, Any]] = None, no_markdown: bool = False, debug: bool = False, web_search: bool = False) -> None:
    """Handle the chat mode interaction loop"""
    # Get stream mode from config if not specified in command line
    config_stream_mode = llm_connector.config.getboolean('DEFAULT', 'stream_mode', fallback=True)
    effective_stream_mode = llm_connector.stream_mode if llm_connector.stream_mode is not None else config_stream_mode

    chat_manager = ChatManager(stream=effective_stream_mode, debug=debug)

    # Initialize chat with context but don't process it yet
    if initial_context:
        if debug:
            print("\n[#555555]Initializing chat with context...[/#555555]", file=sys.stderr)
        chat_manager.start_session(initial_context)
        # If we have context, add it as the first message but don't process it
        if 'context' in initial_context and initial_context['context']:
            chat_manager.add_message("system", initial_context['context'])
    else:
        chat_manager.start_session(None)

    # Print welcome message in a box
    console.print("\n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    console.print("┃                                FlowAI Chat Mode                             ┃")
    console.print("┃                                                                             ┃")
    console.print("┃ Type your message and press Enter. Type '/help' for available commands.     ┃")
    console.print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n")

    while True:
        try:
            # Display prompt with status info using Rich markup
            console.print("")  # Add newline before prompt
            status_display = chat_manager.get_status_display()
            console.print(status_display, end="")
            # Set input color to light gray
            sys.stdout.write("\033[38;5;249m")  # ANSI color code for light gray
            user_message = input()
            sys.stdout.write("\033[0m")  # Reset color

            if debug:
                print(f"\n[#555555]User input: '{user_message}'[/#555555]", file=sys.stderr)

            # Handle chat commands
            if not chat_manager.handle_command(user_message):
                break

            if user_message.startswith('/'):
                continue

            # Add user message to history
            chat_manager.add_message("user", user_message)

            # Get chat history for context
            messages = chat_manager.get_formatted_history()

            if debug:
                print("[#555555]Starting LLM processing with full context...[/#555555]", file=sys.stderr)
                print(f"[#555555]Number of messages in history: {len(messages)}[/#555555]", file=sys.stderr)

            # Start timing and show loading indicator
            start_time = time.time()
            console.print("\n", end="")

            response = ""
            loading_live = None
            try:
                if not chat_manager.stream:
                    loading_live = Live(generate_status_table(0), refresh_per_second=10, transient=True)
                    loading_live.start()

                if debug:
                    print("[#555555]Sending request to LLM...[/#555555]", file=sys.stderr)

                for chunk in llm_connector.chat_completion(messages=messages, stream=chat_manager.stream):
                    response += chunk
                    if chat_manager.stream:
                        sys.stdout.write(chunk)
                        sys.stdout.flush()
                    elif loading_live:
                        elapsed_time = time.time() - start_time
                        loading_live.update(generate_status_table(elapsed_time))

                if debug:
                    elapsed_time = time.time() - start_time
                    print(f"[#555555]LLM processing completed in {elapsed_time:.3f}s[/#555555]", file=sys.stderr)
            finally:
                if loading_live:
                    loading_live.stop()

            if chat_manager.stream:
                sys.stdout.write("\n")
                sys.stdout.flush()

            # Add assistant response to history
            chat_manager.add_message("assistant", response)

            # Update token counts in chat manager (set instead of add)
            chat_manager.total_input_tokens = llm_connector.input_tokens
            chat_manager.total_output_tokens = llm_connector.output_tokens

            if debug:
                print(f"[#555555]Token usage - Input: {llm_connector.input_tokens}, Output: {llm_connector.output_tokens}[/#555555]", file=sys.stderr)

            # Display response if not streaming
            if not chat_manager.stream:
                if no_markdown:
                    console.print(response)
                else:
                    console.print(Markdown(response))

        except KeyboardInterrupt:
            console.print("\n[yellow]Chat interrupted. Type '/quit' to exit or continue chatting.[/yellow]")
            continue
        except Exception as e:
            console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
            continue

def display_available_models(config):
    """Display all available models from all providers"""
    print("Available models:")
    models = get_available_models(config)
    for provider, provider_models in models.items():
        print(f"\n{provider.capitalize()}:")
        if provider_models and provider_models[0] not in ["No API key set", "Error fetching models"]:
            for model in provider_models:
                print(f"  {model}")

    print("\nProviders with missing API keys or errors:")
    for provider, url in provider_urls.items():
        if provider not in models or models[provider][0] in [f"{provider}/No API key set", "Error fetching models"]:
            print(f"{provider.capitalize()}: {url}")

def display_status(config):
    """Display current FlowAI status"""
    current_model = config.get('DEFAULT', 'default_model', fallback='Not set')
    current_stream_mode = config.getboolean('DEFAULT', 'stream_mode', fallback=True)
    print(f"Current FlowAI Status\n\nModel: {current_model}\nStream mode: {'On' if current_stream_mode else 'Off'}")

@app.command(help="""FlowAI - AI-powered development assistant

A powerful CLI tool that helps streamline your development workflow using AI.

After setting up your API keys, you'll have access to an advanced help system:

    flowai --command help "your question here"

For example, try these questions:

    flowai --command help "how do I use FlowAI for code reviews?"

    flowai --command help "what's the best way to generate commit messages?"

    flowai --command help "explain the different context options"

The AI will provide detailed, contextual help based on your specific questions!""")
def main(
    model: Optional[str] = typer.Option(None, help="Specify the LLM model to use"),
    list_models: bool = typer.Option(False, "--list-models", help="List available models for all providers"),
    init: bool = typer.Option(False, "--init", help="Initialize FlowAI configuration"),
    status: bool = typer.Option(False, "--status", help="Show current model and settings"),
    stream: Optional[bool] = typer.Option(None, "--stream/--no-stream", "-S/-s", help="Stream mode: -S to enable, -s to disable"),
    context_file: Optional[str] = typer.Option(None, "--context-file", "-c", help="Path to a context file for global context"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug mode to display prompts"),
    version: bool = typer.Option(False, "--version", help="Show the version of FlowAI"),
    prompt_file: Optional[str] = typer.Option(None, "--prompt-file", "-p", help="Path to a file containing a detailed prompt"),
    select_prompt_file: bool = typer.Option(False, "--select-prompt-file", help="Select a prompt file from the flowai-prompts directory"),
    context_shell_command: Optional[str] = typer.Option(None, "--context-shell-command", help="Shell command to generate context"),
    context_from_clipboard: bool = typer.Option(False, "--context-from-clipboard", help="Set context from the system clipboard"),
    no_markdown: bool = typer.Option(False, "--no-markdown", help="Return the response without Markdown formatting"),
    command: Optional[str] = typer.Option(None, "--command", help="Command to run (use '--command list' to see available commands)"),
    chat: bool = typer.Option(False, "--chat", help="Start or continue a chat session after command execution"),
    web_search: bool = typer.Option(False, "--web-search", help="Enable web search capability (only supported by some models)"),
    prompt: Optional[str] = typer.Argument(None, help="The prompt to send to the LLM (optional if --prompt-file or --select-prompt-file is used)")
):
    """Main entry point for the FlowAI CLI"""
    try:
        # Handle broken pipe errors gracefully
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)

        # Initialize variables
        context = ""
        file_prompt = ""
        system_prompt = ""
        full_prompt = ""
        initial_context = None

        # Initialize config
        config_manager = ConfigManager()
        config = config_manager.load_config()

        # Get stream mode from config if not specified in command line
        default_stream = config.getboolean('DEFAULT', 'stream_mode', fallback=True)
        stream_mode = stream if stream is not None else default_stream

        # Check for first-time run
        config_dir = Path.home() / ".config" / "flowai"
        version_file = config_dir / "VERSION"
        if not version_file.exists():
            first_run_onboarding(config_manager)
            if not config_manager.config_exists():
                console.print("\n[yellow]Please run 'flowai --init' after setting up your API keys to start using FlowAI.[/yellow]")
                return

        # Handle early returns for simple commands
        if version:
            print(f"FlowAI version {__version__}")
            return

        if init:
            init_config()
            return

        if list_models:
            display_available_models(config)
            return

        if status:
            display_status(config)
            return

        # Check for stdin content
        if not sys.stdin.isatty():
            if debug:
                print("\n[#555555]Reading content from stdin...[/#555555]", file=sys.stderr)
            context = sys.stdin.read().strip()
            # If we have context but no other arguments, show error unless chat mode is explicitly requested
            if not any([prompt, prompt_file, select_prompt_file, command, list_models, init, status, version]):
                if not chat:
                    console.print(Panel.fit(
                        "[bold red]Error: Context provided without prompt or chat mode![/bold red]\n\n"
                        "When providing context (via pipe, file, or command), you must either:\n"
                        "1. Specify a prompt/command to process the context\n"
                        "2. Use --chat to discuss the context interactively\n\n"
                        "Examples:\n"
                        "  git diff | flowai --chat\n"
                        "  git diff | flowai \"summarize these changes\"\n"
                        "  git diff | flowai --command review",
                        title="Invalid Usage",
                        border_style="red"
                    ))
                    raise typer.Exit(code=1)
                chat = True
            # Reopen stdin for interactive use if needed
            if chat:
                try:
                    sys.stdin.close()
                    sys.stdin = open('/dev/tty')
                except Exception as e:
                    print(f"\nWarning: Could not reopen terminal for interactive use. Chat mode may not be available.", file=sys.stderr)

        # Handle direct chat mode
        if chat and not any([prompt, prompt_file, select_prompt_file, command, list_models, init, status, version]):
            if not config_manager.config_exists():
                raise ValueError("No configuration file found. Please run 'flowai --init' to set up FlowAI.")

            model = model or config.get('DEFAULT', 'default_model')
            if not model:
                raise ValueError("No valid model set. Please run 'flowai --init' or use --model to set a model.")

            # Convert model format if needed (from old ':' format to new '/' format)
            if ':' in model and '/' not in model:
                provider, model_name = model.split(':', 1)
                model = f"{provider}/{model_name}"

            llm_connector = LLMConnector(
                config=config,
                model=model,
                system_prompt=config_manager.get_system_prompt(),
                stream_mode=stream_mode,
                web_search=web_search
            )

            # Check if web search is requested but not supported
            if web_search and not llm_connector.supports_web_search():
                console.print("[yellow]Warning: Web search is only supported by Google models. Your request will proceed without web search.[/yellow]")

            # Create initial context with stdin content or context file if available
            initial_context = {
                'input_tokens': 0,
                'output_tokens': 0
            }

            if context:
                initial_context['context'] = context
                initial_context['last_command'] = "Chat with context from stdin"

            if context_file:
                try:
                    with open(context_file, 'r') as f:
                        context = f.read().strip()
                    initial_context['context'] = context
                    initial_context['last_command'] = f'Reading context from file: {context_file}'
                except FileNotFoundError:
                    console.print(f"[bold red]Error: Context file '{context_file}' not found.[/bold red]")
                    raise typer.Exit(code=1)
                except IOError:
                    console.print(f"[bold red]Error: Unable to read context file '{context_file}'.[/bold red]")
                    raise typer.Exit(code=1)

            handle_chat_mode(llm_connector, initial_context, no_markdown, debug, web_search)
            return

        # Show help if no input is provided and not in chat mode
        if not any([prompt, prompt_file, select_prompt_file, command, list_models, init, status, version, chat]):
            console.print("[blue]No command detected. type 'flowai --help' for more information...[/blue]\n")
            raise typer.Exit()

        # Check for version updates (only if not first run)
        if check_version():
            update_files()  # Update files, but don't return - continue with the command
            console.print("[green]Update complete![/green]\n")

        if version:
            print(f"FlowAI version: {__version__}")
            return

        if not config_manager.config_exists():
            raise ValueError("No configuration file found. Please run 'flowai --init' to set up FlowAI.")

        config = config_manager.load_config()
        system_prompt = config_manager.get_system_prompt()

        if status:
            current_model = config.get('DEFAULT', 'default_model', fallback='Not set')
            current_stream_mode = config.getboolean('DEFAULT', 'stream_mode', fallback=True)
            print(f"Current FlowAI Status\n\nModel: {current_model}\nStream mode: {'On' if current_stream_mode else 'Off'}")
            return

        if list_models:
            print("Available models:")
            models = get_available_models(config)
            for provider, provider_models in models.items():
                print(f"\n{provider.capitalize()}:")
                if provider_models and provider_models[0] not in ["No API key set", "Error fetching models"]:
                    for model in provider_models:
                        print(f"  {model}")

            print("\nProviders with missing API keys or errors:")
            for provider, url in provider_urls.items():
                if provider not in models or models[provider][0] in [f"{provider}/No API key set", "Error fetching models"]:
                    print(f"{provider.capitalize()}: {url}")
            return

        # Handle command listing and execution
        if command == "list":
            display_available_commands()
            return
        elif command:
            commands = parse_prompt_index()
            if command not in commands:
                console.print(f"\n[bold red]Unknown command: {command}[/bold red]\n")
                display_available_commands()
                raise typer.Exit(code=1)

            cmd_info = commands[command]

            # Set default help prompt if using help command without a prompt
            if command == "help" and not prompt:
                prompt = """Please provide a concise overview of FlowAI. Include:
1. What the program does and its main features
2. Available command-line switches and their usage
3. Common use cases and example commandsp"""

            # Handle any user prompts in the context command
            context_shell_command = handle_user_prompts(cmd_info['context_command'])
            prompt_file = cmd_info['prompt_file']

            # Override any existing prompt file or context command
            if prompt_file:
                prompt_file = prompt_file
            if context_shell_command:
                context_shell_command = context_shell_command

            # Override no_markdown based on command format if specified
            if cmd_info['format']:
                no_markdown = cmd_info['format'] == 'raw'

            # If no prompt provided but command has user_input defined, prompt the user
            if not prompt and cmd_info['user_input']:
                user_response = questionary.text(f"{cmd_info['user_input']}: ").ask()
                if user_response:  # Only use the response if user provided one
                    prompt = user_response

        # Check for prompt or prompt file first
        if not (prompt or prompt_file or select_prompt_file or command):
            raise ValueError("No prompt provided. Please provide a prompt, use --prompt-file, --select-prompt-file, or --command.")

        # Only validate configuration if we're not listing models or showing version/status
        if not (list_models or version or status):
            is_valid, error_message = config_manager.validate_config()
            if not is_valid:
                raise ValueError(f"Configuration error: {error_message}\nPlease run 'flowai --init' to reconfigure FlowAI.")

        model = model or config.get('DEFAULT', 'default_model')
        if not model:
            raise ValueError("No valid model set. Please run 'flowai --init' or use --model to set a model.")

        # Convert model format if needed (from old ':' format to new '/' format)
        if ':' in model and '/' not in model:
            provider, model_name = model.split(':', 1)
            model = f"{provider}/{model_name}"
        elif '/' not in model:
            raise ValueError("Invalid model format. Model should be in format 'provider/model_name'.")

        provider, model_name = model.split('/', 1)
        llm_connector = LLMConnector(
            config=config,
            model=model,
            system_prompt=system_prompt,
            stream_mode=stream_mode,
            web_search=web_search
        )

        # Check if web search is requested but not supported
        if web_search and not llm_connector.supports_web_search():
            console.print("[yellow]Warning: Web search is only supported by Google models. Your request will proceed without web search.[/yellow]")

        # Handle prompt file and command-line prompt
        file_prompt = ""
        if prompt_file:
            try:
                with open(prompt_file, 'r') as f:
                    file_prompt = f.read().strip()
                if debug:
                    print("\n[#555555]Template Prompt:[/#555555]", file=sys.stderr)
                    print(f"[#555555]{file_prompt}[/#555555]", file=sys.stderr)
            except FileNotFoundError:
                console.print(f"[bold red]Error: Prompt file '{prompt_file}' not found.[/bold red]")
                raise typer.Exit(code=1)
            except IOError:
                console.print(f"[bold red]Error: Unable to read prompt file '{prompt_file}'.[/bold red]")
                raise typer.Exit(code=1)
        elif select_prompt_file:
            if os.isatty(sys.stdin.fileno()):
                prompts_dir = Path.home() / "flowai-prompts"
                prompt_files = list(prompts_dir.glob("*.txt"))
                if not prompt_files:
                    console.print(f"[bold red]No prompt files found in {prompts_dir}.[/bold red]")
                    raise typer.Exit(code=1)
                prompt_file_choices = [Choice(str(file.name), value=str(file)) for file in prompt_files]
                selected_prompt_file = questionary.select(
                    "Select a prompt file:",
                    choices=prompt_file_choices
                ).ask()
                if not selected_prompt_file:
                    console.print("[bold red]No prompt file selected. Exiting.[/bold red]")
                    raise typer.Exit(code=1)
                with open(selected_prompt_file, 'r') as f:
                    file_prompt = f.read().strip()
                if debug:
                    print("\n[#555555]Selected Template Prompt:[/#555555]", file=sys.stderr)
                    print(f"[#555555]{file_prompt}[/#555555]", file=sys.stderr)
            else:
                console.print("[bold red]Error: --select-prompt-file requires an interactive terminal.[/bold red]")
                raise typer.Exit(code=1)

        # Show user prompt in debug mode
        if debug and prompt:
            print("\n[#555555]User Prompt:[/#555555]", file=sys.stderr)
            print(f"[#555555]{prompt}[/#555555]", file=sys.stderr)

        # Combine file prompt and command-line prompt
        full_prompt = file_prompt
        if prompt:
            # If there's a file prompt, add the user's prompt at the beginning
            # This ensures user instructions are prominent for the LLM
            if file_prompt:
                full_prompt = f"User Instructions: {prompt}\n\n{file_prompt}"
            else:
                full_prompt = prompt

        if debug:
            print("\n[#555555]System Prompt:[/#555555]", file=sys.stderr)
            print(f"[#555555]{system_prompt}[/#555555]", file=sys.stderr)

        # Check if context is required
        context_required = "{{CONTEXT}}" in full_prompt or any(keyword in full_prompt.lower() for keyword in [
            "git diff",
            "code changes",
            "analyze the changes",
            "review the code",
            "context will be provided",
            "__START_CONTEXT__"
        ])

        # Handle context_file and stdin
        if context_file:
            try:
                with open(context_file, 'r') as f:
                    context = f.read().strip()
                if debug:
                    print("\n[#555555]Context from file:[/#555555]", file=sys.stderr)
                    print(f"[#555555]{context}[/#555555]", file=sys.stderr)

                # Create initial context for chat mode
                if chat:
                    initial_context = {
                        'context': context,
                        'last_command': f'Reading context from file: {context_file}',
                        'input_tokens': 0,
                        'output_tokens': 0
                    }
            except FileNotFoundError:
                console.print(f"[bold red]Error: Context file '{context_file}' not found.[/bold red]")
                raise typer.Exit(code=1)
            except IOError:
                console.print(f"[bold red]Error: Unable to read context file '{context_file}'.[/bold red]")
                raise typer.Exit(code=1)

            # Check if stdin is also present
            if not sys.stdin.isatty():
                console.print("[bold red]Error: Cannot use both --context-file and stdin for context. Please choose one method.[/bold red]")
                raise typer.Exit(code=1)

        # Run the shell command and capture its output
        if context_shell_command:
            try:
                if os.name == 'nt':  # Windows
                    context = subprocess.check_output(f'cmd.exe /c "{context_shell_command}"', shell=True, text=True).strip()
                else:  # Unix-based systems
                    shell = get_shell()
                    context = subprocess.check_output(f"{shell} -c '{context_shell_command}'", shell=True, text=True).strip()
                if debug:
                    print("\n[#555555]Context from command:[/#555555]", file=sys.stderr)
                    print(f"[#555555]{context}[/#555555]", file=sys.stderr)
            except subprocess.CalledProcessError as e:
                console.print(f"[bold red]Error: Failed to run shell command '{context_shell_command}'.[/bold red]")
                console.print(f"[bold red]{e}[/bold red]")
                raise typer.Exit(code=1)
            except ValueError as e:
                console.print(f"[bold red]Error: {str(e)}[/bold red]")
                raise typer.Exit(code=1)

        # Set context from clipboard if --context-from-clipboard is provided
        if context_from_clipboard:
            context = pyperclip.paste()
            if debug:
                print("\n[#555555]Context from clipboard:[/#555555]", file=sys.stderr)
                print(f"[#555555]{context}[/#555555]", file=sys.stderr)

        # Check if context is required but missing
        if context_required and not context:
            console.print(Panel.fit(
                "[bold red]Error: This prompt requires context, but no context was provided![/bold red]\n\n"
                "You can provide context in several ways:\n\n"
                "[bold blue]1. Pipe content directly:[/bold blue]\n"
                "   git diff -w | flowai --prompt-file ~/flowai-prompts/prompt-commit-message.txt\n\n"
                "[bold blue]2. Use a context file:[/bold blue]\n"
                "   flowai --context-file changes.diff --prompt-file ~/flowai-prompts/prompt-commit-message.txt\n\n"
                "[bold blue]3. Use a shell command:[/bold blue]\n"
                "   flowai --context-shell-command \"git diff -w\" --prompt-file ~/flowai-prompts/prompt-commit-message.txt\n\n"
                "[bold blue]4. Use clipboard content:[/bold blue]\n"
                "   flowai --context-from-clipboard --prompt-file ~/flowai-prompts/prompt-commit-message.txt\n",
                title="Context Required",
                border_style="red"
            ))
            raise typer.Exit(code=1)

        # Add context to prompt
        if context:
            if debug:
                print("\n[#555555]Adding context to prompt...[/#555555]", file=sys.stderr)
            if "{{CONTEXT}}" in full_prompt:
                full_prompt = full_prompt.replace("{{CONTEXT}}", context)
            else:
                # If no {{CONTEXT}} tag is found, append the context
                full_prompt = f"{full_prompt}\n\n__START_CONTEXT__\n{context}\n__END_CONTEXT__"

            if debug:
                print("\n[#555555]Context:[/#555555]", file=sys.stderr)
                print(f"[#555555]{context}[/#555555]", file=sys.stderr)

        if debug:
            print("\n[#555555]Final Prompt to LLM:[/#555555]", file=sys.stderr)
            print(f"[#555555]{full_prompt}[/#555555]", file=sys.stderr)

        start_time = time.time()
        full_response = ""

        if stream:
            for chunk in llm_connector.send_prompt(prompt=full_prompt, debug=debug):
                sys.stdout.write(chunk)
                sys.stdout.flush()
            sys.stdout.write("\n")
            sys.stdout.flush()
        else:
            with Live(generate_status_table(0), refresh_per_second=10, transient=not debug) as live:
                for chunk in llm_connector.send_prompt(prompt=full_prompt, debug=debug):
                    full_response += chunk
                    elapsed_time = time.time() - start_time
                    live.update(generate_status_table(elapsed_time))

        elapsed_time = time.time() - start_time
        if debug:
            print(f"[bold blue]Total response time:[/bold blue] {elapsed_time:.3f}s", file=sys.stderr)
            print("[bold green]Response:[/bold green]\n", file=sys.stderr)
        if no_markdown:
            sys.stdout.write(full_response)
            sys.stdout.flush()
        else:
            # Process the response to ensure proper markdown formatting
            lines = full_response.splitlines()
            formatted_lines = []
            in_list = False

            for line in lines:
                line = line.rstrip()
                # Handle bullet points
                if line.strip().startswith('•'):
                    if not in_list:
                        formatted_lines.append('')  # Add space before list starts
                        in_list = True
                    formatted_lines.append(line.replace('•', '*'))
                else:
                    # If we're leaving a list, add extra space
                    if in_list and line.strip():
                        formatted_lines.append('')
                        in_list = False
                    # Add paragraphs with proper spacing
                    if line.strip():
                        formatted_lines.append(line)
                    elif formatted_lines and formatted_lines[-1] != '':
                        formatted_lines.append('')

            # Ensure proper spacing at the end
            if formatted_lines and formatted_lines[-1] != '':
                formatted_lines.append('')

            formatted_response = '\n'.join(formatted_lines)
            md = Markdown(formatted_response, justify="left")
            console.print(md)

        # Print model and token usage to stderr only if not entering chat mode
        if not chat:
            if debug:
                print(f"[#555555]Token usage - Input: {llm_connector.input_tokens}, Output: {llm_connector.output_tokens}[/#555555]", file=sys.stderr)
            print(f"\n\n[#555555]Model used: {llm_connector.model} | Input tokens: {llm_connector.input_tokens} | Output tokens: {llm_connector.output_tokens} | Elapsed time: {elapsed_time:.3f}s[/#555555]", file=sys.stderr)

        # Handle chat mode
        if chat:
            if debug:
                print("\n[#555555]Starting chat mode...[/#555555]", file=sys.stderr)

            # Create initial context if we don't have one yet
            if not initial_context:
                initial_context = {
                    'input_tokens': llm_connector.input_tokens,
                    'output_tokens': llm_connector.output_tokens
                }
                if context:
                    initial_context['context'] = context
                if prompt:
                    initial_context['prompt'] = prompt
                if full_prompt:
                    initial_context['full_prompt'] = full_prompt
                if 'response' in locals():
                    initial_context['last_response'] = response

            if debug and initial_context:
                print("[#555555]With initial context:[/#555555]", file=sys.stderr)
                print(f"[#555555]{initial_context}[/#555555]", file=sys.stderr)

            handle_chat_mode(llm_connector, initial_context, no_markdown, debug, web_search)
            return

    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
        if debug:
            traceback.print_exc()

if __name__ == "__main__":
    app()
