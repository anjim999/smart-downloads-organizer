#!/bin/bash

# Real-World Automation Setup: Install as a Systemd Background Service
# This will make the downloads organizer run automatically on startup!

echo "🛠️ Installing Smart Downloads Organizer as a background service..."

# Define paths
SERVICE_NAME="smart-organizer.service"
SERVICE_DIR="$HOME/.config/systemd/user"
SCRIPT_PATH="$(pwd)/organize.py"
PYTHON_PATH="$(which python3)"

# Create the systemd directory if it doesn't exist
mkdir -p "$SERVICE_DIR"

# Generate the service file
cat > "$SERVICE_DIR/$SERVICE_NAME" << EOF
[Unit]
Description=Smart Downloads Organizer Watcher
After=network.target

[Service]
Type=simple
ExecStart=$PYTHON_PATH $SCRIPT_PATH --watch
Restart=on-failure
RestartSec=5
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=smart-organizer

[Install]
WantedBy=default.target
EOF

echo "✅ Created service file at $SERVICE_DIR/$SERVICE_NAME"

# Reload systemd, enable and start the service
systemctl --user daemon-reload
systemctl --user enable $SERVICE_NAME
systemctl --user restart $SERVICE_NAME

echo "🚀 Service started and enabled to run on boot!"
echo ""
echo "To check the status, run: systemctl --user status $SERVICE_NAME"
echo "To stop it, run: systemctl --user stop $SERVICE_NAME"
echo "To view logs, run: journalctl --user -u $SERVICE_NAME -f"
