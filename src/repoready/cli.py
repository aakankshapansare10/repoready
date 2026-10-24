"""Command-line entry point for RepoReady."""

import argparse
import json
import sys
from pathlib import Path

from repoready import __version__
from repoready.checks import (
    find_github_workflow,
    find_gitignore,
    find_license,
    find_readme,
)


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="repoready",
        description="Check whether a local project has the essentials for GitHub.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        type=Path,
        help="project directory to inspect (defaults to the current directory)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="print the findings as JSON",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="save JSON output to this file",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="allow replacing an existing output file",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def main() -> int:
    """Check the requested folder and print or save the results."""
    parser = build_parser()
    args = parser.parse_args()

    if args.output is not None and not args.json:
        parser.error("--output requires --json")
    if args.force and args.output is None:
        parser.error("--force requires --output")

    project_path = args.path.expanduser().resolve()

    if not project_path.exists():
        print(f"Error: folder does not exist: {project_path}", file=sys.stderr)
        return 2
    if not project_path.is_dir():
        print(f"Error: expected a folder, got a file: {project_path}", file=sys.stderr)
        return 2

    try:
        readme_path = find_readme(project_path)
        license_path = find_license(project_path)
        gitignore_path = find_gitignore(project_path)
        workflow_path = find_github_workflow(project_path)
    except OSError as error:
        print(f"Error: cannot inspect folder: {error}", file=sys.stderr)
        return 2

    check_definitions = [
        (
            "README",
            readme_path,
            "Add a README.md with an overview, setup steps, and usage.",
        ),
        (
            "License",
            license_path,
            "Choose a license, then add its text in a LICENSE file.",
        ),
        (
            ".gitignore",
            gitignore_path,
            "Add rules for generated files and local environment folders.",
        ),
        (
            "GitHub Actions workflow",
            workflow_path,
            "Add a YAML workflow under .github/workflows/ to automate checks.",
        ),
    ]

    check_results = []
    for check_name, found_path, suggestion in check_definitions:
        relative_path = (
            found_path.relative_to(project_path).as_posix()
            if found_path is not None
            else None
        )
        check_results.append(
            {
                "name": check_name,
                "passed": found_path is not None,
                "path": relative_path,
                "suggestion": None if found_path is not None else suggestion,
            }
        )

    passed_count = sum(result["passed"] for result in check_results)
    score = passed_count * 100 // len(check_results)
    report = {
        "project": project_path.name,
        "checks": check_results,
        "score": {
            "points": score,
            "max_points": 100,
            "passed": passed_count,
            "total": len(check_results),
        },
    }

    if args.json:
        report_text = json.dumps(report, indent=2) + "\n"
        if args.output is None:
            print(report_text, end="")
            return 0

        output_path = args.output.expanduser().resolve()
        if output_path.is_dir():
            print(f"Error: output path is a folder: {output_path}", file=sys.stderr)
            return 2
        if output_path.exists() and not args.force:
            print(
                f"Error: output file already exists: {output_path}. "
                "Use --force to replace it.",
                file=sys.stderr,
            )
            return 2
        try:
            output_path.write_text(report_text, encoding="utf-8")
        except OSError as error:
            print(f"Error: cannot write report: {error}", file=sys.stderr)
            return 2
        print(f"JSON report saved: {output_path}")
        return 0

    print(f"RepoReady scan: {project_path}")
    for result in check_results:
        if result["passed"]:
            print(f"[PASS] {result['name']} found: {result['path']}")
        else:
            print(f"[TODO] No {result['name']} found.")
            print(f"       {result['suggestion']}")

    print(
        f"\nProject checklist: {score}/100 "
        f"({passed_count}/{len(check_results)} checks passed)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
