"""Database utilities for Snowpack Stack."""

import logging
from typing import Any, Dict, List, Optional, Tuple

import psycopg2
from psycopg2.extensions import connection as pg_connection

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """Database connection manager."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize database connection manager.

        Args:
            config: Database configuration dictionary
        """
        self.config = config
        self.connection: Optional[pg_connection] = None

    def __enter__(self) -> "DatabaseConnection":
        """Context manager entry.

        Returns:
            DatabaseConnection: Self for use in with statement
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.close()

    def connect(self) -> None:
        """Establish database connection."""
        try:
            # Validate required parameters
            required_params = ["database", "user", "password"]
            missing_params = [param for param in required_params if param not in self.config]
            if missing_params:
                raise ValueError(
                    f"Missing required database parameters: {', '.join(missing_params)}"
                )

            # Use connection_name as host if host is not provided
            host = self.config.get("host", self.config.get("connection_name", "localhost"))

            # Get port value
            port_value = self.config.get("port", 5432)
            try:
                port = int(port_value)
                logger.info(f"Using database port: {port}")
            except (ValueError, TypeError) as e:
                logger.error(f"Invalid port value '{port_value}': {e}")
                raise ValueError(
                    f"Invalid port value '{port_value}'. Must be a valid integer."
                ) from e

            self.connection = psycopg2.connect(
                host=host,
                port=port,
                database=self.config["database"],
                user=self.config["user"],
                password=self.config["password"],
            )
            logger.info(
                f"Successfully connected to database {self.config['database']} on {host}:{port}"
            )
        except Exception as e:
            logger.error("Failed to connect to database: %s", e)
            raise

    def close(self) -> None:
        """Close database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def fetch_all_tables(self, schema: str) -> List[str]:
        """Fetch all tables from a schema.

        Args:
            schema: Schema name

        Returns:
            List[str]: List of table names
        """
        if not self.connection:
            self.connect()

        try:
            cursor = self.connection.cursor()
            query = """
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = %s 
                  AND table_type = 'BASE TABLE'
                ORDER BY table_name;
            """
            cursor.execute(query, (schema,))
            tables = [row[0] for row in cursor.fetchall()]
            cursor.close()
            return tables
        except Exception as e:
            logger.error("Error fetching tables for schema '%s': %s", schema, e)
            return []

    def fetch_columns(self, schema: str, table: str) -> List[Tuple[str, str, str, str]]:
        """Fetch column details from a table.

        Args:
            schema: Schema name
            table: Table name

        Returns:
            List[Tuple]: List of (schema, table, column, type) tuples
        """
        if not self.connection:
            self.connect()

        try:
            cursor = self.connection.cursor()
            query = """
                SELECT table_schema, table_name, column_name, data_type 
                FROM information_schema.columns 
                WHERE table_schema = %s AND table_name = %s
                ORDER BY ordinal_position;
            """
            cursor.execute(query, (schema, table))
            columns = cursor.fetchall()
            cursor.close()
            return columns
        except Exception as e:
            logger.error("Error fetching columns for %s.%s: %s", schema, table, e)
            return []
