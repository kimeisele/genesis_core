"""
Test frozen core integrity - ensure modules haven't been modified.

⚠️ DEPRECATION NOTICE:
This test uses hash-based verification which is part of the old "Frozen Core" paradigm.
Genesis Core has migrated to "Conventional Core" which uses pattern-based checks.

See: tests/test_consistency.py for the new approach
See: .genesis/MIGRATION_TO_CONVENTIONAL.md for details

This test is kept for backward compatibility but may be removed in future versions.
"""

import hashlib
import pytest
from pathlib import Path


def calculate_sha256(file_path: Path) -> str:
    """Calculate SHA-256 hash of a file"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


class TestFrozenIntegrity:
    """Test that core modules remain frozen (unchanged)"""

    # Expected hashes from FROZEN_MANIFEST.md
    # Updated after black formatting (code style consistency)
    EXPECTED_HASHES = {
        "__init__.py": "5cb515b96ae34a121fe76e80a5330c10c1fbe27035e3ba01dfb9392241da791f",
        "io.py": "82de793900f734f4ed35c83c46b35ba7b894082e69c51eaf97de1e4cc3f2d1f8",
        "storage.py": "4f4c224a2affdb59563a8fe7d04eed9086dd25a3bf90222a8ca7ceb01e8c7ed2",
        "schema.py": "38af14afd87c54e72eef2ab60230d6058ba95920001599ddb932c2367ecee59b",
        "entity.py": "18e87d4dc03f91d7e2606141eadfff92189f22f954d55f1ad08802f371c252cf",
        "transform.py": "135695eb7875716e61f8fd913731eb4f48dbd03cffb93791b930879c318997a4",
        "process.py": "4bec7ad2e852f61b47b558642a24ea93f3c607d91dda257049929a4a7b5162fc",
        "validation.py": "ecdb3507b7bc1dc836b59a1f55d6b7b04c579a80c57fa5281cf80feb9339c6ef",
        "identity.py": "0c0a24b94a63b855f5de05c0ff6c00536b7beedec1d79b84669b35d329c86382",
    }

    @pytest.fixture
    def core_path(self) -> Path:
        """Get path to genesis_core module"""
        return Path(__file__).parent.parent / "genesis_core"

    def test_all_core_modules_exist(self, core_path):
        """Verify all core modules exist"""
        for module_name in self.EXPECTED_HASHES.keys():
            module_path = core_path / module_name
            assert module_path.exists(), f"Core module {module_name} is missing!"

    def test_core_integrity_hashes(self, core_path):
        """Verify core modules haven't been modified (hash check)"""
        for module_name, expected_hash in self.EXPECTED_HASHES.items():
            module_path = core_path / module_name
            actual_hash = calculate_sha256(module_path)

            assert actual_hash == expected_hash, (
                f"\n\n"
                f"🚨 FROZEN CORE VIOLATION DETECTED! 🚨\n"
                f"Module: {module_name}\n"
                f"Expected: {expected_hash}\n"
                f"Actual:   {actual_hash}\n"
                f"\n"
                f"Core modules are FROZEN and must not be modified!\n"
                f"See FROZEN_MANIFEST.md for extension policy.\n"
            )

    def test_no_extra_modules(self, core_path):
        """Verify no unauthorized modules were added to core"""
        actual_files = {
            f.name
            for f in core_path.iterdir()
            if f.is_file() and f.suffix == ".py" and f.name != "py.typed"
        }

        expected_files = set(self.EXPECTED_HASHES.keys())
        extra_files = actual_files - expected_files

        assert len(extra_files) == 0, (
            f"\n\n"
            f"🚨 UNAUTHORIZED MODULES DETECTED IN CORE! 🚨\n"
            f"Extra files: {extra_files}\n"
            f"\n"
            f"Core modules are frozen. New functionality must go in extensions/\n"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
