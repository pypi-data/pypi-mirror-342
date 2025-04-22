# snowpack_stack/validator.py
import logging
import re

import yaml

logger = logging.getLogger(__name__)


def validate_config(config, allowed_values_file):
    """Validate configuration against allowed values from allowed_values.yaml."""
    try:
        with open(allowed_values_file, "r") as f:
            allowed = yaml.safe_load(f)
    except Exception as e:
        logger.error("Failed to load allowed values file: %s", e)
        raise

    errors = []

    # Validate source type
    source_type = config.get("source", {}).get("type", "")
    if source_type not in allowed.get("source", {}).get("allowed", []):
        errors.append(
            f"Invalid source type: {source_type}. Allowed: {allowed.get('source', {}).get('allowed', [])}"
        )

    # Validate ingestion
    ingestion = config.get("ingestion", "")
    if ingestion not in allowed.get("ingestion", {}).get("allowed", []):
        errors.append(
            f"Invalid ingestion value: {ingestion}. Allowed: {allowed.get('ingestion', {}).get('allowed', [])}"
        )

    # Validate transformer
    transformer = config.get("transformer", "")
    if transformer not in allowed.get("transformer", {}).get("allowed", []):
        errors.append(
            f"Invalid transformer value: {transformer}. Allowed: {allowed.get('transformer', {}).get('allowed', [])}"
        )

    # Validate destination type
    destination_type = config.get("destination", {}).get("type", "")
    allowed_dest = allowed.get("destination", {}).get("allowed", [])
    if destination_type not in allowed_dest:
        errors.append(
            f"Invalid destination type: {destination_type}. Allowed: {', '.join(allowed_dest)}"
        )

    # Validate etl_owner email
    etl_owner = config.get("etl_owner", "")
    email_regex = allowed.get("etl_owner", {}).get("regex", "")
    if not re.match(email_regex, etl_owner):
        errors.append(f"Invalid etl_owner email: {etl_owner}")

    # Validate required fields are present
    required_fields = {
        "source.connection_name": lambda c: c.get("source", {}).get("connection_name"),
        "source.database.user": lambda c: c.get("source", {}).get("database", {}).get("user"),
        "source.database.password": lambda c: c.get("source", {})
        .get("database", {})
        .get("password"),
        "source.database.database": lambda c: c.get("source", {})
        .get("database", {})
        .get("database"),
        "source.schemas": lambda c: c.get("source", {}).get("schemas"),
    }

    for field, getter in required_fields.items():
        if not getter(config):
            errors.append(f"Missing required field: {field}")

    if errors:
        for error in errors:
            logger.error("Validation Error: %s", error)
        raise ValueError("Configuration validation failed: " + "; ".join(errors))
    else:
        logger.info("Configuration validated successfully.")
