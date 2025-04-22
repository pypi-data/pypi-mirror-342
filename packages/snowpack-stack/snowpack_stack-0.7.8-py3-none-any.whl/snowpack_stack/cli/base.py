"""Base class for all CLI commands in the Snowpack Stack."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from snowpack_stack.core.config import load_config
from snowpack_stack.generators.base import BaseGenerator

logger = logging.getLogger(__name__)


class BaseCommand(ABC):
    """Abstract base class for all CLI commands."""

    def __init__(self):
        """Initialize the command."""
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.config: Optional[Dict[str, Any]] = None
        self.generator: Optional[BaseGenerator] = None

    @abstractmethod
    def create_generator(self, config: Dict[str, Any]) -> BaseGenerator:
        """Create the appropriate generator for this command.

        Args:
            config: Configuration dictionary

        Returns:
            BaseGenerator: An instance of a generator
        """

    def setup(self) -> bool:
        """Set up the command by loading config and creating generator.

        Returns:
            bool: True if setup was successful, False otherwise
        """
        try:
            self.config = load_config()
            if not self.config:
                self.logger.error("Failed to load configuration")
                return False

            self.generator = self.create_generator(self.config)
            if not self.generator:
                self.logger.error("Failed to create generator")
                return False

            return True
        except Exception as e:
            self.logger.error(f"Setup failed: {str(e)}")
            return False

    def execute(self) -> bool:
        """Execute the command.

        Returns:
            bool: True if execution was successful, False otherwise
        """
        if not self.setup():
            return False

        try:
            if not self.generator.validate():
                self.logger.error("Validation failed")
                return False

            return self.generator.generate()
        except Exception as e:
            self.logger.error(f"Execution failed: {str(e)}")
            return False

    @classmethod
    def run(cls) -> int:
        """Run the command and return exit code.

        Returns:
            int: 0 for success, 1 for failure
        """
        command = cls()
        success = command.execute()
        return 0 if success else 1
