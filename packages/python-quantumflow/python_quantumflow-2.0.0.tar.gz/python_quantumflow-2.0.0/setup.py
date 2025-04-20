#!/usr/bin/env python
import os
from setuptools import setup, find_packages, Command
from setuptools.command.develop import develop
from setuptools.command.install import install
import shutil
import sys
import io

# Use io.open with explicit encoding to avoid UnicodeDecodeError
with io.open("README.md", encoding="utf-8") as f:
    long_description = f.read()

class VerifyFlowsCommand(Command):
    """Custom command to verify all .qflow definitions."""
    description = "Lint and validate all .qflow definitions"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run the verification process."""
        print("Verifying flow definitions...")
        try:
            from src.quantumflow.validation import validate_flows
            validate_flows()
            print("All flows verified successfully!")
        except ImportError:
            print("Error: quantumflow package not installed. Install the package first.")
            sys.exit(1)
        except Exception as e:
            print(f"Error verifying flows: {e}")
            sys.exit(1)

setup(
    name="python-quantumflow",
    version="2.0.0",
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
    install_requires=[
        # Add dependencies here
    ],
)