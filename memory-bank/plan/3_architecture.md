# WhisperFlow Refactoring - Architecture

## Proposed Class Structure

- **config/** - Configuration system
  - ConfigManager class for settings management
  - YAML-based configuration file
  - Default configuration values

- **core/** - Application core
  - Application class for lifecycle management
  - Constants and system-wide definitions

- **services/** - Functional services
  - Audio recording and processing
  - Transcription and language handling
  - Output and clipboard management
  - Input and hotkey management
  - Integration services (Spotify, platform)

- **utils/** - Utility functions
  - Logging utilities
  - Resource management

## Design Patterns to Implement

1. **Singleton Pattern**
   - Configuration Manager
   - Model Manager
   - Application instance

2. **Factory Pattern**
   - Platform-specific text inserter creation
   - Audio processor creation

3. **Observer Pattern**
   - Hotkey event handling
   - Recording state notifications

4. **Strategy Pattern**
   - Text insertion strategies (X11 vs Wayland)
   - Transcription strategies (based on language)

5. **Command Pattern**
   - Audio recording operations
   - Transcription operations
   - Output operations

6. **Facade Pattern**
   - Simplified interfaces for complex subsystems
   - Clean API between components