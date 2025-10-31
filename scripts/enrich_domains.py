"""Main script to read domains from CSV and enrich them."""

import sys
import os
import time
import pandas as pd
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.enrichment.enrichment_pipeline import enrich_domain
from src.database.neo4j_client import Neo4jClient
from src.database.postgres_client import PostgresClient


def read_domains_csv(csv_path: str) -> pd.DataFrame:
    """Read domains from CSV file."""
    try:
        df = pd.read_csv(csv_path)
        
        # Validate required columns
        if "domain" not in df.columns:
            raise ValueError("CSV must contain a 'domain' column")
        
        # Ensure optional columns exist
        if "source" not in df.columns:
            df["source"] = "Unknown"
        if "notes" not in df.columns:
            df["notes"] = ""
        
        return df
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        raise


def process_domains(csv_path: str, limit: int = None):
    """Process domains from CSV and enrich them."""
    print(f"Reading domains from {csv_path}...")
    df = read_domains_csv(csv_path)
    
    if limit:
        df = df.head(limit)
    
    print(f"Found {len(df)} domains to process\n")
    
    # Initialize database clients
    neo4j = Neo4jClient()
    postgres = PostgresClient()
    
    try:
        ip_api_count = 0
        last_minute_start = time.time()
        
        for idx, row in df.iterrows():
            domain = row["domain"].strip()
            source = row.get("source", "Unknown")
            notes = row.get("notes", "")
            
            print(f"\n[{idx + 1}/{len(df)}] Processing: {domain}")
            
            # Rate limiting for IP API (45 requests/minute)
            current_time = time.time()
            if current_time - last_minute_start >= 60:
                # Reset counter every minute
                ip_api_count = 0
                last_minute_start = current_time
            
            if ip_api_count >= 45:
                # Wait until next minute
                wait_time = 60 - (current_time - last_minute_start) + 1
                print(f"  ⏳ Rate limit reached (45/min). Waiting {wait_time:.0f} seconds...")
                time.sleep(wait_time)
                ip_api_count = 0
                last_minute_start = time.time()
            
            # Enrich domain
            enrichment_data = enrich_domain(domain)
            
            # Track IP API calls (increment if IP was found and looked up)
            if enrichment_data.get("ip_address"):
                ip_api_count += 1
            
            # Small delay to avoid overwhelming APIs
            time.sleep(1)
            
            # Store in PostgreSQL
            domain_id = postgres.insert_domain(domain, source, notes)
            postgres.insert_enrichment(domain_id, enrichment_data)
            
            # Store in Neo4j
            neo4j.create_domain(domain, source, notes)
            
            # Create host node and link
            if enrichment_data.get("ip_address"):
                neo4j.create_host(
                    host_name=enrichment_data.get("host_name", "Unknown"),
                    ip=enrichment_data["ip_address"],
                    asn=enrichment_data.get("asn"),
                    country=enrichment_data.get("country"),
                    isp=enrichment_data.get("isp")
                )
                neo4j.link_domain_to_host(domain, enrichment_data["ip_address"])
            
            # Create CDN node and link
            if enrichment_data.get("cdn"):
                neo4j.create_cdn(enrichment_data["cdn"])
                neo4j.link_domain_to_cdn(domain, enrichment_data["cdn"])
            
            # Create CMS node and link
            if enrichment_data.get("cms"):
                neo4j.create_cms(enrichment_data["cms"])
                neo4j.link_domain_to_cms(domain, enrichment_data["cms"])
            
            # Create registrar node and link
            if enrichment_data.get("registrar"):
                neo4j.create_registrar(enrichment_data["registrar"])
                neo4j.link_domain_to_registrar(domain, enrichment_data["registrar"])
            
            # Create payment processor nodes and links (don't show in graph, but store for data)
            if enrichment_data.get("payment_processor"):
                processors = [p.strip() for p in enrichment_data["payment_processor"].split(",")]
                for processor in processors:
                    neo4j.create_payment_processor(processor)
                    neo4j.link_domain_to_payment(domain, processor)
            
            print(f"  ✓ Stored in databases")
    
    finally:
        neo4j.close()
        postgres.close()
    
    print(f"\n✓ Processing complete! Enriched {len(df)} domains.")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Enrich domains from CSV file")
    parser.add_argument(
        "--csv",
        type=str,
        default="data/input/domains.csv",
        help="Path to CSV file with domains"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of domains to process (for testing)"
    )
    
    args = parser.parse_args()
    
    # Check if CSV exists
    if not os.path.exists(args.csv):
        print(f"Error: CSV file not found: {args.csv}")
        print("Please create a CSV file with the following format:")
        print("domain,source,notes")
        print("example.com,NGO list,Known NCII site")
        sys.exit(1)
    
    process_domains(args.csv, limit=args.limit)

