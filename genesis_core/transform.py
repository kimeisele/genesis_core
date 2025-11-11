"""
Transform - Genesis Core Module

⚠️ FROZEN CORE MODULE ⚠️

This module is part of the Genesis Core and MUST NOT be modified.

Core Principle: Defines transformations between data structures.

If you need to:
- Add features → Create an extension in extensions/transform_extended.py
- Fix bugs → Create a wrapper in extensions/transform_patches.py
- Change behavior → Create an adapter in extensions/transform_adapters.py

DO NOT MODIFY THIS FILE.

Last Known Good State: 2025-11-11
"""

from typing import Callable
from dataclasses import dataclass

from . import entity as entity_module


@dataclass
class Transform:
    """Transform definition between schemas."""
    name: str
    from_schema: str
    to_schema: str
    logic: Callable[[entity_module.Entity], dict]


# Registry of all transforms
_transforms: dict[str, Transform] = {}


def define_transform(
    name: str,
    from_schema: str,
    to_schema: str,
    logic: Callable[[entity_module.Entity], dict]
) -> Transform:
    """
    Define named transformation between schemas.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        name: Unique transform name
        from_schema: Source schema name
        to_schema: Target schema name
        logic: Function that takes Entity and returns dict for new entity

    Returns:
        Transform: The defined transform

    Raises:
        KeyError: If transform name already exists
    """
    if name in _transforms:
        raise KeyError(f"Transform '{name}' already defined")

    transform = Transform(
        name=name,
        from_schema=from_schema,
        to_schema=to_schema,
        logic=logic
    )
    _transforms[name] = transform
    return transform


def apply_transform(entity: entity_module.Entity, transform_name: str) -> entity_module.Entity:
    """
    Apply transformation to entity.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        entity: Source entity
        transform_name: Name of transform to apply

    Returns:
        Entity: New entity with transformed data

    Raises:
        KeyError: If transform does not exist
        ValueError: If entity schema doesn't match transform source schema
    """
    transform = get_transform(transform_name)

    if entity.schema_name != transform.from_schema:
        raise ValueError(
            f"Entity schema '{entity.schema_name}' does not match "
            f"transform source schema '{transform.from_schema}'"
        )

    # Apply transformation logic
    new_data = transform.logic(entity)

    # Create new entity with target schema
    return entity_module.create_entity(transform.to_schema, new_data)


def get_transform(name: str) -> Transform:
    """
    Retrieve transform definition.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        name: Transform name

    Returns:
        Transform: The transform definition

    Raises:
        KeyError: If transform does not exist
    """
    if name not in _transforms:
        raise KeyError(f"Transform '{name}' not found")

    return _transforms[name]


def list_transforms() -> list[str]:
    """
    List all defined transforms.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Returns:
        list[str]: Sorted list of transform names
    """
    return sorted(_transforms.keys())
