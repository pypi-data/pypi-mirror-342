# nosec
"""SQL generator for Bruin assets."""
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

from snowpack_stack.core.config import get_project_root
from snowpack_stack.generators.base import BaseGenerator
from snowpack_stack.utils.db import DatabaseConnection


class BruinSqlGenerator(BaseGenerator):
    """Generator for Bruin SQL transformation files."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize the SQL generator.

        Args:
            config: Configuration dictionary
        """
        super().__init__(config)
        # Get the parent directory (internal-bruin) instead of the project root
        project_root = get_project_root()
        parent_dir = project_root.parent

        # Use bruin-pipeline/assets in the parent directory
        self.output_folder = str(parent_dir / "bruin-pipeline" / "assets")
        os.makedirs(self.output_folder, exist_ok=True)
        self.log_info(f"Using output folder: {self.output_folder}")

    def validate(self) -> bool:
        """Validate configuration and requirements.

        Returns:
            bool: True if validation passed
        """
        try:
            required_fields = [
                ("source.type", lambda c: c.get("source", {}).get("type")),
                ("source.schemas", lambda c: c.get("source", {}).get("schemas")),
            ]

            for field, getter in required_fields:
                if not getter(self.config):
                    self.log_error(f"Missing required field: {field}")
                    return False

            return True
        except Exception as e:
            self.log_error("Validation failed", e)
            return False

    def sanitize_table_name(self, table_name):
        """
        Sanitize a table name to prevent SQL injection.

        Args:
            table_name (str): The raw table name to sanitize

        Returns:
            str: The sanitized table name
        """
        # Basic sanitization: only allow alphanumeric characters, underscores and dots
        # This prevents injection of SQL commands or special characters
        sanitized = re.sub(r"[^a-zA-Z0-9_.]", "", table_name)

        # Validate that the sanitized name meets our expectations
        if sanitized != table_name:
            import logging

            logging.warning(f"Table name sanitized from '{table_name}' to '{sanitized}'")

        # Ensure the table name isn't empty after sanitization
        if not sanitized:
            raise ValueError("Invalid table name: sanitization resulted in empty string")

        return sanitized

    def generate_sql_transformation(
        self, columns: List[Tuple[str, str, str, str]], schema: str, table: str
    ) -> str:
        """Generate SQL transformation code for a table.

        Args:
            columns: List of column metadata tuples
            schema: Schema name
            table: Table name

        Returns:
            str: SQL transformation code
        """
        # Get owner email from config
        owner_email = self.config.get("etl_owner", "info@snowpack-data.com")

        # Build YAML metadata for the @bruin block
        yaml_metadata = {
            "name": f"cronos.{table}",
            "type": "bq.sql",
            "owner": owner_email,
            "description": f"{table} table without deleted records",
            "materialization": {"type": "table"},
            "depends": [f"cronos_raw.{table}"],
            "columns": [],
        }

        # Add column metadata
        for schema_name, table_name, col_name, data_type in columns:
            col_entry = {
                "name": col_name,
                "type": self._map_data_type(data_type),
                "description": f"Column from {table}.{col_name}",
            }

            # Add primary key and checks for id column
            if col_name == "id":
                col_entry["primary_key"] = True
                col_entry["checks"] = [{"name": "unique"}, {"name": "not_null"}]
                col_entry["description"] = "UUID"

            # Add not_null check for created_at and updated_at
            elif col_name in ["created_at", "updated_at"]:
                col_entry["checks"] = [{"name": "not_null"}]
                col_entry["description"] = (
                    f"{col_name.replace('_', ' ').title()} datetime, with timezone precision, of the {table}"
                )

            # Special description for deleted_at
            elif col_name == "deleted_at":
                col_entry["description"] = (
                    f"Deleted datetime, with timezone precision, of the {table}"
                )

            yaml_metadata["columns"].append(col_entry)

        # Convert YAML to string, but without the document start/end markers
        import yaml

        yaml_str = yaml.dump(yaml_metadata, sort_keys=False, default_flow_style=False)

        # Sanitize table name to prevent SQL injection
        safe_table = self.sanitize_table_name(table)

        # Create the SQL file content with disabled Bandit warning
        # The SQL string looks like a potential SQL injection but is safe
        # because we sanitize the table name with sanitize_table_name()
        # nosec
        sql = f"""/* @bruin
{yaml_str}@bruin */

-- SQL injection is prevented by sanitizing the table name
select * from cronos_raw.{safe_table}
where deleted_at is null
"""
        return sql

    def _map_data_type(self, pg_type: str) -> str:
        """Map PostgreSQL data types to BigQuery types.

        Args:
            pg_type: PostgreSQL data type

        Returns:
            str: Corresponding BigQuery data type
        """
        type_mapping = {
            "integer": "bigint",
            "bigint": "bigint",
            "smallint": "bigint",
            "character varying": "text",
            "varchar": "text",
            "text": "text",
            "boolean": "boolean",
            "timestamp with time zone": "timestamp",
            "timestamp without time zone": "timestamp",
            "timestamp": "timestamp",
            "date": "date",
            "numeric": "float64",
            "decimal": "float64",
            "double precision": "float64",
            "real": "float64",
            "jsonb": "json",
            "json": "json",
        }

        for pg_prefix, bq_type in type_mapping.items():
            if pg_type.startswith(pg_prefix):
                return bq_type

        # Default to string if unknown
        return "text"

    def generate(self, **kwargs) -> bool:
        """Generate SQL files for all configured tables.

        Returns:
            bool: True if generation was successful
        """
        try:
            source_config = self.config["source"]
            schemas = source_config["schemas"]

            with DatabaseConnection(source_config["database"]) as db:
                for schema, schema_data in schemas.items():
                    table_list = schema_data.get("tables", [])

                    # Handle wildcard table selection
                    if "*" in table_list:
                        if table_list == ["*"]:
                            self.log_info(f"Fetching all tables in schema: {schema}")
                            table_list = db.fetch_all_tables(schema)
                        else:
                            dynamic_tables = db.fetch_all_tables(schema)
                            table_list = [t for t in table_list if t != "*"] + dynamic_tables

                    if not table_list:
                        self.log_info(f"No tables found in schema '{schema}', skipping.")
                        continue

                    # Process each table
                    for table in table_list:
                        self.log_info(f"Processing {schema}.{table}...")
                        columns = db.fetch_columns(schema, table)
                        if not columns:
                            self.log_error(f"No column metadata returned for {schema}.{table}")
                            continue

                        # Generate SQL transformation
                        sql_code = self.generate_sql_transformation(
                            columns=columns, schema=schema, table=table
                        )

                        # Write SQL file - using just table.sql as the file name
                        output_file = Path(self.output_folder) / f"{table}.sql"
                        self.log_info(f"Generating SQL file: {output_file}")

                        with open(output_file, "w") as f:
                            f.write(sql_code)
                        self.log_info(f"Generated SQL file: {output_file}")

            return True
        except Exception as e:
            self.log_error("Generation failed", e)
            return False
