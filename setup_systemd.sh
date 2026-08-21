#!/bin/bash
set -e

PROJECT_DIR="/home/ravi/Desktop/Study Material/Projects/Personal/twitter-automation"
SYSTEMD_USER_DIR="$HOME/.config/systemd/user"

echo "Setting up systemd timer for Twitter Automation..."

mkdir -p "$SYSTEMD_USER_DIR"

cp "$PROJECT_DIR/systemd/twitter-generator.service" "$SYSTEMD_USER_DIR/"
cp "$PROJECT_DIR/systemd/twitter-generator.timer" "$SYSTEMD_USER_DIR/"

echo "Reloading systemd user daemon..."
systemctl --user daemon-reload

echo "Enabling and starting twitter-generator.timer..."
systemctl --user enable --now twitter-generator.timer

echo "=================================================="
echo "Systemd Timer successfully installed & started!"
echo "=================================================="
systemctl --user status twitter-generator.timer --no-pager
echo "--------------------------------------------------"
systemctl --user list-timers twitter-generator.timer --no-pager
