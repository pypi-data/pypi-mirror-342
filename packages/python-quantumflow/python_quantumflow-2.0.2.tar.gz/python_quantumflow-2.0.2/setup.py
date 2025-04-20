
from setuptools import setup, find_packages

# Using direct string for the long description to avoid file loading issues
long_description = """# Python QuantumFlow

A next-generation type-and-data-flow framework for Python with a lightweight footprint.

## Overview

Python QuantumFlow is a powerful yet lightweight framework that enhances Python's data flow capabilities.

## Features

| Feature | Version 1.x | Version 2.x |
|---------|------------|-------------|
| Type Conversion | Basic types only | Complex nested structures |
| Error Handling | Manual try/except | Automatic with @retry |
| Async Support | Limited | Full async/await |
"""

setup(
    name="python-quantumflow",
    version="2.0.2",
    author="Magi Sharma",
    author_email="magi@example.com",
    description="Python QuantumFlow: Advanced type conversion for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/magi8101/python-quantumflow",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[],
)
