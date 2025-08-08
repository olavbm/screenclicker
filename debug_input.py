#!/usr/bin/env python3

import os
import sys

def check_environment():
    """Check the current environment and permissions."""
    print("=== Environment Check ===")
    print(f"Python version: {sys.version}")
    print(f"Session type: {os.environ.get('XDG_SESSION_TYPE', 'unknown')}")
    print(f"Display: {os.environ.get('DISPLAY', 'not set')}")
    print(f"Wayland display: {os.environ.get('WAYLAND_DISPLAY', 'not set')}")
    print(f"Desktop session: {os.environ.get('XDG_CURRENT_DESKTOP', 'unknown')}")
    print(f"User: {os.environ.get('USER', 'unknown')}")
    
    # Check groups
    try:
        import grp
        groups = [g.gr_name for g in grp.getgrall() if os.environ.get('USER', '') in g.gr_mem]
        print(f"User groups: {groups}")
    except:
        print("Could not get user groups")

def test_pynput_basic():
    """Test basic pynput functionality."""
    print("\n=== Testing pynput ===")
    
    try:
        from pynput.keyboard import Controller as KeyboardController
        from pynput.mouse import Controller as MouseController
        
        print("✓ pynput imports successful")
        
        # Test keyboard controller
        kb = KeyboardController()
        print("✓ Keyboard controller created")
        
        # Test mouse controller  
        mouse = MouseController()
        print("✓ Mouse controller created")
        print(f"Current mouse position: {mouse.position}")
        
    except Exception as e:
        print(f"✗ pynput error: {e}")

def test_window_info():
    """Try to get window information."""
    print("\n=== Window Information ===")
    
    # Try different methods to get window info
    methods = [
        ("xdotool", ["xdotool", "getactivewindow"]),
        ("wmctrl", ["wmctrl", "-a"]),
        ("swaymsg", ["swaymsg", "-t", "get_tree"]),
    ]
    
    import subprocess
    
    for name, cmd in methods:
        try:
            result = subprocess.run(cmd[:1] + ["--version"], capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                print(f"✓ {name} is available")
                try:
                    if name == "swaymsg":
                        result = subprocess.run(["swaymsg", "-t", "get_tree"], capture_output=True, text=True, timeout=2)
                        if result.returncode == 0:
                            print(f"Sway compositor detected")
                    elif name == "xdotool":
                        result = subprocess.run(["xdotool", "getactivewindow"], capture_output=True, text=True, timeout=2)
                        if result.returncode == 0:
                            print(f"Active window ID: {result.stdout.strip()}")
                except:
                    pass
            else:
                print(f"✗ {name} not working")
        except FileNotFoundError:
            print(f"✗ {name} not installed")
        except Exception as e:
            print(f"✗ {name} error: {e}")

def test_direct_typing():
    """Test if we can type anything at all."""
    print("\n=== Direct Typing Test ===")
    
    try:
        from pynput.keyboard import Controller, Key
        import time
        
        kb = Controller()
        
        print("Attempting to type 'TEST' in 3 seconds...")
        print("Focus any text input now!")
        
        time.sleep(3)
        
        # Try different approaches
        print("Method 1: Using .type()")
        kb.type("TEST1")
        time.sleep(1)
        
        print("Method 2: Using individual key presses")
        for char in "TEST2":
            kb.press(char)
            kb.release(char)
            time.sleep(0.1)
        
        print("Method 3: Using Key constants")
        kb.press(Key.space)
        kb.release(Key.space)
        kb.type("TEST3")
        
        print("Typing test completed!")
        
    except Exception as e:
        print(f"Direct typing failed: {e}")

if __name__ == "__main__":
    check_environment()
    test_pynput_basic()
    test_window_info()
    test_direct_typing()