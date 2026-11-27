#!/bin/bash

set -euo pipefail

APP_URL="http://localhost:8000/tickets"
MAX_RETRIES=10
RETRY_DELAY=3

for ((attempt=1; attempt<=MAX_RETRIES; attempt++)); do
    echo "Health check attempt $attempt of $MAX_RETRIES"

    if curl -fsS --max-time 5 "$APP_URL" > /dev/null 2>&1; then
        echo "SUCCESS: Application is healthy"
        exit 0
    fi

    if ((attempt < MAX_RETRIES)); then
        sleep "$RETRY_DELAY"
    fi
done

echo "ERROR: Application health check failed" >&2
exit 1
