"""
Implementation of the 'remove' command for Snowpack Stack tool manager.

This module provides functionality to remove previously added tools from tracking.
"""

import argparse
import logging
import sys

# Import tool manager modules
from snowpack_stack.cli.tool_manager.metadata import (
    is_tool_registered,
    load_metadata,
    unregister_tool,
)
from snowpack_stack.cli.tool_manager.utils import (
    handle_command_exception,
    print_error,
    print_header,
    print_success,
)

# Setup logging
logger = logging.getLogger(__name__)


def remove_tool(tool_name, force=False):
    """
    Remove a previously added tool from Snowpack Stack tracking.

    This function:
    1. Checks if the tool is registered
    2. Confirms with the user before proceeding (unless force=True)
    3. Unregisters the tool from the metadata file
    4. Provides guidance on manual cleanup

    Args:
        tool_name (str): The name of the tool to remove (dbt, bruin)
        force (bool): Whether to skip confirmation before removing

    Returns:
        bool: True if the tool was successfully removed, False otherwise
    """
    tool_name = tool_name.lower()
    logger.info(f"Removing tool: {tool_name}")

    # Check if the tool is registered
    if not is_tool_registered(tool_name):
        print_error(f"{tool_name} is not registered with Snowpack Stack.")
        return False

    # Get tool details for reference
    metadata = load_metadata()
    tool_data = metadata.get("tools", {}).get(tool_name, {})
    project_path = tool_data.get("project_path")
    initialized = tool_data.get("initialized", False)

    # Confirm with the user before proceeding
    if not force:
        print_header(f"Remove {tool_name} from Snowpack Stack")
        print(f"This will remove {tool_name} from Snowpack Stack tracking.")
        print("Note: This will NOT uninstall the tool or delete any project files.")

        if initialized and project_path:
            print(f"\nThe {tool_name} project at '{project_path}' will remain on your system.")

        confirm = input("\nContinue with removal? (y/n): ").strip().lower()
        if confirm not in ["y", "yes"]:
            print("\nOperation cancelled.")
            return False

    # Unregister the tool from metadata
    success = unregister_tool(tool_name)

    if success:
        print_success(f"{tool_name} has been successfully removed from Snowpack Stack tracking.")

        # Provide guidance on manual cleanup
        if initialized and project_path:
            print("\n=== Manual Cleanup ===\n")
            print(
                f"If you want to completely remove the {tool_name} project, you can delete its directory:"
            )
            print(f"  rm -rf {project_path}")

            if tool_name == "dbt":
                print("\nYou may also want to remove any profiles created for this project:")
                print("  ~/.dbt/profiles.yml")
            elif tool_name == "bruin":
                print("\nYou may also want to check for any Bruin configuration files:")
                print("  ~/.bruin/")

        logger.info(f"Successfully removed {tool_name}")
        return True
    else:
        print_error(f"Failed to remove {tool_name} from metadata.")
        return False


def remove_command(args):
    """
    Handler for the 'remove' command when called from the main CLI.

    Args:
        args (Namespace): The parsed command-line arguments

    Returns:
        int: Exit code (0 for success, non-zero for errors)
    """
    try:
        success = remove_tool(args.tool_name, args.force)
        return 0 if success else 1
    except Exception as e:
        return handle_command_exception(e, "remove")


def main():
    """
    Main entry point for the 'remove' command when called directly.

    Parses command line arguments and calls the remove_tool function.
    """
    parser = argparse.ArgumentParser(
        description="Remove a previously added data tool from Snowpack Stack tracking"
    )
    parser.add_argument("tool_name", help="The tool to remove (dbt, bruin)")
    parser.add_argument(
        "--force", action="store_true", help="Skip confirmation prompt before removing"
    )

    args = parser.parse_args()

    try:
        success = remove_tool(args.tool_name, args.force)
        sys.exit(0 if success else 1)
    except Exception as e:
        exit_code = handle_command_exception(e, "remove")
        sys.exit(exit_code)


if __name__ == "__main__":
    main()
