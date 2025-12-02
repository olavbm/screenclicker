# ScreenClicker - VLM Game Automation for Wayland

A Python library for screen automation on Sway/Wayland, designed to enable Vision Language Models to play browser games autonomously.

## Project Goal

Build an AI agent that can play [A Dark Room](https://adarkroom.doublespeakgames.com/) using locally-hosted VLMs (Qwen3-VL via Ollama).

## Architecture

```
Screenshot → VLM Analysis → Decision → Mouse/Keyboard Action → Repeat
```

The library provides:
1. **Screen capture** - Wayland-native via `grim`
2. **Input automation** - Mouse/keyboard via `uinput` virtual devices
3. **VLM integration** - Ollama client for local vision models

## Library Structure

### Core Modules (`screenclicker/`)

- **`mouse.py`** - Mouse operations via uinput
  - `left_click(x, y)`, `right_click(x, y)`, `move_mouse(x, y)`

- **`keyboard.py`** - Keyboard input via uinput
  - `text(string)` - Type text

- **`screen.py`** - Screen capture via grim
  - `screenshot()`, `screenshot_region()`, `screenshot_monitor()`, `get_screen_info()`

- **`ollama_client.py`** - Local VLM integration
  - `OllamaClient` - Full client with chat, generate, streaming
  - `describe_image()`, `screenshot_and_describe()` - Vision helpers
  - `quick_chat()`, `quick_generate()` - Convenience functions

- **`openrouter_client.py`** - Cloud VLM fallback
  - OpenRouter API for cloud-hosted vision models

- **`config.py`** - Ollama configuration
  - Host, port, model, system prompt settings

## Environment

- **OS**: Linux with Wayland
- **Window Manager**: Sway
- **VLM**: Ollama with qwen3-vl:4b (locally hosted, SSH tunneled from desktop)
- **Python**: 3.8+

## System Dependencies

```bash
sudo apt install ydotool grim
# Ollama: https://ollama.com/
ollama pull qwen3-vl:4b
```

## Key Technical Solutions

### Wayland Automation
- **Problem**: Wayland security blocks traditional automation (pynput, pyautogui)
- **Solution**: Linux `uinput` kernel module for virtual devices
- Uses `ydotool` for cursor movement, `grim` for screenshots

### VLM Integration
- Local Ollama server (can be remote via SSH tunnel)
- Qwen3-VL for vision understanding
- Screenshot → base64 → chat API with images

## Testing

```bash
pytest                    # All tests
pytest -m "not slow"      # Fast tests only
python test_qwen3vl.py    # Test VLM connection
```

## Development Notes

- All mouse/keyboard input uses uinput (no root required on most systems)
- Screenshots are PNG bytes by default, can save to file
- VLM responses are synchronous; streaming available via `stream=True`
- Config supports environment variables: `OLLAMA_HOST`, `OLLAMA_PORT`, `OLLAMA_MODEL`

## Target Game: A Dark Room

[A Dark Room](https://adarkroom.doublespeakgames.com/) is a text-based incremental game with:
- Button clicks (stoke fire, gather wood, check traps)
- Resource management
- Exploration mechanics
- Minimal UI - good for VLM parsing

The game state is primarily text-based, making it suitable for VLM analysis.
