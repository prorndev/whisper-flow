from pynput import keyboard
from typing import Set
from whisper_flow.config.settings import settings
from whisper_flow.core.event_bus import event_bus
from whisper_flow.core.events import RecordingStartRequested, RecordingStopRequested

class HotkeyManager:
    """Listens for global hotkeys and publishes events."""
    def __init__(self):
        self._pressed_keys: Set[keyboard.Key] = set()
        self._is_recording = False
        self._listener = keyboard.Listener(on_press=self._on_press, on_release=self._on_release)
        
        # Convert string hotkeys from config to pynput Key objects
        self._hotkey_ru = self._parse_hotkey(settings.hotkeys.ru)
        self._hotkey_en = self._parse_hotkey(settings.hotkeys.en)
        self._all_hotkey_keys = self._hotkey_ru | self._hotkey_en

    def _parse_hotkey(self, key_strings: list[str]) -> Set[keyboard.Key]:
        """Converts a list of key strings from config into a set of pynput Key objects."""
        keys = set()
        for key_str in key_strings:
            try:
                # e.g., "Key.ctrl" -> keyboard.Key.ctrl
                keys.add(eval(f"keyboard.{key_str}"))
            except (AttributeError, SyntaxError):
                # For regular character keys like 'v'
                keys.add(keyboard.KeyCode.from_char(key_str))
        return keys

    def _on_press(self, key):
        """Handles key press events."""
        self._pressed_keys.add(key)
        
        if not self._is_recording:
            lang = None
            if self._hotkey_en.issubset(self._pressed_keys):
                lang = 'en'
            elif self._hotkey_ru.issubset(self._pressed_keys):
                lang = 'ru'
            
            if lang:
                self._is_recording = True
                event_bus.publish(RecordingStartRequested(language=lang))

    def _on_release(self, key):
        """Handles key release events."""
        if self._is_recording and key in self._all_hotkey_keys:
            self._is_recording = False
            # The language doesn't matter on stop, but we pass it for consistency
            event_bus.publish(RecordingStopRequested(language='any'))

        if key in self._pressed_keys:
            self._pressed_keys.remove(key)

    def start(self):
        """Starts the hotkey listener."""
        print("Hotkey listener started. Ready for input.")
        self._listener.start()

    def stop(self):
        """Stops the hotkey listener."""
        print("Stopping hotkey listener...")
        self._listener.stop()
        
    def join(self):
        """Waits for the listener thread to complete."""
        self._listener.join() 