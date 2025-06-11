# WhisperFlow - Style Guide

## Code Style Standards

### Python Code Style
- **Formatting**: Follow PEP 8 guidelines
- **Line Length**: Maximum 88 characters (Black formatter compatible)
- **Imports**: Group standard library, third-party, and local imports
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Documentation**: Docstrings for public functions and classes

### Project Structure
- **Configuration**: Keep constants at module top
- **Error Handling**: Explicit exception handling with logging
- **Resource Management**: Use context managers for file/stream operations
- **Threading**: Clear thread safety patterns and documentation

### WhisperFlow Specific Patterns

### Global State Management
- Minimize global variables, use clear naming when necessary
- Thread-safe operations for recording state
- Explicit cleanup and resource management

### Audio Processing
- Consistent sample rate handling (16kHz standard)
- Memory-efficient streaming for large audio buffers
- Proper file cleanup and garbage collection

### System Integration
- Platform detection with graceful fallbacks
- Service availability checks (Spotify, display server)
- Permission and capability validation

### Performance Guidelines
- Lazy loading for ML models and heavy resources
- GPU utilization optimization with CPU fallbacks
- Memory management for audio processing

### Documentation Standards
- Inline comments for complex algorithms
- Function docstrings with parameter and return descriptions
- README updates for new features or configuration changes
- Memory Bank documentation for architectural decisions

### Testing Approach
- Unit tests for core transcription logic
- Integration tests for system interactions
- Manual testing for hotkey and audio workflows
- Performance benchmarking for transcription speed