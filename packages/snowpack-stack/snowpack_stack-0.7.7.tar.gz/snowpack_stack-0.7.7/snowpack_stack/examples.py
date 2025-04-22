"""
Snowpack Stack Usage Examples.

This module provides example usage of the Snowpack Stack package.
"""

# These imports are used in function examples
import os
from typing import Any, Dict, List

import yaml

# Use dummy assignments to prevent unused import warnings
_: Dict
_: Any
_: List
_: os
_: yaml


def authenticate_example():
    """Example showing how to authenticate with the Snowpack Stack package."""
    import snowpack_stack as snowpack

    # Method 1: Set email directly
    email = "your.email@example.com"  # Replace with your actual email
    snowpack.set_user_email(email)

    # Method 2: Use environment variable
    # Set SNOWPACK_USER_EMAIL environment variable
    # os.environ["SNOWPACK_USER_EMAIL"] = "your.email@example.com"
    # snowpack.authenticate()

    # Method 3: Save email to config file for future use
    # from snowpack_stack.auth import save_user_email
    # save_user_email("your.email@example.com")
    # snowpack.authenticate()

    # Check if authentication was successful
    if snowpack.is_authenticated():
        print("Authentication successful!")
    else:
        print("Authentication failed. Please check your email.")


def generate_yaml_assets_example():
    """Example showing how to generate YAML assets."""
    import snowpack_stack as snowpack

    # First, authenticate
    snowpack.set_user_email("your.email@example.com")  # Replace with your actual email

    # Generate YAML assets using default configuration
    result = snowpack.generate_yaml_assets()
    print(f"Generated YAML assets: {result}")

    # Generate YAML assets with custom configuration
    custom_config = {
        "etl_owner": "your.email@example.com",
        "source": {
            "type": "postgres",
            "connection_name": "postgres_cronos",
            "database": {
                "user": "${CLOUD_SQL_USER}",
                "password": "${CLOUD_SQL_PASSWORD}",
                "database": "${CLOUD_SQL_DATABASE_NAME}",
                "port": "${CLOUD_SQL_PORT}",
            },
            "schemas": {"public": {"tables": ["users", "orders"]}},  # Only specific tables
        },
        "ingestion": "ingestr",
        "transformer": "bruin",
    }

    result = snowpack.generate_yaml_assets(config=custom_config)
    print(f"Generated YAML assets with custom config: {result}")


def generate_sql_assets_example():
    """Example showing how to generate SQL assets."""
    import snowpack_stack as snowpack

    # First, authenticate
    snowpack.set_user_email("your.email@example.com")  # Replace with your actual email

    # Generate SQL assets using default configuration
    result = snowpack.generate_sql_assets()
    print(f"Generated SQL assets: {result}")


def run_bruin_generators_example():
    """Example showing how to run all Bruin generators."""
    import snowpack_stack as snowpack

    # First, authenticate
    snowpack.set_user_email("your.email@example.com")  # Replace with your actual email

    # Run all Bruin generators
    result = snowpack.run_bruin_generators()
    print(f"Ran all Bruin generators: {result}")


def run_all_example():
    """Example showing how to run all generators."""
    import snowpack_stack as snowpack

    # First, authenticate
    snowpack.set_user_email("your.email@example.com")  # Replace with your actual email

    # Run all generators
    result = snowpack.run_all()
    print(f"Ran all generators: {result}")


def use_bruin_generators_directly():
    """Example showing how to use the Bruin generators directly."""
    import snowpack_stack as snowpack
    from snowpack_stack.core.config import load_config

    # First, authenticate
    snowpack.set_user_email("your.email@example.com")  # Replace with your actual email

    # Load configuration
    config = load_config()
    if not config:
        print("Failed to load configuration.")
        return

    # Create and use the YAML generator directly
    yaml_generator = snowpack.BruinYamlGenerator(config)
    if yaml_generator.validate():
        yaml_generator.generate()

    # Create and use the SQL generator directly
    sql_generator = snowpack.BruinSqlGenerator(config)
    if sql_generator.validate():
        sql_generator.generate()


if __name__ == "__main__":
    # Run the examples
    authenticate_example()
    # generate_yaml_assets_example()
    # generate_sql_assets_example()
    # run_bruin_generators_example()
    # run_all_example()
    # use_bruin_generators_directly()
