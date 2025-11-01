# Manual Render Deployment Guide

This guide walks you through manually deploying your Flask app to Render (free tier).

## Prerequisites

✅ **PostgreSQL Database**: Already created on Render
- Host: `dpg-d42kod95pdvs73d5nt30-a.oregon-postgres.render.com`
- Port: `5432`
- User: `ncii_user`
- Password: `Zu1uJcsJjAfN3ZAx4N9aN9vjwFqKrj91`
- Database: `ncii`

✅ **GitHub Repository**: https://github.com/NomadBuilder/AISiteResearch

## Step-by-Step Instructions

### Step 1: Create Web Service

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click the **"New +"** button (top right)
3. Select **"Web Service"** from the dropdown

### Step 2: Connect GitHub Repository

1. Click **"Connect GitHub"** (if not already connected)
2. Authorize Render to access your GitHub account
3. Select your repository: **`NomadBuilder/AISiteResearch`**
4. Click **"Connect"**

### Step 3: Configure Service Settings

Fill in the following:

**Basic Settings:**
- **Name**: `ncii-infra-mapping` (or any name you prefer)
- **Region**: Choose closest to you (e.g., `Oregon (US West)`)

**Build & Deploy:**
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120`

**Plan:**
- Select **"Free"** plan

### Step 4: Add Environment Variables

Before clicking "Create Web Service", scroll down to **"Advanced"** section and click **"Add Environment Variable"** for each:

**PostgreSQL Connection:**
1. Key: `POSTGRES_HOST`
   Value: `dpg-d42kod95pdvs73d5nt30-a.oregon-postgres.render.com`

2. Key: `POSTGRES_PORT`
   Value: `5432`

3. Key: `POSTGRES_USER`
   Value: `ncii_user`

4. Key: `POSTGRES_PASSWORD`
   Value: `Zu1uJcsJjAfN3ZAx4N9aN9vjwFqKrj91`

5. Key: `POSTGRES_DB`
   Value: `ncii`

**Application Settings:**
6. Key: `FLASK_ENV`
   Value: `production`

7. Key: `SECRET_KEY`
   Value: `659262f096f5dd75ab3676d73f32a23edaf70d161ecb863760256f31f1dab187`

8. Key: `OPENAI_API_KEY` (Optional - only if you want AI analysis)
   Value: (Leave empty or add your OpenAI key)

**Note**: Neo4j variables are NOT needed - the app works with PostgreSQL only!

### Step 5: Create and Deploy

1. Scroll to bottom and click **"Create Web Service"**
2. Render will start building your app (takes 2-5 minutes)
3. Watch the build logs - you'll see it installing dependencies
4. Once deployed, you'll see "Your service is live at: https://ncii-infra-mapping.onrender.com"

### Step 6: Verify Deployment

1. Click on your service name in the dashboard
2. Go to **"Logs"** tab to see if there are any errors
3. Visit your app URL (should be something like `https://ncii-infra-mapping.onrender.com`)
4. The app may take 30-60 seconds to start on first request (free tier spins down after inactivity)

## Troubleshooting

### App won't start
- Check the **"Logs"** tab in Render dashboard
- Common issues:
  - Missing environment variables → Check "Environment" tab
  - Database connection errors → Verify PostgreSQL credentials
  - Import errors → Check build logs

### Database connection errors
- Verify all PostgreSQL environment variables are set correctly
- Make sure PostgreSQL database is running (check in Render dashboard)
- Try the connection from Render's shell: Go to service → "Shell" tab → run:
  ```bash
  python3 -c "from src.database.postgres_client import PostgresClient; PostgresClient(); print('Connected!')"
  ```

### First request is slow
- Normal on free tier - app spins down after 15 min inactivity
- Takes ~30 seconds to wake up on first request after inactivity

## Updating Your App

Whenever you push to GitHub:
1. Render automatically detects changes
2. Rebuilds and redeploys automatically
3. Check "Events" tab to see deployment status

## Cost

**Free tier includes:**
- Web service: 512 MB RAM
- PostgreSQL: 768 MB RAM
- Spins down after 15 min inactivity (wakes automatically)
- Auto-deploy from GitHub

**To upgrade (optional):**
- $7/month for always-on service (no spin-down)

