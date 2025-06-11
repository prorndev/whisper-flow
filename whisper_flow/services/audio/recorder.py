import sounddevice as sd
import numpy as np
import threading

from whisper_flow.config.settings import settings
from whisper_flow.core.event_bus import event_bus
from whisper_flow.core.events import (
    RecordingStartRequested, 
    RecordingStopRequested, 
    AudioChunkReady,
    AppShutdown
)

class AudioRecorder:
    """Handles audio recording."""
    def __init__(self):
        self._is_recording = False
        self._recording_thread: threading.Thread = None
        self._recorded_audio: list[np.ndarray] = []
        self._input_language: str = None
        self._setup_subscriptions()

    def _setup_subscriptions(self):
        """Subscribes to relevant events."""
        event_bus.subscribe(RecordingStartRequested, self._handle_start_recording)
        event_bus.subscribe(RecordingStopRequested, self._handle_stop_recording)
        event_bus.subscribe(AppShutdown, self.stop)

    def _handle_start_recording(self, event: RecordingStartRequested):
        """Event handler to start a new recording."""
        if self._is_recording:
            return
        
        print(f"Starting recording for language: {event.language}")
        self._is_recording = True
        self._input_language = event.language
        self._recorded_audio = []
        
        self._recording_thread = threading.Thread(target=self._record_audio_loop)
        self._recording_thread.start()

    def _handle_stop_recording(self, event: RecordingStopRequested):
        """Event handler to stop the current recording."""
        if not self._is_recording:
            return
        
        print("Stopping recording...")
        self._is_recording = False # Signal the thread to stop
        self._recording_thread.join() # Wait for the thread to finish
        print("Recording thread finished.")

        if self._recorded_audio:
            audio_data = np.concatenate(self._recorded_audio, axis=0)
            event_bus.publish(AudioChunkReady(audio_data=audio_data))
        
        self._recorded_audio = []

    def _record_audio_loop(self):
        """The main loop for the recording thread."""
        def callback(indata, frames, time, status):
            if status:
                print(f"Audio callback status: {status}")
            if self._is_recording:
                self._recorded_audio.append(indata.copy())

        try:
            with sd.InputStream(
                samplerate=settings.audio.samplerate, 
                channels=1, 
                callback=callback
            ):
                while self._is_recording:
                    sd.sleep(100)
        except Exception as e:
            print(f"Error during audio recording: {e}")

    def stop(self, event: AppShutdown = None):
        """Stops the recording service."""
        if self._is_recording:
            self._is_recording = False
            if self._recording_thread and self._recording_thread.is_alive():
                self._recording_thread.join()
        print("Audio recorder shut down.") 