#!/usr/bin/env python3
"""
File Organizer - OS-agnostic file sorting utility
Organizes files by extension into dedicated folders with logging and duplicate handling.
"""

import os
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Optional
from directory_browser import get_directory_path


def get_file_extension(file_path: Path) -> str:
    """Extract lowercase extension without dot, or 'no_extension' if none."""
    ext = file_path.suffix.lower()
    return ext[1:] if ext else 'no_extension'


def find_directory_by_partial_path(partial_path: str) -> Optional[Path]:
    """
    Find a directory by partial path match.
    Tries exact match first, then searches in common locations.
    
    Args:
        partial_path: Partial path string to search for
    
    Returns:
        Path to found directory or None if not found
    """
    partial_lower = partial_path.lower()
    
    # First, try exact match or expanduser/resolve
    try:
        exact_path = Path(partial_path).expanduser().resolve()
        if exact_path.exists() and exact_path.is_dir():
            return exact_path
    except Exception:
        pass
    
    # Search in common locations (current directory, home, and immediate subdirectories)
    search_locations = [
        Path('.').resolve(),  # Current directory
        Path.home(),  # Home directory
    ]
    
    matches = []
    
    for location in search_locations:
        if not location.exists():
            continue
        
        try:
            # Check if location itself matches
            if partial_lower in str(location).lower() or partial_lower in location.name.lower():
                matches.append(location)
            
            # Check immediate subdirectories (one level deep)
            for item in location.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    # Check if name matches
                    if partial_lower in item.name.lower():
                        matches.append(item)
                    # Check if full path matches
                    elif partial_lower in str(item).lower():
                        matches.append(item)
        except (PermissionError, OSError):
            continue
    
    # If no matches in common locations, try a limited search in home directory
    if not matches:
        try:
            home = Path.home()
            # Search one level deeper in home directory
            for item in home.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    if partial_lower in item.name.lower():
                        matches.append(item)
                    else:
                        # Check subdirectories one level deep
                        try:
                            for subitem in item.iterdir():
                                if subitem.is_dir() and not subitem.name.startswith('.'):
                                    if partial_lower in subitem.name.lower() or partial_lower in str(subitem).lower():
                                        matches.append(subitem)
                        except (PermissionError, OSError):
                            continue
        except (PermissionError, OSError):
            pass
    
    # Return the most specific match (longest path that contains the partial)
    if matches:
        # Sort by path length (longest first) to get most specific match
        matches.sort(key=lambda p: len(str(p)), reverse=True)
        return matches[0]
    
    return None


def organize_files(directory: Path, non_interactive: bool = False, overwrite: bool = False) -> dict:
    """
    Organize files in directory by extension into folders.

    Args:
        directory: Directory path to organize
        non_interactive: If True, automatically create copies instead of prompting (default: False)
        overwrite: If True, automatically overwrite duplicates (default: False)
                   Note: overwrite takes precedence over non_interactive

    Returns:
        dict: Mapping of folder names to list of files moved
    """
    files_by_type = defaultdict(list)
    moved_files = defaultdict(list)
    folder_status = {}  # Track if folder was created or existed

    # Scan directory and group files by extension (ignores hidden files starting with '.')
    for item in directory.iterdir():
        if item.is_file() and not item.name.startswith('.'):
            ext = get_file_extension(item)
            files_by_type[ext].append(item)

    # Create extension folders and move files into them
    for ext, files in files_by_type.items():
        folder_path = directory / ext
        folder_existed = folder_path.exists()
        folder_status[ext] = folder_existed

        # Create folder only if it doesn't exist, otherwise reuse existing
        if not folder_existed:
            folder_path.mkdir(exist_ok=True)
            print(f"✓ Created: {ext}/")
        else:
            print(f"→ Using: {ext}/")

        # Move each file, handling name conflicts
        for file in files:
            destination = folder_path / file.name

            # Handle duplicate files based on mode
            if destination.exists():
                if overwrite:
                    # Auto-overwrite mode
                    print(f"  → {file.name} (overwriting existing)")
                elif non_interactive:
                    # Auto-create copy mode
                    stem = destination.stem
                    suffix = destination.suffix
                    copy_num = 1
                    while destination.exists():
                        destination = folder_path / f"{stem}_copy{copy_num}{suffix}"
                        copy_num += 1
                    print(f"  → {file.name} (created {destination.name})")
                else:
                    # Interactive mode - prompt user
                    response = input(f"\n⚠ '{file.name}' exists in {ext}/. Overwrite? (y/n): ").lower()
                    if response != 'y':
                        # Generate unique filename: name_copy1.ext, name_copy2.ext, etc.
                        stem = destination.stem
                        suffix = destination.suffix
                        copy_num = 1
                        while destination.exists():
                            destination = folder_path / f"{stem}_copy{copy_num}{suffix}"
                            copy_num += 1
                        print(f"  → {file.name} (created {destination.name})")
                    else:
                        print(f"  → {file.name} (overwriting existing)")

            else:
                print(f"  → {file.name}")

            shutil.move(str(file), str(destination))
            moved_files[ext].append(destination.name)

    return moved_files, folder_status


def verify_organization(directory: Path, quiet: bool = False) -> bool:
    """
    Recursively verify all files are in correctly named folders.

    Args:
        directory: Directory to verify
        quiet: If True, suppress output

    Returns:
        bool: True if all files are properly organized
    """
    if not quiet:
        print("\n--- Verification ---")
    misplaced = []

    # Walk directory tree checking file placement
    for root, dirs, files in os.walk(directory):
        root_path = Path(root)

        # Top-level directory should only contain folders (and log files)
        if root_path == directory:
            for file in files:
                if not file.startswith('organization_log'):
                    misplaced.append(f"Top level: {file}")
        else:
            # Files must be in folders matching their extension
            folder_name = root_path.name
            for file in files:
                file_ext = get_file_extension(Path(file))
                if file_ext != folder_name:
                    misplaced.append(f"{file} in {folder_name}/ (should be in {file_ext}/)")

    # Report verification results
    if misplaced:
        if not quiet:
            print("✗ Issues found:")
            for issue in misplaced:
                print(f"  • {issue}")
        return False
    else:
        if not quiet:
            print("✓ All files organized correctly")
        return True


def create_log(directory: Path, moved_files: dict, folder_status: dict, quiet: bool = False) -> None:
    """Append organization details to single log file."""
    log_path = directory / "organization_log.txt"

    # Append mode keeps history from all runs
    with open(log_path, 'a') as log:
        # Format date as "14 Nov 2025" for readability
        date_formatted = datetime.now().strftime("%d %b %Y")
        time_formatted = datetime.now().strftime("%H:%M:%S")

        # Write compact header with timestamp
        log.write(f"\n{'=' * 60}\n")
        log.write(f"[{date_formatted} @ {time_formatted}] {directory.name}/\n")
        log.write(f"{'=' * 60}\n")

        # List each folder and the files moved into it
        for folder in sorted(moved_files.keys()):
            files = moved_files[folder]
            status = "NEW" if not folder_status[folder] else "EXISTING"

            log.write(f"\n[{folder}/] {status} • {len(files)} file(s)\n")
            for file in sorted(files):
                log.write(f"  → {file}\n")

    if not quiet:
        print(f"\n✓ Log updated: {log_path.name}")


def get_directory_from_args_or_input(args_path: Optional[str] = None) -> Optional[Path]:
    """
    Get directory path from command-line argument or user input.
    
    Args:
        args_path: Directory path from command-line arguments (can be partial)
    
    Returns:
        Path to directory or None if cancelled/invalid
    """
    if args_path:
        # Try to find directory by partial or full path
        directory = find_directory_by_partial_path(args_path)
        
        if directory:
            print(f"✓ Found directory: {directory}")
            return directory
        else:
            print(f"✗ Could not find directory matching: {args_path}")
            print("Please try again with a more specific path or use interactive mode.")
            return None
    
    # No command-line argument, use simplified interactive mode
    print("\nEnter directory path (or press Enter for current directory):")
    path_input = input("Path: ").strip()
    
    if not path_input:
        # Default to current directory
        directory = Path('.').resolve()
        print(f"→ Using current directory: {directory}")
    else:
        # Try to find directory by partial or full path
        directory = find_directory_by_partial_path(path_input)
        
        if not directory:
            print(f"✗ Could not find directory matching: {path_input}")
            print("\nWould you like to:")
            print("  [1] Try browsing directories")
            print("  [2] Cancel")
            choice = input("\nEnter choice: ").strip().lower()
            
            if choice == '1':
                directory = get_directory_path()
            else:
                return None
    
    return directory


def main():
    """
    Main execution flow for file cleanup application.
    
    Handles command-line argument parsing, directory selection, file organization,
    and web interface launching. Returns appropriate exit codes for automation.
    
    Returns:
        int: Exit code (0 for success, 1 for error, 130 for KeyboardInterrupt)
    """
    parser = argparse.ArgumentParser(
        prog='Easy-File-Cleanup.py',
        description='File Organizer - Organizes files by extension into dedicated folders',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=True,
        epilog="""
USAGE EXAMPLES:
  Basic Usage:
    %(prog)s /path/to/directory              # Organize specific directory
    %(prog)s Downloads                       # Find and organize Downloads folder
    %(prog)s ~/Documents                     # Organize Documents in home directory
    %(prog)s                                 # Interactive mode (prompts for directory)
    %(prog)s --help                          # Show this help message

  Automation/Non-Interactive Mode:
    %(prog)s Downloads --yes                 # Auto-create copies for duplicates (scriptable)
    %(prog)s Downloads --non-interactive     # Same as --yes
    %(prog)s Downloads --overwrite           # Auto-overwrite duplicates (use with caution)
    %(prog)s Downloads --quiet               # Minimal output (for scripts)

  Web Interface:
    %(prog)s --html                          # Launch web-based GUI interface
                                             # (Requires Flask: pip install Flask)

  Combined Options:
    %(prog)s ~/Downloads --yes --quiet       # Fully automated, minimal output

DIRECTORY SELECTION:
  - Full path: /Users/name/Downloads
  - Partial path: Downloads (searches current dir and home)
  - Home shortcut: ~/Documents
  - Current directory: . or leave empty in interactive mode

DUPLICATE HANDLING:
  - Interactive (default): Prompts for each duplicate
  - --yes/--non-interactive: Automatically creates copies (file_copy1.ext, etc.)
  - --overwrite: Automatically overwrites existing files (use with caution)

OUTPUT:
  - Creates extension-based folders (pdf/, jpg/, txt/, etc.)
  - Files without extensions go to no_extension/
  - Generates organization_log.txt with history
  - Verifies organization after completion

INSTALLATION:
  - No installation required (uses Python standard library)
  - For web interface: pip install Flask
  - Make executable: chmod +x Easy-File-Cleanup.py

EXAMPLES:
  # Quick organize
  %(prog)s ~/Downloads

  # Web interface
  %(prog)s --html

  # Automated cleanup
  %(prog)s Downloads --yes --quiet

  # Get help
  %(prog)s --help

For more information, visit: https://github.com/stewartalexander/File_Cleanup
        """
    )
    parser.add_argument(
        'directory',
        nargs='?',
        help='Directory path to organize (full path, partial name, or ~/path)'
    )
    parser.add_argument(
        '--yes',
        action='store_true',
        help='Non-interactive mode: automatically create copies for duplicates (scriptable)'
    )
    parser.add_argument(
        '--non-interactive',
        action='store_true',
        dest='non_interactive',
        help='Same as --yes: automatically create copies for duplicates'
    )
    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='Automatically overwrite duplicate files (use with caution)'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Minimal output (useful for automation scripts)'
    )
    parser.add_argument(
        '--html',
        action='store_true',
        help='Launch web-based GUI interface (requires Flask: pip install Flask)'
    )
    
    args = parser.parse_args()
    
    # If --html flag is set, launch web interface
    if args.html:
        try:
            from web_interface import run_server
        except ImportError as e:
            error_msg = str(e).lower()
            if 'flask' in error_msg or 'web_interface' in error_msg:
                if not args.quiet:
                    print("\n" + "=" * 60)
                    print("✗ Flask is required for web interface mode")
                    print("=" * 60)
                    print("\n📦 INSTALLATION INSTRUCTIONS:")
                    print("\n  Option 1: Install Flask only")
                    print("    pip install Flask")
                    print("\n  Option 2: Install from requirements file")
                    print("    pip install -r requirements.txt")
                    print("\n" + "-" * 60)
                    print("ℹ️  NOTE: The script works normally without --html flag.")
                    print("   You can use all CLI features without Flask installed.")
                    print("=" * 60 + "\n")
            else:
                if not args.quiet:
                    print(f"\n✗ Error importing web interface: {e}\n")
            return 1
        except Exception as e:
            if not args.quiet:
                print(f"\n✗ Error loading web interface: {e}\n")
            return 1
        
        run_server()
        return 0
    
    # Determine non-interactive mode
    non_interactive = args.yes or args.non_interactive
    
    if not args.quiet:
        print("File Organizer v1.1")
        print("=" * 60)

    # Get target directory from command-line argument or user input
    # If non-interactive and no directory provided, fail
    if not args.directory and non_interactive:
        parser.error("Directory path required in non-interactive mode. Use --help for usage.")
    
    # In non-interactive mode, skip interactive prompts
    if non_interactive and args.directory:
        directory = find_directory_by_partial_path(args.directory)
        if not directory:
            if not args.quiet:
                print(f"✗ Could not find directory matching: {args.directory}")
            return 1
        if not args.quiet:
            print(f"✓ Found directory: {directory}")
    else:
        directory = get_directory_from_args_or_input(args.directory)
    
    if directory is None:
        if not args.quiet:
            print("\n⚠ Cancelled by user")
        return 1

    # Validate directory exists before proceeding
    if not directory.exists() or not directory.is_dir():
        if not args.quiet:
            print(f"✗ Error: '{directory}' is not a valid directory")
        return 1

    if not args.quiet:
        print(f"\nOrganizing: {directory.name}/")
        print("-" * 60)

    # Step 1: Sort files into extension-based folders
    moved_files, folder_status = organize_files(directory, non_interactive=non_interactive, overwrite=args.overwrite)

    if not moved_files:
        if not args.quiet:
            print("\n→ No files to organize")
        return 0

    # Step 2: Recursively verify correct organization
    is_organized = verify_organization(directory, quiet=args.quiet)

    # Step 3: Append to single log file (maintains history)
    create_log(directory, moved_files, folder_status, quiet=args.quiet)

    if not args.quiet:
        print("\n" + "=" * 60)
        print("✓ Organization complete")
    
    return 0 if is_organized else 1


if __name__ == "__main__":
    import sys
    try:
        exit_code = main()
        sys.exit(exit_code if exit_code is not None else 0)
    except KeyboardInterrupt:
        print("\n\n⚠ Cancelled by user")
        sys.exit(130)  # Standard exit code for Ctrl+C
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)