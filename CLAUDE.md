# ScreenClicker - Wayland Automation Library

A professional Python library for screen automation that works on Wayland/Sway systems. Provides a minimal, clean API for mouse clicks and keyboard input that bypasses Wayland security restrictions.

## Project Overview

This project solves the fundamental challenge of screen automation on Wayland Linux systems, where traditional automation libraries are blocked by security restrictions. The solution uses low-level `uinput` virtual devices to provide reliable mouse and keyboard control.

## Library Structure

### Core Library (`screenclicker/`)
- **`__init__.py`** - Main library API with three simple functions:
  - `right_click(x, y)` - Right click at coordinates using uinput
  - `left_click(x, y)` - Left click at coordinates using uinput  
  - `text(string)` - Type text using uinput keyboard controller

### Testing Suite (`tests/`)
- **`test_screenclicker.py`** - Comprehensive test suite covering all functionality:
  - Core API functions (right_click, left_click, text)
  - Mouse coordinate handling and validation
  - Text input scenarios with various character sets
  - Terminal automation workflows
  - Integration testing (mouse + keyboard operations)

### Package Structure
- **`setup.py`** - Package configuration and dependencies
- **`pytest.ini`** - Test configuration and markers
- **`requirements.txt`** - Project dependencies
- **`README.md`** - Quick start guide and usage

## Technical Implementation

### Mouse Control (uinput Solution)
- **Problem**: Wayland security model blocks traditional mouse automation libraries (pynput, pyautogui)
- **Solution**: Uses Linux uinput kernel module to create virtual mouse devices
- **Status**: ✅ **Fully Working** - bypasses Wayland restrictions completely

### Keyboard Control (Pure uinput Solution)
- **Implementation**: Uses uinput virtual devices for all keyboard input
- **Advantage**: Consistent behavior across all applications (existing and newly spawned)
- **Discovery**: Pure uinput approach provides most reliable text input on Wayland
- **Status**: ✅ **Fully Working** with unified uinput implementation

### Key Breakthroughs
1. **Mouse automation**: uinput virtual devices bypass Wayland mouse restrictions
2. **Keyboard automation**: Pure uinput solution provides consistent text input across all applications
3. **Terminal automation**: Direct process launch + uinput input works reliably for complex workflows
4. **Test methodology**: Streamlined pytest suite efficiently validates all core functionality

## Dependencies

- `python-uinput>=1.0.1` - Low-level input device creation for mouse and keyboard
- `pytest>=7.0.0` - Testing framework

## Usage Examples

```python
# Simple API - works on Wayland/Sway
from screenclicker import right_click, left_click, text

# Mouse clicks (using uinput)
right_click(400, 400)   # Right click at coordinates
left_click(500, 300)    # Left click at coordinates

# Text input (using uinput)
text("Hello from ScreenClicker!")  # Type text

# Terminal automation example
import subprocess
process = subprocess.Popen(['foot'])  # Open terminal
time.sleep(2)
left_click(960, 540)  # Focus terminal
text("echo 'Automation works!'")  # Type command
```

## Environment Compatibility

- **OS**: Linux with Wayland compositor
- **Tested on**: Sway window manager with dual monitor setup
- **Mouse**: ✅ **Fully Working** via uinput virtual devices
- **Keyboard**: ✅ **Fully Working** via pure uinput implementation
- **Terminal automation**: ✅ **Fully Working** with direct process management

## Testing & Quality Assurance

**Test Suite**: 5 comprehensive tests using pytest (streamlined from 18 redundant tests)
- **Fast tests** (3): Core API validation, coordinate handling, text input scenarios
- **Slow tests** (2): Terminal automation workflows, integration testing
- **Test coverage**:
  - `test_library_api()` - Core function validation (right_click, left_click, text)
  - `test_mouse_coordinates()` - Mouse coordinate handling across screen areas
  - `test_text_input_scenarios()` - Various text types including symbols and commands
  - `test_terminal_automation()` - Complete terminal workflow automation (slow)
  - `test_integration_workflow()` - Combined mouse + keyboard operations (slow)

**Run tests**:
```bash
pytest                    # All tests (includes visual verification)
pytest -m "not slow"      # Fast tests only (3 tests)
pytest tests/test_screenclicker.py  # Run specific test file
```

## Development Journey

1. **Initial Challenge**: Standard automation libraries blocked by Wayland security
2. **Mouse Solution**: uinput virtual devices bypass Wayland mouse restrictions  
3. **Keyboard Evolution**: Started with dual approach (pynput + uinput), refined to pure uinput
4. **Terminal Breakthrough**: Direct process launch + click-to-focus + uinput input works reliably
5. **Library Design**: Minimal 3-function API with streamlined testing (reduced from 18 to 5 tests)
6. **Final Achievement**: Production-ready Wayland automation solution with proven real-world workflows

## Architecture & Security

- **Mouse control**: Creates virtual mouse devices via uinput (no root required)
- **Keyboard input**: Pure uinput virtual devices for consistent cross-application input
- **Process management**: Direct subprocess control for reliable application launching
- **Focus management**: Click-to-focus ensures input reaches correct applications
- **Wayland compliance**: Works within security model by using kernel-level virtual devices

## Real-World Applications

**Proven working scenarios**:
- ✅ Mouse clicking at specific coordinates across multi-monitor setups
- ✅ Text input with special characters, symbols, and command strings
- ✅ Terminal automation workflows (open → type commands → execute → close)
- ✅ Application launching and focus management
- ✅ Integration workflows combining mouse and keyboard operations
- ✅ Cross-application input consistency (existing and newly spawned processes)

**Production ready**: Streamlined library with minimal dependencies provides reliable automation for GUI testing, process automation, and interactive scripting on Wayland systems.