from dataclasses import dataclass
import numpy as np
from whisper_flow.core.event_bus import Event

# --- Application Events ---
@dataclass
class AppStart(Event):
    pass

@dataclass
class AppShutdown(Event):
    pass

# --- Hotkey Events ---
@dataclass
class HotkeyEvent(Event):
    language: str

@dataclass
class RecordingStartRequested(HotkeyEvent):
    pass

@dataclass
class RecordingStopRequested(HotkeyEvent):
    pass

# --- Audio Events ---
@dataclass
class AudioChunkReady(Event):
    audio_data: np.ndarray

# --- Transcription Events ---
@dataclass
class TranscriptionReady(Event):
    text: str

# --- Spotify Events ---
@dataclass
class SpotifyStatus(Event):
    is_playing: bool 