# Scripts Directory

Utility scripts for ChordMaker to extract and manage chord data.

## extract-chords.js

A Node.js script to extract chords and lyrics from Ultimate Guitar tabs for offline use.

### Requirements

- Node.js 18+ (for built-in `fetch` support)

### Installation

No additional packages needed - uses Node.js built-in `fetch` API.

### Usage

```bash
node scripts/extract-chords.js <URL> [output-file]
```

### Examples

```bash
# Basic usage (saves to auto-named file)
node scripts/extract-chords.js "https://tabs.ultimate-guitar.com/tab/westlife/i-lay-my-love-on-you-chords-464"

# Custom output filename
node scripts/extract-chords.js "https://tabs.ultimate-guitar.com/tab/westlife/i-lay-my-love-on-you-chords-464" "my-song.txt"

# Save to data directory
node scripts/extract-chords.js "https://tabs.ultimate-guitar.com/tab/artist/song-name" "data/my-chord-sheet.txt"
```

### Output

The script creates a formatted text file containing:
- Song title and artist
- Difficulty level
- Tuning information
- Full chord progression and lyrics
- Metadata and source URL

### Features

✅ Extracts chords and lyrics for offline use  
✅ Auto-generates filenames from song titles  
✅ Preserves formatting and structure  
✅ Includes metadata (difficulty, tuning)  
✅ Error handling and validation  

### Example Output

```
════════════════════════════════════════════════════════════
CHORDMAKER - OFFLINE CHORD SHEET
════════════════════════════════════════════════════════════

Title: I Lay My Love On You
Artist: Westlife
Difficulty: Beginner
Tuning: Standard
Extracted: 2026-04-16T...
Source: https://tabs.ultimate-guitar.com/...

════════════════════════════════════════════════════════════
CHORD CONTENT
════════════════════════════════════════════════════════════

[Verse]
Em      Am
...chord content here...
```

### Troubleshooting

**"HTTP 404" error**
- Verify the URL is correct
- Check that the Ultimate Guitar page exists

**"Node.js 18+ required"**
- Upgrade Node.js: https://nodejs.org/

**Output file not created**
- Check you have write permissions in the directory
- Verify the output path exists

### Future Enhancements

- Support for multiple tab websites
- Batch processing multiple URLs
- Format conversion (PDF, JSON, etc.)
- Audio playback integration
