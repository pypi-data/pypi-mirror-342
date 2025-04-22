# snowpack_stack/config_loader.py
import logging
import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def get_project_root():
    """Get the project root directory."""
    # Start from the current file's location
    current_file = Path(__file__).resolve()

    # Navigate up to find the project root (snowpack_stack_product)
    project_root = current_file.parent.parent.parent

    # Verify we're in the right place
    if not (project_root / "snowpack_stack").exists():
        raise ValueError(f"Could not find project root at {project_root}")

    return project_root


def find_config_file(filename):
    """Find a configuration file in various possible locations."""
    project_root = get_project_root()

    # Primary search locations
    search_paths = [
        project_root / filename,  # internal-bruin/filename
        Path.cwd() / filename,  # ./filename
        Path.cwd() / "configs" / filename,  # ./configs/filename
        project_root / "configs" / filename,  # internal-bruin/configs/filename
    ]

    for path in search_paths:
        if path.is_file():
            logger.info("Found configuration file: %s", path)
            return str(path)

    raise FileNotFoundError(
        f"Could not find {filename} in any of these locations: {[str(p) for p in search_paths]}"
    )


def load_env_files():
    """Load environment variables from .env files in various locations."""
    project_root = get_project_root()

    # Primary search locations
    search_paths = [
        project_root / ".env",  # internal-bruin/.env (primary location)
        Path.cwd() / ".env",  # ./.env (fallback)
    ]

    env_files_found = False
    for path in search_paths:
        if path.is_file():
            logger.info("Loading environment variables from: %s", path)
            load_dotenv(str(path), override=True)
            env_files_found = True

    if not env_files_found:
        logger.warning("No .env file found in search paths: %s", [str(p) for p in search_paths])


def replace_env_vars(value):
    """Recursively replace environment variables in strings."""
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


def load_config(config_file):
    """Load the configuration file and replace environment variables."""
    # First, load environment variables
    load_env_files()

    try:
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)
    except Exception as e:
        logger.error("Failed to load configuration file: %s", e)
        raise

    # Process the configuration
    try:
        processed_config = replace_env_vars(config)

        # Log which environment variables were replaced
        for section in ["source", "destination"]:
            if section in processed_config:
                logger.info("Processed %s configuration", section)

        return processed_config
    except Exception as e:
        logger.error("Error processing configuration: %s", e)
        raise
