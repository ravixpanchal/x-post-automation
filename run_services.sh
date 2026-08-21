#!/bin/bash
PROJECT_DIR="/home/ravi/Desktop/Study Material/Projects/Personal/twitter-automation"
cd "$PROJECT_DIR" || exit

# Ensure virtualenv is used
VENV_PYTHON="$PROJECT_DIR/venv/bin/python"

# Print instructions
echo "Starting Flask Server..."
# Run flask app in background, redirect logs to app.log
"$VENV_PYTHON" -u app.py > app.log 2>&1 &
FLASK_PID=$!
echo "Flask Server started with PID: $FLASK_PID"

NGROK_BIN=$(command -v ngrok || echo "/snap/bin/ngrok")
"$NGROK_BIN" http --domain=matted-crested-hesitancy.ngrok-free.dev 5000 > ngrok.log 2>&1 &
NGROK_PID=$!
echo "ngrok started with PID: $NGROK_PID"

# Wait a couple of seconds for ngrok to initialize
sleep 4

# Fetch the public URL from ngrok API
NGROK_URL=$(curl -s http://127.0.0.1:4040/api/tunnels | grep -o '"public_url":"[^"]*' | head -n1 | cut -d'"' -f4)

echo "============================================="
echo "Flask Log is written to app.log"
echo "ngrok Log is written to ngrok.log"
echo "ngrok Public URL: $NGROK_URL"
echo "Configure the following Request URL in Slack:"
echo "$NGROK_URL/slack/actions"
echo "============================================="

# Keep script running to allow clean exit on Ctrl+C
cleanup() {
    echo "Stopping services..."
    kill $FLASK_PID
    kill $NGROK_PID
    exit
}

trap cleanup INT TERM

# Wait for children
wait
