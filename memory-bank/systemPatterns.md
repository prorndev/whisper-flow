# WhisperFlow - System Patterns

## Design Patterns

### Observer Pattern
- **Context**: Hotkey event handling
- **Implementation**: pynput keyboard listener with callback system
- **Benefits**: Decoupled event detection from processing logic

### State Machine Pattern
- **Context**: Recording lifecycle management
- **States**: idle -> recording -> processing -> idle
- **Guards**: Thread safety with global state coordination

### Strategy Pattern
- **Context**: Platform-specific input simulation
- **Strategies**: X11 (xdotool) vs Wayland (ydotool)
- **Selection**: Runtime platform detection

### Template Method Pattern
- **Context**: Audio processing workflow
- **Steps**: record -> save -> transcribe -> output -> cleanup
- **Variations**: Language-specific processing paths

## Architectural Patterns

### Layered Architecture
1. **UI Layer**: Hotkey detection and system interaction
2. **Service Layer**: Audio recording and transcription coordination
3. **Integration Layer**: Spotify, clipboard, input simulation
4. **Data Layer**: Temporary file management and model loading

### Event-Driven Architecture
- **Events**: Hotkey press/release, audio chunks, transcription completion
- **Handlers**: Asynchronous processing with thread coordination
- **Benefits**: Responsive UI with non-blocking operations

## Error Handling Patterns

### Graceful Degradation
- **GPU Unavailable**: Automatic CPU fallback
- **Spotify Unreachable**: Continue without media control
- **Platform Detection Failure**: Default to safe assumptions

### Resource Cleanup
- **RAII Pattern**: Context managers for audio streams
- **Explicit Cleanup**: Temporary file removal and memory management
- **Exception Safety**: Finally blocks and atexit handlers

## Performance Patterns

### Lazy Loading
- **AI Models**: Load only when first transcription needed
- **System Services**: Connect to services on demand

### Resource Pooling
- **Audio Buffers**: Reuse allocated memory for recordings
- **Thread Management**: Background processing without blocking