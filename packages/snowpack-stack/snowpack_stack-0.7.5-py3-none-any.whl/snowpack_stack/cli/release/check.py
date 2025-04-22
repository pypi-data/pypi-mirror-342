"""Check if a version exists in the repository.

This module provides a command to check if a version exists in the repository,
which is useful before creating a new release.
"""

import argparse
import sys
from typing import List, Optional, Union

# Import our secure subprocess utilities


def check_version() -> int:
    """
    Check if a version exists in the repository.

    Returns:
        int: Exit code (0 if safe to publish, 1 if exists, 2 if error)
    """
    try:
        # Run the check_version.py script from the parent directory
        from snowpack_stack.cli.release import run_script

        return run_script("check_version.py")
    except Exception as e:
        print(f"Error checking version: {e}")
        return 2


def main(args: Optional[Union[List[str], argparse.Namespace]] = None) -> int:
    """
    Main entry point for the check version CLI command.

    Args:
        args: Command-line arguments or argparse.Namespace object (unused, kept for consistency)

    Returns:
        int: Exit code (0 if safe to publish, 1 if exists, 2 if error)
    """
    # For the check command, we don't need to parse any arguments
    # But we still need to handle both list and Namespace cases consistently
    return check_version()


if __name__ == "__main__":
    sys.exit(main())
