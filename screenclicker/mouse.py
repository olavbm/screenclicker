"""Mouse operations for ScreenClicker.

Uses hybrid approach:
- uinput for clicks (no daemon required)
- ydotool for cursor movement (visible movement on Wayland)

Coordinates are relative to the target monitor (default: monitor 0).
The click functions automatically offset to global screen coordinates.
"""

import time
import uinput
import subprocess

# Default monitor index (0 = first monitor in list)
_target_monitor = 0


def set_target_monitor(index: int):
    """Set which monitor to target for clicks."""
    global _target_monitor
    _target_monitor = index


def get_target_monitor() -> int:
    """Get current target monitor index."""
    return _target_monitor


def _get_monitor_info(monitor_index: int = None):
    """Get monitor info including global offset."""
    from .screen import get_screen_info
    screen_info = get_screen_info()

    if not screen_info['monitors']:
        return {'x': 0, 'y': 0, 'width': 1920, 'height': 1200}

    idx = monitor_index if monitor_index is not None else _target_monitor
    if idx >= len(screen_info['monitors']):
        idx = 0

    return screen_info['monitors'][idx]


def _get_total_screen_size():
    """Get total screen dimensions across all monitors."""
    from .screen import get_screen_info
    screen_info = get_screen_info()

    if not screen_info['monitors']:
        return 1920, 1200

    max_x = 0
    max_y = 0
    for m in screen_info['monitors']:
        max_x = max(max_x, m['x'] + m['width'])
        max_y = max(max_y, m['y'] + m['height'])

    return max_x, max_y


def _create_mouse_device():
    """Create virtual mouse device with total screen dimensions."""
    try:
        max_x, max_y = _get_total_screen_size()

        return uinput.Device([
            uinput.BTN_LEFT,
            uinput.BTN_RIGHT,
            uinput.ABS_X + (0, max_x - 1, 0, 0),
            uinput.ABS_Y + (0, max_y - 1, 0, 0),
        ])
    except PermissionError:
        raise PermissionError("uinput access denied. Check /dev/uinput permissions.")
    except Exception as e:
        raise RuntimeError(f"Failed to create mouse device: {e}")


def _click_uinput(x, y, button, monitor_index=None):
    """Click at coordinates using uinput virtual device.

    Args:
        x, y: Coordinates relative to target monitor
        button: uinput button constant
        monitor_index: Override target monitor (uses default if None)
    """
    # Get monitor offset
    monitor = _get_monitor_info(monitor_index)
    global_x = monitor['x'] + x
    global_y = monitor['y'] + y

    device = _create_mouse_device()
    time.sleep(0.1)  # Let device initialize

    # Move to global position
    device.emit(uinput.ABS_X, global_x, syn=False)
    device.emit(uinput.ABS_Y, global_y, syn=True)
    time.sleep(0.05)

    # Click
    device.emit(button, 1)  # Press
    time.sleep(0.02)
    device.emit(button, 0)  # Release

    return True


def right_click(x, y, monitor_index=None):
    """Right click at coordinates (relative to target monitor)."""
    try:
        return _click_uinput(x, y, uinput.BTN_RIGHT, monitor_index)
    except Exception as e:
        raise RuntimeError(f"Right click failed: {e}")


def left_click(x, y, monitor_index=None):
    """Left click at coordinates (relative to target monitor)."""
    try:
        return _click_uinput(x, y, uinput.BTN_LEFT, monitor_index)
    except Exception as e:
        raise RuntimeError(f"Left click failed: {e}")


def move_mouse(x, y, monitor_index=None):
    """Move cursor to coordinates using ydotool (visible movement).

    Args:
        x, y: Coordinates relative to target monitor
        monitor_index: Override target monitor (uses default if None)

    Requires ydotoold daemon running: ydotoold &
    """
    try:
        # Get monitor offset
        monitor = _get_monitor_info(monitor_index)
        global_x = monitor['x'] + x
        global_y = monitor['y'] + y

        result = subprocess.run(
            ['ydotool', 'mousemove', '-a', str(global_x), str(global_y)],
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
