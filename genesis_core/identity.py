"""
Identity - Genesis Core Module

⚠️ FROZEN CORE MODULE ⚠️

This module is part of the Genesis Core and MUST NOT be modified.

Core Principle: Provides authentication and authorization primitives.

If you need to:
- Add features → Create an extension in extensions/identity_extended.py
- Fix bugs → Create a wrapper in extensions/identity_patches.py
- Change behavior → Create an adapter in extensions/identity_adapters.py

DO NOT MODIFY THIS FILE.

Last Known Good State: 2025-11-11
"""

from typing import Any
from dataclasses import dataclass, field
import fnmatch


@dataclass
class Subject:
    """Subject (user/service) with attributes."""

    id: str
    attributes: dict[str, Any]


@dataclass
class Permission:
    """Permission definition."""

    action: str
    resource_pattern: str


# Registry of subjects
_subjects: dict[str, Subject] = {}

# Registry of permissions per subject
_permissions: dict[str, list[Permission]] = {}


def create_subject(subject_id: str, attributes: dict) -> Subject:
    """
    Create subject (user/service) with attributes.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        subject_id: Unique subject identifier
        attributes: Subject attributes (e.g., name, email, roles)

    Returns:
        Subject: The created subject

    Raises:
        KeyError: If subject ID already exists
    """
    if subject_id in _subjects:
        raise KeyError(f"Subject '{subject_id}' already exists")

    subject = Subject(id=subject_id, attributes=attributes.copy())
    _subjects[subject_id] = subject
    _permissions[subject_id] = []

    return subject


def get_subject(subject_id: str) -> Subject:
    """
    Retrieve subject by ID.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        subject_id: Subject ID

    Returns:
        Subject: The subject

    Raises:
        KeyError: If subject does not exist
    """
    if subject_id not in _subjects:
        raise KeyError(f"Subject '{subject_id}' not found")

    return _subjects[subject_id]


def grant_permission(subject_id: str, action: str, resource_pattern: str) -> None:
    """
    Grant permission to subject.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        subject_id: Subject ID
        action: Action name (e.g., "read", "write", "delete")
        resource_pattern: Resource pattern with wildcards (e.g., "doc:*", "user:123")

    Returns:
        None

    Raises:
        KeyError: If subject does not exist
    """
    if subject_id not in _subjects:
        raise KeyError(f"Subject '{subject_id}' not found")

    permission = Permission(action=action, resource_pattern=resource_pattern)
    _permissions[subject_id].append(permission)


def check_permission(subject_id: str, action: str, resource_id: str) -> bool:
    """
    Check if subject has permission.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        subject_id: Subject ID
        action: Action to check
        resource_id: Specific resource ID

    Returns:
        bool: True if permission granted, False otherwise

    Raises:
        KeyError: If subject does not exist
    """
    if subject_id not in _subjects:
        raise KeyError(f"Subject '{subject_id}' not found")

    # Check each permission for match
    for permission in _permissions[subject_id]:
        if permission.action == action:
            # Use fnmatch for wildcard pattern matching
            if fnmatch.fnmatch(resource_id, permission.resource_pattern):
                return True

    return False


def list_permissions(subject_id: str) -> list[Permission]:
    """
    List all permissions for subject.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        subject_id: Subject ID

    Returns:
        list[Permission]: List of permissions

    Raises:
        KeyError: If subject does not exist
    """
    if subject_id not in _subjects:
        raise KeyError(f"Subject '{subject_id}' not found")

    return _permissions[subject_id].copy()
