"""
Access control module for Snowpack Stack.

This module provides role-based access control functionality for differentiating
between public and internal features. It uses API key verification to authenticate
Snowpack developers for access to internal features.
"""

import hmac
import logging
import os
import secrets
import socket
from datetime import datetime
from typing import Any, Dict

# Configure logging
logger = logging.getLogger(__name__)


# Define access levels
class AccessLevel:
    """Access level constants for different types of features."""

    PUBLIC = "public"
    INTERNAL = "internal"


# Base exceptions for authentication
class SnowpackAuthError(Exception):
    """Base exception for all authentication errors."""


class KeyMissingError(SnowpackAuthError):
    """Raised when required API keys are missing."""


class AccessDeniedError(SnowpackAuthError):
    """Raised when a user tries to access restricted commands."""


class ConfigurationError(SnowpackAuthError):
    """Raised when there's an issue with the authentication configuration."""


# Command definitions with access levels
COMMANDS = {
    "build": {
        "access_level": AccessLevel.PUBLIC,
        "description": "Generate assets",
    },
    "setup": {
        "access_level": AccessLevel.PUBLIC,
        "description": "Configure your environment",
        "subcommands": {
            "auth": {
                "access_level": AccessLevel.PUBLIC,
                "description": "Set up authentication",
            },
            "verify": {
                "access_level": AccessLevel.PUBLIC,
                "description": "Verify installation",
            },
            "verify-internal": {
                "access_level": AccessLevel.PUBLIC,
                "description": "Verify internal developer access",
            },
            "rotate-key": {
                "access_level": AccessLevel.INTERNAL,
                "description": "Generate a new API key",
            },
        },
    },
    "release": {
        "access_level": AccessLevel.INTERNAL,
        "description": "Manage releases and versions",
    },
}


def is_snowpack_developer() -> bool:
    """
    Check if the user is a verified Snowpack developer.

    This function checks if the user has the proper API key set in their
    environment that matches the expected key value for Snowpack developers.

    Returns:
        bool: True if the user is a verified Snowpack developer, False otherwise.

    Raises:
        KeyMissingError: If the user's API key is not set but an expected key is.
    """
    expected_key = os.environ.get("SNOWPACK_STACK_INTERNAL_KEY")
    user_key = os.environ.get("SNOWPACK_STACK_API_KEY")

    if not expected_key:
        logger.warning(
            "SNOWPACK_STACK_INTERNAL_KEY environment variable not set. Running in public mode."
        )
        return False

    if not user_key:
        raise KeyMissingError(
            "SNOWPACK_STACK_API_KEY environment variable not found.\n"
            "To access internal features, please:\n"
            '1. Generate a key using: python -c "import secrets; print(secrets.token_hex(32))"\n'
            '2. Add the key to your .zshrc: export SNOWPACK_STACK_API_KEY="your_generated_key"\n'
            "3. Contact the Snowpack team to validate your key for access."
        )

    # Use constant-time comparison to prevent timing attacks
    return hmac.compare_digest(user_key, expected_key)


def check_command_access(command_name: str, subcommand_name: str = None) -> bool:
    """
    Check if the user has access to the specified command.

    This function verifies whether the current user has permission to execute
    the requested command based on the command's access level (public or internal).
    Public commands are available to all users, while internal commands require
    a valid API key.

    Args:
        command_name (str): The name of the command to check access for.
        subcommand_name (str, optional): The name of the subcommand, if applicable.

    Returns:
        bool: True if access is granted.

    Raises:
        ValueError: If the command or subcommand name is unknown.
        AccessDeniedError: If the user doesn't have access to the command.
        KeyMissingError: If the required API key is missing.
    """
    if command_name not in COMMANDS:
        raise ValueError(f"Unknown command: {command_name}")

    command_info = COMMANDS[command_name]

    # Check subcommand access if provided
    if subcommand_name:
        if "subcommands" not in command_info or subcommand_name not in command_info["subcommands"]:
            raise ValueError(f"Unknown subcommand: {command_name} {subcommand_name}")

        required_level = command_info["subcommands"][subcommand_name]["access_level"]
    else:
        required_level = command_info["access_level"]

    # Public commands are always accessible
    if required_level == AccessLevel.PUBLIC:
        return True

    # Internal commands require verification
    if required_level == AccessLevel.INTERNAL:
        # Log access attempt
        verify_key_usage(command_name, subcommand_name)

        if is_snowpack_developer():
            return True
        else:
            command_desc = (
                f"'{command_name} {subcommand_name}'" if subcommand_name else f"'{command_name}'"
            )
            raise AccessDeniedError(
                f"The {command_desc} command is restricted to Snowpack developers. "
                "Please contact the Snowpack team for access."
            )


def verify_key_usage(command_name: str, subcommand_name: str = None) -> None:
    """
    Monitor and log API key usage.

    This function records when internal commands are accessed,
    which can help detect potential unauthorized access attempts.

    Args:
        command_name (str): The name of the command being accessed.
        subcommand_name (str, optional): The name of the subcommand, if applicable.
    """
    command_desc = f"{command_name} {subcommand_name}" if subcommand_name else command_name

    if subcommand_name and "subcommands" in COMMANDS.get(command_name, {}):
        subcommand_info = COMMANDS[command_name]["subcommands"].get(subcommand_name, {})
        if subcommand_info.get("access_level") == AccessLevel.INTERNAL:
            logger.info(
                f"Internal command '{command_desc}' accessed",
                extra={
                    "command": command_desc,
                    "user_email": os.environ.get("SNOWPACK_USER_EMAIL", "unknown"),
                    "timestamp": datetime.now().isoformat(),
                    "hostname": socket.gethostname(),
                },
            )
    elif COMMANDS.get(command_name, {}).get("access_level") == AccessLevel.INTERNAL:
        logger.info(
            f"Internal command '{command_desc}' accessed",
            extra={
                "command": command_desc,
                "user_email": os.environ.get("SNOWPACK_USER_EMAIL", "unknown"),
                "timestamp": datetime.now().isoformat(),
                "hostname": socket.gethostname(),
            },
        )


def get_key_info() -> Dict[str, Any]:
    """
    Get information about the current API key configuration.

    Returns:
        Dict[str, Any]: Information about the key configuration.
    """
    key = os.environ.get("SNOWPACK_STACK_API_KEY", "")
    if not key:
        return {"status": "missing", "message": "No API key configured"}

    # Only take first few and last few chars for identification without exposing key
    key_hint = f"{key[:3]}...{key[-3:]}" if len(key) > 6 else "***"

    return {
        "status": "configured",
        "key_hint": key_hint,
    }


def rotate_key() -> str:
    """
    Generate a new API key.

    This is a utility function that generates a new API key and
    provides instructions for updating the key in the environment.

    Returns:
        str: The newly generated key.
    """
    new_key = secrets.token_hex(32)

    print("New API key generated:")
    print(f"  {new_key}")
    print("\nTo use this key:")
    print("1. Update your .zshrc file:")
    print(f'   export SNOWPACK_STACK_API_KEY="{new_key}"')
    print("2. Contact the Snowpack team to update the master key")
    print("3. After confirmation, source your .zshrc:")
    print("   source ~/.zshrc")

    return new_key


# Configure logging filter for sensitive data
class SensitiveDataFilter(logging.Filter):
    """Filter to prevent sensitive data from being logged."""

    def __init__(self, patterns=None):
        super().__init__()
        self.patterns = patterns or [
            "SNOWPACK_STACK_API_KEY",
            "SNOWPACK_STACK_INTERNAL_KEY",
            "api_key",
            "secret",
            "password",
            "token",
        ]

    def filter(self, record):
        if hasattr(record, "msg") and record.msg and isinstance(record.msg, str):
            message = record.msg
            for pattern in self.patterns:
                if pattern in message:
                    # Replace sensitive data with placeholders
                    record.msg = record.msg.replace(pattern + "=", pattern + "=[REDACTED]")
        return True


# Apply filter to logger
logger.addFilter(SensitiveDataFilter())
