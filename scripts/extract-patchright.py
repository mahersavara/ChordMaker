#!/usr/bin/env python3
"""
ChordMaker - Extract chord data using Patchright (Undetected Playwright)
Patchright is a drop-in replacement for Playwright that bypasses Cloudflare.

Installation:
    pip install patchright beautifulsoup4

Reference: https://github.com/Kaliiiiiiiiii-Vinyzu/patchright
Passes: Cloudflare, Kasada, Akamai, Shape/F5, DataDome, and 15+ other bot detection systems
"""

import asyncio
import sys
from pathlib import Path

# Try to import patchright, fall back to playwright if not available
try:
    from patchright.async_api import async_playwright
    USING_PATCHRIGHT = True
except ImportError:
    print("⚠️  Patchright not installed. Install with: pip install patchright")
    print("   Attempting fallback to Playwright...")
    try:
        from playwright.async_api import async_playwright
        USING_PATCHRIGHT = False
    except ImportError:
        print("❌ Neither Patchright nor Playwright found. Install with:")
        print("   pip install patchright beautifulsoup4")
        sys.exit(1)

from bs4 import BeautifulSoup


class ChordExtractor:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    async def extract_from_url(self, url: str, output_file: str = None) -> str:
        """
        Extract chord data from Ultimate Guitar URL using Patchright.
        Patchright bypasses Cloudflare by patching Playwright's detection signatures.
        """
        print(f"🎸 Extracting chords from: {url}")
        print(f"🔧 Using: {'Patchright (Undetected)' if USING_PATCHRIGHT else 'Playwright'}")

        try:
            async with async_playwright() as p:
                # Launch browser - Patchright automatically applies stealth patches
                browser = await p.chromium.launch(
                    headless=True,
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--disable-dev-shm-usage",
                    ]
                )

                context = await browser.new_context()
                page = await context.new_page()

                # Set realistic headers
                await page.set_extra_http_headers(self.headers)

                # Navigate to URL
                print(f"⏳ Loading page (with Cloudflare bypass)...")
                try:
                    await page.goto(url, wait_until="networkidle", timeout=30000)
                except Exception as e:
                    print(f"⚠️  Navigation warning: {e}")
                    # Continue anyway - page may have loaded partially
                    pass

                # Wait for content to load
                await page.wait_for_timeout(2000)

                # Extract page content
                content = await page.content()

                await browser.close()

                # Parse and extract chords
                chords = self._parse_chords(content)

                if chords:
                    print(f"✅ Found {len(chords)} chord lines")
                    if output_file:
                        self._save_chords(chords, output_file)
                        print(f"💾 Saved to: {output_file}")
                    return chords
                else:
                    print("⚠️  No chord content found (Cloudflare may still be blocking)")
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

            # Get all text
            text = soup.get_text()

            # Filter for chord-like content
            lines = text.split("\n")
            chord_lines = []

            for line in lines:
                line = line.strip()
                if len(line) > 0:
                    # Look for common chord patterns and song structure keywords
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
                    # Also include lines with chord symbols (A, E, D, G, etc.)
                    elif any(
                        chord in line for chord in ["Am", "Dm", "G", "C", "D", "A", "E"]
                    ):
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


async def main():
    if len(sys.argv) < 2:
        print("Usage: python extract-patchright.py <url> [output_file]")
        print("Example:")
        print(
            '  python extract-patchright.py "https://tabs.ultimate-guitar.com/tab/..." "output.txt"'
        )
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    extractor = ChordExtractor()
    await extractor.extract_from_url(url, output_file)


if __name__ == "__main__":
    asyncio.run(main())
