#!/bin/bash
# Keep Render service awake by pinging it every 5 minutes

RENDER_URL="https://ncii-infra-mapping.onrender.com/"
INTERVAL=300  # 5 minutes in seconds

echo "Starting keepalive for Render service..."
echo "URL: $RENDER_URL"
echo "Ping interval: $INTERVAL seconds (5 minutes)"
echo "Press Ctrl+C to stop"
echo ""

while true; do
    echo "$(date): Pinging Render service..."
    curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" "$RENDER_URL" || echo "Failed to ping"
    sleep $INTERVAL
done

