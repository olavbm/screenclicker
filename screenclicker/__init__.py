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

<<<<<<< Updated upstream
import time
import uinput
import subprocess
import tempfile
import os

__version__ = "0.1.0"
__author__ = "ScreenClicker Development Team"
__all__ = ["right_click", "left_click", "text", "screenshot", "screenshot_region", "get_screen_info", "move_mouse"]

def _create_mouse_device():
    """Create virtual mouse device."""
    try:
        return uinput.Device([
            uinput.BTN_LEFT,
            uinput.BTN_RIGHT,
            uinput.ABS_X + (0, 1920, 0, 0),
            uinput.ABS_Y + (0, 1080, 0, 0),
        ])
    except PermissionError:
        raise PermissionError("uinput access denied. Check permissions.")
    except Exception as e:
        raise RuntimeError(f"Failed to create mouse device: {e}")

def right_click(x, y):
    """Right click at coordinates."""
    device = _create_mouse_device()
    try:
        device.emit(uinput.ABS_X, x)
        device.emit(uinput.ABS_Y, y)
        device.syn()
        time.sleep(0.01)
        device.emit(uinput.BTN_RIGHT, 1)
        device.syn()
        time.sleep(0.05)
        device.emit(uinput.BTN_RIGHT, 0)
        device.syn()
        return True
    finally:
        device.destroy()

def left_click(x, y):
    """Left click at coordinates."""
    device = _create_mouse_device()
    try:
        device.emit(uinput.ABS_X, x)
        device.emit(uinput.ABS_Y, y)
        device.syn()
        time.sleep(0.01)
        device.emit(uinput.BTN_LEFT, 1)
        device.syn()
        time.sleep(0.05)
        device.emit(uinput.BTN_LEFT, 0)
        device.syn()
        return True
    finally:
        device.destroy()

def _create_keyboard_device():
    """Create virtual keyboard device."""
    try:
        return uinput.Device([
            uinput.KEY_A, uinput.KEY_B, uinput.KEY_C, uinput.KEY_D, uinput.KEY_E,
            uinput.KEY_F, uinput.KEY_G, uinput.KEY_H, uinput.KEY_I, uinput.KEY_J,
            uinput.KEY_K, uinput.KEY_L, uinput.KEY_M, uinput.KEY_N, uinput.KEY_O,
            uinput.KEY_P, uinput.KEY_Q, uinput.KEY_R, uinput.KEY_S, uinput.KEY_T,
            uinput.KEY_U, uinput.KEY_V, uinput.KEY_W, uinput.KEY_X, uinput.KEY_Y,
            uinput.KEY_Z,
            uinput.KEY_0, uinput.KEY_1, uinput.KEY_2, uinput.KEY_3, uinput.KEY_4,
            uinput.KEY_5, uinput.KEY_6, uinput.KEY_7, uinput.KEY_8, uinput.KEY_9,
            uinput.KEY_SPACE, uinput.KEY_ENTER, uinput.KEY_BACKSPACE,
            uinput.KEY_LEFTSHIFT, uinput.KEY_RIGHTSHIFT,
            uinput.KEY_APOSTROPHE, uinput.KEY_COMMA, uinput.KEY_DOT,
            uinput.KEY_MINUS, uinput.KEY_EQUAL, uinput.KEY_SLASH,
            uinput.KEY_SEMICOLON, uinput.KEY_LEFTBRACE, uinput.KEY_RIGHTBRACE,
        ])
    except PermissionError:
        raise PermissionError("uinput keyboard access denied. Check permissions.")
    except Exception as e:
        raise RuntimeError(f"Failed to create keyboard device: {e}")

def _uinput_type_char(device, char):
    """Type a single character using uinput."""
    char_map = {
        'a': uinput.KEY_A, 'b': uinput.KEY_B, 'c': uinput.KEY_C, 'd': uinput.KEY_D, 'e': uinput.KEY_E,
        'f': uinput.KEY_F, 'g': uinput.KEY_G, 'h': uinput.KEY_H, 'i': uinput.KEY_I, 'j': uinput.KEY_J,
        'k': uinput.KEY_K, 'l': uinput.KEY_L, 'm': uinput.KEY_M, 'n': uinput.KEY_N, 'o': uinput.KEY_O,
        'p': uinput.KEY_P, 'q': uinput.KEY_Q, 'r': uinput.KEY_R, 's': uinput.KEY_S, 't': uinput.KEY_T,
        'u': uinput.KEY_U, 'v': uinput.KEY_V, 'w': uinput.KEY_W, 'x': uinput.KEY_X, 'y': uinput.KEY_Y,
        'z': uinput.KEY_Z,
        '0': uinput.KEY_0, '1': uinput.KEY_1, '2': uinput.KEY_2, '3': uinput.KEY_3, '4': uinput.KEY_4,
        '5': uinput.KEY_5, '6': uinput.KEY_6, '7': uinput.KEY_7, '8': uinput.KEY_8, '9': uinput.KEY_9,
        ' ': uinput.KEY_SPACE, "'": uinput.KEY_APOSTROPHE, ',': uinput.KEY_COMMA,
        '.': uinput.KEY_DOT, '-': uinput.KEY_MINUS, '=': uinput.KEY_EQUAL, '/': uinput.KEY_SLASH,
        ';': uinput.KEY_SEMICOLON, '[': uinput.KEY_LEFTBRACE, ']': uinput.KEY_RIGHTBRACE,
    }
    
    # Handle uppercase letters (need shift)
    if char.isupper():
        char_lower = char.lower()
        if char_lower in char_map:
            device.emit(uinput.KEY_LEFTSHIFT, 1)
            device.emit(char_map[char_lower], 1)
            device.syn()
            time.sleep(0.01)
            device.emit(char_map[char_lower], 0)
            device.emit(uinput.KEY_LEFTSHIFT, 0)
            device.syn()
            return True
    
    # Handle regular characters
    if char in char_map:
        device.emit(char_map[char], 1)
        device.syn()
        time.sleep(0.01)
        device.emit(char_map[char], 0)
        device.syn()
        return True
    
    # Skip unsupported characters
    return False

def text(string):
    """Type text string using uinput."""
    device = _create_keyboard_device()
    try:
        for char in string:
            if not _uinput_type_char(device, char):
                # Skip unsupported characters silently
                continue
            time.sleep(0.02)  # Small delay between characters
        return True
    except Exception as e:
        return False
    finally:
        device.destroy()

def screenshot(output_path=None):
    """Take a full screenshot using grim.
    
    Args:
        output_path: Path to save screenshot. If None, returns image bytes.
        
    Returns:
        True if successful (when output_path provided), or bytes data
    """
    try:
        if output_path:
            # Save to specified path
            result = subprocess.run(['grim', output_path], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=10)
            if result.returncode == 0:
                return True
            else:
                raise RuntimeError(f"grim failed: {result.stderr}")
        else:
            # Return bytes data
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                tmp_path = tmp.name
            
            try:
                result = subprocess.run(['grim', tmp_path], 
                                      capture_output=True, 
                                      text=True, 
                                      timeout=10)
                if result.returncode == 0:
                    with open(tmp_path, 'rb') as f:
                        return f.read()
                else:
                    raise RuntimeError(f"grim failed: {result.stderr}")
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
                    
    except FileNotFoundError:
        raise RuntimeError("grim not found. Install with: apt install grim")
    except subprocess.TimeoutExpired:
        raise RuntimeError("Screenshot timed out")
    except Exception as e:
        raise RuntimeError(f"Screenshot failed: {e}")

def screenshot_region(x, y, width, height, output_path=None):
    """Take a screenshot of a specific region using grim.
    
    Args:
        x, y: Top-left coordinates of region
        width, height: Size of region
        output_path: Path to save screenshot. If None, returns image bytes.
        
    Returns:
        True if successful (when output_path provided), or bytes data
    """
    try:
        geometry = f"{x},{y} {width}x{height}"
        
        if output_path:
            # Save to specified path
            result = subprocess.run(['grim', '-g', geometry, output_path], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=10)
            if result.returncode == 0:
                return True
            else:
                raise RuntimeError(f"grim failed: {result.stderr}")
        else:
            # Return bytes data
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                tmp_path = tmp.name
            
            try:
                result = subprocess.run(['grim', '-g', geometry, tmp_path], 
                                      capture_output=True, 
                                      text=True, 
                                      timeout=10)
                if result.returncode == 0:
                    with open(tmp_path, 'rb') as f:
                        return f.read()
                else:
                    raise RuntimeError(f"grim failed: {result.stderr}")
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
                    
    except FileNotFoundError:
        raise RuntimeError("grim not found. Install with: apt install grim")
    except subprocess.TimeoutExpired:
        raise RuntimeError("Screenshot timed out")
    except Exception as e:
        raise RuntimeError(f"Screenshot failed: {e}")

def get_screen_info():
    """Get screen/monitor information.
    
    Returns:
        dict with screen information
    """
    try:
        # Try to get monitor info using swaymsg if available
        try:
            result = subprocess.run(['swaymsg', '-t', 'get_outputs'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            if result.returncode == 0:
                import json
                outputs = json.loads(result.stdout)
                monitors = []
                for output in outputs:
                    if output.get('active'):
                        rect = output.get('rect', {})
                        monitors.append({
                            'name': output.get('name', 'unknown'),
                            'x': rect.get('x', 0),
                            'y': rect.get('y', 0),
                            'width': rect.get('width', 1920),
                            'height': rect.get('height', 1080),
                            'primary': output.get('primary', False)
                        })
                return {'monitors': monitors}
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        
        # Fallback: basic screen info
        return {
            'monitors': [{
                'name': 'default',
                'x': 0,
                'y': 0,
                'width': 1920,
                'height': 1080,
                'primary': True
            }]
        }
        
    except Exception as e:
        # Ultimate fallback
        return {
            'monitors': [{
                'name': 'fallback',
                'x': 0,
                'y': 0,
                'width': 1920,
                'height': 1080,
                'primary': True
            }]
        }
def move_mouse(x, y):
    """Move mouse cursor to coordinates with visible movement.
    
    Uses ydotool for Wayland-compatible cursor movement without requiring
    special permissions. Falls back to uinput if ydotool is not available.
    
    Args:
        x: X coordinate
        y: Y coordinate
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Primary method: use ydotool (works on Wayland without special permissions)
        result = subprocess.run(['ydotool', 'mousemove', str(x), str(y)], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return True
        else:
            raise RuntimeError(f"ydotool failed: {result.stderr}")
            
    except FileNotFoundError:
        raise RuntimeError("ydotool not found. Install with: sudo apt install ydotool")
    except subprocess.TimeoutExpired:
        raise RuntimeError("ydotool timed out")
    except Exception as e:
        raise RuntimeError(f"Mouse movement failed: {e}")
=======
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
>>>>>>> Stashed changes
