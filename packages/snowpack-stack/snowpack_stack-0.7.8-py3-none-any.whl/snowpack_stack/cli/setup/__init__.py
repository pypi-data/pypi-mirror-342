"""Setup CLI commands.

This package provides CLI commands for setting up and configuring Snowpack Stack,
including authentication, verification, and key rotation.
"""

from typing import List, Optional


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the setup CLI command.

    Args:
        args: Command line arguments

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    # Default to verify if no subcommand is provided
    if not args or not args[0]:
        from snowpack_stack.cli.setup.verify import main as verify_main

        return verify_main()

    # Process subcommands
    subcommand = args[0]

    # Import these only if needed to avoid circular imports
    from snowpack_stack.utils.subprocess_utils import validate_command_argument

    # Validate subcommand
    if not validate_command_argument(subcommand):
        print(f"Error: Invalid subcommand: {subcommand}")
        return 1

    # Handle different subcommands
    if subcommand == "verify":
        from snowpack_stack.cli.setup.verify import main as verify_main

        return verify_main()
    elif subcommand == "verify-internal":
        from snowpack_stack.cli.setup.verify_internal import main as verify_internal_main

        return verify_internal_main()
    elif subcommand == "auth":
        from snowpack_stack.cli.setup.auth import main as auth_main

        if len(args) > 1:
            return auth_main(args[1:])
        else:
            return auth_main()
    elif subcommand == "rotate-key":
        from snowpack_stack.cli.setup.rotate_key import main as rotate_key_main

        return rotate_key_main()
    else:
        print(f"Error: Unknown subcommand: {subcommand}")
        return 1
