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
import os
import traceback
from pathlib import Path

# Ensure we can find our modules when running from PyInstaller bundle
if hasattr(sys, '_MEIPASS'):
    # Running from PyInstaller bundle
    # Add the bundle directory to path so we can import our modules
    bundle_dir = Path(sys._MEIPASS)
    if str(bundle_dir) not in sys.path:
        sys.path.insert(0, str(bundle_dir))
else:
    # Running from source - add parent directory to path
    script_dir = Path(__file__).parent
    if str(script_dir) not in sys.path:
        sys.path.insert(0, str(script_dir))


def log_error(message: str, exc: Exception = None) -> None:
    """Log errors to a file for debugging windowed apps."""
    log_file = Path.home() / "Mac-File-Cleanup-errors.log"
    try:
        with open(log_file, "a") as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"{message}\n")
            if exc:
                f.write(f"Error: {exc}\n")
                f.write(traceback.format_exc())
            f.write(f"{'='*60}\n")
    except Exception:
        pass  # If we can't write logs, at least try to show the error


def main() -> int:
    """Launch the Flask web interface."""
    try:
        # Explicitly import our modules to ensure PyInstaller includes them
        import file_cleanup  # noqa: F401
        import directory_browser  # noqa: F401
        from web_interface import run_server
    except ImportError as exc:  # Flask not installed
        error_msg = (
            "\n✗ Flask is required for the desktop launcher.\n"
            "  If you downloaded the packaged app, Flask should already be bundled.\n"
            "  Please re-download the release asset.\n"
            "\n  If running from source, install with:\n"
            "    pip install Flask\n"
            "  (The CLI still works without Flask.)\n"
        )
        print(error_msg)
        log_error("ImportError: Flask not found", exc)
        return 1
    except Exception as exc:  # Other import issues
        error_msg = f"\n✗ Failed to load web interface: {exc}\n"
        print(error_msg, file=sys.stderr)
        log_error("Failed to import web_interface", exc)
        return 1

    try:
        run_server()
        return 0
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        return 130
    except Exception as exc:
        error_msg = f"\n✗ Failed to start web interface: {exc}\n"
        print(error_msg, file=sys.stderr)
        log_error("Failed to start web server", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())

