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

# Ensure dependencies (Flask) are present so they are bundled
python3 -m pip install --upgrade pip >/dev/null 2>&1 || true
python3 -m pip install -r requirements.txt

pyinstaller \
  --onefile \
  --windowed \
  --name "Mac File Cleanup" \
  --add-data "templates:templates" \
  gui_launcher.py

echo ""
echo "Build complete."
echo "Launch via: dist/Mac File Cleanup"
echo "(double-clickable app that starts the web UI on localhost)"

