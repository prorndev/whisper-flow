import concurrent.futures
from whisper_flow.config.settings import settings
from whisper_flow.core.event_bus import event_bus
from whisper_flow.core.events import AppShutdown
from whisper_flow.services.input.hotkey_manager import HotkeyManager
from whisper_flow.services.audio.recorder import AudioRecorder
from whisper_flow.services.transcription.transcriber import Transcriber
from whisper_flow.services.output.output_service import OutputService
from whisper_flow.services.integration.spotify_service import SpotifyService

class Application:
    def __init__(self):
        print("Initializing WhisperFlow...")
        self.settings = settings
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
        
        # Initialize all services
        self.hotkey_manager = HotkeyManager()
        self.audio_recorder = AudioRecorder()
        self.transcriber = Transcriber(self.executor)
        self.output_service = OutputService()
        self.spotify_service = SpotifyService()

    def run(self):
        print("WhisperFlow is running.")
        print(f"Using device: {self.settings.performance.device}")
        
        self.hotkey_manager.start()
        
        # The listener's join() method will block the main thread,
        # keeping the application alive.
        try:
            self.hotkey_manager.join()
        except KeyboardInterrupt:
            self.shutdown()

    def shutdown(self):
        print("Shutting down WhisperFlow...")
        event_bus.publish(AppShutdown())
        self.hotkey_manager.stop()
        self.executor.shutdown(wait=True)
        print("Shutdown complete.")
        # Graceful shutdown logic will be here
        # e.g., self.hotkey_manager.stop() 