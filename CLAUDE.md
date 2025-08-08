# Screen Clicker - Python Automation for Wayland

A Python-based screen automation toolkit that works on Wayland/Sway systems, providing both mouse and keyboard control capabilities.

## Project Overview

This project successfully implements screen automation on Wayland Linux systems, which typically block traditional mouse automation due to security restrictions. The solution uses low-level input devices to bypass these limitations.

## Key Files

### Core Functionality
- **`clicker.py`** - Main mouse automation module using uinput
  - `right_click(x, y)` - Right click at absolute coordinates
  - `move_mouse_circle(center_x, center_y, radius, duration)` - Smooth circular mouse movement
  - Creates virtual mouse devices that work on Wayland

- **`debug_input.py`** - Keyboard automation and system analysis
  - Comprehensive keyboard input functions using pynput
  - System environment detection (compositor type, input capabilities)
  - Text typing, key combinations, and navigation helpers

- **`uinput_clicker.py`** - Extended mouse testing and functionality
  - Both relative and absolute mouse positioning
  - Comprehensive mouse button support (left, right, middle)
  - Detailed testing and debugging capabilities

## Technical Implementation

### Mouse Control (Wayland Solution)
- **Problem**: Wayland security model blocks traditional mouse automation libraries (pynput, pyautogui)
- **Solution**: Uses Linux uinput kernel module to create virtual input devices
- **Requirements**: 
  - `python-uinput` library
  - Proper uinput permissions (usually works without root on modern systems)

### Keyboard Control (Works Natively)
- **Library**: pynput (works on Wayland for keyboard input)
- **Capabilities**: Text typing, key combinations, navigation keys
- **Status**: Fully functional without special permissions

## Dependencies

- `python-uinput>=1.0.1` - Low-level input device creation
- `pynput` - Keyboard automation (works on Wayland)

## Usage Examples

```python
# Mouse automation
from clicker import right_click, move_mouse_circle

right_click(400, 400)  # Right click at coordinates
move_mouse_circle(500, 400, 150, 5.0)  # Draw circle

# Keyboard automation  
from debug_input import test_direct_typing
test_direct_typing()  # Type test text
```

## Environment Compatibility

- **OS**: Linux with Wayland compositor
- **Tested on**: Sway window manager
- **Mouse**: ✅ Works via uinput virtual devices
- **Keyboard**: ✅ Works natively via pynput

## Development History

1. **Initial Challenge**: Standard mouse libraries (pynput) were blocked by Wayland security
2. **Discovery**: Keyboard automation worked immediately with pynput
3. **Research Phase**: Investigated various Wayland-specific solutions
4. **Breakthrough**: uinput approach successfully bypassed Wayland restrictions
5. **Implementation**: Built working mouse control with absolute positioning and smooth movement

## Security Notes

- Mouse control requires uinput access (typically available to regular users)
- Creates virtual input devices that the system treats as hardware
- Keyboard automation works within normal Wayland security boundaries
- No root privileges required for standard usage

## Future Enhancements

- Screen coordinate detection and window targeting
- Integration with Sway-specific window management commands  
- Extended gesture and pattern movement functions
- Multi-monitor coordinate mapping