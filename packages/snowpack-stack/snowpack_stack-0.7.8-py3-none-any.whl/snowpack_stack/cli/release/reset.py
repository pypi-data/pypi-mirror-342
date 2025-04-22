"""Reset a version by deleting and recreating the tag.

This module provides a command to reset a version by deleting its tag
and recreating it, which can be useful for fixing mistakes in releases.
"""

import argparse
import sys
from typing import List, Optional, Union

# Import our secure subprocess utilities
from snowpack_stack.utils.subprocess_utils import run_git_command, validate_command_argument


def reset_version(version: str) -> int:
    """
    Reset a version by deleting and recreating the tag.

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
        # Delete the tag locally
        run_git_command(["tag", "-d", tag_version], check=False)

        # Delete the tag remotely
        run_git_command(["push", "--delete", "origin", tag_version], check=False)

        # Run the release script to recreate the tag
        from snowpack_stack.cli.release import run_script

        return run_script("release.py", "--set", version)
    except Exception as e:
        print(f"Error resetting version: {e}")
        return 1


def main(args: Optional[Union[List[str], argparse.Namespace]] = None) -> int:
    """
    Main entry point for the reset version CLI command.

    Args:
        args: Command-line arguments or argparse.Namespace object

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    # If args is already a Namespace object, extract values directly
    if isinstance(args, argparse.Namespace):
        version = getattr(args, "version", None)
        if not version:
            print("Error: Version is required")
            return 1
        return reset_version(version)

    # Otherwise, parse arguments normally
    parser = argparse.ArgumentParser(
        description="Reset a version by deleting and recreating the tag"
    )
    parser.add_argument("version", help="Version to reset (e.g., '0.4.1')")

    parsed_args = parser.parse_args(args)

    return reset_version(parsed_args.version)


if __name__ == "__main__":
    sys.exit(main())
