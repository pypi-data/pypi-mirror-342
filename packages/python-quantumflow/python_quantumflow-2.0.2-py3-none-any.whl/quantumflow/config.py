"""
QuantumFlow Configuration Module

This module handles configuration settings for QuantumFlow, including
default effects and color themes.
"""

import os
from enum import Enum
from typing import Dict, Any, Optional
import json

# ANSI color codes for terminal output
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    
    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    
    # Bright variants
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"


class EffectType(Enum):
    AUTO_CONVERSION = "auto_conversion"
    TYPE_CHECKING = "type_checking"
    ERROR_HANDLING = "error_handling"
    LOGGING = "logging"
    COLORIZE = "colorize"


# Default configuration
DEFAULT_CONFIG = {
    "effects": {
        EffectType.AUTO_CONVERSION.value: True,
        EffectType.TYPE_CHECKING.value: True,
        EffectType.ERROR_HANDLING.value: True,
        EffectType.LOGGING.value: True,
        EffectType.COLORIZE.value: True,
    },
    "colors": {
        "success": Colors.GREEN,
        "error": Colors.RED,
        "warning": Colors.YELLOW,
        "info": Colors.BLUE,
        "highlight": Colors.MAGENTA,
        "code": Colors.CYAN,
    },
    "terminal_output": True
}


class QuantumFlowConfig:
    """Configuration manager for QuantumFlow."""
    
    _instance = None
    _config: Dict[str, Any] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(QuantumFlowConfig, cls).__new__(cls)
            cls._instance._config = DEFAULT_CONFIG.copy()
            cls._instance._load_user_config()
        return cls._instance
    
    def _load_user_config(self):
        """Load user configuration from file if it exists."""
        config_path = os.path.expanduser("~/.quantumflow/config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                # Update only existing keys to prevent invalid settings
                for section, settings in user_config.items():
                    if section in self._config:
                        if isinstance(settings, dict):
                            self._config[section].update(settings)
                        else:
                            self._config[section] = settings
            except (json.JSONDecodeError, IOError):
                # If there's an error, just use defaults
                pass
    
    def save_config(self):
        """Save current configuration to user config file."""
        config_dir = os.path.expanduser("~/.quantumflow")
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        
        config_path = os.path.join(config_dir, "config.json")
        with open(config_path, 'w') as f:
            json.dump(self._config, f, indent=2)
    
    def get_effect(self, effect_type: EffectType) -> bool:
        """Get whether an effect is enabled."""
        return self._config["effects"].get(effect_type.value, False)
    
    def set_effect(self, effect_type: EffectType, enabled: bool):
        """Enable or disable an effect."""
        self._config["effects"][effect_type.value] = enabled
    
    def get_color(self, color_name: str) -> str:
        """Get a color code by name."""
        return self._config["colors"].get(color_name, Colors.RESET)
    
    def set_color(self, color_name: str, color_code: str):
        """Set a color code by name."""
        self._config["colors"][color_name] = color_code
    
    def is_terminal_output_enabled(self) -> bool:
        """Check if terminal colored output is enabled."""
        return self._config.get("terminal_output", True)
    
    def set_terminal_output(self, enabled: bool):
        """Enable or disable terminal colored output."""
        self._config["terminal_output"] = enabled
    
    def reset_to_defaults(self):
        """Reset configuration to default values."""
        self._config = DEFAULT_CONFIG.copy()


# Create a global configuration instance
config = QuantumFlowConfig()


def colorize(text: str, color_name: str) -> str:
    """Colorize text if terminal output is enabled."""
    if not config.is_terminal_output_enabled():
        return text
    
    color = config.get_color(color_name)
    return f"{color}{text}{Colors.RESET}"


def success(text: str) -> str:
    """Format text as success message."""
    return colorize(text, "success")


def error(text: str) -> str:
    """Format text as error message."""
    return colorize(text, "error")


def warning(text: str) -> str:
    """Format text as warning message."""
    return colorize(text, "warning")


def info(text: str) -> str:
    """Format text as info message."""
    return colorize(text, "info")


def highlight(text: str) -> str:
    """Format text as highlighted."""
    return colorize(text, "highlight")


def code(text: str) -> str:
    """Format text as code."""
    return colorize(text, "code")
