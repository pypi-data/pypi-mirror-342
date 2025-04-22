"""
Metadata management module for Snowpack Stack tool manager.

This module provides functionality to track installed tools, their versions,
and initialization status.
"""

import datetime
import json
import logging
import os
import tempfile
from pathlib import Path

# Assuming this import exists in the project
from snowpack_stack.core.config import get_project_root

# Setup logging
logger = logging.getLogger(__name__)

# Constants
METADATA_FILENAME = ".snowpack-tools.json"


def get_metadata_path():
    """
    Get the path to the metadata file in the project root.

    Returns:
        Path: The path to the metadata file
    """
    try:
        project_root = get_project_root()
        return project_root / METADATA_FILENAME
    except Exception as e:
        logger.error(f"Error getting project root: {e}")
        # Fallback to current directory if project root can't be determined
        return Path(os.getcwd()) / METADATA_FILENAME


def load_metadata():
    """
    Load the metadata file if it exists, or return a default structure.

    Returns:
        dict: The metadata dictionary
    """
    metadata_path = get_metadata_path()

    # Default metadata structure
    default_metadata = {
        "schema_version": 1,
        "last_updated": datetime.datetime.now().isoformat(),
        "tools": {},
    }

    if not metadata_path.exists():
        logger.info(f"Metadata file not found at {metadata_path}. Creating new metadata.")
        return default_metadata

    try:
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
            logger.debug(f"Loaded metadata from {metadata_path}")
            return metadata
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing metadata file: {e}")
        logger.info("Creating new metadata file with default structure")
        return default_metadata
    except Exception as e:
        logger.error(f"Error loading metadata file: {e}")
        return default_metadata


def save_metadata(metadata):
    """
    Save the metadata dictionary to the metadata file.

    Args:
        metadata (dict): The metadata dictionary to save

    Returns:
        bool: True if the metadata was successfully saved, False otherwise
    """
    metadata_path = get_metadata_path()
    logger.debug(f"Attempting to save metadata to: {metadata_path}")

    # Update the last_updated timestamp
    metadata["last_updated"] = datetime.datetime.now().isoformat()

    try:
        # Use atomic write to prevent corruption
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            json.dump(metadata, temp_file, indent=2)

        # Replace the original file with the temporary file
        os.replace(temp_file.name, metadata_path)
        logger.debug(f"Saved metadata to {metadata_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving metadata file: {e}")
        # Try to clean up the temporary file if it exists
        try:
            if os.path.exists(temp_file.name):
                os.remove(temp_file.name)
        except OSError as remove_error:
            logger.warning(
                f"Failed to remove temporary metadata file {temp_file.name} after save error: {remove_error}"
            )
        return False


def is_tool_registered(tool_name):
    """
    Check if a specific tool is already registered in the metadata.

    Args:
        tool_name (str): The name of the tool to check

    Returns:
        bool: True if the tool is registered, False otherwise
    """
    metadata = load_metadata()
    return tool_name in metadata.get("tools", {})


def register_tool(tool_name, version, variant=None, initialized=False, project_path=None):
    """
    Add or update a tool entry in the metadata.

    Args:
        tool_name (str): The name of the tool to register
        version (str): The version of the tool
        variant (str, optional): The variant of the tool (e.g., dbt-bigquery)
        initialized (bool, optional): Whether the tool has been initialized
        project_path (str, optional): The path to the tool's project

    Returns:
        bool: True if the tool was successfully registered, False otherwise
    """
    metadata = load_metadata()
    logger.debug(f"Registering tool '{tool_name}'. Current metadata: {metadata}")

    # Create the tool entry
    tool_entry = {
        "added_on": datetime.datetime.now().isoformat(),
        "version": version,
        "initialized": initialized,
    }

    # Add optional fields if provided
    if variant:
        tool_entry["variant"] = variant

    if project_path:
        tool_entry["project_path"] = project_path

    # Add or update the tool in the metadata
    metadata.setdefault("tools", {})[tool_name] = tool_entry
    logger.debug(f"Updated metadata structure: {metadata}")

    # Save the updated metadata
    success = save_metadata(metadata)
    if success:
        logger.info(f"Registered tool: {tool_name} (version: {version})")
    else:
        # Add log if saving failed
        logger.error(f"Failed to save metadata after attempting to register tool: {tool_name}")

    return success


def unregister_tool(tool_name):
    """
    Remove a tool entry from the metadata.

    Args:
        tool_name (str): The name of the tool to unregister

    Returns:
        bool: True if the tool was successfully unregistered, False if the tool wasn't registered
    """
    metadata = load_metadata()

    # Check if the tool is registered
    if tool_name not in metadata.get("tools", {}):
        logger.warning(f"Tool not registered: {tool_name}")
        return False

    # Remove the tool from the metadata
    del metadata["tools"][tool_name]

    # Save the updated metadata
    success = save_metadata(metadata)
    if success:
        logger.info(f"Unregistered tool: {tool_name}")

    return success
