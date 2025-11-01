#!/bin/bash
# Quick script to check Render database status

export POSTGRES_HOST='dpg-d42kod95pdvs73d5nt30-a.oregon-postgres.render.com'
export POSTGRES_PORT='5432'
export POSTGRES_USER='ncii_user'
export POSTGRES_PASSWORD='Zu1uJcsJjAfN3ZAx4N9aN9vjwFqKrj91'
export POSTGRES_DB='ncii'

python3 scripts/check_render_db.py

