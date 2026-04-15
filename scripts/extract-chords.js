#!/usr/bin/env node

/**
 * ChordMaker - Ultimate Guitar Chord Extractor
 * Extracts chords and lyrics from Ultimate Guitar tabs for offline use
 * 
 * Usage: node extract-chords.js <URL> [output-file]
 * Example: node extract-chords.js "https://tabs.ultimate-guitar.com/tab/westlife/i-lay-my-love-on-you-chords-464" output.txt
 */

const fs = require('fs');
const path = require('path');

// Simple HTML parser for chord extraction
class ChordExtractor {
  constructor(html) {
    this.html = html;
  }

  // Extract title from the page
  extractTitle() {
    const titleMatch = this.html.match(/<h1[^>]*>([^<]+)<\/h1>/i);
    const metaMatch = this.html.match(/<title>([^<]+)<\/title>/i);
    return titleMatch ? titleMatch[1].trim() : (metaMatch ? metaMatch[1].split(' @')[0] : 'Unknown');
  }

  // Extract artist
  extractArtist() {
    const artistMatch = this.html.match(/by\s+([^@<\n]+)/i);
    return artistMatch ? artistMatch[1].trim() : 'Unknown';
  }

  // Extract chord content (main content area)
  extractChordContent() {
    // Look for the main tab content
    const contentPatterns = [
      /<pre[^>]*class="[^"]*tab[^"]*"[^>]*>([\s\S]*?)<\/pre>/gi,
      /<div[^>]*class="[^"]*content[^"]*"[^>]*>([\s\S]*?)<\/div>/gi,
      /<article[^>]*>([\s\S]*?)<\/article>/gi
    ];

    for (const pattern of contentPatterns) {
      const matches = this.html.match(pattern);
      if (matches && matches.length > 0) {
        return this.cleanHtml(matches[0]);
      }
    }

    return 'Could not extract chord content - please visit the URL directly';
  }

  // Clean HTML tags while preserving structure
  cleanHtml(text) {
    return text
      .replace(/<[^>]+>/g, '') // Remove all HTML tags
      .replace(/&nbsp;/g, ' ')
      .replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>')
      .replace(/&amp;/g, '&')
      .replace(/&quot;/g, '"')
      .replace(/&apos;/g, "'")
      .replace(/\n\s*\n\s*\n/g, '\n\n') // Remove excessive blank lines
      .trim();
  }

  // Extract metadata
  extractMetadata() {
    const metadata = {};
    
    // Try to find difficulty
    const diffMatch = this.html.match(/difficulty:\s*(\w+)/i);
    metadata.difficulty = diffMatch ? diffMatch[1] : 'Unknown';

    // Try to find tuning
    const tuningMatch = this.html.match(/tuning:\s*([^<\n]+)/i);
    metadata.tuning = tuningMatch ? tuningMatch[1].trim() : 'Standard';

    return metadata;
  }

  extract() {
    return {
      title: this.extractTitle(),
      artist: this.extractArtist(),
      content: this.extractChordContent(),
      metadata: this.extractMetadata()
    };
  }
}

// Main execution
async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log(`
ChordMaker - Ultimate Guitar Chord Extractor
=============================================

Usage: node extract-chords.js <URL> [output-file]

Arguments:
  <URL>            Ultimate Guitar tab URL
  [output-file]    Output file (default: song-title.txt)

Example:
  node extract-chords.js "https://tabs.ultimate-guitar.com/tab/westlife/i-lay-my-love-on-you-chords-464"

The script will:
1. Fetch the tab page
2. Extract chords and lyrics
3. Save to a text file for offline use
    `);
    process.exit(1);
  }

  const url = args[0];
  let outputFile = args[1];

  try {
    console.log(`📥 Fetching: ${url}`);
    
    // Fetch the page with User-Agent header
    const response = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}\n\nNote: The website may require authentication or have blocked this request.`);
    }

    const html = await response.text();
    console.log('✅ Page fetched successfully');

    // Extract chords
    console.log('🎸 Extracting chord content...');
    const extractor = new ChordExtractor(html);
    const data = extractor.extract();

    // Generate output filename if not provided
    if (!outputFile) {
      const sanitizedTitle = data.title
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/^-|-$/g, '');
      outputFile = `${sanitizedTitle}.txt`;
    }

    // Create formatted output
    const output = `
════════════════════════════════════════════════════════════
CHORDMAKER - OFFLINE CHORD SHEET
════════════════════════════════════════════════════════════

Title: ${data.title}
Artist: ${data.artist}
Difficulty: ${data.metadata.difficulty}
Tuning: ${data.metadata.tuning}
Extracted: ${new Date().toISOString()}
Source: ${url}

════════════════════════════════════════════════════════════
CHORD CONTENT
════════════════════════════════════════════════════════════

${data.content}

════════════════════════════════════════════════════════════
END OF CHORD SHEET
════════════════════════════════════════════════════════════

📝 Note: This file was extracted for personal offline use.
🔗 Original source: ${url}
    `.trim();

    // Write to file
    fs.writeFileSync(outputFile, output);
    console.log(`💾 Saved to: ${outputFile}`);
    console.log(`📊 File size: ${fs.statSync(outputFile).size} bytes`);
    console.log(`✨ Done!`);

  } catch (error) {
    console.error(`❌ Error: ${error.message}`);
    process.exit(1);
  }
}

// Check if fetch is available (Node.js 18+)
if (typeof fetch === 'undefined') {
  console.error('❌ Error: This script requires Node.js 18+ (with built-in fetch)');
  console.error('Please upgrade Node.js: https://nodejs.org/');
  process.exit(1);
}

main();
