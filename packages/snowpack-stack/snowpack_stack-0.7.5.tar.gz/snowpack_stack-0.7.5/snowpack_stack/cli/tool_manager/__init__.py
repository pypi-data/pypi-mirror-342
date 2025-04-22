"""
Tool Manager module for Snowpack Stack.

This module provides functionality to add, verify, and remove data tools
like dbt and Bruin for use with Snowpack Stack.

Examples:
    # Add dbt to your project
    $ snowpack-stack add dbt

    # Add bruin to your project
    $ snowpack-stack add bruin

    # Remove a previously added tool
    $ snowpack-stack remove dbt

    # Force reinstallation of a tool
    $ snowpack-stack add dbt --force

    # Remove a tool without confirmation
    $ snowpack-stack remove bruin --force
"""

from snowpack_stack.cli.tool_manager.add_command import add_command
from snowpack_stack.cli.tool_manager.remove_command import remove_command


def register_commands(subparsers):
    """
    Register tool manager commands with the main CLI parser.

    Args:
        subparsers: The subparsers object from the main CLI parser
    """
    # Add command
    add_parser = subparsers.add_parser(
        "add", help="Add and verify a data tool for use with Snowpack Stack"
    )
    add_parser.add_argument("tool_name", help="The tool to add (dbt, bruin)")
    add_parser.add_argument(
        "--force",
        action="store_true",
        help="Force reinstallation even if the tool is already registered",
    )
    add_parser.set_defaults(func=add_command)

    # Remove command
    remove_parser = subparsers.add_parser(
        "remove", help="Remove a previously added data tool from Snowpack Stack tracking"
    )
    remove_parser.add_argument("tool_name", help="The tool to remove (dbt, bruin)")
    remove_parser.add_argument(
        "--force", action="store_true", help="Skip confirmation prompt before removing"
    )
    remove_parser.set_defaults(func=remove_command)
