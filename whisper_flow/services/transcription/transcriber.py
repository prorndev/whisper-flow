import numpy as np
import os
from scipy.io.wavfile import write
import gc

from whisper_flow.config.settings import settings
from whisper_flow.core.event_bus import event_bus
from whisper_flow.core.events import AudioChunkReady, TranscriptionReady, RecordingStartRequested
from whisper_flow.services.transcription.model_manager import model_manager
from whisper_flow.services.transcription.language import get_keyboard_layout

class Transcriber:
    """Handles the audio transcription process."""
    def __init__(self, executor):
        self.executor = executor
        self._input_language = 'ru'  # Default
        self._setup_subscriptions()

    def _setup_subscriptions(self):
        """Subscribes to relevant events."""
        event_bus.subscribe(AudioChunkReady, self.on_audio_chunk_ready)
        event_bus.subscribe(RecordingStartRequested, self.on_recording_start)

    def on_recording_start(self, event: RecordingStartRequested):
        """Captures the input language when recording starts."""
        self._input_language = event.language

    def on_audio_chunk_ready(self, event: AudioChunkReady):
        """Submits the audio data for transcription in a background thread."""
        future = self.executor.submit(self._transcribe_task, event.audio_data)
        future.add_done_callback(self._on_transcription_complete)

    def _transcribe_task(self, audio_data: np.ndarray) -> str:
        """The actual transcription logic that runs in a worker thread."""
        print("\n--- Audio Processing ---")
        try:
            if audio_data.size == 0:
                print("No audio data to process.")
                return ""

            target_lang = get_keyboard_layout()
            task = "transcribe"
            if self._input_language != target_lang:
                task = "translate"

            print(f"Task: {task.capitalize():<10} | Input: {self._input_language} | Output: {target_lang}")
            
            # Write audio to a temporary file for stable processing
            write(settings.audio.temp_filename, settings.audio.samplerate, audio_data)

            model = model_manager.get_model()
            segments, info = model.transcribe(
                settings.audio.temp_filename,
                beam_size=settings.performance.beam_size,
                task=task,
                language=self._input_language if task == "transcribe" else None,
                initial_prompt=settings.transcription.prompts.get(target_lang)
            )
            
            print(f"Model detected source as '{info.language}' with probability {info.language_probability:.4f}")
            transcribed_text = "".join(segment.text for segment in segments)
            return transcribed_text.strip()
        
        finally:
            # Clean up the audio file and run garbage collection
            if os.path.exists(settings.audio.temp_filename):
                os.remove(settings.audio.temp_filename)
            gc.collect()
            print("--- Processing Finished ---")

    def _on_transcription_complete(self, future):
        """Callback that fires when transcription is done."""
        try:
            text = future.result()
            if text:
                print(f"Final Output: {text}")
                event_bus.publish(TranscriptionReady(text=text))
            else:
                print("Transcription produced no text.")
        except Exception as e:
            print(f"An error occurred during transcription task: {e}") 