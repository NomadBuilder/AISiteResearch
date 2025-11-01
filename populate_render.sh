#!/bin/bash
# Script to populate Render PostgreSQL database with domains

echo "🚀 Populating Render PostgreSQL database..."
echo ""

# Set Render PostgreSQL connection (override local .env)
export POSTGRES_HOST='dpg-d42kod95pdvs73d5nt30-a.oregon-postgres.render.com'
export POSTGRES_PORT='5432'
export POSTGRES_USER='ncii_user'
export POSTGRES_PASSWORD='Zu1uJcsJjAfN3ZAx4N9aN9vjwFqKrj91'
export POSTGRES_DB='ncii'

echo "Using Render database: $POSTGRES_HOST"
echo ""

# Run enrichment script
python3 scripts/enrich_domains.py --csv data/input/domains.csv

echo ""
echo "✅ Done! Check your Render app: https://ncii-infra-mapping.onrender.com/"

