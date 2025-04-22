"""Main CLI entry point for Snowpack Stack.

This module provides the main CLI entry point for Snowpack Stack,
with subcommands for building assets, setting up the environment,
and managing releases.
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import List, Optional

from snowpack_stack import __version__

# from snowpack_stack.cli.verify import main as verify_main # This seems redundant with setup verify
from snowpack_stack.cli.tool_manager import register_commands as register_tool_commands

# Import subcommand registration and runner functions
# REMOVED: from snowpack_stack.cli.build import main as build_main
# REMOVED: from snowpack_stack.cli.release import main as release_main
# REMOVED: from snowpack_stack.cli.setup import main as setup_main


# Note: Direct imports for specific command mains are removed as we use run_* functions


# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Placeholder for access control if needed from HEAD merge (assuming it exists elsewhere now)
# from snowpack_stack.core.security import check_command_access, AccessDeniedError, KeyMissingError, AccessLevel, COMMANDS


def run_build_command(args: argparse.Namespace) -> int:
    """Run the build command.

    Args:
        args: Command line arguments

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    from snowpack_stack.cli import build

    # Convert argparse.Namespace to list of arguments for build.main
    build_args = []

    if hasattr(args, "build_command") and args.build_command:
        build_args.append(args.build_command)

        if args.build_command == "bruin" and hasattr(args, "asset_type") and args.asset_type:
            build_args.append(args.asset_type)

    return build.main(build_args)


def run_setup_command(args: argparse.Namespace) -> int:
    """Run the setup command.

    Args:
        args: Command line arguments

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    # Check for the specific subcommands based on dest='setup_type'
    if hasattr(args, "setup_type") and args.setup_type:
        if args.setup_type == "auth":
            from snowpack_stack.cli.setup.auth import main as auth_main

            return auth_main(args)
        elif args.setup_type == "verify":
            from snowpack_stack.cli.setup.verify import main as verify_main

            return verify_main()
        elif args.setup_type == "verify-internal":
            from snowpack_stack.cli.setup.verify_internal import main as verify_internal_main

            return verify_internal_main()
        elif args.setup_type == "rotate-key":
            # Placeholder: Need to integrate access control check if applicable
            # try:
            #     check_command_access("setup", "rotate-key")
            from snowpack_stack.cli.setup.rotate_key import main as rotate_key_main

            return rotate_key_main()
            # except AccessDeniedError as e:
            #     print(f"Error: {e}")
            #     return 1
            # except KeyMissingError as e:
            #     print(f"Error: {e}")
            #     return 1
        else:
            # Should not happen if command is valid
            logger.error(f"Unknown setup type: {args.setup_type}")
            return 1  # Or print help?
    else:
        # Default behavior if no specific setup subcommand is given (e.g., 'snowpack setup')
        # Run both auth and verify (original default logic)
        from snowpack_stack.cli.setup.auth import main as auth_main
        from snowpack_stack.cli.setup.verify import main as verify_main

        auth_result = auth_main(args)  # Pass args for potential --email
        if auth_result != 0:
            return auth_result
        return verify_main()


def run_release_command(args: argparse.Namespace) -> int:
    """Run the release command.

    Args:
        args: Command line arguments

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    # Combine logic - use origin/main structure but potentially add access checks from HEAD
    # Placeholder: Need to integrate access control check if applicable
    # try:
    #     check_command_access("release")
    if hasattr(args, "release_command") and args.release_command:
        if args.release_command == "create":
            from snowpack_stack.cli.release.create import main as create_main

            return create_main(args)
        elif args.release_command == "check":
            from snowpack_stack.cli.release.check import main as check_main

            return check_main()
        elif args.release_command == "reset":
            from snowpack_stack.cli.release.reset import main as reset_main

            return reset_main(args)
        elif args.release_command == "changelog":
            from snowpack_stack.cli.release.changelog import main as changelog_main

            return changelog_main(args)
    else:
        # Show help for release command (using the parser creation function)
        parser = create_release_parser()  # Need to ensure this function is available
        parser.print_help()
        return 0
    # except AccessDeniedError as e:
    #     print(f"Error: {e}")
    #     # Potentially show available commands based on access level
    #     return 1
    # except KeyMissingError as e:
    #     print(f"Error: {e}")
    #     return 1


def create_build_parser(subparsers):
    """Create the parser for the build command.

    Args:
        subparsers: Subparsers object from the main parser

    Returns:
        argparse.ArgumentParser: The build command parser
    """
    build_parser = subparsers.add_parser("build", help="Build assets")
    build_subparsers = build_parser.add_subparsers(dest="build_command")

    # All subcommand (default behavior)
    all_parser = build_subparsers.add_parser("all", help="Build all assets")

    # Bruin subcommand
    bruin_parser = build_subparsers.add_parser("bruin", help="Build Bruin assets")
    bruin_subparsers = bruin_parser.add_subparsers(dest="asset_type")

    yaml_parser = bruin_subparsers.add_parser("yaml", help="Build Bruin YAML assets")
    sql_parser = bruin_subparsers.add_parser("sql", help="Build Bruin SQL assets")

    # Set default function for build command
    build_parser.set_defaults(func=run_build_command)

    return build_parser


def create_setup_parser(subparsers):
    """Create the parser for the setup command.

    Args:
        subparsers: Subparsers object from the main parser

    Returns:
        argparse.ArgumentParser: The setup command parser
    """
    setup_parser = subparsers.add_parser("setup", help="Setup commands")
    setup_subparsers = setup_parser.add_subparsers(dest="setup_type")

    # Auth subcommand
    auth_parser = setup_subparsers.add_parser("auth", help="Authentication setup")
    auth_parser.add_argument("--email", help="Email address for authentication")

    # Verify subcommand
    verify_parser = setup_subparsers.add_parser("verify", help="Verify installation")

    # Add commands from HEAD if they exist
    # Verify internal command
    verify_internal_parser = setup_subparsers.add_parser(
        "verify-internal", help="Verify internal developer access"
    )

    # Rotate key command
    rotate_key_parser = setup_subparsers.add_parser(
        "rotate-key", help="Generate a new API key (internal access only)"
    )

    # Set default function for setup command
    setup_parser.set_defaults(func=run_setup_command)

    return setup_parser


def create_release_parser(subparsers=None):
    """Create the parser for the release command.

    Args:
        subparsers: Optional subparsers object. If None, create standalone parser.

    Returns:
        argparse.ArgumentParser: The release command parser
    """
    if subparsers:
        release_parser = subparsers.add_parser(
            "release", help="Release management commands (internal access only)"
        )
    else:
        # Standalone parser for showing help in run_release_command
        release_parser = argparse.ArgumentParser(
            prog="snowpack release",
            description="Release management commands (internal access only)",
        )

    release_subparsers = release_parser.add_subparsers(dest="release_command")

    # Create subcommand
    create_parser = release_subparsers.add_parser("create", help="Create a new release")
    create_parser.add_argument(
        "version_bump",
        nargs="?",
        choices=["major", "minor", "patch"],
        help="Version component to bump",
    )
    create_parser.add_argument(
        "--set", dest="specific_version", help="Set a specific version instead of bumping"
    )
    create_parser.add_argument(
        "--no-push", action="store_true", help="Don't push changes to remote"
    )
    # Add pre-release flag from HEAD if needed
    create_parser.add_argument(
        "--pre-release", action="store_true", help="Create a pre-release version"
    )

    # Check subcommand
    check_parser = release_subparsers.add_parser(
        "check", help="Check release status/version consistency"
    )

    # Reset subcommand
    reset_parser = release_subparsers.add_parser(
        "reset", help="Reset a release version (use with caution)"
    )
    reset_parser.add_argument("version", help="Version to reset (e.g., '0.4.1')")

    # Changelog subcommand
    changelog_parser = release_subparsers.add_parser("changelog", help="Generate a changelog")
    changelog_parser.add_argument(
        "--from", dest="from_ref", help="Starting reference (tag or commit)"
    )
    changelog_parser.add_argument(
        "--to", dest="to_ref", default="HEAD", help="Ending reference (tag or commit)"
    )
    changelog_parser.add_argument("--output", help="Output file (default: stdout)")

    # Set default function for release command
    if subparsers:  # Only set func if attaching to main parser
        release_parser.set_defaults(func=run_release_command)

    return release_parser


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI.

    Args:
        args: Command line arguments (defaults to sys.argv[1:])

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    if args is None:
        args = sys.argv[1:]

    # Basic version check from HEAD
    try:
        pyproject_path = Path.cwd() / "pyproject.toml"
        if pyproject_path.exists():
            with open(pyproject_path, "rb") as f:
                # Use importlib.metadata or tomllib based on Python version
                try:
                    import tomllib  # Python 3.11+

                    data = tomllib.load(f)
                except ImportError:
                    import tomli  # Older Python

                    data = tomli.load(f)

                toml_version = data.get("tool", {}).get("poetry", {}).get("version")
                if toml_version and __version__ != toml_version:
                    print(
                        f"Warning: Version mismatch detected - pyproject.toml ({toml_version}) vs __init__.py ({__version__})"
                    )
                    print("Consider running 'snowpack release check' to verify consistency.")
    except Exception as e:
        logger.warning(f"Failed to perform pyproject.toml version check: {e}", exc_info=False)
        pass  # Silently continue if this check fails - not critical

    # Setup main parser
    parser = argparse.ArgumentParser(
        description="Snowpack Stack - A modular, configuration-driven data pipeline automation framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,  # Use RawDescriptionHelpFormatter if needed
    )
    # Add global --version flag handled by argparse itself
    parser.add_argument(
        "-v", "--version", action="version", version=f"Snowpack Stack version: {__version__}"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Register command parsers
    create_build_parser(subparsers)
    create_setup_parser(subparsers)
    create_release_parser(subparsers)
    register_tool_commands(subparsers)  # Register tool manager commands

    # Parse arguments
    try:
        parsed_args = parser.parse_args(args)
    except SystemExit as e:
        # Argparse handles --help and exits, return the code
        return e.code

    # Dispatch command
    if not parsed_args.command:
        # No command was specified
        parser.print_help()
        return 1  # Indicate error/no action
    elif hasattr(parsed_args, "func"):
        # Command was registered with set_defaults(func=...)
        # Includes setup, release, tool manager commands
        try:
            return parsed_args.func(parsed_args)
        except SystemExit:  # Allow SystemExit to propagate for argparse errors
            raise
        except Exception as e:
            logger.error(f"Command '{parsed_args.command}' failed: {e}", exc_info=True)
            return 1
    else:
        # Handle commands without an explicit func set (like build before fix)
        if parsed_args.command == "build":
            # This path might be redundant now that build_parser sets func
            try:
                return run_build_command(parsed_args)
            except SystemExit:  # Allow SystemExit to propagate for argparse errors
                raise
            except Exception as e:
                logger.error(f"Command '{parsed_args.command}' failed: {e}", exc_info=True)
                return 1
        else:
            # Should not happen if all commands are registered correctly
            logger.error(f"Unknown command structure for: {parsed_args.command}")
            parser.print_help()
            return 1


if __name__ == "__main__":
    sys.exit(main())
