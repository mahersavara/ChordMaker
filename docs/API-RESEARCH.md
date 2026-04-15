# ChordMaker - API Research & Findings

## Internet API Research Summary

### Investigation Results

**Question:** Does Ultimate Guitar have a public API?

**Answer:** No public official API, but a reverse-engineered mobile API exists.

### What We Discovered

1. **Official REST API** ❌
   - No public REST API endpoints
   - All patterns (`/api/v1/tabs/ID`, `/api/v2/tabs/ID`, etc.) return 403 Forbidden
   - Not documented or supported by Ultimate Guitar

2. **Mobile API** ⚠️
   - Undocumented mobile API exists (used by the official app)
   - Reverse-engineered by developers (see: Pilfer/ultimate-guitar-scraper on GitHub)
   - Also protected by Cloudflare - returns 403 Forbidden without proper authentication
   - Requires specific headers and authentication tokens not publicly available

3. **Web Scraping**
   - Content is server-side rendered (SSR) - embedded directly in HTML
   - Cloudflare blocks headless browsers (Playwright, Puppeteer) with security verification
   - Real browsers load the content successfully
   - Protection: User-Agent detection + Cloudflare challenge pages

### GitHub Projects Found

These projects use various approaches:

| Project | Language | Approach | Status |
|---------|----------|----------|--------|
| **Pilfer/ultimate-guitar-scraper** | Go | Mobile API reverse-engineering | Active (121★) |
| **joncardasis/ultimate-api** | Python | HTML scraping with Flask | Active (113★) |
| **seanfhear/tab-scraper** | Python | Web scraping | Active |
| **hedwiggggg/ugrip** | JavaScript | HTML + PDF generation | Active |
| **fridasor/tabscraper** | Python | Web scraping CLI | Recently updated |

### Key Insight from Research

From Pilfer/ultimate-guitar-scraper documentation:
> "Fun fact: on mobile, UG doesn't have a 'list tabs by artist name/id' endpoint. They just load ~7 pages."

This confirms that even the mobile API has limitations and is not fully documented.

### Why Direct URL Extraction is Challenging

1. **Cloudflare Protection**
   - Detects automated requests (403 Forbidden)
   - Detects headless browsers (serves challenge page instead of content)
   - Blocks API access without proper headers

2. **No Public API**
   - Ultimate Guitar doesn't offer official API access
   - All scraping is reverse-engineering or HTML parsing

3. **Rate Limiting**
   - Site protects against aggressive scraping
   - Mobile API requires authentication

### Our Solution: Local HTML Extraction

**The most reliable and maintainable approach is:**

1. Save the webpage using your browser (File > Save Page As)
2. Run our `extract-local.py` script on the saved HTML
3. Get clean, formatted chord sheets

**Why this works:**
- Bypasses Cloudflare (you use your real browser)
- No API authentication needed
- No headless browser detection
- Fast and reliable
- Works offline

### Files in This Investigation

- `extract-url.py` - Attempted Playwright browser automation (blocked by Cloudflare)
- `extract-mobile-api.py` - Attempted mobile API access (also blocked)
- `extract-local.py` - ✅ **Recommended & Working** - Local HTML extraction

### Conclusion

**Direct live URL extraction is not feasible** due to Cloudflare and API restrictions. However, **local HTML extraction is a perfect solution** that's already fully implemented and working.

For production use, consider:
1. User saves webpage → `extract-local.py` ✅ Recommended
2. Direct URL with saved session cookies (not implemented)
3. Integrate with existing projects like Pilfer/ultimate-guitar-scraper (Go-based)

---

*Last Updated: 2026-04-16*
*Research Scope: Ultimate Guitar API availability and accessibility*
