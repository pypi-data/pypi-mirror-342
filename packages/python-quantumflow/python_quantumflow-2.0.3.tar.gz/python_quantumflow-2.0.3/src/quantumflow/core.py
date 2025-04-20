"""
Python QuantumFlow Core Module

This module provides the core functionality of Python QuantumFlow,
including type conversion and flow control.
"""

import functools
import logging
import time
import random
import asyncio
import atexit
import sys
import inspect
from typing import Any, Callable, Type, TypeVar, Union, get_type_hints

# ANSI color codes for terminal output
RESET = "\033[0m"
BOLD = "\033[1m"
MAGENTA = "\033[35m"
BLUE = "\033[34m"
CYAN = "\033[36m"

# Signature string
SIGNATURE = f"\n{BOLD}{MAGENTA}────────────────────────────────────────{RESET}\n{CYAN}Created with Python QuantumFlow by Magi Sharma{RESET}"

from .config import config, EffectType, success, error, warning, info, highlight, code

T = TypeVar('T')

def flow(target_type: Type[T]) -> Callable[[Any], T]:
    """
    Create a flow function that converts the input to the specified target type.
    
    Args:
        target_type: The type to convert to.
        
    Returns:
        A function that takes an input and returns it converted to the target type.
    """
    def converter(value: Any) -> T:
        # Apply colorization if enabled
        if config.get_effect(EffectType.COLORIZE):
            print(info(f"Converting {highlight(str(type(value).__name__))} to {highlight(str(target_type.__name__))}"))
        
        # Apply conversion logic
        try:
            # Simple case: already the correct type
            if isinstance(value, target_type):
                return value
            
            # Try to convert using the target type constructor
            result = target_type(value)
            
            # Show success message if colorize is enabled
            if config.get_effect(EffectType.COLORIZE):
                print(success(f"Successfully converted to {highlight(str(target_type.__name__))}"))
            
            return result
        except Exception as e:
            # Apply error handling if enabled
            if config.get_effect(EffectType.ERROR_HANDLING):
                print(error(f"Conversion error: {str(e)}"))
                # Could implement retry logic or fallback here
            raise
    
    return converter

def qflow(func: Callable) -> Callable:
    """
    Decorator that applies Python QuantumFlow effects to a function.
    
    This decorator enables automatic type conversion based on type hints,
    error handling, and colorized output.
    
    Args:
        func: The function to decorate.
        
    Returns:
        The decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Apply auto-conversion effect if enabled
        if config.get_effect(EffectType.AUTO_CONVERSION):
            # Get type hints for the function
            hints = get_type_hints(func)
            
            # Get the parameter names
            sig = inspect.signature(func)
            param_names = list(sig.parameters.keys())
            
            # Convert positional arguments based on type hints
            converted_args = list(args)
            for i, arg in enumerate(args):
                if i < len(param_names):
                    param_name = param_names[i]
                    if param_name in hints:
                        target_type = hints[param_name]
                        # Apply the flow conversion
                        try:
                            converted_args[i] = flow(target_type)(arg)
                        except:
                            # If conversion fails, keep original value
                            pass
            
            # Convert keyword arguments based on type hints
            converted_kwargs = {}
            for key, value in kwargs.items():
                if key in hints:
                    target_type = hints[key]
                    try:
                        converted_kwargs[key] = flow(target_type)(value)
                    except:
                        # If conversion fails, keep original value
                        converted_kwargs[key] = value
                else:
                    converted_kwargs[key] = value
            
            # Call the function with converted arguments
            result = func(*converted_args, **converted_kwargs)
        else:
            # If auto-conversion is disabled, just call the function normally
            result = func(*args, **kwargs)
        
        # Show signature if colorize effect is enabled
        if config.get_effect(EffectType.COLORIZE):
            print(SIGNATURE)
            
        return result
    
    return wrapper

def with_typeflow():
    """
    Context manager for QuantumFlow operations.
    
    This enables automatic type conversion within the context block.
    
    Returns:
        A context manager object.
    """
    class TypeFlowContext:
        def __enter__(self):
            # Enable all effects when entering the context
            for effect in EffectType:
                config.set_effect(effect, True)
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            # Keep effects enabled when exiting
            return False
    
    return TypeFlowContext()

def async_flow(func):
    """
    Decorator for async functions to make them part of a flow.
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await func(*args, **kwargs)
    return wrapper

def retry(max_attempts=3, backoff_factor=0.5, exceptions=(Exception,)):
    """
    Decorator to retry a function if it raises specified exceptions.
    
    Args:
        max_attempts: Maximum number of retry attempts
        backoff_factor: Exponential backoff factor
        exceptions: Tuple of exceptions to catch and retry
    """
    def decorator(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        sleep_time = backoff_factor * (2 ** attempt) + random.uniform(0, 0.1)
                        await asyncio.sleep(sleep_time)
                    else:
                        raise last_exception
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        sleep_time = backoff_factor * (2 ** attempt) + random.uniform(0, 0.1)
                        time.sleep(sleep_time)
                    else:
                        raise last_exception
        
        # Choose the appropriate wrapper based on whether the function is async
        if inspect.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    
    return decorator

def configure_logging(level="INFO", fancy=False):
    """Configure basic logging."""
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {level}")
    logging.basicConfig(level=numeric_level)

def fancy_print(message, style=None, end="\n"):
    """Print with styling using ANSI color codes for terminal output.
    
    If style is not provided, will attempt to apply default styling based on message content.
    """
    # Define ANSI color codes
    COLORS = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "bold": "\033[1m",
        "dim": "\033[2m",
        "italic": "\033[3m",
        "underline": "\033[4m",
        "reset": "\033[0m"
    }
    
    # Auto-detect style if none provided
    if style is None:
        message_lower = message.lower()
        
        # Apply default styling based on message content
        if any(kw in message_lower for kw in ["error", "failed", "exception", "crash"]):
            style = "bold red"
        elif any(kw in message_lower for kw in ["warning", "caution", "attention"]):
            style = "bold yellow"
        elif any(kw in message_lower for kw in ["success", "completed", "done", "finished"]):
            style = "bold green"
        elif any(kw in message_lower for kw in ["info", "note", "notice"]):
            style = "cyan"
        elif any(kw in message_lower for kw in ["debug", "trace"]):
            style = "dim"
        elif any(kw in message_lower for kw in ["important", "critical"]):
            style = "bold magenta"
        elif message.isupper():  # ALL CAPS text gets bold styling
            style = "bold"
        elif message.startswith(("=>", "->", ">>", "-->")):  # Arrow indicators
            style = "bold blue"
        elif message.startswith(("# ", "## ", "### ")):  # Heading-like text
            heading_level = message.count('#')
            if heading_level == 1:
                style = "bold magenta"
            elif heading_level == 2:
                style = "bold blue"
            else:
                style = "bold cyan"
        else:
            # Default effects for normal text - subtle gradient effect across the text
            return _gradient_print(message, end=end)
    
    if style:
        # Parse multiple styles (e.g., "bold red")
        style_parts = style.split()
        codes = ""
        for part in style_parts:
            if part in COLORS:
                codes += COLORS[part]
        
        # Apply style and reset after the message
        print(f"{codes}{message}{COLORS['reset']}", end=end)
    else:
        print(message, end=end)

def _gradient_print(text, start_color=(70, 130, 180), end_color=(138, 43, 226), end="\n"):
    """Print text with a color gradient using ANSI RGB color codes."""
    start_r, start_g, start_b = start_color
    end_r, end_g, end_b = end_color
    result = ""
    
    for i, char in enumerate(text):
        # Calculate the gradient position
        ratio = i / (len(text) - 1) if len(text) > 1 else 0
        
        # Interpolate between start and end colors
        r = int(start_r + (end_r - start_r) * ratio)
        g = int(start_g + (end_g - start_g) * ratio)
        b = int(start_b + (end_b - start_b) * ratio)
        
        # Add the colored character
        result += f"\033[38;2;{r};{g};{b}m{char}"
    
    # Reset color at the end
    print(f"{result}\033[0m", end=end)
    return True

def print_author_credit(small=True):
    """Print a small credit line with the author's name.
    
    This function can be called at the end of scripts to provide attribution.
    """
    if small:
        # Subtle, small attribution
        print("\n\033[38;2;180;180;180m" + "─" * 40 + "\033[0m")
        print("\033[38;2;180;180;180mCreated with QuantumFlow by Magi Sharma\033[0m")
    else:
        # More elaborate attribution with gradient
        author_text = "Created by Magi Sharma"
        framework_text = "QUANTUMFLOW FRAMEWORK"
        version_text = "v0.6.1"
        
        print("\n" + "─" * 50)
        
        # Print author with gradient
        result = ""
        start_r, start_g, start_b = 255, 215, 0  # Gold
        end_r, end_g, end_b = 255, 140, 0  # Dark orange
        
        for i, char in enumerate(author_text):
            ratio = i / (len(author_text) - 1) if len(author_text) > 1 else 0
            r = int(start_r + (end_r - start_r) * ratio)
            g = int(start_g + (end_g - start_g) * ratio)
            b = int(start_b + (end_b - start_b) * ratio)
            result += f"\033[38;2;{r};{g};{b}m{char}"
        
        print(f"{result}\033[0m")
        
        # Print framework name with different gradient
        result = ""
        start_r, start_g, start_b = 0, 191, 255  # Deep sky blue
        end_r, end_g, end_b = 138, 43, 226  # Purple
        
        for i, char in enumerate(framework_text):
            ratio = i / (len(framework_text) - 1) if len(framework_text) > 1 else 0
            r = int(start_r + (end_r - start_r) * ratio)
            g = int(start_g + (end_g - start_g) * ratio)
            b = int(start_b + (end_b - start_b) * ratio)
            result += f"\033[38;2;{r};{g};{b}m{char}"
        
        print(f"{result} \033[38;2;150;150;150m{version_text}\033[0m")
        print("─" * 50)

def _show_credits_on_exit():
    """Show small author credits when the program exits."""
    # Only show on regular exits, not errors or interrupts
    if sys.exc_info()[0] is None:
        print_author_credit(small=True)

# Register the exit handler
atexit.register(_show_credits_on_exit)

def create_progress(description=None):
    """Create a simple progress indicator."""
    return None  # Fallback to simple printing

# Add console object for compatibility
console = None