# Screen Clicker - Wayland Python Automation

Python screen automation that works on **Wayland/Sway** systems.

## System Requirements

- **OS**: Linux with Wayland compositor  
- **Tested on**: Sway window manager
- **Python**: 3.6+

## Installation

```bash
pip install python-uinput pynput
```

## Usage

### Mouse Control
```python
from clicker import right_click, move_mouse_circle

# Right click at coordinates
right_click(400, 400)

# Move mouse in a circle
move_mouse_circle(center_x=500, center_y=400, radius=150, duration=5.0)
```

### Keyboard Control  
```python
from debug_input import test_direct_typing

# Type text automatically
test_direct_typing()
```

### Quick Test
```bash
python3 clicker.py
```

## How It Works

- **Mouse**: Uses `uinput` to create virtual input devices (bypasses Wayland restrictions)
- **Keyboard**: Uses `pynput` (works natively on Wayland)

## Files

- `clicker.py` - Main mouse automation functions
- `debug_input.py` - Keyboard automation and system info
- `uinput_clicker.py` - Extended mouse testing tools