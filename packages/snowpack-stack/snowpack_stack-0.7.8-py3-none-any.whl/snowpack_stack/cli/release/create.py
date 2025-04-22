"""Create a new release.

This module provides a command to create a new release by bumping the version
or setting a specific version, with support for both standard releases and pre-releases.
"""

import argparse
import sys
from typing import List, Optional, Union

# Import our secure subprocess utilities


def create_release(
    version_bump: Optional[str] = None,
    specific_version: Optional[str] = None,
    pre_release: bool = False,
    no_push: bool = False,
) -> int:
    """
    Create a new release by bumping the version or setting a specific version.

    This will:
    1. Update version in pyproject.toml and __init__.py
    2. Commit those changes
    3. Create a git tag
    4. Optionally push the changes to the remote

    Args:
        version_bump: Which component to bump (major, minor, patch)
        specific_version: Specific version to set
        pre_release: Whether to create a pre-release (for feature branches)
        no_push: Whether to push the changes to remote

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    try:
        # Run the release.py script
        from snowpack_stack.cli.release import run_script

        cmd_args = []

        if specific_version:
            cmd_args.extend(["--set", specific_version])
        elif version_bump:
            cmd_args.append(version_bump)
        else:
            print("Error: Either version_bump or specific_version is required")
            return 1

        if pre_release:
            cmd_args.append("--pre-release")

        if no_push:
            cmd_args.append("--no-push")

        result = run_script("release.py", *cmd_args)

        if result == 0:
            print("✅ Release created successfully!")
            print(
                "The version has been updated in files, committed, tagged, and optionally pushed."
            )

        return result
    except Exception as e:
        print(f"Error creating release: {e}")
        return 1


def main(args: Optional[Union[List[str], argparse.Namespace]] = None) -> int:
    """
    Main entry point for the create release CLI command.

    Args:
        args: Command-line arguments or argparse.Namespace object

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    # If args is already a Namespace object, extract values directly
    if isinstance(args, argparse.Namespace):
        return create_release(
            version_bump=getattr(args, "version_bump", None),
            specific_version=getattr(args, "specific_version", None),
            pre_release=getattr(args, "pre_release", False),
            no_push=getattr(args, "no_push", False),
        )

    # Otherwise, parse arguments normally
    parser = argparse.ArgumentParser(description="Create a new release")
    parser.add_argument(
        "version_bump",
        nargs="?",
        choices=["major", "minor", "patch"],
        help="Version component to bump",
    )
    parser.add_argument(
        "--set", dest="specific_version", help="Set a specific version instead of bumping"
    )
    parser.add_argument(
        "--pre-release",
        action="store_true",
        help="Create a pre-release version (for feature branches)",
    )
    parser.add_argument("--no-push", action="store_true", help="Don't push changes to remote")

    parsed_args = parser.parse_args(args)

    return create_release(
        version_bump=parsed_args.version_bump,
        specific_version=parsed_args.specific_version,
        pre_release=parsed_args.pre_release,
        no_push=parsed_args.no_push,
    )


if __name__ == "__main__":
    sys.exit(main())
