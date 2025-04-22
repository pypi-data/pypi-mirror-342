"""Build module for snowpack_stack CLI."""
from typing import List, Optional

from snowpack_stack.cli.build.all import main as all_main
from snowpack_stack.cli.build.bruin import main as bruin_main
from snowpack_stack.cli.build.bruin.sql import main as sql_main
from snowpack_stack.cli.build.bruin.yaml import main as yaml_main

__all__ = ["all_main", "bruin_main", "sql_main", "yaml_main"]

def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the build CLI command.
    
    Args:
        args: Command line arguments
        
    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    if not args or len(args) == 0 or args[0] == "all":
        return all_main()
    
    # Import these only if needed to avoid circular imports
    from snowpack_stack.utils.subprocess_utils import validate_command_argument
    
    # Validate generator argument
    generator = args[0]
    if not validate_command_argument(generator):
        print(f"Error: Invalid generator: {generator}")
        return 1
    
    # Handle bruin generator
    if generator == "bruin":
        if len(args) > 1 and args[1]:
            # Handle sub-generators
            asset_type = args[1]
            if not validate_command_argument(asset_type):
                print(f"Error: Invalid asset type: {asset_type}")
                return 1
                
            if asset_type == "yaml":
                return yaml_main()
            elif asset_type == "sql":
                return sql_main()
            else:
                print(f"Error: Unknown asset type: {asset_type}")
                return 1
        else:
            # Run all bruin generators
            return bruin_main()
            
    print(f"Error: Unknown generator: {generator}")
    return 1
