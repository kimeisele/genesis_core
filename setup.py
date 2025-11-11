"""
Setup configuration for Genesis Core package.

This makes Genesis Core installable via pip.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8")

setup(
    name="genesis-core",
    version="1.0.0",

    # Package info
    packages=find_packages(exclude=["tests", "scripts", "extensions", "examples"]),
    python_requires=">=3.10",

    # Dependencies
    install_requires=[
        # Genesis Core has ZERO dependencies - it's completely self-contained
    ],

    # Metadata
    author="Genesis Core Team",
    author_email="info@genesis-core.dev",
    description="Frozen Core modules for building unbreakable systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kimeisele/genesis_core",

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
    ],

    # Keywords
    keywords="frozen-core, unbreakable-systems, entity-system, schema-validation, process-workflow",

    # Project URLs
    project_urls={
        "Bug Reports": "https://github.com/kimeisele/genesis_core/issues",
        "Source": "https://github.com/kimeisele/genesis_core",
        "Documentation": "https://github.com/kimeisele/genesis_core#readme",
    },

    # Include package data
    include_package_data=True,
    zip_safe=False,
)
