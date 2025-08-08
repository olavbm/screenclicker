#!/usr/bin/env python3
"""
Mouse clicker using uinput for Wayland/Sway
This bypasses Wayland security by creating a virtual input device.
"""

import time
import uinput

def create_mouse_device():
    """Create a virtual mouse device with uinput."""
    try:
        device = uinput.Device([
            uinput.BTN_LEFT,
            uinput.BTN_RIGHT, 
            uinput.BTN_MIDDLE,
            uinput.REL_X,
            uinput.REL_Y,
            # Try absolute positioning too
            uinput.ABS_X + (0, 1920, 0, 0),  # Screen width range
            uinput.ABS_Y + (0, 1080, 0, 0),  # Screen height range
        ])
        print("✓ Virtual mouse device created successfully")
        return device
    except PermissionError:
        print("❌ Permission denied - need root access or proper udev rules")
        print("Try: sudo python3 uinput_clicker.py")
        return None
    except Exception as e:
        print(f"❌ Failed to create mouse device: {e}")
        return None

def right_click_relative(device, rel_x, rel_y):
    """Right click using relative movement."""
    if not device:
        return False
    
    try:
        print(f"Moving mouse relative ({rel_x}, {rel_y})")
        device.emit(uinput.REL_X, rel_x)
        device.emit(uinput.REL_Y, rel_y) 
        device.syn()
        
        time.sleep(0.1)
        
        print("Performing right click...")
        device.emit(uinput.BTN_RIGHT, 1)  # Press
        device.syn()
        time.sleep(0.05)
        device.emit(uinput.BTN_RIGHT, 0)  # Release  
        device.syn()
        
        print("✓ Right click completed")
        return True
    except Exception as e:
        print(f"❌ Right click failed: {e}")
        return False

def right_click_absolute(device, x, y):
    """Right click using absolute positioning.""" 
    if not device:
        return False
        
    try:
        print(f"Moving mouse to absolute position ({x}, {y})")
        device.emit(uinput.ABS_X, x)
        device.emit(uinput.ABS_Y, y)
        device.syn()
        
        time.sleep(0.1)
        
        print("Performing right click...")
        device.emit(uinput.BTN_RIGHT, 1)  # Press
        device.syn()
        time.sleep(0.05)
        device.emit(uinput.BTN_RIGHT, 0)  # Release
        device.syn()
        
        print("✓ Absolute right click completed")
        return True
    except Exception as e:
        print(f"❌ Absolute right click failed: {e}")
        return False

def test_uinput_mouse():
    """Test uinput mouse functionality."""
    print("=== UInput Mouse Test ===")
    
    device = create_mouse_device()
    if not device:
        return False
    
    try:
        print("\n1. Testing relative movement + right click...")
        print("Watch for mouse movement and context menu...")
        time.sleep(2)
        right_click_relative(device, 50, 50)
        
        time.sleep(2)
        
        print("\n2. Testing absolute positioning + right click...")
        print("This should move to (400, 400) and right click...")
        time.sleep(2) 
        right_click_absolute(device, 400, 400)
        
        print("\n✓ UInput test completed!")
        return True
        
    finally:
        if device:
            device.destroy()
            print("Device cleaned up")

if __name__ == "__main__":
    success = test_uinput_mouse()
    if not success:
        print("\n=== Troubleshooting ===")
        print("1. Try running with sudo: sudo python3 uinput_clicker.py")
        print("2. Check if uinput module is loaded: lsmod | grep uinput")
        print("3. Check device permissions: ls -l /dev/uinput")