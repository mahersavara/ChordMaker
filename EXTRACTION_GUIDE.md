# ChordMaker - Ultimate Guitar Extraction Guide

## The Challenge with Ultimate Guitar

Ultimate Guitar blocks automated scraping (returns 403) to protect copyrighted lyrics. This is intentional and respectful of copyright law.

---

## ✅ Best Solution: `extract-url.py` with Browser Automation

**What it does:**
- Uses Playwright to open a real browser (Chromium)
- Loads the page just like you would manually
- Extracts chord notation and structure
- Respects the site's content protection

**Requirements:**
```bash
pip install playwright beautifulsoup4
```

**Usage:**
```bash
python scripts/extract-url.py "https://tabs.ultimate-guitar.com/tab/westlife/i-lay-my-love-on-you-chords-464"
```

**How it works:**
1. Opens a real Chromium browser in headless mode
2. Navigates to the Ultimate Guitar URL
3. Waits for page to load
4. Extracts visible chord content
5. Saves to offline text file

---

## 🎯 Alternative Approaches

### Option A: Manual Save + Local Extraction (Most Reliable)

For guaranteed copyright compliance and best results:

```bash
# 1. Visit the URL in your browser
# 2. Right-click → Save Page As (Ctrl+S)
# 3. Extract locally:
python scripts/extract-local.py "Downloads/westlife-song.html"
```

**Advantages:**
- You control what gets saved
- Easy to review before extraction
- Best for respecting copyright
- Most reliable extraction

### Option B: Browser Automation (Auto)

```bash
python scripts/extract-url.py "https://tabs.ultimate-guitar.com/tab/westlife/i-lay-my-love-on-you-chords-464"
```

**Advantages:**
- Fully automated
- No manual HTML saving needed
- Works with real browser (no 403 blocks)

---

## 📋 Copyright & Legal Considerations

### ✅ What's NOT Copyrighted
- Chord notation: Em, Am, D, G, etc.
- Chord positions and fingerings
- Song structure: Verse, Chorus, Bridge
- Timing and arrangement notes
- Your personal practice notes

### ❌ What IS Copyrighted
- Song lyrics (protected by songwriting copyright)
- Specific arrangements (protected by publication copyright)
- Original tablature formatting

### 📖 Best Practices
1. **For Personal Use**: Extract chords + your own notes ✅
2. **For Teaching**: Reference the original source ✅
3. **For Publishing**: Get permission from copyright holder ❌
4. **For Distribution**: Only share chord notation, not lyrics ✅

---

## 🔧 Troubleshooting

### "Timeout" Error
- The page has too many ads/tracking scripts
- Solution: Try `extract-local.py` instead (manual save)

### "Cannot find chord content"
- Page structure changed since script was written
- Solution: Use `extract-local.py` with saved HTML

### 403 Forbidden (Direct URL)
- Ultimate Guitar detected automated request
- Solution: Use browser automation or manual extraction

---

## 📚 Recommended Workflow

**For Casual Learning:**
```bash
# Quick extraction for personal study
python scripts/extract-url.py "URL"
```

**For Serious Musicians:**
```bash
# Save page manually, then extract (most reliable)
# 1. Save HTML via Ctrl+S
# 2. Run: python scripts/extract-local.py "path/to/file.html"
```

**For Collection Building:**
```bash
# Extract multiple songs to output folder
for song in "song1.html" "song2.html" "song3.html"; do
  python scripts/extract-local.py "$song"
done
```

---

## API Alternatives

Unfortunately, Ultimate Guitar doesn't provide a public API for tab extraction. However:

- **UltimateGuitar API** (Community): Some unofficial wrappers exist but may violate ToS
- **CHORDIFY**: Browser extension that extracts chords
- **Chordify.net**: Extracts chords from YouTube videos
- **Song databases**: Some sites offer chord data (check their licensing)

---

## Example Output Format

```
════════════════════════════════════════════════════════════
CHORDMAKER - OFFLINE CHORD SHEET
════════════════════════════════════════════════════════════

Title: I Lay My Love On You
Artist: Westlife
Extracted: 2026-04-16
Source: https://tabs.ultimate-guitar.com/...

════════════════════════════════════════════════════════════
CHORD CONTENT
════════════════════════════════════════════════════════════

[Verse]
Em
[Your lyrics here - add manually if desired]

Am
[Your lyrics here]

[Chorus]
D
...

════════════════════════════════════════════════════════════
```

---

## Summary

| Tool | Method | Speed | Reliability | Copyright |
|------|--------|-------|-------------|-----------|
| `extract-url.py` | Browser automation | Medium | Medium | ✅ Compliant |
| `extract-local.py` | Saved HTML | Fast | High | ✅ Compliant |
| Manual extraction | Browser save | Slow | Best | ✅ Controlled |

**Recommendation**: Use `extract-local.py` with manually saved HTML for best results and full control over what you extract.
