#!/usr/bin/env bash
set -e

# Load env
set -a
source /app/.env
set +a

# Parse time (HH:MM)
SCRAPE_HOUR=$(echo "$SCRAPE_TIME" | cut -d: -f1)
SCRAPE_MIN=$(echo "$SCRAPE_TIME" | cut -d: -f2)

DUMP_HOUR=$(echo "$DUMP_TIME" | cut -d: -f1)
DUMP_MIN=$(echo "$DUMP_TIME" | cut -d: -f2)

# Generate crontab
cat <<EOF > /etc/cron.d/car-cron
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin

$SCRAPE_MIN $SCRAPE_HOUR * * * cd /app && python -m src.main >> /app/scrape.log 2>&1
$DUMP_MIN $DUMP_HOUR * * * cd /app && ./scripts/dump_db.sh >> /app/dump.log 2>&1
EOF

chmod 0644 /etc/cron.d/car-cron
crontab /etc/cron.d/car-cron

echo "Cron jobs registered:"
crontab -l

exec cron -f
