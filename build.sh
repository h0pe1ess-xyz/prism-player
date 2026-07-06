#!/bin/bash
echo "🚀 Building Prism Player..."

# Check if pyinstaller is installed
if ! command -v pyinstaller &> /dev/null
then
    echo "📦 PyInstaller not found. Installing..."
    pip install pyinstaller
fi

# Build
pyinstaller --name prism_player \
    --onefile \
    --hidden-import=mutagen \
    --hidden-import=pydbus \
    --hidden-import=pypresence \
    --hidden-import=yt_dlp \
    --hidden-import=blessed \
    main.py

echo "✅ Build complete! You can find the binary in the 'dist' folder."
