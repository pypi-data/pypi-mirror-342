import os
import shutil
from pathlib import Path

import jinja2


def copy_templates(templates_dir: str, project_dir: str, project_name: str):
    """Copy template files to the project directory with variable substitution.
    
    Args:
        templates_dir: Path to templates directory
        project_dir: Path to target project directory
        project_name: Name of the project
    """
    template_path = os.path.join(templates_dir, "default")
    
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template directory not found: {template_path}")
    
    # Setup Jinja2 environment
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_path),
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    
    # Variables to substitute in templates
    variables = {
        "project_name": project_name,
        "project_title": project_name.replace("-", " ").replace("_", " ").title(),
        "package_name": project_name.replace("-", "_").lower(),
    }
    
    # Process each file in the template directory
    for root, dirs, files in os.walk(template_path):
        # Get the relative path from the template directory
        rel_path = os.path.relpath(root, template_path)
        
        # Create the corresponding directory in the project
        if rel_path != ".":
            target_dir = os.path.join(project_dir, rel_path)
            os.makedirs(target_dir, exist_ok=True)
        
        # Process each file
        for file in files:
            src_file = os.path.join(root, file)
            
            # Skip certain files
            if file.endswith(".pyc") or file.startswith("__pycache__"):
                continue
            
            # Determine the target file path
            if rel_path == ".":
                tgt_file = os.path.join(project_dir, file)
            else:
                tgt_file = os.path.join(project_dir, rel_path, file)
            
            # Process files with Jinja2 if they're text files
            if _is_text_file(src_file):
                with open(src_file, "r", encoding="utf-8") as f:
                    content = f.read()
                
                try:
                    template = env.from_string(content)
                    rendered = template.render(**variables)
                    
                    with open(tgt_file, "w", encoding="utf-8") as f:
                        f.write(rendered)
                except Exception as e:
                    print(f"Warning: Could not render template {src_file}: {str(e)}")
                    # Fallback to copying the file as-is
                    shutil.copy2(src_file, tgt_file)
            else:
                # Binary files are copied as-is
                shutil.copy2(src_file, tgt_file)


def _is_text_file(file_path: str) -> bool:
    """Determine if a file is a text file."""
    # Common text file extensions
    text_extensions = {
        ".py", ".txt", ".md", ".html", ".css", ".js", ".json", ".yml", ".yaml", 
        ".ini", ".cfg", ".toml", ".env", ".example", ".gitignore", ".sh", ".bat", 
        ".ps1", ".sql", ".xml"
    }
    
    ext = os.path.splitext(file_path)[1].lower()
    if ext in text_extensions:
        return True
    
    # Try to read the file as text
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            f.read(1024)  # Read a small chunk
        return True
    except:
        return False 