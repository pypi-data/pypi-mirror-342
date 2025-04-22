#!/usr/bin/env python3
import os
import shutil
import sys
import time
from pathlib import Path

import click
import colorama
from colorama import Fore, Style
from jinja2 import Environment, FileSystemLoader
from tqdm import tqdm

from create_agent.utils import copy_templates

# Initialize colorama for cross-platform colored terminal text
colorama.init()

# ASCII Art for welcome message "Create Agent CLI"
WELCOME_ART = f"""{Fore.CYAN}
================================================
 ______ ______ _______ _______ _______ _______ 
|      |   __ \    ___|   _   |_     _|    ___|
|   ---|      <    ___|       | |   | |    ___|  
|______|___|__|_______|___|___| |___| |_______| 
 _______ _______ _______ _______ _______ 
|   _   |     __|    ___|    |  |_     _|
|       |    |  |    ___|       | |   | 
|___|___|_______|_______|__|____| |___|  

================================================                                                                                                       
                                                             
{Style.RESET_ALL}"""


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
    # Display welcome message with ASCII art
    click.echo(WELCOME_ART)
    click.echo(f"{Fore.GREEN}Welcome to Create Agent CLI!{Style.RESET_ALL}")
    click.echo(f"{Fore.YELLOW}The easiest way to scaffold an LLM agent API project{Style.RESET_ALL}\n")
    
    # If project name is not provided, prompt the user
    if not project_name:
        project_name = click.prompt(f"{Fore.CYAN}What would you like to name your agent project?{Style.RESET_ALL}")
        
        # Validate project name
        if not project_name or not project_name.strip():
            click.echo(f"{Fore.RED}Error: Project name cannot be empty.{Style.RESET_ALL}")
            sys.exit(1)
        
        project_name = project_name.strip()
    
    click.echo(f"\n{Fore.GREEN}Creating new agent project: {Fore.CYAN}{project_name}{Style.RESET_ALL}")
    
    # Create the project directory
    project_dir = os.path.join(output_dir, project_name)
    if os.path.exists(project_dir):
        click.echo(f"{Fore.RED}Error: Directory '{project_dir}' already exists.{Style.RESET_ALL}")
        sys.exit(1)
    
    # Simulate initialization with progress bar
    click.echo(f"\n{Fore.YELLOW}Initializing project structure...{Style.RESET_ALL}")
    with tqdm(total=100, desc="Initializing", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
        for i in range(10, 101, 10):
            time.sleep(0.1)  # Simulate work
            pbar.update(10)
    
    # Copy templates to project directory
    templates_dir = os.path.join(os.path.dirname(__file__), "templates")
    
    try:
        os.makedirs(project_dir)
        
        # Simulate project generation with progress bar
        click.echo(f"\n{Fore.YELLOW}Generating project files...{Style.RESET_ALL}")
        
        # Perform the template copying with visual feedback
        copy_templates(templates_dir, project_dir, project_name, show_progress=True)
        
        click.echo(f"\n{Fore.GREEN}✅ Project created successfully at {Fore.CYAN}{project_dir}{Style.RESET_ALL}")
        click.echo(f"\n{Fore.YELLOW}Next steps:{Style.RESET_ALL}")
        click.echo(f"  {Fore.CYAN}cd {project_name}{Style.RESET_ALL}")
        click.echo(f"  {Fore.CYAN}python -m venv venv{Style.RESET_ALL}")
        click.echo(f"  {Fore.CYAN}source venv/bin/activate  # On Windows: venv\\Scripts\\activate{Style.RESET_ALL}")
        click.echo(f"  {Fore.CYAN}pip install -r requirements.txt{Style.RESET_ALL}")
        click.echo(f"  {Fore.CYAN}cp .env.example .env{Style.RESET_ALL}")
        click.echo(f"  {Fore.CYAN}# Edit .env with your configuration{Style.RESET_ALL}")
        click.echo(f"  {Fore.CYAN}uvicorn app.main:app --reload{Style.RESET_ALL}")
        
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        # Cleanup if something went wrong
        if os.path.exists(project_dir):
            shutil.rmtree(project_dir)
        sys.exit(1)


if __name__ == "__main__":
    main() 