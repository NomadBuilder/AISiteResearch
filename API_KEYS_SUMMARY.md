# API Keys Summary

## ✅ **REQUIRED: NONE**

The tool works completely **without any API keys** using free alternatives.

---

## 📋 Optional API Keys (In Order of Recommendation)

### 1. **BuiltWith API** ⭐ Best Free Option
- **Key Name**: `BUILTWITH_API_KEY`
- **Free Tier**: ✅ **10 requests/day** (signup required)
- **Purpose**: Technology stack detection (CMS, frameworks, analytics)
- **Get Key**: https://api.builtwith.com/
- **Why First**: Free tier available, comprehensive detection

---

### 2. **IPLocate.io**
- **Key Name**: `IPLOCATE_API_KEY`
- **Free Tier**: ✅ **1,000 requests/day** (works without key!)
- **Purpose**: IP → Location, ASN, ISP, Hosting provider
- **Get Key**: https://www.iplocate.io/ (optional - already works without key)
- **Why**: Already functional without key, but key gives higher limits

---

### 3. **WhatCMS**
- **Key Name**: `WHATCMS_API_KEY`
- **Free Tier**: ⚠️ Limited free lookups
- **Purpose**: CMS detection
- **Get Key**: https://whatcms.org/API
- **Why**: Basic CMS detection, but BuiltWith is better if you can get it

---

### 4. **Wappalyzer API** 💰 Paid Only
- **Key Name**: `WAPPALYZER_API_KEY`
- **Free Tier**: ❌ **Paid only** ($99+/month)
- **Purpose**: Most comprehensive tech stack detection
- **Get Key**: https://www.wappalyzer.com/pricing/
- **Why**: Best results, but expensive

---

### 5. **Shodan API**
- **Key Name**: `SHODAN_API_KEY`
- **Free Tier**: ✅ **100 requests/month**
- **Purpose**: Advanced infrastructure intelligence, vulnerabilities
- **Get Key**: https://account.shodan.io/register
- **Why**: Useful for advanced infrastructure analysis

---

## 🎯 Recommended Setup

### Minimal (No Keys Needed)
```
✅ Use default free APIs
✅ Works out of the box
⚠️ Rate limits: 45 IP lookups/minute
```

### Best Free Setup
```
1. Get BuiltWith API key (10/day free) ⭐
2. IPLocate works without key (1,000/day)
3. Header-based CMS detection (unlimited)
```

### Production Setup
```
1. BuiltWith API key (or upgrade to paid)
2. IPLocate API key (for higher limits)
3. Wappalyzer API key (if budget allows)
```

---

## 📝 Quick Setup

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Add keys to `.env`:
```bash
# Optional - only add keys you have
BUILTWITH_API_KEY=your_key_here
IPLOCATE_API_KEY=your_key_here
WHATCMS_API_KEY=your_key_here
WAPPALYZER_API_KEY=your_key_here
SHODAN_API_KEY=your_key_here
```

3. The tool automatically uses keys if available, falls back if not.

---

## 🔑 Key Priority Order

**For best results with free options:**
1. **BuiltWith** (10/day free) - Get this first!
2. **IPLocate** (already works, key optional)
3. **Shodan** (100/month free) - For advanced analysis

**Skip these unless you have budget:**
- Wappalyzer (paid only)
- WhatCMS (BuiltWith is better)

---

## 📊 Comparison

| API | Free Tier | Best For | Priority |
|-----|-----------|----------|----------|
| BuiltWith | ✅ 10/day | Tech stack | ⭐⭐⭐ High |
| IPLocate | ✅ 1,000/day | IP location | ⭐⭐ Medium |
| Shodan | ✅ 100/month | Infrastructure | ⭐⭐ Medium |
| WhatCMS | ⚠️ Limited | CMS only | ⭐ Low |
| Wappalyzer | ❌ Paid | Everything | 💰 If budget |

---

**Bottom Line**: Start with **BuiltWith** (free tier), everything else is optional!

