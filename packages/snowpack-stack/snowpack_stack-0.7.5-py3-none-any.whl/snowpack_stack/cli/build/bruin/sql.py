"""Build Bruin SQL assets."""

def main() -> int:
    """Build Bruin SQL assets.
    
    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    from snowpack_stack import generate_sql_assets
    try:
        generate_sql_assets() 
        return 0 # Return 0 on success
    except Exception as e:
        # Log error appropriately here if needed
        print(f"Error during SQL asset generation: {e}")
        return 1 # Return non-zero on failure 