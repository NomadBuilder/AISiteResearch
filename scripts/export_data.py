"""Export enriched data to CSV or JSON."""

import sys
import os
import json
import pandas as pd
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.postgres_client import PostgresClient


def export_to_csv(output_path: str = None):
    """Export all enriched domains to CSV."""
    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"data/output/enriched_domains_{timestamp}.csv"
    
    postgres = PostgresClient()
    
    try:
        data = postgres.get_all_enriched_domains()
        df = pd.DataFrame(data)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        df.to_csv(output_path, index=False)
        print(f"✓ Exported {len(df)} domains to {output_path}")
    
    finally:
        postgres.close()


def export_to_json(output_path: str = None):
    """Export all enriched domains to JSON."""
    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"data/output/enriched_domains_{timestamp}.json"
    
    postgres = PostgresClient()
    
    try:
        data = postgres.get_all_enriched_domains()
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f"✓ Exported {len(data)} domains to {output_path}")
    
    finally:
        postgres.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Export enriched data")
    parser.add_argument(
        "--format",
        type=str,
        choices=["csv", "json", "both"],
        default="both",
        help="Export format"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output file path (optional)"
    )
    
    args = parser.parse_args()
    
    if args.format in ["csv", "both"]:
        export_to_csv(args.output)
    
    if args.format in ["json", "both"]:
        export_to_json(args.output)

