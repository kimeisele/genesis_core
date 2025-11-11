"""
Schema - Genesis Core Module

⚠️ FROZEN CORE MODULE ⚠️

This module is part of the Genesis Core and MUST NOT be modified.

Core Principle: Defines data structures and validates them without domain logic.

If you need to:
- Add features → Create an extension in extensions/schema_extended.py
- Fix bugs → Create a wrapper in extensions/schema_patches.py
- Change behavior → Create an adapter in extensions/schema_adapters.py

DO NOT MODIFY THIS FILE.

Last Known Good State: 2025-11-11
"""

from typing import Any
from dataclasses import dataclass


@dataclass
class Schema:
    """Schema definition with typed fields."""
    name: str
    fields: dict[str, type]


@dataclass
class ValidationResult:
    """Result of schema validation."""
    is_valid: bool
    errors: list[str]


# Registry of all defined schemas
_schemas: dict[str, Schema] = {}


def define_schema(name: str, fields: dict[str, type]) -> Schema:
    """
    Define a named schema with typed fields.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        name: Unique schema name
        fields: Dictionary mapping field names to Python types

    Returns:
        Schema: The defined schema

    Raises:
        KeyError: If schema name already exists
    """
    if name in _schemas:
        raise KeyError(f"Schema '{name}' already defined")

    schema = Schema(name=name, fields=fields)
    _schemas[name] = schema
    return schema


def get_schema(name: str) -> Schema:
    """
    Retrieve schema definition by name.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        name: Schema name

    Returns:
        Schema: The schema definition

    Raises:
        KeyError: If schema does not exist
    """
    if name not in _schemas:
        raise KeyError(f"Schema '{name}' not found")

    return _schemas[name]


def validate_data(schema_name: str, data: dict) -> ValidationResult:
    """
    Validate data against schema.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        schema_name: Name of schema to validate against
        data: Dictionary to validate

    Returns:
        ValidationResult: Validation result with errors if any

    Raises:
        KeyError: If schema does not exist
    """
    schema = get_schema(schema_name)
    errors = []

    # Check for missing fields
    for field_name, field_type in schema.fields.items():
        if field_name not in data:
            errors.append(f"Missing required field: {field_name}")
            continue

        # Check type
        value = data[field_name]
        if not isinstance(value, field_type):
            errors.append(
                f"Field '{field_name}' has wrong type: "
                f"expected {field_type.__name__}, got {type(value).__name__}"
            )

    # Check for extra fields
    for field_name in data.keys():
        if field_name not in schema.fields:
            errors.append(f"Unexpected field: {field_name}")

    return ValidationResult(is_valid=len(errors) == 0, errors=errors)


def list_schemas() -> list[str]:
    """
    List all defined schema names.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Returns:
        list[str]: Sorted list of schema names
    """
    return sorted(_schemas.keys())
