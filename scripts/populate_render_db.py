#!/usr/bin/env python3
"""Populate Render PostgreSQL database with domains."""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.postgres_client import PostgresClient
from src.enrichment.enrichment_pipeline import enrich_domain
import time

# List of domains to enrich (from your previous input)
DOMAINS = [
    "adultdeepfakes.com",
    "realdeepfakes.com",
    "deepfakeporn.net",
    "sexcelebrity.net",
    "deephot.link",
    "aicelebs.club",
    "deepfucks.com",
    "deepkpop.com",
    "porndeepfake.net",
    "sexystars.online",
    "desifakes.com",
    "deepfakesporn.com",
    "undress.cc",
    "clothoff.net",
    "facy.ai",
    "nudify.online",
    "pornworks.com",
    "deepstrip.com",
]

def normalize_provider_name(name):
    """Normalize provider names to merge variants."""
    if not name:
        return name
    name_lower = name.lower().strip()
    if 'cloudflare' in name_lower:
        return 'Cloudflare, Inc.'
    if 'namecheap' in name_lower:
        return 'Namecheap, Inc.'
    return name.strip()


def populate_database():
    """Populate Render database with domains."""
    print(f"Connecting to Render PostgreSQL database...")
    print(f"Host: {os.getenv('POSTGRES_HOST', 'localhost')}")
    
    postgres = PostgresClient()
    
    try:
        # Check existing domains
        existing_domains = postgres.get_all_enriched_domains()
        existing_domain_names = {d.get('domain', '').lower() for d in existing_domains}
        print(f"Found {len(existing_domain_names)} existing domains in database")
        
        # Filter out already enriched domains
        domains_to_process = [
            d for d in DOMAINS 
            if d.lower() not in existing_domain_names
        ]
        
        if not domains_to_process:
            print("All domains already enriched!")
            return
        
        print(f"\nProcessing {len(domains_to_process)} new domains...")
        
        ip_api_count = 0
        last_minute_start = time.time()
        
        for idx, domain in enumerate(domains_to_process):
            print(f"\n[{idx + 1}/{len(domains_to_process)}] Processing: {domain}")
            
            # Rate limiting for IP API (45 requests/minute)
            current_time = time.time()
            if current_time - last_minute_start >= 60:
                ip_api_count = 0
                last_minute_start = current_time
            
            if ip_api_count >= 45:
                wait_time = 60 - (current_time - last_minute_start) + 1
                print(f"  ⏳ Rate limit reached. Waiting {wait_time:.0f} seconds...")
                time.sleep(wait_time)
                ip_api_count = 0
                last_minute_start = time.time()
            
            # Enrich domain
            try:
                enrichment_data = enrich_domain(domain)
                
                if enrichment_data.get("ip_address"):
                    ip_api_count += 1
                
                # Store in PostgreSQL
                domain_id = postgres.insert_domain(domain, "Manual import", "")
                postgres.insert_enrichment(domain_id, enrichment_data)
                
                print(f"  ✓ Stored in database")
                
                # Small delay to avoid overwhelming APIs
                time.sleep(1)
                
            except Exception as e:
                print(f"  ✗ Error: {e}")
                continue
        
        # Final count
        final_domains = postgres.get_all_enriched_domains()
        print(f"\n✓ Complete! Database now contains {len(final_domains)} domains")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        postgres.close()


if __name__ == "__main__":
    # Set Render database connection if not already set
    if not os.getenv("POSTGRES_HOST"):
        print("Set Render PostgreSQL connection:")
        print("export POSTGRES_HOST='dpg-d42kod95pdvs73d5nt30-a.oregon-postgres.render.com'")
        print("export POSTGRES_PORT='5432'")
        print("export POSTGRES_USER='ncii_user'")
        print("export POSTGRES_PASSWORD='Zu1uJcsJjAfN3ZAx4N9aN9vjwFqKrj91'")
        print("export POSTGRES_DB='ncii'")
        print("\nOr create a .env file with these values")
        sys.exit(1)
    
    populate_database()

