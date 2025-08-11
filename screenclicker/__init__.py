"""
ScreenClicker - Minimal screen automation library for Wayland/Linux

Simple API for mouse clicks, cursor movement, and text input on Wayland systems.

Key features:
- Mouse clicks and cursor movement using uinput and ydotool
- Text input using uinput virtual keyboards  
- Screen capture using grim
- Multi-monitor support via swaymsg
- Works on Wayland without elevated permissions (with ydotool)

System dependencies:
- ydotool: For cursor movement (sudo apt install ydotool)
- grim: For screenshots (sudo apt install grim)
"""

from .mouse import right_click, left_click, move_mouse
from .keyboard import text
from .screen import screenshot, screenshot_region, get_screen_info, screenshot_monitor
from .ollama_client import OllamaClient, quick_chat, quick_generate, describe_image, screenshot_and_describe, data_from_path, describe_image_from_path
from .openrouter_client import (
    OpenRouterClient, 
    quick_chat as openrouter_chat, 
    quick_generate as openrouter_generate,
    describe_image as openrouter_describe_image,
    screenshot_and_describe as openrouter_screenshot_describe,
    describe_image_from_path as openrouter_describe_from_path
)
from .config import (
    get_config, set_config, set_host, set_port, set_model, set_system_prompt,
    get_url, get_model, get_system_prompt, reset_config
)

__version__ = "0.1.0"
__author__ = "ScreenClicker Development Team"
__all__ = [
    "right_click", 
    "left_click", 
    "move_mouse",
    "text", 
    "screenshot", 
    "screenshot_region", 
    "screenshot_monitor",
    "get_screen_info",
    "OllamaClient",
    "quick_chat",
    "quick_generate",
    "describe_image",
    "screenshot_and_describe",
    "data_from_path",
    "describe_image_from_path",
    "OpenRouterClient",
    "openrouter_chat",
    "openrouter_generate", 
    "openrouter_describe_image",
    "openrouter_screenshot_describe",
    "openrouter_describe_from_path",
    "get_config",
    "set_config", 
    "set_host", 
    "set_port", 
    "set_model",
    "set_system_prompt",
    "get_url",
    "get_model",
    "get_system_prompt",
    "reset_config"
]
