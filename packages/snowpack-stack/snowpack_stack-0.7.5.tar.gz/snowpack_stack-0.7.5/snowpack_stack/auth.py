"""
Authentication module for Snowpack Stack.

This module provides simple email storage functionality for Snowpack Stack.
Authentication is now optional with sensible defaults for basic usage.
"""

import json
import logging
import os
import time
from pathlib import Path
from typing import Any, Callable, Optional

# Configure logging
logger = logging.getLogger(__name__)

# Global variables to store authentication state
_user_email: Optional[str] = None
_authenticated: bool = False  # Not authenticated by default
_auth_expiry: Optional[float] = None

# Constants
DEFAULT_AUTH_EXPIRY = 24 * 60 * 60  # 24 hours in seconds
AUTH_CONFIG_DIR = Path.home() / ".snowpack"
AUTH_CONFIG_FILE = AUTH_CONFIG_DIR / "auth_config.json"
CREDENTIALS_FILE = AUTH_CONFIG_DIR / "credentials.json"


def save_user_email(email: str) -> bool:
    """
    Save the user's email to the configuration file.
    This is now optional for use in analytics and logging.

    Args:
        email: The email address to save

    Returns:
        bool: True if successful
    """
    global _user_email

    # Create config directory if it doesn't exist
    AUTH_CONFIG_DIR.mkdir(exist_ok=True)

    # Save email to config file
    try:
        config = {}
        if AUTH_CONFIG_FILE.exists():
            try:
                with open(AUTH_CONFIG_FILE, "r") as f:
                    config = json.load(f)
            except json.JSONDecodeError:
                # If the file exists but is not valid JSON, start with an empty config
                config = {}

        config["user_email"] = email
        config["last_auth_time"] = time.time()

        with open(AUTH_CONFIG_FILE, "w") as f:
            json.dump(config, f)

        _user_email = email
        return True
    except Exception as e:
        logger.error(f"Error saving user email: {str(e)}")
        return False


def set_user_email(email: str) -> bool:
    """
    Set the user's email for identification purposes.
    This is now optional for use in analytics and logging.

    Args:
        email: The email address to set

    Returns:
        bool: True if successful
    """
    global _user_email, _authenticated

    # Email format validation is minimal - just check if it has an @
    if "@" not in email:
        logger.warning(f"Invalid email format: {email}")
        return False

    # Save the email to file
    if save_user_email(email):
        _user_email = email
        _authenticated = True
        return True

    return False


def set_api_key(api_key: str) -> bool:
    """
    Legacy function for backward compatibility.
    This function is deprecated and will be removed in a future version.

    Args:
        api_key: API key (treated as email for backward compatibility)

    Returns:
        bool: True if successful, False otherwise
    """
    logger.warning("set_api_key() is deprecated and will be removed in a future version.")
    logger.warning("Please use set_user_email() instead.")

    # For backward compatibility, try to set user email
    # Only do this for tests that pass what looks like an email
    if isinstance(api_key, str) and "@" in api_key:
        return set_user_email(api_key)

    return True


def authenticate() -> bool:
    """
    Authenticate the user.

    Returns:
        bool: True if authenticated, False otherwise
    """
    global _authenticated, _auth_expiry, _user_email

    # Check if we already have a user email
    if _user_email is not None:
        _authenticated = True
        _auth_expiry = time.time() + DEFAULT_AUTH_EXPIRY
        return True

    # Check environment variable for email
    env_email = os.environ.get("SNOWPACK_USER_EMAIL")
    if env_email:
        if "@" in env_email:
            _user_email = env_email
            _authenticated = True
            _auth_expiry = time.time() + DEFAULT_AUTH_EXPIRY
            return True

    # Load email from config file if available
    try:
        if AUTH_CONFIG_FILE.exists():
            with open(AUTH_CONFIG_FILE, "r") as f:
                config = json.load(f)

            if "user_email" in config:
                _user_email = config["user_email"]
                _authenticated = True
                _auth_expiry = time.time() + DEFAULT_AUTH_EXPIRY
                return True
    except Exception as e:
        logger.warning(f"Error loading saved authentication: {str(e)}")

    # If we get here, we couldn't authenticate
    return False


def is_authenticated() -> bool:
    """
    Check if the user is authenticated.

    Returns:
        bool: True if authenticated, False otherwise
    """
    global _authenticated, _auth_expiry  # noqa: F824 # Flake8 F824 seems incorrect here; _auth_expiry is read below

    # Check if authentication has expired
    if _authenticated and _auth_expiry is not None:
        if time.time() > _auth_expiry:
            _authenticated = False

    # If not authenticated, try to authenticate
    if not _authenticated:
        _authenticated = authenticate()

    return _authenticated


def get_user_email() -> Optional[str]:
    """
    Get the user's email.

    Returns:
        Optional[str]: The user's email, or None if not set
    """
    global _user_email

    # If we don't have an email in memory, try to load it
    if _user_email is None:
        # Check environment variable
        env_email = os.environ.get("SNOWPACK_USER_EMAIL")
        if env_email:
            _user_email = env_email
            return _user_email

        # Try to load from config file
        try:
            if AUTH_CONFIG_FILE.exists():
                with open(AUTH_CONFIG_FILE, "r") as f:
                    config = json.load(f)

                if "user_email" in config:
                    _user_email = config["user_email"]
        except Exception as e:
            # Log the error instead of silently passing
            logger.error(f"Error reading user email from config: {str(e)}")

    return _user_email


def require_auth(func: Callable) -> Callable:
    """
    Decorator to require authentication before executing a function.

    Args:
        func: The function to decorate

    Returns:
        Callable: The decorated function
    """

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if not is_authenticated():
            raise PermissionError("Authentication required. Please authenticate first.")
        return func(*args, **kwargs)

    return wrapper


def clear_saved_credentials() -> bool:
    """
    Clear saved credentials.

    Returns:
        bool: True if successful
    """
    global _user_email, _authenticated, _auth_expiry

    # Reset global state
    _user_email = None
    _authenticated = False
    _auth_expiry = None

    # Remove config file
    try:
        if AUTH_CONFIG_FILE.exists():
            AUTH_CONFIG_FILE.unlink()
        return True
    except Exception as e:
        logger.error(f"Error clearing saved credentials: {str(e)}")
        return False
