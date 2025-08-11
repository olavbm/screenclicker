"""Screen operations for ScreenClicker."""

import subprocess
import tempfile
import os
import json


def screenshot(output_path=None):
    """Take a full screenshot using grim.
    
    Args:
        output_path: Path to save screenshot. If None, returns image bytes.
        
    Returns:
        True if successful (when output_path provided), or bytes data
    """
    try:
        if output_path:
            # Save to specified path
            result = subprocess.run(['grim', output_path], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=10)
            if result.returncode == 0:
                return True
            else:
                raise RuntimeError(f"grim failed: {result.stderr}")
        else:
            # Return bytes data
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                tmp_path = tmp.name
            
            try:
                result = subprocess.run(['grim', tmp_path], 
                                      capture_output=True, 
                                      text=True, 
                                      timeout=10)
                if result.returncode == 0:
                    with open(tmp_path, 'rb') as f:
                        return f.read()
                else:
                    raise RuntimeError(f"grim failed: {result.stderr}")
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
                    
    except FileNotFoundError:
        raise RuntimeError("grim not found. Install with: apt install grim")
    except subprocess.TimeoutExpired:
        raise RuntimeError("Screenshot timed out")
    except Exception as e:
        raise RuntimeError(f"Screenshot failed: {e}")


def screenshot_region(x, y, width, height, output_path=None):
    """Take a screenshot of a specific region using grim.
    
    Args:
        x, y: Top-left coordinates of region
        width, height: Size of region
        output_path: Path to save screenshot. If None, returns image bytes.
        
    Returns:
        True if successful (when output_path provided), or bytes data
    """
    try:
        geometry = f"{x},{y} {width}x{height}"
        
        if output_path:
            # Save to specified path
            result = subprocess.run(['grim', '-g', geometry, output_path], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=10)
            if result.returncode == 0:
                return True
            else:
                raise RuntimeError(f"grim failed: {result.stderr}")
        else:
            # Return bytes data
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                tmp_path = tmp.name
            
            try:
                result = subprocess.run(['grim', '-g', geometry, tmp_path], 
                                      capture_output=True, 
                                      text=True, 
                                      timeout=10)
                if result.returncode == 0:
                    with open(tmp_path, 'rb') as f:
                        return f.read()
                else:
                    raise RuntimeError(f"grim failed: {result.stderr}")
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
                    
    except FileNotFoundError:
        raise RuntimeError("grim not found. Install with: apt install grim")
    except subprocess.TimeoutExpired:
        raise RuntimeError("Screenshot timed out")
    except Exception as e:
        raise RuntimeError(f"Screenshot failed: {e}")


def get_screen_info():
    """Get screen/monitor information.
    
    Returns:
        dict with screen information
    """
    try:
        # Try to get monitor info using swaymsg if available
        try:
            result = subprocess.run(['swaymsg', '-t', 'get_outputs'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            if result.returncode == 0:
                outputs = json.loads(result.stdout)
                monitors = []
                for output in outputs:
                    if output.get('active'):
                        rect = output.get('rect', {})
                        monitors.append({
                            'name': output.get('name', 'unknown'),
                            'x': rect.get('x', 0),
                            'y': rect.get('y', 0),
                            'width': rect.get('width', 1920),
                            'height': rect.get('height', 1200),
                            'primary': output.get('primary', False)
                        })
                return {'monitors': monitors}
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        
        # Fallback: basic screen info
        return {
            'monitors': [{
                'name': 'default',
                'x': 0,
                'y': 0,
                'width': 1920,
                'height': 1200,
                'primary': True
            }]
        }
        
    except Exception as e:
        # Ultimate fallback
        return {
            'monitors': [{
                'name': 'fallback',
                'x': 0,
                'y': 0,
                'width': 1920,
                'height': 1200,
                'primary': True
            }]
        }


def screenshot_monitor(monitor_index=0, output_path=None):
    """Take a screenshot of a specific monitor.
    
    Args:
        monitor_index: Index of monitor to capture (0 = first monitor, 1 = second, etc.)
        output_path: Path to save screenshot. If None, returns image bytes.
        
    Returns:
        True if successful (when output_path provided), or bytes data
        
    Raises:
        RuntimeError: If monitor index is invalid or screenshot fails
    """
    try:
        # Get monitor information
        screen_info = get_screen_info()
        monitors = screen_info['monitors']
        
        if monitor_index < 0 or monitor_index >= len(monitors):
            raise RuntimeError(f"Invalid monitor index {monitor_index}. Available monitors: 0-{len(monitors)-1}")
        
        monitor = monitors[monitor_index]
        
        # Use screenshot_region to capture the specific monitor
        return screenshot_region(
            monitor['x'], 
            monitor['y'], 
            monitor['width'], 
            monitor['height'], 
            output_path
        )
        
    except Exception as e:
        raise RuntimeError(f"Monitor screenshot failed: {e}")
