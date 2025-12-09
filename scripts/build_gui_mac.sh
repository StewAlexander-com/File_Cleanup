#!/usr/bin/env bash
set -euo pipefail

# Build a double-clickable macOS app bundle for the web UI using PyInstaller.
# This keeps the existing CLI/TUI untouched. Output goes to dist/EasyFileCleanupGUI.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

# Ensure dependencies (Flask) are present so they are bundled
python3 -m pip install --upgrade pip >/dev/null 2>&1 || true
python3 -m pip install -r requirements.txt
python3 -m pip install pyinstaller >/dev/null 2>&1 || true

# Clean up previous builds
echo "Cleaning up previous build artifacts..."
rm -rf build dist "Mac File Cleanup.spec"

# Build the .app bundle (without --onefile for proper macOS app structure)
python3 -m PyInstaller \
  --windowed \
  --name "Mac File Cleanup" \
  --add-data "templates:templates" \
  gui_launcher.py

# Create zip file for distribution
echo ""
echo "Creating distribution zip..."
ditto -c -k --keepParent "dist/Mac File Cleanup.app" "Mac-File-Cleanup.zip"

echo ""
echo "Build complete."
echo "Launch via: dist/Mac File Cleanup.app"
echo "Distribution zip: Mac-File-Cleanup.zip"
echo "(double-clickable app that starts the web UI on localhost)"

