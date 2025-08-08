"""Keyboard operations for ScreenClicker."""

import time
import uinput


def _create_keyboard_device():
    """Create virtual keyboard device."""
    try:
        return uinput.Device([
            uinput.KEY_A, uinput.KEY_B, uinput.KEY_C, uinput.KEY_D, uinput.KEY_E,
            uinput.KEY_F, uinput.KEY_G, uinput.KEY_H, uinput.KEY_I, uinput.KEY_J,
            uinput.KEY_K, uinput.KEY_L, uinput.KEY_M, uinput.KEY_N, uinput.KEY_O,
            uinput.KEY_P, uinput.KEY_Q, uinput.KEY_R, uinput.KEY_S, uinput.KEY_T,
            uinput.KEY_U, uinput.KEY_V, uinput.KEY_W, uinput.KEY_X, uinput.KEY_Y,
            uinput.KEY_Z,
            uinput.KEY_0, uinput.KEY_1, uinput.KEY_2, uinput.KEY_3, uinput.KEY_4,
            uinput.KEY_5, uinput.KEY_6, uinput.KEY_7, uinput.KEY_8, uinput.KEY_9,
            uinput.KEY_SPACE, uinput.KEY_ENTER, uinput.KEY_BACKSPACE,
            uinput.KEY_LEFTSHIFT, uinput.KEY_RIGHTSHIFT,
            uinput.KEY_APOSTROPHE, uinput.KEY_COMMA, uinput.KEY_DOT,
            uinput.KEY_MINUS, uinput.KEY_EQUAL, uinput.KEY_SLASH,
            uinput.KEY_SEMICOLON, uinput.KEY_LEFTBRACE, uinput.KEY_RIGHTBRACE,
        ])
    except PermissionError:
        raise PermissionError("uinput keyboard access denied. Check permissions.")
    except Exception as e:
        raise RuntimeError(f"Failed to create keyboard device: {e}")


def _uinput_type_char(device, char):
    """Type a single character using uinput."""
    char_map = {
        'a': uinput.KEY_A, 'b': uinput.KEY_B, 'c': uinput.KEY_C, 'd': uinput.KEY_D, 'e': uinput.KEY_E,
        'f': uinput.KEY_F, 'g': uinput.KEY_G, 'h': uinput.KEY_H, 'i': uinput.KEY_I, 'j': uinput.KEY_J,
        'k': uinput.KEY_K, 'l': uinput.KEY_L, 'm': uinput.KEY_M, 'n': uinput.KEY_N, 'o': uinput.KEY_O,
        'p': uinput.KEY_P, 'q': uinput.KEY_Q, 'r': uinput.KEY_R, 's': uinput.KEY_S, 't': uinput.KEY_T,
        'u': uinput.KEY_U, 'v': uinput.KEY_V, 'w': uinput.KEY_W, 'x': uinput.KEY_X, 'y': uinput.KEY_Y,
        'z': uinput.KEY_Z,
        '0': uinput.KEY_0, '1': uinput.KEY_1, '2': uinput.KEY_2, '3': uinput.KEY_3, '4': uinput.KEY_4,
        '5': uinput.KEY_5, '6': uinput.KEY_6, '7': uinput.KEY_7, '8': uinput.KEY_8, '9': uinput.KEY_9,
        ' ': uinput.KEY_SPACE, "'": uinput.KEY_APOSTROPHE, ',': uinput.KEY_COMMA,
        '.': uinput.KEY_DOT, '-': uinput.KEY_MINUS, '=': uinput.KEY_EQUAL, '/': uinput.KEY_SLASH,
        ';': uinput.KEY_SEMICOLON, '[': uinput.KEY_LEFTBRACE, ']': uinput.KEY_RIGHTBRACE,
    }
    
    # Handle uppercase letters (need shift)
    if char.isupper():
        char_lower = char.lower()
        if char_lower in char_map:
            device.emit(uinput.KEY_LEFTSHIFT, 1)
            device.emit(char_map[char_lower], 1)
            device.syn()
            time.sleep(0.01)
            device.emit(char_map[char_lower], 0)
            device.emit(uinput.KEY_LEFTSHIFT, 0)
            device.syn()
            return True
    
    # Handle regular characters
    if char in char_map:
        device.emit(char_map[char], 1)
        device.syn()
        time.sleep(0.01)
        device.emit(char_map[char], 0)
        device.syn()
        return True
    
    # Skip unsupported characters
    return False


def text(string):
    """Type text string using uinput."""
    device = _create_keyboard_device()
    try:
        for char in string:
            if not _uinput_type_char(device, char):
                # Skip unsupported characters silently
                continue
            time.sleep(0.02)  # Small delay between characters
        return True
    except Exception as e:
        return False
    finally:
        device.destroy()