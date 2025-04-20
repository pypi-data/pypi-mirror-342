"""
Python QuantumFlow: Advanced type conversion and flow control for Python

A lightweight yet powerful framework for handling data flow and type conversions
with a focus on elegance and performance.
"""

import sys
import random
import importlib.metadata

try:
    __version__ = importlib.metadata.version("python-quantumflow")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.6.1"  # Default version if not installed via pip

# Import core components to make them available at package level
from .core import flow, qflow, with_typeflow

# Display signature when the module is imported
def _display_signature():
    # ANSI color codes for terminal output
    RESET = "\033[0m"
    BOLD = "\033[1m"
    MAGENTA = "\033[35m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    
    # Random quantum-inspired emoji
    quantum_emojis = ["⚛️", "🔄", "✨", "🌌", "🔮", "🧪", "🚀", "💫", "⚡", "🌠"]
    emoji = random.choice(quantum_emojis)
    
    # Only display in interactive mode or when running a script
    if not sys.argv[0].endswith("pytest") and not sys.argv[0].endswith("sphinx-build"):
        print(f"\n{BOLD}{MAGENTA}────────────────────────────────────────{RESET}")
        print(f"{BOLD}{BLUE}{emoji} Powered by Python QuantumFlow v{__version__}{RESET}")
        print(f"{CYAN}Created with quantum precision by Magi Sharma{RESET}")
        print(f"{BOLD}{MAGENTA}────────────────────────────────────────{RESET}\n")

# Display the signature when imported
_display_signature()

# Clean up namespace
del _display_signature
del random
del sys
del importlib