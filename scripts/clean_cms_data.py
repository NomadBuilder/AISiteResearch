#!/usr/bin/env python3
"""
Clean incorrect CMS values from existing database records.
Removes non-CMS technologies (Bootstrap, jQuery, Nginx, Cloudflare, etc.) from CMS field.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.postgres_client import PostgresClient
from src.database.neo4j_client import Neo4jClient
from dotenv import load_dotenv

load_dotenv()

# Valid CMS platforms (whitelist)
VALID_CMS_PLATFORMS = [
    "wordpress", "joomla", "drupal", "shopify", "squarespace", "wix",
    "magento", "woocommerce", "prestashop", "opencart", "bigcommerce",
    "ghost", "grav", "strapi", "contentful", "craft cms", "expressionengine",
    "typo3", "concrete5", "silverstripe", "sitecore", "umbraco", "kentico",
    "pimcore", "aem", "adobe experience manager", "liferay", "sharepoint",
    "dnn", "dotnetnuke", "plone", "modx", "processwire", "textpattern",
    "bolt", "pico", "kirby", "statamic", "wagtail", "django cms", "weebly",
    "carrd", "webflow", "tumblr", "medium", "blogger", "blogspot"
]

# Technologies that are NOT CMS (should be removed from CMS field)
NOT_CMS = [
    "bootstrap", "jquery", "nginx", "apache", "cloudflare", "react", "vue",
    "angular", "node.js", "php", "python", "ruby", "java", "javascript",
    "typescript", "css", "html", "sass", "less", "webpack", "gulp",
    "babel", "express", "django", "rails", "laravel", "flask", "spring",
    "asp.net", "symfony", "fastly", "cloudfront", "akamai", "maxcdn",
    "keycdn", "bunnycdn", "stackpath", "sucuri", "incapsula", "imperva",
    # Additional non-CMS technologies found in data
    "amazon s3", "s3", "jsdelivr", "polyfill", "fingerprintjs", "next.js",
    "netlify", "statcounter", "google cloud", "amazon web services", "aws",
    "iconicons", "cloud storage", "cdn", "hosting", "platform", "analytics",
    "counter", "icons", "font awesome", "fontawesome"
]


def is_valid_cms(cms_value):
    """Check if CMS value is a valid CMS platform."""
    if not cms_value:
        return True  # None/empty is valid
    
    cms_lower = str(cms_value).lower()
    
    # Check if it's explicitly NOT a CMS
    if any(not_cms in cms_lower for not_cms in NOT_CMS):
        return False
    
    # Check if it's a valid CMS
    if any(valid_cms in cms_lower for valid_cms in VALID_CMS_PLATFORMS):
        return True
    
    # If not in either list, be conservative and don't remove it
    # (might be a valid CMS we haven't added to the list)
    return True


def clean_postgres_cms_data():
    """Clean incorrect CMS values from PostgreSQL."""
    postgres = PostgresClient()
    
    try:
        cursor = postgres.conn.cursor()
        
        # Get all domains with CMS values
        cursor.execute("""
            SELECT de.id, de.domain_id, de.cms, d.domain
            FROM domain_enrichment de
            JOIN domains d ON de.domain_id = d.id
            WHERE de.cms IS NOT NULL AND de.cms != ''
        """)
        
        rows = cursor.fetchall()
        print(f"Found {len(rows)} domains with CMS values")
        
        cleaned_count = 0
        invalid_cms_values = {}
        
        for row in rows:
            enrichment_id, domain_id, cms_value, domain = row
            
            if not is_valid_cms(cms_value):
                invalid_cms_values[cms_value] = invalid_cms_values.get(cms_value, 0) + 1
                
                # Clear the CMS value
                cursor.execute("""
                    UPDATE domain_enrichment
                    SET cms = NULL
                    WHERE id = %s
                """, (enrichment_id,))
                
                cleaned_count += 1
                print(f"  ✗ Removed invalid CMS '{cms_value}' from {domain}")
        
        postgres.conn.commit()
        cursor.close()
        
        print(f"\n✅ PostgreSQL cleanup complete!")
        print(f"   - Cleaned {cleaned_count} domains")
        print(f"   - Invalid CMS values found:")
        for cms_val, count in sorted(invalid_cms_values.items(), key=lambda x: x[1], reverse=True):
            print(f"     • {cms_val}: {count} domains")
        
        return cleaned_count
        
    except Exception as e:
        print(f"❌ Error cleaning PostgreSQL: {e}")
        import traceback
        traceback.print_exc()
        return 0
    finally:
        postgres.close()


def clean_neo4j_cms_data():
    """Clean incorrect CMS values from Neo4j."""
    neo4j = Neo4jClient()
    
    try:
        # Get all CMS nodes - need to fetch all records first
        query = "MATCH (c:CMS) RETURN c.name as name"
        
        with neo4j.driver.session() as session:
            result = session.run(query)
            cms_nodes = []
            for record in result:
                cms_name = record.get("name")
                if cms_name:
                    cms_nodes.append(cms_name)
        
        print(f"\nFound {len(cms_nodes)} CMS nodes in Neo4j")
        
        cleaned_count = 0
        nodes_to_delete = []
        
        for cms_name in cms_nodes:
            if not is_valid_cms(cms_name):
                nodes_to_delete.append(cms_name)
                cleaned_count += 1
                print(f"  ✗ Will delete invalid CMS node: {cms_name}")
        
        # Delete invalid CMS nodes and their relationships
        with neo4j.driver.session() as session:
            for cms_name in nodes_to_delete:
                # Delete relationships first
                delete_rel_query = """
                MATCH (d:Domain)-[r:USES_CMS]->(c:CMS {name: $cms_name})
                DELETE r
                """
                session.run(delete_rel_query, {"cms_name": cms_name})
                
                # Delete the CMS node
                delete_node_query = """
                MATCH (c:CMS {name: $cms_name})
                DELETE c
                """
                session.run(delete_node_query, {"cms_name": cms_name})
            
            session.close()
        
        print(f"\n✅ Neo4j cleanup complete!")
        print(f"   - Deleted {cleaned_count} invalid CMS nodes")
        
        return cleaned_count
        
    except Exception as e:
        print(f"❌ Error cleaning Neo4j: {e}")
        import traceback
        traceback.print_exc()
        return 0
    finally:
        neo4j.close()


def main():
    """Main cleanup function."""
    print("🧹 Starting CMS data cleanup...")
    print("=" * 60)
    
    # Clean PostgreSQL
    postgres_cleaned = clean_postgres_cms_data()
    
    # Clean Neo4j
    neo4j_cleaned = clean_neo4j_cms_data()
    
    print("\n" + "=" * 60)
    print(f"✅ Cleanup complete!")
    print(f"   - PostgreSQL: {postgres_cleaned} domains cleaned")
    print(f"   - Neo4j: {neo4j_cleaned} CMS nodes deleted")
    print(f"\n💡 Tip: Re-enrich domains to detect correct CMS values if needed")


if __name__ == "__main__":
    main()

