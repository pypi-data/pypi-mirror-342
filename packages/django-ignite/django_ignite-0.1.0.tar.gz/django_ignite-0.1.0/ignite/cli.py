from InquirerPy import prompt
from InquirerPy.utils import InquirerPyStyle
from rich import print
from typing import Dict

# Importing the setup_environment function from env_manager
from ignite.env_manager import setup_environment
from ignite.project_creator import install_django, start_django_project, modify_settings_py

# CLI styles
custom_style: InquirerPyStyle = {
    "questionmark": "ansiyellow",
    "answer": "ansigreen",
    "input": "ansiyellow",
    "pointer": "ansiyellow",
}

def get_user_input() -> Dict[str, str]:
    """Prompt the user for basic project configuration."""

    questions = [
        {
            "type": "input",
            "message": "project name:",
            "name": "project_name",
            "default": "my_project"
        },
        {
            "type": "list",
            "message": "django version:",
            "name": "django_version",
            "choices": ["4.2", "5.2"],
            "default": "4.2"
        },
        {
            "type": "list",
            "message": "environment:",
            "name": "env_type",
            "choices": ["uv", "venv"],
            "default": "uv"
        },
        {
            "type": "confirm",
            "message": "create project in root directory?",
            "name": "in_root",
            "default": False
        }
    ]

    return prompt(questions, style=custom_style)

def main() -> None:
    print("[cyan]Welcome to Django Ignite!\n")

    answers = get_user_input()

    print("[cyan]\nInitialized project with the following settings:")
    print(f"project     : {answers['project_name']}")
    print(f"version     : {answers['django_version']}")
    print(f"environment : {answers['env_type']}")

    # Call the setup_environment function to create the virtual environment
    setup_environment(answers["env_type"])
    install_django(answers["django_version"])
    
    # Create project (in root or subfolder)
    start_django_project(
        project_name=answers["project_name"],
        in_root=answers["in_root"]
    )

    # Modify settings.py in the right location
    project_root = "." if answers["in_root"] else answers["project_name"]
    modify_settings_py(project_root)


if __name__ == "__main__":
    main()
