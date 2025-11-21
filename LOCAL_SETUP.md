# Local Development Setup

## Current Configuration

Your local environment is now configured to connect to **Render's production database**, so you can:
- ✅ Work locally with real production data
- ✅ See all 110+ domains and their relationships
- ✅ Test changes before deploying to Render
- ✅ Keep production data safe (read-only access recommended)

## Database Connection

**Local `.env` file** is configured to use Render's PostgreSQL:
- Host: `dpg-d42kod95pdvs73d5nt30-a.oregon-postgres.render.com`
- Database: `ncii`
- User: `ncii_user`

## Running Locally

1. **Start the Flask server:**
   ```bash
   python3 app.py
   ```

2. **Access the application:**
   - Splash page: http://localhost:5001
   - Dashboard: http://localhost:5001/dashboard

3. **The app will automatically:**
   - Connect to Render's database
   - Load all 110+ domains
   - Display the graph visualization
   - Show all statistics and analysis

## Production (Render)

The production deployment at https://ncii-infra-mapping.onrender.com/ uses the same database, so:
- ✅ Changes you make locally will work in production
- ✅ Data is shared between local and production
- ✅ No need to sync databases

## Environment Variables

Your `.env` file contains:
- `POSTGRES_HOST` - Render database host
- `POSTGRES_PORT` - 5432
- `POSTGRES_USER` - ncii_user
- `POSTGRES_PASSWORD` - (stored securely)
- `POSTGRES_DB` - ncii

## Switching Between Local and Production Databases

If you want to use local Docker databases instead:

1. **Start Docker Desktop**
2. **Start local databases:**
   ```bash
   docker-compose up -d
   ```
3. **Update `.env` to use localhost:**
   ```bash
   POSTGRES_HOST=localhost
   POSTGRES_DB=ncii_infra
   ```

## Current Status

✅ **Local app connected to Render's database**
✅ **110 domains loaded**
✅ **Graph visualization working**
✅ **All API endpoints functional**

## Notes

- The app works with PostgreSQL only (Neo4j is optional)
- All data is read from the same database as production
- Be careful with write operations - they will affect production data
- Consider using a separate test database for development if needed

