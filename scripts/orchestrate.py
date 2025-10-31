"""Prefect orchestration script for running enrichment pipeline."""

import sys
from pathlib import Path
from prefect import flow, task
from prefect.tasks import task_inputs
import time

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.enrich_domains import process_domains
from scripts.export_data import export_to_csv, export_to_json


@task(name="enrich-domains", log_prints=True)
def enrich_domains_task(csv_path: str, limit: int = None):
    """Task to enrich domains from CSV."""
    print(f"Starting enrichment for {csv_path}")
    process_domains(csv_path, limit=limit)
    return True


@task(name="export-csv", log_prints=True)
def export_csv_task():
    """Task to export data to CSV."""
    print("Exporting data to CSV...")
    export_to_csv()
    return True


@task(name="export-json", log_prints=True)
def export_json_task():
    """Task to export data to JSON."""
    print("Exporting data to JSON...")
    export_to_json()
    return True


@flow(name="ncii-infrastructure-enrichment", log_prints=True)
def enrichment_flow(csv_path: str = "data/input/domains.csv", limit: int = None, export_format: str = "both"):
    """
    Main Prefect flow for enriching domains and exporting results.
    
    Args:
        csv_path: Path to CSV file with domains
        limit: Limit number of domains to process (for testing)
        export_format: Export format - "csv", "json", or "both"
    """
    print(f"Starting NCII Infrastructure Enrichment Flow")
    print(f"CSV Path: {csv_path}")
    print(f"Limit: {limit if limit else 'None (process all)'}")
    print(f"Export Format: {export_format}")
    
    # Step 1: Enrich domains
    enrich_result = enrich_domains_task(csv_path, limit=limit)
    
    if not enrich_result:
        print("Enrichment failed, stopping flow")
        return
    
    # Step 2: Export data
    if export_format in ["csv", "both"]:
        export_csv_task()
    
    if export_format in ["json", "both"]:
        export_json_task()
    
    print("✓ Enrichment flow completed successfully")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run enrichment pipeline with Prefect")
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
        help="Limit number of domains to process"
    )
    parser.add_argument(
        "--export",
        type=str,
        choices=["csv", "json", "both"],
        default="both",
        help="Export format"
    )
    
    args = parser.parse_args()
    
    # Run the flow
    enrichment_flow(
        csv_path=args.csv,
        limit=args.limit,
        export_format=args.export
    )

