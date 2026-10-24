"""Checks for the project files RepoReady knows about."""

from pathlib import Path

README_NAMES = {
    "readme",
    "readme.md",
    "readme.markdown",
    "readme.rst",
    "readme.txt",
}

LICENSE_NAMES = {
    "license",
    "license.md",
    "license.markdown",
    "license.rst",
    "license.txt",
    "license-mit",
    "license-mit.txt",
    "license-apache",
    "license-apache.txt",
    "license-apache-2.0",
    "licence",
    "licence.md",
    "licence.rst",
    "licence.txt",
    "copying",
    "copying.md",
    "copying.txt",
    "unlicense",
}

GITIGNORE_NAMES = {".gitignore"}
WORKFLOW_EXTENSIONS = {".yml", ".yaml"}


def _find_named_file(project_path: Path, accepted_names: set[str]) -> Path | None:
    """Find the first root-level file whose name is in accepted_names."""
    for item in project_path.iterdir():
        if item.is_file() and item.name.casefold() in accepted_names:
            return item
    return None


def find_readme(project_path: Path) -> Path | None:
    """Return the README file in a project root, or None when it is missing."""
    return _find_named_file(project_path, README_NAMES)


def find_license(project_path: Path) -> Path | None:
    """Return a common license file in a project root, or None when missing."""
    return _find_named_file(project_path, LICENSE_NAMES)


def find_gitignore(project_path: Path) -> Path | None:
    """Return the .gitignore file in a project root, or None when missing."""
    return _find_named_file(project_path, GITIGNORE_NAMES)


def find_github_workflow(project_path: Path) -> Path | None:
    """Return a YAML GitHub Actions workflow, or None when no workflow exists."""
    workflow_directory = project_path / ".github" / "workflows"
    if not workflow_directory.is_dir():
        return None

    for item in workflow_directory.iterdir():
        if item.is_file() and item.suffix.casefold() in WORKFLOW_EXTENSIONS:
            return item
    return None
