from InquirerPy import prompt
import shutil
import os
import subprocess
import sys
from rich import print

POSSIBLE_ENV_DIRS = [".venv", "venv", ".env", "env"]

def setup_environment(env_type: str) -> None:
    """Set up virtual environment using uv or venv, with safe detection and optional cleanup."""

    print(f"\n[cyan]environment setup:[/cyan] [bold]{env_type}[/bold]")

    # Check for any existing environment
    existing_env = next((d for d in POSSIBLE_ENV_DIRS if os.path.exists(d)), None)

    if existing_env:
        print(f"[yellow]{existing_env} already exists.[/yellow]")

        question = [
            {
                "type": "list",
                "message": "Select an action for the environment: ",
                "name": "env_action",
                "choices": [
                    {"name": "Create New", "value": "recreate"},
                    {"name": "Use Old Env", "value": "use"},
                ],
                "default": "recreate"
            }
        ]

        answer = prompt(question)
        action = answer["env_action"]

        if action == "use":
            print(f"[green]using existing environment: {existing_env}[/green]")
            return
        elif action == "recreate":
            print(f"[yellow]removing existing environment: {existing_env}[/yellow]")
            shutil.rmtree(existing_env)

    # Create new environment
    if env_type == "uv":
        if shutil.which("uv") is None:
            print("[red]uv is not installed.[/red]")

            install_prompt = [
                {
                    "type": "confirm",
                    "message": "Would you like to install uv now?",
                    "name": "install_uv",
                    "default": True
                }
            ]

            answer = prompt(install_prompt)
            if answer["install_uv"]:
                if os.name == "nt":
                    print("[yellow]Installing uv on Windows...[/yellow]")
                    subprocess.run([
                        "powershell", "-Command",
                        "iwr https://astral.sh/uv/install.ps1 -useb | iex"
                    ], shell=True)
                else:
                    print("[yellow]Installing uv on Unix/macOS...[/yellow]")
                    subprocess.run([
                        "sh", "-c",
                        "curl -Ls https://astral.sh/uv/install.sh | sh"
                    ])
                
                if shutil.which("uv") is None:
                    print("[red]uv installation failed or not added to PATH.[/red]")
                    sys.exit(1)
            else:
                print("[red]uv is required to proceed. exiting.[/red]")
                sys.exit(1)

        subprocess.run(["uv", "venv", ".venv"], check=True)
