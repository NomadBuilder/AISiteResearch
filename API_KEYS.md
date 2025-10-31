# API Keys Guide

## Required API Keys: **NONE** ✅

The tool works **without any API keys** using free alternatives and fallbacks.

## Optional API Keys (Recommended for Better Results)

### 1. **IPLocate.io** (IP Location & Hosting)
- **Key**: `IPLOCATE_API_KEY`
- **Purpose**: IP → Location, ASN, ISP, Hosting provider
- **Free Tier**: 1,000 requests/day (no key needed)
- **With Key**: Higher rate limits
- **Get Key**: https://www.iplocate.io/
- **Status**: ✅ Already integrated

**Fallback**: Uses ip-api.com (45 requests/minute, no key needed)

---

### 2. **WhatCMS** (CMS/Technology Detection)
- **Key**: `WHATCMS_API_KEY`
- **Purpose**: Detect CMS and technology stack
- **Free Tier**: Limited free lookups
- **Get Key**: https://whatcms.org/API
- **Status**: ✅ Already integrated

**Fallback**: Uses HTTP header analysis and content scanning

---

### 3. **Wappalyzer API** (Advanced Tech Stack Detection) 🔥
- **Key**: `WAPPALYZER_API_KEY`
- **Purpose**: Comprehensive technology detection (CMS, frameworks, analytics, etc.)
- **Free Tier**: ❌ Paid only (starts at $99/month)
- **Get Key**: https://www.wappalyzer.com/pricing/
- **Status**: ⚠️ Not yet integrated (can be added)

**Alternative Free Options**:
- BuiltWith API (free tier available)
- WhatRuns (browser extension, no API)

---

### 4. **BuiltWith API** (Technology Stack Detection)
- **Key**: `BUILTWITH_API_KEY`
- **Purpose**: Detect technologies, frameworks, CMS, analytics
- **Free Tier**: ✅ 10 requests/day (with signup)
- **Get Key**: https://api.builtwith.com/
- **Status**: ⚠️ Not yet integrated (can be added)

---

### 5. **Shodan API** (Infrastructure Intelligence)
- **Key**: `SHODAN_API_KEY`
- **Purpose**: Comprehensive infrastructure data, vulnerabilities, services
- **Free Tier**: ✅ 100 requests/month
- **Get Key**: https://account.shodan.io/register
- **Status**: ⚠️ Not yet integrated (can be added)

---

## Current Implementation Status

| API | Status | Required? | Free Alternative? |
|-----|--------|-----------|------------------|
| IPLocate.io | ✅ Integrated | No | ✅ ip-api.com |
| WhatCMS | ✅ Integrated | No | ✅ Header analysis |
| Wappalyzer | ❌ Not integrated | No | ⚠️ Paid only |
| BuiltWith | ❌ Not integrated | No | ✅ Free tier |
| Shodan | ❌ Not integrated | No | ✅ Free tier |

## How to Add API Keys

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your keys:
```bash
# Optional API Keys
IPLOCATE_API_KEY=your_key_here
WHATCMS_API_KEY=your_key_here
WAPPALYZER_API_KEY=your_key_here  # If we add support
BUILTWITH_API_KEY=your_key_here    # If we add support
SHODAN_API_KEY=your_key_here       # If we add support
```

3. The tool will automatically use keys if available, fallback if not.

## Recommendations

### For Minimal Setup (No Keys)
- ✅ Use default free APIs (ip-api.com, header analysis)
- ✅ Works out of the box
- ⚠️ Rate limits: 45 IP lookups/minute, basic CMS detection

### For Better Results (Get Free Keys)
1. **BuiltWith** (10/day free) - Best free tech stack detection
2. **IPLocate.io** (1,000/day free) - Already working without key
3. **Shodan** (100/month free) - Advanced infrastructure data

### For Production/Scale (Paid Options)
1. **Wappalyzer API** - Most comprehensive ($99+/month)
2. **BuiltWith Pro** - Good balance ($295/month)
3. **IPLocate.io Pro** - Higher limits

## Rate Limits (Without Keys)

- **ip-api.com**: 45 requests/minute
- **IPLocate.io**: 1,000 requests/day (no key)
- **Header-based CMS detection**: Unlimited (but less accurate)
- **WHOIS/DNS**: Unlimited (local lookups)

The tool handles rate limits gracefully and continues processing even if some APIs fail.

