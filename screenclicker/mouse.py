"""Mouse operations for ScreenClicker."""

import time
import uinput
import subprocess


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