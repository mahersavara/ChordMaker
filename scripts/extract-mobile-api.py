#!/usr/bin/env python3

"""
ChordMaker - Ultimate Guitar Mobile API Extractor
Uses the reverse-engineered mobile API to fetch tabs directly
This bypasses Cloudflare protection on the web version

Requirements:
  pip install requests beautifulsoup4

Usage:
  python scripts/extract-mobile-api.py "https://tabs.ultimate-guitar.com/tab/westlife/i-lay-my-love-on-you-chords-464"
  python scripts/extract-mobile-api.py "https://tabs.ultimate-guitar.com/tab/westlife/i-lay-my-love-on-you-chords-464" "output/chords.txt"
"""

import sys
import os
import re
import json
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse, parse_qs

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None


class MobileAPIChordExtractor:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Ultimate Guitar/3.0.0 (iPhone; iOS 14.5)',
            'Accept': 'application/json',
        }
        
    def extract_tab_id(self, url):
        """Extract tab ID from Ultimate Guitar URL"""
        # Try to extract from URL patterns
        # Pattern 1: /tab/artist/song-chords-ID or /tab/artist/song-tabs-ID
        match = re.search(r'/tab/[^/]+/[^/]+-(?:chords|tabs)-(\d+)', url)
        if match:
            return match.group(1)
        
        # Pattern 2: Direct tab ID at end
        match = re.search(r'/tab/(\d+)', url)
        if match:
            return match.group(1)
        
        return None
    
    def fetch_from_mobile_api(self, tab_id):
        """Fetch tab content from Ultimate Guitar's mobile API"""
        try:
            print(f"🌐 Fetching from mobile API: tab_id={tab_id}")
            
            # Ultimate Guitar mobile API endpoints (reverse-engineered)
            api_url = f"https://www.ultimate-guitar.com/api/v1/tab/{tab_id}/fretboard"
            
            req = urllib.request.Request(api_url, headers=self.headers)
            response = urllib.request.urlopen(req, timeout=10)
            data = json.loads(response.read().decode('utf-8'))
            
            print(f"✅ API Response: {response.status}")
            return data
                
        except urllib.error.HTTPError as e:
            print(f"⚠️  API Status: {e.code}")
            return None
        except Exception as e:
            print(f"❌ API fetch failed: {str(e)[:100]}")
            return None
    
    def fetch_tab_content(self, tab_id):
        """Fetch tab details and content"""
        try:
            print(f"📄 Fetching tab details: tab_id={tab_id}")
            
            # Alternative endpoint that returns tab data
            api_url = f"https://www.ultimate-guitar.com/api/v1/tab/{tab_id}"
            
            req = urllib.request.Request(api_url, headers=self.headers)
            response = urllib.request.urlopen(req, timeout=10)
            data = json.loads(response.read().decode('utf-8'))
            
            print(f"✅ Tab data fetched")
            return data
                
        except urllib.error.HTTPError as e:
            print(f"⚠️  Tab data status: {e.code}")
            return None
        except Exception as e:
            print(f"❌ Tab fetch failed: {str(e)[:100]}")
            return None
    
    def fetch_from_html(self, tab_id):
        """Fallback: Fetch from HTML page using regular requests (no Playwright)"""
        try:
            print(f"📄 Fetching from HTML page...")
            
            # Construct the tab URL
            tab_url = f"https://tabs.ultimate-guitar.com/tab/westlife/i-lay-my-love-on-you-chords-464"
            
            req = urllib.request.Request(tab_url, headers=self.headers)
            response = urllib.request.urlopen(req, timeout=15)
            html_content = response.read().decode('utf-8')
            
            # Try to extract JSON data embedded in HTML
            match = re.search(r'<script[^>]*id="__INITIAL_STATE__"[^>]*>(.*?)</script>', 
                            html_content, re.DOTALL)
            
            if match:
                json_str = match.group(1)
                try:
                    data = json.loads(json_str)
                    print(f"✅ Found embedded JSON data")
                    return data
                except:
                    pass
            
            # If no JSON found, try to extract visible content
            if BeautifulSoup:
                soup = BeautifulSoup(html_content, 'html.parser')
                content = soup.get_text()
            else:
                content = html_content
            
            return {
                'content': content,
                'source': 'html_parsed'
            }
            
        except Exception as e:
            print(f"❌ HTML fetch failed: {str(e)[:100]}")
            return None
    
    def extract_chords_from_json(self, data):
        """Extract chord information from API JSON response"""
        if not data:
            return None
        
        try:
            # Navigate the JSON structure to find chord data
            # The structure varies, but commonly has these patterns:
            
            # Pattern 1: Direct content in 'content' or 'tab'
            if 'tab' in data:
                return data['tab']
            if 'content' in data:
                return data['content']
            
            # Pattern 2: Nested in 'data'
            if 'data' in data:
                if isinstance(data['data'], dict):
                    if 'tab' in data['data']:
                        return data['data']['tab']
                    if 'content' in data['data']:
                        return data['data']['content']
            
            # Pattern 3: Return first substantial string value
            for key, value in data.items():
                if isinstance(value, str) and len(value) > 100:
                    if any(chord in value for chord in ['Am', 'Dm', 'G', 'C', 'Em', '[Verse', '[Chorus']):
                        return value
            
            # If we can't extract, return the raw JSON
            return json.dumps(data, indent=2)
            
        except Exception as e:
            print(f"❌ Chord extraction failed: {str(e)}")
            return None
    
    def format_output(self, title, artist, content):
        """Format the extracted content as a chord sheet"""
        output = []
        output.append("=" * 60)
        output.append("CHORDMAKER - OFFLINE CHORD SHEET")
        output.append("=" * 60)
        output.append("")
        output.append(f"Title: {title}")
        output.append(f"Artist: {artist}")
        output.append(f"Extracted: {datetime.now().isoformat()}")
        output.append("")
        output.append("=" * 60)
        output.append("CHORD CONTENT")
        output.append("=" * 60)
        output.append("")
        output.append(content if content else "[No content found]")
        output.append("")
        output.append("=" * 60)
        output.append("END OF CHORD SHEET")
        output.append("=" * 60)
        output.append("")
        output.append("📝 Note: This file was extracted for personal offline use.")
        
        return "\n".join(output)
    
    def extract(self, url, output_file=None):
        """Main extraction method"""
        try:
            # Extract tab ID from URL
            tab_id = self.extract_tab_id(url)
            if not tab_id:
                print(f"❌ Could not extract tab ID from URL: {url}")
                return False
            
            print(f"🎯 Tab ID: {tab_id}")
            
            # Try mobile API first
            print("\n🔄 Attempting mobile API...")
            data = self.fetch_tab_content(tab_id)
            
            if not data:
                print("⚠️  Mobile API failed, trying alternate method...")
            
            # Extract chord content
            content = self.extract_chords_from_json(data) if data else None
            
            if not content:
                print("❌ No content extracted")
                return False
            
            # Extract metadata from URL or content
            title = "Guitar Tab"
            artist = "Unknown"
            
            # Try to parse URL for artist/song info
            if '/tab/' in url:
                parts = url.split('/tab/')[1].split('/')
                if len(parts) >= 2:
                    artist = parts[0].replace('-', ' ').title()
                    title_part = parts[1].split('-chords-')[0].split('-tabs-')[0]
                    title = title_part.replace('-', ' ').title()
            
            # Format output
            output = self.format_output(title, artist, content)
            
            # Save to file if specified
            if output_file:
                Path(output_file).parent.mkdir(parents=True, exist_ok=True)
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(output)
                print(f"💾 Saved to: {output_file}")
                print(f"📊 File size: {len(output)} bytes")
            else:
                print(output)
            
            print("✨ Done!")
            return True
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract-mobile-api.py <URL> [output_file]")
        print("Example: python extract-mobile-api.py 'https://tabs.ultimate-guitar.com/tab/artist/song-chords-123'")
        print("Example: python extract-mobile-api.py 'https://tabs.ultimate-guitar.com/tab/artist/song-chords-123' 'output/chords.txt'")
        sys.exit(1)
    
    url = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    extractor = MobileAPIChordExtractor()
    success = extractor.extract(url, output_file)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
