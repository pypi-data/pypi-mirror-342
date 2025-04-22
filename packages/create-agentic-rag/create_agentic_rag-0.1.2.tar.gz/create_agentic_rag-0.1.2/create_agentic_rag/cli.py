import os
import shutil
from pathlib import Path
import click
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def copy_template_files(destination):
    """Copy template files to the destination directory."""
    # Get the template directory relative to this file
    template_dir = Path(__file__).parent / "template"
    
    if not template_dir.exists():
        raise click.ClickException(f"Template directory not found at {template_dir}")
    
    console.print(f"[blue]Copying template files from {template_dir}[/blue]")
    
    try:
        # Copy all files and directories from template
        for item in template_dir.iterdir():
            if item.is_file():
                shutil.copy2(item, destination / item.name)
                console.print(f"[green]Created file: {item.name}[/green]")
            elif item.is_dir():
                shutil.copytree(item, destination / item.name)
                console.print(f"[green]Created directory: {item.name}[/green]")
    except Exception as e:
        raise click.ClickException(f"Error copying template files: {str(e)}")

def create_project(destination):
    """Create a new project from the template."""
    try:
        # Create destination directory if it doesn't exist
        destination = Path(destination).resolve()
        
        if destination.exists() and any(destination.iterdir()):
            raise click.ClickException(f"Directory {destination} already exists and is not empty")
            
        destination.mkdir(parents=True, exist_ok=True)
        console.print(f"[blue]Creating new project in {destination}[/blue]")
        
        # Copy template files
        copy_template_files(destination)
        
        console.print("\n[green]✨ Project created successfully![/green]")
        console.print("\n[yellow]Next steps:[/yellow]")
        console.print(f"1. cd {destination}")
        console.print("2. python -m venv venv")
        console.print("3. source venv/bin/activate  # On Windows: .\\venv\\Scripts\\activate")
        console.print("4. pip install -r requirements.txt")
        console.print("5. cp .env.example .env")
        console.print("6. # Edit .env with your configuration")
        
    except click.ClickException as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise
    except Exception as e:
        console.print(f"[red]Unexpected error: {str(e)}[/red]")
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