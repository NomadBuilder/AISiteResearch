# NCII Infrastructure Mapping Tool

A tool to map and visualize the infrastructure (hosts, CDNs, CMS, payment processors, domains) behind AI-generated non-consensual intimate imagery (NCII) websites.

## Project Overview

This tool helps NGOs, researchers, and law enforcement track infrastructure patterns by:
- Ingesting domain lists from CSV or curated sources
- Enriching domains with hosting, CDN, and tech stack data using free APIs
- Visualizing relationships in an interactive graph
- Exporting enriched datasets for analysis

## Ethics & Safety

- **No content collection**: This tool only collects metadata (IPs, hosting info, tech stack)
- **Anonymized data**: Personal information is not stored
- **Compliance**: Designed to comply with data privacy and NCII laws
- **Secure access**: API keys and database credentials are stored securely

## Prerequisites

- Python 3.9+
- Docker and Docker Compose
- Free API keys (optional):
  - IPLocate.io (1,000 requests/day free tier)
  - WhatCMS (limited free lookups)

## Quick Start

1. **Clone and setup**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Start databases**:
```bash
docker-compose up -d
```

3. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your API keys if needed
```

4. **Prepare input CSV**:
Create `data/input/domains.csv`:
```csv
domain,source,notes
example1.com,NGO list,Known NCII site
example2.net,Web search,High traffic
```

5. **Run enrichment pipeline**:
```bash
python scripts/enrich_domains.py
```

6. **Start visualization server**:
```bash
python app.py
```

Visit `http://localhost:5000` to view the interactive graph.

## Project Structure

```
.
├── app.py                 # Flask web server for visualization
├── scripts/
│   ├── enrich_domains.py  # Main enrichment pipeline
│   └── export_data.py     # Export to CSV/JSON
├── src/
│   ├── enrichment/        # Enrichment modules
│   ├── database/          # Database models and connections
│   └── visualization/     # Frontend visualization code
├── data/
│   ├── input/             # Input CSV files
│   └── output/            # Exported datasets
├── templates/             # HTML templates
├── static/                # CSS, JS, images
└── docker-compose.yml     # Database containers
```

## V1 Features

- ✅ CSV input processing
- ✅ WHOIS and DNS enrichment
- ✅ IP location and hosting lookup
- ✅ CMS/tech stack detection
- ✅ Neo4j graph database storage
- ✅ Interactive D3.js visualization
- ✅ CSV/JSON export

## Roadmap

- **V2**: Automated crawler, larger domain intake
- **V3**: Payment processor detection, CDN network mapping
- **V4**: Live dashboard, real-time alerts

## License

This project is intended for legitimate research, NGO, and law enforcement use only.

