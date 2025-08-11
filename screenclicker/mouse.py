"""Mouse operations for ScreenClicker."""

import time
import uinput
import subprocess


def _create_mouse_device():
    """Create virtual mouse device with actual screen dimensions."""
    try:
        # Get actual screen resolution dynamically
        from .screen import get_screen_info
        screen_info = get_screen_info()
        
        if screen_info['monitors']:
            # Use first monitor dimensions
            monitor = screen_info['monitors'][0]
            max_x = monitor['width'] - 1
            max_y = monitor['height'] - 1
        else:
            # Fallback dimensions
            max_x = 1919
            max_y = 1199
            
        return uinput.Device([
            uinput.BTN_LEFT,
            uinput.BTN_RIGHT,
            uinput.ABS_X + (0, max_x, 0, 0),
            uinput.ABS_Y + (0, max_y, 0, 0),
        ])
    except PermissionError:
        raise PermissionError("uinput access denied. Check permissions.")
    except Exception as e:
        raise RuntimeError(f"Failed to create mouse device: {e}")

def right_click(x, y):
    """Right click at coordinates using ydotool (consistent coordinate system)."""
    try:
        # Move cursor to coordinates
        result1 = subprocess.run(['ydotool', 'mousemove', str(x), str(y)], 
                               capture_output=True, text=True, timeout=5)
        if result1.returncode != 0:
            raise RuntimeError(f"ydotool mousemove failed: {result1.stderr}")
            
        # Small delay to ensure movement completes
        time.sleep(0.05)
        
        # Right click at current position
        result2 = subprocess.run(['ydotool', 'click', '2'], 
                               capture_output=True, text=True, timeout=5)
        if result2.returncode != 0:
            raise RuntimeError(f"ydotool click failed: {result2.stderr}")
            
        return True
            
    except FileNotFoundError:
        raise RuntimeError("ydotool not found. Install with: sudo apt install ydotool")
    except subprocess.TimeoutExpired:
        raise RuntimeError("ydotool timed out")
    except Exception as e:
        raise RuntimeError(f"Right click failed: {e}")

def left_click(x, y):
    """Left click at coordinates using ydotool (consistent coordinate system)."""
    try:
        # Move cursor to coordinates
        result1 = subprocess.run(['ydotool', 'mousemove', str(x), str(y)], 
                               capture_output=True, text=True, timeout=5)
        if result1.returncode != 0:
            raise RuntimeError(f"ydotool mousemove failed: {result1.stderr}")
            
        # Small delay to ensure movement completes
        time.sleep(0.05)
        
        # Left click at current position
        result2 = subprocess.run(['ydotool', 'click', '1'], 
                               capture_output=True, text=True, timeout=5)
        if result2.returncode != 0:
            raise RuntimeError(f"ydotool click failed: {result2.stderr}")
            
        return True
            
    except FileNotFoundError:
        raise RuntimeError("ydotool not found. Install with: sudo apt install ydotool")
    except subprocess.TimeoutExpired:
        raise RuntimeError("ydotool timed out")
    except Exception as e:
        raise RuntimeError(f"Left click failed: {e}")


def move_mouse(x, y):
    """Move mouse cursor to coordinates with visible movement.
    
    Uses ydotool for Wayland-compatible cursor movement without requiring
    special permissions.
    
    Args:
        x: X coordinate
        y: Y coordinate
        
    Returns:
        bool: True if successful. Raises an error otherwise.
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
