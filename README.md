# ScreenClicker - VLM-Powered Game Automation for Wayland

A Python library for screen automation on **Sway/Wayland** systems, designed to enable Vision Language Models (VLMs) to play browser games autonomously.

**Goal**: Build an AI agent that can play [A Dark Room](https://adarkroom.doublespeakgames.com/) using locally-hosted VLMs.

## How It Works

```
Screenshot → VLM Analysis → Decision → Mouse/Keyboard Action → Repeat
```

1. Capture the screen using Wayland-native tools
2. Send screenshot to a locally-hosted VLM (e.g., Qwen3-VL via Ollama)
3. VLM analyzes the game state and decides on an action
4. Execute mouse clicks or keyboard input via uinput virtual devices
5. Loop

## Installation

```bash
# Python dependencies
pip install -e .

# System dependencies (Arch/Debian)
sudo apt install ydotool grim

# Ollama for local VLM hosting
# See: https://ollama.com/
ollama pull qwen3-vl:4b
```

## Quick Start

```python
from screenclicker import (
    left_click, text, screenshot_monitor,
    OllamaClient, describe_image, screenshot_and_describe
)

# Take a screenshot and ask the VLM what's on screen
description = screenshot_and_describe("What buttons are visible?")
print(description)

# Or step by step:
client = OllamaClient()
screenshot_bytes = screenshot_monitor(0)
response = client.chat(
    "qwen3-vl:4b",
    [{"role": "user", "content": "What should I click next in this game?"}],
    images=[screenshot_bytes]
)
print(response['message']['content'])

# Execute actions
left_click(500, 300)
text("hello")
```

## Core API

### Screen Capture
```python
screenshot()                    # Full screen as bytes
screenshot("file.png")          # Save to file
screenshot_monitor(0)           # Capture specific monitor
screenshot_region(x, y, w, h)   # Capture region
get_screen_info()               # Monitor layout info
```

### Mouse & Keyboard
```python
left_click(x, y)    # Left click at coordinates
right_click(x, y)   # Right click at coordinates
move_mouse(x, y)    # Move cursor
text("string")      # Type text
```

### VLM Integration (Ollama)
```python
OllamaClient(host="http://localhost:11434")  # Connect to Ollama
describe_image(image_bytes, "prompt")         # Analyze image
screenshot_and_describe("prompt")             # Screenshot + analyze
quick_chat(model="qwen3-vl:4b", prompt="...")  # Chat completion
```

## System Requirements

- **OS**: Linux with Wayland compositor
- **Window Manager**: Sway (tested)
- **VLM Server**: Ollama with a vision model (qwen3-vl recommended)
- **Python**: 3.8+

## Testing

```bash
pytest                    # All tests
pytest -m "not slow"      # Fast tests only
python test_qwen3vl.py    # Test VLM connection
```

## Project Status

Building toward autonomous gameplay of [A Dark Room](https://adarkroom.doublespeakgames.com/).

Current capabilities:
- Screen capture on Wayland/Sway
- Mouse clicks and keyboard input via uinput
- VLM integration via Ollama (local) and OpenRouter (cloud)
- Screenshot analysis with vision models

Next steps:
- Game state parsing
- Action decision loop
- Memory/context management for game progress
