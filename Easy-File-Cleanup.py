#!/usr/bin/env python3
"""
Easy File Cleanup - Friendly entry script for the file organizer.

This script is a thin wrapper around the underlying `file_cleanup` module.
It exists so you can run `Easy-File-Cleanup.py` directly from the command line
while keeping a valid Python module name (`file_cleanup`) for imports and tests.
"""

from file_cleanup import main


if __name__ == "__main__":
    # Delegate all logic to the main() function in file_cleanup.py
    # main() already returns an appropriate exit code for automation.
    import sys

    exit_code = main()
    sys.exit(exit_code if exit_code is not None else 0)


