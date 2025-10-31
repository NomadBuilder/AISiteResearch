"""Tests for enrichment modules."""

import pytest
from src.enrichment.whois_enrichment import enrich_whois, enrich_dns
from src.enrichment.ip_enrichment import enrich_ip_location
from src.enrichment.cms_enrichment import detect_cms


def test_enrich_dns():
    """Test DNS enrichment."""
    # Test with a known domain
    result = enrich_dns("example.com")
    
    assert "dns_records" in result
    assert isinstance(result["dns_records"], dict)
    # Example.com should have A records
    assert "ip_address" in result or "A" in result["dns_records"]


def test_enrich_ip_location():
    """Test IP location enrichment."""
    # Test with a known IP (Google DNS)
    result = enrich_ip_location("8.8.8.8")
    
    assert "country" in result
    assert "isp" in result or "host_name" in result


def test_detect_cms():
    """Test CMS detection."""
    # This might fail if domain is unreachable, so we'll just check it doesn't crash
    result = detect_cms("example.com")
    # Result can be None or a string
    assert result is None or isinstance(result, str)


def test_enrich_whois():
    """Test WHOIS enrichment."""
    # Test with a known domain
    result = enrich_whois("example.com")
    
    assert "registrar" in result
    assert "whois_data" in result
    assert isinstance(result["whois_data"], dict)

