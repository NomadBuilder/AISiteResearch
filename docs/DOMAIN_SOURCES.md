# Domain Discovery Sources

This document outlines various methods to discover and expand your domain list for NCII infrastructure mapping.

## Current Status
- **Domains in database**: ~100 domains
- **Target**: Expand to 500+ domains for better pattern analysis

## Methods for Domain Discovery

### 1. **Manual Collection from Research Sources**

#### Research Papers & Reports
- Search academic databases (Google Scholar, arXiv) for papers on:
  - Deepfake detection
  - NCII (Non-Consensual Intimate Imagery) research
  - AI-generated content detection
- Look for datasets or appendices that list domains
- Contact researchers who publish on this topic

#### NGO & Activist Lists
- Organizations working on revenge porn/NCI:
  - Cyber Civil Rights Initiative
  - Without My Consent
  - Revenge Porn Helpline
- Check their reports and publications for domain lists

#### Security Research Reports
- Security companies publish reports on:
  - Deepfake sites
  - AI-generated content platforms
  - Malicious AI services
- Examples: Palo Alto Networks, Trend Micro, Kaspersky reports

### 2. **Automated Web Search**

#### Google Custom Search API
```bash
# Requires API key from Google Cloud Console
# Free tier: 100 queries/day
# $5 per 1,000 queries after that
```

#### DuckDuckGo (No API Key Needed)
- Can scrape HTML results (respects privacy)
- Limited to ~50 results per query
- Multiple queries needed for large lists

#### Search Queries to Try:
- "deepfake site:reddit.com"
- "deepnude alternative"
- "undress ai" site:github.com
- "nudify online"
- "ai porn generator"
- "deepfake porn sites"

### 3. **Reddit & Social Media**

#### Reddit Sources
- r/deepfakes (check comments/links)
- r/onions (for .onion domains)
- r/illegallifeprotips (may mention sites)
- Use Pushshift API to search comments

#### Twitter/X
- Search hashtags: #deepfake #deepnude #nudify
- Look for links in tweets
- Use Twitter API (requires API key)

#### Telegram Channels
- Many sites advertise on Telegram
- Search public channels for links

### 4. **Public Domain Lists**

#### GitHub Repositories
- Search for "deepfake sites list"
- "ncii domains"
- "ai porn domains"
- Some researchers publish lists

#### Pastebin & Similar Sites
- Sites often share domain lists on paste sites
- Search for pastebin links in forums

### 5. **Security APIs**

#### urlscan.io
- Free tier: 10,000 searches/month
- Search for: "deepfake", "deepnude", "nudify"
- Extract domains from scan results

#### Shodan
- Search for specific technologies
- "X-Powered-By: WordPress" + "deepfake" in title
- Requires API key ($49/month)

#### VirusTotal
- Search for domains flagged for malicious content
- Free tier: 4 requests/minute
- Can search by tags/categories

### 6. **DNS Enumeration**

#### Subdomain Discovery
- If you find one domain, discover subdomains:
  - `subdomain.example.com`
  - `www.example.com`
  - `api.example.com`

#### Reverse DNS Lookup
- Find domains on same IP
- May reveal related sites

### 7. **Manual Collection Methods**

#### Browser Extension
- Create extension to collect domains from:
  - Browser history
  - Links on pages
  - Reddit/Twitter mentions

#### Web Scraping
- Scrape domain lists from:
  - Forum posts
  - Blog articles
  - Comment sections

## Recommended Approach

### Phase 1: Quick Wins (Get to 200-300 domains)
1. **Reddit search** (free, fast)
   ```bash
   python scripts/discover_domains.py --method reddit --limit 200
   ```

2. **File import** - If you have any existing lists
   ```bash
   python scripts/discover_domains.py --method file --file your_list.txt
   ```

3. **Web search** (limited but free)
   ```bash
   python scripts/discover_domains.py --method search --query "deepfake sites"
   ```

### Phase 2: Scale Up (Get to 500+ domains)
1. **Google Custom Search API** ($5 for 1,000 queries)
   - Most comprehensive results
   - High quality domains

2. **urlscan.io API** (free tier: 10k/month)
   - Search for specific patterns
   - Get domains from scan results

3. **Manual research** - Compile from papers/reports

### Phase 3: Maintain & Expand
1. **Ongoing monitoring**
   - Set up alerts for new domains
   - Monitor forums/Reddit for mentions
   - Track new registrations (via WHOIS monitoring)

2. **Community contributions**
   - Accept submissions
   - Collaborate with researchers

## Using the Discovery Script

```bash
# Install required dependencies
pip install beautifulsoup4 requests

# Discover from Reddit (free, no API key)
python scripts/discover_domains.py --method reddit --limit 200

# Discover from web search
python scripts/discover_domains.py --method search --query "deepfake deepnude"

# Discover from a text file
python scripts/discover_domains.py --method file --file my_domains.txt

# Combine all methods
python scripts/discover_domains.py --method all --limit 100

# Output will be saved to data/input/domains.csv
```

## Next Steps After Discovery

1. **Review domains** - Remove false positives
2. **Deduplicate** - Script handles this automatically
3. **Enrich domains**:
   ```bash
   python scripts/enrich_domains.py --csv data/input/domains.csv
   ```
4. **Analyze patterns** - Check Analysis tab in web UI

## Important Notes

⚠️ **Ethical Considerations**:
- Only collect publicly available domain information
- Do not scrape private/authenticated content
- Respect robots.txt and rate limits
- Focus on domains already publicly known

⚠️ **Legal Considerations**:
- Ensure you have right to collect this data
- Respect terms of service of APIs
- Consider GDPR/privacy implications if storing personal data

⚠️ **Rate Limiting**:
- Don't hammer APIs/sites
- Use delays between requests
- Respect rate limits to avoid IP bans

## Additional Resources

- **Google Custom Search API**: https://developers.google.com/custom-search
- **urlscan.io API**: https://urlscan.io/docs/api/
- **Pushshift Reddit API**: https://github.com/pushshift/api
- **Shodan API**: https://www.shodan.io/api


