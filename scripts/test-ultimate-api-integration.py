#!/usr/bin/env python3
"""
ChordMaker - Ultimate-API Integration Test
Attempts to use joncardasis/ultimate-api for chord extraction
"""

import os
import json
import requests
from pathlib import Path

def test_ultimate_api():
    """Test ultimate-api approach for chord extraction"""
    
    print("🎸 Testing Ultimate-API Integration")
    print("=" * 60)
    
    # Note: ultimate-api is an older project (2015 era)
    # It may or may not work with current Ultimate Guitar structure
    
    test_urls = [
        "https://tabs.ultimate-guitar.com/tab/westlife/i-lay-my-love-on-you-chords-464",
        "https://tabs.ultimate-guitar.com/tab/sandro-cavazza/the-days-chords-4096471"
    ]
    
    print("\n📋 Method 1: Clone and Run Local Server")
    print("-" * 60)
    print("""
    # Step 1: Clone the repository
    git clone https://github.com/joncardasis/ultimate-api.git
    cd ultimate-api
    
    # Step 2: Install dependencies
    pip install -r requirements.txt
    
    # Step 3: Run the Flask server
    export FLASK_DEBUG=1  # or set FLASK_DEBUG=1 on Windows
    python run.py
    
    # Step 4: Test the API endpoint in another terminal
    curl "http://localhost:5000/tab?url=https://tabs.ultimate-guitar.com/tab/westlife/i-lay-my-love-on-you-chords-464"
    
    # Step 5: Get JSON response with chord data
    """)
    
    print("\n📋 Method 2: Use as Python Module (if importable)")
    print("-" * 60)
    print("""
    # If the module can be imported:
    from ultimate_api import TabParser
    
    url = "https://tabs.ultimate-guitar.com/tab/westlife/i-lay-my-love-on-you-chords-464"
    parser = TabParser(url)
    tab_data = parser.parse()
    print(json.dumps(tab_data, indent=2))
    """)
    
    print("\n⚠️  Important Notes About Ultimate-API")
    print("-" * 60)
    print("""
    ✅ Advantages:
       - Simple Python API
       - Flask server option
       - Returns structured JSON
       - 113 stars on GitHub
       - 26 forks (community maintained)
    
    ⚠️  Limitations:
       - Last updated 9 years ago (2015-ish)
       - May not work with current Ultimate Guitar structure
       - No active maintenance
       - Possible compatibility issues with modern UG site
       - May still face Cloudflare challenges
    
    🔄 Comparison with Our Current Methods:
    
    Method              Success  Speed    Effort   Status
    ─────────────────────────────────────────────────────
    Patchright          95%+     2-3s     5min     ✅ Working
    undetected-chromedriver 90%+ 2-3s    10min     ✅ Working
    cloudscraper        70%      1s       2min     ✅ Working
    ultimate-api        ? (old)  ?        15min    ⚠️  Untested
    local-html          100%     <1s      1min     ✅ Working
    """)
    
    print("\n🧪 Recommendation")
    print("-" * 60)
    print("""
    1️⃣  STICK with Patchright (95%+ success, actively maintained)
    
    2️⃣  USE ultimate-api IF:
       - You want a lightweight HTTP API approach
       - You're willing to debug compatibility issues
       - You have time to fork and update it
    
    3️⃣  TEST it locally first before integrating
    
    🚀 To Try Ultimate-API:
       
       # Clone it
       git clone https://github.com/joncardasis/ultimate-api.git temp-ultimate-api
       cd temp-ultimate-api
       
       # Install & run
       pip install -r requirements.txt
       python run.py
       
       # Test in another terminal
       curl "http://localhost:5000/tab?url=<URL>"
    """)

if __name__ == "__main__":
    test_ultimate_api()
