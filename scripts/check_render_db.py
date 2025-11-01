#!/usr/bin/env python3
"""Quick script to check Render PostgreSQL database status."""

import sys
import os
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.postgres_client import PostgresClient

def check_database():
    """Check Render database status."""
    # Set Render PostgreSQL connection if not already set
    if not os.getenv("POSTGRES_HOST"):
        os.environ["POSTGRES_HOST"] = "dpg-d42kod95pdvs73d5nt30-a.oregon-postgres.render.com"
        os.environ["POSTGRES_PORT"] = "5432"
        os.environ["POSTGRES_USER"] = "ncii_user"
        os.environ["POSTGRES_PASSWORD"] = "Zu1uJcsJjAfN3ZAx4N9aN9vjwFqKrj91"
        os.environ["POSTGRES_DB"] = "ncii"
    
    print("🔍 Checking Render PostgreSQL database...")
    print(f"   Host: {os.getenv('POSTGRES_HOST')}")
    print(f"   Database: {os.getenv('POSTGRES_DB')}\n")
    
    try:
        postgres = PostgresClient()
        
        # Get all domains
        domains = postgres.get_all_enriched_domains()
        
        print(f"✅ Connected successfully!\n")
        print(f"📊 Database Statistics:")
        print(f"   Total domains: {len(domains)}")
        
        if domains:
            # Count enriched vs not enriched
            enriched = sum(1 for d in domains if d.get('ip_address') or d.get('host_name'))
            not_enriched = len(domains) - enriched
            
            print(f"   Enriched: {enriched}")
            print(f"   Not yet enriched: {not_enriched}\n")
            
            # Show some stats
            hosts = {}
            cdns = {}
            cms = {}
            registrars = {}
            
            for domain in domains:
                if domain.get('host_name'):
                    hosts[domain['host_name']] = hosts.get(domain['host_name'], 0) + 1
                if domain.get('cdn'):
                    cdns[domain['cdn']] = cdns.get(domain['cdn'], 0) + 1
                if domain.get('cms'):
                    cms[domain['cms']] = cms.get(domain['cms'], 0) + 1
                if domain.get('registrar'):
                    registrars[domain['registrar']] = registrars.get(domain['registrar'], 0) + 1
            
            if hosts:
                print(f"🏢 Top Hosting Providers:")
                for host, count in sorted(hosts.items(), key=lambda x: x[1], reverse=True)[:5]:
                    print(f"   {host}: {count} domains")
                print()
            
            if cdns:
                print(f"🌐 Top CDNs:")
                for cdn, count in sorted(cdns.items(), key=lambda x: x[1], reverse=True)[:5]:
                    print(f"   {cdn}: {count} domains")
                print()
            
            if registrars:
                print(f"📝 Top Registrars:")
                for reg, count in sorted(registrars.items(), key=lambda x: x[1], reverse=True)[:5]:
                    print(f"   {reg}: {count} domains")
                print()
            
            # Show most recent domains
            print(f"📋 Most Recent Domains (last 10):")
            for i, domain in enumerate(domains[-10:], 1):
                domain_name = domain.get('domain', 'Unknown')
                enriched_status = "✓" if (domain.get('ip_address') or domain.get('host_name')) else "○"
                print(f"   {enriched_status} {domain_name}")
        
        else:
            print("   ⚠️  No domains found in database yet.")
            print("   Run: python3 scripts/enrich_domains.py --csv data/input/domains.csv")
        
        postgres.close()
        
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    check_database()

