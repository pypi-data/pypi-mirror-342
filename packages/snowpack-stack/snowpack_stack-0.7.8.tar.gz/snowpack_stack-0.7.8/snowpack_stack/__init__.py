# snowpack_stack/__init__.py
"""
Snowpack Stack - A modular, configuration-driven data pipeline automation framework.

This package provides tools for automating data pipeline setup and maintenance,
with a focus on Bruin-compatible asset generation.
"""

# This version string will be dynamically replaced during build by poetry-dynamic-versioning
# Manually keeping it in sync with pyproject.toml as a fallback when running from source
__version__ = "0.7.8"


def get_version():
    """Return the package version."""
    return __version__


# Import key modules and functions for the public API
from snowpack_stack.auth import (
    authenticate,
    get_user_email,
    is_authenticated,
    set_api_key,
    set_user_email,
)
from snowpack_stack.core.config import ConfigLoader
from snowpack_stack.generators.bruin.sql_generator import BruinSqlGenerator
from snowpack_stack.generators.bruin.yaml_generator import BruinYamlGenerator

# IMPORTANT: The set_api_key() function is deprecated and will be removed in a future version.
# Please use set_user_email() instead for identification purposes.


# Create convenience functions for the most common operations
def generate_yaml_assets(*args, **kwargs):
    """Generate Bruin-compatible YAML asset files for raw tables."""
    # Check authentication
    if not is_authenticated():
        raise PermissionError("Authentication required. Please authenticate first.")

    # Ensure we always have a config parameter
    if not args and "config" not in kwargs:
        kwargs["config"] = {}

    generator = BruinYamlGenerator(*args, **kwargs)
    return generator.generate()


def generate_sql_assets(*args, **kwargs):
    """Generate Bruin-compatible SQL transformation files."""
    # Check authentication
    if not is_authenticated():
        raise PermissionError("Authentication required. Please authenticate first.")

    # Ensure we always have a config parameter
    if not args and "config" not in kwargs:
        kwargs["config"] = {}

    generator = BruinSqlGenerator(*args, **kwargs)
    return generator.generate()


def run_bruin_generators(*args, **kwargs):
    """Run all Bruin-specific generators."""
    # Check authentication
    if not is_authenticated():
        raise PermissionError("Authentication required. Please authenticate first.")

    results = {}
    results.update(generate_yaml_assets(*args, **kwargs))
    results.update(generate_sql_assets(*args, **kwargs))
    return results


def run_all(*args, **kwargs):
    """Run all available generators in the package."""
    # Check authentication
    if not is_authenticated():
        raise PermissionError("Authentication required. Please authenticate first.")

    # Currently only Bruin generators are implemented
    return run_bruin_generators(*args, **kwargs)


# Set __all__ to control what gets imported with "from snowpack_stack import *"
__all__ = [
    "authenticate",
    "set_user_email",
    "get_user_email",
    "set_api_key",  # Kept for backward compatibility
    "is_authenticated",
    "BruinYamlGenerator",
    "BruinSqlGenerator",
    "ConfigLoader",
    "generate_yaml_assets",
    "generate_sql_assets",
    "run_bruin_generators",
    "run_all",
    "get_version",
]
