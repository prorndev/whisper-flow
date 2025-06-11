from whisper_flow.services.integration.spotify import SpotifyControl
from whisper_flow.core.event_bus import event_bus
from whisper_flow.core.events import RecordingStartRequested, RecordingStopRequested

class SpotifyService:
    """Manages Spotify integration."""
    def __init__(self):
        self._spotify_control = SpotifyControl()
        self._was_playing = False
        self._setup_subscriptions()

    def _setup_subscriptions(self):
        event_bus.subscribe(RecordingStartRequested, self._on_recording_start)
        event_bus.subscribe(RecordingStopRequested, self._on_recording_stop)

    def _on_recording_start(self, event: RecordingStartRequested):
        """Pauses Spotify if it was playing."""
        self._was_playing = self._spotify_control.is_playing()
        if self._was_playing:
            self._spotify_control.pause()

    def _on_recording_stop(self, event: RecordingStopRequested):
        """Resumes Spotify if it was previously playing."""
        if self._was_playing:
            self._spotify_control.play()
        self._was_playing = False 