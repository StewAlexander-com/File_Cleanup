#!/usr/bin/env python3
"""
Comprehensive test suite for file_cleanup.py
Tests all functionality including file organization, duplicate handling, verification, and logging.
"""

import os
import sys
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
from io import StringIO

# Import the module to test
import file_cleanup


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
        with patch('builtins.input', return_value='/nonexistent/path'):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                file_cleanup.main()
                output = fake_out.getvalue()
                self.assertIn("not a valid directory", output)

    def test_main_no_files(self):
        """Test main function with empty directory."""
        with patch('builtins.input', return_value='.'):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                file_cleanup.main()
                output = fake_out.getvalue()
                self.assertIn("No files to organize", output)

    def test_main_full_workflow(self):
        """Test complete workflow from main function."""
        self.create_test_files(["doc1.pdf", "img1.jpg", "text1.txt"])
        
        with patch('builtins.input', return_value='.'):
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


def run_tests():
    """Run all tests and report results."""
    print("=" * 70)
    print("File Cleanup Test Suite")
    print("=" * 70)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestFileCleanup)
    
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

