# snowpack_stack/source_handler.py
"""
Handles data source connections and interactions.
"""

import logging
from typing import Dict, List, Tuple

import psycopg2

logger = logging.getLogger(__name__)


class BaseSourceHandler:
    """Base class for source handlers."""

    def __init__(self, connection_params: Dict[str, str]):
        self.connection_params = connection_params

    def get_tables(self) -> List[Tuple]:
        """
        Get all tables from the source.

        Returns:
            List[Tuple]: List of tables with their schemas
        """
        raise NotImplementedError("Subclasses must implement get_tables")

    def get_columns(self, schema: str, table: str) -> List[Tuple]:
        """
        Get columns for a specific table.

        Args:
            schema (str): Schema name
            table (str): Table name

        Returns:
            List[Tuple]: List of column details
        """
        raise NotImplementedError("Subclasses must implement get_columns")


class PostgresSourceHandler(BaseSourceHandler):
    """Handler for PostgreSQL database sources."""

    def __init__(self, connection_params: Dict[str, str]):
        super().__init__(connection_params)
        self.conn = None
        self.connect()

    def connect(self):
        """Establish connection to the PostgreSQL database."""
        try:
            self.conn = psycopg2.connect(**self.connection_params)
            logger.info("Connected to PostgreSQL database")
        except psycopg2.Error as e:
            logger.error(f"Error connecting to PostgreSQL: {e}")
            raise

    def get_tables(self) -> List[Tuple]:
        """
        Get all tables from the PostgreSQL database.

        Returns:
            List[Tuple]: List of (schema, table) tuples
        """
        query = """
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
        AND table_type = 'BASE TABLE'
        ORDER BY table_schema, table_name
        """

        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            tables = cursor.fetchall()
            cursor.close()
            return tables
        except psycopg2.Error as e:
            logger.error(f"Error fetching tables: {e}")
            raise

    def get_columns(self, schema: str, table: str) -> List[Tuple]:
        """
        Get columns for a specific table.

        Args:
            schema (str): Schema name
            table (str): Table name

        Returns:
            List[Tuple]: List of column details (schema, table, name, type)
        """
        query = """
        SELECT table_schema, table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = %s
        AND table_name = %s
        ORDER BY ordinal_position
        """

        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (schema, table))
            columns = cursor.fetchall()
            cursor.close()
            return columns
        except psycopg2.Error as e:
            logger.error(f"Error fetching columns: {e}")
            raise


def get_source_handler(source_type: str, connection_params: Dict[str, str]):
    """
    Factory function to get the appropriate source handler.

    Args:
        source_type (str): Type of source ('postgres', etc.)
        connection_params (Dict[str, str]): Connection parameters

    Returns:
        BaseSourceHandler: An instance of the appropriate source handler
    """
    if source_type.lower() == "postgres":
        return PostgresSourceHandler(connection_params)
    else:
        raise ValueError(f"Unsupported source type: {source_type}")
