"""Comprehensive test suite for ScreenClicker library."""

import time
import pytest
import subprocess
import uinput
import os
import tempfile
from screenclicker import right_click, left_click, text, screenshot, screenshot_region, get_screen_info, move_mouse, screenshot_monitor


class TerminalManager:
    """Manage terminal process lifecycle."""
    
    def __init__(self):
        self.process = None
    
    def open_terminal(self):
        """Open terminal using subprocess."""
        terminals = ['foot', 'alacritty', 'gnome-terminal', 'xterm']
        
        for terminal_cmd in terminals:
            try:
                self.process = subprocess.Popen([terminal_cmd])
                time.sleep(2)
                left_click(960, 540)  # Focus terminal
                time.sleep(0.5)
                return True
            except (FileNotFoundError, Exception):
                continue
        
        return False
    
    def close_terminal(self):
        """Close the terminal process."""
        if self.process:
            try:
                # Ctrl+D to exit
                kb_device = uinput.Device([uinput.KEY_LEFTCTRL, uinput.KEY_D])
                kb_device.emit(uinput.KEY_LEFTCTRL, 1)
                kb_device.emit(uinput.KEY_D, 1)
                kb_device.syn()
                time.sleep(0.01)
                kb_device.emit(uinput.KEY_D, 0)
                kb_device.emit(uinput.KEY_LEFTCTRL, 0)
                kb_device.syn()
                kb_device.destroy()
                time.sleep(1)
                
                if self.process.poll() is None:
                    self.process.terminate()
                    time.sleep(0.5)
                    
                if self.process.poll() is None:
                    self.process.kill()
                
                return True
            except Exception:
                return False
        return True


def press_enter():
    """Press Enter key using uinput."""
    kb_device = uinput.Device([uinput.KEY_ENTER])
    kb_device.emit(uinput.KEY_ENTER, 1)
    kb_device.syn()
    time.sleep(0.01)
    kb_device.emit(uinput.KEY_ENTER, 0)
    kb_device.syn()
    kb_device.destroy()


def test_mouse_operations():
    """Test mouse click and movement operations."""
    print("\n=== Testing Mouse Operations ===")
    
    # Test different coordinate ranges
    coordinates = [
        (100, 100),   # Top-left area
        (960, 540),   # Center screen
        (1800, 1000), # Bottom-right area
        (0, 0),       # Edge case
    ]
    
    for x, y in coordinates:
        assert left_click(x, y) is True
        time.sleep(0.05)
        assert right_click(x, y) is True
        time.sleep(0.05)
    
    print("✓ Mouse click operations working")


def test_keyboard_operations():
    """Test keyboard text input operations."""
    print("\n=== Testing Keyboard Operations ===")
    
    # Test different text types
    test_strings = [
        "Simple text",
        "Numbers: 12345", 
        "Symbols: !@#$%^&*()",
        "Mixed: Hello123!@#",
        "echo 'Terminal command'",
        "Multi word command with spaces"
    ]
    
    for test_string in test_strings:
        assert text(test_string) is True
        time.sleep(0.05)
    
    print("✓ Keyboard text input working")


def test_cursor_movement():
    """Test cursor movement functionality."""
    print("\n=== Testing Cursor Movement ===")
    
    # Test circular cursor movement pattern
    import math
    
    center_x, center_y = 960, 540  # Center of typical screen
    radius = 200  # Circle radius
    steps = 24  # Number of points in circle (smooth motion)
    
    print(f"Moving cursor in circle: center ({center_x}, {center_y}), radius {radius}")
    
    for i in range(steps):
        # Calculate angle for this step
        angle = (2 * math.pi * i) / steps
        
        # Calculate position on circle
        x = int(center_x + radius * math.cos(angle))
        y = int(center_y + radius * math.sin(angle))
        
        assert move_mouse(x, y) is True
        time.sleep(0.001)  # Smooth motion timing
    
    # Return to center
    assert move_mouse(center_x, center_y) is True
    time.sleep(0.01)
    
    print("✓ Circular cursor movement working")


def test_screen_capture():
    """Test all screen capture functionality."""
    print("\n=== Testing Screen Capture ===")
    
    # Test basic screenshot to file
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
        tmp_path = tmp_file.name
    
    try:
        result = screenshot(tmp_path)
        assert result is True
        assert os.path.exists(tmp_path)
        assert os.path.getsize(tmp_path) > 0
        print("✓ Full screenshot to file working")
        
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
    
    # Test screenshot returning bytes
    screenshot_bytes = screenshot()
    assert isinstance(screenshot_bytes, bytes)
    assert len(screenshot_bytes) > 0
    assert screenshot_bytes.startswith(b'\x89PNG')  # PNG signature
    print("✓ Full screenshot bytes working")
    
    # Test region screenshot
    region_bytes = screenshot_region(0, 0, 200, 150)
    assert isinstance(region_bytes, bytes)
    assert len(region_bytes) > 0
    assert region_bytes.startswith(b'\x89PNG')
    print("✓ Region screenshot working")
    
    # Test monitor screenshot (new function)
    monitor_bytes = screenshot_monitor(0)
    assert isinstance(monitor_bytes, bytes)
    assert len(monitor_bytes) > 0
    assert monitor_bytes.startswith(b'\x89PNG')
    print("✓ Monitor screenshot working")




def test_screen_info():
    """Test screen information functionality.""" 
    print("\n=== Testing Screen Info ===")
    
    info = get_screen_info()
    assert isinstance(info, dict)
    assert 'monitors' in info
    assert isinstance(info['monitors'], list)
    assert len(info['monitors']) > 0
    
    # Check first monitor has expected fields
    monitor = info['monitors'][0]
    required_fields = ['name', 'x', 'y', 'width', 'height', 'primary']
    for field in required_fields:
        assert field in monitor
        
    # Basic validation
    assert monitor['width'] > 0
    assert monitor['height'] > 0
    assert isinstance(monitor['x'], int)
    assert isinstance(monitor['y'], int)
    
    print(f"✓ Screen info detected {len(info['monitors'])} monitor(s)")


@pytest.mark.slow
def test_terminal_automation():
    """Test complete terminal automation workflow."""
    print("\n=== Testing Terminal Automation ===")
    
    terminal = TerminalManager()
    
    try:
        # Open terminal
        assert terminal.open_terminal() is True
        
        # Run commands
        commands = [
            "echo 'ScreenClicker Test'",
            "date",
            "whoami",
            "echo 'Automation complete'"
        ]
        
        for command in commands:
            assert text(command) is True
            time.sleep(0.2)
            press_enter()
            time.sleep(0.5)
        
        print("✓ Terminal automation working")
        
    finally:
        terminal.close_terminal()


@pytest.mark.slow
def test_integration_workflow():
    """Test integrated mouse and keyboard operations."""
    print("\n=== Testing Integration Workflow ===")
    
    terminal = TerminalManager()
    
    try:
        # Combined workflow: click to position, then type
        assert terminal.open_terminal() is True
        
        # Click to ensure focus, then type command
        left_click(960, 540)
        time.sleep(0.3)
        
        assert text("echo 'Integration test: mouse + keyboard'") is True
        time.sleep(0.3)
        press_enter()
        time.sleep(0.5)
        
        # Another click and command
        left_click(960, 540)
        time.sleep(0.2)
        
        assert text("ls -la | head -3") is True
        time.sleep(0.3)
        press_enter()
        time.sleep(0.8)
        
        print("✓ Integration workflow working")
        
    finally:
        terminal.close_terminal()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
