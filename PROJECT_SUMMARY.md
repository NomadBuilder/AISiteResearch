# Project Summary

## Overview

This is a complete V1 implementation of the NCII Infrastructure Mapping Tool. The system maps and visualizes infrastructure (hosts, CDNs, CMS, payment processors, domains) behind websites using free APIs and tools.

## Architecture

### Components

1. **Data Input** (`scripts/enrich_domains.py`)
   - Reads domains from CSV files
   - Supports source and notes metadata
   - Can limit processing for testing

2. **Enrichment Pipeline** (`src/enrichment/`)
   - **WHOIS/DNS** (`whois_enrichment.py`): Domain registration and DNS records
   - **IP Location** (`ip_enrichment.py`): Hosting, ASN, geographic data
   - **CMS Detection** (`cms_enrichment.py`): Technology stack identification
   - **Payment Detection** (`payment_detection.py`): Payment processor identification
   - **Pipeline** (`enrichment_pipeline.py`): Orchestrates all enrichment steps

3. **Data Storage**
   - **Neo4j** (`src/database/neo4j_client.py`): Graph database for relationships
   - **PostgreSQL** (`src/database/postgres_client.py`): Relational storage for metadata

4. **Visualization** (`app.py`, `templates/`, `static/`)
   - Flask web server
   - D3.js interactive graph visualization
   - Real-time statistics and filtering

5. **Export** (`scripts/export_data.py`)
   - CSV export for analysis
   - JSON export for APIs/integration

6. **Orchestration** (`scripts/orchestrate.py`)
   - Prefect workflow management
   - Task dependencies and logging

## File Structure

```
ncii-infra-mapping/
├── app.py                    # Flask web server
├── docker-compose.yml        # Database containers
├── requirements.txt          # Python dependencies
├── Makefile                 # Convenience commands
├── README.md                # Main documentation
├── QUICKSTART.md            # Quick start guide
├── .env.example             # Environment template
├── .gitignore               # Git ignore rules
│
├── scripts/
│   ├── enrich_domains.py    # Main enrichment script
│   ├── export_data.py       # Data export
│   └── orchestrate.py       # Prefect orchestration
│
├── src/
│   ├── database/
│   │   ├── neo4j_client.py  # Neo4j graph database
│   │   └── postgres_client.py # PostgreSQL client
│   │
│   └── enrichment/
│       ├── whois_enrichment.py    # WHOIS/DNS
│       ├── ip_enrichment.py       # IP location
│       ├── cms_enrichment.py      # CMS detection
│       ├── payment_detection.py   # Payment processors
│       └── enrichment_pipeline.py # Main pipeline
│
├── templates/
│   └── index.html           # Visualization page
│
├── static/
│   ├── css/
│   │   └── style.css        # Styling
│   └── js/
│       └── visualization.js # D3.js graph
│
├── data/
│   ├── input/
│   │   └── domains.example.csv # Example input
│   └── output/              # Exported data
│
└── tests/
    └── test_enrichment.py   # Unit tests
```

## Key Features

### ✅ V1 Requirements Met

- [x] CSV input processing
- [x] WHOIS and DNS enrichment
- [x] IP location and hosting lookup (free APIs)
- [x] CMS/tech stack detection
- [x] Payment processor detection
- [x] Neo4j graph database storage
- [x] PostgreSQL relational storage
- [x] Interactive D3.js visualization
- [x] CSV/JSON export
- [x] Docker containerization
- [x] Prefect orchestration

### Data Flow

```
CSV Input → Enrichment Pipeline → Neo4j (Graph) + PostgreSQL (Metadata) → Visualization
                                                        ↓
                                                    Export (CSV/JSON)
```

### Free APIs Used

1. **IPLocate.io**: IP → Location, ASN, ISP (1,000/day free)
2. **ip-api.com**: Fallback IP lookup (45/min free)
3. **WhatCMS**: CMS detection (limited free tier)
4. **python-whois**: WHOIS data (no API key needed)
5. **dnspython**: DNS records (no API key needed)

## Usage Examples

### Basic Enrichment

```bash
python scripts/enrich_domains.py --csv data/input/domains.csv
```

### With Limit (Testing)

```bash
python scripts/enrich_domains.py --csv data/input/domains.csv --limit 5
```

### Prefect Orchestration

```bash
python scripts/orchestrate.py --csv data/input/domains.csv --export both
```

### Visualization

```bash
python app.py
# Open http://localhost:5000
```

### Export

```bash
python scripts/export_data.py --format csv
```

## Database Schema

### Neo4j Nodes
- **Domain**: Domains being tracked
- **Host**: IP addresses and hosting providers
- **CDN**: Content delivery networks
- **CMS**: Content management systems
- **PaymentProcessor**: Payment processors

### Neo4j Relationships
- `Domain -[:HOSTED_ON]-> Host`
- `Domain -[:USES_CDN]-> CDN`
- `Domain -[:USES_CMS]-> CMS`
- `Domain -[:USES_PAYMENT]-> PaymentProcessor`

### PostgreSQL Tables
- **domains**: Domain metadata (domain, source, notes)
- **domain_enrichment**: Enrichment data (IP, hosting, CMS, etc.)

## Ethics & Safety

- ✅ No content collection (metadata only)
- ✅ Anonymized data storage
- ✅ Secure credential management
- ✅ Compliance-focused design

## Next Steps (V2+)

- Automated web crawler
- Larger domain intake
- Incremental updates
- Payment processor network mapping
- Multi-API enrichment correlation
- Real-time dashboard
- NGO/law enforcement data feed integration

## Testing

Run tests with:
```bash
pytest tests/ -v
```

## Notes

- Default database passwords are in `.env.example` - change for production
- API keys are optional but recommended for higher rate limits
- The system gracefully handles API failures and continues processing
- All data is stored locally by default (Docker containers)

