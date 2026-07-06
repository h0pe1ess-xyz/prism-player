#!/bin/bash
# Install PyInstaller if you don't have it:
# pip install pyinstaller

echo "Building Prism Player binary..."
pyinstaller --onefile --name prism-player --collect-all ytmusicapi --collect-all yt_dlp main.py
echo "Build complete! The binary is located at dist/prism-player"
