# Deployment Guide for Render

This guide will help you deploy the NCII Infrastructure Mapping application to Render.

## Prerequisites

1. **GitHub Account** - Your code needs to be in a GitHub repository
2. **Render Account** - Sign up at [render.com](https://render.com) (free tier available)
3. **Neo4j Aura Account** - Sign up for free Neo4j cloud database at [neo4j.com/cloud/aura](https://neo4j.com/cloud/aura)

## Step 1: Prepare Your Code

Make sure your code is committed and pushed to GitHub. The following files should be in your repository:
- `app.py`
- `requirements.txt`
- `Procfile`
- `render.yaml` (optional, but recommended)
- All source files in `src/`
- `templates/` and `static/` directories

## Step 2: Set Up Neo4j Aura (Free Cloud Database)

1. Go to [neo4j.com/cloud/aura](https://neo4j.com/cloud/aura)
2. Sign up for a free account
3. Create a new **Free Database**
4. Choose a region close to you
5. Once created, note down:
   - **Connection URI** (e.g., `neo4j+s://xxxxx.databases.neo4j.io`)
   - **Username** (usually `neo4j`)
   - **Password** (you'll set this)

## Step 3: Deploy PostgreSQL Database on Render

1. Log into [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `ncii-postgres`
   - **Database**: `ncii_infra`
   - **User**: `ncii_user`
   - **Plan**: **Free** (768 MB RAM, 256 MB disk)
   - **Region**: Choose closest to you
4. Click **"Create Database"**
5. Wait for it to be ready (2-3 minutes)
6. Copy the **Internal Database URL** - you'll need this for environment variables

## Step 4: Deploy Web Service on Render

### Option A: Using render.yaml (Recommended)

1. In Render Dashboard, click **"New +"** → **"Blueprint"**
2. Connect your GitHub repository
3. Render will automatically detect `render.yaml`
4. Click **"Apply"** to create the services
5. After creation, go to your web service settings and add these environment variables manually:
   - `NEO4J_URI` - Your Neo4j Aura connection URI
   - `NEO4J_USER` - Your Neo4j username (usually `neo4j`)
   - `NEO4J_PASSWORD` - Your Neo4j password
   - `OPENAI_API_KEY` - (Optional) If you want to use OpenAI for analysis

### Option B: Manual Setup

1. In Render Dashboard, click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `ncii-infra-mapping`
   - **Environment**: **Python 3**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120`
   - **Plan**: **Free** (512 MB RAM)
4. Go to **"Environment"** tab and add these variables:

   **Database Connection (from PostgreSQL service):**
   - `POSTGRES_HOST` - Host from PostgreSQL service
   - `POSTGRES_PORT` - Port (usually `5432`)
   - `POSTGRES_USER` - Database user
   - `POSTGRES_PASSWORD` - Database password
   - `POSTGRES_DB` - Database name (`ncii_infra`)

   **Neo4j Connection (from Neo4j Aura):**
   - `NEO4J_URI` - Your Neo4j Aura URI (e.g., `neo4j+s://xxxxx.databases.neo4j.io`)
   - `NEO4J_USER` - Usually `neo4j`
   - `NEO4J_PASSWORD` - Your Neo4j password

   **Application Settings:**
   - `FLASK_ENV` - `production`
   - `SECRET_KEY` - Generate a random secret key (use `openssl rand -hex 32`)
   - `OPENAI_API_KEY` - (Optional) Your OpenAI API key if using OpenAI analysis

5. Click **"Create Web Service"**

## Step 5: Initialize Databases

After deployment, you need to initialize your databases:

1. Go to your web service on Render
2. Click **"Shell"** tab (or use SSH)
3. Run these commands:

```bash
# Initialize PostgreSQL schema (tables will be created automatically on first connection)
python3 -c "from src.database.postgres_client import PostgresClient; PostgresClient(); print('PostgreSQL initialized')"

# If you have domain data to import, you can run enrichment:
# python3 scripts/enrich_domains.py domains.csv
```

**Note**: The PostgreSQL schema will be created automatically when the app first connects. Neo4j nodes will be created as domains are enriched.

## Step 6: Access Your Application

1. Once deployed, Render will provide a URL like: `https://ncii-infra-mapping.onrender.com`
2. The app may take 30-60 seconds to start on first request (free tier spins down after inactivity)
3. Share this URL with organizations

## Important Notes

### Free Tier Limitations

- **Render Free Tier**: 
  - Spins down after 15 minutes of inactivity
  - Takes ~30 seconds to wake up on first request
  - 512 MB RAM for web service
  - 768 MB RAM for PostgreSQL

- **Neo4j Aura Free**:
  - Up to 50,000 nodes
  - 50,000 relationships
  - Perfect for this use case

### Troubleshooting

1. **App won't start**: Check logs in Render dashboard → "Logs" tab
2. **Database connection errors**: Verify environment variables are set correctly
3. **Neo4j connection issues**: Make sure you're using the correct URI format (`neo4j+s://` for Aura)
4. **Slow first load**: Normal on free tier - app is spinning up

### Upgrading (Optional)

If you need better performance:
- **Render Paid Plans**: $7/month for always-on service
- **Neo4j Aura**: Paid plans available for larger datasets

## Security Considerations

1. **Never commit** `.env` files or API keys to GitHub
2. Use Render's environment variables for all secrets
3. Generate a strong `SECRET_KEY` for production
4. Consider enabling HTTPS (enabled by default on Render)

## Support

- Render Docs: https://render.com/docs
- Neo4j Aura Docs: https://neo4j.com/docs/aura/
- Render Support: Available in dashboard

