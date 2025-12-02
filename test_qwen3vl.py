#!/usr/bin/env python3
"""
Test script for Qwen 3 VL via Ollama (SSH tunneled).

Usage:
    python test_qwen3vl.py                    # Uses localhost:11434
    python test_qwen3vl.py --host localhost --port 11434
"""

import argparse
from screenclicker import OllamaClient, screenshot_monitor

DEFAULT_MODEL = "qwen3-vl:4b"


def test_connection(client: OllamaClient) -> bool:
    """Test basic connection to Ollama server."""
    print("Testing connection...")
    if client.is_connected():
        print("  Connected to Ollama server")
        return True
    else:
        print("  FAILED: Cannot connect to Ollama server")
        return False


def test_list_models(client: OllamaClient) -> bool:
    """List available models and check for qwen3-vl."""
    print("\nListing models...")
    try:
        result = client.list()
        # Handle both old format (dict with 'name') and new format (Model objects with .model)
        raw_models = result.get('models', [])
        models = []
        for m in raw_models:
            if hasattr(m, 'model'):
                models.append(m.model)
            elif isinstance(m, dict) and 'name' in m:
                models.append(m['name'])
            elif isinstance(m, dict) and 'model' in m:
                models.append(m['model'])
            else:
                models.append(str(m))
        print(f"  Available models: {models}")

        # Check if qwen3-vl is available
        qwen_models = [m for m in models if 'qwen' in m.lower()]
        if qwen_models:
            print(f"  Found Qwen models: {qwen_models}")
            return True
        else:
            print(f"  WARNING: No Qwen models found. Available: {models}")
            return False
    except Exception as e:
        print(f"  FAILED: {e}")
        return False


def test_text_generation(client: OllamaClient, model: str) -> bool:
    """Test basic text generation."""
    print(f"\nTesting text generation with {model}...")
    try:
        response = client.chat(
            model,
            [{"role": "user", "content": "Say hello in exactly 5 words."}]
        )
        content = response['message']['content']
        print(f"  Response: {content}")
        return True
    except Exception as e:
        print(f"  FAILED: {e}")
        return False


def test_vision(client: OllamaClient, model: str) -> bool:
    """Test vision capabilities with a screenshot."""
    print(f"\nTesting vision with {model}...")
    try:
        # Take a screenshot
        print("  Taking screenshot...")
        screenshot_bytes = screenshot_monitor(0)
        print(f"  Screenshot size: {len(screenshot_bytes)} bytes")

        # Send to vision model
        print("  Sending to vision model...")
        response = client.chat(
            model,
            [{"role": "user", "content": "Briefly describe what you see on this screen in 2-3 sentences."}],
            images=[screenshot_bytes]
        )
        content = response['message']['content']
        print(f"  Vision response: {content}")
        return True
    except Exception as e:
        print(f"  FAILED: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Test Qwen 3 VL via Ollama")
    parser.add_argument("--host", default="localhost", help="Ollama host (default: localhost)")
    parser.add_argument("--port", type=int, default=11434, help="Ollama port (default: 11434)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Model name (default: {DEFAULT_MODEL})")
    args = parser.parse_args()

    model = args.model
    url = f"http://{args.host}:{args.port}"
    print(f"Testing Qwen 3 VL at {url}")
    print(f"Model: {model}")
    print("=" * 50)

    client = OllamaClient(host=url)

    results = {
        "Connection": test_connection(client),
        "List Models": test_list_models(client),
        "Text Generation": test_text_generation(client, model),
        "Vision": test_vision(client, model),
    }

    print("\n" + "=" * 50)
    print("Results:")
    for test, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"  {test}: {status}")

    all_passed = all(results.values())
    print(f"\nOverall: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit(main())
