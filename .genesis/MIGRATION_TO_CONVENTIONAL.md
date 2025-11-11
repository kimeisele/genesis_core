# Migration to Conventional Core

**Date:** 2025-11-11
**Status:** Complete

## What Changed

Genesis Core has evolved from **"Frozen Core"** to **"Conventional Core"**.

### Old Paradigm: Frozen Core

- Core modules were "frozen" with SHA-256 hashes
- `test_frozen_integrity.py` verified hashes hadn't changed
- Any modification = test failure
- Very rigid, could kill development flow

### New Paradigm: Conventional Core

- Core modules follow **conventions and patterns**
- `test_consistency.py` checks patterns, not hashes
- Modifications allowed if they follow conventions
- Balance between consistency and flow

## Key Files

### Added
- `README.md` → "FOR AI ASSISTANTS" section at top
- `.genesis/PATTERNS.md` → Coding patterns guide
- `.genesis/templates/` → Templates for workflows, extensions, schemas
- `tests/test_consistency.py` → Pattern-based tests
- `.pre-commit-config.yaml` → Pre-commit hooks
- `.genesis/MIGRATION_TO_CONVENTIONAL.md` → This file

### Modified
- `README.md` → Now says "CONVENTIONAL" instead of "FROZEN"

### Kept (for now)
- `tests/test_frozen_integrity.py` → Still exists but deprecated
- `FROZEN_MANIFEST.md` → Still exists, consider updating
- `scripts/verify_frozen.py` → Still exists, consider updating

## What to Update

If you want to fully commit to Conventional Core:

1. **Update FROZEN_MANIFEST.md**
   - Rename to `CONVENTIONAL_MANIFEST.md`
   - Update language from "frozen" to "conventional"
   - Remove hash-based enforcement language

2. **Update GitHub Workflows**
   - `.github/workflows/freeze_check.yml` → Run `test_consistency.py`
   - `.github/workflows/freeze-check.yml` → Run `test_consistency.py`
   - Remove hash verification, keep pattern checks

3. **Update scripts/verify_frozen.py**
   - Rename to `scripts/verify_consistency.py`
   - Change from hash-based to pattern-based checks
   - Or keep it for backward compatibility

4. **Deprecate test_frozen_integrity.py**
   - Add deprecation notice at top
   - Point to `test_consistency.py` as replacement

## Philosophy Shift

### Frozen Core (Old)
```
❌ FORBIDDEN: Modify any file in genesis_core/
✅ ALLOWED: Create wrappers only
```

**Problem:** Too rigid for iterative development with AI

### Conventional Core (New)
```
⚠️  STABLE: Core changes rarely, ask first
✅ ENCOURAGED: Follow patterns in .genesis/PATTERNS.md
✅ TESTED: test_consistency.py checks conventions
```

**Benefit:** Maintains consistency while allowing necessary evolution

## For AI Assistants

If you're an AI assistant reading this:

1. **Read README.md first** → See "FOR AI ASSISTANTS" section
2. **Check .genesis/PATTERNS.md** → Follow these patterns
3. **Run tests before commit:** `pytest tests/test_consistency.py`
4. **Ask user before modifying core** → Even though it's allowed

The goal is **guided consistency**, not rigid enforcement.

## Backward Compatibility

Old tests still work:
- `test_frozen_integrity.py` → Will still run, might fail (that's OK)
- `verify_frozen.py` → Will still work, might report violations

New tests are additive:
- `test_consistency.py` → Primary consistency checks
- Both can coexist during transition

## Next Steps

1. ✅ Conventional Core implemented
2. ⏳ Consider updating FROZEN_MANIFEST.md
3. ⏳ Update GitHub workflows to use test_consistency.py
4. ⏳ Add deprecation notices to old frozen checks
5. ⏳ Optionally: Remove frozen checks entirely after testing

## Questions?

This migration maintains the **spirit** of Genesis Core (stability, consistency) while adopting a more **pragmatic** approach that works better with AI-assisted development.

The core is still special. We just check it differently.
