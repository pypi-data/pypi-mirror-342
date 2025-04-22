"""Build all assets."""

def main() -> int:
    """Build all assets.
    
    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    # Import these only when needed to avoid circular imports
    from snowpack_stack.cli.build.bruin import main as bruin_main
    
    # Run all builders
    result = bruin_main() 
    return 0 if isinstance(result, int) and result == 0 else 1 # Return 0 on success 