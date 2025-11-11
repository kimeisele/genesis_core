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
| `genesis_core/io.py` | ✅ Frozen | `82de793900f734f4ed35c83c46b35ba7b894082e69c51eaf97de1e4cc3f2d1f8` |
| `genesis_core/storage.py` | ✅ Frozen | `4f4c224a2affdb59563a8fe7d04eed9086dd25a3bf90222a8ca7ceb01e8c7ed2` |
| `genesis_core/schema.py` | ✅ Frozen | `38af14afd87c54e72eef2ab60230d6058ba95920001599ddb932c2367ecee59b` |
| `genesis_core/entity.py` | ✅ Frozen | `18e87d4dc03f91d7e2606141eadfff92189f22f954d55f1ad08802f371c252cf` |
| `genesis_core/transform.py` | ✅ Frozen | `135695eb7875716e61f8fd913731eb4f48dbd03cffb93791b930879c318997a4` |
| `genesis_core/process.py` | ✅ Frozen | `4bec7ad2e852f61b47b558642a24ea93f3c607d91dda257049929a4a7b5162fc` |
| `genesis_core/validation.py` | ✅ Frozen | `ecdb3507b7bc1dc836b59a1f55d6b7b04c579a80c57fa5281cf80feb9339c6ef` |
| `genesis_core/identity.py` | ✅ Frozen | `0c0a24b94a63b855f5de05c0ff6c00536b7beedec1d79b84669b35d329c86382` |

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
