"""
Command to verify internal access.

This command checks if the user has internal access to snowpack-stack
based on their API key configuration.
"""

import os

from snowpack_stack.access_control import get_key_info, is_snowpack_developer


def main():
    """Run the verify-internal command."""
    print("Verifying internal developer access...")

    # Check if API key is set
    api_key = os.environ.get("SNOWPACK_STACK_API_KEY")
    if not api_key:
        print("\n❌ SNOWPACK_STACK_API_KEY environment variable not found.")
        print("\nTo configure internal access:")
        print("1. Generate a secure key using:")
        print('   python -c "import secrets; print(secrets.token_hex(32))"')
        print("2. Add to your .zshrc:")
        print('   export SNOWPACK_STACK_API_KEY="your_generated_key"')
        print("3. Contact the Snowpack team to validate your key")
        return 1

    # Print key information
    key_info = get_key_info()
    if key_info["status"] == "configured":
        print(f"API key configured: {key_info['key_hint']}")

    # Check if internal key is set (requires server-side configuration)
    internal_key = os.environ.get("SNOWPACK_STACK_INTERNAL_KEY")
    if not internal_key:
        print("\n❌ SNOWPACK_STACK_INTERNAL_KEY not configured in this environment.")
        print("This is expected for local development environments.")
        print("The CI/CD GitHub Actions system should have this key configured.")
        print("\n⚠️ Running in Public mode. Internal commands will not be available.")
        return 1

    # Check if the developer has access
    try:
        has_access = is_snowpack_developer()
        if has_access:
            print("\n✅ Verified as a Snowpack Data internal developer!")
            print("You now have access to internal commands like 'release'.")
            return 0
        else:
            print("\n❌ Access verification failed.")
            print("Your API key does not match the expected value.")
            print("Please contact the Snowpack team to get the correct key.")
            return 1
    except Exception as e:
        print(f"\n❌ Error during verification: {str(e)}")
        return 1


if __name__ == "__main__":
    main()
