#!/usr/bin/env python3
"""
ChordMaker - Extract chord data using cloudscraper
Cloudscraper is a lightweight module specifically for Cloudflare bypass.

Installation:
    pip install cloudscraper beautifulsoup4

Reference: https://github.com/VeNoMouS/cloudscraper
Best for: Simple, lightweight Cloudflare bypass (no JavaScript rendering)
"""

import sys
from pathlib import Path
from bs4 import BeautifulSoup

try:
    import cloudscraper
except ImportError:
    print("❌ cloudscraper not installed. Install with:")
    print("   pip install cloudscraper beautifulsoup4")
    sys.exit(1)


class ChordExtractor:
    def __init__(self):
        # Create cloudscraper instance
        self.scraper = cloudscraper.create_scraper()

    def extract_from_url(self, url: str, output_file: str = None) -> str:
        """
        Extract chord data from Ultimate Guitar URL using cloudscraper.
        Note: Cloudscraper doesn't render JavaScript, so success depends on static HTML.
        """
        print(f"🎸 Extracting chords from: {url}")
        print(f"🔧 Using: cloudscraper (Lightweight Cloudflare bypass)")
        print(f"⚠️  Note: This method doesn't render JavaScript")

        try:
            print(f"⏳ Fetching page...")

            response = self.scraper.get(url, timeout=10)

            if response.status_code != 200:
                print(f"❌ Failed: HTTP {response.status_code}")
                return ""

            # Parse and extract chords
            chords = self._parse_chords(response.text)

            if chords:
                print(f"✅ Found {len(chords.split(chr(10)))} chord lines")
                if output_file:
                    self._save_chords(chords, output_file)
                    print(f"💾 Saved to: {output_file}")
                return chords
            else:
                print("⚠️  No chord content found")
                print("💡 Try Patchright or undetected-chromedriver instead (they render JavaScript)")
                return ""

        except Exception as e:
            print(f"❌ Error: {e}")
            return ""

    def _parse_chords(self, html: str) -> str:
        """Parse HTML for chord content"""
        try:
            soup = BeautifulSoup(html, "html.parser")

            # Remove script and style tags
            for tag in soup(["script", "style"]):
                tag.decompose()

            text = soup.get_text()
            lines = text.split("\n")
            chord_lines = []

            for line in lines:
                line = line.strip()
                if len(line) > 0:
                    if any(
                        keyword in line.upper()
                        for keyword in [
                            "VERSE",
                            "CHORUS",
                            "BRIDGE",
                            "INTRO",
                            "OUTRO",
                            "PRE-CHORUS",
                        ]
                    ):
                        chord_lines.append(line)
                    elif any(chord in line for chord in ["Am", "Dm", "G", "C", "D", "A", "E"]):
                        chord_lines.append(line)

            return "\n".join(chord_lines) if chord_lines else text[:500]

        except Exception as e:
            print(f"Parse error: {e}")
            return ""

    def _save_chords(self, content: str, output_file: str):
        """Save extracted chords to file"""
        try:
            Path(output_file).parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            print(f"Save error: {e}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract-cloudscraper.py <url> [output_file]")
        print("Example:")
        print(
            '  python extract-cloudscraper.py "https://tabs.ultimate-guitar.com/tab/..." "output.txt"'
        )
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    extractor = ChordExtractor()
    extractor.extract_from_url(url, output_file)


if __name__ == "__main__":
    main()
