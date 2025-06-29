from faster_whisper import WhisperModel
import gc
import torch
from whisper_flow.config.settings import settings

class ModelManager:
    """Loads and manages the Whisper model."""
    _instance = None
    _model = None
    _usage_count = 0

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelManager, cls).__new__(cls)
        return cls._instance

    def get_model(self) -> WhisperModel:
        """Lazily loads the model on first request and returns it."""
        if self._model is None:
            self._load_model()
        
        self._usage_count += 1
        
        # Периодическая перезагрузка модели для предотвращения деградации
        if self._usage_count >= settings.performance.model_reload_after_uses:
            print(f"🔄 Reloading model after {self._usage_count} uses to prevent quality degradation...")
            self._reload_model()
        
        # После _load_model() или _reload_model() _model гарантированно не None
        assert self._model is not None, "Model should be loaded at this point"
        return self._model

    def _load_model(self):
        """Loads the Whisper model."""
        print("Loading Whisper model...")
        try:
            self._model = WhisperModel(
                settings.performance.model_size,
                device=settings.performance.device,
                compute_type=settings.performance.compute_type
            )
            print("Model loaded successfully.")
            self._usage_count = 0
        except Exception as e:
            print(f"Error loading Whisper model: {e}")
            raise

    def _reload_model(self):
        """Reloads the model to clear accumulated state."""
        self._cleanup_model()
        self._load_model()

    def _cleanup_model(self):
        """Cleans up the current model and frees GPU memory."""
        if self._model is not None:
            del self._model
            self._model = None
        
        # Принудительная очистка GPU памяти
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
        
        # Принудительная сборка мусора
        gc.collect()
        print("Model cleanup completed.")

    def force_reload(self):
        """Manually force model reload."""
        print("Force reloading model...")
        self._reload_model()

# Singleton instance
model_manager = ModelManager() 