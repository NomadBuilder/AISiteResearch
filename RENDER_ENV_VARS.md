# Render Environment Variables Setup

## PostgreSQL Connection (Already Created)
From your Render PostgreSQL database:

- **POSTGRES_HOST**: `dpg-d42kod95pdvs73d5nt30-a.oregon-postgres.render.com`
- **POSTGRES_PORT**: `5432`
- **POSTGRES_USER**: `ncii_user`
- **POSTGRES_PASSWORD**: `Zu1uJcsJjAfN3ZAx4N9aN9vjwFqKrj91`
- **POSTGRES_DB**: `ncii`

## Neo4j Aura Connection
From your Neo4j Aura database (you need to get the connection URI):

- **NEO4J_URI**: `neo4j+s://bcab6690-xxxxx.databases.neo4j.io` (get full URI from Neo4j dashboard)
- **NEO4J_USER**: `neo4j`
- **NEO4J_PASSWORD**: `ylKmf7j1ykGb4LR9K1UFEf7Lv4fJD4R6lIasFYF596c`

## Application Settings

- **FLASK_ENV**: `production`
- **SECRET_KEY**: Generate with: `openssl rand -hex 32`
- **OPENAI_API_KEY**: (Optional) Your OpenAI API key if using AI analysis

## How to Add in Render:

1. Go to your web service in Render Dashboard
2. Click on "Environment" tab
3. Add each variable above
4. Click "Save Changes"
5. Render will automatically redeploy

