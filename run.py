#!/usr/bin/env python3
"""
Run a natural language command to interact with the screen.

Usage:
    python run.py "click the fourier text"
    python run.py "click the close button"
"""

import sys
from screenclicker import left_click, screenshot_monitor, OllamaClient


def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py \"<command>\"")
        print("Example: python run.py \"click the fourier text\"")
        sys.exit(1)

    command = sys.argv[1]
    print(f"Command: {command}")

    # Take screenshot
    print("Taking screenshot...")
    img = screenshot_monitor(0)

    # Ask VLM for coordinates
    client = OllamaClient()

    prompt = f"""Look at this screenshot. The user wants to: {command}

Find the exact pixel coordinates (x, y) where I should click.
Response format - just the coordinates, nothing else:
x,y"""

    print("Asking VLM for coordinates...")
    response = client.chat(
        "qwen3-vl:4b",
        [{"role": "user", "content": prompt}],
        images=[img]
    )

    result = response['message']['content'].strip()
    print(f"VLM response: {result}")

    # Parse coordinates
    try:
        # Handle various formats: "x,y" or "x, y" or "(x,y)"
        result = result.replace("(", "").replace(")", "").replace(" ", "")
        x, y = map(int, result.split(","))
        print(f"Clicking at ({x}, {y})...")
        left_click(x, y)
        print("Done!")
    except ValueError:
        print(f"Could not parse coordinates from: {result}")
        sys.exit(1)


if __name__ == "__main__":
    main()
