# snowpack_stack/transformer.py
import logging
import os

from snowpack_stack.config_loader import get_project_root
from snowpack_stack.type_mapper import map_db_type

logger = logging.getLogger(__name__)


class BaseTransformer:
    def __init__(self):
        pass

    def generate_ingestr_yaml(self, columns, schema, table, owner, source_connection, destination):
        raise NotImplementedError


class BruinTransformer(BaseTransformer):
    def __init__(self):
        # For transformer "bruin", define output folder relative to project root
        project_root = get_project_root()

        # The output folder should always be in bruin-pipeline/assets
        self.output_folder = str(project_root / "bruin-pipeline" / "assets")
        logger.info("Using output folder: %s", self.output_folder)

        # Ensure the output directory exists
        os.makedirs(self.output_folder, exist_ok=True)

    def generate_ingestr_yaml(self, columns, schema, table, owner, source_connection, destination):
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
        for row in columns:
            _, _, col_name, data_type = row
            mapped_type = map_db_type(source_connection, data_type, destination)
            col_entry = {"name": col_name, "type": mapped_type, "description": ""}
            if col_name == "id":
                col_entry["primary_key"] = True
                col_entry["checks"] = [{"name": "unique"}, {"name": "not_null"}]
            elif col_name in ["created_at", "updated_at"]:
                col_entry["checks"] = [{"name": "not_null"}]
            yaml_dict["columns"].append(col_entry)
        return yaml_dict


def get_transformer(transformer_type):
    """Factory function to return a transformer object based on transformer type."""
    if transformer_type.lower() == "bruin":
        return BruinTransformer()
    else:
        raise ValueError(f"Unsupported transformer type: {transformer_type}")
