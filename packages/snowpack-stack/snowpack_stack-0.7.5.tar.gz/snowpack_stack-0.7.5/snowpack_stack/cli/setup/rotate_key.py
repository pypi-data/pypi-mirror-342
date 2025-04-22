"""
Command to generate a new API key.

This command generates a new API key for internal access and provides
instructions for configuring it.
"""

from snowpack_stack.access_control import rotate_key


def main():
    """Run the rotate-key command."""
    print("Generating a new API key for internal access...\n")

    # Generate and display the new key with instructions
    rotate_key()

    print("\nRemember to update the SNOWPACK_STACK_INTERNAL_KEY secret in GitHub Actions")
    print("if you want to use this key for CI/CD workflows.")

    return 0


if __name__ == "__main__":
    main()
