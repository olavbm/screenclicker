"""Comprehensive test suite for ScreenClicker library."""

import time
import pytest
import subprocess
import uinput
from screenclicker import right_click, left_click, text


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


def test_library_api():
    """Test core library functions: right_click, left_click, text."""
    print("\n=== Testing Library API ===")
    
    # Test basic function calls
    assert right_click(400, 400) is True
    assert left_click(500, 500) is True
    assert text("test string") is True
    
    # Test parameter validation
    assert right_click(0, 0) is True
    assert left_click(1920, 1080) is True
    
    # Test text with special characters
    assert text("Hello, World! @#$%^&*()") is True
    
    print("✓ All API functions working")


def test_mouse_coordinates():
    """Test mouse click coordinate handling."""
    print("\n=== Testing Mouse Coordinates ===")
    
    # Test different coordinate ranges
    coordinates = [
        (100, 100),   # Top-left area
        (960, 540),   # Center screen
        (1800, 1000), # Bottom-right area
        (0, 0),       # Edge case
    ]
    
    for x, y in coordinates:
        assert left_click(x, y) is True
        time.sleep(0.1)
        assert right_click(x, y) is True
        time.sleep(0.1)
    
    print("✓ Mouse coordinate handling working")


def test_text_input_scenarios():
    """Test various text input scenarios."""
    print("\n=== Testing Text Input Scenarios ===")
    
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
        time.sleep(0.1)
    
    print("✓ Text input scenarios working")


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