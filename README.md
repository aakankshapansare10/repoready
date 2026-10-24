# RepoReady

RepoReady is a beginner-friendly Python command-line tool that checks a local repository for the essentials that make a GitHub project easy to understand and use.

## What it checks now

- Whether the project root contains a README (`README`, `README.md`, `README.markdown`, `README.rst`, or `README.txt`).
- Whether it contains a common license filename, such as `LICENSE`, `LICENSE.md`, `COPYING`, or `UNLICENSE`.
- Whether it contains a `.gitignore` file.
- Whether `.github/workflows/` contains a GitHub Actions workflow ending in `.yml` or `.yaml`.

The current checklist gives each of these four checks equal weight. It checks whether expected files are present, not whether their content is good. Treat the score as a reminder list, not a measure of code quality. License detection checks a filename only; choosing a license and its terms is up to the project owner.

## Automated code check

On pushes and pull requests, GitHub Actions installs the project with its development tools and runs Ruff to check Python code style. It does not run a test suite yet.

## Learning roadmap

1. Accept a project folder from the command line. **Done**
2. Inspect files in that folder safely. **Done**
3. Add more checks and turn findings into a clear score. **First score done; more checks planned**
4. Export a report people can share. **JSON output added**
5. Package the tool so it is easy to install.

## Start here

Use Python 3.10 or newer. From this folder, create and activate a virtual environment, then install the project in editable mode:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -e .
```

Print a human-readable checklist or a JSON report:

```powershell
repoready .
repoready . --json
```

The JSON report includes the project folder name, each check's result and relative file path, any suggested next step, and the score. It does not include the full local folder path.

