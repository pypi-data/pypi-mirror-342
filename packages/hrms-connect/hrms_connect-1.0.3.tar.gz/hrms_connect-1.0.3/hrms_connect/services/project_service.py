import json
from pathlib import Path

PROJECTS_FILE = Path("projects.json")


def load_projects():
    if not PROJECTS_FILE.exists():
        return []
    with open(PROJECTS_FILE, "r") as f:
        return json.load(f)


def save_projects(projects):
    with open(PROJECTS_FILE, "w") as f:
        json.dump(projects, f, indent=2)


def list_projects():
    return load_projects()


def add_project(name):
    projects = load_projects()
    if name in projects:
        return f"⚠️ Project '{name}' already exists."
    projects.append(name)
    save_projects(projects)
    return f"✅ Project '{name}' added."


def delete_project(name):
    projects = load_projects()
    if name not in projects:
        return f"❌ Project '{name}' not found."
    projects.remove(name)
    save_projects(projects)
    return f"🗑️ Project '{name}' deleted."
