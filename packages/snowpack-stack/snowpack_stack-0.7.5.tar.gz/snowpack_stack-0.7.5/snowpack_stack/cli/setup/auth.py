"""Authentication setup command.

This module provides the command to set up authentication.
"""

import argparse
import sys
from typing import List, Optional


def main(args: Optional[List[str]] = None) -> int:
    """Run the authentication setup command.

    Args:
        args: Command line arguments (defaults to sys.argv[1:])

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    # This is equivalent to the current snowpack-auth command
    from snowpack_stack.cli.auth import authenticate_email
    from snowpack_stack.cli.auth import main as auth_main

    # If we're being called from the main CLI parser, args will be None
    # or it will be a Namespace object with an email attribute
    if args is None:
        return auth_main()

    # If args is a list, parse it
    if isinstance(args, list):
        parser = argparse.ArgumentParser(description="Authentication setup")
        parser.add_argument("--email", help="Email address for authentication")
        parsed_args = parser.parse_args(args)

        # Pass the email to the auth_main function if provided
        if hasattr(parsed_args, "email") and parsed_args.email:
            return auth_main(["--email", parsed_args.email])
        return auth_main()

    # If args is a Namespace object, extract the email if present
    if hasattr(args, "email") and args.email:
        return authenticate_email(args.email)

    return authenticate_email()


if __name__ == "__main__":
    sys.exit(main())
