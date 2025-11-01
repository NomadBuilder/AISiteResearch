#!/usr/bin/env python3
"""Fix all VARCHAR columns to TEXT in Render PostgreSQL database."""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.postgres_client import PostgresClient

def fix_all_columns_to_text():
    """Alter table columns from VARCHAR to TEXT to prevent truncation."""
    # Set Render PostgreSQL connection
    if not os.getenv("POSTGRES_HOST"):
        os.environ["POSTGRES_HOST"] = "dpg-d42kod95pdvs73d5nt30-a.oregon-postgres.render.com"
        os.environ["POSTGRES_PORT"] = "5432"
        os.environ["POSTGRES_USER"] = "ncii_user"
        os.environ["POSTGRES_PASSWORD"] = "Zu1uJcsJjAfN3ZAx4N9aN9vjwFqKrj91"
        os.environ["POSTGRES_DB"] = "ncii"
    
    print("🔧 Converting VARCHAR columns to TEXT in Render database...")
    
    try:
        postgres = PostgresClient()
        cursor = postgres.conn.cursor()
        
        # Alter columns to TEXT (unlimited length)
        columns_to_fix = [
            "host_name",
            "isp",
            "cdn",
            "cms",
            "payment_processor",
            "registrar",
            "expiration_date",
            "updated_date",
            "whois_status",
            "web_server",
        ]
        
        for col_name in columns_to_fix:
            try:
                cursor.execute(f"ALTER TABLE domain_enrichment ALTER COLUMN {col_name} TYPE TEXT")
                print(f"✅ Updated {col_name} column to TEXT")
            except Exception as e:
                print(f"⚠️  {col_name} column: {e}")
        
        postgres.conn.commit()
        cursor.close()
        postgres.close()
        
        print("\n✅ All columns converted to TEXT!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    fix_all_columns_to_text()

