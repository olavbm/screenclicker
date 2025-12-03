#!/usr/bin/env python3
"""
Ask the VLM about the current screen.

Usage:
    python chat.py "what do you see here?"
    python chat.py "where is the close button?"
    python chat.py --monitor 1 "describe the UI layout"
"""

import argparse
from screenclicker import screenshot_monitor, OllamaClient
from screenclicker.config import get_model


def main():
    parser = argparse.ArgumentParser(description="Ask VLM about the screen")
    parser.add_argument("prompt", nargs="?", default="What do you see on this screen?",
                        help="Question to ask (default: 'What do you see on this screen?')")
    parser.add_argument("--monitor", "-m", type=int, default=0, help="Monitor index (default: 0)")
    args = parser.parse_args()

    print(f"Prompt: {args.prompt}")
    print(f"Monitor: {args.monitor}")

    # Take screenshot
    print("Taking screenshot...")
    img = screenshot_monitor(args.monitor)
    print(f"Screenshot: {len(img)} bytes")

    # Ask VLM
    print("Asking VLM...")
    client = OllamaClient()
    response = client.chat(
        get_model(),
        [{"role": "user", "content": args.prompt}],
        images=[img]
    )

    print()
    print(response['message']['content'])


if __name__ == "__main__":
    main()
