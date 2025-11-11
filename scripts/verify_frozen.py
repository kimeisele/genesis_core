#!/usr/bin/env python3
"""
Frozen Core Verification Script

Verifies that frozen core modules haven't been modified.
Run this before and after ANY changes to the codebase.

Usage:
    python3 scripts/verify_frozen.py

Exit codes:
    0 - All checks passed
    1 - Frozen core violated
"""

import hashlib
from pathlib import Path
import sys


# Expected hashes from FROZEN_MANIFEST.md
FROZEN_HASHES = {
    "genesis_core/__init__.py": "5cb515b96ae34a121fe76e80a5330c10c1fbe27035e3ba01dfb9392241da791f",
    "genesis_core/io.py": "82de793900f734f4ed35c83c46b35ba7b894082e69c51eaf97de1e4cc3f2d1f8",
    "genesis_core/storage.py": "4f4c224a2affdb59563a8fe7d04eed9086dd25a3bf90222a8ca7ceb01e8c7ed2",
    "genesis_core/schema.py": "38af14afd87c54e72eef2ab60230d6058ba95920001599ddb932c2367ecee59b",
    "genesis_core/entity.py": "18e87d4dc03f91d7e2606141eadfff92189f22f954d55f1ad08802f371c252cf",
    "genesis_core/transform.py": "135695eb7875716e61f8fd913731eb4f48dbd03cffb93791b930879c318997a4",
    "genesis_core/process.py": "4bec7ad2e852f61b47b558642a24ea93f3c607d91dda257049929a4a7b5162fc",
    "genesis_core/validation.py": "ecdb3507b7bc1dc836b59a1f55d6b7b04c579a80c57fa5281cf80feb9339c6ef",
    "genesis_core/identity.py": "0c0a24b94a63b855f5de05c0ff6c00536b7beedec1d79b84669b35d329c86382",
}


def get_file_hash(path: Path) -> str:
    """
    Calculate SHA-256 hash of a file.

    Args:
        path: Path to file

    Returns:
        str: Hex digest of SHA-256 hash
    """
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_frozen_core() -> int:
    """
    Verify all frozen core modules.

    Returns:
        int: Exit code (0 = success, 1 = violations found)
    """
    print("=" * 70)
    print("FROZEN CORE VERIFICATION")
    print("=" * 70)
    print()

    violations = []
    warnings = []
    checked = 0

    # Get project root (parent of scripts/)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    print(f"Project root: {project_root}")
    print(f"Checking {len(FROZEN_HASHES)} frozen modules...")
    print()

    for module_path, expected_hash in FROZEN_HASHES.items():
        full_path = project_root / module_path
        checked += 1

        # Check if file exists
        if not full_path.exists():
            violations.append({
                "module": module_path,
                "issue": "DELETED",
                "severity": "CRITICAL"
            })
            print(f"❌ {module_path}")
            print(f"   ERROR: File has been DELETED")
            print()
            continue

        # Check hash
        actual_hash = get_file_hash(full_path)

        if actual_hash != expected_hash:
            violations.append({
                "module": module_path,
                "issue": "MODIFIED",
                "severity": "CRITICAL",
                "expected": expected_hash[:16] + "...",
                "actual": actual_hash[:16] + "..."
            })
            print(f"❌ {module_path}")
            print(f"   ERROR: File has been MODIFIED (FORBIDDEN)")
            print(f"   Expected: {expected_hash[:16]}...")
            print(f"   Actual:   {actual_hash[:16]}...")
            print()
        else:
            print(f"✅ {module_path}")

    # Summary
    print()
    print("=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    print()
    print(f"Modules checked: {checked}")
    print(f"Violations found: {len(violations)}")
    print()

    if violations:
        print("🚫 FROZEN CORE VIOLATED")
        print()
        print("The following modules were modified or deleted:")
        print()

        for violation in violations:
            print(f"  • {violation['module']}: {violation['issue']}")

        print()
        print("=" * 70)
        print("WHAT TO DO:")
        print("=" * 70)
        print()
        print("1. Revert changes to core modules")
        print("2. Create extensions instead:")
        print()
        print("   # Create extensions/[module]_extended.py")
        print("   from genesis_core import [module] as core_module")
        print()
        print("   def your_new_function():")
        print("       # Your logic here")
        print("       return core_module.some_function()")
        print()
        print("3. Read FROZEN_MANIFEST.md for details")
        print()

        return 1

    else:
        print("✅ FROZEN CORE INTACT")
        print()
        print("All core modules are unchanged.")
        print("The frozen contract is maintained.")
        print()

        return 0


def main():
    """Main entry point."""
    exit_code = verify_frozen_core()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
