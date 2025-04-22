"""
Shared utilities for the Snowpack Stack tool manager.

This module provides common functions used across the tool manager commands.
"""

import logging

# Setup logging
logger = logging.getLogger(__name__)


def print_header(text):
    """
    Print a formatted header with the provided text.

    Args:
        text (str): The header text to print
    """
    print(f"\n{'=' * 50}")
    print(f"  {text}")
    print(f"{'=' * 50}\n")


def print_success(text):
    """
    Print a success message.

    Args:
        text (str): The success message to print
    """
    print(f"\n✅ {text}")


def print_warning(text):
    """
    Print a warning message.

    Args:
        text (str): The warning message to print
    """
    print(f"\n⚠️  {text}")


def print_error(text):
    """
    Print an error message.

    Args:
        text (str): The error message to print
    """
    print(f"\n❌ {text}")


def handle_command_exception(e, command_name):
    """
    Handle exceptions in command execution with standardized error reporting.

    Args:
        e (Exception): The exception that was raised
        command_name (str): The name of the command that raised the exception

    Returns:
        int: Exit code (always 1 for errors)
    """
    if isinstance(e, KeyboardInterrupt):
        print("\nOperation cancelled by user.")
    else:
        logger.error(f"Error in {command_name} command: {e}")
        print_error(f"An unexpected error occurred: {e}")

    return 1
