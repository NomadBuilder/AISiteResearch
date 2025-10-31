# Quick Start Guide

This guide will help you get the NCII Infrastructure Mapping tool up and running quickly.

## Prerequisites

1. **Python 3.9+** installed
2. **Docker and Docker Compose** installed
3. **Git** (optional, for cloning)

## Step-by-Step Setup

### 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python packages
pip install -r requirements.txt
```

### 2. Start Databases

```bash
# Start Neo4j and PostgreSQL containers
docker-compose up -d

# Wait a few seconds for databases to initialize
sleep 10

# Verify databases are running
docker ps
```

You should see two containers running:
- `ncii-infra-neo4j` on ports 7474 (HTTP) and 7687 (Bolt)
- `ncii-infra-postgres` on port 5432

### 3. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env if needed (defaults should work for local development)
# Add API keys if you have them:
# - IPLOCATE_API_KEY (optional)
# - WHATCMS_API_KEY (optional)
```

### 4. Prepare Input Data

Create a CSV file with domains to analyze:

```bash
# Create input directory if it doesn't exist
mkdir -p data/input

# Create domains.csv (or use the example)
cat > data/input/domains.csv << EOF
domain,source,notes
example.com,Test,Sample domain for testing
example.net,Test,Another test domain
EOF
```

### 5. Run Enrichment Pipeline

```bash
# Basic enrichment (processes all domains in CSV)
python scripts/enrich_domains.py

# Or with options:
python scripts/enrich_domains.py --csv data/input/domains.csv --limit 5
```

The script will:
- Read domains from CSV
- Enrich each domain with WHOIS, DNS, IP location, CMS, and payment processor data
- Store results in Neo4j and PostgreSQL

### 6. View Visualization

```bash
# Start Flask web server
python app.py
```

Open your browser to `http://localhost:5000` to see the interactive graph visualization.

### 7. Export Data

```bash
# Export to CSV and JSON
python scripts/export_data.py

# Or export only CSV
python scripts/export_data.py --format csv

# Or export only JSON
python scripts/export_data.py --format json
```

Exported files will be saved to `data/output/` with timestamps.

## Using Prefect Orchestration

For more advanced workflow management:

```bash
# Run with Prefect
python scripts/orchestrate.py --csv data/input/domains.csv

# With options
python scripts/orchestrate.py --csv data/input/domains.csv --limit 10 --export both
```

## Using Make Commands

The project includes a Makefile for convenience:

```bash
# Setup environment
make setup

# Start databases
make start-db

# Run enrichment
make enrich

# Start visualization
make visualize

# Export data
make export

# Stop databases
make stop-db
```

## Troubleshooting

### Databases Not Starting

```bash
# Check if ports are already in use
lsof -i :7474  # Neo4j HTTP
lsof -i :7687  # Neo4j Bolt
lsof -i :5432  # PostgreSQL

# If ports are in use, either stop the conflicting service
# or modify ports in docker-compose.yml
```

### Connection Errors

- **Neo4j**: Make sure the container is running and check credentials in `.env`
- **PostgreSQL**: Verify the container is running and credentials match

### API Rate Limits

- IPLocate.io: 1,000 requests/day (free tier)
- ip-api.com: 45 requests/minute (free tier)
- WhatCMS: Limited free lookups

If you hit rate limits, the script will continue but some enrichments may be incomplete.

### Empty Visualization

If the graph is empty:
1. Make sure you've run the enrichment pipeline first
2. Check that domains were successfully processed (check console output)
3. Verify Neo4j has data: Open http://localhost:7474 and run `MATCH (n) RETURN n LIMIT 10`

## Next Steps

- Add more domains to `data/input/domains.csv`
- Customize enrichment modules in `src/enrichment/`
- Extend visualization in `static/js/visualization.js`
- Add new data sources or APIs

## Support

For issues or questions, refer to the main README.md file.

