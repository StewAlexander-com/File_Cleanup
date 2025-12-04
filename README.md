# Easy File Cleanup

Easy File Cleanup (`Easy-File-Cleanup.py`) is a Python utility that automatically organizes files by their extension into dedicated folders. Perfect for cleaning up cluttered directories and maintaining an organized file structure.

## Features

- 🗂️ **Automatic Organization**: Sorts files by extension into dedicated folders
- 🔄 **Duplicate Handling**: Interactive prompts for handling duplicate files
- ✅ **Verification**: Automatically verifies that all files are correctly organized
- 📝 **Logging**: Maintains a detailed log of all organization activities
- 🖥️ **Cross-Platform**: Works on Windows, macOS, and Linux
- 🚫 **Safe**: Ignores hidden files and preserves existing folder structures
- 📂 **Directory Browser TUI**: Interactive file browser for easy directory selection (similar to 'nnn')
- ⌨️ **Command-Line Support**: Pass directory paths directly as arguments
- 🔍 **Partial Path Matching**: Find directories by partial name or path
- 🎯 **Simplified Interface**: Quick directory selection with smart defaults
- 🤖 **Fully Scriptable**: Non-interactive flags for automation and cron jobs
- 📋 **Enhanced CLI Help**: Comprehensive help documentation with usage examples

## Installation

### Prerequisites

- Python 3.6 or higher
- No additional dependencies required (uses Python standard library only)

### Setup

1. **Clone the repository** (the code resides in the `File_Cleanup` folder):
   ```bash
   git clone https://github.com/StewAlexander-com/File_Cleanup.git
   cd File_Cleanup
   ```

2. **Make the script executable** (macOS/Linux):
   ```bash
   chmod +x Easy-File-Cleanup.py
   ```

   **Note**: On Windows, this step is optional as Python scripts can be run directly.

3. **Verify Python installation**:
   ```bash
   python3 --version
   # or on Windows:
   python --version
   ```

## How to Run

### Command-Line Usage (Recommended)

You can now pass the directory path directly as a command-line argument.
You can use either the original script name (`file_cleanup.py`) or the
friendlier wrapper script (`Easy-File-Cleanup.py`):

```bash
# Full path
python3 Easy-File-Cleanup.py /path/to/directory
# or
python3 file_cleanup.py /path/to/directory

# Partial path (searches for directories containing the string)
python3 Easy-File-Cleanup.py Downloads

# Home directory shortcut
python3 Easy-File-Cleanup.py ~/Documents

# Interactive mode (no arguments)
python3 Easy-File-Cleanup.py
```

**Examples**:
```bash
# Organize Downloads folder
python3 Easy-File-Cleanup.py ~/Downloads

# Organize current directory
python3 Easy-File-Cleanup.py .

# Find and organize a directory by partial name
python3 Easy-File-Cleanup.py MyProject
```

### Interactive Mode

If you run without arguments, you'll be prompted for the directory:

```bash
python3 Easy-File-Cleanup.py
```

You'll see:
```
Enter directory path (or press Enter for current directory):
Path: 
```

- **Enter a path**: Type full or partial path (e.g., `Downloads`, `/Users/name/Documents`)
- **Press Enter**: Uses current directory
- **Path not found**: Option to browse directories or cancel

### macOS and Linux

**Method 1: Direct execution** (if made executable):
```bash
./Easy-File-Cleanup.py [directory]
```

**Method 2: Using Python interpreter**:
```bash
python3 Easy-File-Cleanup.py [directory]
```

### Windows

**Method 1: Using Python launcher**:
```bash
python Easy-File-Cleanup.py [directory]
```

**Method 2: Using Python 3 explicitly**:
```bash
py -3 Easy-File-Cleanup.py [directory]
```

**Method 3: Double-click** (if Python is associated with `.py` files):
- Simply double-click `Easy-File-Cleanup.py` in File Explorer

### Automation & Scripting Mode

The script is fully automation-ready with non-interactive flags:

```bash
# Fully automated (for scripts, cron jobs, automation)
python3 file_cleanup.py ~/Downloads --yes --quiet

# Auto-create copies for duplicates (safe for automation)
python3 file_cleanup.py Downloads --non-interactive

# Auto-overwrite duplicates (use with caution)
python3 file_cleanup.py Downloads --overwrite

# Minimal output (useful for automation)
python3 file_cleanup.py Downloads --quiet
```

**Available Flags**:
- `--yes` / `--non-interactive`: Automatically create copies for duplicates (no prompts)
- `--overwrite`: Automatically overwrite duplicate files (use with caution)
- `--quiet`: Minimal output (useful for automation scripts)
- `--help`: Display comprehensive help documentation

**Exit Codes** (for automation):
- `0`: Success
- `1`: Error (invalid directory, organization failed, etc.)
- `130`: Interrupted by user (Ctrl+C)

### Advanced Usage

1. **Command-line argument**: Pass directory path directly
   ```bash
   python3 file_cleanup.py /path/to/organize
   ```

2. **Partial path matching**: The program will search for directories matching your input
   ```bash
   python3 file_cleanup.py Downloads  # Finds any directory with "Downloads" in the name
   ```

3. **Interactive mode**: Run without arguments for guided selection
   - Enter path manually or press Enter for current directory
   - If path not found, option to browse directories

4. **View help**: Get comprehensive usage information
   ```bash
   python3 file_cleanup.py --help
   ```

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

### Example Sessions

**Example 1: Command-Line Usage**
```bash
$ python3 file_cleanup.py ~/Downloads

File Organizer v1.0
============================================================
✓ Found directory: /Users/username/Downloads

Organizing: Downloads/
------------------------------------------------------------
✓ Created: pdf/
  → document1.pdf
  → report.pdf
✓ Created: jpg/
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

**Example 2: Partial Path Matching**
```bash
$ python3 file_cleanup.py Downloads

File Organizer v1.0
============================================================
✓ Found directory: /Users/username/Downloads

Organizing: Downloads/
...
```

**Example 3: Interactive Mode**
```bash
$ python3 file_cleanup.py

File Organizer v1.0
============================================================

Enter directory path (or press Enter for current directory):
Path: MyProject

✓ Found directory: /Users/username/MyProject

Organizing: MyProject/
...
```

**Example 4: Using Directory Browser (when path not found)**
```bash
$ python3 file_cleanup.py

Enter directory path (or press Enter for current directory):
Path: NonexistentPath

✗ Could not find directory matching: NonexistentPath

Would you like to:
  [1] Try browsing directories
  [2] Cancel

Enter choice: 1

[Directory Browser opens - navigate with arrow keys, press Enter to select]
...
```

## What the Program Does

### Core Functionality

1. **File Scanning**: Scans the specified directory for all files (excluding hidden files starting with `.`)

2. **Folder Creation**: Creates folders named after file extensions (e.g., `pdf/`, `jpg/`, `txt/`). Files without extensions go into a `no_extension/` folder.

3. **File Organization**: Moves each file into its corresponding extension folder

4. **Duplicate Handling**: 
   - **Interactive mode (default)**: Prompts for each duplicate file
   - **Non-interactive mode (`--yes`/`--non-interactive`)**: Automatically creates copies (`file_copy1.ext`, `file_copy2.ext`, etc.)
   - **Overwrite mode (`--overwrite`)**: Automatically overwrites existing files (use with caution)
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

The project includes a simplified, focused test suite that verifies core functionality with real mock files.

### Running Tests

To run the test suite:

```bash
python3 test_file_cleanup.py
```

**Note**: On Windows, use `python` instead of `python3`.

### Test Coverage

The test suite includes **9 focused tests** covering core functionality:

#### Core Functionality Tests
- ✅ **Folder Creation**: Verifies extension-based folders are created correctly
- ✅ **File Organization**: Tests that files are moved to correct extension folders
- ✅ **Case-Insensitive Extensions**: Tests that `.PDF`, `.pdf`, and `.Pdf` all go to the same folder
- ✅ **No Extension Handling**: Ensures files without extensions go into `no_extension/` folder
- ✅ **Hidden Files**: Confirms hidden files (starting with `.`) are properly ignored

#### Duplicate Handling Tests
- ✅ **Copy Creation**: Verifies automatic copy naming (`_copy1`, `_copy2`, etc.) when duplicates exist

#### Verification and Logging Tests
- ✅ **Organization Verification**: Tests detection of correctly organized files
- ✅ **Log Creation**: Verifies log file is created with correct format and content

#### Integration Tests
- ✅ **Main Function**: Tests end-to-end execution with command-line arguments
- ✅ **Interactive Mode**: Tests main function in interactive mode (no arguments)

### Test Results

All tests are currently **passing** ✅:

```
----------------------------------------------------------------------
Ran 9 tests in 0.072s

OK
```

**Test Features:**
- Creates mock files with various extensions automatically
- Tests real file organization in isolated temporary directories
- Verifies all core functionality works correctly
- Fast execution with no hanging or blocking operations

### Test Architecture

- **Isolated Testing**: Each test runs in a temporary directory that is automatically cleaned up
- **Mock Files**: Automatically creates 17+ mock files with various extensions for realistic testing
- **Mocking**: Uses `unittest.mock` to handle interactive prompts during testing
- **No Side Effects**: Tests don't modify your actual files or directories
- **Fast Execution**: All tests complete in under 0.1 seconds
- **Cross-Platform**: Works identically on Windows, macOS, and Linux

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

- **GitHub**: [@StewAlexander-com](https://github.com/StewAlexander-com)
- **Repository**: [`StewAlexander-com/File_Cleanup`](https://github.com/StewAlexander-com/File_Cleanup)

For questions, bug reports, or feature requests, please open an issue on GitHub.

## License

This project is open source and available for use and modification.

---

**Version**: 1.2  
**Last Updated**: 2025

### Recent Updates

**v1.2** (Latest):
- 🤖 **Full Scriptability**: Added `--yes`, `--non-interactive`, `--overwrite`, and `--quiet` flags
- 📋 **Enhanced CLI Help**: Comprehensive help documentation with usage examples
- 🔧 **Automation Ready**: Proper exit codes and non-interactive modes for cron jobs and scripts
- 🔇 **Quiet Mode**: Minimal output option for automation pipelines

**v1.1**:
- ✨ **Command-Line Arguments**: Pass directory paths directly as arguments
- 🔍 **Partial Path Matching**: Find directories by partial name or path
- 🎯 **Simplified Interface**: Quick directory selection with smart defaults
- 🧪 **Refactored Tests**: Streamlined test suite with automatic mock file generation
- 🚀 **Performance**: Faster execution and improved user experience

