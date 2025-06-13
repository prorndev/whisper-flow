#!/bin/bash

# Определяем DISPLAY, если не задан
export DISPLAY=${DISPLAY:-:0}

# Определяем XAUTHORITY, если не задан
if [ -z "$XAUTHORITY" ]; then
    if [ -f "$HOME/.Xauthority" ]; then
        export XAUTHORITY="$HOME/.Xauthority"
    else
        XAUTH=$(ls /run/user/$(id -u)/*/Xauthority 2>/dev/null | head -n1)
        if [ -n "$XAUTH" ]; then
            export XAUTHORITY="$XAUTH"
        fi
    fi
fi

# Find the user's site-packages directory for Python 3
SITE_PACKAGES=$(python3 -c "import site; print(site.getusersitepackages())")

# Construct the path to the NVIDIA cuDNN libraries
NVIDIA_LIB_DIR="$SITE_PACKAGES/nvidia/cudnn/lib"

# Check if the directory exists and set the library path
if [ -d "$NVIDIA_LIB_DIR" ]; then
    echo "Found cuDNN libraries at: $NVIDIA_LIB_DIR"
    # Prepend the cuDNN path to LD_LIBRARY_PATH to ensure it's found first.
    export LD_LIBRARY_PATH="$NVIDIA_LIB_DIR:$LD_LIBRARY_PATH"
    echo "LD_LIBRARY_PATH is now set for this session."
else
    echo "Warning: cuDNN library directory not found at $NVIDIA_LIB_DIR"
    echo "The script will continue, but may fail if CUDA is used."
fi

# Run the main application
echo "Starting WhisperFlow..."
python3 -m whisper_flow.main 