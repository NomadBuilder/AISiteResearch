#!/usr/bin/env python3
"""Compare local and Render database results."""

import sys
import os
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.postgres_client import PostgresClient

def get_database_stats(postgres):
    """Get statistics from a database."""
    domains = postgres.get_all_enriched_domains()
    
    stats = {
        'total': len(domains),
        'enriched': sum(1 for d in domains if d.get('ip_address') or d.get('host_name')),
        'hosts': Counter(),
        'cdns': Counter(),
        'cms': Counter(),
        'registrars': Counter(),
    }
    
    for domain in domains:
        if domain.get('host_name'):
            stats['hosts'][domain['host_name']] += 1
        if domain.get('cdn'):
            stats['cdns'][domain['cdn']] += 1
        if domain.get('cms'):
            stats['cms'][domain['cms']] += 1
        if domain.get('registrar'):
            stats['registrars'][domain['registrar']] += 1
    
    return stats, domains

print("=" * 80)
print("DATABASE COMPARISON: Local vs Render")
print("=" * 80)

# Local database
print("\n📊 LOCAL DATABASE:")
print("-" * 80)
try:
    os.environ["POSTGRES_HOST"] = "localhost"
    os.environ["POSTGRES_PORT"] = "5432"
    os.environ["POSTGRES_USER"] = "ncii_user"
    os.environ["POSTGRES_PASSWORD"] = "ncii123password"
    os.environ["POSTGRES_DB"] = "ncii_infra"
    
    local_postgres = PostgresClient()
    local_stats, local_domains = get_database_stats(local_postgres)
    local_postgres.close()
    
    print(f"Total domains: {local_stats['total']}")
    print(f"Enriched: {local_stats['enriched']}")
    print(f"\nTop Hosts:")
    for host, count in local_stats['hosts'].most_common(5):
        print(f"  {host}: {count}")
    print(f"\nTop CDNs:")
    for cdn, count in local_stats['cdns'].most_common(5):
        print(f"  {cdn}: {count}")
    print(f"\nTop Registrars:")
    for reg, count in local_stats['registrars'].most_common(5):
        print(f"  {reg}: {count}")
    
except Exception as e:
    print(f"❌ Error connecting to local database: {e}")
    local_stats = None

# Render database
print("\n\n🌐 RENDER DATABASE:")
print("-" * 80)
try:
    os.environ["POSTGRES_HOST"] = "dpg-d42kod95pdvs73d5nt30-a.oregon-postgres.render.com"
    os.environ["POSTGRES_PORT"] = "5432"
    os.environ["POSTGRES_USER"] = "ncii_user"
    os.environ["POSTGRES_PASSWORD"] = "Zu1uJcsJjAfN3ZAx4N9aN9vjwFqKrj91"
    os.environ["POSTGRES_DB"] = "ncii"
    
    render_postgres = PostgresClient()
    render_stats, render_domains = get_database_stats(render_postgres)
    render_postgres.close()
    
    print(f"Total domains: {render_stats['total']}")
    print(f"Enriched: {render_stats['enriched']}")
    print(f"\nTop Hosts:")
    for host, count in render_stats['hosts'].most_common(5):
        print(f"  {host}: {count}")
    print(f"\nTop CDNs:")
    for cdn, count in render_stats['cdns'].most_common(5):
        print(f"  {cdn}: {count}")
    print(f"\nTop Registrars:")
    for reg, count in render_stats['registrars'].most_common(5):
        print(f"  {reg}: {count}")
    
except Exception as e:
    print(f"❌ Error connecting to Render database: {e}")
    render_stats = None

# Comparison
if local_stats and render_stats:
    print("\n\n🔍 COMPARISON:")
    print("-" * 80)
    print(f"Domain count difference: {render_stats['total'] - local_stats['total']} ({render_stats['total']} vs {local_stats['total']})")
    print(f"Enriched difference: {render_stats['enriched'] - local_stats['enriched']} ({render_stats['enriched']} vs {local_stats['enriched']})")
    
    # Compare top providers
    print("\nHost Provider Comparison:")
    local_top_hosts = {h: c for h, c in local_stats['hosts'].most_common(5)}
    render_top_hosts = {h: c for h, c in render_stats['hosts'].most_common(5)}
    for host in set(list(local_top_hosts.keys()) + list(render_top_hosts.keys())):
        local_count = local_top_hosts.get(host, 0)
        render_count = render_top_hosts.get(host, 0)
        diff = render_count - local_count
        if diff != 0:
            print(f"  {host}: Local={local_count}, Render={render_count} (diff: {diff:+d})")
        else:
            print(f"  {host}: {local_count} (same)")
    
    print("\nCDN Comparison:")
    local_top_cdns = {c: count for c, count in local_stats['cdns'].most_common(5)}
    render_top_cdns = {c: count for c, count in render_stats['cdns'].most_common(5)}
    for cdn in set(list(local_top_cdns.keys()) + list(render_top_cdns.keys())):
        local_count = local_top_cdns.get(cdn, 0)
        render_count = render_top_cdns.get(cdn, 0)
        diff = render_count - local_count
        if diff != 0:
            print(f"  {cdn}: Local={local_count}, Render={render_count} (diff: {diff:+d})")
        else:
            print(f"  {cdn}: {local_count} (same)")

print("\n" + "=" * 80)


