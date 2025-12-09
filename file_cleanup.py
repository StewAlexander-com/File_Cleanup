#!/usr/bin/env python3
"""
File Organizer - OS-agnostic file sorting utility
Organizes files by extension into dedicated folders with logging and duplicate handling.
"""

import os
import sys
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


def organize_files(directory: Path, non_interactive: bool = False, overwrite: bool = False, quiet: bool = False) -> dict:
    """
    Organize files in directory by extension into folders.

    Args:
        directory: Directory path to organize
        non_interactive: If True, automatically create copies instead of prompting (default: False)
        overwrite: If True, automatically overwrite duplicates (default: False)
                   Note: overwrite takes precedence over non_interactive
        quiet: If True, suppress all output (default: False)

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
            if not quiet:
                print(f"✓ Created: {ext}/")
        else:
            if not quiet:
                print(f"→ Using: {ext}/")

        # Move each file, handling name conflicts
        for file in files:
            destination = folder_path / file.name

            # Handle duplicate files based on mode
            if destination.exists():
                if overwrite:
                    # Auto-overwrite mode
                    if not quiet:
                        print(f"  → {file.name} (overwriting existing)")
                elif non_interactive:
                    # Auto-create copy mode
                    stem = destination.stem
                    suffix = destination.suffix
                    copy_num = 1
                    while destination.exists():
                        destination = folder_path / f"{stem}_copy{copy_num}{suffix}"
                        copy_num += 1
                    if not quiet:
                        print(f"  → {file.name} (created {destination.name})")
                else:
                    # Interactive mode - prompt user (should not happen in automation)
                    # Safety check: if non_interactive is False but we're in automation context,
                    # default to creating copy to avoid hanging
                    if non_interactive:
                        # This should never happen, but safety fallback
                        response = 'n'
                    elif not quiet:
                        response = input(f"\n⚠ '{file.name}' exists in {ext}/. Overwrite? (y/n): ").lower()
                    else:
                        # In quiet mode without non_interactive, default to creating copy
                        response = 'n'
                    if response != 'y':
                        # Generate unique filename: name_copy1.ext, name_copy2.ext, etc.
                        stem = destination.stem
                        suffix = destination.suffix
                        copy_num = 1
                        while destination.exists():
                            destination = folder_path / f"{stem}_copy{copy_num}{suffix}"
                            copy_num += 1
                        if not quiet:
                            print(f"  → {file.name} (created {destination.name})")
                    else:
                        if not quiet:
                            print(f"  → {file.name} (overwriting existing)")

            else:
                if not quiet:
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


def find_similar_flags(invalid_arg: str, valid_flags: list) -> list:
    """
    Find flags similar to the invalid argument (for typo suggestions).
    
    Args:
        invalid_arg: The invalid flag that was entered
        valid_flags: List of valid flag names (without -- prefix)
    
    Returns:
        List of similar flags, sorted by similarity
    """
    if not invalid_arg or not invalid_arg.startswith('--'):
        return []
    
    invalid_arg = invalid_arg[2:]  # Remove '--' prefix
    suggestions = []
    
    for flag in valid_flags:
        # Check for partial matches
        if invalid_arg in flag or flag in invalid_arg:
            suggestions.append(flag)
        # Check for similar length and character overlap
        elif abs(len(invalid_arg) - len(flag)) <= 2:
            # Simple similarity: count matching characters
            matches = sum(1 for a, b in zip(invalid_arg, flag) if a == b)
            if matches >= min(len(invalid_arg), len(flag)) * 0.6:  # 60% similarity
                suggestions.append(flag)
    
    return suggestions[:3]  # Return top 3 suggestions


class CustomArgumentParser(argparse.ArgumentParser):
    """
    Custom ArgumentParser that provides helpful error messages for invalid flags.
    """
    
    def error(self, message):
        """
        Override error method to provide user-friendly flag suggestions.
        
        Args:
            message: The error message from argparse
        """
        # Check if the error is about an unknown argument (invalid flag)
        if 'unrecognized arguments' in message.lower() or 'invalid choice' in message.lower():
            # Extract the invalid argument from the error message
            invalid_arg = None
            if 'unrecognized arguments:' in message:
                invalid_arg = message.split('unrecognized arguments:')[-1].strip().split()[0]
            
            # Define all valid flags
            valid_flags = ['html', 'tui', 'yes', 'non-interactive', 'overwrite', 'quiet', 'help']
            
            print(f"\n✗ Error: Unknown flag or option")
            if invalid_arg:
                print(f"   '{invalid_arg}' is not a valid option.\n")
                
                # Try to suggest similar flags
                suggestions = find_similar_flags(invalid_arg, valid_flags)
                if suggestions:
                    print("💡 Did you mean one of these?")
                    for sug in suggestions:
                        print(f"   --{sug}")
                    print()
            else:
                print(f"   {message}\n")
            
            print("=" * 70)
            print("Available Flags:")
            print("=" * 70)
            print("\n  Interface Options:")
            print("    --html              Launch web-based GUI interface")
            print("                        (Requires Flask: pip install Flask)")
            print("    --tui               Launch terminal user interface")
            print("                        (ncurses directory browser)")
            print("\n  Duplicate Handling:")
            print("    --yes               Non-interactive: auto-create copies for duplicates")
            print("    --non-interactive   Same as --yes")
            print("    --overwrite         Auto-overwrite duplicate files (use with caution)")
            print("\n  Output Control:")
            print("    --quiet             Minimal output (useful for automation)")
            print("\n  Help:")
            print("    --help, -h          Show comprehensive help documentation")
            print("\n" + "=" * 70)
            print("\n💡 Quick Examples:")
            print("   %s --html              # Launch web interface" % self.prog)
            print("   %s --tui               # Launch terminal interface" % self.prog)
            print("   %s Downloads --yes     # Organize with auto-copy for duplicates" % self.prog)
            print("   %s --help              # Show full help\n" % self.prog)
            
            self.exit(2, "")
        else:
            # For other errors, use default argparse behavior
            super().error(message)


def main():
    """
    Main execution flow for file cleanup application.
    
    Handles command-line argument parsing, directory selection, file organization,
    and web interface launching. Returns appropriate exit codes for automation.
    
    Returns:
        int: Exit code (0 for success, 1 for error, 130 for KeyboardInterrupt)
    """
    parser = CustomArgumentParser(
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

  Terminal User Interface (TUI):
    %(prog)s --tui                           # Launch ncurses directory browser
    %(prog)s --tui ~/Downloads               # Start TUI from specific directory

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

  # Terminal user interface (ncurses directory browser)
  %(prog)s --tui

  # Automated cleanup
  %(prog)s Downloads --yes --quiet

  # Get help
  %(prog)s --help

For more information, visit: https://github.com/StewAlexander-com/File_Cleanup
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
    parser.add_argument(
        '--tui',
        action='store_true',
        help='Launch terminal user interface (ncurses directory browser) for directory selection'
    )
    
    args = parser.parse_args()
    
    # Validate flag combinations for automation
    automation_flags = ['--yes', '--non-interactive', '--overwrite', '--quiet']
    interactive_flags = ['--html', '--tui']
    
    # Check for conflicting flags (automation + interactive)
    has_automation = args.yes or args.non_interactive or args.overwrite or args.quiet
    has_interactive = args.html or args.tui
    
    if has_automation and has_interactive:
        parser.error(
            "Cannot combine automation flags (--yes, --non-interactive, --overwrite, --quiet) "
            "with interactive flags (--html, --tui).\n"
            "For automation, use: %(prog)s <directory> --yes --quiet\n"
            "For interactive use, use: %(prog)s --html or %(prog)s --tui"
        )
    
    # If --tui flag is set, launch TUI directory browser
    if args.tui:
        from directory_browser import browse_directory
        
        if not args.quiet:
            print("File Organizer v1.1")
            print("=" * 60)
            print("\n📂 Terminal User Interface - Directory Browser")
            print("=" * 60)
            print("\nNavigate directories and press 's' to select a directory for cleanup.")
            print("Press 'q' or ESC to cancel.\n")
        
        # Start browsing from the provided directory or home directory
        start_path = None
        if args.directory:
            start_path = find_directory_by_partial_path(args.directory)
            if start_path:
                if not args.quiet:
                    print(f"Starting from: {start_path}\n")
            else:
                if not args.quiet:
                    print(f"⚠ Could not find directory matching: {args.directory}")
                    print("Starting TUI from home directory instead.\n")
        
        directory = browse_directory(start_path)
        
        if directory is None:
            if not args.quiet:
                print("\n⚠ Cancelled by user")
            return 1
        
        if not args.quiet:
            print(f"\n✓ Selected directory: {directory}")
            print(f"\nOrganizing: {directory.name}/")
            print("-" * 60)
        
        # Proceed with file organization
        non_interactive = args.yes or args.non_interactive
        moved_files, folder_status = organize_files(directory, non_interactive=non_interactive, overwrite=args.overwrite, quiet=args.quiet)
        
        if not moved_files:
            if not args.quiet:
                print("\n→ No files to organize")
            return 0
        
        # Verify organization
        is_organized = verify_organization(directory, quiet=args.quiet)
        
        # Create log
        create_log(directory, moved_files, folder_status, quiet=args.quiet)
        
        if not args.quiet:
            print("\n" + "=" * 60)
            print("✓ Organization complete")
        
        return 0 if is_organized else 1
    
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
    # If non-interactive and no directory provided, fail fast with clear error
    if not args.directory and non_interactive:
        if not args.quiet:
            parser.error("Directory path required in non-interactive mode. Use --help for usage.")
        else:
            # In quiet mode, just return error code without argparse error message
            return 1
    
    # In non-interactive mode, skip interactive prompts and fail fast on errors
    if non_interactive and args.directory:
        directory = find_directory_by_partial_path(args.directory)
        if not directory:
            if not args.quiet:
                print(f"✗ Could not find directory matching: {args.directory}", file=sys.stderr)
            return 1
        if not args.quiet:
            print(f"✓ Found directory: {directory}")
    else:
        # Interactive mode - but if quiet is set, we should still try to be non-interactive
        if args.quiet and args.directory:
            # Quiet mode with directory: treat as non-interactive
            directory = find_directory_by_partial_path(args.directory)
            if not directory:
                print(f"✗ Could not find directory matching: {args.directory}", file=sys.stderr)
                return 1
        else:
            directory = get_directory_from_args_or_input(args.directory)
    
    if directory is None:
        if not args.quiet:
            print("\n⚠ Cancelled by user")
        return 1

    # Validate directory exists before proceeding
    if not directory.exists() or not directory.is_dir():
        if not args.quiet:
            print(f"✗ Error: '{directory}' is not a valid directory", file=sys.stderr)
        else:
            # In quiet mode, still output critical errors to stderr
            print(f"Error: '{directory}' is not a valid directory", file=sys.stderr)
        return 1

    if not args.quiet:
        print(f"\nOrganizing: {directory.name}/")
        print("-" * 60)

    # Step 1: Sort files into extension-based folders
    moved_files, folder_status = organize_files(directory, non_interactive=non_interactive, overwrite=args.overwrite, quiet=args.quiet)

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