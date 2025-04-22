"""
Installation guidance module for Snowpack Stack tool manager.

This module provides functionality to guide users through installing
required tools if they're not already installed.
"""

import logging
from typing import List, Optional, Tuple

from snowpack_stack.cli.tool_manager.metadata import load_metadata
from snowpack_stack.cli.tool_manager.verify import is_version_outdated, verify_tool

# Setup logging
logger = logging.getLogger(__name__)

# Documentation links
DBT_DOCS_URL = "https://docs.getdbt.com/docs/get-started/installation"
BRUIN_DOCS_URL = "https://bruin-data.github.io/bruin/getting-started/introduction/installation.html"


def provide_dbt_installation_guidance():
    """
    Provide guidance for installing dbt.

    Prints detailed instructions for installing dbt with different adapters.
    """
    print("\n=== dbt Installation Guidance ===\n")
    print("dbt is not installed or not found in your PATH.")
    print("To install dbt, you need to choose an adapter based on your data warehouse:")
    print("\n1. For BigQuery:")
    print("   pip install dbt-bigquery")
    print("\n2. For Snowflake:")
    print("   pip install dbt-snowflake")
    print("\n3. For PostgreSQL:")
    print("   pip install dbt-postgres")
    print("\n4. For other adapters, see the documentation.")
    print(f"\nFor more information, visit: {DBT_DOCS_URL}")
    print(
        "\nAfter installation, you may need to restart your terminal or activate your virtual environment."
    )


def provide_bruin_installation_guidance():
    """
    Provide guidance for installing Bruin.

    Prints instructions for installing Bruin.
    """
    print("\n=== Bruin Installation Guidance ===\n")
    print("Bruin is not installed or not found in your PATH.")
    print("To install Bruin, follow these steps:")
    print("\n1. Install via homebrew:")
    print("   brew install bruin-data/tap/bruin")
    print("\n2. Verify the installation:")
    print("   bruin --version")
    print(f"\nFor more information, visit: {BRUIN_DOCS_URL}")
    print(
        "\nAfter installation, you may need to restart your terminal or activate your virtual environment."
    )


def provide_installation_guidance(tool_name: str):
    """
    Provide installation guidance for a specific tool.

    Args:
        tool_name (str): The name of the tool to provide guidance for (dbt, bruin)
    """
    tool_name = tool_name.lower()

    if tool_name == "dbt":
        provide_dbt_installation_guidance()
    elif tool_name == "bruin":
        provide_bruin_installation_guidance()
    else:
        print(f"\n=== Installation Guidance for {tool_name} ===\n")
        print(f"Sorry, installation guidance for {tool_name} is not available.")
        print("Please refer to the tool's documentation for installation instructions.")


def verify_after_installation(tool_name: str) -> Tuple[bool, Optional[str], List[str]]:
    """
    Prompt the user to confirm they've completed installation and re-verify the tool.

    Args:
        tool_name (str): The name of the tool to verify

    Returns:
        Tuple[bool, Optional[str], List[str]]:
            - success: True if the tool was successfully verified, False otherwise
            - version: The version of the tool if installed, None otherwise
            - variants: List of variants/adapters if available
    """
    print("DEBUG: Entering verify_after_installation")
    print("\nPlease confirm when you have completed the installation.")
    input("Press Enter to continue...")

    print(f"\nVerifying {tool_name} installation...")
    is_installed, version, variants = verify_tool(tool_name)

    if is_installed and version:
        print(f"\n✅ {tool_name} is now installed (version: {version}).")
        if variants:
            print(f"   Detected variants/adapters: {', '.join(variants)}")
        return True, version, variants
    elif is_installed:
        print(f"\n⚠️  {tool_name} seems to be installed, but we couldn't determine the version.")
        return True, None, variants
    else:
        print(f"\n❌ {tool_name} is still not detected in your PATH.")
        print("Would you like to:")
        print("1. See the installation guidance again")
        print("2. Continue anyway (not recommended)")
        print("3. Exit")

        choice = input("\nEnter your choice (1-3): ")
        logger.debug(f"User choice for post-installation verification failure: {choice}")
        print(f"DEBUG: repr(choice) = {repr(choice)}")

        if choice == "1":
            provide_installation_guidance(tool_name)
            print("DEBUG: Returning False (User chose 1)")
            return False, None, []
        elif choice == "2":
            print("\n⚠️  Continuing without verified installation. This may cause issues later.")
            print("DEBUG: Returning True, None (User chose 2)")
            return True, None, []  # Indicate success (user override), but no version
        else:
            # User chose 3 or invalid input
            print("\nSkipping further verification attempts for this tool.")
            print("DEBUG: Returning False (User chose 3 or invalid)")
            # Do NOT exit here - let the caller (retry_installation) handle it.
            # sys.exit(1)
            return False, None, []


def retry_installation(
    tool_name: str, max_attempts: int = 3
) -> Tuple[bool, Optional[str], List[str]]:
    """
    Attempt to verify a tool installation with multiple retries.
    Guides user through installation if verification fails.

    Args:
        tool_name (str): The name of the tool to verify
        max_attempts (int, optional): Maximum number of verification attempts

    Returns:
        Tuple[bool, Optional[str], List[str]]:
            Represents the final state:
            - success: True if tool is considered installed (even if forced by user choice 2).
            - version: The version string if found.
            - variants: List of variants/adapters.
    """
    print("DEBUG: Entering retry_installation")
    last_success = False
    last_version = None
    last_variants = []

    for attempt in range(1, max_attempts + 1):
        logger.info(f"Verification attempt {attempt}/{max_attempts} for {tool_name}")

        if attempt > 1:
            print(f"\nRetrying verification ({attempt}/{max_attempts})...")

        # verify_after_installation now handles the full prompt/check/choice loop
        # It returns:
        # (True, version, variants) if verified ok
        # (True, None, []) if user chose '2' (continue anyway)
        # (False, None, []) if user chose '1' (see guidance) or '3' (exit - handled by sys.exit within)
        # We need to handle the sys.exit case gracefully if possible, or adjust verify_after_installation

        try:
            success, version, variants = verify_after_installation(tool_name)
            last_success, last_version, last_variants = success, version, variants

            if success and version:
                # Verified successfully, check for outdated
                metadata = load_metadata()
                min_version = metadata.get("tools", {}).get(tool_name, {}).get("min_version")
                if version and min_version and is_version_outdated(version, min_version):
                    logger.warning(
                        f"Your {tool_name} version ({version}) is older than the recommended version ({min_version})."
                    )
                    print("Consider upgrading for the best experience.")
                print("DEBUG: Verification successful with version.")
                return True, version, variants  # Exit loop on success with version
            elif success and version is None:
                # User chose '2' (Continue anyway)
                print("DEBUG: User chose to continue without verified version.")
                # Treat as success for the purpose of adding the tool, but without version info
                return True, None, []  # Exit loop, indicating installed but unknown version
            else:  # success is False
                # User chose '1' (See guidance again) - loop continues
                print(
                    f"DEBUG: Verification failed (attempt {attempt}), user likely chose to see guidance."
                )
                if attempt < max_attempts:
                    print("\nLet's try again. Make sure the tool is properly installed.")
                    # Guidance is shown within verify_after_installation if choice is 1
                    # provide_installation_guidance(tool_name) # No need to call here
                else:
                    print(f"\nVerification failed after {max_attempts} attempts.")

        except SystemExit:
            # If verify_after_installation called sys.exit (user chose 3)
            print("DEBUG: User chose to exit during verification.")
            # Propagate the exit or return failure? For now, return failure.
            return False, None, []

    # If loop finishes without success
    print(f"\nFailed to verify {tool_name} after {max_attempts} attempts.")
    print("You can continue, but some functionality may not work correctly.")
    return last_success, last_version, last_variants  # Return the result of the last attempt
