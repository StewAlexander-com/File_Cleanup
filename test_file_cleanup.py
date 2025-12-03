#!/usr/bin/env python3
"""
Simplified test suite for file_cleanup.py
Tests core functionality with a real test directory containing mock files.
"""

import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from io import StringIO

# Import the modules to test
import file_cleanup


class TestFileCleanup(unittest.TestCase):
    """Simplified test suite for file cleanup functionality."""

    def setUp(self):
        """Set up test environment before each test."""
        # Create a temporary directory for testing
        self.test_dir = Path(tempfile.mkdtemp(prefix="file_cleanup_test_"))
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create mock files with various extensions
        self.create_mock_files()

    def tearDown(self):
        """Clean up after each test."""
        os.chdir(self.original_cwd)
        # Remove the entire test directory
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def create_mock_files(self):
        """Create a variety of mock files with different extensions."""
        mock_files = [
            "document1.pdf",
            "document2.pdf",
            "image1.jpg",
            "image2.png",
            "image3.JPG",  # Test case insensitivity
            "text1.txt",
            "text2.txt",
            "spreadsheet.xlsx",
            "presentation.pptx",
            "script.py",
            "data.json",
            "archive.zip",
            "video.mp4",
            "audio.mp3",
            "readme",  # No extension
            "LICENSE",  # No extension, uppercase
        ]
        
        for filename in mock_files:
            file_path = self.test_dir / filename
            file_path.write_text(f"Mock content for {filename}")

    def test_organize_files_creates_folders(self):
        """Test that organize_files creates extension-based folders."""
        moved_files, folder_status = file_cleanup.organize_files(self.test_dir)
        
        # Verify folders were created for each extension
        self.assertTrue((self.test_dir / "pdf").exists())
        self.assertTrue((self.test_dir / "jpg").exists())
        self.assertTrue((self.test_dir / "png").exists())
        self.assertTrue((self.test_dir / "txt").exists())
        self.assertTrue((self.test_dir / "xlsx").exists())
        self.assertTrue((self.test_dir / "pptx").exists())
        self.assertTrue((self.test_dir / "py").exists())
        self.assertTrue((self.test_dir / "json").exists())
        self.assertTrue((self.test_dir / "zip").exists())
        self.assertTrue((self.test_dir / "mp4").exists())
        self.assertTrue((self.test_dir / "mp3").exists())
        self.assertTrue((self.test_dir / "no_extension").exists())

    def test_organize_files_moves_files_correctly(self):
        """Test that files are moved to correct extension folders."""
        moved_files, folder_status = file_cleanup.organize_files(self.test_dir)
        
        # Verify PDF files were moved
        self.assertTrue((self.test_dir / "pdf" / "document1.pdf").exists())
        self.assertTrue((self.test_dir / "pdf" / "document2.pdf").exists())
        
        # Verify JPG files (including case-insensitive)
        self.assertTrue((self.test_dir / "jpg" / "image1.jpg").exists())
        self.assertTrue((self.test_dir / "jpg" / "image3.JPG").exists())
        
        # Verify PNG file
        self.assertTrue((self.test_dir / "png" / "image2.png").exists())
        
        # Verify TXT files
        self.assertTrue((self.test_dir / "txt" / "text1.txt").exists())
        self.assertTrue((self.test_dir / "txt" / "text2.txt").exists())
        
        # Verify files without extensions
        self.assertTrue((self.test_dir / "no_extension" / "readme").exists())
        self.assertTrue((self.test_dir / "no_extension" / "LICENSE").exists())
        
        # Verify original files are gone from root
        self.assertFalse((self.test_dir / "document1.pdf").exists())
        self.assertFalse((self.test_dir / "image1.jpg").exists())

    def test_organize_files_case_insensitive(self):
        """Test that extensions are handled case-insensitively."""
        moved_files, folder_status = file_cleanup.organize_files(self.test_dir)
        
        # image3.JPG should go to jpg folder (lowercase)
        self.assertTrue((self.test_dir / "jpg" / "image3.JPG").exists())
        self.assertIn("image3.JPG", moved_files["jpg"])

    def test_verify_organization_success(self):
        """Test verification with correctly organized files."""
        # First organize the files
        file_cleanup.organize_files(self.test_dir)
        
        # Then verify
        result = file_cleanup.verify_organization(self.test_dir)
        self.assertTrue(result)

    def test_create_log(self):
        """Test that log file is created with correct content."""
        moved_files, folder_status = file_cleanup.organize_files(self.test_dir)
        file_cleanup.create_log(self.test_dir, moved_files, folder_status)
        
        # Verify log file exists
        log_path = self.test_dir / "organization_log.txt"
        self.assertTrue(log_path.exists())
        
        # Verify log contains expected content
        log_content = log_path.read_text()
        self.assertIn("pdf", log_content)
        self.assertIn("jpg", log_content)
        self.assertIn("document1.pdf", log_content)

    def test_main_function_with_directory(self):
        """Test main function with a directory path."""
        with patch('sys.argv', ['file_cleanup.py', str(self.test_dir)]):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                file_cleanup.main()
                output = fake_out.getvalue()
                
                # Verify organization happened
                self.assertIn("Organizing", output)
                self.assertIn("Created", output)
                self.assertIn("Organization complete", output)
                
                # Verify files were actually organized
                self.assertTrue((self.test_dir / "pdf" / "document1.pdf").exists())
                self.assertTrue((self.test_dir / "jpg" / "image1.jpg").exists())

    def test_main_function_interactive_mode(self):
        """Test main function in interactive mode (no args)."""
        with patch('sys.argv', ['file_cleanup.py']):
            with patch('builtins.input', return_value=''):
                with patch('sys.stdout', new=StringIO()) as fake_out:
                    file_cleanup.main()
                    output = fake_out.getvalue()
                    self.assertIn("Organizing", output)

    def test_duplicate_file_handling(self):
        """Test handling of duplicate files."""
        # Create a folder with a file already in it
        pdf_folder = self.test_dir / "pdf"
        pdf_folder.mkdir()
        (pdf_folder / "document1.pdf").write_text("Original")
        
        # Create duplicate in root
        (self.test_dir / "document1.pdf").write_text("New")
        
        # Mock input to not overwrite
        with patch('builtins.input', return_value='n'):
            moved_files, folder_status = file_cleanup.organize_files(self.test_dir)
        
        # Should create a copy
        self.assertTrue((pdf_folder / "document1_copy1.pdf").exists())
        self.assertEqual((pdf_folder / "document1_copy1.pdf").read_text(), "New")

    def test_hidden_files_ignored(self):
        """Test that hidden files are ignored."""
        # Create a hidden file
        (self.test_dir / ".hidden_file").write_text("hidden")
        
        moved_files, folder_status = file_cleanup.organize_files(self.test_dir)
        
        # Hidden file should still be in root
        self.assertTrue((self.test_dir / ".hidden_file").exists())
        # Should not be in any moved_files
        for files in moved_files.values():
            self.assertNotIn(".hidden_file", files)


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
        if result.failures:
            print("\nFailures:")
            for test, traceback in result.failures:
                print(f"  - {test}")
        if result.errors:
            print("\nErrors:")
            for test, traceback in result.errors:
                print(f"  - {test}")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(run_tests())
