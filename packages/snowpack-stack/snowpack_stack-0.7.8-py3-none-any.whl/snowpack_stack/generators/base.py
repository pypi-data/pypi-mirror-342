"""Base class for all generators in the Snowpack Stack."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class BaseGenerator(ABC):
    """Abstract base class for all generators."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize the generator with configuration.

        Args:
            config: Configuration dictionary loaded from config files
        """
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    @abstractmethod
    def generate(self, **kwargs) -> bool:
        """Generate the output files.

        Args:
            **kwargs: Additional arguments specific to the generator

        Returns:
            bool: True if generation was successful, False otherwise
        """

    @abstractmethod
    def validate(self) -> bool:
        """Validate the configuration and requirements.

        Returns:
            bool: True if validation passed, False otherwise
        """

    def log_error(self, message: str, error: Optional[Exception] = None) -> None:
        """Log an error message with optional exception details.

        Args:
            message: The error message
            error: Optional exception object
        """
        if error:
            self.logger.error(f"{message}: {str(error)}")
        else:
            self.logger.error(message)

    def log_info(self, message: str) -> None:
        """Log an info message.

        Args:
            message: The info message
        """
        self.logger.info(message)
