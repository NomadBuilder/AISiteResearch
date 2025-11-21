#!/bin/bash
# Run enrichment with Mac sleep prevention

# Set Render database connection
export POSTGRES_HOST='dpg-d42kod95pdvs73d5nt30-a.oregon-postgres.render.com'
export POSTGRES_PORT='5432'
export POSTGRES_USER='ncii_user'
export POSTGRES_PASSWORD='Zu1uJcsJjAfN3ZAx4N9aN9vjwFqKrj91'
export POSTGRES_DB='ncii'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

echo "🚀 Starting enrichment with Mac sleep prevention..."
echo "📝 Logs: enrichment.log"
echo "⏸️  Press Ctrl+C to stop (Mac will sleep normally after)"
echo ""

# Use caffeinate to prevent Mac sleep during enrichment
# -d: prevent display sleep
# -i: prevent idle sleep
# -m: prevent disk sleep
# -s: prevent system sleep (only on AC power)
# -w: wait for process to exit
caffeinate -dimsu -w $$ python3 scripts/enrich_missing_only.py 2>&1 | tee enrichment.log

echo ""
echo "✅ Enrichment complete! Mac can sleep normally now."


