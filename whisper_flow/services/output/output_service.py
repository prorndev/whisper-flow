from whisper_flow.core.event_bus import event_bus
from whisper_flow.core.events import TranscriptionReady
from whisper_flow.services.output.clipboard import copy_to_clipboard
from whisper_flow.services.output.text_inserter import get_text_inserter

class OutputService:
    """Handles the final output of the transcribed text."""
    def __init__(self):
        self._text_inserter = get_text_inserter()
        self._setup_subscriptions()

    def _setup_subscriptions(self):
        """Subscribes to relevant events."""
        event_bus.subscribe(TranscriptionReady, self.on_transcription_ready)

    def on_transcription_ready(self, event: TranscriptionReady):
        """Handles the transcribed text by pasting it or copying to clipboard as fallback."""
        if not event.text:
            return
        
        # Step 1: Try to insert text into input field first
        success = self._text_inserter.insert(event.text)
        
        # Step 2: If insertion failed, copy to clipboard as fallback
        if not success:
            print("Text insertion failed, copying to clipboard as fallback.")
            copy_to_clipboard(event.text) 