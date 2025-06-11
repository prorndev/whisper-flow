# WhisperFlow - Project Brief

## Project Overview
WhisperFlow is a voice transcription system utility for Ubuntu that enables rapid voice-to-text conversion with automatic clipboard integration and application pasting.

## Core Functionality
- Hotkey-driven voice recording: Ctrl + Super (Russian), Shift + Ctrl + Super (English)
- Local Whisper transcription: Uses faster-whisper for privacy and offline operation
- Spotify integration: Auto-pause/resume during recording
- Multi-language support: Russian/English with translation capabilities
- Cross-platform compatibility: Wayland & X11 display server support
- Automatic text insertion: Clipboard copy + paste to active window

## Technical Architecture
- Language: Python 3
- Core Dependencies: faster-whisper, pynput, sounddevice, pydbus
- Audio Processing: 16kHz sampling, WAV format
- GPU Acceleration: CUDA support with fallback to CPU
- System Integration: xdotool/ydotool for input simulation

## Current State
- Fully functional voice transcription utility
- Complete hotkey management system
- Robust Spotify integration
- Cross-language detection and processing
- Production-ready with proper error handling

## Development Focus
- Performance optimization
- User experience enhancements
- Feature expansion
- System integration improvements

## Target Users
- Ubuntu users requiring fast voice-to-text workflow
- Multilingual users (Russian/English)
- Privacy-conscious users preferring local processing
- Productivity-focused professionals