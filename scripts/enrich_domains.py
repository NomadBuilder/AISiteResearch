"""Main script to read domains from CSV and enrich them."""

import sys
import os
import time
# import pandas as pd  # Optional - use CSV module instead
import csv
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.enrichment.enrichment_pipeline import enrich_domain
from src.database.postgres_client import PostgresClient


def normalize_provider_name(name):
    """Normalize provider names to merge variants (e.g., 'Cloudflare' and 'Cloudflare, Inc.')."""
    if not name:
        return name
    name_lower = name.lower().strip()
    # Cloudflare variants
    if 'cloudflare' in name_lower:
        return 'Cloudflare, Inc.'
    # Namecheap variants
    if 'namecheap' in name_lower:
        return 'Namecheap, Inc.'
    # Return original if no normalization needed
    return name.strip()


def read_domains_csv(csv_path: str) -> list:
    """Read domains from CSV file."""
    domains = []
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Support both 'domain' and 'url' column names
                domain = row.get('domain') or row.get('url', '').strip()
                if domain:
                    # Remove http:// or https:// if present
                    domain = domain.replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0].strip()
                    if domain:
                        domains.append({
                            'domain': domain,
                            'source': row.get('source', 'Unknown'),
                            'notes': row.get('notes', '')
                        })
        
        if not domains:
            raise ValueError("CSV must contain a 'domain' column with at least one domain")
        
        return domains
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        raise


def process_domains(csv_path: str, limit: int = None):
    """Process domains from CSV and enrich them."""
    print(f"Reading domains from {csv_path}...")
    domains_data = read_domains_csv(csv_path)
    
    if limit:
        domains_data = domains_data[:limit]
    
    print(f"Found {len(domains_data)} domains to process\n")
    
    # Initialize database clients
    try:
        from src.database.neo4j_client import Neo4jClient
        neo4j = Neo4jClient()
        neo4j_available = True
    except (ImportError, Exception):
        neo4j_available = False
        neo4j = None
        print("Note: Neo4j not available, storing in PostgreSQL only")
    
    postgres = PostgresClient()
    
    try:
        ip_api_count = 0
        last_minute_start = time.time()
        
        for idx, row in enumerate(domains_data):
            domain = row["domain"].strip()
            source = row.get("source", "Unknown")
            notes = row.get("notes", "")
            
            print(f"\n[{idx + 1}/{len(domains_data)}] Processing: {domain}")
            
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
            
            # Store in Neo4j (optional)
            if neo4j_available:
                try:
                    neo4j.create_domain(domain, source, notes)
                    
                    # Create host node and link (normalize host name)
                    if enrichment_data.get("ip_address"):
                        host_name = enrichment_data.get("host_name", "Unknown")
                        normalized_host_name = normalize_provider_name(host_name) if host_name != "Unknown" else host_name
                        normalized_isp = normalize_provider_name(enrichment_data.get("isp")) if enrichment_data.get("isp") else None
                        neo4j.create_host(
                            host_name=normalized_host_name,
                            ip=enrichment_data["ip_address"],
                            asn=enrichment_data.get("asn"),
                            isp=normalized_isp
                        )
                        neo4j.link_domain_to_host(domain, enrichment_data["ip_address"])
                    
                    # Create CDN node and link (normalize name)
                    if enrichment_data.get("cdn"):
                        normalized_cdn = normalize_provider_name(enrichment_data["cdn"])
                        neo4j.create_cdn(normalized_cdn)
                        neo4j.link_domain_to_cdn(domain, normalized_cdn)
                    
                    # Create CMS node and link
                    if enrichment_data.get("cms"):
                        neo4j.create_cms(enrichment_data["cms"])
                        neo4j.link_domain_to_cms(domain, enrichment_data["cms"])
                    
                    # Create registrar node and link (normalize name)
                    if enrichment_data.get("registrar"):
                        normalized_registrar = normalize_provider_name(enrichment_data["registrar"])
                        neo4j.create_registrar(normalized_registrar)
                        neo4j.link_domain_to_registrar(domain, normalized_registrar)
                    
                    # Create payment processor nodes and links
                    if enrichment_data.get("payment_processor"):
                        processors = [p.strip() for p in enrichment_data["payment_processor"].split(",")]
                        for processor in processors:
                            neo4j.create_payment_processor(processor)
                            neo4j.link_domain_to_payment(domain, processor)
                except Exception as e:
                    print(f"  ⚠ Neo4j storage failed (continuing): {e}")
            
            print(f"  ✓ Stored in database")
    
    finally:
        if neo4j_available and neo4j:
            neo4j.close()
        postgres.close()
    
    print(f"\n✓ Processing complete! Enriched {len(domains_data)} domains.")


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

