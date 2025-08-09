"""Image preprocessing for VLM-friendly screenshots."""

from PIL import Image, ImageDraw
import io


def add_grid(image_bytes, grid_size=50, color='red', opacity=0.3):
    """Add a coordinate grid overlay to screenshot for VLM spatial reference.
    
    Args:
        image_bytes: Screenshot image data as bytes
        grid_size: Spacing between grid lines in pixels (default: 50)
        color: Grid line color (default: 'red')
        opacity: Grid opacity from 0.0 to 1.0 (default: 0.3)
        
    Returns:
        bytes: Processed image with grid overlay
    """
    try:
        # Open image from bytes
        img = Image.open(io.BytesIO(image_bytes))
        
        # Create overlay for grid
        overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)
        
        width, height = img.size
        
        # Convert color name to RGB if needed
        if isinstance(color, str):
            color_map = {
                'red': (255, 0, 0),
                'green': (0, 255, 0),
                'blue': (0, 0, 255),
                'white': (255, 255, 255),
                'black': (0, 0, 0),
                'yellow': (255, 255, 0),
                'cyan': (0, 255, 255),
                'magenta': (255, 0, 255)
            }
            rgb_color = color_map.get(color.lower(), (255, 0, 0))  # Default to red
        else:
            rgb_color = color
            
        # Calculate alpha value from opacity
        alpha = int(opacity * 255)
        rgba_color = rgb_color + (alpha,)
        
        # Draw vertical lines
        for x in range(0, width, grid_size):
            draw.line([(x, 0), (x, height)], fill=rgba_color, width=1)
            
        # Draw horizontal lines  
        for y in range(0, height, grid_size):
            draw.line([(0, y), (width, y)], fill=rgba_color, width=1)
        
        # Convert base image to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
            
        # Composite overlay onto original image
        result = Image.alpha_composite(img, overlay)
        
        # Convert back to RGB if input was RGB
        if image_bytes[:4] == b'\x89PNG':
            # Keep as RGBA for PNG to preserve transparency
            pass
        else:
            result = result.convert('RGB')
        
        # Save to bytes
        output_buffer = io.BytesIO()
        result.save(output_buffer, format='PNG')
        return output_buffer.getvalue()
        
    except Exception as e:
        raise RuntimeError(f"Grid overlay failed: {e}")