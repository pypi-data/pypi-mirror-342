"""
Implementation of the 'add' command for Snowpack Stack tool manager.

This module provides functionality to add and verify data tools like dbt and Bruin.
"""

import argparse
import logging
import sys

from snowpack_stack.cli.tool_manager.initialize import (
    initialize_tool_project,
    should_initialize_project,
)
from snowpack_stack.cli.tool_manager.install import (
    provide_installation_guidance,
    retry_installation,
)
from snowpack_stack.cli.tool_manager.metadata import is_tool_registered, register_tool
from snowpack_stack.cli.tool_manager.utils import (
    handle_command_exception,
    print_error,
    print_header,
    print_success,
    print_warning,
)

# Import tool manager modules
from snowpack_stack.cli.tool_manager.verify import is_version_outdated, verify_tool

# Setup logging
logger = logging.getLogger(__name__)

# Minimum recommended versions
RECOMMENDED_VERSIONS = {"dbt": "1.8.0", "bruin": "0.11.0"}


def add_tool(tool_name, force=False):
    """
    Add and verify a data tool for use with Snowpack Stack.

    This function guides the user through the process of adding a tool to Snowpack Stack:
    1. Verifies if the tool is installed
    2. Provides installation guidance if needed
    3. Checks for outdated versions
    4. Helps with project initialization or registration
    5. Registers the tool in the metadata file

    Args:
        tool_name (str): The name of the tool to add (dbt, bruin)
        force (bool): Whether to force reinstallation if the tool is already registered

    Returns:
        bool: True if the tool was successfully added, False otherwise
    """
    tool_name = tool_name.lower()
    logger.info(f"Adding tool: {tool_name}")

    # Check if the tool is supported
    if tool_name not in ["dbt", "bruin"]:
        print_error(f"Unsupported tool: {tool_name}")
        print("Currently supported tools: dbt, bruin")
        return False

    # Check if the tool is already registered
    if is_tool_registered(tool_name) and not force:
        print_warning(f"{tool_name} is already registered with Snowpack Stack.")
        print("Use --force to reinstall or reconfigure.")
        return False
    elif is_tool_registered(tool_name) and force:
        print_warning(f"Forcing reinstallation of {tool_name}.")

    # Step 1: Verify if the tool is installed
    print_header(f"Verifying {tool_name} Installation")
    is_installed, version, variants = verify_tool(tool_name)

    # Step 2: If not installed, provide installation guidance
    if not is_installed:
        print_error(f"{tool_name} is not installed or not found in your PATH.")
        provide_installation_guidance(tool_name)

        # Retry installation with verification
        is_installed, version, variants = retry_installation(tool_name)

        if not is_installed:
            print_error(f"Failed to verify {tool_name} installation.")
            return False

    # Step 3: Check for outdated versions
    if version and tool_name in RECOMMENDED_VERSIONS:
        if is_version_outdated(version, RECOMMENDED_VERSIONS[tool_name]):
            print_warning(
                f"Your {tool_name} version ({version}) is older than the recommended version ({RECOMMENDED_VERSIONS[tool_name]})."
            )
            print("Consider upgrading for the best experience.")

    # Step 4: Project setup (initialize new or use existing)
    project_path = None
    initialized = False

    if tool_name in ["dbt", "bruin"]:
        setup_action, existing_path = should_initialize_project(tool_name)
        print(
            f"DEBUG: add_tool received setup_action='{setup_action}', existing_path='{existing_path}'"
        )

        if setup_action == "new":
            success, project_path = initialize_tool_project(tool_name)
            initialized = success

            if not success:
                print_warning(f"Failed to initialize {tool_name} project. You can try again later.")
        elif setup_action == "existing":
            project_path = existing_path
            initialized = True
            print(f"DEBUG: add_tool set project_path='{project_path}'")
        else:
            print(f"\nSkipping {tool_name} project setup.")

    # Step 5: Register the tool in metadata
    variant = variants[0] if variants else None
    success = register_tool(
        tool_name=tool_name,
        version=version,
        variant=variant,
        initialized=initialized,
        project_path=project_path,
    )

    if success:
        print_success(f"{tool_name} has been successfully added to Snowpack Stack!")

        # Print next steps
        print("\n=== Next Steps ===\n")
        if initialized and project_path:
            print(f"Your {tool_name} project is ready at: {project_path}")
            print(f"You can start working with {tool_name} right away.")
        else:
            print(f"To initialize a {tool_name} project later, run:")
            print(f"  cd /path/to/your/project")
            print(f"  {tool_name} init [project_name]")

        logger.info(f"Successfully added {tool_name}")
        return True
    else:
        print_error(f"Failed to register {tool_name} in metadata.")
        return False


def add_command(args):
    """
    Handler for the 'add' command when called from the main CLI.

    Args:
        args (Namespace): The parsed command-line arguments

    Returns:
        int: Exit code (0 for success, non-zero for errors)
    """
    try:
        success = add_tool(args.tool_name, args.force)
        return 0 if success else 1
    except Exception as e:
        return handle_command_exception(e, "add")


def main():
    """
    Main entry point for the 'add' command when called directly.

    Parses command line arguments and calls the add_tool function.
    """
    parser = argparse.ArgumentParser(
        description="Add and verify a data tool for use with Snowpack Stack"
    )
    parser.add_argument("tool_name", help="The tool to add (dbt, bruin)")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force reinstallation even if the tool is already registered",
    )

    args = parser.parse_args()

    try:
        success = add_tool(args.tool_name, args.force)
        sys.exit(0 if success else 1)
    except Exception as e:
        exit_code = handle_command_exception(e, "add")
        sys.exit(exit_code)


if __name__ == "__main__":
    main()
