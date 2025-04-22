"""Configuration management for Snowpack Stack."""

import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def get_project_root() -> Path:
    """Get the project root directory.

    Returns:
        Path: Project root directory
    """
    # Start from the current file's location
    current_file = Path(__file__).resolve()

    # Navigate up to find the project root (snowpack_stack_product)
    project_root = current_file.parent.parent.parent

    # Verify we're in the right place
    if not (project_root / "snowpack_stack").exists():
        raise ValueError(f"Could not find project root at {project_root}")

    return project_root


def find_config_file(filename: str) -> Optional[Path]:
    """Find a configuration file in various possible locations.

    Args:
        filename: Name of the configuration file to find

    Returns:
        Optional[Path]: Path to the config file if found, None otherwise
    """
    project_root = get_project_root()

    # Primary search locations
    search_paths = [
        project_root / "configs" / filename,  # configs/filename
        project_root / filename,  # ./filename
    ]

    for path in search_paths:
        if path.is_file():
            logger.info("Found configuration file: %s", path)
            return path

    logger.error(
        "Could not find %s in any of these locations: %s", filename, [str(p) for p in search_paths]
    )
    return None


def load_env_files() -> None:
    """Load environment variables from .env files."""
    project_root = get_project_root()
    current_dir = Path.cwd()

    # Determine if we're in a subdirectory of internal-bruin
    parent_dir = project_root.parent
    internal_bruin_dir = None

    # Try to identify the internal-bruin directory
    if (parent_dir / ".env").exists():
        internal_bruin_dir = parent_dir
        logger.info(f"Found parent directory with .env file: {parent_dir}")

    # More comprehensive search paths with parent directory prioritized
    search_paths = [
        # First check the parent directory if it looks like internal-bruin
        internal_bruin_dir / ".env" if internal_bruin_dir else None,
        # Then check standard locations
        project_root / ".env",  # Project root .env
        current_dir / ".env",  # Current directory .env
        project_root.parent / ".env",  # Parent directory .env
        project_root / "configs" / ".env",  # configs/.env
        Path.home() / ".env.snowpack",  # User home directory
    ]

    # Filter out None entries
    search_paths = [p for p in search_paths if p is not None]

    # Add debug information
    logger.info("Searching for .env files in: %s", [str(p) for p in search_paths])

    env_files_found = False
    for path in search_paths:
        if path.is_file():
            logger.info("Loading environment variables from: %s", path)
            try:
                # Load the .env file without any validation or modification
                load_dotenv(str(path), override=True)
                env_files_found = True
            except Exception as e:
                logger.error("Error loading .env file %s: %s", path, e)

    if not env_files_found:
        logger.warning(
            "No .env file found in search paths. Environment variables must be set directly in the environment."
        )
        logger.warning("Searched paths: %s", [str(p) for p in search_paths])


def replace_env_vars(value: Any) -> Any:
    """Recursively replace environment variables in configuration values.

    Args:
        value: Configuration value to process

    Returns:
        Any: Processed configuration value
    """
    if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
        env_var = value[2:-1]
        env_value = os.getenv(env_var)
        if env_value is None:
            logger.warning("Environment variable not found: %s", env_var)
            return f"Missing {env_var}"

        return env_value
    elif isinstance(value, dict):
        return {k: replace_env_vars(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [replace_env_vars(item) for item in value]
    return value


def load_config() -> Optional[Dict[str, Any]]:
    """Load and process configuration files.

    Returns:
        Optional[Dict[str, Any]]: Processed configuration dictionary
    """
    try:
        # First, load environment variables
        load_env_files()

        # Find configuration files
        config_file = find_config_file("autogen_config.yaml")
        if not config_file:
            return None

        # Load main configuration
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)

        # Process environment variables
        config = replace_env_vars(config)

        # Log processed sections
        for section in ["source", "destination"]:
            if section in config:
                logger.info("Processed %s configuration", section)

        return config
    except Exception as e:
        logger.error("Failed to load configuration: %s", e)
        return None


class ConfigLoader:
    """Configuration loader wrapper class.

    This class provides an object-oriented interface to the configuration loading functionality.
    """

    @staticmethod
    def load() -> Optional[Dict[str, Any]]:
        """Load configuration from files.

        Returns:
            Optional[Dict[str, Any]]: Loaded configuration dictionary
        """
        return load_config()
