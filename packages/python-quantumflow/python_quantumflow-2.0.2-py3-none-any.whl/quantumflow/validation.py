"""
Validation utilities for QuantumFlow.
"""

import ast
import importlib
import inspect
import os
import sys
from typing import Any, Dict, List, Optional, Set, Tuple

def validate_flows():
    """Validate all flow definitions in the current project."""
    # Find all Python files
    python_files = []
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    
    # Check each file for flow definitions
    valid_flows = 0
    invalid_flows = 0
    
    for file_path in python_files:
        try:
            # Parse the file
            with open(file_path, "r") as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            # Find all functions with @qflow decorator
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    has_qflow = False
                    
                    # Check for @qflow decorator
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Name) and decorator.id == "qflow":
                            has_qflow = True
                        elif isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name) and decorator.func.id == "qflow":
                            has_qflow = True
                    
                    if has_qflow:
                        # Validate the flow
                        if validate_flow_definition(node):
                            valid_flows += 1
                        else:
                            invalid_flows += 1
                            print(f"Invalid flow definition in {file_path}: {node.name}")
        
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
    
    print(f"Validation complete: {valid_flows} valid flows, {invalid_flows} invalid flows")
    
    return invalid_flows == 0

def validate_flow_definition(node: ast.FunctionDef) -> bool:
    """Validate a flow definition."""
    # Check for type annotations
    has_annotations = all(arg.annotation is not None for arg in node.args.args)
    
    # Check for docstring
    has_docstring = (len(node.body) > 0 and 
                    isinstance(node.body[0], ast.Expr) and 
                    isinstance(node.body[0].value, ast.Str))
    
    # Check for return statement
    has_return = any(isinstance(stmt, ast.Return) for stmt in ast.walk(node))
    
    # Check for return type annotation
    has_return_annotation = node.returns is not None
    
    # All checks must pass
    return has_annotations and has_docstring and has_return and has_return_annotation