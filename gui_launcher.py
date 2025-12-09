#!/usr/bin/env python3
"""
Desktop launcher for the Easy File Cleanup web UI.

Purpose:
    - Provides a double-clickable entrypoint for users who prefer a GUI.
    - Intended for PyInstaller/py2app/py2exe packaging.
    - Leaves the existing CLI/TUI experience untouched.

Usage:
    python3 gui_launcher.py          # Starts the web interface (same as --html)
    pyinstaller --onefile --windowed --name "EasyFileCleanupGUI" \
        --add-data "templates:templates" gui_launcher.py

Notes:
    - The launcher only depends on Flask at runtime. If Flask is missing,
      users receive a clear instruction rather than a crash.
    - The web interface remains bound to localhost for security.
"""

import sys


def main() -> int:
    """Launch the Flask web interface."""
    try:
        from web_interface import run_server
    except ImportError as exc:  # Flask not installed
        print(
            "\n✗ Flask is required for the desktop launcher.\n"
            "  If you downloaded the packaged app, Flask should already be bundled.\n"
            "  Please re-download the release asset.\n"
            "\n  If running from source, install with:\n"
            "    pip install Flask\n"
            "  (The CLI still works without Flask.)\n"
        )
        return 1
    except Exception as exc:  # Other import issues
        print(f"\n✗ Failed to load web interface: {exc}\n", file=sys.stderr)
        return 1

    try:
        run_server()
        return 0
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        return 130
    except Exception as exc:
        print(f"\n✗ Failed to start web interface: {exc}\n", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

