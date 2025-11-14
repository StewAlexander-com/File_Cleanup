#!/usr/bin/env python3
"""
Directory Browser TUI - Cross-platform directory selection interface
Provides a simple file browser similar to 'nnn' for selecting directories.
"""

import os
import sys
from pathlib import Path
from typing import Optional, List, Tuple

# Try to import curses for better UI, fallback to simple mode if not available
try:
    import curses
    HAS_CURSES = True
except ImportError:
    HAS_CURSES = False


class SimpleDirectoryBrowser:
    """Simple directory browser using basic input/output (cross-platform fallback)."""
    
    def __init__(self, start_path: Optional[Path] = None):
        """Initialize browser with starting path."""
        if start_path is None:
            start_path = Path.home()
        self.current_path = Path(start_path).resolve()
        self.history = []  # For 'back' navigation
        
    def get_items(self) -> Tuple[List[Path], List[Path]]:
        """Get directories and files in current path."""
        try:
            items = sorted(self.current_path.iterdir())
            dirs = [item for item in items if item.is_dir() and not item.name.startswith('.')]
            files = [item for item in items if item.is_file()]
            return dirs, files
        except PermissionError:
            return [], []
    
    def display(self) -> str:
        """Display current directory and return selected path or command."""
        dirs, files = self.get_items()
        
        # Clear screen (cross-platform)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=" * 70)
        print("Directory Browser")
        print("=" * 70)
        print(f"\nCurrent: {self.current_path}")
        print("-" * 70)
        
        # Show parent directory option
        if self.current_path.parent != self.current_path:
            print("  [0] .. (go up)")
        else:
            print("  [0] (root directory)")
        
        # Show directories
        print("\n📁 Directories:")
        for i, d in enumerate(dirs, start=1):
            print(f"  [{i}] {d.name}/")
        
        # Show files (for reference, not selectable)
        if files:
            print(f"\n📄 Files ({len(files)} files, not selectable)")
        
        print("\n" + "-" * 70)
        print("Commands:")
        print("  [t] Type path manually")
        print("  [s] Select current directory")
        print("  [h] Go to home directory")
        print("  [q] Cancel")
        print("=" * 70)
        
        choice = input("\nEnter choice: ").strip().lower()
        return choice
    
    def navigate(self, choice: str) -> Optional[Path]:
        """Navigate based on user choice. Returns selected path or None."""
        dirs, _ = self.get_items()
        
        if choice == 'q':
            return None
        elif choice == 's':
            return self.current_path
        elif choice == 't':
            path_str = input("\nEnter directory path: ").strip()
            if not path_str:
                return None
            try:
                path = Path(path_str).expanduser().resolve()
                if path.exists() and path.is_dir():
                    return path
                else:
                    print(f"✗ Error: '{path}' is not a valid directory")
                    input("Press Enter to continue...")
                    return None
            except Exception as e:
                print(f"✗ Error: {e}")
                input("Press Enter to continue...")
                return None
        elif choice == 'h':
            self.current_path = Path.home()
            return None
        elif choice == '0':
            # Go up one directory
            if self.current_path.parent != self.current_path:
                self.current_path = self.current_path.parent
            return None
        else:
            # Try to parse as number for directory selection
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(dirs):
                    self.current_path = dirs[idx]
                    return None
                else:
                    print(f"✗ Invalid choice: {choice}")
                    input("Press Enter to continue...")
                    return None
            except ValueError:
                print(f"✗ Invalid choice: {choice}")
                input("Press Enter to continue...")
                return None
    
    def browse(self) -> Optional[Path]:
        """Main browse loop. Returns selected directory path or None."""
        while True:
            choice = self.display()
            result = self.navigate(choice)
            if result is not None:
                return result


class CursesDirectoryBrowser:
    """Directory browser using curses for better UI (Unix/macOS only)."""
    
    def __init__(self, start_path: Optional[Path] = None):
        """Initialize browser with starting path."""
        if start_path is None:
            start_path = Path.home()
        self.current_path = Path(start_path).resolve()
        self.selected_idx = 0
        self.scroll_offset = 0
        
    def get_items(self) -> List[Path]:
        """Get directories in current path."""
        try:
            items = sorted(self.current_path.iterdir())
            dirs = [item for item in items if item.is_dir() and not item.name.startswith('.')]
            return dirs
        except PermissionError:
            return []
    
    def _get_breadcrumbs(self) -> List[Path]:
        """Get list of parent directories for breadcrumb navigation."""
        breadcrumbs = []
        path = self.current_path
        while path != path.parent:
            breadcrumbs.insert(0, path)
            path = path.parent
        # Add root
        breadcrumbs.insert(0, path)
        return breadcrumbs
    
    def display(self, stdscr) -> Optional[str]:
        """Display directory browser using curses."""
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        # Get breadcrumbs for navigation
        breadcrumbs = self._get_breadcrumbs()
        
        # Header with full path
        header = f"Directory Browser"
        stdscr.addstr(0, 0, header[:width-1], curses.A_BOLD)
        stdscr.addstr(1, 0, "=" * (width - 1))
        
        # Breadcrumb navigation (clickable path)
        breadcrumb_line = 2
        path_str = str(self.current_path)
        if len(path_str) > width - 1:
            # Truncate from left if too long
            path_str = "..." + path_str[-(width-4):]
        stdscr.addstr(breadcrumb_line, 0, f"Path: {path_str}"[:width-1], curses.A_DIM)
        
        # Show breadcrumb shortcuts (1-9 keys to jump to parent levels)
        # Display shows: [1]parent [2]grandparent [3]great-grandparent etc.
        if len(breadcrumbs) > 1:
            breadcrumb_shortcuts = []
            # Show parents in reverse order (most recent first): parent, grandparent, etc.
            # We want to show up to 9 parent levels
            num_levels = min(9, len(breadcrumbs) - 1)  # -1 to exclude current
            for i in range(num_levels):
                # Go backwards from current: breadcrumbs[-2] = parent, breadcrumbs[-3] = grandparent
                bc_idx = len(breadcrumbs) - 2 - i
                if bc_idx >= 0:
                    bc = breadcrumbs[bc_idx]
                    name = bc.name if bc.name else "/"
                    breadcrumb_shortcuts.append(f"[{i+1}]{name}")
            
            if breadcrumb_shortcuts:
                shortcuts_str = " | ".join(breadcrumb_shortcuts)
                if len(shortcuts_str) > width - 1:
                    shortcuts_str = shortcuts_str[:width-1]
                stdscr.addstr(breadcrumb_line + 1, 0, shortcuts_str[:width-1], curses.A_DIM)
        
        separator_line = breadcrumb_line + (2 if len(breadcrumbs) > 1 else 1)
        stdscr.addstr(separator_line, 0, "-" * (width - 1))
        
        # Get directories
        dirs = self.get_items()
        
        # Add parent directory option
        if self.current_path.parent != self.current_path:
            dirs = [self.current_path.parent] + dirs
        
        # Navigation instructions
        instructions = [
            "↑↓: Navigate | Enter: Go into | s: Select | ←/b: Up | 1-9: Jump to level | t: Type path | h: Home | q: Quit"
        ]
        y_pos = height - len(instructions) - 1
        for i, instr in enumerate(instructions):
            stdscr.addstr(y_pos + i, 0, instr[:width-1], curses.A_DIM)
        
        # Display directories
        display_start = separator_line + 1
        display_height = y_pos - display_start - 1
        visible_dirs = dirs[self.scroll_offset:self.scroll_offset + display_height]
        
        for i, d in enumerate(visible_dirs):
            y = display_start + i
            if y >= y_pos:
                break
            
            # Highlight selected item
            attr = curses.A_REVERSE if (self.scroll_offset + i) == self.selected_idx else 0
            
            # Format display
            if d == self.current_path.parent:
                display = f"  .. (go up)"
            else:
                display = f"  📁 {d.name}/"
            
            stdscr.addstr(y, 0, display[:width-1], attr)
        
        stdscr.refresh()
        
        # Handle input
        key = stdscr.getch()
        
        if key == ord('q') or key == 27:  # q or ESC
            return None
        elif key == ord('\n') or key == ord('\r'):  # Enter - navigate into directory
            if dirs and 0 <= self.selected_idx < len(dirs):
                selected = dirs[self.selected_idx]
                if selected == self.current_path.parent:
                    # Go up to parent
                    self.current_path = selected
                    self.selected_idx = 0
                    self.scroll_offset = 0
                    return 'navigate'
                else:
                    # Navigate into the selected subdirectory
                    self.current_path = selected
                    self.selected_idx = 0
                    self.scroll_offset = 0
                    return 'navigate'
        elif key == ord('s'):  # 's' key to select current directory
            return str(self.current_path)
        elif key == curses.KEY_UP:
            if self.selected_idx > 0:
                self.selected_idx -= 1
                if self.selected_idx < self.scroll_offset:
                    self.scroll_offset = self.selected_idx
            return 'navigate'
        elif key == curses.KEY_DOWN:
            if dirs and self.selected_idx < len(dirs) - 1:
                self.selected_idx += 1
                if self.selected_idx >= self.scroll_offset + display_height:
                    self.scroll_offset = self.selected_idx - display_height + 1
            return 'navigate'
        elif key == curses.KEY_LEFT or key == ord('b'):
            if self.current_path.parent != self.current_path:
                self.current_path = self.current_path.parent
                self.selected_idx = 0
                self.scroll_offset = 0
            return 'navigate'
        elif key == ord('h'):
            self.current_path = Path.home()
            self.selected_idx = 0
            self.scroll_offset = 0
            return 'navigate'
        elif ord('1') <= key <= ord('9'):  # Number keys 1-9 to jump to breadcrumb levels
            # Recalculate breadcrumbs for navigation
            nav_breadcrumbs = self._get_breadcrumbs()
            # Map 1-9 to breadcrumb levels (1 = parent, 2 = grandparent, etc.)
            level = key - ord('1')  # 0-8
            # Calculate which breadcrumb level (from end, so 1 = parent, 2 = grandparent, etc.)
            if level < len(nav_breadcrumbs) - 1:  # -1 because we don't want to jump to current
                target_idx = len(nav_breadcrumbs) - 2 - level  # Reverse order: 1=parent, 2=grandparent
                if 0 <= target_idx < len(nav_breadcrumbs):
                    self.current_path = nav_breadcrumbs[target_idx]
                    self.selected_idx = 0
                    self.scroll_offset = 0
            return 'navigate'
        elif key == ord('t'):
            curses.endwin()
            path_str = input("\nEnter directory path: ").strip()
            if path_str:
                try:
                    path = Path(path_str).expanduser().resolve()
                    if path.exists() and path.is_dir():
                        return str(path)
                    else:
                        print(f"✗ Error: '{path}' is not a valid directory")
                        input("Press Enter to continue...")
                except Exception as e:
                    print(f"✗ Error: {e}")
                    input("Press Enter to continue...")
            return 'navigate'
        else:
            return 'navigate'
    
    def browse(self) -> Optional[Path]:
        """Main browse loop using curses. Returns selected directory path or None."""
        def _browse(stdscr):
            curses.curs_set(0)  # Hide cursor
            while True:
                result = self.display(stdscr)
                if result is None:
                    return None
                elif result != 'navigate':
                    return Path(result)
        
        try:
            return curses.wrapper(_browse)
        except KeyboardInterrupt:
            return None


def browse_directory(start_path: Optional[Path] = None) -> Optional[Path]:
    """
    Browse and select a directory using TUI.
    
    Args:
        start_path: Starting directory path (defaults to home directory)
    
    Returns:
        Selected directory Path or None if cancelled
    """
    if HAS_CURSES and sys.stdin.isatty():
        # Use curses interface if available
        browser = CursesDirectoryBrowser(start_path)
    else:
        # Use simple interface (Windows or non-interactive)
        browser = SimpleDirectoryBrowser(start_path)
    
    return browser.browse()


def get_directory_path() -> Optional[Path]:
    """
    Get directory path from user - either by typing or browsing.
    
    Returns:
        Selected directory Path or None if cancelled
    """
    print("\nHow would you like to select the directory?")
    print("  [1] Type path manually")
    print("  [2] Browse directories")
    print("  [3] Use current directory (.)")
    print("  [q] Cancel")
    
    choice = input("\nEnter choice: ").strip().lower()
    
    if choice == 'q':
        return None
    elif choice == '1':
        path_str = input("\nEnter directory path: ").strip()
        if not path_str:
            return None
        try:
            path = Path(path_str).expanduser().resolve()
            if path.exists() and path.is_dir():
                return path
            else:
                print(f"✗ Error: '{path}' is not a valid directory")
                return None
        except Exception as e:
            print(f"✗ Error: {e}")
            return None
    elif choice == '2':
        return browse_directory()
    elif choice == '3' or choice == '':
        return Path('.').resolve()
    else:
        print(f"✗ Invalid choice: {choice}")
        return None


if __name__ == "__main__":
    # Test the browser
    print("Directory Browser Test")
    result = get_directory_path()
    if result:
        print(f"\n✓ Selected: {result}")
    else:
        print("\n✗ Cancelled")

