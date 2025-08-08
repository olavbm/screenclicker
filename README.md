# ScreenClicker - Wayland Automation Library

Professional Python library for screen automation on **Wayland/Sway** systems.

## Installation

```bash
pip install python-uinput
```

## Usage

```python
from screenclicker import right_click, left_click, text

# Mouse clicks
right_click(400, 400)   # Right click at coordinates
left_click(500, 300)    # Left click at coordinates

# Text input
text("Hello from ScreenClicker!")  # Type text
```

## Testing

```bash
# Install with dev dependencies
pip install -e .

# Run tests
pytest                    # All tests
pytest -m "not slow"      # Fast tests only
```

## How It Works

Uses `uinput` virtual devices to bypass Wayland security restrictions:
- **Mouse**: Virtual mouse devices for clicking
- **Keyboard**: Virtual keyboard devices for text input

## System Requirements

- **OS**: Linux with Wayland compositor
- **Tested on**: Sway window manager  
- **Python**: 3.6+