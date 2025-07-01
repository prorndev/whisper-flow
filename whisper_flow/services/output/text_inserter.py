from abc import ABC, abstractmethod
import subprocess
import os

from whisper_flow.config.settings import settings

class TextInsertionStrategy(ABC):
    """Abstract base class for text insertion strategies."""
    @abstractmethod
    def insert(self, text: str) -> bool:
        pass

class X11TextInserter(TextInsertionStrategy):
    """Uses xdotool to type text directly in X11."""
    
    def insert(self, text: str) -> bool:
        try:
            # Find the active window first
            window_id_proc = subprocess.run(
                ["xdotool", "getactivewindow"],
                capture_output=True, text=True, check=True,
                timeout=settings.output.paste_tool_timeout
            )
            window_id = window_id_proc.stdout.strip()

            if window_id:
                print(f"Found active window {window_id}. Typing text directly.")
                # Type text directly using xdotool
                subprocess.run(
                    ["xdotool", "type", text],
                    check=True,
                    timeout=settings.output.paste_tool_timeout
                )
                print("Text typed successfully.")
                return True
            else:
                print("No active window found to type into.")
                return False
        except FileNotFoundError:
            print("Text insertion failed: 'xdotool' not found.")
            return False
        except subprocess.TimeoutExpired:
            print("Text insertion timed out (xdotool may be unresponsive).")
            return False
        except Exception as e:
            print(f"An error occurred during X11 text insertion: {e}")
            return False

class WaylandTextInserter(TextInsertionStrategy):
    """Uses ydotool to type text in Wayland."""
    def insert(self, text: str) -> bool:
        try:
            subprocess.run(
                ["ydotool", "type", text],
                check=True,
                timeout=settings.output.paste_tool_timeout
            )
            print("Text typed using ydotool.")
            return True
        except FileNotFoundError:
            print("Text insertion failed: 'ydotool' not found.")
            return False
        except subprocess.TimeoutExpired:
            print("Text insertion timed out (ydotool may be unresponsive).")
            return False
        except Exception as e:
            print(f"An error occurred during Wayland text insertion: {e}")
            return False

def get_text_inserter() -> TextInsertionStrategy:
    """Factory function to get the appropriate text inserter for the environment."""
    session_type = os.environ.get("XDG_SESSION_TYPE", "x11").lower()
    if "wayland" in session_type:
        print("Wayland session detected. Using ydotool for text insertion.")
        return WaylandTextInserter()
    print("X11 session detected. Using xdotool for text insertion.")
    return X11TextInserter() 