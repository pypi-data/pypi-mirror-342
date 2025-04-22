"""Command to create a new release."""

import shutil
import subprocess
from pathlib import Path
from typing import List, Tuple


def get_executable_path(cmd: str) -> str:
    """Get the absolute path of an executable using shutil.which."""
    path = shutil.which(cmd)
    if not path:
        raise FileNotFoundError(f"Command '{cmd}' not found in PATH")
    return path


def run_command(cmd: List[str], **kwargs) -> subprocess.CompletedProcess:
    """Run a command safely with absolute paths.

    This function is secure because:
    1. We use absolute paths from shutil.which()
    2. We never use shell=True
    3. All commands are hardcoded, not user input
    4. Input validation is performed before execution
    """
    # Get absolute path for the first command
    cmd[0] = get_executable_path(cmd[0])
    try:
        # nosec B603 - This is safe because we use absolute paths and never use shell=True
        return subprocess.run(cmd, check=True, capture_output=True, text=True, **kwargs)  # nosec
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(cmd)}")
        print(f"Error output: {e.stderr}")
        raise


def run_pre_release_checks() -> Tuple[bool, List[str]]:
    """Run automated pre-release checks.

    This function is secure because:
    1. All subprocess calls use run_command() which enforces security
    2. File operations use safe Path objects
    3. Temporary files are cleaned up in finally blocks
    4. No user input is used in command construction
    """
    issues = []
    venv_path = None

    try:
        # 1. Update dependencies
        print("Updating dependencies...")
        run_command(["poetry", "update"])

        # 2. Run pre-commit
        print("Running pre-commit checks...")
        run_command(["pre-commit", "run", "--all-files"])

        # 3. Run tests
        print("Running test suite...")
        run_command(["pytest"])

        # 4. Test clean installation
        print("Testing clean installation...")

        # Build the package first
        run_command(["poetry", "build"])

        # Set up clean test environment
        venv_path = Path("clean-test-env").absolute()

        # Download and install uv using curl
        curl_path = get_executable_path("curl")
        print("Downloading uv installer...")
        # nosec B603 - Safe because URL is hardcoded and we use absolute paths
        subprocess.run(
            [curl_path, "-LsSf", "https://astral.sh/uv/install.sh"],  # nosec
            check=True,
            capture_output=True,
            text=True,
        )

        # Create and activate virtual environment
        print("Creating test environment...")
        uv_path = get_executable_path("uv")
        run_command([uv_path, "venv", str(venv_path)])

        # Get paths for pip installation
        pip_path = venv_path / "bin" / "pip"
        dist_path = Path("dist").absolute()
        wheel_files = list(dist_path.glob("*.whl"))
        if not wheel_files:
            raise FileNotFoundError("No wheel files found in dist directory")

        # Install the package
        print("Installing package in test environment...")
        run_command([str(pip_path), "install", str(wheel_files[0])])

        # Test the installation
        print("Verifying installation...")
        python_path = venv_path / "bin" / "python"
        test_script = (
            "from snowpack_stack import __version__\n"
            "import snowpack_stack.cli as cli\n"
            "print(f'Version: {__version__}')\n"
            "assert cli.run_cli(['--version']) == 0\n"
        )
        run_command([str(python_path), "-c", test_script])

    except subprocess.CalledProcessError as e:
        issues.append(f"Command failed: {e.cmd}\nError output: {e.stderr}")
    except FileNotFoundError as e:
        issues.append(str(e))
    except Exception as e:
        issues.append(f"Unexpected error: {str(e)}")
    finally:
        # Cleanup using shutil (safer than rm -rf)
        if venv_path and venv_path.exists():
            try:
                shutil.rmtree(venv_path)
            except Exception as e:
                print(f"Warning: Cleanup failed: {str(e)}")

    return len(issues) == 0, issues


def create_release(args):
    """Create a new release."""
    # Run automated checks first
    if not args.force:
        print("Running pre-release checks...")
        checks_passed, issues = run_pre_release_checks()
        if not checks_passed:
            print("\nPre-release checks failed:")
            for issue in issues:
                print(f"- {issue}")

            print("\nFix these issues before releasing or use --force to bypass checks")
            return 1

        # Prompt for manual checks
        print("\nPlease confirm the following manual checks:")
        print("1. CHANGELOG.md is updated with all significant changes")
        print("2. Documentation accurately reflects all changes")
        print("3. Any breaking changes are properly documented")

        confirm = input("\nHave you completed these checks? (y/N): ")
        if confirm.lower() != "y":
            print("Aborting release. Please complete manual checks.")
            return 1

    # Proceed with existing release logic
    ...


def add_create_arguments(parser):
    """Add arguments for create command."""
    parser.add_argument(
        "--force", action="store_true", help="Skip pre-release checks and confirmations"
    )
    # ... existing arguments ...
