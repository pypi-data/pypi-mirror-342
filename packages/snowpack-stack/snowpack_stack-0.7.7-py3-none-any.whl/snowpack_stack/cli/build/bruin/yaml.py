"""Build Bruin YAML assets."""

def main() -> int:
    """Build Bruin YAML assets.
    
    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    from snowpack_stack import generate_yaml_assets
    try:
        generate_yaml_assets() 
        return 0 # Return 0 on success
    except Exception as e:
        # Log error appropriately here if needed
        print(f"Error during YAML asset generation: {e}")
        return 1 # Return non-zero on failure 