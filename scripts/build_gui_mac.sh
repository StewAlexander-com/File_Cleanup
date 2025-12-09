#!/usr/bin/env bash
set -euo pipefail

# Build a double-clickable macOS app bundle for the web UI using PyInstaller.
# This keeps the existing CLI/TUI untouched. Output goes to dist/EasyFileCleanupGUI.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v pyinstaller >/dev/null 2>&1; then
  echo "PyInstaller is not installed. Install with: pip install pyinstaller"
  exit 1
fi

pyinstaller \
  --onefile \
  --windowed \
  --name "EasyFileCleanupGUI" \
  --add-data "templates:templates" \
  gui_launcher.py

echo ""
echo "Build complete."
echo "Launch via: dist/EasyFileCleanupGUI"
echo "(double-clickable app that starts the web UI on localhost)"

