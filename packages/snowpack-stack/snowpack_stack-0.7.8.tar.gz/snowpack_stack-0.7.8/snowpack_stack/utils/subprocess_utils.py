"""
Secure subprocess utilities for Snowpack Stack.

This module provides secure ways to execute subprocess commands with enhanced
security features to prevent command injection and other subprocess-related
vulnerabilities.
"""

import logging
import re
import shutil
import subprocess  # nosec B404 - This is a centralized subprocess utility module with security controls
from pathlib import Path
from typing import Dict, List, Optional

# Configure logging
logger = logging.getLogger(__name__)

# Regular expression for validating command arguments
# Rejects characters commonly used in command injection
SAFE_ARGUMENT_PATTERN = re.compile(r"^[a-zA-Z0-9\s_.+/:=@\-,]*$")

# List of allowed executables that can be used with subprocess
# This is a safety measure to prevent executing arbitrary commands
ALLOWED_EXECUTABLES = {"git", "poetry", "pip", "python", "python3", "gcloud", "gsutil"}


def validate_command_argument(arg: str) -> bool:
    """
    Validate a command argument to prevent command injection.

    Args:
        arg: The command argument to validate

    Returns:
        bool: True if the argument is safe, False otherwise
    """
    if not isinstance(arg, str):
        return False

    # Check if the argument contains unsafe characters
    return bool(SAFE_ARGUMENT_PATTERN.match(arg))


def validate_command(cmd: List[str]) -> bool:
    """
    Validate an entire command to ensure it's safe to execute.

    Args:
        cmd: List of command arguments

    Returns:
        bool: True if the command is safe, False otherwise
    """
    if not cmd or not isinstance(cmd, list):
        return False

    # Get the executable name (first part of the command)
    executable = Path(cmd[0]).name

    # If it's a full path, extract just the filename
    if "/" in executable or "\\" in executable:
        executable = Path(executable).name

    # Check if the executable is in the allowed list
    if executable not in ALLOWED_EXECUTABLES:
        logger.warning(f"Executable not in allowed list: {executable}")
        return False

    # Validate each argument
    for arg in cmd[1:]:
        if not validate_command_argument(str(arg)):
            logger.warning(f"Invalid command argument: {arg}")
            return False

    return True


def get_executable_path(executable: str) -> Optional[str]:
    """
    Get the full path to an executable using shutil.which().

    Args:
        executable: Name of the executable to find

    Returns:
        Optional[str]: Full path to the executable or None if not found
    """
    # Get the full path to the executable
    executable_path = shutil.which(executable)
    if not executable_path:
        logger.error(f"Executable not found: {executable}")
        return None

    return executable_path


def run_command(
    cmd: List[str],
    check: bool = True,
    capture_output: bool = True,
    text: bool = True,
    env: Optional[Dict[str, str]] = None,
    cwd: Optional[str] = None,
) -> subprocess.CompletedProcess:
    """
    Run a command securely with enhanced validation and security features.

    Args:
        cmd: Command to run as a list of arguments
        check: Whether to check the return code
        capture_output: Whether to capture stdout/stderr
        text: Whether to return stdout/stderr as strings
        env: Environment variables to set
        cwd: Working directory for the command

    Returns:
        subprocess.CompletedProcess: Result of the command

    Raises:
        ValueError: If the command is invalid
        subprocess.CalledProcessError: If the command fails and check=True
    """
    if not cmd:
        raise ValueError("Empty command")

    # Make a copy of the command to avoid modifying the original
    cmd_copy = list(cmd)

    # Sanitize executable with full path
    if not Path(cmd_copy[0]).is_absolute():
        executable_path = get_executable_path(cmd_copy[0])
        if not executable_path:
            raise ValueError(f"Executable not found: {cmd_copy[0]}")
        cmd_copy[0] = executable_path

    # Validate the command
    if not validate_command(cmd_copy):
        raise ValueError(f"Invalid command: {cmd_copy}")

    try:
        # Run the command
        logger.debug(f"Running command: {' '.join(cmd_copy)}")
        return subprocess.run(  # nosec B603 - Input is validated and shell=False is enforced
            cmd_copy,
            check=check,
            capture_output=capture_output,
            text=text,
            env=env,
            cwd=cwd,
            shell=False,  # Never use shell=True for security
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed with code {e.returncode}: {' '.join(cmd_copy)}")
        logger.error(f"STDOUT: {e.stdout}")
        logger.error(f"STDERR: {e.stderr}")
        raise
    except Exception as e:
        logger.error(f"Error running command: {e}")
        raise


def run_python_module(
    module: str,
    args: List[str] = None,
    check: bool = True,
    capture_output: bool = True,
    text: bool = True,
    env: Optional[Dict[str, str]] = None,
    cwd: Optional[str] = None,
) -> subprocess.CompletedProcess:
    """
    Run a Python module securely.

    Args:
        module: Python module to run
        args: Arguments to pass to the module
        check: Whether to check the return code
        capture_output: Whether to capture stdout/stderr
        text: Whether to return stdout/stderr as strings
        env: Environment variables to set
        cwd: Working directory for the command

    Returns:
        subprocess.CompletedProcess: Result of the command
    """
    if args is None:
        args = []

    # Get the Python executable path
    python_path = sys.executable

    # Construct the command
    cmd = [python_path, "-m", module] + args

    # Run the command
    return run_command(
        cmd=cmd, check=check, capture_output=capture_output, text=text, env=env, cwd=cwd
    )


def run_git_command(
    args: List[str],
    check: bool = True,
    capture_output: bool = True,
    text: bool = True,
    cwd: Optional[str] = None,
) -> subprocess.CompletedProcess:
    """
    Run a git command securely.

    Args:
        args: Git command arguments
        check: Whether to check the return code
        capture_output: Whether to capture stdout/stderr
        text: Whether to return stdout/stderr as strings
        cwd: Working directory for the command

    Returns:
        subprocess.CompletedProcess: Result of the command
    """
    # Get the git executable path
    git_path = get_executable_path("git")
    if not git_path:
        raise ValueError("Git executable not found")

    # Construct the command
    cmd = [git_path] + args

    # Run the command
    return run_command(cmd=cmd, check=check, capture_output=capture_output, text=text, cwd=cwd)


def run_poetry_command(
    args: List[str],
    check: bool = True,
    capture_output: bool = True,
    text: bool = True,
    cwd: Optional[str] = None,
) -> subprocess.CompletedProcess:
    """
    Run a poetry command securely.

    Args:
        args: Poetry command arguments
        check: Whether to check the return code
        capture_output: Whether to capture stdout/stderr
        text: Whether to return stdout/stderr as strings
        cwd: Working directory for the command

    Returns:
        subprocess.CompletedProcess: Result of the command
    """
    # Get the poetry executable path
    poetry_path = get_executable_path("poetry")
    if not poetry_path:
        raise ValueError("Poetry executable not found")

    # Construct the command
    cmd = [poetry_path] + args

    # Run the command
    return run_command(cmd=cmd, check=check, capture_output=capture_output, text=text, cwd=cwd)


def run_gcloud_command(
    args: List[str],
    check: bool = True,
    capture_output: bool = True,
    text: bool = True,
    cwd: Optional[str] = None,
) -> subprocess.CompletedProcess:
    """
    Run a gcloud command securely.

    Args:
        args: Gcloud command arguments
        check: Whether to check the return code
        capture_output: Whether to capture stdout/stderr
        text: Whether to return stdout/stderr as strings
        cwd: Working directory for the command

    Returns:
        subprocess.CompletedProcess: Result of the command
    """
    # Get the gcloud executable path
    gcloud_path = get_executable_path("gcloud")
    if not gcloud_path:
        raise ValueError("Gcloud executable not found")

    # Construct the command
    cmd = [gcloud_path] + args

    # Run the command
    return run_command(cmd=cmd, check=check, capture_output=capture_output, text=text, cwd=cwd)


# Add Python's sys module for getting the current Python executable
import sys
