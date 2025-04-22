"""
Project initialization module for Snowpack Stack tool manager.

This module provides functionality to initialize new projects for tools
like dbt and Bruin.
"""

import logging
import os
import shutil
import subprocess

# Setup logging
logger = logging.getLogger(__name__)


def initialize_dbt_project(project_name=None):
    """
    Initialize a new dbt project.

    Args:
        project_name (str, optional): The name of the project to create.
            If None, the user will be prompted to provide a name.

    Returns:
        tuple: (success, project_path)
            - success: True if the project was successfully initialized
            - project_path: The path to the initialized project
    """
    # If no project name is provided, prompt the user
    if not project_name:
        print("\n=== Initialize dbt Project ===\n")
        project_name = input("Enter a name for your dbt project: ").strip()

        # Validate project name
        if not project_name:
            print("❌ Project name cannot be empty.")
            return False, None

    # Ensure the project name is valid for dbt
    # Replace spaces with underscores and remove special characters
    safe_project_name = "".join(c if c.isalnum() or c == "_" else "_" for c in project_name)
    if safe_project_name != project_name:
        print(f"⚠️  Project name adjusted to '{safe_project_name}' for compatibility.")
        project_name = safe_project_name

    print(f"\nInitializing dbt project '{project_name}'...")

    # Find the absolute path to dbt
    dbt_path = shutil.which("dbt")
    if not dbt_path:
        logger.error("dbt executable not found in PATH.")
        print(
            "\n❌ Error: 'dbt' command not found. Please ensure dbt is installed and in your system's PATH."
        )
        return False, None

    # Check if the project directory already exists
    project_path = os.path.abspath(project_name)
    if os.path.exists(project_path):
        print(f"\n⚠️  Directory '{project_path}' already exists.")
        overwrite = (
            input("Continue and potentially overwrite existing files? (y/n): ").strip().lower()
        )
        if overwrite not in ["y", "yes"]:
            print("\nOperation cancelled.")
            return False, None

    try:
        # First, try with --skip-profile-setup flag (available in newer dbt versions)
        print("\nAttempting to initialize project with --skip-profile-setup...")
        try:
            # Use the absolute path for dbt
            result = subprocess.run(
                [dbt_path, "init", project_name, "--skip-profile-setup"],
                capture_output=True,
                text=True,
                check=False,
                timeout=30,
            )  # nosec B603

            # If successful, process the result
            if result.returncode == 0 and os.path.exists(
                os.path.join(project_path, "dbt_project.yml")
            ):
                print("\nOutput:")
                print(result.stdout)
                print(f"\n✅ dbt project initialized successfully at: {project_path}")
                return True, project_path
        except (subprocess.TimeoutExpired, subprocess.SubprocessError):
            print("\n⚠️  Initialization with --no-interaction flag failed or timed out.")

        # If the first attempt failed, try the standard approach with a timeout
        print("\nAttempting to initialize project with standard command...")
        try:
            # Use the absolute path for dbt
            result = subprocess.run(
                [dbt_path, "init", project_name],
                capture_output=True,
                text=True,
                check=False,
                timeout=30,
            )  # nosec B603

            # Display the output
            if result.stdout:
                print("\nOutput:")
                print(result.stdout)

            if result.stderr and result.returncode != 0:
                print("\nErrors:")
                print(result.stderr)

            # Verify the project was created
            if os.path.exists(os.path.join(project_path, "dbt_project.yml")):
                print(f"\n✅ dbt project initialized successfully at: {project_path}")
                return True, project_path
        except subprocess.TimeoutExpired:
            print("\n⚠️  Standard initialization timed out.")

    except Exception as e:
        logger.error(f"Error initializing dbt project: {e}")
        print(f"\n❌ Error initializing dbt project: {e}")


def initialize_bruin_project(project_name=None):
    """
    Initialize a new Bruin project.

    Args:
        project_name (str, optional): The name of the project to create.
            If None, the user will be prompted to provide a name.

    Returns:
        tuple: (success, project_path)
            - success: True if the project was successfully initialized
            - project_path: The path to the initialized project
    """
    # If no project name is provided, prompt the user
    if not project_name:
        print("\n=== Initialize Bruin Project ===\n")
        project_name = input("Enter a name for your Bruin project: ").strip()

        # Validate project name
        if not project_name:
            print("❌ Project name cannot be empty.")
            return False, None

    # Ensure the project name is valid
    # Replace spaces with hyphens and remove special characters
    safe_project_name = "".join(c if c.isalnum() or c == "-" else "-" for c in project_name)
    if safe_project_name != project_name:
        print(f"❌ Invalid project name: '{project_name}'.")
        print("   Bruin project names can only contain letters, numbers, and hyphens (-).")
        return False, None

    # Ask user to select a template
    print("\n=== Select Bruin Template ===\n")
    print("Please enter a template name or press Enter to use 'default'")
    print("See available templates at: https://bruin-data.github.io/bruin/commands/init.html")

    template_choice = input("\nTemplate name: ").strip()
    if not template_choice:
        template_choice = "default"
        print("Using default template")

    print(f"\nInitializing Bruin project '{project_name}' with template '{template_choice}'...")

    # Find the absolute path to bruin
    bruin_path = shutil.which("bruin")
    if not bruin_path:
        logger.error("bruin executable not found in PATH.")
        print(
            "\n❌ Error: 'bruin' command not found. Please ensure Bruin is installed and in your system's PATH."
        )
        return False, None

    try:
        # Run bruin init command with the selected template and project name
        # Use the absolute path for bruin
        result = subprocess.run(
            [bruin_path, "init", template_choice, project_name],
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        )  # nosec B603

        # Display the output
        if result.stdout:
            print("\nOutput:")
            print(result.stdout)

        if result.stderr and result.returncode != 0:
            print("\nErrors:")
            print(result.stderr)
            return False, None

        # Get the absolute path to the project
        project_path = os.path.abspath(project_name)

        # Verify the project was created
        if os.path.exists(project_path) and os.path.isdir(project_path):
            print(f"\n✅ Bruin project initialized successfully at: {project_path}")
            return True, project_path
        else:
            print(
                "\n❌ Bruin project initialization failed. The project directory was not created."
            )
            return False, None

    except subprocess.TimeoutExpired:
        print("\n❌ Bruin init command timed out.")
        print("Try running 'bruin init' manually and then register the tool with Snowpack Stack.")
        return False, None
    except Exception as e:
        logger.error(f"Error initializing Bruin project: {e}")
        print(f"\n❌ Error initializing Bruin project: {e}")
        return False, None


def initialize_tool_project(tool_name, project_name=None):
    """
    Initialize a new project for a specific tool.

    Args:
        tool_name (str): The name of the tool to initialize a project for (dbt, bruin)
        project_name (str, optional): The name of the project to create

    Returns:
        tuple: (success, project_path)
            - success: True if the project was successfully initialized
            - project_path: The path to the initialized project
    """
    tool_name = tool_name.lower()

    if tool_name == "dbt":
        success, project_path = initialize_dbt_project(project_name)
        if not success:
            print("\n⚠️  Failed to initialize dbt project.")
            print(
                "You can still use dbt with Snowpack Stack, but you'll need to initialize a project manually later."
            )
            # Return partial success - we couldn't initialize but we can still register the tool
            return False, None
        return success, project_path
    elif tool_name == "bruin":
        return initialize_bruin_project(project_name)
    else:
        logger.error(f"Unsupported tool for initialization: {tool_name}")
        print(f"\n❌ Initialization not supported for {tool_name}.")
        return False, None


def should_initialize_project(tool_name):
    """
    Ask the user if they want to initialize a new project or use an existing one.

    Args:
        tool_name (str): The name of the tool

    Returns:
        tuple: (action, existing_path)
            - action: "new" for new project, "existing" for existing project, "none" for no project
            - existing_path: Path to existing project if action is "existing", None otherwise
    """
    print(f"\n=== {tool_name.upper()} Project Setup ===\n")
    print("Do you want to:")
    print(f"1. Initialize a new {tool_name} project")
    print(f"2. Use an existing {tool_name} project")
    print("3. Skip project setup for now")

    while True:
        choice = input("\nEnter your choice (1-3): ").strip()

        if choice == "1":
            return "new", None
        elif choice == "2":
            path = register_existing_project(tool_name)
            if path:
                return "existing", path
            # If registration failed, ask again
            continue
        elif choice == "3":
            return "none", None
        else:
            print("Please enter a number between 1 and 3.")


def register_existing_project(tool_name):
    """
    Register an existing project by asking for its path and verifying it.

    Args:
        tool_name (str): The name of the tool

    Returns:
        str or None: Path to the existing project if valid, None otherwise
    """
    print(f"\n=== Register Existing {tool_name.upper()} Project ===\n")
    print(f"Please enter the full path to your existing {tool_name} project directory:")
    print("Example: /Users/username/projects/my_dbt_project")

    project_path = input("\nProject path: ").strip()

    if not project_path:
        print("❌ Path cannot be empty.")
        return None

    # Convert to absolute path and normalize
    project_path = os.path.abspath(os.path.expanduser(project_path))

    # Verify the path exists and is a directory
    if not os.path.exists(project_path):
        print(f"❌ Path does not exist: {project_path}")
        return None

    if not os.path.isdir(project_path):
        print(f"❌ Path is not a directory: {project_path}")
        return None

    # Verify it's a valid project directory based on the tool
    if tool_name.lower() == "dbt":
        if not os.path.exists(os.path.join(project_path, "dbt_project.yml")):
            print("❌ Not a valid dbt project directory (missing dbt_project.yml)")
            return None
    elif tool_name.lower() == "bruin":
        # Check for typical Bruin project files
        if not (
            os.path.exists(os.path.join(project_path, "bruin.yaml"))
            or os.path.exists(os.path.join(project_path, "bruin.yml"))
        ):
            print("❌ Not a valid Bruin project directory (missing bruin.yaml or bruin.yml)")
            return None

    print(f"\n✅ Valid {tool_name} project found at: {project_path}")
    return project_path
