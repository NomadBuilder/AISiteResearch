#!/usr/bin/env python3
"""Fix all column sizes in Render PostgreSQL database."""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.postgres_client import PostgresClient

def fix_all_column_sizes():
    """Alter table columns to increase size limits."""
    # Set Render PostgreSQL connection
    if not os.getenv("POSTGRES_HOST"):
        os.environ["POSTGRES_HOST"] = "dpg-d42kod95pdvs73d5nt30-a.oregon-postgres.render.com"
        os.environ["POSTGRES_PORT"] = "5432"
        os.environ["POSTGRES_USER"] = "ncii_user"
        os.environ["POSTGRES_PASSWORD"] = "Zu1uJcsJjAfN3ZAx4N9aN9vjwFqKrj91"
        os.environ["POSTGRES_DB"] = "ncii"
    
    print("🔧 Fixing all column sizes in Render database...")
    
    try:
        postgres = PostgresClient()
        cursor = postgres.conn.cursor()
        
        # Alter columns to increase size
        columns_to_fix = [
            ("cdn", "VARCHAR(255)"),
            ("cms", "VARCHAR(255)"),
            ("expiration_date", "VARCHAR(255)"),
            ("updated_date", "VARCHAR(255)"),
        ]
        
        for col_name, col_type in columns_to_fix:
            try:
                cursor.execute(f"ALTER TABLE domain_enrichment ALTER COLUMN {col_name} TYPE {col_type}")
                print(f"✅ Updated {col_name} column to {col_type}")
            except Exception as e:
                print(f"⚠️  {col_name} column: {e}")
        
        postgres.conn.commit()
        cursor.close()
        postgres.close()
        
        print("\n✅ All column sizes fixed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    fix_all_column_sizes()

