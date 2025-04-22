# snowpack_stack/main.py

import logging
import sys
from pathlib import Path

import yaml

from snowpack_stack.config_loader import find_config_file, get_project_root, load_config
from snowpack_stack.source_handler import get_source_handler
from snowpack_stack.transformer import get_transformer
from snowpack_stack.validator import validate_config


def setup_logging():
    """Set up logging with both console and file output."""
    # Create logs directory in the project root
    project_root = get_project_root()
    log_dir = project_root / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    # Configure logging
    log_file = log_dir / "snowpack_stack.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler(str(log_file))],
    )
    return logging.getLogger(__name__)


def write_yaml_file(yaml_data, output_file):
    """Write the YAML dictionary to a file."""
    try:
        # Ensure the directory exists
        output_dir = Path(output_file).parent
        output_dir.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w") as f:
            yaml.dump(yaml_data, f, sort_keys=False, default_flow_style=False)
    except Exception as e:
        logger.error("Error writing YAML file: %s", e)
        raise


def main():
    # Set up logging first
    global logger
    logger = setup_logging()

    try:
        # 1. Find and load configuration files
        config_file = find_config_file("autogen_config.yaml")
        allowed_values_file = find_config_file("allowed_values.yaml")

        logger.info("Using config file: %s", config_file)
        logger.info("Using allowed values file: %s", allowed_values_file)

        # 2. Load configuration
        try:
            config = load_config(config_file)
        except Exception as e:
            logger.error("Error loading configuration: %s", e)
            sys.exit(1)

        # 3. Validate configuration
        try:
            validate_config(config, allowed_values_file)
        except Exception as e:
            logger.error("Configuration validation failed: %s", e)
            sys.exit(1)

        # 4. Initialize source handler
        source_type = config["source"]["type"]
        source_db_config = config["source"]["database"]
        try:
            source_handler = get_source_handler(source_type, source_db_config)
        except Exception as e:
            logger.error("Failed to create source handler: %s", e)
            sys.exit(1)

        # 5. Initialize transformer object
        transformer_type = config["transformer"]
        try:
            transformer_obj = get_transformer(transformer_type)
        except Exception as e:
            logger.error("Failed to get transformer: %s", e)
            sys.exit(1)

        # 6. Get destination information
        destination_type = config["destination"]["type"]
        destination_config = config["destination"].get("connection", {})
        logger.info("Destination: %s, Connection Config: %s", destination_type, destination_config)

        # 7. Define and create output folder from transformer object
        output_folder = Path(transformer_obj.output_folder)
        output_folder.mkdir(parents=True, exist_ok=True)
        logger.info("Using output folder: %s", output_folder)

        # 8. Get schema and tables to process
        schemas = config["source"]["schemas"]
        etl_owner = config["etl_owner"]
        source_connection = config["source"]["connection_name"]

        # 9. Process each schema and its tables
        for schema, schema_data in schemas.items():
            table_list = schema_data.get("tables", [])
            # If "*" is present, dynamically fetch all tables
            if "*" in table_list:
                if table_list == ["*"]:
                    logger.info("Fetching all tables in schema: %s", schema)
                    table_list = source_handler.fetch_all_tables(schema)
                else:
                    dynamic_tables = source_handler.fetch_all_tables(schema)
                    table_list = [t for t in table_list if t != "*"] + dynamic_tables

            if not table_list:
                logger.warning("No tables found or accessible in schema '%s', skipping.", schema)
                continue

            # Process each table
            for table in table_list:
                logger.info("Processing %s.%s...", schema, table)
                try:
                    columns = source_handler.fetch_columns(schema, table)
                    if not columns:
                        logger.warning(
                            "No column metadata returned for %s.%s. Skipping.", schema, table
                        )
                        continue
                except Exception as e:
                    logger.error("Failed to fetch metadata for %s.%s: %s", schema, table, e)
                    continue

                # Generate YAML metadata using the transformer
                try:
                    yaml_data = transformer_obj.generate_ingestr_yaml(
                        columns=columns,
                        schema=schema,
                        table=table,
                        owner=etl_owner,
                        source_connection=source_connection,
                        destination=destination_type,
                    )
                except Exception as e:
                    logger.error("Failed to generate YAML data for %s.%s: %s", schema, table, e)
                    continue

                # Write YAML file
                output_yaml_path = output_folder / f"raw_{table}.asset.yml"
                try:
                    write_yaml_file(yaml_data, str(output_yaml_path))
                    logger.info("YAML metadata file '%s' generated successfully.", output_yaml_path)
                except Exception as e:
                    logger.error("Failed to write YAML file for %s.%s: %s", schema, table, e)
                    continue

    except Exception as e:
        logger.error("An unexpected error occurred: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
