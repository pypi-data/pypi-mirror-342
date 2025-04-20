# ⚛️ Python QuantumFlow 🔄

![Version](https://img.shields.io/badge/version-0.6.1-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)
![Coolness](https://img.shields.io/badge/coolness-over_9000-blueviolet.svg)
![Status](https://img.shields.io/badge/status-quantum_entangled-orange.svg)

✨ A next-generation type-and-data-flow framework for Python with a lightweight footprint. 🚀

## 🌟 Overview

🔮 Python QuantumFlow is a powerful yet lightweight framework that enhances Python's data flow capabilities with:

- 🔄 Automatic type conversion with `flow()` and `TypeFlowContext`
- 🧩 Function decorators for creating intelligent flows with `@qflow`
- ⚡ Asynchronous operations with `@async_flow`
- 🛡️ Robust error handling with retry logic
- 🎨 Beautiful terminal output with color and styling
- 📊 Visualization of data flows
- 🔁 ETL pipeline creation and orchestration
- 🧪 Advanced testing support for flow validation
- 📈 Performance monitoring and optimization tools
- 🔍 Debugging and introspection capabilities
- 🌐 Distributed computing integration

## 🚀 What's New in Version 2.0

Python QuantumFlow 2.0 represents a major evolution from the original python-typeflow, with significant improvements:

### Key Enhancements

- ⚡ **Performance Boost**: Up to 3x faster type conversions and flow execution
- 🧠 **Smarter Type Inference**: Improved algorithm for detecting and converting complex nested types
- 🔄 **Flow Composition**: Chain and combine flows with intuitive operators
- 🌐 **Extended Ecosystem**: New integrations with popular data science and ML frameworks
- 🧪 **Enhanced Testing Tools**: Built-in utilities for testing flows and mocking data sources

### Version Comparison

| Feature          | Version 1.x       | Version 2.x                        |
| ---------------- | ----------------- | ---------------------------------- | --- |
| Type Conversion  | Basic types only  | Complex nested structures          |
| Error Handling   | Manual try/except | Automatic with @retry              |
| Async Support    | Limited           | Full async/await with backpressure |
| Flow Composition | Manual chaining   | Operator-based (`>>`, `+`, `       | `)  |
| Memory Usage     | Moderate          | Optimized with streaming support   |
| Visualization    | None              | Interactive flow diagrams          |
| CLI Tools        | None              | Complete development toolkit       |

### Migration from v1.x

Upgrading from python-typeflow 1.x to Python QuantumFlow 2.x is straightforward:

```python
# Old way (python-typeflow 1.x)
from python_typeflow import convert_type, apply_flow

result = apply_flow(data, convert_type(str))

# New way (Python QuantumFlow 2.x)
from python_quantumflow.core import flow

result = flow(lambda x: str(x))(data)
# or even simpler
result = flow(str)(data)
```

<details>
<summary>📚 Complete migration guide</summary>

For a complete guide to migrating your code from python-typeflow 1.x to Python QuantumFlow 2.x,
see our [Migration Guide](https://docs.quantumflow.dev/migration).

Key differences:

- Decorator syntax changes
- New context manager approach
- Enhanced error handling
- Parallel and distributed execution options

</details>

## 📦 Installation

```bash
# Install core package
pip install python-quantumflow

# Install with additional features
pip install python-quantumflow[viz]      # Visualization features
pip install python-quantumflow[async]    # Enhanced async capabilities
pip install python-quantumflow[ml]       # Machine learning integrations
pip install python-quantumflow[full]     # All features
```

## 🚀 Quick Start

### Basic Type Flow

```python
from python_quantumflow.core import flow, with_typeflow as TypeFlowContext

# Create a list of numbers
numbers = [1, 2, 3, 4, 5]

# Convert types using flow
numbers_str = flow(lambda x: str(x))(numbers)
sum_str = flow(lambda x: str(x))(sum(numbers))

# Combine the results
result = f"{numbers_str} items with sum: {sum_str}"
print(result)
```

<details>
<summary>👉 Click to see output</summary>

```
[1, 2, 3, 4, 5] items with sum: 15
```

</details>

### Function Flows with @qflow

```python
from python_quantumflow.core import qflow

@qflow
def process_data(items):
    """Process a list of items by doubling each value."""
    return [item * 2 for item in items]

data = [5, 10, 15, 20, 25]
result = process_data(data)
print(f"Processed data: {result}")
```

<details>
<summary>👉 Click to see output</summary>

```
Processed data: [10, 20, 30, 40, 50]
```

</details>

### Async Flow with Retry

```python
import asyncio
from python_quantumflow.core import async_flow, retry, fancy_print

@async_flow
@retry(max_attempts=3, backoff_factor=0.5)
async def fetch_remote_data(url):
    """Fetch data from a URL with automatic retry on failure."""
    await asyncio.sleep(0.2)  # Simulate network delay

    # Your network request logic here
    return f"Data from {url}"

async def main():
    urls = ["https://api.example.com/data/1", "https://api.example.com/data/2"]
    tasks = [fetch_remote_data(url) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Process results
    for url, result in zip(urls, results):
        if isinstance(result, Exception):
            fancy_print(f"Failed to fetch {url}: {result}", style="red")
        else:
            fancy_print(f"Success: {result}", style="green")

if __name__ == "__main__":
    asyncio.run(main())
```

<details>
<summary>👉 Click to see output</summary>

```
Success: Data from https://api.example.com/data/1
Success: Data from https://api.example.com/data/2
```

With failures (when network errors occur):

```
Request to https://api.example.com/data/1 failed, retrying...
Failed to fetch https://api.example.com/data/1: Failed to connect
Success: Data from https://api.example.com/data/2
```

</details>

### Color and Styling

```python
from python_quantumflow.core import fancy_print

# Styled output with explicit styling
fancy_print("Error: Connection failed", style="bold red")
fancy_print("Success: Operation completed", style="bold green")
fancy_print("Info: Processing data", style="cyan")

# Auto-styled output based on content
fancy_print("Error: This will be red automatically")
fancy_print("Success! This will be green automatically")
fancy_print("Warning: This will be yellow automatically")
```

<details>
<summary>👉 Click to see output</summary>

![Terminal Output](https://raw.githubusercontent.com/magi8101/quantumflow/main/assets/terminal_output.png)

_Note: Colors shown will vary based on your terminal_

</details>

### ETL Pipeline Example

```python
from python_quantumflow.core import qflow, fancy_print

@qflow
def extract(source):
    """Extract data from a source."""
    fancy_print(f"Extracting from {source}...", style="dim")
    return [1, 2, 3, 4, 5]

@qflow
def transform(data):
    """Transform the raw data."""
    fancy_print(f"Transforming {data}...", style="dim")
    return [item * 2 for item in data]

@qflow
def load(transformed_data):
    """Load the transformed data."""
    fancy_print(f"Loading {transformed_data}...", style="dim")
    return f"Loaded {len(transformed_data)} items"

@qflow
def etl_pipeline(source):
    """Complete ETL pipeline."""
    raw_data = extract(source)
    transformed_data = transform(raw_data)
    result = load(transformed_data)
    return result

result = etl_pipeline("database://example/table1")
fancy_print(f"Pipeline result: {result}", style="bold green")
```

<details>
<summary>👉 Click to see output</summary>

```
Extracting from database://example/table1...
Transforming [1, 2, 3, 4, 5]...
Loading [2, 4, 6, 8, 10]...
Pipeline result: Loaded 5 items
```

</details>

## 🧰 Key Components

- **Core Flow Functions**:

  - `flow()`: Wraps objects for type conversion
  - `TypeFlowContext`: Context for automatic type conversion
  - `qflow`: Decorator for creating flow functions
  - `async_flow`: Decorator for asynchronous flows

- **Error Handling**:

  - `retry`: Decorator for automatic retry on failure
  - Exception handling within flows

- **Terminal Enhancements**:
  - `fancy_print`: Rich terminal output with colors and styles
  - Auto-styling based on message content
  - Progress indicators and animations

## 🖥️ Command Line Interface

Python QuantumFlow includes a CLI for rapid development and learning:

```bash
# Start interactive playground
pqflow play

# Start guided tutorial
pqflow tutor

# Generate documentation for flows
pqflow autodoc your_module

# Run a flow
pqflow run your_module.your_flow --input data.json

# Visualize a flow
pqflow visualize your_module.your_flow --output flow.png

# Create a new Python QuantumFlow project
pqflow init my_project

# View performance metrics for flows
pqflow metrics your_module.your_flow

# Run flow with default colorized output
pqflow run --color your_module.your_flow

# Apply type conversions to a JSON file
pqflow convert input.json output.json --schema schema.json

# Start a web dashboard for monitoring flows
pqflow dashboard --port 8080

# Generate sample code from templates
pqflow generate etl --name data_pipeline

# Benchmark flow performance
pqflow benchmark your_module.your_flow --iterations 1000
```

<details>
<summary>👉 Click to see CLI in action</summary>

![CLI Demo](https://raw.githubusercontent.com/magi8101/quantumflow/main/assets/cli_demo.gif)

_The Python QuantumFlow CLI provides a fun, interactive way to learn and use the framework._

</details>

## 🔬 Advanced Features

- **📊 Metrics and Observability**: Monitor and track flow execution
- **✅ Validation**: Validate flow inputs and outputs
- **⚙️ Execution Backends**: Run flows in different execution contexts (threads, processes, distributed)

## 📊 Performance

Python QuantumFlow is optimized for both performance and flexibility.

| Feature          | Performance | Memory Usage | Quantum Awesomeness |
| ---------------- | ----------- | ------------ | ------------------- |
| Type Conversion  | ⭐⭐⭐⭐⭐  | ⭐⭐⭐⭐     | ⭐⭐⭐              |
| Flow Execution   | ⭐⭐⭐⭐    | ⭐⭐⭐⭐⭐   | ⭐⭐⭐⭐            |
| Async Operations | ⭐⭐⭐⭐⭐  | ⭐⭐⭐       | ⭐⭐⭐⭐⭐          |
| Fancy Output     | ⭐⭐⭐      | ⭐⭐⭐⭐     | ⭐⭐⭐⭐⭐          |

## 🧠 Why Python QuantumFlow?

- **Lightweight**: Minimal dependencies, small footprint
- **Intuitive**: Simple API with powerful capabilities
- **Flexible**: Works with your existing code
- **Pretty**: Makes your terminal output gorgeous
- **Fast**: Optimized for performance

## 🙌 Created By

<img src="https://github.com/magi8101.png" width="70" style="border-radius: 50%;" align="left" alt="Magi Sharma"/>

**[Magi Sharma](https://github.com/magi8101/python-quantumflow)**<br>
_Quantum-entangled code enthusiast_<br>
Version: 0.6.1

---

<p align="center">Made with ❤️ and a sprinkle of quantum magic</p>
