"""CLI commands for managing Snowpack Stack releases.

This module provides CLI commands for managing Snowpack Stack releases,
including checking versions, creating releases, and resetting versions.
"""

import argparse
import sys

# Import the run_script function from the release package
from snowpack_stack.cli.release import run_script

# Import our secure subprocess utilities instead of using subprocess directly
from snowpack_stack.utils.subprocess_utils import (
    run_command,
    run_git_command,
    validate_command_argument,
)


def safe_run_command(cmd, check=True, capture_output=True):
    """Run a command safely with validation.

    Args:
        cmd: Command to run (list)
        check: Whether to check return code
        capture_output: Whether to capture stdout/stderr

    Returns:
        subprocess.CompletedProcess: Result of the command
    """
    # Validate all command arguments
    for arg in cmd:
        if not validate_command_argument(str(arg)):
            print(f"Error: Invalid command argument: {arg}")
            raise ValueError(f"Invalid command argument: {arg}")

    try:
        return run_command(cmd=cmd, check=check, capture_output=capture_output, text=True)
    except Exception as e:
        print(f"Error running command: {e}")
        raise


def reset_version(version):
    """Reset a version by deleting and recreating the tag.

    Args:
        version: Version to reset (e.g., "0.4.1")

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    # Validate version input
    if not validate_command_argument(version):
        print(f"Error: Invalid version: {version}")
        return 1

    # Format the version with 'v' prefix if not already present
    tag_version = version if version.startswith("v") else f"v{version}"

    try:
        # Delete the tag locally - use our secure git command function
        run_git_command(["tag", "-d", tag_version], check=False)

        # Delete the tag remotely - use our secure git command function
        run_git_command(["push", "--delete", "origin", tag_version], check=False)

        # Use the release script with the specific version
        return run_script("release.py", "--set", version)
    except Exception as e:
        print(f"Error resetting version: {e}")
        return 1


def main():
    """Main entry point for the release CLI command.

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    parser = argparse.ArgumentParser(description="Manage Snowpack Stack releases")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Check version command
    check_parser = subparsers.add_parser(
        "check", help="Check version consistency across files and Git tags"
    )
    check_parser.epilog = """
    The check command verifies that versions are consistent between:
    - pyproject.toml
    - snowpack_stack/__init__.py
    - Latest Git tag
    
    This helps ensure your code and Git tags are properly synchronized.
    """
    check_parser.formatter_class = argparse.RawDescriptionHelpFormatter

    # Release command
    release_parser = subparsers.add_parser("create", help="Create a new release")
    release_parser.add_argument(
        "version_bump",
        nargs="?",
        choices=["major", "minor", "patch"],
        help="Version component to bump",
    )
    release_parser.add_argument(
        "--set", dest="specific_version", help="Set a specific version instead of bumping"
    )
    release_parser.add_argument(
        "--pre-release",
        action="store_true",
        help="Create a pre-release version (for feature branches)",
    )
    release_parser.add_argument(
        "--no-push", action="store_true", help="Don't push changes to remote"
    )

    # Add more detailed description to help text
    release_parser.epilog = """
    The create command will:
    1. Update the version in pyproject.toml and __init__.py
    2. Commit these changes to Git
    3. Create a Git tag matching the version
    4. Push the changes and tag to the remote (unless --no-push is used)
    
    This ensures that the version in your code always matches the Git tag.
    """
    release_parser.formatter_class = argparse.RawDescriptionHelpFormatter

    # Reset command
    reset_parser = subparsers.add_parser(
        "reset", help="Reset a version by deleting and recreating the tag"
    )
    reset_parser.add_argument("version", help="Version to reset (e.g., '0.4.1')")

    # Changelog command
    changelog_parser = subparsers.add_parser("changelog", help="Generate a changelog")
    changelog_parser.add_argument(
        "--from", dest="from_ref", help="Starting reference (tag or commit)"
    )
    changelog_parser.add_argument(
        "--to", dest="to_ref", default="HEAD", help="Ending reference (tag or commit)"
    )
    changelog_parser.add_argument("--output", help="Output file (default: stdout)")

    # Status command
    status_parser = subparsers.add_parser(
        "status", help="Show status of versions, branches, and publishing"
    )

    args = parser.parse_args()

    # Validate all string inputs from args
    if args.command == "reset" and hasattr(args, "version"):
        if not validate_command_argument(args.version):
            print(f"Error: Invalid version: {args.version}")
            return 1

    if args.command == "create" and hasattr(args, "specific_version") and args.specific_version:
        if not validate_command_argument(args.specific_version):
            print(f"Error: Invalid version: {args.specific_version}")
            return 1

    if args.command == "changelog":
        if (
            hasattr(args, "from_ref")
            and args.from_ref
            and not validate_command_argument(args.from_ref)
        ):
            print(f"Error: Invalid from reference: {args.from_ref}")
            return 1
        if hasattr(args, "to_ref") and args.to_ref and not validate_command_argument(args.to_ref):
            print(f"Error: Invalid to reference: {args.to_ref}")
            return 1
        if hasattr(args, "output") and args.output and not validate_command_argument(args.output):
            print(f"Error: Invalid output file: {args.output}")
            return 1

    if args.command == "check":
        return run_script("check_version_consistency.py")

    elif args.command == "create":
        cmd_args = []

        if args.specific_version:
            cmd_args.extend(["--set", args.specific_version])
        elif args.version_bump:
            cmd_args.append(args.version_bump)
        else:
            parser.error("Either version_bump or --set is required for release command")

        if args.pre_release:
            cmd_args.append("--pre-release")

        if args.no_push:
            cmd_args.append("--no-push")

        return run_script("release.py", *cmd_args)

    elif args.command == "reset":
        return reset_version(args.version)

    elif args.command == "changelog":
        cmd_args = []

        if args.from_ref:
            cmd_args.extend(["--from", args.from_ref])

        if args.to_ref:
            cmd_args.extend(["--to", args.to_ref])

        if args.output:
            cmd_args.extend(["--output", args.output])

        return run_script("generate_changelog.py", *cmd_args)

    elif args.command == "status":
        return run_script("check_release_status.py")

    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
