import pydbus
from gi.repository import GLib

class SpotifyControl:
    """A service to control Spotify via DBus."""
    def __init__(self):
        self._player = None
        self._connect()

    def _connect(self):
        """Attempts to connect to the Spotify DBus player."""
        try:
            bus = pydbus.SessionBus()
            self._player = bus.get("org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2")
        except GLib.Error as e:
            print(f"Info: Could not connect to Spotify DBus: {e}. Is Spotify running?")
            self._player = None

    def _get_playback_status(self) -> str:
        """Gets the current playback status from Spotify."""
        if not self._player:
            self._connect() # Try to reconnect if player is not valid
        
        if self._player:
            try:
                return self._player.PlaybackStatus
            except GLib.Error as e:
                print(f"Error getting Spotify status: {e}")
                self._player = None # Invalidate on error
        
        return "Stopped" # Default status if connection fails

    def is_playing(self) -> bool:
        """Checks if Spotify is currently playing."""
        return self._get_playback_status() == 'Playing'

    def pause(self):
        """Pauses Spotify if it is playing."""
        if self._player and self.is_playing():
            try:
                self._player.Pause()
                print("Spotify paused.")
            except GLib.Error as e:
                print(f"Error pausing Spotify: {e}")

    def play(self):
        """Resumes Spotify if it is not playing."""
        if self._player and not self.is_playing():
            try:
                self._player.Play()
                print("Resumed Spotify.")
            except GLib.Error as e:
                print(f"Error resuming Spotify: {e}") 