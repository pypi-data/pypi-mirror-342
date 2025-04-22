"""Command for generating Bruin YAML asset files."""

from typing import Any, Dict

from snowpack_stack.cli.base import BaseCommand
from snowpack_stack.generators.base import BaseGenerator
from snowpack_stack.generators.bruin.yaml_generator import BruinYamlGenerator


class YamlGeneratorCommand(BaseCommand):
    """Command for generating YAML asset files."""

    def create_generator(self, config: Dict[str, Any]) -> BaseGenerator:
        """Create a YAML generator instance.

        Args:
            config: Configuration dictionary

        Returns:
            BaseGenerator: YAML generator instance
        """
        return BruinYamlGenerator(config)
