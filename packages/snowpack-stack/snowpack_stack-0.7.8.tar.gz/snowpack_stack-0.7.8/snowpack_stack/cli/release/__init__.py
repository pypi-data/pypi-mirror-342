"""Release CLI commands.

This package provides CLI commands for managing Snowpack Stack releases,
including checking versions, creating releases, and resetting versions.
"""

import sys
from pathlib import Path
from typing import List, Optional


def run_script(script_name: str, *args) -> int:
    """Run a script from the scripts directory.

    Args:
        script_name: Name of the script to run
        *args: Arguments to pass to the script

    Returns:
        int: Exit code from the script
    """
    # Import these functions only when needed to avoid circular imports
    from snowpack_stack.utils.subprocess_utils import run_command, validate_command_argument

    # Validate script name
    if not validate_command_argument(script_name):
        print(f"Error: Invalid script name: {script_name}")
        return 1

    # Validate all arguments
    for arg in args:
        if not validate_command_argument(str(arg)):
            print(f"Error: Invalid script argument: {arg}")
            return 1

    # Get the path to the scripts directory
    scripts_dir = Path(__file__).parent.parent.parent.parent / "scripts"
    script_path = scripts_dir / script_name

    if not script_path.exists():
        print(f"Error: Script {script_name} not found at {script_path}")
        return 1

    # Construct the command
    python_exe = sys.executable
    cmd = [python_exe, str(script_path)] + list(args)

    # Run the command
    try:
        result = run_command(cmd=cmd, check=True, capture_output=True, text=True)
        # Print output for visibility
        if result.stdout:
            print(result.stdout)
        return result.returncode
    except Exception as e:
        print(f"Error running {script_name}: {e}")
        return 1


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the release CLI command.

    Args:
        args: Command line arguments

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    # Import the subprocess utilities here to avoid circular imports
    from snowpack_stack.utils.subprocess_utils import validate_command_argument

    if not args or len(args) == 0:
        # Default to check command if no subcommand is provided
        return run_script("check_version_consistency.py")

    # Get the subcommand
    subcommand = args[0]

    # Handle help flag for the main release command
    if subcommand == "--help":
        print("Snowpack Stack Release Commands:")
        print("\nAvailable subcommands:")
        print("  check       - Check version consistency across files and git tags")
        print("  create      - Create a new release version")
        print("  changelog   - Generate a changelog from git commits")
        print("  reset       - Reset version to a specific value")
        print("  status      - Check the current release status")
        print("\nExamples:")
        print("  snowpack release check")
        print("  snowpack release create patch")
        print("  snowpack release create minor --pre-release")
        print("  snowpack release create --set 0.5.0 --no-push")
        print("  snowpack release changelog")
        print("  snowpack release reset 0.4.0")
        print("  snowpack release status")
        return 0

    # Validate subcommand
    if not validate_command_argument(subcommand):
        print(f"Error: Invalid subcommand: {subcommand}")
        return 1

    # Process different subcommands
    if subcommand == "check":
        return run_script("check_version_consistency.py")
    elif subcommand == "create":
        # Check for help flag for the create command
        if len(args) > 1 and args[1] == "--help":
            print(
                "Usage: snowpack release create (major|minor|patch|--set VERSION) [--pre-release] [--no-push]"
            )
            print("\nArguments:")
            print("  major|minor|patch - Increment the version by the specified level")
            print("  --set VERSION     - Set the version to a specific value")
            print("\nOptions:")
            print(
                "  --pre-release     - Create a pre-release version (adds branch name to version)"
            )
            print("  --no-push         - Don't push the changes to the remote repository")
            print("\nExamples:")
            print("  snowpack release create patch            # Create a patch release")
            print("  snowpack release create minor            # Create a minor release")
            print("  snowpack release create major            # Create a major release")
            print("  snowpack release create patch --pre-release  # Create a pre-release version")
            print("  snowpack release create --set 0.5.0      # Set version to 0.5.0")
            return 0

        # Process create command with its arguments
        if len(args) < 2:
            print("Error: Missing arguments for create command")
            print(
                "Usage: snowpack release create (major|minor|patch|--set VERSION) [--pre-release] [--no-push]"
            )
            return 1

        # Extract arguments for create command
        create_args = args[1:]

        # Check for flags
        pre_release_flag = "--pre-release" in create_args
        no_push_flag = "--no-push" in create_args

        # Clean list of remaining arguments (remove the flags)
        remaining_args = [arg for arg in create_args if arg not in ["--pre-release", "--no-push"]]

        # Prepare the command arguments
        script_args = []

        # Handle the main command type
        if not remaining_args:
            print("Error: Missing version type or --set argument")
            print(
                "Usage: snowpack release create (major|minor|patch|--set VERSION) [--pre-release] [--no-push]"
            )
            return 1

        if remaining_args[0] == "--set" and len(remaining_args) > 1:
            script_args.extend(["--set", remaining_args[1]])
        elif remaining_args[0] in ["major", "minor", "patch"]:
            script_args.append(remaining_args[0])
        else:
            print(f"Error: Invalid arguments for create command: {' '.join(create_args)}")
            print(
                "Usage: snowpack release create (major|minor|patch|--set VERSION) [--pre-release] [--no-push]"
            )
            return 1

        # Add flags if present
        if pre_release_flag:
            script_args.append("--pre-release")
        if no_push_flag:
            script_args.append("--no-push")

        # Pass all arguments to the script
        return run_script("release.py", *script_args)
    elif subcommand == "changelog":
        # Handle changelog command
        return run_script("generate_changelog.py")
    elif subcommand == "reset":
        if len(args) < 2:
            print("Error: Missing version argument for reset command")
            print("Usage: snowpack release reset VERSION")
            return 1
        version = args[1]
        if not validate_command_argument(version):
            print(f"Error: Invalid version: {version}")
            return 1
        # Use the reset_version function from the release.py module
        from snowpack_stack.cli.release import reset_version

        return reset_version(version)
    elif subcommand == "status":
        return run_script("check_release_status.py")
    else:
        print(f"Error: Unknown release subcommand: {subcommand}")
        return 1
