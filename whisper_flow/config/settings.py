import yaml
from pydantic import BaseModel, Field
import torch
from typing import List, Dict

# --- Pydantic Models for Configuration ---

class AppSettings(BaseModel):
    lock_file: str = "/tmp/whisper_flow.lock"

class AudioSettings(BaseModel):
    samplerate: int = 16000
    temp_filename: str = "/tmp/recorded_audio.wav"

class HotkeySettings(BaseModel):
    ru: List[str] = Field(default_factory=lambda: ["Key.ctrl", "Key.cmd"])
    en: List[str] = Field(default_factory=lambda: ["Key.shift", "Key.ctrl", "Key.cmd"])

class PerformanceSettings(BaseModel):
    device: str = "auto"
    compute_type: str = "auto"
    model_size: str = "large-v3"
    beam_size: int = 1

    def __init__(self, **data):
        super().__init__(**data)
        if self.device == "auto":
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        if self.compute_type == "auto":
            self.compute_type = "float16" if self.device == "cuda" else "int8"

class TranscriptionSettings(BaseModel):
    prompts: Dict[str, str]

class OutputSettings(BaseModel):
    paste_tool_timeout: int = 2

class Settings(BaseModel):
    app: AppSettings
    audio: AudioSettings
    hotkeys: HotkeySettings
    performance: PerformanceSettings
    transcription: TranscriptionSettings
    output: OutputSettings

# --- Configuration Loading ---

def load_settings(path: str = "config.yaml") -> Settings:
    """Loads settings from a YAML file and validates them using Pydantic."""
    try:
        with open(path, 'r') as f:
            config_data = yaml.safe_load(f)
        return Settings(**config_data)
    except FileNotFoundError:
        print(f"Warning: Configuration file not found at '{path}'. Using default settings.")
        return Settings(
            app=AppSettings(),
            audio=AudioSettings(),
            hotkeys=HotkeySettings(),
            performance=PerformanceSettings(),
            transcription=TranscriptionSettings(prompts={}),
            output=OutputSettings()
        )
    except Exception as e:
        print(f"Error loading or validating configuration: {e}")
        print("Falling back to default settings.")
        # Create a default settings object in case of validation error
        return Settings(
            app=AppSettings(),
            audio=AudioSettings(),
            hotkeys=HotkeySettings(),
            performance=PerformanceSettings(),
            transcription=TranscriptionSettings(prompts={}),
            output=OutputSettings()
        )

# --- Singleton Instance ---
# Load settings once and provide a single instance for the application.
settings = load_settings()

if __name__ == '__main__':
    # For testing purposes
    print("Configuration loaded successfully!")
    print("\n--- Performance Settings ---")
    print(f"  Device: {settings.performance.device}")
    print(f"  Compute Type: {settings.performance.compute_type}")
    print("\n--- Hotkey Settings ---")
    print(f"  Russian Hotkey: {' + '.join(settings.hotkeys.ru)}")
    print(f"  English Hotkey: {' + '.join(settings.hotkeys.en)}")
    print("\n--- Transcription Prompts ---")
    print(f"  RU Prompt available: {'yes' if 'ru' in settings.transcription.prompts else 'no'}")
    print(f"  EN Prompt available: {'yes' if 'en' in settings.transcription.prompts else 'no'}") 