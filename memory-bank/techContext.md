# WhisperFlow - Technical Context

## Technology Stack
- **Runtime**: Python 3.x
- **Audio Processing**: sounddevice, scipy, numpy
- **AI/ML**: faster-whisper (OpenAI Whisper local implementation)
- **System Integration**: pynput, pydbus
- **Clipboard**: pyperclip
- **Input Simulation**: xdotool (X11), ydotool (Wayland)

## Architecture Overview
- **Event-driven**: Hotkey listener triggers recording workflow
- **Threaded Processing**: Non-blocking audio recording and processing
- **State Management**: Global state coordination for recording lifecycle
- **Resource Management**: GPU/CPU adaptive processing
- **System Abstraction**: Cross-platform display server support

## Performance Characteristics
- **GPU Acceleration**: CUDA support with automatic fallback
- **Memory Efficiency**: Streaming audio processing with cleanup
- **Processing Speed**: float16 (GPU) / int8 (CPU) optimized models
- **Startup Time**: Lazy model loading to minimize cold start

## Platform Integration
- **Display Servers**: X11 and Wayland compatibility
- **Audio System**: PulseAudio/ALSA integration
- **Desktop Environment**: DE-agnostic clipboard and input handling
- **Permission Model**: Wayland requires ydotool service

## Security & Privacy
- **Local Processing**: No network calls for transcription
- **Temporary Files**: Secure cleanup of audio data
- **Process Isolation**: Minimal system privileges required
- **Data Handling**: In-memory processing with file cleanup