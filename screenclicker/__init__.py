"""
ScreenClicker - VLM-powered screen automation for Wayland/Sway

Core features:
- Mouse clicks and cursor movement via uinput/ydotool
- Text input via uinput virtual keyboards
- Screen capture via grim with multi-monitor support
- VLM integration via Ollama for vision-based automation

System dependencies:
- ydotool: For cursor movement (sudo apt install ydotool)
- grim: For screenshots (sudo apt install grim)
- ollama: For local VLM hosting (https://ollama.com)
"""

from .mouse import right_click, left_click, move_mouse
from .keyboard import text
from .screen import screenshot, screenshot_region, get_screen_info, screenshot_monitor
from .ollama_client import (
    OllamaClient,
    quick_chat,
    quick_generate,
    describe_image,
    screenshot_and_describe,
    data_from_path,
    describe_image_from_path
)
from .config import (
    get_config, set_config, set_host, set_port, set_model, set_system_prompt,
    get_url, get_model, get_system_prompt, reset_config
)

__version__ = "0.2.0"
__all__ = [
    # Mouse
    "right_click",
    "left_click",
    "move_mouse",

    # Keyboard
    "text",

    # Screen capture
    "screenshot",
    "screenshot_region",
    "screenshot_monitor",
    "get_screen_info",

    # VLM (Ollama)
    "OllamaClient",
    "quick_chat",
    "quick_generate",
    "describe_image",
    "screenshot_and_describe",
    "data_from_path",
    "describe_image_from_path",

    # Config
    "get_config",
    "set_config",
    "set_host",
    "set_port",
    "set_model",
    "set_system_prompt",
    "get_url",
    "get_model",
    "get_system_prompt",
    "reset_config",
]
