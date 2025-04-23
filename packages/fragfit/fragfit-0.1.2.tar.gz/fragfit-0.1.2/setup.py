#!/usr/bin/env python
from setuptools import setup
import os

# Default values in case we can't read pyproject.toml
default_metadata = {
    "name": "fragfit",
    "version": "0.1.1",
    "description": "Fragment formula fitting",
    "license": "MIT",
    "python_requires": ">=3.9",
    "install_requires": [
        "numpy>=1.20.0",
        "pandas>=1.3.0", 
        "molmass>=2024.10.25",
        "more-itertools>=10.1.0",
    ],
}

# Try to read from pyproject.toml if possible
try:
    import tomli
    with open("pyproject.toml", "rb") as f:
        pyproject = tomli.load(f)
    
    # Extract the dependencies
    dependencies = pyproject.get("project", {}).get("dependencies", default_metadata["install_requires"])
    python_requires = pyproject.get("project", {}).get("requires-python", default_metadata["python_requires"])
    version = pyproject.get("project", {}).get("version", default_metadata["version"])
    description = pyproject.get("project", {}).get("description", default_metadata["description"])
    license_info = pyproject.get("project", {}).get("license", default_metadata["license"])
    if isinstance(license_info, dict):
        license = license_info.get("text", default_metadata["license"])
    else:
        license = license_info
except (ImportError, FileNotFoundError):
    # If tomli is not available or pyproject.toml doesn't exist, use defaults
    dependencies = default_metadata["install_requires"]
    python_requires = default_metadata["python_requires"]
    version = default_metadata["version"]
    description = default_metadata["description"]
    license = default_metadata["license"]

# Setup for conda-build to pick up metadata
setup(
    name="fragfit",
    version=version,
    description=description,
    license=license,
    python_requires=python_requires,
    install_requires=dependencies,
) 