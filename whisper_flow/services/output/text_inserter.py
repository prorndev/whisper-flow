from abc import ABC, abstractmethod
import subprocess
import os
from pynput.keyboard import Controller, Key

from whisper_flow.config.settings import settings

class TextInsertionStrategy(ABC):
    """Abstract base class for text insertion strategies."""
    @abstractmethod
    def insert(self, text: str):
        pass

class X11TextInserter(TextInsertionStrategy):
    """Uses xdotool to paste text in X11."""
    def __init__(self):
        self._keyboard = Controller()

    def insert(self, text: str):
        try:
            # Find the active window
            window_id_proc = subprocess.run(
                ["xdotool", "getactivewindow"],
                capture_output=True, text=True, check=True,
                timeout=settings.output.paste_tool_timeout
            )
            window_id = window_id_proc.stdout.strip()

            if window_id:
                print(f"Found active window {window_id}. Simulating paste (Ctrl+V).")
                self._keyboard.press(Key.ctrl)
                self._keyboard.press('v')
                self._keyboard.release('v')
                self._keyboard.release(Key.ctrl)
                print("Paste command sent.")
            else:
                print("No active window found to paste into. Text remains in clipboard.")
        except FileNotFoundError:
            print("Paste command failed: 'xdotool' not found.")
        except subprocess.TimeoutExpired:
            print("Pasting timed out (window may be unresponsive).")
        except Exception as e:
            print(f"An error occurred during X11 pasting: {e}")

class WaylandTextInserter(TextInsertionStrategy):
    """Uses ydotool to type text in Wayland."""
    def insert(self, text: str):
        try:
            subprocess.run(
                ["ydotool", "type", text],
                check=True,
                timeout=settings.output.paste_tool_timeout
            )
            print("Pasted text using ydotool.")
        except FileNotFoundError:
            print("Paste command failed: 'ydotool' not found.")
        except subprocess.TimeoutExpired:
            print("Pasting timed out (ydotool may be unresponsive).")
        except Exception as e:
            print(f"An error occurred during Wayland pasting: {e}")

def get_text_inserter() -> TextInsertionStrategy:
    """Factory function to get the appropriate text inserter for the environment."""
    session_type = os.environ.get("XDG_SESSION_TYPE", "x11").lower()
    if "wayland" in session_type:
        print("Wayland session detected. Using ydotool for text insertion.")
        return WaylandTextInserter()
    print("X11 session detected. Using xdotool for text insertion.")
    return X11TextInserter() 