import os
import shutil
from pathlib import Path
import click
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def copy_template_files(destination):
    """Copy template files to the destination directory."""
    template_dir = Path(__file__).parent.parent
    for item in template_dir.glob("*"):
        if item.name not in ["create_agentic_rag", "setup.py", "README.md"]:
            if item.is_file():
                shutil.copy2(item, destination / item.name)
            elif item.is_dir():
                shutil.copytree(item, destination / item.name)

def create_project(destination):
    """Create a new project from the template."""
    try:
        # Create destination directory if it doesn't exist
        destination = Path(destination)
        destination.mkdir(parents=True, exist_ok=True)
        
        # Copy template files
        copy_template_files(destination)
        
        console.print(f"[green]Successfully created project at {destination}[/green]")
        console.print("\nNext steps:")
        console.print("1. cd into your project directory")
        console.print("2. Create a virtual environment: python -m venv venv")
        console.print("3. Activate the virtual environment")
        console.print("4. Install dependencies: pip install -r requirements.txt")
        console.print("5. Copy .env.example to .env and configure your environment variables")
        
    except Exception as e:
        console.print(f"[red]Error creating project: {str(e)}[/red]")
        raise click.Abort()

@click.command()
@click.argument('project_name', required=False)
def main(project_name):
    """Create a new agentic RAG project."""
    if not project_name:
        project_name = Prompt.ask("Enter project name")
    
    create_project(project_name)

if __name__ == '__main__':
    main() 