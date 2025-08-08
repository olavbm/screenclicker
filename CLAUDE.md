# ScreenClicker - Wayland Automation Library

A professional Python library for screen automation and capture that works on Wayland/Sway systems. Provides a minimal, clean API for mouse clicks, keyboard input, and screen capture that bypasses Wayland security restrictions.

## Project Overview

This project solves the fundamental challenge of screen automation on Wayland Linux systems, where traditional automation libraries are blocked by security restrictions. The solution uses low-level `uinput` virtual devices to provide reliable mouse and keyboard control.

## Library Structure

### Core Library (`screenclicker/`)
The library is now organized into modular files for better maintainability:

- **`__init__.py`** - Clean API imports and package metadata
- **`mouse.py`** - Mouse operations module:
  - `right_click(x, y)` - Right click at coordinates using uinput
  - `left_click(x, y)` - Left click at coordinates using uinput  
  - `move_mouse(x, y)` - Move cursor to coordinates using ydotool
- **`keyboard.py`** - Keyboard operations module:
  - `text(string)` - Type text using uinput keyboard controller
- **`screen.py`** - Screen capture and monitor operations module:
  - `screenshot(output_path=None)` - Capture full screen using grim
  - `screenshot_region(x, y, width, height, output_path=None)` - Capture screen regions
  - `screenshot_monitor(monitor_index=0, output_path=None)` - Capture specific monitor for ViT workflows
  - `get_screen_info()` - Get monitor layout and resolution information

**Complete API (8 functions)**: All functions available via single import from main package.

### Testing Suite (`tests/`)
- **`test_screenclicker.py`** - Streamlined test suite with 7 comprehensive tests:
  - `test_mouse_operations()` - Mouse click coordinate handling and validation
  - `test_keyboard_operations()` - Text input scenarios with various character sets
  - `test_cursor_movement()` - Smooth circular cursor movement validation using ydotool
  - `test_screen_capture()` - All screenshot functions (full, region, monitor, bytes/file output)
  - `test_screen_info()` - Monitor detection and information gathering
  - `test_terminal_automation()` - Complete terminal workflow automation (slow)
  - `test_integration_workflow()` - Combined mouse + keyboard operations (slow)

### Package Structure
- **`setup.py`** - Package configuration and dependencies
- **`pytest.ini`** - Test configuration and markers
- **`requirements.txt`** - Project dependencies
- **`README.md`** - Quick start guide and usage

## Technical Implementation

### Mouse Control (Hybrid Solution)
- **Problem**: Wayland security model blocks traditional mouse automation libraries (pynput, pyautogui)
- **Solution**: Uses Linux uinput kernel module for clicks and ydotool for cursor movement
- **Status**: ✅ **Fully Working** - bypasses Wayland restrictions without special permissions

### Keyboard Control (Pure uinput Solution)
- **Implementation**: Uses uinput virtual devices for all keyboard input
- **Advantage**: Consistent behavior across all applications (existing and newly spawned)
- **Discovery**: Pure uinput approach provides most reliable text input on Wayland
- **Status**: ✅ **Fully Working** with unified uinput implementation

### Screen Capture (Wayland-Native Solution)
- **Implementation**: Uses grim command-line tool via subprocess
- **Capabilities**: Full screen capture, region capture, individual monitor capture, bytes/file output
- **Monitor Support**: Multi-monitor detection and coordinate mapping via swaymsg
- **ViT Integration**: New `screenshot_monitor()` function optimized for Vision AI workflows
- **Status**: ✅ **Fully Working** with comprehensive capture options

### Key Breakthroughs
1. **Mouse automation**: uinput virtual devices bypass Wayland mouse restrictions
2. **Keyboard automation**: Pure uinput solution provides consistent text input across all applications
3. **Screen capture**: grim integration provides native Wayland screenshot capabilities
4. **Cursor movement**: ydotool provides smooth visible movement without special permissions
5. **Modular architecture**: Clean separation of concerns with mouse, keyboard, and screen modules
6. **Monitor-specific capture**: Direct monitor screenshot capability for ViT and AI workflows
7. **Test methodology**: Streamlined pytest suite with circular cursor movement and comprehensive coverage

## Dependencies

### Python Dependencies
- `python-uinput>=1.0.1` - Low-level input device creation for mouse and keyboard
- `pytest>=7.0.0` - Testing framework

### System Dependencies  
- `ydotool` - Wayland-compatible cursor movement without special permissions
  - Install: `sudo apt install ydotool`
- `grim` - Wayland screenshot capture
  - Install: `sudo apt install grim`

## Usage Examples

```python
# Complete API - works on Wayland/Sway (now with modular structure)
from screenclicker import (
    right_click, left_click, move_mouse, text, 
    screenshot, screenshot_region, screenshot_monitor, get_screen_info
)

# Mouse operations (from mouse.py)
right_click(400, 400)   # Right click at coordinates
left_click(500, 300)    # Left click at coordinates
move_mouse(600, 400)    # Smooth cursor movement

# Keyboard operations (from keyboard.py)
text("Hello from ScreenClicker!")  # Type text

# Screen operations (from screen.py)
screenshot("full_screen.png")       # Save full screenshot
screenshot_bytes = screenshot()     # Get screenshot as bytes
screenshot_region(0, 0, 500, 300, "region.png")  # Capture area

# Monitor-specific capture (perfect for ViT workflows)
monitor_bytes = screenshot_monitor(0)  # Capture laptop screen
monitor_bytes = screenshot_monitor(1)  # Capture external monitor

# Monitor information
info = get_screen_info()
print(f"Detected {len(info['monitors'])} monitors")

# Vision AI workflow example
screenshot_data = screenshot_monitor(1)  # Capture 4K monitor
# ... process with ViT model ...
move_mouse(predicted_x, predicted_y)    # Move to predicted location
left_click(predicted_x, predicted_y)    # Click at prediction
```

## Environment Compatibility

- **OS**: Linux with Wayland compositor
- **Tested on**: Sway window manager with dual monitor setup (1920x1200 + 3840x2160)
- **Mouse clicks**: ✅ **Fully Working** via uinput virtual devices
- **Cursor movement**: ✅ **Fully Working** via ydotool (smooth circular motion)
- **Keyboard**: ✅ **Fully Working** via pure uinput implementation
- **Terminal automation**: ✅ **Fully Working** with direct process management
- **Multi-monitor**: ✅ **Fully Working** with individual monitor capture

## Testing & Quality Assurance

**Test Suite**: 7 streamlined tests using pytest (cleaned up from 8, eliminated redundancy)
- **Fast tests** (5): Core functionality validation, streamlined for efficiency
- **Slow tests** (2): Terminal automation workflows, integration testing  
- **Test coverage**:
  - `test_mouse_operations()` - Mouse click operations across coordinate ranges
  - `test_keyboard_operations()` - Text input with various character sets and symbols
  - `test_cursor_movement()` - Smooth circular cursor movement (24-point circle)
  - `test_screen_capture()` - All screenshot functions including new monitor capture
  - `test_screen_info()` - Monitor detection and information gathering
  - `test_terminal_automation()` - Complete terminal workflow automation (slow)
  - `test_integration_workflow()` - Combined mouse + keyboard operations (slow)

**Run tests**:
```bash
pytest                    # All tests (7 tests total)
pytest -m "not slow"      # Fast tests only (5 tests, ~17 seconds)
pytest tests/test_screenclicker.py  # Run specific test file
```

## Development Journey

1. **Initial Challenge**: Standard automation libraries blocked by Wayland security
2. **Mouse Solution**: uinput virtual devices bypass Wayland mouse restrictions  
3. **Keyboard Evolution**: Started with dual approach (pynput + uinput), refined to pure uinput
4. **Cursor Movement Breakthrough**: ydotool provides visible cursor movement without special permissions
5. **Terminal Breakthrough**: Direct process launch + click-to-focus + uinput input works reliably
6. **Modular Refactor**: Reorganized monolithic code into clean mouse/keyboard/screen modules
7. **ViT Integration**: Added `screenshot_monitor()` for Vision AI workflows
8. **Test Optimization**: Streamlined from 8 to 7 tests, eliminated redundancy, added circular movement
9. **Final Achievement**: Production-ready modular Wayland automation solution

## Architecture & Security

- **Modular Design**: Separated concerns into mouse.py, keyboard.py, and screen.py modules
- **Mouse control**: Creates virtual mouse devices via uinput for clicks (no root required)
- **Cursor movement**: Uses ydotool for visible movement without special permissions
- **Keyboard input**: Pure uinput virtual devices for consistent cross-application input
- **Process management**: Direct subprocess control for reliable application launching
- **Focus management**: Click-to-focus ensures input reaches correct applications
- **Wayland compliance**: Works within security model using kernel-level virtual devices and system tools

## Real-World Applications

**Proven working scenarios**:
- ✅ Mouse clicking at specific coordinates across multi-monitor setups
- ✅ Smooth circular cursor movement patterns for demonstrations and testing
- ✅ Text input with special characters, symbols, and command strings
- ✅ Full screen, region, and individual monitor screenshot capture
- ✅ Multi-monitor detection and coordinate mapping (dual 1920x1200 + 3840x2160)
- ✅ Terminal automation workflows (open → type commands → execute → close)
- ✅ Application launching and focus management
- ✅ Integration workflows combining mouse, keyboard, cursor movement, and screen capture
- ✅ Cross-application input consistency (existing and newly spawned processes)
- ✅ **Vision AI workflows**: Monitor-specific screenshot capture optimized for ViT processing

**Production ready**: Complete modular automation platform with minimal dependencies provides reliable GUI testing, process automation, screen analysis, and ViT-controlled automation on Wayland systems. Clean architecture supports easy maintenance and extension.