import os
import re
from rich.console import Console
from rich.syntax import Syntax
from .core.openai_utils import get_openai_response

console = Console()
SUPPORTED_SCRIPT_TYPES = ["bash", "python", "powershell"]

def clean_generated_code(code: str, language: str) -> str:
    """Removes potential markdown code fences and leading/trailing whitespace."""
    if not code: return ""
    code = code.strip()
    pattern = re.compile(r"^\s*```(?:\w+\s*?\n)?(.*?)\n?```\s*$", re.DOTALL | re.IGNORECASE)
    match = pattern.match(code)
    return match.group(1).strip() if match else code

# --- UPDATED SIGNATURE: Added dry_run ---
def generate_script(task_description: str, output_type: str = "bash", dry_run: bool = False):
    """
    Generates a script based on a natural language task description.

    Args:
        task_description: The description of the task for the script.
        output_type: The desired script type (e.g., "bash", "python"). Defaults to "bash".
        dry_run: If True, indicates that the script should only be displayed (currently always true).
    """
    output_type_lower = output_type.lower()
    if output_type_lower not in SUPPORTED_SCRIPT_TYPES:
        console.print(f"[bold red]Error: Unsupported script type '{output_type}'.[/bold red]")
        console.print(f"Supported types are: {', '.join(SUPPORTED_SCRIPT_TYPES)}")
        return

    console.print(f"Generating [bold yellow]{output_type_lower}[/bold yellow] script for task: '{task_description}'...")
    # --- Add message if dry_run is active ---
    if dry_run:
        console.print("[cyan]--dry-run active: Script will only be displayed.[/cyan]")

    # Construct the prompt
    prompt = f"""
    You are an expert script generator. Your task is to generate a functional and safe script based on the user's request.

    User Request: "{task_description}"

    Desired Script Type: {output_type_lower}

    Instructions:
    1.  Generate a complete, runnable script that performs the requested task.
    2.  Prioritize clarity and readability.
    3.  Add comments to explain key parts of the script, especially complex logic.
    4.  If the task involves potentially destructive actions (e.g., deleting files, modifying system settings), include safety checks (e.g., user confirmation prompts, dry-run options if applicable) or at least warn the user in comments.
    5.  Ensure the script uses standard libraries and commands commonly available on most systems for the specified script type.
    6.  IMPORTANT: Output ONLY the raw script code itself. Do not include *any* surrounding text, explanations, or markdown formatting like ```script_type ... ```. Just the code.

    Begin script code:
    """

    generated_code = get_openai_response(prompt, model="gpt-4o")
    processed_code = clean_generated_code(generated_code, output_type_lower) if generated_code else ""

    if processed_code and processed_code != "Model returned an empty response.":
        console.print("\n✨ [bold green]Generated Script:[/bold green]")
        lexer_map = {"bash": "bash", "python": "python", "powershell": "powershell"}
        lexer_name = lexer_map.get(output_type_lower, "text")
        syntax = Syntax(processed_code, lexer_name, theme="default", line_numbers=True)
        console.print(syntax)
        console.print("\n[bold yellow]⚠️ Warning:[/bold yellow] [yellow]Always review generated scripts carefully before executing them, especially if they involve file operations or system changes.[/yellow]")
    else:
        console.print(f"[bold red]Failed to generate the {output_type_lower} script.[/bold red]")
        if generated_code and not processed_code:
             console.print(f"[grey50]Model original (unprocessed) response: {generated_code}[/grey50]")

    # --- Placeholder for future execution logic ---
    # if not dry_run:
    #     # Execute the script here (use with extreme caution!)
    #     # Consider saving to file and running, or using subprocess
    #     console.print("\n[grey50]Execution logic not implemented.[/grey50]")
    # --- END Placeholder ---