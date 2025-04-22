"""Verification command to check installation.

This module provides a simple command to verify that the package is installed correctly.
"""

import logging
import sys
from typing import List, Optional

from snowpack_stack.auth import authenticate, get_user_email

# Configure logging
logger = logging.getLogger(__name__)


def main(args: Optional[List[str]] = None) -> int:
    """Run the verification command.

    Args:
        args: Command line arguments (not used)

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    print("Verifying Snowpack Stack installation...")
    print(f"Snowpack Stack version: {__import__('snowpack_stack').__version__}")

    # Check authentication status
    authenticate()
    email = get_user_email()
    if email:
        print(f"User email: {email}")
    else:
        print("No user email set. You can set one with:")
        print("  snowpack setup auth --email <your-email>")
        print("This is optional but helps with usage tracking and support.")

    # Check if we're in a virtual environment
    in_venv = sys.prefix != sys.base_prefix
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"Python version: {python_version}")
    print(f"Using virtual environment: {'Yes' if in_venv else 'No'}")

    # Print a success message
    print("\n✅ Snowpack Stack is ready to use!")
    print("\nQuick start:")
    print("  # Set your email (optional)")
    print("  snowpack setup auth --email your.email@example.com")
    print("\n  # Generate YAML assets")
    print("  snowpack build bruin yaml")
    print("\n  # Generate SQL assets")
    print("  snowpack build bruin sql")
    print("\n  # Run all generators")
    print("  snowpack build")

    return 0


if __name__ == "__main__":
    sys.exit(main())
