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
    "genesis_core/io.py": "d123e3b46f49b67f62fa0aa4cec2de1cbb6e7409a4774aa80f083ea964e71eba",
    "genesis_core/storage.py": "4f4c224a2affdb59563a8fe7d04eed9086dd25a3bf90222a8ca7ceb01e8c7ed2",
    "genesis_core/schema.py": "805ee369d3b9fbfb7ff3f574044733fa2016e44818b2feab3fbb599ea25315d1",
    "genesis_core/entity.py": "10626db0d39fa827ebae8927a19d561e4dff65248cf1341b5872807e7b6595ea",
    "genesis_core/transform.py": "063a8b2eda0c3c9a1e25dd6cc838856652ff577de7818c06556044e5b14f8568",
    "genesis_core/process.py": "c73749c01a693e8cdbda40f233433c27ecfe3b79204a7276e581d7e84ec2d94c",
    "genesis_core/validation.py": "6124968b2ec871e5a0a22abdac098c36c5036dd80a8398b06c49bf88770007aa",
    "genesis_core/identity.py": "d578c373d720edbaee629d829cb1865eca803d79a2bf55df9b0bfa1f5b5e0ca7",
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
