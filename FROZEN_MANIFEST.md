# FROZEN CORE MANIFEST

**Version:** 1.0.0
**Freeze Date:** 2025-11-11
**Status:** FROZEN

## Purpose

This manifest documents the frozen state of Genesis Core modules. These modules are **immutable** and must never be modified. Any changes to these files will break the frozen core contract.

## Frozen Modules

| Module | Status | SHA-256 Hash |
|--------|--------|--------------|
| `genesis_core/__init__.py` | ✅ Frozen | `5cb515b96ae34a121fe76e80a5330c10c1fbe27035e3ba01dfb9392241da791f` |
| `genesis_core/io.py` | ✅ Frozen | `d123e3b46f49b67f62fa0aa4cec2de1cbb6e7409a4774aa80f083ea964e71eba` |
| `genesis_core/storage.py` | ✅ Frozen | `4f4c224a2affdb59563a8fe7d04eed9086dd25a3bf90222a8ca7ceb01e8c7ed2` |
| `genesis_core/schema.py` | ✅ Frozen | `805ee369d3b9fbfb7ff3f574044733fa2016e44818b2feab3fbb599ea25315d1` |
| `genesis_core/entity.py` | ✅ Frozen | `10626db0d39fa827ebae8927a19d561e4dff65248cf1341b5872807e7b6595ea` |
| `genesis_core/transform.py` | ✅ Frozen | `063a8b2eda0c3c9a1e25dd6cc838856652ff577de7818c06556044e5b14f8568` |
| `genesis_core/process.py` | ✅ Frozen | `c73749c01a693e8cdbda40f233433c27ecfe3b79204a7276e581d7e84ec2d94c` |
| `genesis_core/validation.py` | ✅ Frozen | `6124968b2ec871e5a0a22abdac098c36c5036dd80a8398b06c49bf88770007aa` |
| `genesis_core/identity.py` | ✅ Frozen | `d578c373d720edbaee629d829cb1865eca803d79a2bf55df9b0bfa1f5b5e0ca7` |

## Extension Policy

### ⚠️ CORE MODULES MUST NOT BE MODIFIED ⚠️

**Forbidden Actions:**

- ❌ Modifying any file in `genesis_core/`
- ❌ Adding functions to core modules
- ❌ Changing function signatures
- ❌ Fixing bugs directly in core (create patches in extensions)
- ❌ Adding parameters to core functions
- ❌ Optimizing core code

**Allowed Actions:**

- ✅ Creating wrappers in `extensions/`
- ✅ Building new functionality in `extensions/`
- ✅ Combining core primitives in creative ways
- ✅ Creating adapters for external systems

### How to Add Features

Instead of modifying core, create extensions:

```python
# ❌ WRONG: Modifying core/storage.py
def store_to_s3(key: str, data: Any):
    # DON'T ADD THIS TO CORE
    ...

# ✅ CORRECT: Create extensions/storage_s3.py
from genesis_core import storage as core_storage

def store(key: str, data: Any):
    """Extended store with S3 persistence"""
    core_storage.store(key, data)  # Use core
    _upload_to_s3(key, data)  # Add S3 logic
```

### How to Fix Bugs

If you find a bug in core:

1. **Critical Security Bugs:** Require team approval to unfreeze
2. **Non-Critical Bugs:** Create a patch in `extensions/[module]_patches.py`

Example patch:

```python
# extensions/storage_patches.py
from genesis_core import storage as core_storage

def store(key: str, data: Any):
    """Patched version with bug fix"""
    # Apply fix here
    return core_storage.store(key, data)
```

## Verification

Run the verification script to check core integrity:

```bash
python3 scripts/verify_frozen.py
```

This script:
- ✅ Verifies all core module hashes match this manifest
- ✅ Detects any unauthorized modifications
- ✅ Ensures frozen contract is maintained

## Unfreeze Criteria

Core modules can ONLY be unfrozen if:

1. **Critical security vulnerability** discovered
2. **Production-breaking bug** that cannot be patched
3. **Team consensus** achieved
4. **Full impact assessment** completed

Even then, changes must:
- Maintain backward compatibility
- Not break existing extensions
- Be documented in change log
- Result in new manifest version

## Success Metrics

The frozen core is successful if:

- ✅ Zero modifications to core for 1+ years
- ✅ All new features built as extensions
- ✅ No developer needs to touch core
- ✅ System remains stable and predictable

## Maintenance Schedule

- **Daily:** Run `verify_frozen.py` in CI/CD
- **Weekly:** Review extension quality
- **Monthly:** Audit core usage patterns
- **Quarterly:** Evaluate freeze policy effectiveness

## Emergency Contacts

If you absolutely must modify core:

1. Stop immediately
2. Document why extension approach won't work
3. Get team approval
4. Create detailed change proposal
5. Update this manifest after changes

---

**Last Verified:** 2025-11-11
**Verification Status:** ✅ All hashes valid
**Next Review:** 2025-12-11

---

*This manifest represents the eternal contract of Genesis Core.*
*Respect the freeze. Build with extensions.*
