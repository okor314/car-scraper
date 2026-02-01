#!/usr/bin/env bash
set -a              
source .env
set +a

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M")
DUMP_DIR="dumps"

mkdir -p "$DUMP_DIR"

PGPASSWORD="$POSTGRES_PASSWORD" pg_dump \
  -h "$POSTGRES_HOST" \
  -p "$POSTGRES_PORT" \
  -U "$POSTGRES_USER" \
  "$POSTGRES_DB" \
  > "$DUMP_DIR/dump_$TIMESTAMP.sql"