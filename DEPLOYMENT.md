# Deployment Guide for Render

This guide will help you deploy the NCII Infrastructure Mapping application to Render.

## Prerequisites

1. **GitHub Account** - Your code needs to be in a GitHub repository
2. **Render Account** - Sign up at [render.com](https://render.com) (free tier available)

**Note**: Neo4j is now optional! The app works perfectly with just PostgreSQL. You can add Neo4j later if you want graph database features, but it's not required.

## Step 1: Prepare Your Code

Make sure your code is committed and pushed to GitHub. The following files should be in your repository:
- `app.py`
- `requirements.txt`
- `Procfile`
- `render.yaml` (optional, but recommended)
- All source files in `src/`
- `templates/` and `static/` directories

## Step 2: Deploy PostgreSQL Database on Render

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

## Step 3: Deploy Web Service on Render

**Note**: Blueprint deployment requires a paid plan. Use manual setup instead:

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

   **Application Settings:**
   - `FLASK_ENV` - `production`
   - `SECRET_KEY` - Generate a random secret key (use `openssl rand -hex 32`)
   - `OPENAI_API_KEY` - (Optional) Your OpenAI API key if using OpenAI analysis

5. Click **"Create Web Service"**

## Step 4: Initialize Database

After deployment, the PostgreSQL schema will be created automatically when the app first connects. 

If you want to import domain data:
1. Go to your web service on Render
2. Click **"Shell"** tab
3. Run: `python3 scripts/enrich_domains.py domains.csv` (if you have a CSV file)

Or use the web interface to add domains one by one via the `/api/enrich` endpoint.

## Step 5: Access Your Application

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

- **Neo4j**: Not required! The app works perfectly with PostgreSQL only.

### Troubleshooting

1. **App won't start**: Check logs in Render dashboard → "Logs" tab
2. **Database connection errors**: Verify PostgreSQL environment variables are set correctly
3. **Slow first load**: Normal on free tier - app is spinning up (~30 seconds)

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
- Render Support: Available in dashboard

