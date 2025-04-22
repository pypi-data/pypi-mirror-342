# -*- coding: utf-8 -*-
import click
from .agent import Agent
from pydantic import BaseModel
import subprocess
import pyperclip
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax # Import Syntax
from rich.theme import Theme
from pydantic_ai.tools import RunContext
import asyncio
from functools import wraps
from typing import Union, Optional
import platform # Needed for get_os_info tool
from .config import DEFAULT_MODEL_NAME

# Define the theme dictionary
cyberpunk_styles = {
    "info": "dim cyan",
    "warning": "magenta",
    "danger": "bold red",
    "request": "bold blue",
    "response": "bold green",
    "command": "bold yellow",
    "output": "white",
    "error": "red",
    "border.request": "blue",
    "border.interpreter": "magenta",
    "border.generator": "cyan",
    "border.executor": "green",
    "border.command": "yellow",
    "border.output": "green",
    "border.error": "red",
    "status": "bold cyan",
}

# Create a Theme instance from the dictionary
cyberpunk_theme = Theme(cyberpunk_styles)

# Pass the Theme object to the Console
console = Console(theme=cyberpunk_theme)

# --- Pydantic Models (unchanged) ---
class QueryInterpretation(BaseModel):
    """Structured interpretation of the user's request."""
    intent: str
    command_type: str
    parameters: dict[str, str] = {}
    constraints: list[str] = []

class CommandRequest(BaseModel):
    """A request for a command to be generated."""
    description: str
    interpretation: Optional[QueryInterpretation] = None

class CommandResponse(BaseModel):
    """A response containing a generated command."""
    command: str = ""
    args: list[str] = []
    expected_output: str = ""

class ExecutedCommand(BaseModel):
    """The result of executing a command."""
    command: str
    args: list[str]
    output: str
    success: bool
    error_message: Optional[str] = None

class InterpreterAgentResponse(BaseModel):
    """Response from the query interpreter agent."""
    text: str
    interpretation: Optional[QueryInterpretation] = None

class GeneratorAgentResponse(BaseModel):
    """Response from the command generator agent."""
    text: str
    command: Optional[CommandResponse] = None

class ExecutorAgentResponse(BaseModel):
    """Response from the command executor agent."""
    text: str
    executed: Optional[ExecutedCommand] = None

# --- Agent Definitions (mostly unchanged, added cyberpunk flair to prompts) ---

# Query Interpreter Agent
interpreter_agent = Agent(
    model_name=DEFAULT_MODEL_NAME,
    deps_type=None,
    system_prompt=(
        'You are a ShellAssist Query Interface. Analyze user requests for terminal operations. '
        'Translate natural language into a structured data packet: {intent, command_type, parameters, constraints}. '
        'Focus on the core directive. Keep text response minimal, like a system log entry. '
        'Example: User: "find all .log files modified today in /var/log" -> '
        'Intent: "find files", Command Type: "file search", Parameters: {"pattern": "*.log", "path": "/var/log", "time": "today"}, Constraints: []'
    ),
    result_type=InterpreterAgentResponse,
    result_retries=5,
    instrument=True,
    temp=0.2,
)

# Command Generator Agent
generator_agent = Agent(
    model_name=DEFAULT_MODEL_NAME,
    deps_type=None,
    system_prompt=(
        'You are a Command Compiler Unit for a ShellAssist. '
        'Generate precise terminal commands from structured requests. '
        'Input: Natural language request + structured interpretation. '
        'Output: MUST include a structured JSON: {"command": "cmd_name", "args": ["arg1", "arg2"]}. '
        'Provide concise explanation and expected output pattern if possible. '
        'Prioritize accuracy and system compatibility (use provided OS info). '
        'Example: Request for "list files detailed" -> {"command": "ls", "args": ["-la"]}.'
    ),
    result_type=GeneratorAgentResponse,
    result_retries=5,
    instrument=True,
    temp=0.1,
)

# Command Executor Agent
executor_agent = Agent(
    model_name=DEFAULT_MODEL_NAME,
    deps_type=None,
    system_prompt=(
        'You are the ShellAssist Command Execution Core. '
        'Execute provided commands and report results. '
        'Input: Structured command {"command": "cmd", "args": [...]}. '
        'Output: Explanation of execution outcome + structured result: '
        '{"command", "args", "output", "success", "error_message"}. '
        'Analyze output, report success/failure, explain errors, suggest fixes. '
        'Highlight security implications or potential risks before execution if obvious, though execution is mandatory. '
        'Format output clearly, potentially using markdown code blocks for raw output.'
    ),
    result_type=ExecutorAgentResponse,
    result_retries=3,
    instrument=True,
    temp=0.1,
)


# --- Tools (unchanged functionality, added ctx type hint) ---
@interpreter_agent.tool
def get_os_info(ctx: RunContext) -> dict:
    """Get information about the operating system."""
    try:
        return {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "user": subprocess.check_output(["whoami"], text=True).strip() # Added user
        }
    except Exception as e:
        return {"system": "unknown", "error": str(e)}

@generator_agent.tool
def check_command_availability(ctx: RunContext, command: str) -> bool:
    """Check if a command is available in the system PATH."""
    try:
        # Use 'which' on Unix-like, 'where' on Windows
        checker_command = "where" if platform.system() == "Windows" else "which"
        result = subprocess.run(
            [checker_command, command],
            capture_output=True,
            text=True,
            check=False,
            shell=platform.system() == "Windows" # shell=True might be needed for 'where' on Windows
        )
        # Also check common built-ins that `which` might not find
        if result.returncode == 0:
            return True
        # Basic check for common shell built-ins (extend as needed)
        builtins = ["cd", "echo", "export", "pwd", "exit", "source", "alias", "unalias"]
        if command in builtins:
             return True # Assume common builtins are available
        return False
    except Exception:
        return False

@executor_agent.tool
def execute_command(ctx: RunContext, command: str, args: list[str]) -> ExecutedCommand:
    """Execute a terminal command and return the result."""
    full_command_list = [command] + args
    console.print(f"[dim cyan]>> Executing: {' '.join(full_command_list)}[/]")
    try:
        # Handle 'cd' separately as it needs to affect the parent process state (which we can't directly do)
        # For this CLI, we'll just report that 'cd' needs to be run manually.
        if command == "cd":
             return ExecutedCommand(
                command=command,
                args=args,
                output=f"Cannot execute 'cd' directly. Run '{command} {' '.join(args)}' manually in your shell.",
                success=False, # Indicate it wasn't truly executed in a persistent way
                error_message="Shell built-in 'cd' changes the current process's directory and cannot be executed this way."
            )

        result = subprocess.run(
            full_command_list,
            capture_output=True,
            text=True,
            check=True,
            # Use shell=True cautiously, maybe only for specific commands or Windows?
            # shell=platform.system() == "Windows",
            shell=False, # Generally safer
            cwd=None # Run in the current directory of the script
        )
        return ExecutedCommand(
            command=command,
            args=args,
            output=result.stdout.strip(),
            success=True
        )
    except subprocess.CalledProcessError as e:
        return ExecutedCommand(
            command=command,
            args=args,
            output=e.stdout.strip(), # Include stdout even on error
            success=False,
            error_message=e.stderr.strip()
        )
    except FileNotFoundError:
        return ExecutedCommand(
            command=command,
            args=args,
            output="",
            success=False,
            error_message=f"Command not found: '{command}'. Ensure it's installed and in your PATH."
        )
    except Exception as e: # Catch other potential errors
        return ExecutedCommand(
            command=command,
            args=args,
            output="",
            success=False,
            error_message=f"An unexpected error occurred: {str(e)}"
        )


# Helper function to handle async click commands
def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper

@click.group()
def cli():
    """ShellAssist Command Interface"""
    console.print(Panel("[bold magenta]::: ShellAssist v0.1 ::: Command Interface Initialized :::[/]", border_style="bold magenta", expand=False))
    pass

# --- Helper to display output/error cleanly ---
def display_result(executed_data: ExecutedCommand):
    """Displays command output or error using Panels and Syntax."""
    if executed_data.success:
        title = f":heavy_check_mark: Command Output ({executed_data.command})"
        border_style = "border.output"
        content_style = "output"
        content = executed_data.output if executed_data.output else "[dim i]Command executed successfully with no output.[/]"

        # Attempt syntax highlighting for common outputs, fallback to plain text
        lexer = "bash" # Default guess
        # Add more guesses based on command? e.g., if command is 'cat *.json', lexer='json'
        if executed_data.command in ['ls', 'tree', 'ps', 'netstat']:
             lexer = 'bash'
        elif executed_data.command in ['cat', 'grep', 'awk'] and any(a.endswith(('.json', '.yml', '.yaml', '.py', '.js', '.html', '.css')) for a in executed_data.args):
             # Very basic guess based on file extension in args
             ext = next((a.split('.')[-1] for a in executed_data.args if '.' in a), None)
             if ext in ['json', 'py', 'js', 'html', 'css', 'yaml', 'yml']:
                 lexer = ext

        console.print(Panel(
            Syntax(content, lexer, theme="dracula", line_numbers=False, word_wrap=True),
            title=title,
            border_style=border_style,
            title_align="left"
        ))

    else:
        title = f":x: Command Error ({executed_data.command})"
        border_style = "border.error"
        error_content = f"[error]{executed_data.error_message}[/]" if executed_data.error_message else "[error]Unknown execution error.[/]"
        if executed_data.output: # Show stdout even on error if it exists
             error_content += f"\n\n[dim]Standard Output:[/]\n{executed_data.output}"

        console.print(Panel(
            error_content,
            title=title,
            border_style=border_style,
            title_align="left"
        ))

# --- CLI Commands ---
@cli.command()
@click.argument('message', nargs=-1)
@coro
async def execute(message: tuple):
    """Generate and execute a command based on your description."""
    if not message:
        console.print("[warning]Please provide a description for the command.[/]")
        return
    message_text = " ".join(message)

    console.print(Panel(Text(message_text, style="request"), title=">: User Directive", border_style="border.request"))

    # --- Interpretation Step ---
    interpreter_response = None
    with console.status("[status]>> Accessing Neural Link: Interpreting Directive...[/]", spinner="dots"):
        try:
            interpreter_response = await interpreter_agent.run(
                f'Interpret this request for a terminal command: {message_text}',
            )
        except Exception as e:
            console.print(Panel(f"[danger]Interpreter Agent Failed: {e}[/]", title="! Agent Error !", border_style="danger"))
            return

    if not interpreter_response or not interpreter_response.data:
         console.print(Panel("[warning]Interpreter returned no data.[/]", title="! Interpretation Failed !", border_style="warning"))
         return

    console.print(Panel(interpreter_response.data.text, title=">> Interpretation Log", border_style="border.interpreter"))
    interpretation_json = interpreter_response.data.interpretation.model_dump_json(indent=2) if interpreter_response.data.interpretation else "{}"


    # --- Generation Step ---
    generator_response = None
    with console.status("[status]>> Compiling Command Sequence...[/]", spinner="dots"):
        try:
            generator_response = await generator_agent.run(
                f'''Generate a terminal command based on this request:
                Original request: {message_text}
                Interpretation: {interpretation_json}''',
            )
        except Exception as e:
            console.print(Panel(f"[danger]Generator Agent Failed: {e}[/]", title="! Agent Error !", border_style="danger"))
            return

    if not generator_response or not generator_response.data:
         console.print(Panel("[warning]Generator returned no data.[/]", title="! Generation Failed !", border_style="warning"))
         return

    console.print(Panel(generator_response.data.text, title=">> Command Compiler Log", border_style="border.generator"))


    # --- Execution Step ---
    if generator_response.data.command and generator_response.data.command.command:
        command_data = generator_response.data.command
        full_command = f"{command_data.command} {' '.join(command_data.args)}"

        # Display the command using Syntax
        console.print(Panel(
            Syntax(full_command, "bash", theme="dracula", line_numbers=False, word_wrap=True),
            title=">: Generated Command Sequence",
            border_style="border.command"
        ))

        # Confirm execution (optional - uncomment to add confirmation step)
        # if not click.confirm(Text("Execute this command?", style="warning"), default=True):
        #    console.print("[info]Execution aborted by user.[/]")
        #    return

        executor_response = None
        with console.status(f"[status]>> Executing Sequence: {command_data.command}...[/]", spinner="dots"):
             try:
                 # We directly call the tool function here now for execution result
                 # The executor agent is only used for *analyzing* the result.
                 executed_data = execute_command(None, command_data.command, command_data.args) # Pass None for RunContext if not needed by tool logic

                 # Now, optionally, run the executor agent to *explain* the results
                 # This adds cost and latency, decide if the explanation is worth it.
                 explanation_prompt = f'''The command `{' '.join([command_data.command] + command_data.args)}` was executed.
                 Result Status: {'Success' if executed_data.success else 'Failure'}
                 Standard Output:
                 ```
                 {executed_data.output}
                 ```
                 Standard Error:
                 ```
                 {executed_data.error_message or 'None'}
                 ```
                 Explain this outcome. If it failed, suggest reasons or fixes.'''

                 executor_response = await executor_agent.run(explanation_prompt)

             except Exception as e:
                 console.print(Panel(f"[danger]Executor Agent/Execution Failed: {e}[/]", title="! Agent/Execution Error !", border_style="danger"))
                 return # Stop if execution phase fails

        # Display the actual command result (output or error)
        if executed_data:
            display_result(executed_data)
        else:
             console.print("[warning]Execution did not return data.[/]")

        # Display Executor Agent's analysis (if run)
        if executor_response and executor_response.data:
             console.print(Panel(executor_response.data.text, title=">> Execution Core Analysis", border_style="border.executor"))
        elif not executor_response :
             console.print("[dim]Skipped execution analysis step.[/dim]")





    else:
        console.print(Panel("[danger]>> No valid command sequence generated. Cannot execute.[/]", title="! Execution Halted !", border_style="danger"))


@cli.command()
@click.argument('query', nargs=-1)
@coro
async def query(query: tuple):
    """Just generate a command without executing it."""
    if not query:
        console.print("[warning]Please provide a description for the command.[/]")
        return
    query_text = " ".join(query)
    console.print(Panel(Text(query_text, style="request"), title=">: User Query", border_style="border.request"))

    # --- Interpretation Step ---
    interpreter_response = None
    with console.status("[status]>> Accessing Neural Link: Interpreting Query...[/]", spinner="dots"):
        try:
            interpreter_response = await interpreter_agent.run(
                f'Interpret this request for a terminal command: {query_text}',
            )
        except Exception as e:
            console.print(Panel(f"[danger]Interpreter Agent Failed: {e}[/]", title="! Agent Error !", border_style="danger"))
            return

    if not interpreter_response or not interpreter_response.data:
         console.print(Panel("[warning]Interpreter returned no data.[/]", title="! Interpretation Failed !", border_style="warning"))
         return

    console.print(Panel(interpreter_response.data.text, title=">> Interpretation Log", border_style="border.interpreter"))
    interpretation_json = interpreter_response.data.interpretation.model_dump_json(indent=2) if interpreter_response.data.interpretation else "{}"


    # --- Generation Step ---
    generator_response = None
    with console.status("[status]>> Compiling Command Sequence...[/]", spinner="dots"):
        try:
            generator_response = await generator_agent.run(
                f'''Generate a terminal command based on this request:
                Original request: {query_text}
                Interpretation: {interpretation_json}''',
            )
        except Exception as e:
            console.print(Panel(f"[danger]Generator Agent Failed: {e}[/]", title="! Agent Error !", border_style="danger"))
            return

    if not generator_response or not generator_response.data:
         console.print(Panel("[warning]Generator returned no data.[/]", title="! Generation Failed !", border_style="warning"))
         return

    console.print(Panel(generator_response.data.text, title=">> Command Compiler Log", border_style="border.generator"))

    # --- Display Generated Command ---
    if generator_response.data.command and generator_response.data.command.command:
        command_data = generator_response.data.command
        full_command = f"{command_data.command} {' '.join(command_data.args)}"

        console.print(Panel(
            Syntax(full_command, "bash", theme="dracula", line_numbers=False, word_wrap=True),
            title=">: Suggested Command Sequence",
            border_style="border.command"
        ))

        # Always try to copy to clipboard for the query command
        try:
            pyperclip.copy(full_command)
            console.print("[info]>> Command sequence copied to clipboard.[/]")
        except Exception as e:
            console.print(f"[warning]Could not copy to clipboard: {e}[/]")

        # Display expected output if available
        if command_data.expected_output:
            console.print(Panel(
                Text(command_data.expected_output, style="output"), # Expected output is likely text, not code
                title=">> Expected Output Pattern",
                border_style="border.output" # Use output border style
            ))
    else:
        console.print(Panel("[warning]>> No command sequence generated.[/]", title="! Generation Result !", border_style="warning"))


if __name__ == "__main__":
    cli()