"""Database migration script to add new enrichment columns."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.postgres_client import PostgresClient


def migrate_database():
    """Add new columns to existing database."""
    pg = PostgresClient()
    
    try:
        cursor = pg.conn.cursor()
        
        # Add new columns (using IF NOT EXISTS via ALTER TABLE)
        migrations = [
            "ALTER TABLE domain_enrichment ADD COLUMN IF NOT EXISTS ip_addresses JSONB",
            "ALTER TABLE domain_enrichment ADD COLUMN IF NOT EXISTS ipv6_addresses JSONB",
            "ALTER TABLE domain_enrichment ADD COLUMN IF NOT EXISTS expiration_date VARCHAR(100)",
            "ALTER TABLE domain_enrichment ADD COLUMN IF NOT EXISTS updated_date VARCHAR(100)",
            "ALTER TABLE domain_enrichment ADD COLUMN IF NOT EXISTS name_servers JSONB",
            "ALTER TABLE domain_enrichment ADD COLUMN IF NOT EXISTS mx_records JSONB",
            "ALTER TABLE domain_enrichment ADD COLUMN IF NOT EXISTS whois_status VARCHAR(255)",
            "ALTER TABLE domain_enrichment ADD COLUMN IF NOT EXISTS web_server VARCHAR(255)",
            "ALTER TABLE domain_enrichment ADD COLUMN IF NOT EXISTS frameworks JSONB",
            "ALTER TABLE domain_enrichment ADD COLUMN IF NOT EXISTS analytics JSONB",
            "ALTER TABLE domain_enrichment ADD COLUMN IF NOT EXISTS languages JSONB",
            "ALTER TABLE domain_enrichment ADD COLUMN IF NOT EXISTS tech_stack JSONB",
            "ALTER TABLE domain_enrichment ADD COLUMN IF NOT EXISTS http_headers JSONB",
            "ALTER TABLE domain_enrichment ADD COLUMN IF NOT EXISTS ssl_info JSONB",
            "ALTER TABLE domain_enrichment ALTER COLUMN payment_processor TYPE VARCHAR(255)",
        ]
        
        print("Running database migrations...")
        for i, migration in enumerate(migrations, 1):
            try:
                cursor.execute(migration)
                print(f"  ✓ Migration {i}/{len(migrations)}")
            except Exception as e:
                print(f"  ⚠️  Migration {i} skipped (may already exist): {e}")
        
        pg.conn.commit()
        print("\n✅ Database migration complete!")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        pg.conn.rollback()
        raise
    finally:
        cursor.close()
        pg.close()


if __name__ == "__main__":
    migrate_database()


