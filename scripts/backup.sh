#!/bin/bash

set -euo pipefail
umask 077

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKUP_DIR="$PROJECT_DIR/backups"
TIMESTAMP="$(date -u '+%Y%m%d_%H%M%S')"
BACKUP_FILE="$BACKUP_DIR/ticketdb_$TIMESTAMP.sql"

mkdir -p "$BACKUP_DIR"

echo "Starting PostgreSQL backup..."

if docker exec ticket-db sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB"' > "$BACKUP_FILE"; then
    echo "Backup completed successfully"
    echo "Backup location: $BACKUP_FILE"
else
    rm -f "$BACKUP_FILE"
    echo "ERROR: Database backup failed" >&2
    exit 1
fi
