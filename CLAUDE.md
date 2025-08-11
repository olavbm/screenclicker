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
- **`ollama_client.py`** - Local LLM and VLM integration module:
  - `OllamaClient()` - Full-featured client for Ollama server interactions with image support
  - `quick_chat(model, prompt, images)` - Chat completion with optional image input
  - `quick_generate(model, prompt, images)` - Text generation with optional image input
  - `describe_image(image_bytes, prompt)` - Analyze images using vision language models
  - `screenshot_and_describe(prompt, monitor)` - One-liner screenshot analysis
  - `data_from_path(file_path)` - Load image data from file paths
  - `describe_image_from_path(file_path, prompt)` - Analyze images directly from files
- **`openrouter_client.py`** - Cloud LLM and VLM integration module:
  - `OpenRouterClient()` - OpenRouter API client with vision model support  
  - `openrouter_chat(prompt, images, api_key)` - Chat completion with cloud models
  - `openrouter_generate(prompt, images, api_key)` - Text generation with cloud models
  - `openrouter_describe_image(image_bytes, prompt, api_key)` - Cloud-based image analysis
  - `openrouter_screenshot_describe(prompt, api_key)` - Live screenshot analysis with cloud AI
  - `openrouter_describe_from_path(file_path, prompt, api_key)` - File-based image analysis

**Complete API (23+ functions)**: All functions available via single import from main package.
**Complete Screen Interaction Pipeline**: Screenshot → AI Analysis → Action automation.

### Testing Suite (`tests/`)
- **`test_screenclicker.py`** - Streamlined test suite with 7 comprehensive tests:
  - `test_mouse_operations()` - Mouse click coordinate handling and validation
  - `test_keyboard_operations()` - Text input scenarios with various character sets
  - `test_cursor_movement()` - Smooth circular cursor movement validation using ydotool
  - `test_screen_capture()` - All screenshot functions (full, region, monitor, bytes/file output)
  - `test_screen_info()` - Monitor detection and information gathering
  - `test_terminal_automation()` - Complete terminal workflow automation (slow)
  - `test_integration_workflow()` - Combined mouse + keyboard operations (slow)
- **`test_ollama.py`** - Comprehensive Ollama integration tests with 11 tests:
  - Real server integration testing (no mocks)
  - Connection and model management validation
  - Chat and text generation with streaming support
  - Error handling for non-existent models
  - Convenience function testing
  - All tests skip gracefully when Ollama server unavailable

### Package Structure
- **`setup.py`** - Package configuration and dependencies
- **`pytest.ini`** - Test configuration and markers
- **`requirements.txt`** - Project dependencies
- **`README.md`** - Quick start guide and usage
- **`.gitignore`** - Comprehensive Python project gitignore

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

### Local LLM and VLM Integration (Ollama Solution)
- **Implementation**: Full-featured client for locally hosted Ollama servers with multimodal support
- **Text Capabilities**: Chat completion, text generation, streaming responses, model management
- **Vision Capabilities**: Image analysis, screenshot description, file-based image processing
- **API Support**: List models, show details, pull models, generate embeddings, image + text input
- **Connection Management**: Robust connection testing with graceful fallbacks
- **Default Model**: gemma3:27b (supports both text and image processing)
- **Status**: ✅ **Fully Working** with comprehensive real-server testing and VLM integration

### Cloud LLM and VLM Integration (OpenRouter Solution)
- **Implementation**: OpenRouter API client using OpenAI-compatible interface for cloud AI access
- **Text Capabilities**: Chat completion, text generation, streaming responses with premium models
- **Vision Capabilities**: Image analysis with GPT-4o Mini, Gemini 2.0, Claude 3.5 Sonnet
- **Free Model Support**: `google/gemma-3-27b-it:free` supports both text and image processing
- **Premium Models**: Access to latest OpenAI, Anthropic, and Google models via API
- **Integration**: Works alongside local Ollama for hybrid local/cloud AI workflows
- **Status**: ✅ **Fully Working** with comprehensive vision model testing and authentication handling

### Key Breakthroughs
1. **Mouse automation**: uinput virtual devices bypass Wayland mouse restrictions
2. **Keyboard automation**: Pure uinput solution provides consistent text input across all applications
3. **Screen capture**: grim integration provides native Wayland screenshot capabilities
4. **Cursor movement**: ydotool provides smooth visible movement without special permissions
5. **Modular architecture**: Clean separation of concerns with mouse, keyboard, screen, ollama, and openrouter modules
6. **Monitor-specific capture**: Direct monitor screenshot capability for ViT and AI workflows
7. **Local LLM integration**: Full Ollama client with streaming, model management, and robust testing
8. **Cloud LLM integration**: OpenRouter client with free gemma3 and premium vision model support
9. **Complete screen interaction pipeline**: Screenshot → AI Analysis → Action automation workflow
10. **Dual AI support**: Hybrid local/cloud AI with both Ollama and OpenRouter integration
11. **Vision Language Model integration**: Complete VLM workflow with gemma3:27b multimodal support (local + cloud)
12. **Test methodology**: Comprehensive pytest suites with real integration testing and graceful fallbacks

## Dependencies

### Python Dependencies
- `python-uinput>=1.0.1` - Low-level input device creation for mouse and keyboard
- `Pillow>=8.0.0` - Image processing and manipulation capabilities
- `ollama>=0.1.0` - Official Ollama Python client for local LLM integration
- `openai>=1.0.0` - OpenAI client for OpenRouter cloud AI integration
- `pytest>=7.0.0` - Testing framework

### System Dependencies  
- `ydotool` - Wayland-compatible cursor movement without special permissions
  - Install: `sudo apt install ydotool`
- `grim` - Wayland screenshot capture
  - Install: `sudo apt install grim`
- `ollama` (optional) - Local LLM and VLM server for AI integration
  - Install: Follow instructions at https://ollama.com/
  - For text + image processing: `ollama pull gemma3:27b`
  - For full test coverage: `ollama pull gemma3:27b`

## Usage Examples

```python
# Complete API - works on Wayland/Sway (now with modular structure + VLM integration)
from screenclicker import (
    right_click, left_click, move_mouse, text, 
    screenshot, screenshot_region, screenshot_monitor, get_screen_info,
    OllamaClient, quick_chat, quick_generate,
    describe_image, screenshot_and_describe, data_from_path, describe_image_from_path
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

# VLM (Vision Language Model) integration - Complete workflow
# Method 1: Screenshot analysis
screenshot_data = screenshot_monitor(1)  # Capture 4K monitor
description = describe_image(screenshot_data, "What applications are visible on this screen?")
print(description)

# Method 2: One-liner screenshot analysis  
description = screenshot_and_describe("Describe the desktop and find any buttons")

# Method 3: File-based image analysis
image_data = data_from_path("path/to/screenshot.jpg")
description = describe_image(image_data, "What do you see?")

# Method 4: File analysis one-liner
description = describe_image_from_path("data/sc.jpg", "What type of content is this?")

# Text-only LLM integration (uses gemma3:27b by default)
response = quick_chat(prompt="What should I do next?")
generated_text = quick_generate(prompt="Write a haiku about automation")

# VLM + Automation workflow example
description = screenshot_and_describe("Find the login button")
# Parse description to find coordinates, then click
# left_click(predicted_x, predicted_y)    # Click based on VLM analysis

# Full client with streaming (supports both text and images)
client = OllamaClient()
if client.is_connected():
    models = client.list()
    print(f"Available models: {[m['name'] for m in models['models']]}")
    
    # Streaming chat with image
    screenshot_data = screenshot()
    for chunk in client.chat("gemma3:27b", [{"role": "user", "content": "What's on screen?"}], 
                            images=[screenshot_data], stream=True):
        print(chunk['message']['content'], end='', flush=True)
```

## Environment Compatibility

- **OS**: Linux with Wayland compositor
- **Tested on**: Sway window manager with dual monitor setup (1920x1200 + 3840x2160)
- **Mouse clicks**: ✅ **Fully Working** via uinput virtual devices
- **Cursor movement**: ✅ **Fully Working** via ydotool (smooth circular motion)
- **Keyboard**: ✅ **Fully Working** via pure uinput implementation
- **Terminal automation**: ✅ **Fully Working** with direct process management
- **Multi-monitor**: ✅ **Fully Working** with individual monitor capture
- **Local LLMs**: ✅ **Fully Working** with Ollama server integration

## Testing & Quality Assurance

**Test Suite**: 18 comprehensive tests across 2 test files
- **ScreenClicker Tests**: 7 streamlined tests for core automation functionality
  - **Fast tests** (5): Core functionality validation, streamlined for efficiency
  - **Slow tests** (2): Terminal automation workflows, integration testing  
- **Ollama Tests**: 11 integration tests for LLM functionality
  - **All tests** are slow (real server integration testing)
  - Requires Ollama server with **gemma3:27b model** specifically
  - Tests skip gracefully with clear messages when model unavailable

**Test coverage**:
- `test_mouse_operations()` - Mouse click operations across coordinate ranges
- `test_keyboard_operations()` - Text input with various character sets and symbols
- `test_cursor_movement()` - Smooth circular cursor movement (24-point circle)
- `test_screen_capture()` - All screenshot functions including monitor capture
- `test_screen_info()` - Monitor detection and information gathering
- `test_terminal_automation()` - Complete terminal workflow automation (slow)
- `test_integration_workflow()` - Combined mouse + keyboard operations (slow)
- `test_ollama_*()` - 11 comprehensive Ollama integration tests (requires gemma3:27b model)

**Run tests**:
```bash
pytest                              # All tests (18 tests total, requires Ollama + gemma3:27b for full coverage)
pytest -m "not slow"                # Fast tests only (5 tests, ~17 seconds)
pytest tests/test_screenclicker.py  # ScreenClicker tests only (7 tests)
pytest tests/test_ollama.py         # Ollama integration tests only (11 tests, requires gemma3:27b)
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
9. **Ollama Integration**: Added comprehensive local LLM support with full client and convenience functions
10. **Repository Cleanup**: Added proper .gitignore and removed cache files from version control
11. **Global Configuration**: Added configuration system for Ollama hostname, port, and model settings
12. **Test Standardization**: Updated Ollama tests to use gemma3:27b model specifically for consistency
13. **System Prompt Support**: Added configurable system prompts for customized LLM behavior
14. **Vision Language Model Integration**: Complete VLM workflow with image analysis and file helpers
15. **Multimodal Default**: Updated to gemma3:27b as default model supporting both text and images
16. **Final Achievement**: Production-ready modular Wayland automation + VLM platform

## Architecture & Security

- **Modular Design**: Separated concerns into mouse.py, keyboard.py, screen.py, and ollama_client.py modules
- **Mouse control**: Creates virtual mouse devices via uinput for clicks (no root required)
- **Cursor movement**: Uses ydotool for visible movement without special permissions
- **Keyboard input**: Pure uinput virtual devices for consistent cross-application input
- **Process management**: Direct subprocess control for reliable application launching
- **Focus management**: Click-to-focus ensures input reaches correct applications
- **AI Integration**: Secure local LLM and VLM access via Ollama with no external API calls
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
- ✅ **Local LLM workflows**: Chat completion, text generation, streaming responses with Ollama
- ✅ **VLM Integration**: Complete vision-language model workflow with image analysis
- ✅ **Screenshot Analysis**: Real-time screen content description using gemma3:27b
- ✅ **File-based Image Processing**: Direct image analysis from file paths with convenience helpers
- ✅ **AI-guided automation**: Combine screen capture + VLM analysis + automated actions

**Production ready**: Complete modular automation + VLM platform with minimal dependencies provides reliable GUI testing, process automation, screen analysis, VLM-controlled automation, and local multimodal AI integration on Wayland systems. Clean architecture supports easy maintenance and extension.