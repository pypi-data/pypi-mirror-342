"""Verification setup command.

This module provides the command to verify the installation.
"""

import sys


def main() -> int:
    """Run the verification setup command.

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    # This is equivalent to the current snowpack-verify command
    from snowpack_stack.cli.verify import main as verify_main

    return verify_main()


if __name__ == "__main__":
    sys.exit(main())
