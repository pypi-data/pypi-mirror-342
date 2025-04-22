"""Authentication CLI module for Snowpack Stack."""

import argparse
import logging
import sys
from typing import List, Optional

from snowpack_stack.auth import clear_saved_credentials, set_user_email

logger = logging.getLogger(__name__)


def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def check_dependencies() -> bool:
    """
    Check if required dependencies are installed.
    This is a simplified version that always returns True.

    Returns:
        bool: Always returns True in this simplified version
    """
    logger.info("Dependency check simplified - assuming all dependencies are available")
    return True


def authenticate_email(email: Optional[str] = None) -> bool:
    """
    Authenticate the user with their email address.
    This is a simplified version that just stores the email.

    Args:
        email: The email address to authenticate with (optional, will prompt if not provided)

    Returns:
        bool: True if successful
    """
    # Prompt for email if not provided
    if not email:
        print("Please enter your email address to identify yourself with Snowpack Stack.")
        print("This email is stored locally and used for displaying in generated assets.")
        email = input("Email: ")

    if not email or "@" not in email:
        print("Invalid email format. Please provide a valid email address.")
        return False

    # Set the email in the authentication module
    result = set_user_email(email)

    if result:
        print(f"Email '{email}' has been stored successfully.")
    else:
        print("Failed to store email. Please try again.")

    return result


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command line arguments.

    Args:
        args: Command line arguments (defaults to sys.argv[1:])

    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(description="Snowpack Stack Authentication")

    # Email argument
    parser.add_argument("--email", help="Email address to use for authentication")

    # Clear argument
    parser.add_argument("--clear", action="store_true", help="Clear saved credentials")

    return parser.parse_args(args)


def main(args_list: Optional[List[str]] = None) -> int:
    """
    Main entry point for authentication CLI.

    Args:
        args_list: Command line arguments (defaults to sys.argv[1:])

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    setup_logging()

    # Parse arguments
    if isinstance(args_list, argparse.Namespace):
        args = args_list
    else:
        args = parse_args(args_list)

    # Check dependencies
    if not check_dependencies():
        logger.error("Missing required dependencies")
        return 1

    # Handle --clear flag
    if args.clear:
        if clear_saved_credentials():
            logger.info("Credentials cleared successfully")
            return 0
        else:
            logger.error("Failed to clear credentials")
            return 1

    # Normal authentication
    success = authenticate_email(args.email)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
