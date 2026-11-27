#!/bin/bash

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMPOSE_FILE="docker-compose.prod.yml"

log() {
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] $1"
}

cd "$PROJECT_DIR"

log "Starting application deployment"

if ! docker info > /dev/null 2>&1; then
    log "ERROR: Docker is unavailable" >&2
    exit 1
fi

if [[ ! -f .env ]]; then
    log "ERROR: .env file is missing" >&2
    exit 1
fi

log "Validating Docker Compose configuration"
docker compose -f "$COMPOSE_FILE" config --quiet

log "Pulling latest container images"
docker compose -f "$COMPOSE_FILE" pull

log "Starting application containers"
docker compose -f "$COMPOSE_FILE" up -d

log "Performing application health check"
./scripts/healthcheck.sh

log "Deployment completed successfully"
