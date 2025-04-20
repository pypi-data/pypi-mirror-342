"""
Command-line interface for QuantumFlow.
"""

import argparse
import asyncio
import code
import importlib
import inspect
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional

from . import __version__, flow, TypeFlowContext, qflow, visualize_flow, fancy_print, is_fancy_output_available
from .core import configure_logging

logger = logging.getLogger("quantumflow")

class QuantumPlayground:
    """Interactive REPL for experimenting with QuantumFlow."""
    
    def __init__(self):
        self.context = {}
        self.history = []
    
    def start(self):
        """Start the playground."""
        print("Welcome to QuantumFlow Playground!")
        print("Type 'help' for assistance or 'exit' to quit.")
        
        # Set up the context with QuantumFlow imports
        self.context = {
            "flow": flow,
            "TypeFlowContext": TypeFlowContext,
            "qflow": qflow,
            "visualize_flow": visualize_flow,
        }
        
        # Create a console with the context
        console = code.InteractiveConsole(self.context)
        console.interact(banner="", exitmsg="Goodbye from QuantumFlow Playground!")

class FlowTutor:
    """Guided wizard for learning QuantumFlow concepts."""
    
    def __init__(self):
        self.lessons = [
            {
                "name": "Introduction to TypeFlow",
                "description": "Learn the basics of TypeFlow and how to use flow() and TypeFlowContext.",
                "steps": [
                    {
                        "instruction": "Let's start by importing the basic components:",
                        "code": "from quantumflow import flow, TypeFlowContext",
                        "expected_output": None
                    },
                    {
                        "instruction": "Now, let's try a simple type conversion:",
                        "code": "with TypeFlowContext():\n    result = flow(42) + ' is the answer'\n    print(result)",
                        "expected_output": "42 is the answer"
                    },
                    {
                        "instruction": "Without TypeFlowContext, this would raise an error:",
                        "code": "try:\n    result = 42 + ' is the answer'\n    print(result)\nexcept TypeError as e:\n    print(f'Error: {e}')",
                        "expected_output": "Error: unsupported operand type(s) for +: 'int' and 'str'"
                    }
                ]
            },
            {
                "name": "Creating Flows with @qflow",
                "description": "Learn how to create and visualize flows using the @qflow decorator.",
                "steps": [
                    {
                        "instruction": "Let's import the necessary components:",
                        "code": "from quantumflow import qflow, visualize_flow",
                        "expected_output": None
                    },
                    {
                        "instruction": "Now, let's define a simple flow:",
                        "code": "@qflow\ndef process_data(data):\n    return [item.upper() for item in data]\n\nresult = process_data(['hello', 'world'])\nprint(result)",
                        "expected_output": "['HELLO', 'WORLD']"
                    },
                    {
                        "instruction": "We can visualize the flow:",
                        "code": "# This would show a graph in a GUI window\n# visualize_flow(process_data)\nprint('Flow visualization would appear in a GUI window')",
                        "expected_output": "Flow visualization would appear in a GUI window"
                    }
                ]
            },
            {
                "name": "Advanced Flow Features",
                "description": "Learn about fancy output, async flows, and retry logic.",
                "steps": [
                    {
                        "instruction": "Let's explore fancy terminal output:",
                        "code": "from quantumflow import fancy_print, create_progress\nimport time\n\nfancy_print('This is styled text!', style='bold magenta')\nfancy_print('Error messages stand out', style='bold red')\nfancy_print('Success messages too', style='bold green')",
                        "expected_output": None
                    },
                    {
                        "instruction": "Now let's try a progress bar:",
                        "code": "progress = create_progress('Processing')\nif progress:\n    with progress:\n        task = progress.add_task('Working...', total=10)\n        for i in range(10):\n            time.sleep(0.2)  # Simulate work\n            progress.update(task, advance=1)\n    fancy_print('Processing complete!', style='green')\nelse:\n    print('Rich library not available for fancy progress bars')",
                        "expected_output": None
                    },
                    {
                        "instruction": "Let's create an async flow with retry logic:",
                        "code": "import asyncio\nimport random\nfrom quantumflow import async_flow, retry\n\n@async_flow\n@retry(max_attempts=3, backoff_factor=0.5)\nasync def fetch_data(url):\n    # Simulate network request\n    await asyncio.sleep(0.2)\n    # Randomly fail to demonstrate retry\n    if random.random() < 0.5:\n        raise ConnectionError('Network error')\n    return f'Data from {url}'\n\n# We'll just define it, not run it since this is synchronous code\nfancy_print('Async flow with retry defined!', style='bold blue')",
                        "expected_output": None
                    }
                ]
            },
            {
                "name": "Building Data Pipelines",
                "description": "Learn how to chain flows to create data processing pipelines.",
                "steps": [
                    {
                        "instruction": "Let's define multiple flows that work together:",
                        "code": "from quantumflow import qflow\nfrom typing import List, Dict\n\n@qflow\ndef extract(source: str) -> List[str]:\n    \"\"\"Extract data from a source.\"\"\"\n    # Simulate data extraction\n    return [f'record-{i}' for i in range(1, 6)]\n\n@qflow\ndef transform(data: List[str]) -> List[Dict]:\n    \"\"\"Transform raw data into structured format.\"\"\"\n    return [{'id': item, 'processed': True, 'value': len(item)} for item in data]\n\n@qflow\ndef load(items: List[Dict]) -> str:\n    \"\"\"Load processed data into a destination.\"\"\"\n    # Simulate loading data\n    return f'Successfully loaded {len(items)} items'\n\n@qflow\ndef etl_pipeline(source: str) -> str:\n    \"\"\"Complete ETL pipeline.\"\"\"\n    raw_data = extract(source)\n    transformed_data = transform(raw_data)\n    result = load(transformed_data)\n    return result\n\n# Run the pipeline\nresult = etl_pipeline('sample-data')\nfancy_print(f'Pipeline result: {result}', style='bold green')",
                        "expected_output": None
                    }
                ]
            }
        ]
        self.current_lesson = 0
        self.current_step = 0
        # Flag to use fancy output if available
        self.use_fancy_output = is_fancy_output_available()
    
    def start(self):
        """Start the tutor."""
        if self.use_fancy_output:
            fancy_print("Welcome to QuantumFlow Tutor!", style="bold cyan")
            fancy_print("This guided tutorial will help you learn QuantumFlow concepts.", style="cyan")
        else:
            print("Welcome to QuantumFlow Tutor!")
            print("This guided tutorial will help you learn QuantumFlow concepts.")
        
        while self.current_lesson < len(self.lessons):
            lesson = self.lessons[self.current_lesson]
            
            if self.use_fancy_output:
                fancy_print(f"\nLesson {self.current_lesson + 1}: {lesson['name']}", style="bold magenta")
                fancy_print(lesson['description'], style="magenta")
            else:
                print(f"\nLesson {self.current_lesson + 1}: {lesson['name']}")
                print(lesson['description'])
            
            self.current_step = 0
            while self.current_step < len(lesson['steps']):
                step = lesson['steps'][self.current_step]
                
                if self.use_fancy_output:
                    fancy_print(f"\nStep {self.current_step + 1}:", style="bold blue")
                    fancy_print(step['instruction'], style="blue")
                    fancy_print("\nCode:", style="bold yellow")
                    
                    # Try to use Rich syntax highlighting if available
                    try:
                        from rich.syntax import Syntax
                        from rich.console import Console
                        console = Console()
                        syntax = Syntax(step['code'], "python", theme="monokai", line_numbers=True)
                        console.print(syntax)
                    except ImportError:
                        fancy_print(step['code'], style="yellow")
                else:
                    print(f"\nStep {self.current_step + 1}:")
                    print(step['instruction'])
                    print("\nCode:")
                    print(step['code'])
                
                if self.use_fancy_output:
                    fancy_print("\nPress Enter to execute this code...", style="dim")
                else:
                    input("\nPress Enter to execute this code...")
                
                # Execute the code
                try:
                    exec(step['code'])
                    if self.use_fancy_output:
                        fancy_print("Code executed successfully!", style="bold green")
                except Exception as e:
                    if self.use_fancy_output:
                        fancy_print(f"Error: {e}", style="bold red")
                    else:
                        print(f"Error: {e}")
                
                # Move to the next step
                self.current_step += 1
            
            # Move to the next lesson
            self.current_lesson += 1
            
            if self.current_lesson < len(self.lessons):
                if self.use_fancy_output:
                    fancy_print("\nReady for the next lesson? (y/n): ", style="bold cyan", end="")
                choice = input("\nReady for the next lesson? (y/n): " if not self.use_fancy_output else "")
                if choice.lower() != 'y':
                    break
        
        if self.use_fancy_output:
            fancy_print("\nTutorial completed! You've learned the basics of QuantumFlow.", style="bold green")
        else:
            print("\nTutorial completed! You've learned the basics of QuantumFlow.")

class AutoDoc:
    """Automatic documentation generator for flows."""
    
    def __init__(self, output_dir: str = "docs"):
        self.output_dir = output_dir
    
    def generate(self, module_paths: List[str]):
        """Generate documentation for flows in the specified modules."""
        os.makedirs(self.output_dir, exist_ok=True)
        
        for module_path in module_paths:
            try:
                module = importlib.import_module(module_path)
                
                # Find all flow functions in the module
                flows = []
                for name, obj in inspect.getmembers(module):
                    if hasattr(obj, "flow"):
                        flows.append((name, obj))
                
                if flows:
                    # Create a markdown file for the module
                    with open(os.path.join(self.output_dir, f"{module_path}.md"), "w") as f:
                        f.write(f"# {module_path}\n\n")
                        
                        for name, flow_func in flows:
                            f.write(f"## {name}\n\n")
                            
                            # Add docstring
                            if flow_func.__doc__:
                                f.write(f"{flow_func.__doc__.strip()}\n\n")
                            
                            # Add signature
                            sig = inspect.signature(flow_func)
                            f.write(f"```python\n{name}{sig}\n```\n\n")
                            
                            # Add type hints
                            if hasattr(flow_func, "flow") and hasattr(flow_func.flow, "type_hints"):
                                f.write("### Type Hints\n\n")
                                for param, type_hint in flow_func.flow.type_hints.items():
                                    if param != "return":
                                        f.write(f"- `{param}`: `{type_hint}`\n")
                                if "return" in flow_func.flow.type_hints:
                                    f.write(f"- Returns: `{flow_func.flow.type_hints['return']}`\n")
                                f.write("\n")
                            
                            # Generate a graph visualization
                            if hasattr(flow_func, "flow"):
                                graph_path = os.path.join(self.output_dir, f"{module_path}_{name}_graph.png")
                                try:
                                    flow_func.flow.visualize(output=graph_path)
                                    f.write(f"### Flow Graph\n\n")
                                    f.write(f"![{name} Graph]({os.path.basename(graph_path)})\n\n")
                                except Exception as e:
                                    logger.warning(f"Failed to generate graph for {name}: {e}")
                    
                    print(f"Documentation generated for {module_path} with {len(flows)} flows")
                else:
                    print(f"No flows found in {module_path}")
            
            except ImportError:
                print(f"Could not import module {module_path}")
            except Exception as e:
                print(f"Error processing module {module_path}: {e}")

def main():
    """Main entry point for the QuantumFlow CLI."""
    parser = argparse.ArgumentParser(description="QuantumFlow: Next-gen type-and-data-flow framework for Python")
    parser.add_argument("--version", action="store_true", help="Show version information")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--no-fancy", action="store_true", help="Disable fancy terminal output")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Play command
    play_parser = subparsers.add_parser("play", help="Start the interactive playground")
    
    # Tutor command
    tutor_parser = subparsers.add_parser("tutor", help="Start the guided tutorial")
    
    # AutoDoc command
    autodoc_parser = subparsers.add_parser("autodoc", help="Generate documentation for flows")
    autodoc_parser.add_argument("modules", nargs="+", help="Module paths to document")
    autodoc_parser.add_argument("--output", default="docs", help="Output directory for documentation")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Run a flow")
    run_parser.add_argument("flow", help="Flow to run (module.function)")
    run_parser.add_argument("--input", help="Input data as JSON")
    
    # Visualize command
    viz_parser = subparsers.add_parser("visualize", help="Visualize a flow")
    viz_parser.add_argument("flow", help="Flow to visualize (module.function)")
    viz_parser.add_argument("--output", help="Output file path")
    viz_parser.add_argument("--format", default="png", choices=["png", "svg", "pdf"], help="Output format")
    
    args = parser.parse_args()
    
    # Configure logging with fancy output unless disabled
    log_level = logging.DEBUG if args.verbose else logging.INFO
    fancy_output = not args.no_fancy
    configure_logging(log_level, fancy=fancy_output)
    
    if args.version:
        if fancy_output and is_fancy_output_available():
            fancy_print(f"QuantumFlow version {__version__}", style="bold cyan")
        else:
            print(f"QuantumFlow version {__version__}")
        return 0
    
    # Enhanced CLI output for commands
    if args.command == "play":
        if fancy_output and is_fancy_output_available():
            fancy_print("Starting QuantumFlow Playground...", style="bold green")
        playground = QuantumPlayground()
        playground.start()
    elif args.command == "tutor":
        if fancy_output and is_fancy_output_available():
            fancy_print("Starting QuantumFlow Tutorial...", style="bold green")
        tutor = FlowTutor()
        tutor.start()
    elif args.command == "autodoc":
        if fancy_output and is_fancy_output_available():
            fancy_print(f"Generating documentation for modules: {', '.join(args.modules)}", style="bold green")
        autodoc = AutoDoc(output_dir=args.output)
        autodoc.generate(args.modules)
    elif args.command == "run":
        try:
            if fancy_output and is_fancy_output_available():
                fancy_print(f"Running flow: {args.flow}", style="bold green")
            
            module_name, func_name = args.flow.rsplit(".", 1)
            module = importlib.import_module(module_name)
            flow_func = getattr(module, func_name)
            
            input_data = None
            if args.input:
                if fancy_output and is_fancy_output_available():
                    fancy_print(f"Loading input data from: {args.input}", style="dim")
                with open(args.input, "r") as f:
                    input_data = json.load(f)
            
            if asyncio.iscoroutinefunction(flow_func):
                result = asyncio.run(flow_func(input_data) if input_data else flow_func())
            else:
                result = flow_func(input_data) if input_data else flow_func()
            
            if fancy_output and is_fancy_output_available():
                fancy_print("Result:", style="bold green")
                
                # Import rich.json only if available and needed
                try:
                    from rich.json import JSON
                    from rich.console import Console
                    console = Console()
                    console.print(JSON(json.dumps(result)))
                except ImportError:
                    print(json.dumps(result, indent=2))
            else:
                print(json.dumps(result, indent=2))
        except Exception as e:
            if fancy_output and is_fancy_output_available():
                fancy_print(f"Error running flow: {e}", style="bold red")
            else:
                print(f"Error running flow: {e}")
            return 1
    elif args.command == "visualize":
        try:
            if fancy_output and is_fancy_output_available():
                fancy_print(f"Visualizing flow: {args.flow}", style="bold green")
            
            module_name, func_name = args.flow.rsplit(".", 1)
            module = importlib.import_module(module_name)
            flow_func = getattr(module, func_name)
            
            visualize_flow(flow_func, format=args.format, output=args.output)
            
            if args.output:
                if fancy_output and is_fancy_output_available():
                    fancy_print(f"Flow visualization saved to: {args.output}", style="bold green")
                else:
                    print(f"Flow visualization saved to {args.output}")
        except Exception as e:
            if fancy_output and is_fancy_output_available():
                fancy_print(f"Error visualizing flow: {e}", style="bold red")
            else:
                print(f"Error visualizing flow: {e}")
            return 1
    else:
        parser.print_help()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())