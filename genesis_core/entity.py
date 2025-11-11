"""
Entity - Genesis Core Module

⚠️ FROZEN CORE MODULE ⚠️

This module is part of the Genesis Core and MUST NOT be modified.

Core Principle: Provides CRUD operations for schema-based entities.

If you need to:
- Add features → Create an extension in extensions/entity_extended.py
- Fix bugs → Create a wrapper in extensions/entity_patches.py
- Change behavior → Create an adapter in extensions/entity_adapters.py

DO NOT MODIFY THIS FILE.

Last Known Good State: 2025-11-11
"""

from typing import Any
from dataclasses import dataclass, field
import uuid

from . import schema


@dataclass
class Entity:
    """Entity with schema and data."""

    id: str
    schema_name: str
    data: dict[str, Any]


# Registry of all entities
_entities: dict[str, Entity] = {}


def create_entity(schema_name: str, data: dict) -> Entity:
    """
    Create new entity from schema and data.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        schema_name: Name of schema to use
        data: Entity data

    Returns:
        Entity: The created entity

    Raises:
        KeyError: If schema does not exist
        ValueError: If data does not validate against schema
    """
    # Validate against schema
    validation = schema.validate_data(schema_name, data)
    if not validation.is_valid:
        raise ValueError(f"Validation failed: {', '.join(validation.errors)}")

    # Create entity with unique ID
    entity_id = str(uuid.uuid4())
    entity = Entity(id=entity_id, schema_name=schema_name, data=data.copy())

    _entities[entity_id] = entity
    return entity


def get_entity(entity_id: str) -> Entity:
    """
    Retrieve entity by ID.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        entity_id: Entity ID

    Returns:
        Entity: The entity

    Raises:
        KeyError: If entity does not exist
    """
    if entity_id not in _entities:
        raise KeyError(f"Entity '{entity_id}' not found")

    return _entities[entity_id]


def update_entity(entity_id: str, updates: dict) -> Entity:
    """
    Update entity fields.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        entity_id: Entity ID
        updates: Dictionary of field updates

    Returns:
        Entity: The updated entity

    Raises:
        KeyError: If entity does not exist
        ValueError: If updates violate schema
    """
    entity = get_entity(entity_id)

    # Create updated data
    updated_data = entity.data.copy()
    updated_data.update(updates)

    # Validate updated data
    validation = schema.validate_data(entity.schema_name, updated_data)
    if not validation.is_valid:
        raise ValueError(f"Validation failed: {', '.join(validation.errors)}")

    # Apply updates
    entity.data = updated_data
    return entity


def delete_entity(entity_id: str) -> None:
    """
    Delete entity by ID.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        entity_id: Entity ID

    Returns:
        None

    Raises:
        KeyError: If entity does not exist
    """
    if entity_id not in _entities:
        raise KeyError(f"Entity '{entity_id}' not found")

    del _entities[entity_id]


def list_entities(schema_name: str = None) -> list[Entity]:
    """
    List entities, optionally filtered by schema.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        schema_name: Optional schema name to filter by

    Returns:
        list[Entity]: List of matching entities
    """
    if schema_name is None:
        return list(_entities.values())

    return [e for e in _entities.values() if e.schema_name == schema_name]
