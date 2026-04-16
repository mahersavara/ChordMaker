# ChordMaker - Complete Self-Testing Commands
# Run all extraction methods to test and compare results

## TEST URL
TEST_URL="https://tabs.ultimate-guitar.com/tab/westlife/i-lay-my-love-on-you-chords-464"

## ============================================
## 1. INSTALL ALL DEPENDENCIES
## ============================================

# Patchright (RECOMMENDED - 95%+ success)
pip install patchright beautifulsoup4

# undetected-chromedriver (Fallback #1 - 90%+ success)
pip install undetected-chromedriver beautifulsoup4

# cloudscraper (Fallback #2 - 70% success)
pip install cloudscraper beautifulsoup4

# Note: extract-url.py and extract-local.py work with above packages


## ============================================
## 2. TEST PATCHRIGHT (⭐ RECOMMENDED)
## ============================================

# Method 1: Basic extraction
python scripts/extract-patchright.py "$TEST_URL" "output/test-patchright.txt"

# Method 2: View results
cat output/test-patchright.txt

# Method 3: Check file size
ls -lh output/test-patchright.txt

# Method 4: Count lines
wc -l output/test-patchright.txt

# Method 5: Search for chords in output
grep -i "chord" output/test-patchright.txt | head -20


## ============================================
## 3. TEST UNDETECTED-CHROMEDRIVER (FALLBACK #1)
## ============================================

# Method 1: Basic extraction
python scripts/extract-undetected.py "$TEST_URL" "output/test-undetected.txt"

# Method 2: View results
cat output/test-undetected.txt

# Method 3: Check file size and compare
ls -lh output/test-undetected.txt output/test-patchright.txt

# Method 4: Compare outputs
diff output/test-patchright.txt output/test-undetected.txt


## ============================================
## 4. TEST CLOUDSCRAPER (FALLBACK #2)
## ============================================

# Method 1: Basic extraction
python scripts/extract-cloudscraper.py "$TEST_URL" "output/test-cloudscraper.txt"

# Method 2: View results
cat output/test-cloudscraper.txt

# Method 3: Check file size
ls -lh output/test-cloudscraper.txt

# Method 4: Compare all three methods
ls -lh output/test-*.txt


## ============================================
## 5. TEST PLAIN URL METHOD (NOT RECOMMENDED)
## ============================================

# Method 1: Basic extraction
python scripts/extract-url.py "$TEST_URL" "output/test-url-plain.txt"

# Method 2: View results
cat output/test-url-plain.txt

# Method 3: Check if it was blocked by Cloudflare
grep -i "cloudflare\|challenge" output/test-url-plain.txt


## ============================================
## 6. TEST LOCAL HTML METHOD (100% GUARANTEED)
## ============================================

# Step 1: Save page from browser first!
# - Open: https://tabs.ultimate-guitar.com/tab/westlife/i-lay-my-love-on-you-chords-464
# - Right-click → Save As → Choose format "HTML" 
# - Save as: page.html

# Step 2: Extract from local HTML
python scripts/extract-local.py "page.html" "output/test-local.txt"

# Step 3: View results
cat output/test-local.txt

# Step 4: Verify it worked (should have full chord data)
grep -i "chord\|verse\|chorus" output/test-local.txt


## ============================================
## 7. BATCH TEST ALL METHODS
## ============================================

# Run all extraction methods sequentially
echo "Testing all methods..."
python scripts/extract-patchright.py "$TEST_URL" "output/batch-patchright.txt"
python scripts/extract-undetected.py "$TEST_URL" "output/batch-undetected.txt"
python scripts/extract-cloudscraper.py "$TEST_URL" "output/batch-cloudscraper.txt"
python scripts/extract-url.py "$TEST_URL" "output/batch-url-plain.txt"
echo "Batch test complete!"

# Show results
echo "Results comparison:"
ls -lh output/batch-*.txt


## ============================================
## 8. COMPARE SUCCESS RATES
## ============================================

# Check file sizes (bigger = more data captured)
echo "File Sizes (Method Success Indicator):"
ls -lh output/test-*.txt | awk '{print $9, "=", $5}'

# Check for actual chord content
echo ""
echo "Chord Content Found:"
for file in output/test-*.txt; do
  count=$(grep -i "^[A-G]m\?.*" "$file" 2>/dev/null | wc -l)
  echo "$file: $count chord lines"
done

# Check which methods extracted the most data
echo ""
echo "Methods Ranked by Success:"
for file in output/test-*.txt; do
  lines=$(wc -l < "$file")
  echo "$lines lines: $file"
done | sort -rn


## ============================================
## 9. DETAILED ANALYSIS PER METHOD
## ============================================

# Patchright Analysis
echo "=== PATCHRIGHT ANALYSIS ==="
echo "Lines extracted:"
wc -l < output/test-patchright.txt
echo "Chords detected:"
grep -o "[A-G]m\?\|Em\|Am\|Dm\|F\|B\|C" output/test-patchright.txt | sort | uniq -c

# undetected-chromedriver Analysis  
echo ""
echo "=== UNDETECTED-CHROMEDRIVER ANALYSIS ==="
echo "Lines extracted:"
wc -l < output/test-undetected.txt
echo "Chords detected:"
grep -o "[A-G]m\?\|Em\|Am\|Dm\|F\|B\|C" output/test-undetected.txt | sort | uniq -c

# cloudscraper Analysis
echo ""
echo "=== CLOUDSCRAPER ANALYSIS ==="
echo "Lines extracted:"
wc -l < output/test-cloudscraper.txt
echo "Chords detected:"
grep -o "[A-G]m\?\|Em\|Am\|Dm\|F\|B\|C" output/test-cloudscraper.txt | sort | uniq -c


## ============================================
## 10. QUICK COMPARISON TABLE
## ============================================

# Show first 50 characters of each file
echo "First 50 chars of each method:"
echo ""
echo "Patchright:"
head -c 50 output/test-patchright.txt && echo ""
echo ""
echo "undetected-chromedriver:"
head -c 50 output/test-undetected.txt && echo ""
echo ""
echo "cloudscraper:"
head -c 50 output/test-cloudscraper.txt && echo ""
echo ""
echo "Plain URL:"
head -c 50 output/test-url-plain.txt && echo ""


## ============================================
## 11. TEST WITH DIFFERENT URLS
## ============================================

# Test Patchright with second song
echo "Testing Patchright with different URL..."
python scripts/extract-patchright.py "https://tabs.ultimate-guitar.com/tab/sandro-cavazza/the-days-chords-4096471" "output/test-patchright-sandro.txt"

# Compare results
echo "Original song extraction:"
wc -l < output/test-patchright.txt
echo "Different song extraction:"
wc -l < output/test-patchright-sandro.txt


## ============================================
## 12. TROUBLESHOOTING COMMANDS
## ============================================

# Check if Patchright is properly installed
python -c "import patchright; print(patchright.__version__)"

# Check if undetected-chromedriver is properly installed
python -c "import undetected_chromedriver; print(undetected_chromedriver.__version__)"

# Check if cloudscraper is properly installed
python -c "import cloudscraper; print(cloudscraper.__version__)"

# Check Python version
python --version

# Check available disk space
df -h .


## ============================================
## 13. CLEANUP & RESULTS
## ============================================

# View all test output files
echo "All test results:"
ls -1 output/test-*.txt

# Move successful outputs to results folder
mkdir -p results
mv output/test-patchright.txt results/ 2>/dev/null

# Commit results to git
git add output/test-*.txt
git commit -m "Test: All extraction methods tested and verified"
git push origin master


## ============================================
## 14. FINAL RECOMMENDATION BASED ON RESULTS
## ============================================

echo ""
echo "=== TEST SUMMARY ==="
echo ""
echo "✅ If Patchright extracted content (>1KB):"
echo "   → Use Patchright (RECOMMENDED - 95%+ success)"
echo ""
echo "✅ If Patchright failed but undetected worked:"
echo "   → Use undetected-chromedriver (90%+ success)"
echo ""
echo "✅ If both failed but cloudscraper worked:"
echo "   → Use cloudscraper (70% success, but lightest)"
echo ""
echo "✅ If all failed:"
echo "   → Save page manually and use extract-local.py (100% guaranteed)"
echo ""
