#!/usr/bin/env python3

"""
ChordMaker - Ultimate Guitar Direct URL Extractor
Uses Playwright to automate browser and extract chords directly from URL
No HTML file needed - works with live URLs

Requirements:
  pip install playwright beautifulsoup4

Setup (first time only):
  playwright install chromium

Usage:
  python scripts/extract-url.py "https://tabs.ultimate-guitar.com/tab/artist/song-chords-123"
  python scripts/extract-url.py "https://tabs.ultimate-guitar.com/tab/artist/song" "output/song.txt"
"""

import sys
import os
import re
from datetime import datetime
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
    from bs4 import BeautifulSoup
except ImportError:
    print("❌ Missing required packages!")
    print("Install with: pip install playwright beautifulsoup4")
    print("Then setup: playwright install chromium")
    sys.exit(1)


class URLChordExtractor:
    def __init__(self):
        self.playwright = None
        self.browser = None
        
    def fetch_url(self, url):
        """Fetch URL using Playwright (real browser)"""
        try:
            print(f"🌐 Opening browser to fetch: {url}")
            self.playwright = sync_playwright().start()
            
            # Use chromium for speed
            self.browser = self.playwright.chromium.launch(headless=True)
            page = self.browser.new_page()
            
            # Set a realistic user agent
            page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            # Navigate to URL (domcontentloaded is faster than networkidle)
            print("📄 Loading page...")
            page.goto(url, wait_until='domcontentloaded', timeout=15000)
            
            # Wait for content to load or timeout gracefully
            try:
                page.wait_for_selector('pre, h1', timeout=5000)
            except:
                pass  # Continue anyway - we'll work with what loaded
            
            # Get page content
            html = page.content()
            
            page.close()
            self.browser.close()
            self.playwright.stop()
            
            return html
            
        except Exception as e:
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            raise Exception(f"Failed to fetch page: {str(e)}")

    def extract_from_html(self, html, url):
        """Extract chord content from HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract title
        title = "Unknown"
        title_tag = soup.find('h1')
        if title_tag:
            title = title_tag.get_text(strip=True)
        else:
            meta_title = soup.find('meta', property='og:title')
            if meta_title:
                title = meta_title.get('content', 'Unknown')
        
        # Extract artist from URL or page
        artist = "Unknown"
        artist_match = re.search(r'/tab/([^/]+)/', url)
        if artist_match:
            artist = artist_match.group(1).replace('-', ' ').title()
        
        # Look for artist link on page
        artist_link = soup.find('a', href=re.compile(r'/artist/'))
        if artist_link:
            artist = artist_link.get_text(strip=True)
        
        # Try multiple extraction strategies
        content = ""
        
        # Strategy 1: Look for pre tags with chord content
        pre_tags = soup.find_all('pre')
        for pre in pre_tags:
            pre_content = pre.get_text()
            if any(indicator in pre_content for indicator in ['[', ']', 'Verse', 'Chorus', 'Bridge', 'Em', 'Am', 'D ', 'G ']):
                content = pre_content
                break
        
        # Strategy 2: Look for div with id="tab" or data-tab
        if not content:
            tab_div = soup.find('div', {'id': re.compile('tab', re.I)})
            if tab_div:
                content = tab_div.get_text()
        
        # Strategy 3: Look for sections with common chord progressions
        if not content:
            for section in soup.find_all(['section', 'article', 'div'], class_=re.compile('tab|chord|content', re.I)):
                section_text = section.get_text()
                # Check if it looks like chord content
                if len(section_text) > 300 and any(chord in section_text for chord in ['Verse', 'Chorus', 'Bridge', 'Intro', 'Outro']):
                    content = section_text
                    break
        
        # Strategy 4: Get all text containing chord markers
        if not content:
            all_text = soup.get_text()
            # Extract sections that likely contain chords
            if 'Verse' in all_text or 'Chorus' in all_text:
                # Find the chunk with song structure
                parts = re.split(r'(Verse|Chorus|Bridge|Intro|Outro|Pre-Chorus)', all_text)
                if len(parts) > 1:
                    content = '\n'.join(parts[-20:])  # Last 20 parts to get main content
        
        if not content:
            content = "Could not extract chord content. The page structure may have changed.\n\nTip: Please visit the URL directly for the full chord sheet."
        
        return {
            'title': title.strip(),
            'artist': artist.strip(),
            'url': url,
            'content': content.strip()
        }

    def clean_text(self, text):
        """Clean extracted text"""
        lines = text.split('\n')
        cleaned = []
        prev_empty = False
        
        for line in lines:
            line = line.rstrip()
            if not line:
                if not prev_empty:
                    cleaned.append('')
                prev_empty = True
            else:
                cleaned.append(line)
                prev_empty = False
        
        return '\n'.join(cleaned)

    def format_output(self, data):
        """Format the extracted data for output"""
        output = f"""════════════════════════════════════════════════════════════
CHORDMAKER - OFFLINE CHORD SHEET
════════════════════════════════════════════════════════════

Title: {data['title']}
Artist: {data['artist']}
Extracted: {datetime.now().isoformat()}
Source: {data['url']}

════════════════════════════════════════════════════════════
CHORD CONTENT
════════════════════════════════════════════════════════════

{self.clean_text(data['content'])}

════════════════════════════════════════════════════════════
END OF CHORD SHEET
════════════════════════════════════════════════════════════

📝 Note: This file was extracted for personal offline use.
🔗 Original source: {data['url']}
"""
        return output


def main():
    if len(sys.argv) < 2:
        print("""
ChordMaker - Ultimate Guitar Direct URL Extractor
===================================================

Works directly with live URLs - no need to save HTML first!

Requirements (first time setup):
  pip install playwright beautifulsoup4
  playwright install chromium

Usage: python scripts/extract-url.py <URL> [output-file]

Arguments:
  <URL>            Ultimate Guitar tab URL
  [output-file]    Output file (default: output/song-name.txt)

Examples:
  python scripts/extract-url.py "https://tabs.ultimate-guitar.com/tab/westlife/i-lay-my-love-on-you-chords-464"
  
  python scripts/extract-url.py "https://tabs.ultimate-guitar.com/tab/westlife/i-lay-my-love-on-you-chords-464" "output/westlife.txt"

How it works:
✓ Opens a real browser (Chromium) to fetch the page
✓ Avoids 403 blocks by using browser headers
✓ Waits for content to fully load
✓ Extracts chord notation and structure
✓ Saves to offline text file

First run will download Chromium (~150MB) - this is one-time only.
        """)
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        extractor = URLChordExtractor()
        html = extractor.fetch_url(url)
        print("✅ Page fetched successfully")
        
        print("🎸 Extracting chord content...")
        data = extractor.extract_from_html(html, url)
        
        # Generate output filename if not provided
        if not output_file:
            output_dir = "output"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            sanitized = re.sub(r'[^a-z0-9]+', '-', data['title'].lower())
            sanitized = sanitized.strip('-')
            output_file = os.path.join(output_dir, f"{sanitized}.txt")
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Format and save output
        formatted_output = extractor.format_output(data)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(formatted_output)
        
        file_size = os.path.getsize(output_file)
        print(f"💾 Saved to: {output_file}")
        print(f"📊 File size: {file_size} bytes")
        print("✨ Done!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
