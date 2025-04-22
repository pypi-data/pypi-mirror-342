"""Bruin build module."""

def main() -> int:
    """Build all Bruin assets.
    
    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    from snowpack_stack.cli.build.bruin.sql import main as sql_main
    from snowpack_stack.cli.build.bruin.yaml import main as yaml_main
    
    # Run all Bruin builders
    sql_exit_code = sql_main()
    if sql_exit_code != 0:
        return sql_exit_code
        
    yaml_exit_code = yaml_main()
    return yaml_exit_code # Return 0 on success
