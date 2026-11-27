#!/bin/bash

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMPOSE_FILE="docker-compose.prod.yml"

cd "$PROJECT_DIR"

echo "Stopping application containers..."

docker compose -f "$COMPOSE_FILE" down

echo "Cleanup completed successfully"
echo "PostgreSQL data volume preserved"
