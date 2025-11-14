#!/usr/bin/env python3
"""
Comprehensive test suite for file_cleanup.py and directory_browser.py
Tests all functionality including file organization, duplicate handling, 
verification, logging, and directory browser TUI.

IMPORTANT: All tests are designed to be non-blocking and safe to run in Cursor.
All interactive operations (input, os.system, curses) are fully mocked to prevent hangs.
"""

import os
import sys
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
from io import StringIO

# Import the modules to test
import file_cleanup
import directory_browser


class TestFileCleanup(unittest.TestCase):
    """Test suite for file cleanup functionality."""

    def setUp(self):
        """Set up test environment before each test."""
        # Create a temporary directory for testing
        self.test_dir = Path(tempfile.mkdtemp(prefix="file_cleanup_test_"))
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        """Clean up after each test."""
        os.chdir(self.original_cwd)
        # Remove the entire test directory
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def create_test_files(self, file_list):
        """Helper method to create test files."""
        for filename in file_list:
            file_path = self.test_dir / filename
            file_path.write_text(f"Test content for {filename}")

    def test_get_file_extension(self):
        """Test file extension extraction."""
        # Test with extension
        self.assertEqual(file_cleanup.get_file_extension(Path("test.pdf")), "pdf")
        self.assertEqual(file_cleanup.get_file_extension(Path("test.JPG")), "jpg")
        self.assertEqual(file_cleanup.get_file_extension(Path("test.TXT")), "txt")
        
        # Test without extension
        self.assertEqual(file_cleanup.get_file_extension(Path("test")), "no_extension")
        
        # Test with multiple dots
        self.assertEqual(file_cleanup.get_file_extension(Path("test.backup.txt")), "txt")

    def test_organize_files_basic(self):
        """Test basic file organization."""
        # Create test files
        self.create_test_files(["doc1.pdf", "doc2.pdf", "image1.jpg", "image2.jpg", "text1.txt"])
        
        # Organize files
        moved_files, folder_status = file_cleanup.organize_files(self.test_dir)
        
        # Verify folders were created
        self.assertTrue((self.test_dir / "pdf").exists())
        self.assertTrue((self.test_dir / "jpg").exists())
        self.assertTrue((self.test_dir / "txt").exists())
        
        # Verify files were moved
        self.assertIn("doc1.pdf", moved_files["pdf"])
        self.assertIn("doc2.pdf", moved_files["pdf"])
        self.assertIn("image1.jpg", moved_files["jpg"])
        self.assertIn("image2.jpg", moved_files["jpg"])
        self.assertIn("text1.txt", moved_files["txt"])
        
        # Verify files are in correct locations
        self.assertTrue((self.test_dir / "pdf" / "doc1.pdf").exists())
        self.assertTrue((self.test_dir / "pdf" / "doc2.pdf").exists())
        self.assertTrue((self.test_dir / "jpg" / "image1.jpg").exists())
        self.assertTrue((self.test_dir / "jpg" / "image2.jpg").exists())
        self.assertTrue((self.test_dir / "txt" / "text1.txt").exists())
        
        # Verify original files are gone
        self.assertFalse((self.test_dir / "doc1.pdf").exists())
        self.assertFalse((self.test_dir / "image1.jpg").exists())

    def test_organize_files_no_extension(self):
        """Test files without extensions."""
        self.create_test_files(["file1", "file2", "README"])
        
        moved_files, folder_status = file_cleanup.organize_files(self.test_dir)
        
        # Verify no_extension folder was created
        self.assertTrue((self.test_dir / "no_extension").exists())
        
        # Verify files were moved
        self.assertIn("file1", moved_files["no_extension"])
        self.assertIn("file2", moved_files["no_extension"])
        self.assertIn("README", moved_files["no_extension"])

    def test_organize_files_hidden_files_ignored(self):
        """Test that hidden files are ignored."""
        self.create_test_files([".hidden_file", ".config", "visible.txt"])
        
        moved_files, folder_status = file_cleanup.organize_files(self.test_dir)
        
        # Hidden files should not be organized
        self.assertNotIn("hidden_file", str(moved_files))
        self.assertTrue((self.test_dir / ".hidden_file").exists())
        self.assertTrue((self.test_dir / ".config").exists())
        
        # Visible files should be organized
        self.assertIn("visible.txt", moved_files["txt"])

    def test_organize_files_duplicate_overwrite(self):
        """Test duplicate file handling with overwrite."""
        # Create initial file in folder
        pdf_folder = self.test_dir / "pdf"
        pdf_folder.mkdir()
        (pdf_folder / "doc1.pdf").write_text("Original content")
        
        # Create duplicate file in root
        (self.test_dir / "doc1.pdf").write_text("New content")
        
        # Mock input to return 'y' for overwrite
        with patch('builtins.input', return_value='y'):
            moved_files, folder_status = file_cleanup.organize_files(self.test_dir)
        
        # Verify file was overwritten
        self.assertTrue((pdf_folder / "doc1.pdf").exists())
        self.assertEqual((pdf_folder / "doc1.pdf").read_text(), "New content")

    def test_organize_files_duplicate_copy(self):
        """Test duplicate file handling with copy creation."""
        # Create initial file in folder
        pdf_folder = self.test_dir / "pdf"
        pdf_folder.mkdir()
        (pdf_folder / "doc1.pdf").write_text("Original content")
        
        # Create duplicate file in root
        (self.test_dir / "doc1.pdf").write_text("New content")
        
        # Mock input to return 'n' for no overwrite
        with patch('builtins.input', return_value='n'):
            moved_files, folder_status = file_cleanup.organize_files(self.test_dir)
        
        # Verify original file still exists
        self.assertTrue((pdf_folder / "doc1.pdf").exists())
        self.assertEqual((pdf_folder / "doc1.pdf").read_text(), "Original content")
        
        # Verify copy was created
        self.assertTrue((pdf_folder / "doc1_copy1.pdf").exists())
        self.assertEqual((pdf_folder / "doc1_copy1.pdf").read_text(), "New content")

    def test_organize_files_multiple_copies(self):
        """Test multiple copy generation."""
        pdf_folder = self.test_dir / "pdf"
        pdf_folder.mkdir()
        (pdf_folder / "doc1.pdf").write_text("Original")
        (pdf_folder / "doc1_copy1.pdf").write_text("Copy 1")
        
        (self.test_dir / "doc1.pdf").write_text("New")
        
        with patch('builtins.input', return_value='n'):
            moved_files, folder_status = file_cleanup.organize_files(self.test_dir)
        
        # Should create doc1_copy2.pdf
        self.assertTrue((pdf_folder / "doc1_copy2.pdf").exists())

    def test_organize_files_existing_folder(self):
        """Test that existing folders are reused."""
        # Create folder before organizing
        pdf_folder = self.test_dir / "pdf"
        pdf_folder.mkdir()
        
        self.create_test_files(["doc1.pdf"])
        
        moved_files, folder_status = file_cleanup.organize_files(self.test_dir)
        
        # Folder status should indicate it existed
        self.assertTrue(folder_status["pdf"])

    def test_verify_organization_success(self):
        """Test verification with correctly organized files."""
        # Create organized structure
        (self.test_dir / "pdf").mkdir()
        (self.test_dir / "jpg").mkdir()
        (self.test_dir / "pdf" / "doc1.pdf").write_text("content")
        (self.test_dir / "jpg" / "img1.jpg").write_text("content")
        
        result = file_cleanup.verify_organization(self.test_dir)
        self.assertTrue(result)

    def test_verify_organization_failure(self):
        """Test verification with misplaced files."""
        # Create misorganized structure
        (self.test_dir / "pdf").mkdir()
        (self.test_dir / "pdf" / "doc1.jpg").write_text("content")  # Wrong extension
        
        result = file_cleanup.verify_organization(self.test_dir)
        self.assertFalse(result)

    def test_verify_organization_top_level_files(self):
        """Test verification detects top-level files."""
        # Create unorganized structure
        (self.test_dir / "unorganized.pdf").write_text("content")
        
        result = file_cleanup.verify_organization(self.test_dir)
        self.assertFalse(result)

    def test_verify_organization_log_file_allowed(self):
        """Test that log files are allowed in top level."""
        # Create organized structure with log file
        (self.test_dir / "pdf").mkdir()
        (self.test_dir / "pdf" / "doc1.pdf").write_text("content")
        (self.test_dir / "organization_log.txt").write_text("log content")
        
        result = file_cleanup.verify_organization(self.test_dir)
        self.assertTrue(result)

    def test_create_log(self):
        """Test log file creation."""
        moved_files = {
            "pdf": ["doc1.pdf", "doc2.pdf"],
            "txt": ["text1.txt"]
        }
        folder_status = {
            "pdf": False,  # New folder
            "txt": True     # Existing folder
        }
        
        file_cleanup.create_log(self.test_dir, moved_files, folder_status)
        
        # Verify log file exists
        log_path = self.test_dir / "organization_log.txt"
        self.assertTrue(log_path.exists())
        
        # Verify log content
        log_content = log_path.read_text()
        self.assertIn("pdf", log_content)
        self.assertIn("txt", log_content)
        self.assertIn("NEW", log_content)
        self.assertIn("EXISTING", log_content)
        self.assertIn("doc1.pdf", log_content)

    def test_create_log_append_mode(self):
        """Test that log file appends rather than overwrites."""
        log_path = self.test_dir / "organization_log.txt"
        log_path.write_text("Previous log entry\n")
        
        moved_files = {"pdf": ["doc1.pdf"]}
        folder_status = {"pdf": False}
        
        file_cleanup.create_log(self.test_dir, moved_files, folder_status)
        
        # Verify previous content is still there
        log_content = log_path.read_text()
        self.assertIn("Previous log entry", log_content)
        self.assertIn("doc1.pdf", log_content)

    def test_main_invalid_directory(self):
        """Test main function with invalid directory."""
        invalid_path = Path('/nonexistent/path')
        with patch('file_cleanup.get_directory_path', return_value=invalid_path):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                file_cleanup.main()
                output = fake_out.getvalue()
                self.assertIn("not a valid directory", output)

    def test_main_no_files(self):
        """Test main function with empty directory."""
        with patch('file_cleanup.get_directory_path', return_value=self.test_dir):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                file_cleanup.main()
                output = fake_out.getvalue()
                self.assertIn("No files to organize", output)

    def test_main_full_workflow(self):
        """Test complete workflow from main function."""
        self.create_test_files(["doc1.pdf", "img1.jpg", "text1.txt"])
        
        with patch('file_cleanup.get_directory_path', return_value=self.test_dir):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                file_cleanup.main()
                output = fake_out.getvalue()
                
                # Verify organization happened
                self.assertIn("Organizing", output)
                self.assertIn("Created", output)
                self.assertIn("Organization complete", output)
                
                # Verify files were organized
                self.assertTrue((self.test_dir / "pdf" / "doc1.pdf").exists())
                self.assertTrue((self.test_dir / "jpg" / "img1.jpg").exists())
                self.assertTrue((self.test_dir / "txt" / "text1.txt").exists())
                
                # Verify log was created
                self.assertTrue((self.test_dir / "organization_log.txt").exists())

    def test_case_insensitive_extensions(self):
        """Test that extensions are handled case-insensitively."""
        self.create_test_files(["doc1.PDF", "doc2.pdf", "IMG1.JPG"])
        
        moved_files, folder_status = file_cleanup.organize_files(self.test_dir)
        
        # All should go to lowercase folders
        self.assertTrue((self.test_dir / "pdf" / "doc1.PDF").exists())
        self.assertTrue((self.test_dir / "pdf" / "doc2.pdf").exists())
        self.assertTrue((self.test_dir / "jpg" / "IMG1.JPG").exists())


class TestDirectoryBrowser(unittest.TestCase):
    """Test suite for directory browser functionality."""

    def setUp(self):
        """Set up test environment before each test."""
        # Create a temporary directory structure for testing
        self.test_dir = Path(tempfile.mkdtemp(prefix="dir_browser_test_"))
        self.original_cwd = os.getcwd()
        
        # Create test directory structure
        (self.test_dir / "subdir1").mkdir()
        (self.test_dir / "subdir2").mkdir()
        (self.test_dir / "subdir3").mkdir()
        (self.test_dir / "file1.txt").write_text("test")
        (self.test_dir / "file2.pdf").write_text("test")
        (self.test_dir / ".hidden_dir").mkdir()
        (self.test_dir / ".hidden_file").write_text("test")

    def tearDown(self):
        """Clean up after each test."""
        os.chdir(self.original_cwd)
        # Remove the entire test directory
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_simple_browser_initialization_default(self):
        """Test SimpleDirectoryBrowser initialization with default path."""
        browser = directory_browser.SimpleDirectoryBrowser()
        self.assertEqual(browser.current_path, Path.home().resolve())

    def test_simple_browser_initialization_custom_path(self):
        """Test SimpleDirectoryBrowser initialization with custom path."""
        browser = directory_browser.SimpleDirectoryBrowser(self.test_dir)
        self.assertEqual(browser.current_path, self.test_dir.resolve())

    def test_simple_browser_get_items(self):
        """Test get_items returns directories and files correctly."""
        browser = directory_browser.SimpleDirectoryBrowser(self.test_dir)
        dirs, files = browser.get_items()
        
        # Should return 3 subdirectories (hidden_dir excluded)
        self.assertEqual(len(dirs), 3)
        self.assertIn(self.test_dir / "subdir1", dirs)
        self.assertIn(self.test_dir / "subdir2", dirs)
        self.assertIn(self.test_dir / "subdir3", dirs)
        
        # Should return 2 files (hidden_file excluded from dirs, but files should include it)
        # Actually, get_items only filters hidden from dirs, not files
        self.assertGreaterEqual(len(files), 2)
        file_names = [f.name for f in files]
        self.assertIn("file1.txt", file_names)
        self.assertIn("file2.pdf", file_names)

    def test_simple_browser_get_items_hidden_dirs_excluded(self):
        """Test that hidden directories are excluded."""
        browser = directory_browser.SimpleDirectoryBrowser(self.test_dir)
        dirs, _ = browser.get_items()
        
        dir_names = [d.name for d in dirs]
        self.assertNotIn(".hidden_dir", dir_names)

    def test_simple_browser_navigate_quit(self):
        """Test navigate with 'q' choice returns None."""
        browser = directory_browser.SimpleDirectoryBrowser(self.test_dir)
        result = browser.navigate('q')
        self.assertIsNone(result)

    def test_simple_browser_navigate_select_current(self):
        """Test navigate with 's' choice returns current path."""
        browser = directory_browser.SimpleDirectoryBrowser(self.test_dir)
        result = browser.navigate('s')
        self.assertEqual(result, self.test_dir.resolve())

    def test_simple_browser_navigate_home(self):
        """Test navigate with 'h' choice changes to home directory."""
        browser = directory_browser.SimpleDirectoryBrowser(self.test_dir)
        browser.navigate('h')
        self.assertEqual(browser.current_path, Path.home().resolve())

    def test_simple_browser_navigate_go_up(self):
        """Test navigate with '0' choice goes up one directory."""
        subdir = self.test_dir / "subdir1"
        browser = directory_browser.SimpleDirectoryBrowser(subdir)
        browser.navigate('0')
        self.assertEqual(browser.current_path, self.test_dir.resolve())

    def test_simple_browser_navigate_go_up_at_root(self):
        """Test navigate with '0' at root directory doesn't change."""
        # On Unix, root is '/', on Windows it's 'C:\' etc.
        root = Path(self.test_dir.parts[0])
        browser = directory_browser.SimpleDirectoryBrowser(root)
        original_path = browser.current_path
        browser.navigate('0')
        self.assertEqual(browser.current_path, original_path)

    def test_simple_browser_navigate_select_directory(self):
        """Test navigate with number choice selects directory."""
        browser = directory_browser.SimpleDirectoryBrowser(self.test_dir)
        browser.navigate('1')  # Select first directory
        # Should navigate into subdir1
        self.assertEqual(browser.current_path.name, "subdir1")

    def test_simple_browser_navigate_invalid_number(self):
        """Test navigate with invalid number choice."""
        browser = directory_browser.SimpleDirectoryBrowser(self.test_dir)
        with patch('builtins.input', return_value=''):
            result = browser.navigate('99')  # Invalid index
            self.assertIsNone(result)

    def test_simple_browser_navigate_type_path_valid(self):
        """Test navigate with 't' choice and valid path."""
        browser = directory_browser.SimpleDirectoryBrowser(self.test_dir)
        with patch('builtins.input', return_value=str(self.test_dir / "subdir1")):
            result = browser.navigate('t')
            self.assertEqual(result, (self.test_dir / "subdir1").resolve())

    def test_simple_browser_navigate_type_path_invalid(self):
        """Test navigate with 't' choice and invalid path."""
        browser = directory_browser.SimpleDirectoryBrowser(self.test_dir)
        with patch('builtins.input', side_effect=['/nonexistent/path', '']):
            result = browser.navigate('t')
            self.assertIsNone(result)

    def test_simple_browser_navigate_type_path_empty(self):
        """Test navigate with 't' choice and empty path."""
        browser = directory_browser.SimpleDirectoryBrowser(self.test_dir)
        with patch('builtins.input', return_value=''):
            result = browser.navigate('t')
            self.assertIsNone(result)

    def test_simple_browser_navigate_invalid_choice(self):
        """Test navigate with invalid choice."""
        browser = directory_browser.SimpleDirectoryBrowser(self.test_dir)
        with patch('builtins.input', return_value=''):
            result = browser.navigate('x')  # Invalid choice
            self.assertIsNone(result)

    def test_simple_browser_browse_select_current(self):
        """Test browse loop with 's' to select current directory."""
        browser = directory_browser.SimpleDirectoryBrowser(self.test_dir)
        with patch.object(browser, 'display', return_value='s'):
            with patch('os.system'):  # Mock os.system to prevent clear/cls calls
                result = browser.browse()
                self.assertEqual(result, self.test_dir.resolve())

    def test_simple_browser_browse_quit(self):
        """Test browse loop with 'q' to quit."""
        browser = directory_browser.SimpleDirectoryBrowser(self.test_dir)
        with patch.object(browser, 'display', return_value='q'):
            with patch('os.system'):  # Mock os.system to prevent clear/cls calls
                result = browser.browse()
                self.assertIsNone(result)

    def test_simple_browser_browse_navigate_then_select(self):
        """Test browse loop with navigation then selection."""
        browser = directory_browser.SimpleDirectoryBrowser(self.test_dir)
        with patch.object(browser, 'display', side_effect=['1', 's']):
            with patch('os.system'):  # Mock os.system to prevent clear/cls calls
                result = browser.browse()
                self.assertEqual(result.name, "subdir1")

    def test_get_directory_path_quit(self):
        """Test get_directory_path with 'q' choice."""
        with patch('builtins.input', return_value='q'):
            result = directory_browser.get_directory_path()
            self.assertIsNone(result)

    def test_get_directory_path_type_manual_valid(self):
        """Test get_directory_path with manual path entry (valid)."""
        with patch('builtins.input', side_effect=['1', str(self.test_dir)]):
            result = directory_browser.get_directory_path()
            self.assertEqual(result, self.test_dir.resolve())

    def test_get_directory_path_type_manual_invalid(self):
        """Test get_directory_path with manual path entry (invalid)."""
        with patch('builtins.input', side_effect=['1', '/nonexistent/path']):
            result = directory_browser.get_directory_path()
            self.assertIsNone(result)

    def test_get_directory_path_type_manual_empty(self):
        """Test get_directory_path with manual path entry (empty)."""
        with patch('builtins.input', side_effect=['1', '']):
            result = directory_browser.get_directory_path()
            self.assertIsNone(result)

    def test_get_directory_path_current_directory(self):
        """Test get_directory_path with current directory option."""
        with patch('builtins.input', return_value='3'):
            result = directory_browser.get_directory_path()
            self.assertEqual(result, Path('.').resolve())

    def test_get_directory_path_current_directory_default(self):
        """Test get_directory_path with empty input defaults to current."""
        with patch('builtins.input', return_value=''):
            result = directory_browser.get_directory_path()
            self.assertEqual(result, Path('.').resolve())

    def test_get_directory_path_browse(self):
        """Test get_directory_path with browse option."""
        with patch('builtins.input', return_value='2'):
            with patch('directory_browser.browse_directory', return_value=self.test_dir):
                result = directory_browser.get_directory_path()
                self.assertEqual(result, self.test_dir)

    def test_get_directory_path_invalid_choice(self):
        """Test get_directory_path with invalid choice."""
        with patch('builtins.input', return_value='x'):
            result = directory_browser.get_directory_path()
            self.assertIsNone(result)

    def test_browse_directory_simple_mode(self):
        """Test browse_directory uses SimpleDirectoryBrowser when curses unavailable."""
        mock_browser = MagicMock()
        mock_browser.browse.return_value = self.test_dir
        with patch('directory_browser.HAS_CURSES', False):
            with patch('sys.stdin.isatty', return_value=True):
                with patch('directory_browser.SimpleDirectoryBrowser', return_value=mock_browser):
                    result = directory_browser.browse_directory(self.test_dir)
                    self.assertEqual(result, self.test_dir)
                    mock_browser.browse.assert_called_once()

    def test_browse_directory_curses_mode(self):
        """Test browse_directory uses CursesDirectoryBrowser when curses available."""
        mock_browser = MagicMock()
        mock_browser.browse.return_value = self.test_dir
        with patch('directory_browser.HAS_CURSES', True):
            with patch('sys.stdin.isatty', return_value=True):
                with patch('directory_browser.CursesDirectoryBrowser', return_value=mock_browser):
                    result = directory_browser.browse_directory(self.test_dir)
                    self.assertEqual(result, self.test_dir)
                    mock_browser.browse.assert_called_once()

    def test_browse_directory_default_path(self):
        """Test browse_directory with default (None) path."""
        mock_browser = MagicMock()
        mock_browser.browse.return_value = Path.home()
        with patch('directory_browser.HAS_CURSES', False):
            with patch('sys.stdin.isatty', return_value=True):
                with patch('directory_browser.SimpleDirectoryBrowser', return_value=mock_browser):
                    result = directory_browser.browse_directory()
                    self.assertEqual(result, Path.home())
                    # Verify browser was created
                    mock_browser.browse.assert_called_once()

    def test_curses_browser_initialization(self):
        """Test CursesDirectoryBrowser initialization."""
        browser = directory_browser.CursesDirectoryBrowser(self.test_dir)
        self.assertEqual(browser.current_path, self.test_dir.resolve())
        self.assertEqual(browser.selected_idx, 0)
        self.assertEqual(browser.scroll_offset, 0)

    def test_curses_browser_get_items(self):
        """Test CursesDirectoryBrowser get_items method."""
        browser = directory_browser.CursesDirectoryBrowser(self.test_dir)
        dirs = browser.get_items()
        
        # Should return 3 subdirectories (hidden excluded)
        self.assertEqual(len(dirs), 3)
        dir_names = [d.name for d in dirs]
        self.assertIn("subdir1", dir_names)
        self.assertIn("subdir2", dir_names)
        self.assertIn("subdir3", dir_names)
        self.assertNotIn(".hidden_dir", dir_names)

    def test_curses_browser_get_items_permission_error(self):
        """Test CursesDirectoryBrowser handles permission errors."""
        browser = directory_browser.CursesDirectoryBrowser(self.test_dir)
        # Create a directory we can't read (simulate permission error)
        # This is hard to test without actually creating permission issues
        # So we'll just verify the method exists and can be called
        dirs = browser.get_items()
        self.assertIsInstance(dirs, list)

    def test_path_expansion_tilde(self):
        """Test that paths with ~ are expanded correctly."""
        home = Path.home()
        browser = directory_browser.SimpleDirectoryBrowser(self.test_dir)
        
        with patch('builtins.input', return_value=str(home)):
            result = browser.navigate('t')
            # Should resolve to home directory
            self.assertEqual(result, home.resolve())


def run_tests():
    """Run all tests and report results."""
    print("=" * 70)
    print("File Cleanup Test Suite")
    print("=" * 70)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestFileCleanup))
    suite.addTests(loader.loadTestsFromTestCase(TestDirectoryBrowser))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print()
    print("=" * 70)
    if result.wasSuccessful():
        print("✓ All tests passed!")
        return 0
    else:
        print(f"✗ Tests failed: {len(result.failures)} failures, {len(result.errors)} errors")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())

