"""
Test frozen core integrity - ensure modules haven't been modified.
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
    EXPECTED_HASHES = {
        "__init__.py": "5cb515b96ae34a121fe76e80a5330c10c1fbe27035e3ba01dfb9392241da791f",
        "io.py": "d123e3b46f49b67f62fa0aa4cec2de1cbb6e7409a4774aa80f083ea964e71eba",
        "storage.py": "4f4c224a2affdb59563a8fe7d04eed9086dd25a3bf90222a8ca7ceb01e8c7ed2",
        "schema.py": "805ee369d3b9fbfb7ff3f574044733fa2016e44818b2feab3fbb599ea25315d1",
        "entity.py": "10626db0d39fa827ebae8927a19d561e4dff65248cf1341b5872807e7b6595ea",
        "transform.py": "063a8b2eda0c3c9a1e25dd6cc838856652ff577de7818c06556044e5b14f8568",
        "process.py": "c73749c01a693e8cdbda40f233433c27ecfe3b79204a7276e581d7e84ec2d94c",
        "validation.py": "6124968b2ec871e5a0a22abdac098c36c5036dd80a8398b06c49bf88770007aa",
        "identity.py": "d578c373d720edbaee629d829cb1865eca803d79a2bf55df9b0bfa1f5b5e0ca7",
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
            f.name for f in core_path.iterdir()
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
