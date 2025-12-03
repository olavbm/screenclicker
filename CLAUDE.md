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
2. **Input automation** - Mouse clicks via `uinput`, cursor movement via `ydotool`
3. **VLM integration** - Ollama client for local vision models

## Project Structure

```
screenclicker/
├── chat.py              # Ask VLM about screen: python chat.py "what do you see?"
├── run.py               # Execute commands: python run.py "click the button"
├── screenclicker/
│   ├── __init__.py      # Package exports
│   ├── config.py        # Ollama config (host, port, model)
│   ├── keyboard.py      # text() - keyboard input via uinput
│   ├── mouse.py         # left_click(), right_click(), move_mouse()
│   ├── ollama_client.py # OllamaClient, describe_image(), etc.
│   └── screen.py        # screenshot(), screenshot_monitor(), get_screen_info()
└── tests/               # Pytest test suite
```

## Core API

### Mouse (`mouse.py`)
- `left_click(x, y, monitor_index=None)` - Left click via uinput
- `right_click(x, y, monitor_index=None)` - Right click via uinput
- `move_mouse(x, y, monitor_index=None)` - Move cursor via ydotool
- `set_target_monitor(index)` - Set default monitor for clicks
- `get_target_monitor()` - Get current target monitor

Coordinates are relative to the target monitor. The functions automatically offset to global screen coordinates for multi-monitor setups.

### Screen (`screen.py`)
- `screenshot()` - Full screen capture
- `screenshot_monitor(index)` - Capture specific monitor
- `screenshot_region(x, y, w, h)` - Capture region
- `get_screen_info()` - Get monitor layout info

### Keyboard (`keyboard.py`)
- `text(string)` - Type text via uinput

### VLM (`ollama_client.py`)
- `OllamaClient` - Full client with chat, generate, streaming
- `describe_image(bytes, prompt)` - Analyze image
- `screenshot_and_describe(prompt, monitor)` - Screenshot + analyze
- `quick_chat(prompt, images)` - Quick chat completion

### Config (`config.py`)
- `set_model(name)` - Set default model (default: qwen3-vl:30b)
- `set_host(host)` - Set Ollama host
- `set_port(port)` - Set Ollama port
- Environment variables: `OLLAMA_HOST`, `OLLAMA_PORT`, `OLLAMA_MODEL`

## CLI Scripts

### chat.py - Ask VLM about screen
```bash
python chat.py "what do you see?"
python chat.py -m 1 "describe this monitor"
```

### run.py - Execute natural language commands
```bash
python run.py "click the start button"
python run.py -m 1 "click the close button"
python run.py -n 5 "click the button"  # 5 samples for averaging
```

Both support `--monitor` / `-m` to select target monitor. `run.py` also supports `--samples` / `-n` to control how many VLM predictions to average (default: 3).

## Environment

- **OS**: Linux with Wayland
- **Window Manager**: Sway
- **VLM**: Ollama with qwen3-vl:30b (SSH tunneled from desktop)
- **Python**: 3.8+
- **Multi-monitor**: Supported (coordinates auto-offset to target monitor)

## System Dependencies

```bash
sudo apt install ydotool grim
# Ollama: https://ollama.com/
ollama pull qwen3-vl:30b
```

## Key Technical Details

### Mouse Input (Hybrid Approach)
- **Clicks**: uinput virtual device (no daemon needed)
- **Cursor movement**: ydotool (requires `ydotoold &` for visible movement)
- **Multi-monitor**: Coordinates offset by monitor position automatically

### Screen Capture
- Uses `grim` for Wayland-native screenshots
- Returns PNG bytes by default
- Per-monitor capture via `screenshot_monitor(index)`

### VLM Integration
- Local Ollama server (can be remote via SSH tunnel)
- Default model: qwen3-vl:30b
- Images sent as base64 in chat API

## Testing

```bash
pytest                    # All tests
pytest -m "not slow"      # Fast tests only
```

## Target Game: A Dark Room

[A Dark Room](https://adarkroom.doublespeakgames.com/) is a text-based incremental game with:
- Button clicks (stoke fire, gather wood, check traps)
- Resource management
- Exploration mechanics
- Minimal UI - good for VLM parsing
