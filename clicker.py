#!/usr/bin/env python3

import time
import math
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
        return None
    except Exception as e:
        print(f"❌ Failed to create mouse device: {e}")
        return None

def right_click(x, y):
    """Right click using absolute positioning.""" 
    device = create_mouse_device()
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
    finally:
        if device:
            device.destroy()

def move_mouse_circle(center_x=500, center_y=500, radius=100, duration=3.0):
    """Move mouse in a circle around the given center point."""
    device = create_mouse_device()
    if not device:
        return False
        
    try:
        print(f"Moving mouse in circle: center=({center_x}, {center_y}), radius={radius}")
        
        # Calculate how many steps for smooth movement
        steps = 60  # 60 points around the circle
        step_delay = duration / steps
        
        for i in range(steps + 1):  # +1 to complete the circle
            angle = (2 * math.pi * i) / steps  # Angle in radians
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            device.emit(uinput.ABS_X, int(x))
            device.emit(uinput.ABS_Y, int(y))
            device.syn()
            
            if i % 10 == 0:  # Report progress every 10 steps
                print(f"  Position: ({int(x)}, {int(y)})")
            
            time.sleep(step_delay)
        
        print("✓ Circle movement completed")
        return True
    except Exception as e:
        print(f"❌ Circle movement failed: {e}")
        return False
    finally:
        if device:
            device.destroy()

if __name__ == "__main__":
    print("=== Mouse Circle Demo ===")
    print("Watch your mouse cursor move in a circle!")
    print("Starting in 3 seconds...")
    
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    # Move mouse in circle
    move_mouse_circle(center_x=500, center_y=400, radius=150, duration=5.0)
    
    time.sleep(1)
    
    # Test right click at center
    print("\nTesting right click at center...")
    right_click(500, 400)