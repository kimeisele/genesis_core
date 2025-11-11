"""
Genesis Core - Frozen Core Architecture for Unbreakable Systems

A minimal, frozen set of core modules that provide immutable building blocks
for reliable software systems. No external dependencies, no modifications,
just pure, predictable primitives.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else __doc__

setup(
    name="genesis-core",
    version="1.0.0",

    # Package structure
    packages=find_packages(exclude=["tests", "tests.*", "scripts", "extensions", "extensions.*"]),
    python_requires=">=3.10",

    # Zero dependencies - core is completely self-contained
    install_requires=[],

    # Metadata
    author="Genesis Core Team",
    author_email="info@genesis-core.dev",
    description="Frozen Core modules for unbreakable systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/genesis-core",
    project_urls={
        "Documentation": "https://github.com/yourusername/genesis-core#readme",
        "Source": "https://github.com/yourusername/genesis-core",
        "Tracker": "https://github.com/yourusername/genesis-core/issues",
    },

    # Classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Typing :: Typed",
    ],

    # Additional package data
    package_data={
        "genesis_core": ["py.typed"],  # PEP 561 marker for type checking
    },

    # Keywords for discoverability
    keywords=[
        "frozen-core",
        "immutable",
        "architecture",
        "primitives",
        "reliable-systems",
        "io",
        "storage",
        "schema",
        "entity",
        "validation",
    ],

    # Entry points (none for now - pure library)
    entry_points={},

    # Testing
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "mypy>=1.0.0",
        ],
    },

    # License
    license="MIT",

    # Include FROZEN_MANIFEST.md as package data
    include_package_data=True,
    zip_safe=False,  # Important: don't zip the package
)
