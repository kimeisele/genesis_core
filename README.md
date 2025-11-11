# Genesis Core

**A frozen core architecture for building unbreakable systems.**

Version: 1.0.0 | Status: FROZEN | Date: 2025-11-11

---

## The Problem

Modern codebases break constantly because AI agents and developers lack system understanding. Every "small change" cascades into unexpected failures. Dependencies shift, modules couple, and stability becomes impossible.

**We needed a different approach.**

## The Solution: Frozen Core

Genesis Core is a set of **8 fundamental, immutable modules** that serve as eternal building blocks for any application. These modules are:

- **Frozen** - Never modified after initial release
- **Neutral** - No domain-specific logic
- **Minimal** - Simplest possible implementation
- **Complete** - Sufficient to build any application through extensions

**Key Insight:** The core never changes. All features are added through extensions that wrap the core, never modify it.

---

## Installation

### From PyPI (Recommended)

```bash
pip install genesis-core
```

### From Source

```bash
git clone https://github.com/yourusername/genesis-core.git
cd genesis-core
pip install -e .
```

### Requirements

- Python 3.10+
- **Zero runtime dependencies** (pure stdlib)

## Architecture

```
genesis-core/               # PyPI Package
├── genesis_core/           # FROZEN CORE (never modify)
│   ├── __init__.py
│   ├── io.py              # File operations
│   ├── storage.py         # Key-value storage
│   ├── schema.py          # Data structure definitions
│   ├── entity.py          # CRUD operations
│   ├── transform.py       # Data transformations
│   ├── process.py         # Workflows/state machines
│   ├── validation.py      # Rule engine
│   └── identity.py        # Auth/permissions
│
├── tests/                 # Test suite
│   ├── test_core_modules.py
│   └── test_frozen_integrity.py
│
├── scripts/
│   └── verify_frozen.py   # Core integrity checker
│
├── setup.py               # Package configuration
├── pyproject.toml         # Modern Python packaging
├── GENESIS_CORE_SPEC.md   # Module specifications
├── FROZEN_MANIFEST.md     # Freeze enforcement
└── README.md              # This file

# Your Project (uses genesis-core)
my_project/
├── requirements.txt       # genesis-core==1.0.0
├── my_app/
│   ├── models.py         # from genesis_core import entity, schema
│   └── storage.py        # from genesis_core import storage
└── extensions/           # Your custom extensions
```

---

## Installation

### Option 1: Install from PyPI (Recommended)

```bash
pip install genesis-core
```

### Option 2: Install from GitHub

```bash
pip install git+https://github.com/kimeisele/genesis_core.git
```

### Option 3: Install from Source

```bash
git clone https://github.com/kimeisele/genesis_core.git
cd genesis_core
pip install -e .
```

Genesis Core has **zero external dependencies**. Pure Python stdlib.

---

## Quick Start

### 1. Import and Use

```python
from genesis_core import entity, schema, storage

# Define a schema
user_schema = schema.define_schema("User", {
    "name": str,
    "email": str,
    "age": int
})

# Create an entity
user = entity.create_entity("User", {
    "name": "Alice",
    "email": "alice@example.com",
    "age": 30
})

# Store it
storage.store(f"user:{user.id}", user)

print(f"Created user: {user.id}")
```

### 2. Run Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Verify frozen contract
python scripts/verify_frozen.py
```

### 4. Build Your Extensions

```python
# my_app/storage_extended.py
from genesis_core import storage as core_storage
import json
from pathlib import Path

def store_to_file(key: str, data: dict):
    """Extended storage with file persistence"""
    # Use core storage
    core_storage.store(key, data)

    # Add file persistence
    Path("data").mkdir(exist_ok=True)
    with open(f"data/{key}.json", "w") as f:
        json.dump(data, f)
```

---

## Core Modules

### 1. `core.io` - File Operations

```python
from genesis_core import io
from pathlib import Path

# Read/write text
content = io.read_text(Path("file.txt"))
io.write_text(Path("output.txt"), content)

# JSON operations
data = io.read_json(Path("data.json"))
io.write_json(Path("result.json"), {"key": "value"})
```

### 2. `core.storage` - Key-Value Storage

```python
from genesis_core import storage

# Store and retrieve
storage.store("user:123", {"name": "Alice"})
user = storage.retrieve("user:123")

# Check existence
if storage.exists("user:123"):
    storage.delete("user:123")
```

### 3. `core.schema` - Data Structures

```python
from genesis_core import schema

# Define schema
user_schema = schema.define_schema("User", {
    "name": str,
    "email": str,
    "age": int
})

# Validate data
result = schema.validate_data("User", {
    "name": "Bob",
    "email": "bob@example.com",
    "age": 30
})

print(result.is_valid)  # True
```

### 4. `core.entity` - CRUD Operations

```python
from genesis_core import entity

# Create entity
user = entity.create_entity("User", {
    "name": "Charlie",
    "email": "charlie@example.com",
    "age": 25
})

# Update entity
updated = entity.update_entity(user.id, {"age": 26})

# List entities
all_users = entity.list_entities("User")
```

### 5. `core.transform` - Data Transformation

```python
from genesis_core import transform

# Define transformation
transform.define_transform(
    "user_to_summary",
    "User",
    "UserSummary",
    lambda e: {"display_name": e.data["name"]}
)

# Apply transformation
summary = transform.apply_transform(user, "user_to_summary")
```

### 6. `core.process` - Workflows

```python
from genesis_core import process

# Define step handlers
def step_validate(entity):
    # Validation logic
    return entity

def step_approve(entity):
    # Approval logic
    return entity

# Register handlers
process.register_step_handler("validate", step_validate)
process.register_step_handler("approve", step_approve)

# Define process
workflow = process.define_process("onboarding", [
    "validate",
    "approve"
])

# Execute
result = process.execute_process("onboarding", user)
```

### 7. `core.validation` - Rule Engine

```python
from genesis_core import validation

# Define rules
validation.define_rule("adult", lambda e: e.data["age"] >= 18)
validation.define_rule("email_valid", lambda e: "@" in e.data["email"])

# Validate
result = validation.validate(user, ["adult", "email_valid"])
print(result.is_valid)  # True or False
print(result.errors)    # List of error messages
```

### 8. `core.identity` - Auth/Permissions

```python
from genesis_core import identity

# Create subject
admin = identity.create_subject("admin_1", {
    "name": "Admin User",
    "role": "admin"
})

# Grant permissions
identity.grant_permission("admin_1", "read", "user:*")
identity.grant_permission("admin_1", "write", "user:*")

# Check permission
can_read = identity.check_permission("admin_1", "read", "user:123")
```

---

## Building Extensions

### The Golden Rule

**NEVER modify `genesis_core/`.** Always create extensions.

### Example: File-Based Storage

```python
# extensions/storage_file.py
from genesis_core import storage as core_storage
from pathlib import Path
import pickle

STORAGE_DIR = Path("./data")

def store(key: str, data: Any) -> None:
    """Extended store with file persistence"""
    # Use core
    core_storage.store(key, data)

    # Add file persistence
    file_path = STORAGE_DIR / f"{key}.pkl"
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)

def retrieve(key: str) -> Any:
    """Extended retrieve with file fallback"""
    try:
        return core_storage.retrieve(key)
    except KeyError:
        # Load from disk
        file_path = STORAGE_DIR / f"{key}.pkl"
        with open(file_path, 'rb') as f:
            return pickle.load(f)
```

### Example: Domain Application

See `extensions/example_agency/` for a complete recruiting agency with:
- Domain schemas (Applicant, Job, Interview)
- Validation rules (email, phone, CV)
- Hiring workflow (validate → screen → interview)

Run it: `python3 extensions/example_agency/main.py`

---

## Verification

### Check Core Integrity

```bash
python3 scripts/verify_frozen.py
```

Output:
```
✅ genesis_core/__init__.py
✅ genesis_core/io.py
✅ genesis_core/storage.py
...

✅ FROZEN CORE INTACT
```

If violated:
```
❌ genesis_core/storage.py
   ERROR: File has been MODIFIED (FORBIDDEN)

🚫 FROZEN CORE VIOLATED
```

### Continuous Integration

Add to your CI/CD:

```yaml
# .github/workflows/verify-frozen.yml
name: Verify Frozen Core

on: [push, pull_request]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Verify frozen core
        run: python3 scripts/verify_frozen.py
```

---

## Rules

### ❌ FORBIDDEN

- Modifying any file in `genesis_core/`
- Adding functions to core modules
- Changing function signatures
- "Improving" or "optimizing" core code
- Fixing bugs directly in core

### ✅ ALLOWED

- Creating wrappers in `extensions/`
- Building new functionality on top of core
- Combining core primitives creatively
- Creating domain-specific applications

### When You Need to "Fix" Core

1. **Option A:** Create a wrapper in `extensions/[module]_patches.py`
2. **Option B:** Build an adapter that works around the issue
3. **Last Resort:** Get team approval to unfreeze (see FROZEN_MANIFEST.md)

---

## Philosophy

### Why Frozen?

1. **Predictability** - Core never changes, system never breaks
2. **Composability** - Simple primitives combine into complex systems
3. **Understandability** - 8 modules, each does one thing
4. **AI-Safe** - Agents can't accidentally break the foundation

### Design Principles

1. **Dumb Core** - No intelligence, no domain logic, no cleverness
2. **Smart Extensions** - All creativity happens here
3. **Wrapper Pattern** - Extensions wrap, never replace
4. **Fail Fast** - Simple error handling, no magic

### Success Metrics

The Genesis Core is successful if:

- ✅ Zero modifications to core for 1+ years
- ✅ Any application can be built using only extensions
- ✅ New developers never need to touch core
- ✅ System remains stable and predictable

---

## Examples & Use Cases

### 1. Recruiting Agency

`extensions/example_agency/` - Complete hiring workflow with:
- Applicant management
- Job postings
- Interview scheduling
- Validation rules

### 2. File-Based Persistence

`extensions/storage_file.py` - Wraps core storage with disk persistence

### 3. Your Application Here

Genesis Core is designed to support:
- Content Management Systems
- E-commerce platforms
- Workflow automation
- Data processing pipelines
- API backends
- ...anything

**The core doesn't care what you build. It just provides the primitives.**

---

## Using Genesis Core in Your Project

### Create a New Project

```bash
# Create project directory
mkdir my_awesome_project
cd my_awesome_project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate on Windows

# Install Genesis Core
pip install genesis-core

# Create your extension
mkdir my_extension
```

### Project Structure

```
my_awesome_project/
├── venv/                     # Virtual environment
├── my_extension/             # Your extension code
│   ├── __init__.py
│   ├── schemas.py           # Define your schemas using core.schema
│   ├── business_logic.py    # Use core.entity, core.process
│   └── main.py
├── requirements.txt          # genesis-core==1.0.0
└── README.md
```

### requirements.txt

```
# Core (zero dependencies)
genesis-core==1.0.0

# Your extension dependencies
requests>=2.31.0
pillow>=10.0.0
typer>=0.9.0
```

### Example Extension

```python
# my_extension/schemas.py
from genesis_core import schema

def setup_schemas():
    """Define your domain schemas."""
    product_schema = schema.define_schema("Product", {
        "name": str,
        "price": int,
        "description": str,
        "in_stock": int
    })

    order_schema = schema.define_schema("Order", {
        "product_id": str,
        "quantity": int,
        "customer_email": str,
        "status": str
    })

    return {"Product": product_schema, "Order": order_schema}


# my_extension/business_logic.py
from genesis_core import entity, storage, validation

def create_product(name: str, price: int, description: str, stock: int):
    """Create a new product."""
    product = entity.create_entity("Product", {
        "name": name,
        "price": price,
        "description": description,
        "in_stock": stock
    })

    storage.store(f"product:{product.id}", product)
    return product


def place_order(product_id: str, quantity: int, email: str):
    """Place an order for a product."""
    # Validate product exists
    product = storage.retrieve(f"product:{product_id}")

    # Check stock
    if product.data["in_stock"] < quantity:
        raise ValueError("Insufficient stock")

    # Create order
    order = entity.create_entity("Order", {
        "product_id": product_id,
        "quantity": quantity,
        "customer_email": email,
        "status": "pending"
    })

    # Update stock
    entity.update_entity(product.id, {
        "in_stock": product.data["in_stock"] - quantity
    })

    storage.store(f"order:{order.id}", order)
    return order


# my_extension/main.py
from . import schemas, business_logic

if __name__ == "__main__":
    # Setup
    schemas.setup_schemas()

    # Use
    product = business_logic.create_product(
        name="Laptop",
        price=999,
        description="Powerful laptop",
        stock=10
    )

    order = business_logic.place_order(
        product_id=product.id,
        quantity=2,
        email="customer@example.com"
    )

    print(f"Order {order.id} placed successfully!")
```

### Key Principles

1. **Import from genesis_core** - Never copy core code
2. **Define your schemas** - Use `core.schema.define_schema()`
3. **Use core primitives** - `entity`, `storage`, `process`, etc.
4. **Add dependencies freely** - Your extension can use any library
5. **Never modify core** - Always wrap, never change

---

## Documentation

- **GENESIS_CORE_SPEC.md** - Complete module specifications
- **FROZEN_MANIFEST.md** - Freeze enforcement and policies
- **extensions/example_agency/** - Working application example

---

## FAQ

### Can I add new core modules?

No. The core is frozen at 8 modules. Create extensions instead.

### What if I find a bug in core?

Create a wrapper in `extensions/[module]_patches.py` that fixes it. Or get team approval to unfreeze.

### Can I optimize core performance?

No. Optimization is a change. Create an optimized wrapper in extensions.

### What about external dependencies (boto3, requests, etc)?

Core has zero dependencies. Extensions can have any dependencies they need.

### How do I handle database persistence?

Create `extensions/storage_db.py` that wraps `core.storage`.

### Can I use Genesis Core in production?

Yes. The frozen architecture makes it MORE stable than traditional codebases.

### What if my domain needs more schemas?

Define them in your extensions using `core.schema`.

---

## Contributing

### For Core

Core is frozen. Do not submit PRs that modify `genesis_core/`.

### For Extensions

Extensions are welcome! Submit PRs for:
- New storage backends (S3, Redis, PostgreSQL)
- Domain applications (CRM, CMS, etc.)
- Utilities and helpers
- Documentation improvements

---

## License

MIT License - See [LICENSE](LICENSE) file for details.

---

## Acknowledgments

Built on the principle that **stability comes from immutability, not perfection.**

The Genesis Core is intentionally simple, deliberately constrained, and permanently frozen.

**Build on it. Don't break it.**

---

## Get Started

### Install

```bash
pip install genesis-core
```

### Use in Your Project

```python
# my_project/main.py
from genesis_core import storage, entity, schema

# Define schemas
schema.define_schema("Product", {
    "name": "Product",
    "fields": {
        "id": {"type": "string", "required": True},
        "name": {"type": "string", "required": True},
        "price": {"type": "number", "required": True},
    }
})

# Create entities
product = entity.create_entity("Product", {
    "id": "prod-001",
    "name": "Widget",
    "price": 29.99
})

# Store and retrieve
storage.store(product["id"], product)
retrieved = storage.retrieve("prod-001")
print(f"Product: {retrieved['name']} - ${retrieved['price']}")
```

### Build Extensions

```python
# my_project/extensions/storage_db.py
from genesis_core import storage as core_storage
import sqlite3

def store(key: str, data: dict):
    """Extended storage with SQLite persistence"""
    # Use core
    core_storage.store(key, data)

    # Add database persistence
    conn = sqlite3.connect("app.db")
    # ... your DB logic here
    conn.close()
```

### Deploy with Confidence

```bash
# requirements.txt
genesis-core==1.0.0  # Frozen - will never break
```

**Welcome to Genesis Core. The foundation that never changes.**

---

## Version History

- **1.0.0** (2025-11-11) - Initial frozen release
  - 8 core modules: io, storage, schema, entity, transform, process, validation, identity
  - Zero dependencies
  - Complete test coverage
  - Frozen manifest and integrity checking
