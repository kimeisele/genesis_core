"""
Consistency tests for Genesis Core.

These tests enforce PATTERNS, not hashes. They check that code follows
conventions and maintains consistency, while allowing necessary changes.

This is the enforcement mechanism for "Conventional Core" philosophy.
"""

import ast
import pytest
from pathlib import Path
from typing import List, Set


# Core modules that should exist
EXPECTED_CORE_MODULES = {
    "__init__.py",
    "io.py",
    "storage.py",
    "schema.py",
    "entity.py",
    "transform.py",
    "process.py",
    "validation.py",
    "identity.py",
}

# External dependencies forbidden in core (keep it zero-dependency)
FORBIDDEN_IMPORTS = {
    "requests",
    "numpy",
    "pandas",
    "boto3",
    "redis",
    "sqlalchemy",
    "django",
    "flask",
    "fastapi",
    "pydantic",
    "aiohttp",
}


class TestCoreStructure:
    """Test that core maintains expected structure."""

    @pytest.fixture
    def core_path(self) -> Path:
        """Get path to genesis_core module."""
        return Path(__file__).parent.parent / "genesis_core"

    def test_all_expected_modules_exist(self, core_path):
        """Verify all expected core modules are present."""
        actual_files = {f.name for f in core_path.iterdir() if f.is_file() and f.suffix == ".py"}

        missing = EXPECTED_CORE_MODULES - actual_files
        assert len(missing) == 0, (
            f"Expected core modules are missing: {missing}\n"
            f"Core should have these 9 fundamental modules."
        )

    def test_no_unauthorized_modules(self, core_path):
        """Ensure no extra modules were added without approval."""
        actual_files = {
            f.name
            for f in core_path.iterdir()
            if f.is_file() and f.suffix == ".py" and f.name != "py.typed"
        }

        extra_files = actual_files - EXPECTED_CORE_MODULES

        # Allow extra files if they start with underscore (private helpers)
        extra_files = {f for f in extra_files if not f.startswith("_")}

        if extra_files:
            print(
                f"\n⚠️  WARNING: Unauthorized modules in core: {extra_files}\n"
                f"Core should only contain the 9 fundamental modules.\n"
                f"New functionality should go in examples/ or extensions.\n"
            )
            # This is a warning, not a failure - user might have a good reason
            # Uncomment to make it a hard failure:
            # assert False, f"Unauthorized modules: {extra_files}"


class TestCodeConventions:
    """Test that code follows established conventions."""

    @pytest.fixture
    def core_path(self) -> Path:
        """Get path to genesis_core module."""
        return Path(__file__).parent.parent / "genesis_core"

    def _get_python_files(self, directory: Path) -> List[Path]:
        """Get all Python files in directory."""
        return list(directory.glob("*.py"))

    def _parse_file(self, file_path: Path) -> ast.Module:
        """Parse a Python file into AST."""
        with open(file_path, "r", encoding="utf-8") as f:
            return ast.parse(f.read(), filename=str(file_path))

    def _get_imports(self, tree: ast.Module) -> Set[str]:
        """Extract all import names from AST."""
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split(".")[0])
        return imports

    def test_core_has_no_external_dependencies(self, core_path):
        """Ensure core modules don't import external libraries."""
        violations = []

        for py_file in self._get_python_files(core_path):
            if py_file.name == "__init__.py":
                continue

            tree = self._parse_file(py_file)
            imports = self._get_imports(tree)

            forbidden = imports & FORBIDDEN_IMPORTS
            if forbidden:
                violations.append(f"{py_file.name}: {forbidden}")

        assert len(violations) == 0, (
            f"\n\n❌ EXTERNAL DEPENDENCIES DETECTED IN CORE!\n"
            f"Violations:\n" + "\n".join(f"  - {v}" for v in violations) + "\n\n"
            f"Genesis Core must have ZERO external dependencies.\n"
            f"Use only Python stdlib.\n"
            f"Put code needing external deps in examples/ or extensions.\n"
        )

    def test_public_functions_have_docstrings(self, core_path):
        """Ensure all public functions have docstrings."""
        violations = []

        for py_file in self._get_python_files(core_path):
            if py_file.name == "__init__.py":
                continue

            tree = self._parse_file(py_file)

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Skip private functions (start with _)
                    if node.name.startswith("_"):
                        continue

                    # Check if docstring exists
                    docstring = ast.get_docstring(node)
                    if not docstring:
                        violations.append(f"{py_file.name}::{node.name}")

        if violations:
            print(
                f"\n⚠️  WARNING: Public functions without docstrings:\n"
                + "\n".join(f"  - {v}" for v in violations)
                + "\n\nPlease add docstrings to public functions.\n"
            )
            # This is a warning for now
            # Uncomment to make it a hard failure:
            # assert False, f"Functions without docstrings: {violations}"

    def test_modules_have_docstrings(self, core_path):
        """Ensure all modules have module-level docstrings."""
        violations = []

        for py_file in self._get_python_files(core_path):
            if py_file.name == "__init__.py":
                continue

            tree = self._parse_file(py_file)
            docstring = ast.get_docstring(tree)

            if not docstring:
                violations.append(py_file.name)

        if violations:
            print(
                f"\n⚠️  WARNING: Modules without docstrings:\n"
                + "\n".join(f"  - {v}" for v in violations)
                + "\n\nPlease add module-level docstrings.\n"
            )


class TestPatternCompliance:
    """Test that code follows Genesis Core patterns."""

    @pytest.fixture
    def examples_path(self) -> Path:
        """Get path to examples directory."""
        return Path(__file__).parent.parent / "examples"

    def test_examples_exist(self, examples_path):
        """Ensure examples directory exists and has content."""
        assert examples_path.exists(), "examples/ directory should exist"
        assert examples_path.is_dir(), "examples/ should be a directory"

        # Should have at least one example
        examples = list(examples_path.iterdir())
        if len(examples) == 0:
            print(
                "\n⚠️  WARNING: No examples found in examples/ directory.\n"
                "Consider adding example extensions for users to learn from.\n"
            )

    def test_templates_exist(self):
        """Ensure template files exist in .genesis/templates/."""
        templates_path = Path(__file__).parent.parent / ".genesis" / "templates"

        assert templates_path.exists(), ".genesis/templates/ directory should exist"

        expected_templates = {
            "workflow.py.template",
            "extension.py.template",
            "schema_setup.py.template",
        }

        actual_templates = {f.name for f in templates_path.iterdir() if f.is_file()}

        missing = expected_templates - actual_templates
        if missing:
            print(
                f"\n⚠️  WARNING: Missing templates: {missing}\n"
                "Templates help AI assistants create consistent code.\n"
            )


class TestProjectStructure:
    """Test overall project structure."""

    def test_frozen_manifest_updated(self):
        """Check if FROZEN_MANIFEST.md reflects new philosophy."""
        manifest_path = Path(__file__).parent.parent / "FROZEN_MANIFEST.md"

        if not manifest_path.exists():
            print("\n⚠️  Note: FROZEN_MANIFEST.md not found (this is OK)")
            return

        content = manifest_path.read_text()

        # Should NOT still talk about hash enforcement if using conventional
        if "hash" in content.lower() and "conventional" in content.lower():
            print(
                "\n⚠️  WARNING: FROZEN_MANIFEST.md might need updating.\n"
                "Consider updating it to reflect 'Conventional Core' philosophy.\n"
            )

    def test_readme_has_ai_section(self):
        """Ensure README has 'FOR AI ASSISTANTS' section."""
        readme_path = Path(__file__).parent.parent / "README.md"
        content = readme_path.read_text()

        assert (
            "FOR AI ASSISTANTS" in content or "FOR AI:" in content
        ), "README should have a section for AI assistants at the top"


# Summary function for manual runs
def test_consistency_summary():
    """Print summary of consistency test philosophy."""
    print(
        "\n"
        "=" * 70 + "\n"
        "GENESIS CORE CONSISTENCY TESTS\n"
        "=" * 70 + "\n"
        "\n"
        "Philosophy: CONVENTIONAL CORE (not Frozen Core)\n"
        "\n"
        "These tests check PATTERNS, not hashes:\n"
        "  ✅ Core structure maintained (9 modules)\n"
        "  ✅ Zero external dependencies in core\n"
        "  ✅ Public functions have docstrings\n"
        "  ✅ Examples and templates exist\n"
        "\n"
        "Tests are WARNINGS, not strict enforcement.\n"
        "The goal: Guide consistency without killing flow.\n"
        "\n"
        "=" * 70 + "\n"
    )


if __name__ == "__main__":
    # Run with pytest
    pytest.main([__file__, "-v", "--tb=short"])
