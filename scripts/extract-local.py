#!/usr/bin/env python3

"""
ChordMaker - Local HTML Chord Extractor
Extracts chords from locally saved HTML files for offline use

Usage:
  python scripts/extract-local.py <html-file> [output-file]

How to use:
  1. Visit Ultimate Guitar in your browser
  2. Right-click → Save As (save as .html file)
  3. Run: python scripts/extract-local.py path/to/saved.html
"""

import sys
import os
import re
from datetime import datetime
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("❌ Missing required package!")
    print("Install with: pip install beautifulsoup4")
    sys.exit(1)


class LocalChordExtractor:
    def extract_from_file(self, file_path):
        """Extract chord content from local HTML file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html = f.read()
        except FileNotFoundError:
            raise Exception(f"File not found: {file_path}")
        except Exception as e:
            raise Exception(f"Error reading file: {str(e)}")
        
        return self.extract_from_html(html)

    def extract_from_html(self, html):
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
        
        # Extract artist
        artist = "Unknown"
        artist_match = re.search(r'by\s+([^<\n]+)', html)
        if artist_match:
            artist = artist_match.group(1).strip()
        
        # Extract chord content from pre tags
        content = ""
        pre_tags = soup.find_all('pre')
        
        for pre in pre_tags:
            pre_content = pre.get_text()
            if any(chord in pre_content for chord in ['[', ']', '(', ')']):
                content = pre_content
                break
        
        # Fallback: look for any text that contains chord patterns
        if not content:
            for div in soup.find_all('div', class_=re.compile('tab|content|lyric', re.I)):
                div_text = div.get_text()
                if len(div_text) > 100:
                    content = div_text
                    break
        
        if not content:
            content = "Could not extract chord content - file may be incomplete"
        
        return {
            'title': title,
            'artist': artist,
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

    def format_output(self, data, source):
        """Format the extracted data for output"""
        output = f"""════════════════════════════════════════════════════════════
CHORDMAKER - OFFLINE CHORD SHEET
════════════════════════════════════════════════════════════

Title: {data['title']}
Artist: {data['artist']}
Extracted: {datetime.now().isoformat()}
Source: {source}

════════════════════════════════════════════════════════════
CHORD CONTENT
════════════════════════════════════════════════════════════

{self.clean_text(data['content'])}

════════════════════════════════════════════════════════════
END OF CHORD SHEET
════════════════════════════════════════════════════════════

📝 Note: This file was extracted for personal offline use.
🔗 Original source: {source}
"""
        return output


def main():
    if len(sys.argv) < 2:
        print("""
ChordMaker - Local HTML Chord Extractor
========================================

For websites that block automated scraping, save the HTML locally first.

Usage: python scripts/extract-local.py <html-file> [output-file]

Arguments:
  <html-file>      Path to saved HTML file
  [output-file]    Output file (default: output/song-name.txt)

How to get the HTML file:
  1. Visit the tab website in your browser
  2. Right-click → "Save As" (or Ctrl+S)
  3. Save as HTML file (.html)
  4. Run this script with the saved file path

Example:
  python scripts/extract-local.py "Downloads/i-lay-my-love.html" "output/westlife.txt"
        """)
        sys.exit(1)

    html_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        print(f"📖 Reading HTML file: {html_file}")
        
        extractor = LocalChordExtractor()
        data = extractor.extract_from_file(html_file)
        print("✅ HTML parsed successfully")
        
        print("🎸 Extracting chord content...")
        
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
        formatted_output = extractor.format_output(data, html_file)
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
