#!/usr/bin/env python3
"""
Domain discovery script - finds domains from various sources.
Supports multiple methods for discovering domains related to NCII/AI-generated content.
"""

import os
import sys
import csv
import json
import requests
from pathlib import Path
from typing import List, Set
from urllib.parse import urlparse
import re

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv

load_dotenv()


def discover_from_google_search(query: str, num_results: int = 100) -> List[str]:
    """
    Discover domains from Google search results.
    Note: This uses a simple approach - for production, consider using Google Custom Search API.
    """
    domains = set()
    
    try:
        # Using DuckDuckGo HTML scraping (no API key needed)
        # In production, use Google Custom Search API or SerpAPI
        print(f"Searching for: {query}")
        
        # Alternative: Use DuckDuckGo (respects privacy, no API key)
        url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            # Extract domains from links
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                try:
                    parsed = urlparse(href)
                    domain = parsed.netloc or parsed.path.split('/')[0]
                    # Clean domain
                    domain = domain.replace('www.', '').strip()
                    if domain and '.' in domain and not domain.startswith('http'):
                        domains.add(domain)
                except:
                    pass
        
        print(f"  Found {len(domains)} unique domains")
        return list(domains)
        
    except Exception as e:
        print(f"  Error searching: {e}")
        return []


def discover_from_file(file_path: str) -> List[str]:
    """Extract domains from a text file (one per line or comma-separated)."""
    domains = set()
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Handle comma-separated
                for item in line.split(','):
                    item = item.strip()
                    # Clean domain
                    item = item.replace('http://', '').replace('https://', '').replace('www.', '')
                    item = item.split('/')[0].split('?')[0]
                    
                    if item and '.' in item:
                        domains.add(item)
        
        print(f"  Found {len(domains)} unique domains from {file_path}")
        return list(domains)
        
    except Exception as e:
        print(f"  Error reading file: {e}")
        return []


def discover_from_api(api_type: str = "urlscan") -> List[str]:
    """
    Discover domains from security APIs.
    Options: urlscan.io, Shodan, etc.
    """
    domains = set()
    
    if api_type == "urlscan":
        try:
            # urlscan.io API (free tier: 10k searches/month)
            api_key = os.getenv("URLSCAN_API_KEY", "")
            
            # Search for related domains
            # Note: This is a placeholder - you'd need to search for specific patterns
            if api_key:
                url = "https://urlscan.io/api/v1/search/"
                params = {
                    "q": "deepfake OR deepnude OR nudify OR undress",
                    "size": 100
                }
                headers = {"API-Key": api_key}
                
                response = requests.get(url, params=params, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    for result in data.get("results", []):
                        domain = result.get("page", {}).get("domain", "")
                        if domain:
                            domains.add(domain)
                            
        except Exception as e:
            print(f"  Error with {api_type} API: {e}")
    
    return list(domains)


def discover_from_reddit(queries: List[str], limit: int = 100) -> List[str]:
    """
    Extract domains mentioned in Reddit posts/comments.
    Uses Pushshift API (free) or Reddit API.
    """
    domains = set()
    
    try:
        # Using Pushshift API (free, no auth needed for read-only)
        for query in queries:
            url = "https://api.pushshift.io/reddit/search/comment/"
            params = {
                "q": query,
                "size": limit,
                "fields": "body"
            }
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                for item in data.get("data", []):
                    body = item.get("body", "")
                    # Extract domains from text
                    domain_pattern = r'(?:https?://)?(?:www\.)?([a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.(?:[a-zA-Z]{2,}))'
                    found = re.findall(domain_pattern, body)
                    for domain in found:
                        domains.add(domain.lower())
        
        print(f"  Found {len(domains)} unique domains from Reddit")
        return list(domains)
        
    except Exception as e:
        print(f"  Error searching Reddit: {e}")
        return []


def discover_from_research_lists() -> List[str]:
    """
    Compile domains from research organizations and public reports.
    You can add known domain lists here.
    """
    domains = set()
    
    # Example: Add domains from known research sources
    # These would typically come from:
    # - Research papers
    # - NGO reports
    # - Public domain lists
    # - Security reports
    
    # Placeholder - add your sources here
    known_sources = [
        # Add file paths or URLs to domain lists
    ]
    
    for source in known_sources:
        if source.startswith('http'):
            # Download and parse
            try:
                response = requests.get(source, timeout=30)
                for line in response.text.split('\n'):
                    domain = line.strip()
                    if domain and '.' in domain:
                        domains.add(domain)
            except:
                pass
        else:
            # Local file
            domains.update(discover_from_file(source))
    
    return list(domains)


def save_domains(domains: List[str], output_file: str, source: str = "discovery"):
    """Save discovered domains to CSV file."""
    output_path = Path(__file__).parent.parent / "data" / "input" / output_file
    
    # Read existing domains to avoid duplicates
    existing_domains = set()
    if output_path.exists():
        with open(output_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_domains.add(row.get('domain', '').lower())
    
    # Add new domains
    new_domains = []
    for domain in domains:
        domain_lower = domain.lower().strip()
        if domain_lower and domain_lower not in existing_domains:
            new_domains.append({
                'domain': domain_lower,
                'source': source,
                'notes': f'Discovered via {source}'
            })
            existing_domains.add(domain_lower)
    
    # Append to file
    file_exists = output_path.exists()
    with open(output_path, 'a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['domain', 'source', 'notes'])
        if not file_exists:
            writer.writeheader()
        writer.writerows(new_domains)
    
    print(f"\n✅ Saved {len(new_domains)} new domains to {output_file}")
    print(f"   Total unique domains in file: {len(existing_domains) + len(new_domains)}")
    
    return len(new_domains)


def main():
    """Main discovery function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Discover domains from various sources")
    parser.add_argument("--method", choices=["search", "file", "reddit", "all"], 
                       default="all", help="Discovery method")
    parser.add_argument("--query", type=str, 
                       default="deepfake deepnude nudify undress ai porn",
                       help="Search query")
    parser.add_argument("--file", type=str, help="Path to domain list file")
    parser.add_argument("--output", type=str, default="domains.csv",
                       help="Output CSV file")
    parser.add_argument("--limit", type=int, default=100,
                       help="Limit number of results")
    
    args = parser.parse_args()
    
    all_domains = set()
    
    print("🔍 Starting domain discovery...")
    print("=" * 60)
    
    if args.method in ["search", "all"]:
        print("\n1. Searching web...")
        search_domains = discover_from_google_search(args.query, args.limit)
        all_domains.update(search_domains)
    
    if args.method in ["file", "all"]:
        if args.file:
            print(f"\n2. Reading from file: {args.file}")
            file_domains = discover_from_file(args.file)
            all_domains.update(file_domains)
        else:
            print("\n2. Skipping file discovery (no --file specified)")
    
    if args.method in ["reddit", "all"]:
        print("\n3. Searching Reddit...")
        reddit_queries = ["deepfake", "deepnude", "nudify", "undress ai"]
        reddit_domains = discover_from_reddit(reddit_queries, args.limit)
        all_domains.update(reddit_domains)
    
    print("\n" + "=" * 60)
    print(f"📊 Total unique domains discovered: {len(all_domains)}")
    
    if all_domains:
        # Save to CSV
        save_domains(list(all_domains), args.output, source=args.method)
        
        print(f"\n💡 Next steps:")
        print(f"   1. Review domains in data/input/{args.output}")
        print(f"   2. Remove any false positives")
        print(f"   3. Run: python scripts/enrich_domains.py --csv data/input/{args.output}")
    else:
        print("\n⚠️  No domains discovered. Try different search terms or methods.")


if __name__ == "__main__":
    main()


