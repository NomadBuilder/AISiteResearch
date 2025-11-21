#!/usr/bin/env python3
"""
Manual domain import tool - helps you add domains from various sources.
Shows preview before adding to database.
"""

import csv
import sys
from pathlib import Path
from typing import List, Set

def read_domains_from_text(text: str) -> List[str]:
    """Extract domains from text (handles various formats)."""
    import re
    domains = set()
    
    # Pattern for domains
    domain_pattern = r'(?:https?://)?(?:www\.)?([a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.(?:[a-zA-Z]{2,}))'
    
    # Find all domains
    matches = re.findall(domain_pattern, text)
    for match in matches:
        domain = match.lower().strip()
        if domain and '.' in domain:
            # Clean up
            domain = domain.replace('www.', '')
            domain = domain.split('/')[0].split('?')[0]
            if len(domain) > 3:
                domains.add(domain)
    
    return list(domains)


def preview_domains(domains: List[str], existing_domains: Set[str]) -> dict:
    """Preview domains before adding."""
    new_domains = []
    duplicates = []
    
    for domain in domains:
        if domain.lower() in existing_domains:
            duplicates.append(domain)
        else:
            new_domains.append(domain)
    
    return {
        'new': new_domains,
        'duplicates': duplicates,
        'total_new': len(new_domains),
        'total_duplicates': len(duplicates)
    }


def get_existing_domains(csv_file: Path) -> Set[str]:
    """Get existing domains from CSV."""
    existing = set()
    if csv_file.exists():
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing.add(row.get('domain', '').lower())
    return existing


def main():
    """Main import function."""
    csv_file = Path(__file__).parent.parent / "data" / "input" / "domains.csv"
    existing_domains = get_existing_domains(csv_file)
    
    print("📥 Manual Domain Import Tool")
    print("=" * 60)
    print(f"\nCurrent domains in database: {len(existing_domains)}")
    print("\nPaste domains below (one per line, or comma-separated, or URLs):")
    print("Press Ctrl+D (Mac/Linux) or Ctrl+Z (Windows) when done, or type 'done':")
    print("-" * 60)
    
    # Read input
    lines = []
    try:
        while True:
            line = input()
            if line.lower().strip() == 'done':
                break
            lines.append(line)
    except EOFError:
        pass
    
    # Extract domains
    text = '\n'.join(lines)
    domains = read_domains_from_text(text)
    
    if not domains:
        print("\n❌ No domains found in input")
        return
    
    # Preview
    preview = preview_domains(domains, existing_domains)
    
    print("\n" + "=" * 60)
    print("📊 Preview Results:")
    print(f"   ✅ New domains: {preview['total_new']}")
    print(f"   ⚠️  Duplicates: {preview['total_duplicates']}")
    print(f"   📋 Total found: {len(domains)}")
    
    if preview['new']:
        print("\n✨ New domains to add (showing first 20):")
        for i, domain in enumerate(preview['new'][:20], 1):
            print(f"   {i:2d}. {domain}")
        if len(preview['new']) > 20:
            print(f"   ... and {len(preview['new']) - 20} more")
    
    if preview['duplicates']:
        print("\n⚠️  Duplicate domains (will be skipped):")
        for domain in preview['duplicates'][:10]:
            print(f"   • {domain}")
        if len(preview['duplicates']) > 10:
            print(f"   ... and {len(preview['duplicates']) - 10} more")
    
    if preview['new']:
        print("\n" + "=" * 60)
        confirm = input(f"\nAdd {preview['total_new']} new domains to database? (yes/no): ")
        
        if confirm.lower() in ['yes', 'y']:
            # Add to CSV
            file_exists = csv_file.exists()
            with open(csv_file, 'a', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['domain', 'source', 'notes'])
                if not file_exists:
                    writer.writeheader()
                
                for domain in preview['new']:
                    writer.writerow({
                        'domain': domain,
                        'source': 'Manual Import',
                        'notes': 'Imported via manual tool'
                    })
            
            print(f"\n✅ Added {preview['total_new']} domains to {csv_file}")
            print(f"   Total domains now: {len(existing_domains) + preview['total_new']}")
        else:
            print("\n❌ Import cancelled")
    else:
        print("\n⚠️  No new domains to add (all are duplicates)")


if __name__ == "__main__":
    main()


