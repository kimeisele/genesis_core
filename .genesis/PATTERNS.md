# Genesis Core Patterns

**For AI Assistants: These are the coding patterns to follow when working on this codebase.**

## Module Structure Pattern

Every Python module should follow this structure:

```python
"""
Module docstring - one line summary.

Detailed explanation of what this module does.

Examples:
    >>> # Show typical usage
    >>> result = main_function(input_data)
    >>> print(result)
"""

from typing import Dict, Any, List, Optional
# Stdlib imports only in genesis_core/
# Group imports: stdlib, third-party, local

# Module-level constants (if needed)
DEFAULT_VALUE = "default"

# Public functions (the module's API)
def public_function(param: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clear one-line summary.

    Detailed explanation of what this function does.

    Args:
        param: Description of the parameter

    Returns:
        Description of what is returned

    Raises:
        ValueError: When validation fails

    Example:
        >>> public_function({"key": "value"})
        {"result": "processed"}
    """
    # Implementation here
    result = _private_helper(param)
    return result


# Private functions (internal helpers)
def _private_helper(data: Dict[str, Any]) -> Dict[str, Any]:
    """Private helper - not part of public API."""
    # Implementation
    return data
```

## Function Signature Pattern

**Preferred pattern for new functions:**

```python
def process_data(input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process input data and return result.

    This pattern makes it easy for AI to chain functions together.
    Dict in, Dict out = composable.
    """
    return {"result": "processed"}
```

**Why Dict -> Dict?**
- Easy to extend without breaking signatures
- Clear for AI assistants to understand
- Composable (output of one = input of another)

## Docstring Pattern

Every public function must have:

1. **One-line summary** (what it does)
2. **Args section** (describe each parameter)
3. **Returns section** (what it returns)
4. **Example** (show how to use it)
5. **Raises** (optional, if it raises exceptions)

```python
def example(data: Dict) -> Dict:
    """
    One-line summary of what it does.

    Longer explanation if needed.
    Can span multiple lines.

    Args:
        data: What this parameter represents

    Returns:
        What the function returns

    Raises:
        ValueError: When this happens

    Example:
        >>> example({"input": "test"})
        {"output": "result"}
    """
    pass
```

## Error Handling Pattern

```python
def validate_input(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate input data.

    Fail fast with clear error messages.
    """
    if not isinstance(data, dict):
        raise TypeError(f"Expected dict, got {type(data).__name__}")

    if "required_field" not in data:
        raise ValueError("Missing required field: 'required_field'")

    return {"valid": True, "data": data}
```

**Pattern: Fail fast with clear errors**
- Use explicit type checks
- Raise exceptions with helpful messages
- Don't hide errors with try/except unless necessary

## Testing Pattern

Every module should have corresponding tests:

```python
# tests/test_my_module.py
"""Tests for my_module."""

import pytest
from genesis_core import my_module


def test_basic_functionality():
    """Test the basic use case."""
    result = my_module.process_data({"input": "test"})
    assert result["status"] == "success"


def test_error_case():
    """Test error handling."""
    with pytest.raises(ValueError):
        my_module.process_data({})  # Missing required field
```

## Import Pattern

**In genesis_core/ (core modules):**
```python
# ONLY stdlib imports
from typing import Dict, Any, List
from pathlib import Path
import json
```

**In examples/ or user projects:**
```python
# Can import anything
from genesis_core import entity, schema, storage
import requests  # External deps OK here
import pandas as pd
```

## Extension Pattern

**How to extend core without modifying it:**

```python
# examples/my_extension/storage_extended.py
"""Extended storage with database persistence."""

from genesis_core import storage as core_storage
import sqlite3

def store(key: str, data: dict) -> None:
    """
    Store data with both in-memory and database persistence.

    This extends core storage without modifying it.
    """
    # Use core functionality
    core_storage.store(key, data)

    # Add our extension (database)
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO storage (key, data) VALUES (?, ?)",
        (key, json.dumps(data))
    )
    conn.commit()
    conn.close()
```

**Pattern: Wrap, don't replace**
- Import core functionality
- Call core functions
- Add your extension on top
- Never modify core files

## Schema Definition Pattern

```python
from genesis_core import schema

# Define schemas at module level or in setup function
USER_SCHEMA = schema.define_schema("User", {
    "name": str,
    "email": str,
    "age": int
})

def setup_schemas():
    """Define all schemas for this domain."""
    schema.define_schema("Product", {
        "id": str,
        "name": str,
        "price": float
    })

    schema.define_schema("Order", {
        "product_id": str,
        "quantity": int,
        "status": str
    })
```

## Process/Workflow Pattern

```python
from genesis_core import process

# Define step handlers
def validate_step(entity):
    """Validate the entity."""
    # Validation logic
    return entity

def approve_step(entity):
    """Approve the entity."""
    # Approval logic
    return entity

# Register handlers
process.register_step_handler("validate", validate_step)
process.register_step_handler("approve", approve_step)

# Define process
workflow = process.define_process("approval_workflow", [
    "validate",
    "approve"
])

# Execute
result = process.execute_process("approval_workflow", my_entity)
```

## Do's and Don'ts

### ✅ DO

- Follow existing patterns in the codebase
- Copy templates from `.genesis/templates/`
- Write clear docstrings with examples
- Use type hints (`Dict[str, Any]`, etc.)
- Ask the user if unsure about core changes
- Run `pytest tests/test_consistency.py` before committing

### ❌ DON'T

- Modify core without asking user first
- Add external dependencies to `genesis_core/`
- Skip docstrings on public functions
- Use complex or clever code (keep it simple)
- Ignore test failures
- Assume what the user wants (ask!)

## When to Create New Modules

**Create in `genesis_core/` only if:**
- It's a fundamental capability needed by many extensions
- It has zero external dependencies
- User explicitly approves it

**Create in `examples/` if:**
- It's domain-specific (e.g., "recruiting", "e-commerce")
- It's an extension of core
- It demonstrates a pattern

**Create in user's project if:**
- It's for one specific use case
- It needs external dependencies
- It's experimental

## Summary

The key principle: **Follow existing patterns, don't invent new ones.**

When in doubt:
1. Look at existing code in `genesis_core/`
2. Look at examples in `examples/`
3. Check this patterns file
4. Ask the user

Keep it simple. Keep it consistent. Keep the flow.
