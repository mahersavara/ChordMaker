# ChordMaker Output Folder

This folder contains extracted chord sheets saved for offline use.

## How to Generate Chord Sheets

Since Ultimate Guitar blocks automated scraping, use the local extraction method:

### Step 1: Save the HTML File
1. Visit the Ultimate Guitar URL in your browser
2. Press `Ctrl+S` (or right-click → "Save As")
3. Save as HTML file to any location (e.g., `Downloads/song.html`)

### Step 2: Extract Using the Script
```bash
cd ChordMaker
python scripts/extract-local.py "path/to/saved.html" "output/song-name.txt"
```

### Example
```bash
python scripts/extract-local.py "Downloads/i-lay-my-love.html" "output/westlife.txt"
```

## File Format

Each chord sheet includes:
- Song title and artist
- Difficulty level
- Tuning information
- Chord diagrams and finger positions
- Lyrics with chord placement
- Practice notes and tips

## Sample File

See `sample-chord-sheet.txt` for a template of the output format.

## Organization Tips

Organize your chord sheets by:
- Artist: `output/westlife/`
- Genre: `output/pop/`, `output/rock/`, etc.
- Difficulty: `output/beginner/`, `output/intermediate/`, etc.

Example:
```
output/
├── westlife/
│   ├── i-lay-my-love-on-you.txt
│   └── flying-without-wings.txt
├── pop/
│   ├── shape-of-you.txt
│   └── perfect.txt
└── sample-chord-sheet.txt
```
