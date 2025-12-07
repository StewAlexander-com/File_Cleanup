#!/usr/bin/env python3
"""
Easy File Cleanup - Friendly entry script for the file organizer.

This script is a thin wrapper around the underlying `file_cleanup` module.
It exists so you can run `Easy-File-Cleanup.py` directly from the command line
while keeping a valid Python module name (`file_cleanup`) for imports and tests.

QUICK START:
    # Organize files in a directory
    python3 Easy-File-Cleanup.py ~/Downloads

    # Launch web interface
    python3 Easy-File-Cleanup.py --html

    # Get help
    python3 Easy-File-Cleanup.py --help

For detailed usage information, run with --help flag.
"""

import sys
from file_cleanup import main


if __name__ == "__main__":
    # Check for help flag first to provide immediate help
    if '--help' in sys.argv or '-h' in sys.argv:
        # Let argparse handle the help display
        # This will show comprehensive help from file_cleanup.main()
        pass
    
    # Delegate all logic to the main() function in file_cleanup.py
    # main() already returns an appropriate exit code for automation.
    # argparse will automatically handle --help and -h flags.
    exit_code = main()
    sys.exit(exit_code if exit_code is not None else 0)


