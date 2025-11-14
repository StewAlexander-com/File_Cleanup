# File Cleanup

A Python utility that automatically organizes files by their extension into dedicated folders. Perfect for cleaning up cluttered directories and maintaining an organized file structure.

## Features

- 🗂️ **Automatic Organization**: Sorts files by extension into dedicated folders
- 🔄 **Duplicate Handling**: Interactive prompts for handling duplicate files
- ✅ **Verification**: Automatically verifies that all files are correctly organized
- 📝 **Logging**: Maintains a detailed log of all organization activities
- 🖥️ **Cross-Platform**: Works on Windows, macOS, and Linux
- 🚫 **Safe**: Ignores hidden files and preserves existing folder structures
- 📂 **Directory Browser TUI**: Interactive file browser for easy directory selection (similar to 'nnn')

## Installation

### Prerequisites

- Python 3.6 or higher
- No additional dependencies required (uses Python standard library only)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/stewartalexander/File_Cleanup.git
   cd File_Cleanup
   ```

2. **Make the script executable** (macOS/Linux):
   ```bash
   chmod +x file_cleanup.py
   ```

   **Note**: On Windows, this step is optional as Python scripts can be run directly.

3. **Verify Python installation**:
   ```bash
   python3 --version
   # or on Windows:
   python --version
   ```

## How to Run

### macOS and Linux

**Method 1: Direct execution** (if made executable):
```bash
./file_cleanup.py
```

**Method 2: Using Python interpreter**:
```bash
python3 file_cleanup.py
```

### Windows

**Method 1: Using Python launcher**:
```bash
python file_cleanup.py
```

**Method 2: Using Python 3 explicitly**:
```bash
py -3 file_cleanup.py
```

**Method 3: Double-click** (if Python is associated with `.py` files):
- Simply double-click `file_cleanup.py` in File Explorer

### Usage

1. Run the script using one of the methods above
2. When prompted, choose how to select the directory:
   - **[1] Type path manually**: Enter the full or relative path
   - **[2] Browse directories**: Use the interactive directory browser (TUI)
   - **[3] Use current directory**: Select the current working directory
   - **[q] Cancel**: Exit the program

3. **Directory Browser (Option 2)**:
   - **macOS/Linux**: Uses `curses` for a full-screen file browser with arrow key navigation
   - **Windows**: Uses a simple numbered menu interface
   - **Navigation**:
     - Arrow keys (↑↓) to navigate directories
     - **Enter** to navigate into a selected directory (go down a level)
     - **`s` key** to select the current directory
     - ← or `b` to go up one level
     - **Number keys (1-9)**: Jump directly to parent levels (1=parent, 2=grandparent, etc.)
     - Breadcrumb shortcuts displayed at top show which number corresponds to which level
   - **Quick Actions**:
     - Type `t` to manually enter a path while browsing
     - Type `h` to jump to home directory
     - Type `q` or ESC to cancel

4. The program will:
   - Scan for files in the directory
   - Create folders based on file extensions (e.g., `pdf/`, `jpg/`, `txt/`)
   - Move files into their respective folders
   - Prompt you if duplicate files are found
   - Verify the organization
   - Create/update a log file

### Example Session

```
File Organizer v1.0
============================================================

How would you like to select the directory?
  [1] Type path manually
  [2] Browse directories
  [3] Use current directory (.)
  [q] Cancel

Enter choice: 2

[Directory Browser opens - navigate with arrow keys, press Enter to select]

Organizing: Downloads/
------------------------------------------------------------
✓ Created: pdf/
  → document1.pdf
  → report.pdf
→ Using: jpg/
  → photo.jpg
  → image.jpg

⚠ 'duplicate.txt' exists in txt/. Overwrite? (y/n): n
  → duplicate_copy1.txt

--- Verification ---
✓ All files organized correctly

✓ Log updated: organization_log.txt

============================================================
✓ Organization complete
```

## What the Program Does

### Core Functionality

1. **File Scanning**: Scans the specified directory for all files (excluding hidden files starting with `.`)

2. **Folder Creation**: Creates folders named after file extensions (e.g., `pdf/`, `jpg/`, `txt/`). Files without extensions go into a `no_extension/` folder.

3. **File Organization**: Moves each file into its corresponding extension folder

4. **Duplicate Handling**: 
   - If a file with the same name already exists in the target folder, you'll be prompted to overwrite or create a copy
   - Copies are automatically named with `_copy1`, `_copy2`, etc.

5. **Verification**: Recursively checks that all files are in the correct folders based on their extensions

6. **Logging**: Creates or appends to `organization_log.txt` with:
   - Timestamp of each run
   - List of folders created or used
   - Files moved into each folder
   - Status (NEW folder vs EXISTING folder)

### Output

The program produces:

- **Organized directory structure**: Files sorted into extension-based folders
- **Console output**: Real-time feedback showing:
  - Folders created or reused
  - Files being moved
  - Verification results
- **Log file** (`organization_log.txt`): Detailed history of all organization runs

### Example Output Structure

```
Downloads/
├── pdf/
│   ├── document1.pdf
│   └── report.pdf
├── jpg/
│   ├── photo.jpg
│   └── image.jpg
├── txt/
│   ├── notes.txt
│   └── duplicate_copy1.txt
└── organization_log.txt
```

## Testing

The project includes a comprehensive test suite to ensure reliability and correctness of all functionality.

### Running Tests

To run the complete test suite:

```bash
python3 test_file_cleanup.py
```

**Note**: On Windows, use `python` instead of `python3`.

### Test Coverage

The test suite includes **59+ comprehensive tests** covering all aspects of the program:

#### Core Functionality Tests
- ✅ **File Extension Extraction**: Tests case-insensitive extension handling and files without extensions
- ✅ **Basic File Organization**: Verifies files are correctly sorted into extension-based folders
- ✅ **No Extension Handling**: Ensures files without extensions go into `no_extension/` folder
- ✅ **Hidden Files**: Confirms hidden files (starting with `.`) are properly ignored
- ✅ **Case-Insensitive Extensions**: Tests that `.PDF`, `.pdf`, and `.Pdf` all go to the same folder

#### Duplicate Handling Tests
- ✅ **Overwrite Option**: Tests interactive overwrite when duplicates are found
- ✅ **Copy Creation**: Verifies automatic copy naming (`_copy1`, `_copy2`, etc.)
- ✅ **Multiple Copies**: Tests sequential copy generation when multiple copies exist

#### Advanced Features Tests
- ✅ **Existing Folders**: Verifies reuse of pre-existing extension folders
- ✅ **Organization Verification**: Tests detection of correctly and incorrectly organized files
- ✅ **Top-Level File Detection**: Ensures verification catches misplaced files
- ✅ **Log File Handling**: Confirms log files are allowed in top-level directory

#### Logging Tests
- ✅ **Log Creation**: Verifies log file is created with correct format
- ✅ **Log Appending**: Tests that multiple runs append to log rather than overwrite
- ✅ **Log Content**: Validates log includes all required information (timestamps, file lists, folder status)

#### Integration Tests
- ✅ **Complete Workflow**: Tests end-to-end execution from main function
- ✅ **Invalid Directory Handling**: Verifies error handling for non-existent directories
- ✅ **Empty Directory Handling**: Tests behavior when no files are present

#### Directory Browser TUI Tests
- ✅ **Simple Browser Initialization**: Tests browser initialization with default and custom paths
- ✅ **Directory Listing**: Verifies correct directory and file listing (hidden files excluded)
- ✅ **Navigation**: Tests all navigation options (quit, select, home, go up, select directory)
- ✅ **Path Input**: Tests manual path entry with valid, invalid, and empty paths
- ✅ **Browse Loop**: Tests complete browse workflow with navigation and selection
- ✅ **get_directory_path Function**: Tests all selection methods (manual, browse, current directory)
- ✅ **browse_directory Function**: Tests browser selection logic (curses vs simple mode)
- ✅ **Curses Browser**: Tests CursesDirectoryBrowser initialization and directory listing
- ✅ **Breadcrumb Navigation**: Tests breadcrumb generation and number key (1-9) navigation
- ✅ **Multi-Level Navigation**: Tests jumping to parent, grandparent, and deeper levels
- ✅ **Navigate Into Directories**: Tests Enter key navigation into subdirectories
- ✅ **Select Current Directory**: Tests 's' key to select current directory
- ✅ **Path Expansion**: Tests tilde expansion and path resolution
- ✅ **Cross-Platform Compatibility**: Ensures tests work on all operating systems

### Test Results

All tests are currently **passing** ✅:

```
----------------------------------------------------------------------
Ran 50+ tests in <1s

OK
```

**Test Breakdown:**
- **18 tests** for file cleanup functionality (`file_cleanup.py`)
- **41+ tests** for directory browser functionality (`directory_browser.py`)

### Test Architecture

- **Isolated Testing**: Each test runs in a temporary directory that is automatically cleaned up
- **Mocking**: Uses `unittest.mock` to handle interactive prompts during testing
- **Comprehensive Coverage**: Tests cover normal operations, edge cases, and error conditions
- **No Side Effects**: Tests don't modify your actual files or directories
- **Non-Blocking**: All tests are designed to be non-interactive and safe to run in IDEs like Cursor
- **Full Mocking**: All blocking operations (input, os.system, curses) are fully mocked to prevent hangs

### Running Tests on Different Operating Systems

The test suite is **cross-platform** and works identically on Windows, macOS, and Linux:

**macOS/Linux**:
```bash
python3 test_file_cleanup.py
```

**Windows**:
```bash
python test_file_cleanup.py
```

All tests use Python's standard library and `pathlib`, ensuring consistent behavior across platforms.

## Why This Program is Useful

### Common Use Cases

- **Downloads Folder Cleanup**: Organize years of accumulated downloads
- **Project Organization**: Keep project directories tidy by file type
- **Media Management**: Separate images, videos, and documents
- **Archive Preparation**: Organize files before backing up or archiving
- **Workspace Maintenance**: Regular cleanup of cluttered workspaces

### Benefits

- ⏱️ **Time Saving**: Automates manual file sorting that would take hours
- 🎯 **Consistency**: Ensures uniform organization across different directories
- 📊 **Accountability**: Log file provides a complete history of changes
- 🛡️ **Safety**: Interactive duplicate handling prevents accidental data loss
- 🔍 **Easy Retrieval**: Files grouped by type are easier to find later

## Contributing

Contributions are welcome! Here are ways you can help improve File Cleanup:

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** and test thoroughly:
   ```bash
   python3 test_file_cleanup.py  # Verify all tests pass
   ```
4. **Commit your changes**:
   ```bash
   git commit -m "Add: description of your feature"
   ```
5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Open a Pull Request** on GitHub

### Areas for Contribution

- Additional file type recognition and categorization
- Configuration file support for custom organization rules
- GUI interface development
- Performance optimizations for large directories
- Additional logging and reporting features
- Additional test cases and edge case coverage
- Documentation improvements

### Code Style

- Follow PEP 8 Python style guidelines
- Include docstrings for all functions
- Add comments for complex logic
- Maintain backward compatibility when possible

## Contact

**Owner**: Stewart Alexander

- **GitHub**: [@stewartalexander](https://github.com/stewartalexander)
- **Repository**: [File_Cleanup](https://github.com/stewartalexander/File_Cleanup)

For questions, bug reports, or feature requests, please open an issue on GitHub.

## License

This project is open source and available for use and modification.

---

**Version**: 1.0  
**Last Updated**: 2025

