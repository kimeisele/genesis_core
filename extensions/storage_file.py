"""
File-based Storage Extension

Wraps genesis_core.storage to persist data to disk.

This extension demonstrates the power of the frozen core architecture:
- It NEVER modifies core.storage
- It wraps core functions with file persistence
- It can be replaced with storage_s3.py or storage_db.py without any core changes
"""

from genesis_core import storage as core_storage
from pathlib import Path
import pickle
from typing import Any


# Configuration
STORAGE_DIR = Path("./data/storage")
STORAGE_DIR.mkdir(parents=True, exist_ok=True)


def _get_file_path(key: str) -> Path:
    """Get file path for a key."""
    # Sanitize key for filesystem
    safe_key = key.replace("/", "_").replace(":", "_")
    return STORAGE_DIR / f"{safe_key}.pkl"


def store(key: str, data: Any) -> None:
    """
    Extended store that saves to file.

    This wraps core.storage.store and adds file persistence.

    Args:
        key: Unique identifier for the data
        data: Any pickleable Python object

    Returns:
        None

    Raises:
        KeyError: If key already exists
    """
    # First, use core storage (for memory cache)
    core_storage.store(key, data)

    # Then persist to disk
    file_path = _get_file_path(key)
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)

    print(f"[storage_file] Persisted '{key}' to {file_path}")


def retrieve(key: str) -> Any:
    """
    Extended retrieve that loads from file if not in memory.

    This wraps core.storage.retrieve with file fallback.

    Args:
        key: Unique identifier

    Returns:
        Any: The stored data

    Raises:
        KeyError: If key does not exist
    """
    # Try core storage first (memory cache)
    try:
        return core_storage.retrieve(key)
    except KeyError:
        pass

    # Load from disk
    file_path = _get_file_path(key)
    if not file_path.exists():
        raise KeyError(f"Key '{key}' not found in storage or disk")

    with open(file_path, 'rb') as f:
        data = pickle.load(f)

    # Populate memory cache
    # We need to bypass the "already exists" check, so we'll directly set it
    core_storage._storage[key] = data

    print(f"[storage_file] Loaded '{key}' from {file_path}")
    return data


def exists(key: str) -> bool:
    """
    Check if key exists in memory or on disk.

    Args:
        key: Key to check

    Returns:
        bool: True if key exists, False otherwise
    """
    # Check memory first
    if core_storage.exists(key):
        return True

    # Check disk
    file_path = _get_file_path(key)
    return file_path.exists()


def delete(key: str) -> None:
    """
    Delete from memory and disk.

    Args:
        key: Key to delete

    Returns:
        None

    Raises:
        KeyError: If key does not exist
    """
    # Delete from memory
    if core_storage.exists(key):
        core_storage.delete(key)

    # Delete from disk
    file_path = _get_file_path(key)
    if file_path.exists():
        file_path.unlink()
        print(f"[storage_file] Deleted '{key}' from disk")
    else:
        raise KeyError(f"Key '{key}' not found")


def list_keys(prefix: str = "") -> list[str]:
    """
    List all keys from memory and disk.

    Args:
        prefix: Optional prefix to filter keys

    Returns:
        list[str]: Sorted list of matching keys
    """
    # Get keys from memory
    memory_keys = set(core_storage.list_keys(prefix))

    # Get keys from disk
    disk_keys = set()
    for file_path in STORAGE_DIR.glob("*.pkl"):
        key = file_path.stem.replace("_", ":")
        if not prefix or key.startswith(prefix):
            disk_keys.add(key)

    # Combine and return
    all_keys = memory_keys | disk_keys
    if prefix:
        return sorted([k for k in all_keys if k.startswith(prefix)])
    return sorted(all_keys)
