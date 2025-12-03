#!/usr/bin/env python3
"""
Run a natural language command to interact with the screen.

Usage:
    python run.py "click the fourier text"
    python run.py "click the close button"
    python run.py --monitor 1 "click the button"
"""

import sys
import argparse
import io
import re
from PIL import Image
from screenclicker import left_click, screenshot_monitor, OllamaClient, set_target_monitor
from screenclicker.config import get_model


def parse_coordinates(text):
    """Parse x,y coordinates from VLM response."""
    # Remove common formatting
    text = text.replace("(", "").replace(")", "").replace(" ", "")
    # Find pattern like "123,456"
    match = re.search(r'(\d+),(\d+)', text)
    if match:
        return int(match.group(1)), int(match.group(2))
    raise ValueError(f"Could not parse coordinates from: {text}")


def get_coordinates(client, model, img, width, height, command):
    """Ask VLM for coordinates once."""
    prompt = f"""This screenshot is {width}x{height} pixels.
The top-left corner is (0,0), bottom-right is ({width-1},{height-1}).

Task: {command}

Find the CENTER of the target element.
Respond with ONLY x,y coordinates (e.g., 500,300):"""

    response = client.chat(
        model,
        [{"role": "user", "content": prompt}],
        images=[img]
    )
    return response['message']['content'].strip()


def main():
    parser = argparse.ArgumentParser(description="Run natural language screen commands")
    parser.add_argument("command", help="Command to execute (e.g., 'click the button')")
    parser.add_argument("--monitor", "-m", type=int, default=0, help="Monitor index (default: 0)")
    parser.add_argument("--samples", "-n", type=int, default=3, help="Number of predictions to average (default: 3)")
    args = parser.parse_args()

    set_target_monitor(args.monitor)
    command = args.command
    print(f"Command: {command}")
    print(f"Monitor: {args.monitor}")

    # Take screenshot
    print("Taking screenshot...")
    img = screenshot_monitor(args.monitor)

    # Get dimensions
    pil_img = Image.open(io.BytesIO(img))
    width, height = pil_img.size
    print(f"Screenshot size: {width}x{height}")

    # Ask VLM multiple times and average
    client = OllamaClient()
    model = get_model()
    predictions = []

    print(f"Getting {args.samples} predictions...")
    for i in range(args.samples):
        result = get_coordinates(client, model, img, width, height, command)
        try:
            x, y = parse_coordinates(result)
            print(f"  #{i+1}: ({x}, {y})")
            predictions.append((x, y))
        except ValueError as e:
            print(f"  #{i+1}: Failed to parse - {result}")

    if not predictions:
        print("No valid predictions received")
        sys.exit(1)

    # Average the predictions
    avg_x = sum(p[0] for p in predictions) // len(predictions)
    avg_y = sum(p[1] for p in predictions) // len(predictions)

    print(f"Average: ({avg_x}, {avg_y})")
    print(f"Clicking...")
    left_click(avg_x, avg_y)
    print("Done!")


if __name__ == "__main__":
    main()
