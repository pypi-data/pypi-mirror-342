"""Command for generating Bruin SQL asset files."""

from typing import Any, Dict

from snowpack_stack.cli.base import BaseCommand
from snowpack_stack.generators.base import BaseGenerator
from snowpack_stack.generators.bruin.sql_generator import BruinSqlGenerator


class SqlGeneratorCommand(BaseCommand):
    """Command for generating SQL asset files."""

    def create_generator(self, config: Dict[str, Any]) -> BaseGenerator:
        """Create a SQL generator instance.

        Args:
            config: Configuration dictionary

        Returns:
            BaseGenerator: SQL generator instance
        """
        return BruinSqlGenerator(config)
