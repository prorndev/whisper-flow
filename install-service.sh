#!/bin/bash

set -e

SERVICE_NAME="wisperflow.service"
PROJECT_DIR="$(pwd)"
USER_SYSTEMD_DIR="$HOME/.config/systemd/user"
SERVICE_PATH="$USER_SYSTEMD_DIR/$SERVICE_NAME"

echo "🔧 Installing WhisperFlow as a user service..."

# Проверка наличия systemd --user
if ! systemctl --user > /dev/null 2>&1; then
  echo "❌ systemd --user не доступен. Убедитесь, что у вас systemd и графическая сессия активна."
  exit 1
fi

# Создаём директорию для systemd, если нужно
mkdir -p "$USER_SYSTEMD_DIR"

# Создаём service-файл
echo "📄 Creating systemd unit file at: $SERVICE_PATH"

cat > "$SERVICE_PATH" <<EOF
[Unit]
Description=WhisperFlow Voice Transcription Service

[Service]
Type=simple
WorkingDirectory=$PROJECT_DIR
ExecStartPre=/bin/rm -f /tmp/whisper_flow.lock
ExecStart=$PROJECT_DIR/run.sh
ExecStopPost=/bin/rm -f /tmp/whisper_flow.lock
Restart=on-failure

[Install]
WantedBy=default.target
EOF

# Перезагружаем systemd и включаем сервис
echo "🔄 Reloading user systemd daemon..."
systemctl --user daemon-reexec
systemctl --user daemon-reload

echo "✅ Enabling and starting service..."
systemctl --user enable --now "$SERVICE_NAME"

echo "🎉 Installed successfully!"
echo "Check status with: systemctl --user status $SERVICE_NAME"
