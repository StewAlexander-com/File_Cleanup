#!/usr/bin/env python3
"""
Test suite for Flask web interface (web_interface.py)
Tests API endpoints and web interface functionality.
"""

import os
import sys
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Check if Flask is available
try:
    from flask import Flask
    from flask.testing import FlaskClient
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

# Import the web interface module
if FLASK_AVAILABLE:
    try:
        from web_interface import app, cleanup_results, cleanup_history
        WEB_INTERFACE_AVAILABLE = True
    except ImportError:
        WEB_INTERFACE_AVAILABLE = False
else:
    WEB_INTERFACE_AVAILABLE = False


@unittest.skipUnless(FLASK_AVAILABLE, "Flask is not installed")
@unittest.skipUnless(WEB_INTERFACE_AVAILABLE, "Web interface module not available")
class TestWebInterface(unittest.TestCase):
    """Test suite for Flask web interface."""

    def setUp(self):
        """Set up test environment before each test."""
        # Create a test client
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Create a temporary directory for testing
        self.test_dir = Path(tempfile.mkdtemp(prefix="web_interface_test_"))
        
        # Clear cleanup results and history
        cleanup_results.clear()
        cleanup_history.clear()

    def tearDown(self):
        """Clean up after each test."""
        # Clean up test directory
        if self.test_dir.exists():
            import shutil
            shutil.rmtree(self.test_dir)
        
        # Clear cleanup results and history
        cleanup_results.clear()
        cleanup_history.clear()

    def test_index_route(self):
        """Test that the index route returns HTML."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'File Cleanup', response.data)
        content_type = response.headers.get('Content-Type', '')
        self.assertIn('text/html', content_type)

    def test_directory_api_no_path(self):
        """Test directory API with no path (defaults to home)."""
        response = self.client.get('/api/directory')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('current_path', data)
        self.assertIn('directories', data)
        self.assertIn('files', data)
        self.assertIn('breadcrumbs', data)

    def test_directory_api_with_path(self):
        """Test directory API with a specific path."""
        # Create a test directory
        test_subdir = self.test_dir / "test_subdir"
        test_subdir.mkdir()
        (test_subdir / "test_file.txt").write_text("test content")
        
        response = self.client.get(f'/api/directory?path={test_subdir}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        # Compare resolved paths (macOS may add /private prefix)
        self.assertEqual(Path(data['current_path']).resolve(), test_subdir.resolve())
        self.assertIn('directories', data)
        self.assertIn('files', data)

    def test_directory_api_invalid_path(self):
        """Test directory API with invalid path."""
        response = self.client.get('/api/directory?path=/nonexistent/path/12345')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_directory_state_api(self):
        """Test directory state API for polling."""
        # Create test files
        (self.test_dir / "file1.txt").write_text("test")
        (self.test_dir / "file2.txt").write_text("test")
        
        response = self.client.get(f'/api/directory-state?path={self.test_dir}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('hash', data)
        self.assertIn('file_count', data)
        self.assertIn('dir_count', data)
        self.assertIn('timestamp', data)
        self.assertEqual(data['file_count'], 2)

    def test_directory_state_api_invalid_path(self):
        """Test directory state API with invalid path."""
        response = self.client.get('/api/directory-state?path=/nonexistent/path/12345')
        self.assertEqual(response.status_code, 400)

    def test_logs_api_no_log_file(self):
        """Test logs API when log file doesn't exist."""
        response = self.client.get(f'/api/logs?path={self.test_dir}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertFalse(data['exists'])

    def test_logs_api_with_log_file(self):
        """Test logs API when log file exists."""
        # Create a log file
        log_file = self.test_dir / "organization_log.txt"
        log_file.write_text("Test log content")
        
        response = self.client.get(f'/api/logs?path={self.test_dir}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['exists'])
        self.assertIn('content', data)
        self.assertEqual(data['content'], "Test log content")

    def test_server_status_api(self):
        """Test server status API."""
        response = self.client.get('/api/server/status')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'running')
        self.assertEqual(data['host'], '127.0.0.1')
        self.assertEqual(data['security'], 'localhost-only')

    def test_cleanup_history_api(self):
        """Test cleanup history API."""
        # Add some mock history
        cleanup_history.append({
            'timestamp': '2024-01-01T00:00:00',
            'directory': str(self.test_dir),
            'file_count': 5,
            'folder_count': 3,
            'is_organized': True
        })
        
        response = self.client.get('/api/cleanup-history')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('history', data)
        self.assertIn('total_operations', data)
        self.assertEqual(len(data['history']), 1)

    def test_directory_structure_api(self):
        """Test directory structure API."""
        # Create a test structure
        subdir = self.test_dir / "test_folder"
        subdir.mkdir()
        (subdir / "file.txt").write_text("test")
        
        response = self.client.get(f'/api/directory-structure?path={self.test_dir}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('structure', data)
        self.assertIn('directory', data)

    def test_directory_structure_api_invalid_path(self):
        """Test directory structure API with invalid path."""
        response = self.client.get('/api/directory-structure?path=/nonexistent/path/12345')
        self.assertEqual(response.status_code, 400)

    @patch('web_interface.organize_files')
    @patch('web_interface.verify_organization')
    @patch('web_interface.create_log')
    def test_cleanup_api(self, mock_create_log, mock_verify, mock_organize):
        """Test cleanup API endpoint."""
        # Mock the cleanup functions
        mock_organize.return_value = (
            {'pdf': ['file1.pdf', 'file2.pdf']},
            {'pdf': False}  # folder_status: False means NEW
        )
        mock_verify.return_value = True
        
        # Create test files
        (self.test_dir / "file1.pdf").write_text("test")
        (self.test_dir / "file2.pdf").write_text("test")
        
        response = self.client.post(
            '/api/cleanup',
            json={
                'path': str(self.test_dir),
                'non_interactive': True,
                'overwrite': False
            },
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('result_id', data)
        self.assertIn('moved_files', data)
        self.assertIn('file_count', data)

    def test_cleanup_api_no_path(self):
        """Test cleanup API without path."""
        response = self.client.post(
            '/api/cleanup',
            json={},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_cleanup_result_api(self):
        """Test cleanup result retrieval API."""
        # Add a result
        result_id = "test_result_123"
        cleanup_results[result_id] = {
            'directory': str(self.test_dir),
            'moved_files': {'pdf': ['file1.pdf']},
            'folder_status': {'pdf': False},
            'is_organized': True,
            'file_count': 1
        }
        
        response = self.client.get(f'/api/cleanup-result/{result_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['file_count'], 1)

    def test_cleanup_result_api_not_found(self):
        """Test cleanup result API with non-existent ID."""
        response = self.client.get('/api/cleanup-result/nonexistent')
        self.assertEqual(response.status_code, 404)


class TestWebInterfaceSecurity(unittest.TestCase):
    """Test security features of the web interface."""

    @unittest.skipUnless(FLASK_AVAILABLE, "Flask is not installed")
    def test_localhost_only_binding(self):
        """Test that server enforces localhost-only binding."""
        from web_interface import run_server
        
        # The run_server function should force host to 127.0.0.1
        # We can't easily test the actual binding, but we can verify
        # the function signature and default behavior
        import inspect
        sig = inspect.signature(run_server)
        default_host = sig.parameters['host'].default
        self.assertEqual(default_host, '127.0.0.1')


@unittest.skipUnless(FLASK_AVAILABLE, "Flask is not installed")
class TestWebInterfaceIntegration(unittest.TestCase):
    """Integration tests for web interface."""

    def setUp(self):
        """Set up test environment."""
        if WEB_INTERFACE_AVAILABLE:
            self.app = app
            self.app.config['TESTING'] = True
            self.client = self.app.test_client()
        self.test_dir = Path(tempfile.mkdtemp(prefix="web_integration_test_"))

    def tearDown(self):
        """Clean up after each test."""
        if self.test_dir.exists():
            import shutil
            shutil.rmtree(self.test_dir)

    @unittest.skipUnless(WEB_INTERFACE_AVAILABLE, "Web interface not available")
    def test_full_workflow(self):
        """Test a complete workflow: browse, cleanup, view results."""
        # 1. Browse directory
        response = self.client.get(f'/api/directory?path={self.test_dir}')
        self.assertEqual(response.status_code, 200)
        
        # 2. Check directory state
        response = self.client.get(f'/api/directory-state?path={self.test_dir}')
        self.assertEqual(response.status_code, 200)
        initial_hash = json.loads(response.data)['hash']
        
        # 3. Get server status
        response = self.client.get('/api/server/status')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['security'], 'localhost-only')


if __name__ == '__main__':
    # Set up test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestWebInterface))
    suite.addTests(loader.loadTestsFromTestCase(TestWebInterfaceSecurity))
    suite.addTests(loader.loadTestsFromTestCase(TestWebInterfaceIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)

