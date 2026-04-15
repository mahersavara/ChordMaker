#!/bin/bash

# ChordMaker GitHub Repository Setup

echo "🎸 ChordMaker GitHub Setup"
echo "=================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "Initializing git repository..."
    git init
else
    echo "Git repository already initialized"
fi

echo ""
echo "📋 Next Steps:"
echo "1. Create a new repository on GitHub (https://github.com/new)"
echo "2. Copy the repository URL"
echo "3. Run: git remote add origin <YOUR_REPO_URL>"
echo "4. Run: git branch -M main"
echo "5. Run: git add ."
echo "6. Run: git commit -m 'Initial commit: ChordMaker project setup'"
echo "7. Run: git push -u origin main"
echo ""
echo "📝 Don't forget to:"
echo "   - Update package.json with your username"
echo "   - Update README.md with project details"
echo "   - Update SETUP.md with installation instructions"
echo "   - Add GitHub repository URL to README"
echo ""
echo "Happy coding! 🎸"
