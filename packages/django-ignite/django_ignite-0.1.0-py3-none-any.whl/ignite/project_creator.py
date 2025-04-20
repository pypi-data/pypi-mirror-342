import subprocess
import os
import sys
from rich import print
import textwrap


def install_django(version: str) -> None:
    """Install the specified Django version inside the virtual environment."""

    print(f"\n[cyan]installing django {version}...[/cyan]")

    # Choose pip path based on OS
    pip_path = (
        os.path.join(".venv", "Scripts", "pip.exe") if os.name == "nt"
        else os.path.join(".venv", "bin", "pip")
    )

    try:
        subprocess.run([pip_path, "install", f"django=={version}"], check=True)
        print(f"[green]django {version} installed successfully[/green]")
    except subprocess.CalledProcessError:
        print(f"[red]failed to install django {version}[/red]")
        sys.exit(1)

def start_django_project(project_name: str, in_root: bool) -> None:
    """Start a Django project with internal 'core' package."""

    print(f"\n[cyan]creating django project: {project_name}[/cyan]")

    django_admin = (
        os.path.join(".venv", "Scripts", "django-admin.exe") if os.name == "nt"
        else os.path.join(".venv", "bin", "django-admin")
    )

    destination = "." if in_root else project_name

    if not in_root:
        os.makedirs(destination, exist_ok=True)

    cmd = [django_admin, "startproject", "core", destination]

    try:
        subprocess.run(cmd, check=True)
        print(f"[green]project created successfully[/green]")
    except subprocess.CalledProcessError:
        print(f"[red]failed to create project in {destination}[/red]")
        sys.exit(1)

def modify_settings_py(project_root: str) -> None:
    """Modify core/settings.py to include third-party app structure."""
    settings_path = os.path.join(project_root, "core", "settings.py")

    try:
        with open(settings_path, "r") as file:
            lines = file.readlines()

        updated_lines = []
        inside_installed_apps = False
        installed_apps_closed = False

        for line in lines:
            stripped = line.strip()
            updated_lines.append(line)

            # Detect the start of INSTALLED_APPS
            if stripped.startswith("INSTALLED_APPS = ["):
                inside_installed_apps = True

            # Detect the closing bracket
            if inside_installed_apps and stripped == "]":
                inside_installed_apps = False
                installed_apps_closed = True
                continue  # Skip appending another line, we’ll add blank line manually

            # Once INSTALLED_APPS is fully processed, insert your block
            if installed_apps_closed:
                block = textwrap.dedent("""\

                    # Third-party applications
                    THIRD_PARTY_APPS = [

                    ]

                    # Custom applications
                    MY_APPS = [

                    ]

                    # Update installed applications
                    INSTALLED_APPS += THIRD_PARTY_APPS
                    INSTALLED_APPS += MY_APPS

                """)
                updated_lines.append(block)
                installed_apps_closed = False  # prevent repeating
        with open(settings_path, "w") as file:
            file.writelines(updated_lines)

        print("[green]settings.py updated successfully[/green]")

    except FileNotFoundError:
        print(f"[red]could not find settings.py in {settings_path}[/red]")
        sys.exit(1)
