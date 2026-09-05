#!/bin/bash
set -e

PROJECT_DIR="/app"
cd "$PROJECT_DIR"

echo "============================================="
echo "🤖 Starting Twitter (X) Automation Services"
echo "============================================="

# Clean stale Chrome locks if volume mounted
PROFILE_DIR="${CHROME_PROFILE_DIR:-/root/.config/twitter-automation-chrome-profile}"
LOCK_FILE="$PROFILE_DIR/SingletonLock"
if [ -f "$LOCK_FILE" ]; then
    rm -f "$LOCK_FILE"
    echo "Cleared stale Chrome profile lock file."
fi

# 1. Start Flask App
echo "Starting Flask Webhook Server on port 5000..."
python3 -u app.py > app.log 2>&1 &
FLASK_PID=$!
echo "Flask Server started (PID: $FLASK_PID)."

# 2. Configure & Start Ngrok
if [ -n "$NGROK_AUTHTOKEN" ]; then
    echo "Setting Ngrok auth token..."
    ngrok config add-authtoken "$NGROK_AUTHTOKEN" > /dev/null 2>&1 || true
fi

echo "Starting Ngrok tunnel..."
if [ -n "$NGROK_DOMAIN" ]; then
    DOMAIN_VAL="$NGROK_DOMAIN"
    if [[ "$DOMAIN_VAL" != http* ]]; then
        DOMAIN_VAL="https://$DOMAIN_VAL"
    fi
    ngrok http --url="$DOMAIN_VAL" 5000 > ngrok.log 2>&1 &
else
    ngrok http 5000 > ngrok.log 2>&1 &
fi
NGROK_PID=$!

sleep 4

# Fetch Public Ngrok URL
NGROK_URL=$(curl -s http://127.0.0.1:4040/api/tunnels | grep -o '"public_url":"[^"]*' | head -n1 | cut -d'"' -f4)

echo "============================================="
echo "✅ All Services Started Successfully!"
if [ -n "$NGROK_URL" ]; then
    echo "🔗 Ngrok Public URL: $NGROK_URL"
    echo "👉 Configure Slack Request URL: $NGROK_URL/slack/actions"
else
    echo "⚠️ Could not extract Ngrok URL automatically. Check ngrok.log or http://localhost:4040"
fi
echo "============================================="

# 3. Background Tweet Generator Loop
generator_loop() {
    INTERVAL_HOURS="${GENERATE_INTERVAL_HOURS:-1}"
    INTERVAL_SECONDS=$((INTERVAL_HOURS * 3600))
    echo "Tweet generator scheduled every $INTERVAL_HOURS hour(s)."
    
    # Run initial post generation on container start
    echo "Running initial tweet generation..."
    python3 generate_post.py || true

    while true; do
        sleep "$INTERVAL_SECONDS"
        echo "Running scheduled tweet generation..."
        python3 generate_post.py || true
    done
}

if [ "$ENABLE_GENERATOR" != "false" ]; then
    generator_loop &
    GENERATOR_PID=$!
fi

cleanup() {
    echo "Stopping services gracefully..."
    kill "$FLASK_PID" 2>/dev/null || true
    kill "$NGROK_PID" 2>/dev/null || true
    if [ -n "$GENERATOR_PID" ]; then
        kill "$GENERATOR_PID" 2>/dev/null || true
    fi
    exit 0
}

trap cleanup INT TERM

# Tail logs to stdout so container output shows server activity
tail -f app.log ngrok.log &
TAIL_PID=$!

wait $TAIL_PID
