"""CLI package for Snowpack Stack."""

from typing import List, Optional


def run_auth() -> int:
    """Run authentication setup command.

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    from snowpack_stack.cli.auth import main as auth_main

    return auth_main()


def run_verify() -> int:
    """Run verification command to check installation and setup.

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    from snowpack_stack.cli.verify import main as verify_main

    return verify_main()


def run_release() -> int:
    """Run release management commands.

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    from snowpack_stack.cli.release import main as release_main

    return release_main()


def run_all() -> int:
    """Run all available commands.

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    from snowpack_stack.cli.bruin import run_all as run_bruin

    commands: List[callable] = [
        run_bruin,
    ]

    exit_code = 0
    for cmd in commands:
        result = cmd()
        if result != 0:
            exit_code = result

    return exit_code


def run_cli(args: Optional[List[str]] = None) -> int:
    """Run the main CLI command.

    Args:
        args: Command line arguments

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    try:
        from snowpack_stack.cli.main import main

        return main(args)
    except ImportError as e:
        print(f"Error loading CLI: {e}")
        print("\nThis may be due to a missing or misconfigured module.")
        print("Please ensure your installation is complete and up-to-date.")
        return 1
    except Exception as e:
        print(f"Unexpected error running CLI: {e}")
        print("Please report this issue to the development team.")
        return 1
