# Genesis Core - Module Specification

**Version:** 1.0.0
**Status:** FROZEN
**Last Modified:** 2025-11-11

## Core Philosophy

Genesis Core consists of **8 fundamental, immutable modules** that provide the deepest abstractions for information processing. These modules are:

- **Neutral** - No domain-specific logic
- **Minimal** - Simplest possible implementation
- **Eternal** - Never modified after freeze
- **Complete** - Sufficient to build any application through extensions

## Module Definitions

### 1. core.io - File Operations

**Purpose:** Neutral file system I/O operations

**Frozen Functions:**

```python
def read_text(path: Path) -> str:
    """Read text file content"""

def write_text(path: Path, content: str) -> None:
    """Write text to file"""

def read_json(path: Path) -> dict:
    """Read and parse JSON file"""

def write_json(path: Path, data: dict) -> None:
    """Write dict as JSON file"""

def exists(path: Path) -> bool:
    """Check if path exists"""

def list_files(directory: Path, pattern: str = "*") -> list[Path]:
    """List files matching pattern"""
```

---

### 2. core.storage - Generic Data Persistence

**Purpose:** Key-value storage abstraction for arbitrary data

**Frozen Functions:**

```python
def store(key: str, data: Any) -> None:
    """Store data with unique key"""

def retrieve(key: str) -> Any:
    """Retrieve data by key"""

def exists(key: str) -> bool:
    """Check if key exists"""

def delete(key: str) -> None:
    """Delete data by key"""

def list_keys(prefix: str = "") -> list[str]:
    """List all keys with optional prefix filter"""
```

---

### 3. core.schema - Data Structure Definition

**Purpose:** Define and validate data structures

**Frozen Functions:**

```python
def define_schema(name: str, fields: dict[str, type]) -> Schema:
    """Define a named schema with typed fields"""

def get_schema(name: str) -> Schema:
    """Retrieve schema definition by name"""

def validate_data(schema_name: str, data: dict) -> ValidationResult:
    """Validate data against schema"""

def list_schemas() -> list[str]:
    """List all defined schema names"""
```

---

### 4. core.entity - Generic Entity Handling

**Purpose:** CRUD operations for schema-based entities

**Frozen Functions:**

```python
def create_entity(schema_name: str, data: dict) -> Entity:
    """Create new entity from schema and data"""

def get_entity(entity_id: str) -> Entity:
    """Retrieve entity by ID"""

def update_entity(entity_id: str, updates: dict) -> Entity:
    """Update entity fields"""

def delete_entity(entity_id: str) -> None:
    """Delete entity by ID"""

def list_entities(schema_name: str = None) -> list[Entity]:
    """List entities, optionally filtered by schema"""
```

---

### 5. core.transform - Data Transformation

**Purpose:** Define and apply transformations between data structures

**Frozen Functions:**

```python
def define_transform(name: str, from_schema: str, to_schema: str, logic: Callable) -> Transform:
    """Define named transformation between schemas"""

def apply_transform(entity: Entity, transform_name: str) -> Entity:
    """Apply transformation to entity"""

def get_transform(name: str) -> Transform:
    """Retrieve transform definition"""

def list_transforms() -> list[str]:
    """List all defined transforms"""
```

---

### 6. core.process - Workflow/State Machine

**Purpose:** Define and execute multi-step processes

**Frozen Functions:**

```python
def define_process(name: str, steps: list[str]) -> Process:
    """Define named process with ordered steps"""

def execute_process(process_name: str, entity: Entity) -> Entity:
    """Execute process on entity"""

def get_process(name: str) -> Process:
    """Retrieve process definition"""

def list_processes() -> list[str]:
    """List all defined processes"""
```

---

### 7. core.validation - Rule Engine

**Purpose:** Define and apply validation rules

**Frozen Functions:**

```python
def define_rule(name: str, condition: Callable[[Entity], bool]) -> Rule:
    """Define named validation rule"""

def validate(entity: Entity, rules: list[str]) -> ValidationResult:
    """Validate entity against list of rules"""

def get_rule(name: str) -> Rule:
    """Retrieve rule definition"""

def list_rules() -> list[str]:
    """List all defined rules"""
```

---

### 8. core.identity - Subject/Permission

**Purpose:** Authentication and authorization primitives

**Frozen Functions:**

```python
def create_subject(subject_id: str, attributes: dict) -> Subject:
    """Create subject (user/service) with attributes"""

def get_subject(subject_id: str) -> Subject:
    """Retrieve subject by ID"""

def grant_permission(subject_id: str, action: str, resource_pattern: str) -> None:
    """Grant permission to subject"""

def check_permission(subject_id: str, action: str, resource_id: str) -> bool:
    """Check if subject has permission"""

def list_permissions(subject_id: str) -> list[Permission]:
    """List all permissions for subject"""
```

---

## Extension Policy

### ⚠️ CORE MODULES ARE FROZEN ⚠️

**Never modify core modules.** Instead:

1. **Wrap** - Create wrappers in `extensions/` that call core functions
2. **Extend** - Add new functionality by combining core primitives
3. **Adapt** - Create adapters for external systems

### Examples:

❌ **FORBIDDEN:**
```python
# Modifying core/storage.py to add S3 support
def store_to_s3(key: str, data: Any) -> None:  # DON'T ADD THIS TO CORE
    ...
```

✅ **CORRECT:**
```python
# extensions/storage_s3.py
from genesis_core import storage as core_storage

def store(key: str, data: Any) -> None:
    """Extended store that saves to S3"""
    core_storage.store(key, data)  # Use core
    _upload_to_s3(key, data)  # Add S3 logic
```

---

## Success Metrics

The Genesis Core is successful if:

1. ✅ All 8 modules are **independently usable**
2. ✅ **Zero domain logic** in core (no "user", "product", "order" concepts)
3. ✅ **Any application** can be built using only extensions
4. ✅ Core remains **unchanged** for 1+ years
5. ✅ New developers **never need to modify core**

---

## Freeze Date

**Frozen on:** 2025-11-11
**Modification Policy:** Only security/critical bugs allowed with approval

---

*This specification defines the eternal contract of Genesis Core.*
