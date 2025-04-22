"""YAML generator for Bruin assets."""

import os
from pathlib import Path
from typing import Any, Dict, List, Tuple

from snowpack_stack.core.config import get_project_root
from snowpack_stack.generators.base import BaseGenerator
from snowpack_stack.utils.db import DatabaseConnection


class BruinYamlGenerator(BaseGenerator):
    """Generator for Bruin YAML asset files."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize the YAML generator.

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
                ("source.connection_name", lambda c: c.get("source", {}).get("connection_name")),
                ("source.database", lambda c: c.get("source", {}).get("database")),
                ("source.schemas", lambda c: c.get("source", {}).get("schemas")),
                ("destination.type", lambda c: c.get("destination", {}).get("type")),
            ]

            for field, getter in required_fields:
                if not getter(self.config):
                    self.log_error(f"Missing required field: {field}")
                    return False

            return True
        except Exception as e:
            self.log_error("Validation failed", e)
            return False

    def generate_yaml_data(
        self,
        columns: List[Tuple[str, str, str, str]],
        schema: str,
        table: str,
        owner: str,
        source_connection: str,
        destination: str,
    ) -> Dict[str, Any]:
        """Generate YAML dictionary for a table.

        Args:
            columns: List of column metadata tuples
            schema: Schema name
            table: Table name
            owner: ETL owner email
            source_connection: Source connection name
            destination: Destination type

        Returns:
            Dict[str, Any]: YAML data dictionary
        """
        yaml_dict = {
            "name": f"cronos_raw.{table}",
            "type": "ingestr",
            "owner": owner,
            "description": f"Raw, unaltered data from the {table} table in the database.",
            "materialization": {"type": "table"},
            "parameters": {
                "source_connection": source_connection,
                "source_table": f"{schema}.{table}",
                "destination": destination,
            },
            "columns": [],
        }

        for schema_name, table_name, col_name, data_type in columns:
            col_entry = {
                "name": col_name,
                "type": data_type,  # We'll handle type mapping in a separate module later
                "description": "",
            }
            if col_name == "id":
                col_entry["primary_key"] = True
                col_entry["checks"] = [{"name": "unique"}, {"name": "not_null"}]
            elif col_name in ["created_at", "updated_at"]:
                col_entry["checks"] = [{"name": "not_null"}]
            yaml_dict["columns"].append(col_entry)

        return yaml_dict

    def generate(self, **kwargs) -> bool:
        """Generate YAML files for all configured tables.

        Returns:
            bool: True if generation was successful
        """
        try:
            source_config = self.config["source"]
            schemas = source_config["schemas"]
            etl_owner = self.config["etl_owner"]
            source_connection = source_config["connection_name"]
            destination_type = self.config["destination"]["type"]

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

                        # Generate and write YAML
                        yaml_data = self.generate_yaml_data(
                            columns=columns,
                            schema=schema,
                            table=table,
                            owner=etl_owner,
                            source_connection=source_connection,
                            destination=destination_type,
                        )

                        output_file = Path(self.output_folder) / f"raw_{table}.asset.yml"
                        with open(output_file, "w") as f:
                            import yaml

                            yaml.dump(yaml_data, f, sort_keys=False, default_flow_style=False)
                        self.log_info(f"Generated YAML file: {output_file}")

            return True
        except Exception as e:
            self.log_error("Generation failed", e)
            return False
