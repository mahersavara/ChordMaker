#!/usr/bin/env python3

"""
ChordMaker - Ultimate Guitar Chord Extractor (Python)
Extracts chords from Ultimate Guitar tabs for offline use

Requirements:
  pip install requests beautifulsoup4

Usage:
  python scripts/extract-chords.py <URL> [output-file]
"""

import sys
import os
import re
from datetime import datetime
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("❌ Missing required packages!")
    print("Install with: pip install requests beautifulsoup4")
    sys.exit(1)


class ChordExtractor:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.session = requests.Session()

    def fetch_page(self, url):
        """Fetch the Ultimate Guitar page"""
        try:
            response = self.session.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch page: {str(e)}")

    def extract_from_html(self, html):
        """Extract chord content from HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract title
        title = "Unknown"
        title_tag = soup.find('h1')
        if title_tag:
            title = title_tag.get_text(strip=True)
        
        # Extract artist
        artist = "Unknown"
        artist_match = re.search(r'by\s+([^<\n]+)', html)
        if artist_match:
            artist = artist_match.group(1).strip()
        
        # Extract chord content - look for pre tags or div with tab content
        content = "Could not extract chord content"
        
        # Try to find pre tag with class containing 'tab'
        for pre in soup.find_all('pre'):
            if 'tab' in pre.get('class', []):
                content = pre.get_text()
                break
        
        # Fallback: look for article tag
        if content == "Could not extract chord content":
            article = soup.find('article')
            if article:
                content = article.get_text()
        
        return {
            'title': title,
            'artist': artist,
            'content': content.strip()
        }

    def clean_text(self, text):
        """Clean extracted text"""
        # Remove extra whitespace
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

    def format_output(self, data, url):
        """Format the extracted data for output"""
        output = f"""════════════════════════════════════════════════════════════
CHORDMAKER - OFFLINE CHORD SHEET
════════════════════════════════════════════════════════════

Title: {data['title']}
Artist: {data['artist']}
Extracted: {datetime.now().isoformat()}
Source: {url}

════════════════════════════════════════════════════════════
CHORD CONTENT
════════════════════════════════════════════════════════════

{self.clean_text(data['content'])}

════════════════════════════════════════════════════════════
END OF CHORD SHEET
════════════════════════════════════════════════════════════

📝 Note: This file was extracted for personal offline use.
🔗 Original source: {url}
"""
        return output


def main():
    if len(sys.argv) < 2:
        print("""
ChordMaker - Ultimate Guitar Chord Extractor (Python)
======================================================

Usage: python scripts/extract-chords.py <URL> [output-file]

Arguments:
  <URL>            Ultimate Guitar tab URL
  [output-file]    Output file (default: auto-generated)

Example:
  python scripts/extract-chords.py "https://tabs.ultimate-guitar.com/tab/westlife/i-lay-my-love-on-you-chords-464"

The script will extract chords and save to output/ folder.
        """)
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        print(f"📥 Fetching: {url}")
        
        extractor = ChordExtractor()
        html = extractor.fetch_page(url)
        print("✅ Page fetched successfully")
        
        print("🎸 Extracting chord content...")
        data = extractor.extract_from_html(html)
        
        # Generate output filename if not provided
        if not output_file:
            # Create output directory if needed
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
        formatted_output = extractor.format_output(data, url)
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
