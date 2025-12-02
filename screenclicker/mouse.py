"""Mouse operations for ScreenClicker.

Uses hybrid approach:
- uinput for clicks (no daemon required)
- ydotool for cursor movement (visible movement on Wayland)
"""

import time
import uinput
import subprocess


def _create_mouse_device():
    """Create virtual mouse device with screen dimensions."""
    try:
        from .screen import get_screen_info
        screen_info = get_screen_info()

        if screen_info['monitors']:
            monitor = screen_info['monitors'][0]
            max_x = monitor['width'] - 1
            max_y = monitor['height'] - 1
        else:
            max_x = 1919
            max_y = 1199

        return uinput.Device([
            uinput.BTN_LEFT,
            uinput.BTN_RIGHT,
            uinput.ABS_X + (0, max_x, 0, 0),
            uinput.ABS_Y + (0, max_y, 0, 0),
        ])
    except PermissionError:
        raise PermissionError("uinput access denied. Check /dev/uinput permissions.")
    except Exception as e:
        raise RuntimeError(f"Failed to create mouse device: {e}")


def _click_uinput(x, y, button):
    """Click at coordinates using uinput virtual device."""
    device = _create_mouse_device()
    time.sleep(0.1)  # Let device initialize

    # Move to position
    device.emit(uinput.ABS_X, x, syn=False)
    device.emit(uinput.ABS_Y, y, syn=True)
    time.sleep(0.05)

    # Click
    device.emit(button, 1)  # Press
    time.sleep(0.02)
    device.emit(button, 0)  # Release

    return True


def right_click(x, y):
    """Right click at coordinates using uinput."""
    try:
        return _click_uinput(x, y, uinput.BTN_RIGHT)
    except Exception as e:
        raise RuntimeError(f"Right click failed: {e}")


def left_click(x, y):
    """Left click at coordinates using uinput."""
    try:
        return _click_uinput(x, y, uinput.BTN_LEFT)
    except Exception as e:
        raise RuntimeError(f"Left click failed: {e}")


def move_mouse(x, y):
    """Move cursor to coordinates using ydotool (visible movement).

    Requires ydotoold daemon running: ydotoold &
    """
    try:
        result = subprocess.run(
            ['ydotool', 'mousemove', '-a', str(x), str(y)],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode != 0:
            raise RuntimeError(f"ydotool failed (is ydotoold running?): {result.stderr}")
        return True
    except FileNotFoundError:
        raise RuntimeError("ydotool not found. Install with: sudo apt install ydotool")
    except subprocess.TimeoutExpired:
        raise RuntimeError("ydotool timed out")
    except Exception as e:
        raise RuntimeError(f"Mouse movement failed: {e}")
