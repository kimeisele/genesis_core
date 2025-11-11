"""
IO - Genesis Core Module

⚠️ FROZEN CORE MODULE ⚠️

This module is part of the Genesis Core and MUST NOT be modified.

Core Principle: Provides neutral file system I/O operations without domain logic.

If you need to:
- Add features → Create an extension in extensions/io_extended.py
- Fix bugs → Create a wrapper in extensions/io_patches.py
- Change behavior → Create an adapter in extensions/io_adapters.py

DO NOT MODIFY THIS FILE.

Last Known Good State: 2025-11-11
"""

from pathlib import Path
from typing import Any
import json


def read_text(path: Path) -> str:
    """
    Read text file content.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        path: Path to text file

    Returns:
        str: File content

    Raises:
        FileNotFoundError: If file does not exist
        IOError: If file cannot be read
    """
    return Path(path).read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    """
    Write text to file.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        path: Path to write to
        content: Text content to write

    Returns:
        None

    Raises:
        IOError: If file cannot be written
    """
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(content, encoding="utf-8")


def read_json(path: Path) -> dict:
    """
    Read and parse JSON file.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        path: Path to JSON file

    Returns:
        dict: Parsed JSON data

    Raises:
        FileNotFoundError: If file does not exist
        json.JSONDecodeError: If file is not valid JSON
    """
    content = read_text(path)
    return json.loads(content)


def write_json(path: Path, data: dict) -> None:
    """
    Write dict as JSON file.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        path: Path to write to
        data: Dictionary to serialize as JSON

    Returns:
        None

    Raises:
        IOError: If file cannot be written
        TypeError: If data is not JSON serializable
    """
    content = json.dumps(data, indent=2, ensure_ascii=False)
    write_text(path, content)


def exists(path: Path) -> bool:
    """
    Check if path exists.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        path: Path to check

    Returns:
        bool: True if path exists, False otherwise
    """
    return Path(path).exists()


def list_files(directory: Path, pattern: str = "*") -> list[Path]:
    """
    List files matching pattern in directory.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        directory: Directory to search
        pattern: Glob pattern (default: "*")

    Returns:
        list[Path]: List of matching file paths

    Raises:
        NotADirectoryError: If directory is not a directory
    """
    dir_path = Path(directory)
    if not dir_path.is_dir():
        raise NotADirectoryError(f"{directory} is not a directory")

    return sorted(dir_path.glob(pattern))
