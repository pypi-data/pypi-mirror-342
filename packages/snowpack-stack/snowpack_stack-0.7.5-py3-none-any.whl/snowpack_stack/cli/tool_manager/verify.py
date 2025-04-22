"""
Tool verification module for Snowpack Stack tool manager.

This module provides functionality to check if required tools are installed
and gather their version information.
"""

import logging
import re
import shutil
import subprocess
from typing import List, Optional, Tuple

from packaging.version import InvalidVersion
from packaging.version import parse as parse_version

# Setup logging
logger = logging.getLogger(__name__)


def is_command_available(command: str) -> bool:
    """
    Check if a command is available in the system PATH.

    Args:
        command (str): The command to check

    Returns:
        bool: True if the command is available, False otherwise
    """
    return shutil.which(command) is not None


def verify_dbt() -> Tuple[bool, Optional[str], List[str]]:
    """
    Verify if dbt is installed and get its version information.

    Returns:
        Tuple[bool, Optional[str], List[str]]:
            - is_installed: True if dbt is installed, False otherwise
            - version: The version of dbt if installed, None otherwise
            - adapters: List of installed adapters if available
    """
    try:
        # Run dbt --version to get version and adapter information
        dbt_path = shutil.which("dbt")
        if not dbt_path:
            logger.info("dbt command not found in PATH")
            return False, None, []

        result = subprocess.run(
            [dbt_path, "--version"], capture_output=True, text=True, check=False
        )  # nosec B603

        if result.returncode != 0:
            logger.error(f"Error running 'dbt --version': {result.stderr}")
            # If dbt --version fails, it might still be installed but misconfigured
            return True, None, []

        output = result.stdout
        logger.debug(f"dbt --version output string: {output}")
        # Add print(repr()) for detailed inspection
        print(f"DEBUG: repr(output) = {repr(output)}")

        # Parse version
        version_match = re.search(r"installed:\s*(\d+\.\d+\.\d+(\.\w+|-\w+)*)", output)
        version = version_match.group(1) if version_match else None

        # Parse adapters/plugins - Simplest possible regex
        adapters = []
        # Find patterns like '- adapter_name:'
        adapter_matches = re.findall(r"- (\w+):", output)
        # Filter out non-adapters
        adapters = [
            match for match in adapter_matches if match.lower() not in ["installed", "latest"]
        ]

        logger.info(f"Found dbt version {version} with adapters: {', '.join(adapters)}")
        return True, version, adapters

    except Exception as e:
        logger.error(f"Error verifying dbt: {e}")
        return True, None, []  # Assume installed if error occurs during check


def verify_bruin() -> Tuple[bool, Optional[str], List[str]]:
    """
    Verify if Bruin is installed and get its version information.

    Returns:
        Tuple[bool, Optional[str], List[str]]:
            - is_installed: True if Bruin is installed, False otherwise
            - version: The version of Bruin if installed, None otherwise
            - variants: Empty list (Bruin doesn't have variants like dbt adapters)
    """
    # Check if bruin command is available in PATH and get its absolute path
    bruin_path = shutil.which("bruin")
    if not bruin_path:
        logger.info("bruin command not found in PATH")
        return False, None, []

    try:
        # Run bruin --version using the absolute path to get version information
        result = subprocess.run(
            [bruin_path, "--version"], capture_output=True, text=True, check=False
        )  # nosec B603

        if result.returncode != 0:
            logger.error(f"Error running 'bruin --version': {result.stderr}")
            return True, None, []

        # Parse the output to extract version
        output = result.stdout

        # Extract version (adjust regex based on actual output format)
        version_match = re.search(r"(\d+\.\d+\.\d+)", output)
        version = version_match.group(1) if version_match else None

        logger.info(f"Found Bruin version {version}")
        return True, version, []

    except Exception as e:
        logger.error(f"Error verifying Bruin: {e}")
        return True, None, []


def verify_tool(tool_name: str) -> Tuple[bool, Optional[str], List[str]]:
    """
    Verify if a specific tool is installed and get its version information.

    Args:
        tool_name (str): The name of the tool to verify (dbt, bruin)

    Returns:
        Tuple[bool, Optional[str], List[str]]:
            - is_installed: True if the tool is installed, False otherwise
            - version: The version of the tool if installed, None otherwise
            - variants: List of variants/adapters if available
    """
    tool_name = tool_name.lower()

    if tool_name == "dbt":
        return verify_dbt()
    elif tool_name == "bruin":
        return verify_bruin()
    else:
        logger.error(f"Unsupported tool: {tool_name}")
        return False, None, []


def is_version_outdated(version: str, min_version: str) -> bool:
    """
    Check if a version is outdated compared to a minimum required version.

    Args:
        version (str): The version to check.
        min_version (str): The minimum version required.

    Returns:
        bool: True if the version is less than the minimum version, False otherwise.
              Returns False if either version string is invalid.
    """
    if not version:
        logger.warning("Provided version is empty, considering it outdated.")
        return True  # Treat empty/None version as outdated

    try:
        current_v = parse_version(version)
        minimum_v = parse_version(min_version)

        # Perform the comparison using packaging library
        is_outdated = current_v < minimum_v
        if is_outdated:
            logger.debug(f"Version '{version}' is outdated compared to minimum '{min_version}'.")
        else:
            logger.debug(f"Version '{version}' meets minimum requirement '{min_version}'.")
        return is_outdated

    except InvalidVersion as e:
        logger.error(f"Error comparing versions ('{version}' vs '{min_version}'): {e}")
        # If we can't parse the versions reliably, assume it's not outdated to avoid false positives
        return False
    except Exception as e:
        # Catch any other unexpected errors during parsing/comparison
        logger.error(f"Unexpected error comparing versions ('{version}' vs '{min_version}'): {e}")
        return False
