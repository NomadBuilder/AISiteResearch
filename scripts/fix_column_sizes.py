#!/usr/bin/env python3
"""Fix column sizes in Render PostgreSQL database."""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.postgres_client import PostgresClient

def fix_column_sizes():
    """Alter table columns to increase size limits."""
    # Set Render PostgreSQL connection
    if not os.getenv("POSTGRES_HOST"):
        os.environ["POSTGRES_HOST"] = "dpg-d42kod95pdvs73d5nt30-a.oregon-postgres.render.com"
        os.environ["POSTGRES_PORT"] = "5432"
        os.environ["POSTGRES_USER"] = "ncii_user"
        os.environ["POSTGRES_PASSWORD"] = "Zu1uJcsJjAfN3ZAx4N9aN9vjwFqKrj91"
        os.environ["POSTGRES_DB"] = "ncii"
    
    print("🔧 Fixing column sizes in Render database...")
    
    try:
        postgres = PostgresClient()
        cursor = postgres.conn.cursor()
        
        # Alter columns to increase size
        try:
            cursor.execute("ALTER TABLE domain_enrichment ALTER COLUMN cdn TYPE VARCHAR(255)")
            print("✅ Updated cdn column to VARCHAR(255)")
        except Exception as e:
            print(f"⚠️  cdn column: {e}")
        
        try:
            cursor.execute("ALTER TABLE domain_enrichment ALTER COLUMN cms TYPE VARCHAR(255)")
            print("✅ Updated cms column to VARCHAR(255)")
        except Exception as e:
            print(f"⚠️  cms column: {e}")
        
        postgres.conn.commit()
        cursor.close()
        postgres.close()
        
        print("\n✅ Column sizes fixed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    fix_column_sizes()

