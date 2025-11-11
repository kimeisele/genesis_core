# Changelog

All notable changes to Genesis Core will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-11

### Added - Initial Frozen Release

#### Core Modules (FROZEN)
- `core.io` - File operations (read_text, write_text, read_json, write_json)
- `core.storage` - Key-value storage (store, retrieve, exists, delete)
- `core.schema` - Data structure definitions (define_schema, validate_data)
- `core.entity` - CRUD operations (create_entity, update_entity, delete_entity)
- `core.transform` - Data transformations (define_transform, apply_transform)
- `core.process` - Workflows and state machines (define_process, execute_process)
- `core.validation` - Rule engine (define_rule, validate)
- `core.identity` - Auth and permissions (create_subject, grant_permission)

#### Extensions (Examples)
- `extensions/storage_file.py` - File-based storage persistence
- `extensions/example_agency/` - Complete recruiting agency example

#### Documentation
- `README.md` - Complete documentation with examples
- `FROZEN_MANIFEST.md` - Freeze enforcement policy
- `GENESIS_CORE_SPEC.md` - Detailed module specifications
- `PROJECT_STRUCTURE.md` - Architecture overview
- `PUBLISHING.md` - PyPI publishing guide

#### Package Infrastructure
- `setup.py` - Setup configuration for pip
- `pyproject.toml` - Modern Python packaging config
- `MANIFEST.in` - Package file inclusion rules
- `LICENSE` - MIT License
- `requirements.txt` - Empty (zero dependencies)
- `requirements-dev.txt` - Development dependencies

#### Testing
- `test_core_basic.py` - Basic functionality tests
- `test_all.py` - Comprehensive test suite
- `test_extension.py` - Extension tests
- `scripts/verify_frozen.py` - Core integrity checker

#### CI/CD
- `.github/workflows/freeze-check.yml` - Automatic freeze verification
- `.github/workflows/publish.yml` - PyPI publishing workflow

#### Type Hints
- `genesis_core/py.typed` - PEP 561 marker for type hints support

### Philosophy
- **Frozen Core** - 8 core modules that never change
- **Zero Dependencies** - Pure Python stdlib only
- **Extension-First** - All features added via extensions
- **AI-Safe** - Agents can't accidentally break the foundation

### Compatibility
- Python >= 3.10
- No external dependencies
- Cross-platform (Linux, macOS, Windows)

---

## [Unreleased]

### Notes
- Core modules are FROZEN and will not change
- Future releases will focus on:
  - Additional extension examples
  - Documentation improvements
  - Tooling enhancements
  - CI/CD improvements
- Core modifications require team approval and unfreezing

---

## Version Guidelines

Given Genesis Core's frozen architecture:

- **Patch releases (1.0.x)** - Bug fixes in tooling/extensions, documentation updates
- **Minor releases (1.x.0)** - New extension examples, improved tests, new utilities
- **Major releases (2.0.0)** - Core changes (requires unfreezing - extremely rare)

**Current Status:** FROZEN at v1.0.0 since 2025-11-11

---

[1.0.0]: https://github.com/kimeisele/genesis_core/releases/tag/v1.0.0
