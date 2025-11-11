"""
Storage - Genesis Core Module

⚠️ FROZEN CORE MODULE ⚠️

This module is part of the Genesis Core and MUST NOT be modified.

Core Principle: Provides neutral key-value storage without persistence specifics.

If you need to:
- Add features → Create an extension in extensions/storage_extended.py
- Fix bugs → Create a wrapper in extensions/storage_patches.py
- Change behavior → Create an adapter in extensions/storage_adapters.py

DO NOT MODIFY THIS FILE.

Last Known Good State: 2025-11-11
"""

from typing import Any


# In-memory storage (simplest implementation)
_storage: dict[str, Any] = {}


def store(key: str, data: Any) -> None:
    """
    Store data with unique key.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        key: Unique identifier for the data
        data: Any Python object

    Returns:
        None

    Raises:
        KeyError: If key already exists
    """
    if key in _storage:
        raise KeyError(f"Key '{key}' already exists")

    _storage[key] = data


def retrieve(key: str) -> Any:
    """
    Retrieve data by key.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        key: Unique identifier

    Returns:
        Any: The stored data

    Raises:
        KeyError: If key does not exist
    """
    if key not in _storage:
        raise KeyError(f"Key '{key}' not found")

    return _storage[key]


def exists(key: str) -> bool:
    """
    Check if key exists.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        key: Key to check

    Returns:
        bool: True if key exists, False otherwise
    """
    return key in _storage


def delete(key: str) -> None:
    """
    Delete data by key.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        key: Key to delete

    Returns:
        None

    Raises:
        KeyError: If key does not exist
    """
    if key not in _storage:
        raise KeyError(f"Key '{key}' not found")

    del _storage[key]


def list_keys(prefix: str = "") -> list[str]:
    """
    List all keys with optional prefix filter.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        prefix: Optional prefix to filter keys (default: "")

    Returns:
        list[str]: Sorted list of matching keys
    """
    if prefix:
        return sorted([k for k in _storage.keys() if k.startswith(prefix)])
    return sorted(_storage.keys())
