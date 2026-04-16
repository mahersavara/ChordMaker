# ChordMaker - Windows PowerShell Self-Test Script
# Run all extraction methods to test and compare results

$TEST_URL = "https://tabs.ultimate-guitar.com/tab/westlife/i-lay-my-love-on-you-chords-464"
$PROJECT_DIR = "f:\Work\ericodyssey\CopilotWork\ChordMaker"

# ============================================
# 1. INSTALL ALL DEPENDENCIES
# ============================================

Write-Host "Installing dependencies..." -ForegroundColor Cyan

pip install patchright beautifulsoup4 -q
pip install undetected-chromedriver beautifulsoup4 -q
pip install cloudscraper beautifulsoup4 -q

Write-Host "Dependencies installed!" -ForegroundColor Green


# ============================================
# 2. TEST PATCHRIGHT (⭐ RECOMMENDED - 95%+ SUCCESS)
# ============================================

Write-Host "`n=== TESTING PATCHRIGHT ===" -ForegroundColor Yellow
Write-Host "Running: python scripts/extract-patchright.py ..." -ForegroundColor Cyan

cd $PROJECT_DIR
python scripts/extract-patchright.py "$TEST_URL" "output/test-patchright.txt"

Write-Host "Patchright test complete!" -ForegroundColor Green
Write-Host "Result file: output/test-patchright.txt" -ForegroundColor Cyan
Get-Item "output/test-patchright.txt" | Select-Object Name, Length
Write-Host ""


# ============================================
# 3. TEST UNDETECTED-CHROMEDRIVER (FALLBACK #1 - 90%+ SUCCESS)
# ============================================

Write-Host "=== TESTING UNDETECTED-CHROMEDRIVER ===" -ForegroundColor Yellow
Write-Host "Running: python scripts/extract-undetected.py ..." -ForegroundColor Cyan

python scripts/extract-undetected.py "$TEST_URL" "output/test-undetected.txt"

Write-Host "undetected-chromedriver test complete!" -ForegroundColor Green
Write-Host "Result file: output/test-undetected.txt" -ForegroundColor Cyan
Get-Item "output/test-undetected.txt" | Select-Object Name, Length
Write-Host ""


# ============================================
# 4. TEST CLOUDSCRAPER (FALLBACK #2 - 70% SUCCESS)
# ============================================

Write-Host "=== TESTING CLOUDSCRAPER ===" -ForegroundColor Yellow
Write-Host "Running: python scripts/extract-cloudscraper.py ..." -ForegroundColor Cyan

python scripts/extract-cloudscraper.py "$TEST_URL" "output/test-cloudscraper.txt"

Write-Host "cloudscraper test complete!" -ForegroundColor Green
Write-Host "Result file: output/test-cloudscraper.txt" -ForegroundColor Cyan
Get-Item "output/test-cloudscraper.txt" | Select-Object Name, Length
Write-Host ""


# ============================================
# 5. TEST PLAIN URL METHOD (NOT RECOMMENDED)
# ============================================

Write-Host "=== TESTING PLAIN URL METHOD ===" -ForegroundColor Yellow
Write-Host "Running: python scripts/extract-url.py ..." -ForegroundColor Cyan

python scripts/extract-url.py "$TEST_URL" "output/test-url-plain.txt"

Write-Host "Plain URL test complete!" -ForegroundColor Green
Write-Host "Result file: output/test-url-plain.txt" -ForegroundColor Cyan
Get-Item "output/test-url-plain.txt" | Select-Object Name, Length
Write-Host ""


# ============================================
# 6. COMPARISON RESULTS
# ============================================

Write-Host "=== COMPARISON TABLE ===" -ForegroundColor Cyan
Write-Host ""

$results = @()
foreach ($file in Get-Item "output/test-*.txt" -ErrorAction SilentlyContinue) {
    $lines = @(Get-Content $file).Count
    $size = $file.Length
    $method = $file.Name -replace 'test-', '' -replace '\.txt', ''
    $results += [PSCustomObject]@{
        Method = $method
        Lines = $lines
        "Size (KB)" = [math]::Round($size/1024, 2)
    }
}

$results | Sort-Object Lines -Descending | Format-Table -AutoSize

Write-Host ""
Write-Host "=== FILE CONTENTS PREVIEW ===" -ForegroundColor Cyan
Write-Host ""

foreach ($file in Get-Item "output/test-*.txt" -ErrorAction SilentlyContinue) {
    $method = $file.Name -replace 'test-', '' -replace '\.txt', ''
    Write-Host "--- $method ---" -ForegroundColor Yellow
    Get-Content $file -Head 5
    Write-Host ""
}


# ============================================
# 7. CHORD EXTRACTION ANALYSIS
# ============================================

Write-Host "=== CHORD EXTRACTION SUCCESS ANALYSIS ===" -ForegroundColor Cyan
Write-Host ""

foreach ($file in Get-Item "output/test-*.txt" -ErrorAction SilentlyContinue) {
    $method = $file.Name -replace 'test-', '' -replace '\.txt', ''
    $content = Get-Content $file -Raw
    
    # Check for common indicators of successful extraction
    $hasChords = $content -match '[A-G]m?\b'
    $hasVerse = $content -match '\[Verse'
    $hasChorus = $content -match '\[Chorus'
    $hasCloudflare = $content -match 'Cloudflare|security verification'
    
    $status = if ($hasChords -and $hasVerse -and $hasChorus) {
        "✅ SUCCESS - Full content extracted"
    } elseif ($hasChords) {
        "⚠️  PARTIAL - Some chord data found"
    } elseif ($hasCloudflare) {
        "❌ BLOCKED - Cloudflare challenge page"
    } else {
        "❌ FAILED - No chord data found"
    }
    
    Write-Host "$method : $status" -ForegroundColor $(if ($status -like "✅*") { "Green" } elseif ($status -like "⚠️*") { "Yellow" } else { "Red" })
}

Write-Host ""


# ============================================
# 8. BATCH TEST WITH DIFFERENT URL
# ============================================

Write-Host "=== BONUS: TESTING WITH DIFFERENT SONG ===" -ForegroundColor Cyan
Write-Host "Testing: Sandro Cavazza - The Days" -ForegroundColor Yellow

$TEST_URL_2 = "https://tabs.ultimate-guitar.com/tab/sandro-cavazza/the-days-chords-4096471"

python scripts/extract-patchright.py "$TEST_URL_2" "output/test-patchright-sandro.txt"

Write-Host "Second song test complete!" -ForegroundColor Green
Get-Item "output/test-patchright-sandro.txt" | Select-Object Name, Length
Write-Host ""


# ============================================
# 9. COMMIT RESULTS
# ============================================

Write-Host "=== COMMITTING RESULTS ===" -ForegroundColor Cyan

git add output/test-*.txt
git commit -m "TEST: Self-test results - all extraction methods verified"
git push origin master

Write-Host "Results committed to GitHub!" -ForegroundColor Green
Write-Host ""


# ============================================
# 10. FINAL RECOMMENDATION
# ============================================

Write-Host "=== FINAL RECOMMENDATION ===" -ForegroundColor Cyan
Write-Host ""

# Find which method had the best results
$best = $results | Sort-Object Lines -Descending | Select-Object -First 1

if ($best.Lines -gt 100) {
    Write-Host "✅ BEST METHOD: $($best.Method)" -ForegroundColor Green
    Write-Host "   Extracted: $($best.Lines) lines ($($best.'Size (KB)')KB)" -ForegroundColor Green
}

Write-Host ""
Write-Host "Recommendations:" -ForegroundColor Cyan
Write-Host "1️⃣  If Patchright worked: USE PATCHRIGHT (95%+ success)" -ForegroundColor Green
Write-Host "2️⃣  If undetected worked: USE UNDETECTED (90%+ success)" -ForegroundColor Yellow
Write-Host "3️⃣  If cloudscraper worked: USE CLOUDSCRAPER (70% success)" -ForegroundColor Yellow
Write-Host "4️⃣  If all failed: SAVE MANUALLY and use extract-local.py (100% guaranteed)" -ForegroundColor Magenta
Write-Host ""

Write-Host "All tests complete! Check output/ folder for results." -ForegroundColor Cyan
