# WhisperFlow

WhisperFlow is a system utility for Ubuntu that allows you to quickly transcribe your voice into text and paste it into the active application.

When you press and hold a hotkey (`Ctrl + Super` for Russian or `Shift + Ctrl + Super` for English), it automatically pauses Spotify (if it's playing), records your voice, and upon release, transcribes the audio using a local Whisper model. The resulting text is then copied to your clipboard and pasted into the currently focused window.

## Features

- **Hotkey Activated**: Press and hold `Ctrl + Super` for Russian or `Shift + Ctrl + Super` for English.
- **Spotify Integration**: Automatically pauses and resumes Spotify during recording.
- **Local Transcription**: Uses `faster-whisper` to perform transcription locally, ensuring privacy and offline functionality.
- **Clipboard & Paste**: Copies text to the clipboard and pastes it into the active input field.
- **Wayland & X11 Support**: Works on both major Linux display servers.
- **Configurable**: Customize settings via the `config.yaml` file.

## Architecture

WhisperFlow uses a modular, event-driven architecture:

- **Core**: Centralized application management with an event bus for communication
- **Services**: Independent modules for audio, transcription, input/output, and integrations
- **Configuration**: YAML-based settings with validation via Pydantic

## Installation

Follow these steps to set up and run WhisperFlow on your Ubuntu system.

### 1. Install System Dependencies

First, you need to install the required system-level packages. These include tools for clipboard management, audio handling, and simulating keyboard input.

Open a terminal and run the following command:

```bash
sudo apt-get update && sudo apt-get install -y python3-pip xdotool ydotool portaudio19-dev xclip
```

### 2. Install Python Libraries

Next, install the necessary Python libraries using `pip` and the provided `requirements.txt` file.

Navigate to the project directory and run:

```bash
pip install -r requirements.txt
```

## Configuration

WhisperFlow uses a configuration file (`config.yaml`) where you can customize various settings:

- **Hotkeys**: Change the key combinations for different languages
- **Audio Settings**: Adjust sample rate and temporary file location
- **Performance**: Configure model size, device (CPU/GPU), and compute type
- **Transcription**: Customize language-specific prompts
- **Output**: Adjust paste tool timeout

Example configuration:

```yaml
# WhisperFlow sample configuration
hotkeys:
  ru:
    - "Key.ctrl"
    - "Key.cmd"
  en:
    - "Key.shift"
    - "Key.ctrl"
    - "Key.cmd"

performance:
  device: "auto"  # "cuda" or "cpu"
  model_size: "large-v3"
```

## How to Run

To ensure that the application can find the necessary NVIDIA libraries for GPU acceleration, **always use the `run.sh` script to launch WhisperFlow.**

Open a terminal in the project directory and run:

```bash
./run.sh
```

## Usage

1. After launching WhisperFlow, its icon will appear in your system tray.
2. Press and hold the hotkey for your preferred language (default: `Ctrl + Super` for Russian or `Shift + Ctrl + Super` for English).
3. While holding the hotkey, speak your message.
4. Release the hotkey when finished. The application will process your speech and paste the text.

## Troubleshooting

- **Audio Issues**: Check your microphone is working correctly and that system audio permissions are granted
- **Clipboard Issues**: Try running the application with elevated privileges if clipboard operations fail
- **GPU Acceleration**: Ensure you have the proper NVIDIA drivers and CUDA installed if using GPU acceleration

## License

This project is licensed under the MIT License - see the LICENSE file for details.
