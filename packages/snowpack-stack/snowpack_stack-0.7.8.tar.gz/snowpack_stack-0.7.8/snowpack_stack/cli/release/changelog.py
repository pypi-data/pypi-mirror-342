"""Generate a changelog from Git commit history.

This module provides a command to generate a changelog from Git commit history
between two references (e.g., tags or commits).
"""

import argparse
import sys
from typing import List, Optional, Union

# Import our secure subprocess utilities
from snowpack_stack.utils.subprocess_utils import run_git_command


def generate_changelog(
    from_ref: Optional[str], to_ref: str = "HEAD", output_file: Optional[str] = None
) -> int:
    """
    Generate a changelog from Git commit history.

    Args:
        from_ref: Starting reference (tag or commit)
        to_ref: Ending reference (tag or commit)
        output_file: Output file (default: stdout)

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    # Build the git command
    range_spec = f"{from_ref}..{to_ref}" if from_ref else to_ref

    # Basic command to get commit messages in a format suitable for a changelog
    args = ["log", range_spec, "--pretty=format:* %s", "--no-merges"]

    try:
        # Run the command using our secure git command function
        result = run_git_command(args, check=True, capture_output=True)

        # Process the output
        changelog = result.stdout

        # Write to file or stdout
        if output_file:
            with open(output_file, "w") as f:
                f.write(changelog)
        else:
            print(changelog)

        return 0
    except Exception as e:
        print(f"Error generating changelog: {e}")
        return 1


def main(args: Optional[Union[List[str], argparse.Namespace]] = None) -> int:
    """
    Main entry point for the generate-changelog CLI command.

    Args:
        args: Command-line arguments or argparse.Namespace object

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    # If args is already a Namespace object, extract values directly
    if isinstance(args, argparse.Namespace):
        return generate_changelog(
            from_ref=getattr(args, "from_ref", None),
            to_ref=getattr(args, "to_ref", "HEAD"),
            output_file=getattr(args, "output", None),
        )

    # Otherwise, parse arguments normally
    parser = argparse.ArgumentParser(description="Generate a changelog from Git commit history")
    parser.add_argument("--from", dest="from_ref", help="Starting reference (tag or commit)")
    parser.add_argument(
        "--to", dest="to_ref", default="HEAD", help="Ending reference (tag or commit)"
    )
    parser.add_argument("--output", help="Output file (default: stdout)")

    parsed_args = parser.parse_args(args)

    return generate_changelog(
        from_ref=parsed_args.from_ref, to_ref=parsed_args.to_ref, output_file=parsed_args.output
    )


if __name__ == "__main__":
    sys.exit(main())
