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
from .ollama_client import OllamaClient, quick_chat, quick_generate

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
    "quick_generate"
]
