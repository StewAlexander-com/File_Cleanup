#!/usr/bin/env python3
"""
File Organizer - OS-agnostic file sorting utility
Organizes files by extension into dedicated folders with logging and duplicate handling.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from directory_browser import get_directory_path


def get_file_extension(file_path: Path) -> str:
    """Extract lowercase extension without dot, or 'no_extension' if none."""
    ext = file_path.suffix.lower()
    return ext[1:] if ext else 'no_extension'


def organize_files(directory: Path) -> dict:
    """
    Organize files in directory by extension into folders.

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

        # Move each file, handling name conflicts interactively
        for file in files:
            destination = folder_path / file.name

            # Prompt user on duplicate files, append '_copyN' if they decline overwrite
            if destination.exists():
                response = input(f"\n⚠ '{file.name}' exists in {ext}/. Overwrite? (y/n): ").lower()
                if response != 'y':
                    # Generate unique filename: name_copy1.ext, name_copy2.ext, etc.
                    stem = destination.stem
                    suffix = destination.suffix
                    copy_num = 1
                    while destination.exists():
                        destination = folder_path / f"{stem}_copy{copy_num}{suffix}"
                        copy_num += 1

            shutil.move(str(file), str(destination))
            moved_files[ext].append(destination.name)
            print(f"  → {file.name}")

    return moved_files, folder_status


def verify_organization(directory: Path) -> bool:
    """
    Recursively verify all files are in correctly named folders.

    Returns:
        bool: True if all files are properly organized
    """
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
        print("✗ Issues found:")
        for issue in misplaced:
            print(f"  • {issue}")
        return False
    else:
        print("✓ All files organized correctly")
        return True


def create_log(directory: Path, moved_files: dict, folder_status: dict) -> None:
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

    print(f"\n✓ Log updated: {log_path.name}")


def main():
    """Main execution flow."""
    print("File Organizer v1.0")
    print("=" * 60)

    # Get target directory from user using TUI browser or manual input
    directory = get_directory_path()
    
    if directory is None:
        print("\n⚠ Cancelled by user")
        return

    # Validate directory exists before proceeding
    if not directory.exists() or not directory.is_dir():
        print(f"✗ Error: '{directory}' is not a valid directory")
        return

    print(f"\nOrganizing: {directory.name}/")
    print("-" * 60)

    # Step 1: Sort files into extension-based folders
    moved_files, folder_status = organize_files(directory)

    if not moved_files:
        print("\n→ No files to organize")
        return

    # Step 2: Recursively verify correct organization
    is_organized = verify_organization(directory)

    # Step 3: Append to single log file (maintains history)
    create_log(directory, moved_files, folder_status)

    print("\n" + "=" * 60)
    print("✓ Organization complete")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Cancelled by user")
    except Exception as e:
        print(f"\n✗ Error: {e}")