# Data Enrichment Roadmap

## Currently Collected ✅

### Domain & DNS
- IP addresses (IPv4 & IPv6)
- DNS records (A, AAAA, MX, NS, CNAME)
- Name servers
- WHOIS data (registrar, creation/expiration dates, status)

### Infrastructure
- Hosting provider (ISP, Host name)
- ASN information
- Geographic location (Country)
- CDN detection

### Technology Stack
- CMS platforms
- Web frameworks (JavaScript & general)
- Programming languages
- Analytics tools
- Web servers
- Payment processors
- Advertising platforms
- Database technologies
- Caching solutions
- Security tools

### HTTP/Headers
- Server headers
- Content-Type
- Status codes
- X-Powered-By

---

## High-Value Additions 🎯

### 1. SSL/TLS Certificate Information ⭐⭐⭐
**Status**: Module created, ready to integrate
- Certificate issuer
- Expiration date
- Subject Alternative Names (SANs) - reveals related domains
- Certificate fingerprints
- Certificate chain
- **Value**: Identifies related domains, certificate security issues

### 2. Reverse IP Lookup ⭐⭐⭐
**Status**: Module created, ready to integrate
- Other domains sharing same IP
- Shared hosting detection
- IP reputation scores
- **Value**: Finds connected infrastructure, shared hosting patterns

### 3. Subdomain Enumeration ⭐⭐⭐
**Status**: Module created, ready to integrate
- Discover all subdomains
- Subdomain infrastructure mapping
- **Value**: Complete infrastructure picture, potential vulnerabilities

### 4. DNS Security Records ⭐⭐
**Status**: Module created, ready to integrate
- SPF records (email authentication)
- DMARC records (email security)
- DKIM records (email signing)
- TXT records (various purposes)
- **Value**: Email infrastructure, security posture

### 5. Security Headers Analysis ⭐⭐
**Status**: Module created, ready to integrate
- HSTS (HTTP Strict Transport Security)
- CSP (Content Security Policy)
- X-Frame-Options
- Security score (0-100)
- **Value**: Security posture assessment

### 6. Threat Intelligence ⭐⭐
**Status**: Module created, needs API keys
- Blacklist status (VirusTotal, AbuseIPDB)
- Malware associations
- Phishing database checks
- Threat scores
- **Value**: Risk assessment, reputation tracking

---

## Medium-Value Additions 📊

### 7. Domain History & Reputation
- Historical WHOIS changes
- Domain age analysis
- Previous owners (WHOIS history)
- Suspicious activity indicators
- **APIs**: SecurityTrails, DomainTools (paid)

### 8. Email Addresses
- Extract from WHOIS records
- Contact form discovery
- Privacy policy analysis
- **Value**: Contact information for reporting

### 9. Social Media Links
- Twitter/X profiles
- Facebook pages
- Instagram accounts
- Other platforms
- **Value**: Online presence mapping

### 10. Website Content Analysis
- Page titles
- Meta descriptions
- Language detection
- Content keywords
- **Value**: Content categorization

### 11. Performance Metrics
- Page load times
- Server response times
- SSL handshake times
- **Value**: Infrastructure quality assessment

### 12. Related Domains Discovery
- Similar registrars
- Shared name servers
- Connected infrastructure
- **Value**: Network mapping

---

## Lower Priority / Advanced 🚀

### 13. Port Scanning
- Open ports detection
- Service identification
- **Note**: May be considered aggressive, use carefully

### 14. Website Screenshots
- Visual capture
- Design patterns
- **Value**: Visual identification

### 15. Mobile App Detection
- iOS app store presence
- Android app presence
- **Value**: Mobile infrastructure

### 16. Blockchain Integration
- Cryptocurrency addresses
- Payment wallet detection
- **Value**: Payment infrastructure

### 17. Domain Marketplace Data
- For-sale listings
- Price information
- **Value**: Domain lifecycle tracking

---

## Implementation Priority

**Phase 1 (High Impact, Easy)**:
1. ✅ SSL Certificate Info (module ready)
2. ✅ Reverse IP Lookup (module ready)
3. ✅ Subdomain Enumeration (module ready)
4. ✅ DNS Security Records (module ready)
5. ✅ Security Headers (module ready)

**Phase 2 (Requires API Keys)**:
6. Threat Intelligence (VirusTotal, AbuseIPDB)
7. Domain History (SecurityTrails)

**Phase 3 (Advanced Features)**:
8. Content Analysis
9. Social Media Discovery
10. Performance Metrics

---

## Free vs Paid APIs

### Free APIs Available:
- ✅ DNS queries (dnspython)
- ✅ WHOIS (python-whois)
- ✅ SSL certificates (Python ssl library)
- ✅ IP geolocation (ip-api.com, IPLocate.io)
- ✅ Reverse DNS (dns.reversename)
- ✅ SecurityTrails (limited free tier)
- ✅ VirusTotal (4 requests/minute free)
- ✅ AbuseIPDB (1,000 requests/day free)

### Paid APIs (Optional):
- SecurityTrails (full subdomain enumeration)
- DomainTools (WHOIS history)
- Shodan (infrastructure intelligence)
- Censys (certificate search)

---

## Next Steps

To add these enrichments:

1. **Immediate** (modules already created):
   ```python
   # Add to enrichment_pipeline.py
   from .ssl_enrichment import enrich_ssl_certificate
   from .reverse_ip_enrichment import reverse_ip_lookup
   from .subdomain_enrichment import enrich_subdomains
   from .dns_security_enrichment import enrich_dns_security
   from .security_enrichment import enrich_security_headers
   ```

2. **Update database schema** to store new fields

3. **Update UI** to display new data columns

4. **Add API keys** (optional) for enhanced threat intelligence

