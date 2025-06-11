from faster_whisper import WhisperModel
from whisper_flow.config.settings import settings

class ModelManager:
    """Loads and manages the Whisper model."""
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelManager, cls).__new__(cls)
        return cls._instance

    def get_model(self) -> WhisperModel:
        """Lazily loads the model on first request and returns it."""
        if self._model is None:
            print("Loading Whisper model...")
            try:
                self._model = WhisperModel(
                    settings.performance.model_size,
                    device=settings.performance.device,
                    compute_type=settings.performance.compute_type
                )
                print("Model loaded successfully.")
            except Exception as e:
                print(f"Error loading Whisper model: {e}")
                # Handle model loading failure, maybe by exiting or using a dummy model
                raise
        return self._model

# Singleton instance
model_manager = ModelManager() 