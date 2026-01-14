#!/usr/bin/env python3
"""
Package skill with UTF-8 encoding support
"""
import sys
import os
import re
import zipfile
from pathlib import Path

def read_text_with_utf8(path):
    """Read text file with UTF-8 encoding"""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def validate_skill(skill_path):
    """Validate skill structure"""
    skill_path = Path(skill_path)

    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found"

    # Read and validate frontmatter
    try:
        content = read_text_with_utf8(skill_md)
    except UnicodeDecodeError:
        return False, "SKILL.md must be UTF-8 encoded"

    if not content.startswith('---'):
        return False, "No YAML frontmatter found"

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    # Parse YAML frontmatter
    import yaml
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in frontmatter: {e}"

    # Check required fields
    if 'name' not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if 'description' not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    name = frontmatter.get('name', '')
    if not re.match(r'^[a-z0-9-]+$', name):
        return False, f"Name '{name}' should be hyphen-case"

    return True, "Skill is valid!"

def package_skill(skill_path, output_dir=None):
    """Package skill into .skill file"""
    skill_path = Path(skill_path)
    name = skill_path.name

    valid, message = validate_skill(skill_path)
    if not valid:
        print(f"Validation failed: {message}")
        return False

    if output_dir is None:
        output_dir = skill_path.parent
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{name}.skill"

    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(skill_path):
            # Skip __pycache__ and .git
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git']]
            for file in files:
                if file.endswith('.pyc'):
                    continue
                file_path = Path(root) / file
                arcname = file_path.relative_to(skill_path)
                zf.write(file_path, arcname)

    print(f"Packaged: {output_file}")
    return True

if __name__ == "__main__":
    skill_path = sys.argv[1] if len(sys.argv) > 1 else '.'
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    valid, message = validate_skill(skill_path)
    print(message)

    if valid:
        package_skill(skill_path, output_dir)
