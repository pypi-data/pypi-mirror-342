
from setuptools import setup, find_packages

# Using the existing README_PYPI.md content
long_description = """
# Python QuantumFlow

A next-generation type-and-data-flow framework for Python with a lightweight footprint.

## Overview

Python QuantumFlow is a powerful yet lightweight framework that enhances Python's data flow capabilities with:

- Automatic type conversion with `flow()` and `TypeFlowContext`
- Function decorators for creating intelligent flows with `@qflow`
- Asynchronous operations with `@async_flow`
- Robust error handling with retry logic
- Beautiful terminal output with color and styling

## Installation

```bash
pip install python-quantumflow
```

## Features Comparison

Version 1.x vs Version 2.x:

| Feature           | python-typeflow V1                  | Python QuantumFlow V2              |
|-------------------|-------------------------------------|-------------------------------------|
| Type Conversion   | Basic types only                    | Complex nested structures           |
| Error Handling    | Manual try/except                   | Automatic with @retry               |
| Async Support     | Limited                             | Full async/await with backpressure  |
| Flow Composition  | Manual chaining                     | Operator-based (>>, +, etc.)        |
| Memory Usage      | Moderate                            | Optimized with streaming support    |
| Visualization     | None                                | Interactive flow diagrams           |
| CLI Tools         | None                                | Complete development toolkit        |
| Terminal Output   | Plain text                          | Rich colors and animations          |
| Testing Support   | Minimal                             | Comprehensive mocking framework     |
| Performance       | Standard                            | Up to 3x faster                     |

## Quick Start

```python
from python_quantumflow.core import flow, qflow

# Simple type conversion
numbers = [1, 2, 3, 4, 5]
str_numbers = flow(str)(numbers)
print(str_numbers)  # "[1, 2, 3, 4, 5]"

# Function decorator for automatic flow
@qflow
def process_data(items):
    return [item * 2 for item in items]

result = process_data(numbers)
print(result)  # [2, 4, 6, 8, 10]
```

## Documentation

For detailed documentation and examples, visit:
- [GitHub Repository](https://github.com/magi8101/python-quantumflow)
- [API Reference](https://python-quantumflow.readthedocs.io/)

## Made by

Created with ❤️ by Magi Sharma


"""

setup(
    name="python-quantumflow",
    version="2.0.3",
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
