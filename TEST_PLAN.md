# Test Plan for File Cleanup Application

## Overview
This document outlines the test plan for the File Cleanup application, including both CLI and Flask web interface components.

## Test Categories

### 1. Core Functionality Tests (`test_file_cleanup.py`)
Tests the core file organization functionality without web interface dependencies.

**Test Coverage:**
- ✅ Folder creation by extension
- ✅ File organization into extension folders
- ✅ Case-insensitive extension handling
- ✅ Files without extensions (no_extension folder)
- ✅ Hidden file handling
- ✅ Duplicate file handling (copy creation)
- ✅ Organization verification
- ✅ Log file creation
- ✅ Main function execution
- ✅ Interactive mode

**Run Command:**
```bash
python3 test_file_cleanup.py
```

### 2. Flask Web Interface Tests (`test_web_interface.py`)
Tests the Flask web interface API endpoints and functionality.

**Test Coverage:**

#### API Endpoint Tests
- ✅ Index route (HTML rendering)
- ✅ Directory listing API (`/api/directory`)
  - Default path (home directory)
  - Specific path
  - Invalid path handling
- ✅ Directory state API (`/api/directory-state`)
  - State hash generation
  - File/directory counting
  - Invalid path handling
- ✅ Logs API (`/api/logs`)
  - Log file reading
  - Missing log file handling
- ✅ Server status API (`/api/server/status`)
  - Status information
  - Security information
- ✅ Cleanup history API (`/api/cleanup-history`)
  - History retrieval
  - History tracking
- ✅ Directory structure API (`/api/directory-structure`)
  - Tree structure generation
  - Invalid path handling
- ✅ Cleanup API (`/api/cleanup`)
  - File organization execution
  - Result generation
  - Error handling
- ✅ Cleanup result API (`/api/cleanup-result/<id>`)
  - Result retrieval
  - Non-existent result handling

#### Security Tests
- ✅ Localhost-only binding enforcement
- ✅ Security status reporting

#### Integration Tests
- ✅ Full workflow (browse → cleanup → view results)
- ✅ Directory state polling
- ✅ Server status checks

**Run Command:**
```bash
python3 test_web_interface.py
```

**Prerequisites:**
- Flask must be installed (`pip install Flask`)
- Web interface module must be importable

**Note:** Tests will be skipped if Flask is not installed, allowing the test suite to run on systems without Flask.

## Test Execution

### Run All Tests
```bash
# Run core functionality tests
python3 test_file_cleanup.py

# Run web interface tests (requires Flask)
python3 test_web_interface.py
```

### Run Specific Test Class
```bash
python3 -m unittest test_web_interface.TestWebInterface
python3 -m unittest test_web_interface.TestWebInterfaceSecurity
python3 -m unittest test_web_interface.TestWebInterfaceIntegration
```

### Run with Verbose Output
```bash
python3 -m unittest -v test_web_interface
```

## Test Environment

### Requirements
- Python 3.6+
- Flask (for web interface tests)
- Standard library modules (unittest, tempfile, pathlib, etc.)

### Test Isolation
- Each test creates its own temporary directory
- Tests clean up after themselves
- No side effects on system files
- Thread-safe test execution

## Manual Testing Checklist

### CLI Functionality
- [ ] Basic file organization
- [ ] Interactive mode
- [ ] Non-interactive mode (`--yes`)
- [ ] Overwrite mode (`--overwrite`)
- [ ] Quiet mode (`--quiet`)
- [ ] Help display (`--help`)
- [ ] Directory path arguments
- [ ] Partial path matching
- [ ] Directory browser TUI

### Web Interface Functionality
- [ ] Server starts with `--html` flag
- [ ] Browser opens automatically (or shows URL)
- [ ] Directory browsing works
- [ ] Breadcrumb navigation
- [ ] File organization via web interface
- [ ] Results display (graph, directory structure)
- [ ] Log viewing
- [ ] Server controls (stop/restart)
- [ ] Polling/auto-refresh
- [ ] Expandable/collapsible directory tree
- [ ] Security: localhost-only access

### Security Testing
- [ ] Server only accessible from localhost
- [ ] Cannot bind to external interfaces
- [ ] Server status shows security info
- [ ] Stop/restart controls work correctly

## Expected Test Results

### Core Tests (`test_file_cleanup.py`)
- **Expected:** All 9+ tests pass
- **Duration:** < 1 second
- **Platform:** Cross-platform (Windows, macOS, Linux)

### Web Interface Tests (`test_web_interface.py`)
- **Expected:** All 15+ tests pass (if Flask installed)
- **Duration:** < 2 seconds
- **Platform:** Cross-platform (Windows, macOS, Linux)

## Continuous Integration

### Pre-commit Checks
1. Run core functionality tests
2. Run web interface tests (if Flask available)
3. Check for linting errors
4. Verify all tests pass

### CI/CD Pipeline
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python3 test_file_cleanup.py
python3 test_web_interface.py

# Check exit codes
echo $?  # Should be 0 if all tests pass
```

## Known Limitations

1. **Flask Dependency:** Web interface tests require Flask. Tests gracefully skip if Flask is not installed.
2. **Browser Testing:** Manual browser testing required for full UI/UX validation.
3. **Performance Testing:** No automated performance benchmarks (manual testing recommended).
4. **Cross-browser Testing:** Manual testing required for different browsers.

## Test Maintenance

### Adding New Tests
1. Follow existing test patterns
2. Use temporary directories for file operations
3. Clean up resources in `tearDown()`
4. Add descriptive test names
5. Include both positive and negative test cases

### Updating Tests
- Update tests when API changes
- Maintain backward compatibility where possible
- Document breaking changes in test failures

## Reporting Issues

When tests fail:
1. Check Python version compatibility
2. Verify dependencies are installed
3. Check file permissions
4. Review test output for specific error messages
5. Ensure test directories are writable

---

**Last Updated:** 2025
**Test Suite Version:** 2.0 (includes Flask web interface tests)

