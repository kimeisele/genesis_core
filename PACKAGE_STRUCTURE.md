# Genesis Core - Pure Package Structure

**Version:** 1.0.0
**Type:** Frozen Core Only
**Status:** Production Ready

---

## Package Contents

When you `pip install genesis-core`, you get **ONLY**:

```
genesis_core/
├── __init__.py
├── io.py              # File operations
├── storage.py         # Key-value storage
├── schema.py          # Data structure definitions
├── entity.py          # CRUD operations
├── transform.py       # Data transformations
├── process.py         # Workflows/state machines
├── validation.py      # Rule engine
└── identity.py        # Auth/permissions
```

**That's it. Nothing else.**

- ✅ Zero dependencies
- ✅ Pure Python stdlib
- ✅ Frozen contract maintained
- ✅ Production ready

---

## What's NOT in the Package

These are in the **repository** for development/examples, but NOT installed:

```
❌ examples/              # Demo extensions (NOT installed)
❌ tests/                 # Test suite (NOT installed)
❌ scripts/               # Dev tools (NOT installed)
❌ docs/                  # Documentation (NOT installed)
```

---

## Repository Structure (for developers)

If you clone the repo, you see:

```
genesis_core/  (GitHub Repo)
├── genesis_core/          # ✅ THE PACKAGE (installed via pip)
│   ├── __init__.py
│   ├── io.py
│   ├── storage.py
│   ├── schema.py
│   ├── entity.py
│   ├── transform.py
│   ├── process.py
│   ├── validation.py
│   └── identity.py
│
├── examples/              # ❌ NOT PART OF PACKAGE
│   ├── example_agency/    #    Demo: Recruiting agency
│   └── storage_file.py    #    Demo: File-based storage
│
├── tests/                 # ❌ NOT PART OF PACKAGE
│   ├── test_core_modules.py
│   └── test_frozen_integrity.py
│
├── scripts/               # ❌ NOT PART OF PACKAGE
│   └── verify_frozen.py
│
├── .github/               # ❌ NOT PART OF PACKAGE
│   └── workflows/
│
├── setup.py               # Package config
├── pyproject.toml         # Modern packaging
├── MANIFEST.in            # What to include
├── README.md              # Documentation
├── FROZEN_MANIFEST.md     # Freeze rules
└── GENESIS_CORE_SPEC.md   # Specs
```

---

## For Users (pip install)

```bash
# Install
pip install genesis-core

# Use
from genesis_core import entity, schema, storage

# Build your extensions in YOUR project
# (not in genesis_core/)
```

---

## For Contributors

```bash
# Clone repo
git clone https://github.com/kimeisele/genesis_core.git
cd genesis_core

# Install in dev mode
pip install -e ".[dev]"

# Run tests
pytest tests/

# Verify frozen
python scripts/verify_frozen.py

# Run examples
python examples/example_agency/main.py
```

---

## Key Principle

**Genesis Core is PURE:**
- Package = ONLY `genesis_core/` module
- Examples = Demos in repo (not installed)
- Extensions = Built in YOUR projects (not here)

**This is intentional. This is correct. This is frozen.**

