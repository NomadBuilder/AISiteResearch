#!/usr/bin/env python3
"""Enrich only domains that are missing from the database."""

import sys
import os
import csv
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.postgres_client import PostgresClient
from scripts.enrich_domains import process_domains

def get_missing_domains():
    """Get list of domains from CSV that aren't in the database."""
    # Get domains from database
    postgres = PostgresClient()
    db_domains = {d.get('domain', '').lower().strip() for d in postgres.get_all_enriched_domains()}
    postgres.close()
    
    # Get domains from CSV
    csv_path = Path(__file__).parent.parent / "data" / "input" / "domains.csv"
    missing_domains = []
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            domain = row.get('domain', '').strip()
            if domain:
                # Normalize domain (remove www., http://, etc.)
                domain_normalized = domain.lower().replace('www.', '').replace('http://', '').replace('https://', '').split('/')[0].strip()
                if domain_normalized not in db_domains:
                    missing_domains.append({
                        'domain': domain_normalized,
                        'source': row.get('source', 'Unknown'),
                        'notes': row.get('notes', '')
                    })
    
    return missing_domains

if __name__ == "__main__":
    print("Finding missing domains...")
    missing = get_missing_domains()
    
    if not missing:
        print("✅ All domains already in database!")
        sys.exit(0)
    
    print(f"Found {len(missing)} missing domains")
    
    # Create temporary CSV with only missing domains
    import tempfile
    temp_csv = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='')
    writer = csv.DictWriter(temp_csv, fieldnames=['domain', 'source', 'notes'])
    writer.writeheader()
    writer.writerows(missing)
    temp_csv.close()
    
    print(f"Created temporary CSV: {temp_csv.name}")
    print(f"Processing {len(missing)} missing domains...\n")
    
    # Process only missing domains
    process_domains(temp_csv.name)
    
    # Cleanup
    os.unlink(temp_csv.name)
    print(f"\n✅ Done! Processed {len(missing)} missing domains.")


