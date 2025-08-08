# ScreenClicker - Wayland Automation Library

Professional Python library for screen automation and capture on **Wayland/Sway** systems.

## Installation

```bash
pip install python-uinput
```

## Usage

```python
from screenclicker import right_click, left_click, text, screenshot, screenshot_region, get_screen_info

# Mouse clicks
right_click(400, 400)   # Right click at coordinates
left_click(500, 300)    # Left click at coordinates

# Text input
text("Hello from ScreenClicker!")  # Type text

# Screenshot capture
screenshot("full_screen.png")       # Save full screenshot
screenshot_bytes = screenshot()     # Get screenshot as bytes

# Region capture  
screenshot_region(0, 0, 500, 300, "region.png")  # Capture specific area
region_bytes = screenshot_region(100, 100, 200, 150)  # Region as bytes

# Monitor information
info = get_screen_info()           # Get monitor details
print(f"Monitors: {len(info['monitors'])}")
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

Uses low-level system tools to provide complete automation capabilities:
- **Mouse**: `uinput` virtual mouse devices for clicking
- **Keyboard**: `uinput` virtual keyboard devices for text input  
- **Screenshots**: `grim` command for Wayland-native screen capture

## System Requirements

- **OS**: Linux with Wayland compositor
- **Tested on**: Sway window manager  
- **Python**: 3.6+