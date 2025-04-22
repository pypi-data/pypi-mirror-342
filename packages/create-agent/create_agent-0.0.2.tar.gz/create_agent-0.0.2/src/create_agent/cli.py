#!/usr/bin/env python3
import os
import shutil
import sys
from pathlib import Path

import click
from jinja2 import Environment, FileSystemLoader

from create_agent.utils import copy_templates


@click.command()
@click.argument("project_name", required=False)
@click.option(
    "--template",
    default="default",
    help="Template to use for the project",
)
@click.option(
    "--output-dir",
    default=".",
    help="Directory where the project will be created",
)
def main(project_name: str, template: str, output_dir: str):
    """Create a new agent project from a template.
    
    PROJECT_NAME is the name of your agent project (e.g., my-agent)
    """
    # If project name is not provided, prompt the user
    if not project_name:
        project_name = click.prompt("What would you like to name your agent project?")
        
        # Validate project name
        if not project_name or not project_name.strip():
            click.echo("Error: Project name cannot be empty.")
            sys.exit(1)
        
        project_name = project_name.strip()
    
    click.echo(f"Creating new agent project: {project_name}")
    
    # Create the project directory
    project_dir = os.path.join(output_dir, project_name)
    if os.path.exists(project_dir):
        click.echo(f"Error: Directory '{project_dir}' already exists.")
        sys.exit(1)
    
    # Copy templates to project directory
    templates_dir = os.path.join(os.path.dirname(__file__), "templates")
    
    try:
        os.makedirs(project_dir)
        copy_templates(templates_dir, project_dir, project_name)
        
        click.echo(f"\n✅ Project created successfully at {project_dir}")
        click.echo("\nNext steps:")
        click.echo(f"  cd {project_name}")
        click.echo("  python -m venv venv")
        click.echo("  source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
        click.echo("  pip install -r requirements.txt")
        click.echo("  cp .env.example .env")
        click.echo("  # Edit .env with your configuration")
        click.echo("  uvicorn app.main:app --reload")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        # Cleanup if something went wrong
        if os.path.exists(project_dir):
            shutil.rmtree(project_dir)
        sys.exit(1)


if __name__ == "__main__":
    main() 