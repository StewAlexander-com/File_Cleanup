# Easy File Cleanup

Easy File Cleanup (`Easy-File-Cleanup.py`) is a Python utility that automatically organizes files by their extension into dedicated folders. Perfect for cleaning up cluttered directories and maintaining an organized file structure.

## Features

- 🗂️ **Automatic Organization**: Sorts files by extension into dedicated folders
- 🔄 **Duplicate Handling**: Interactive prompts for handling duplicate files
- ✅ **Verification**: Automatically verifies that all files are correctly organized
- 📝 **Logging**: Maintains a detailed log of all organization activities
- 🖥️ **Cross-Platform**: Works on Windows, macOS, and Linux
- 🚫 **Safe**: Ignores hidden files and preserves existing folder structures
- 📂 **ncurses Directory Browser TUI**: Full-screen terminal interface for directory browsing (similar to 'nnn') - automatically available in interactive mode
- ⌨️ **Command-Line Support**: Pass directory paths directly as arguments
- 🔍 **Partial Path Matching**: Find directories by partial name or path
- 🎯 **Simplified Interface**: Quick directory selection with smart defaults
- 🤖 **Fully Scriptable**: Non-interactive flags for automation and cron jobs
- 📋 **Enhanced CLI Help**: Comprehensive help documentation with usage examples
- 🌐 **Web GUI Interface**: Modern web-based interface with directory browsing, cleanup operations, and visualization
- 📊 **Cleanup History Graph**: Visual timeline of cleanup operations with Chart.js
- 📂 **Directory Tree View**: Expandable/collapsible directory structure visualization
- 🔄 **Auto-Refresh**: Automatic polling with exponential backoff to detect directory changes
- 🔒 **Secure**: Localhost-only binding for security
- ⚙️ **Server Controls**: Stop and restart server from web interface

## Installation

### Prerequisites

- Python 3.6 or higher
- **For CLI mode**: No additional dependencies required (uses Python standard library only)
- **For Web GUI mode**: Flask (install with `pip install Flask` or `pip install -r requirements.txt`)

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

### Web Interface (Recommended for Interactive Use)

Launch the modern web-based GUI for the easiest experience:

```bash
python3 Easy-File-Cleanup.py --html
```

**Features**:
- 🖱️ **Point-and-Click**: Navigate directories with your mouse
- 📊 **Visual Feedback**: See cleanup results with graphs and statistics
- 📂 **Directory Tree**: Expandable/collapsible folder structure view
- 🔄 **Auto-Refresh**: Automatically detects and shows directory changes
- 📝 **Log Viewer**: View organization logs directly in the browser
- ⚙️ **Server Controls**: Manage server from the web interface

The server will:
- Automatically find an available port (starts from 5000)
- Open your browser automatically
- Display the URL if auto-open fails
- Run securely on localhost only (127.0.0.1)

**Web Interface Features**:

The web interface provides a modern, user-friendly way to organize files with a clean, responsive design:

**Interface Layout**:

```
+================================================================================+
|  File Cleanup                                              [Server Controls]   |
|  Organize files by extension into dedicated folders                            |
+==========================================+=====================================+
|                                          |                                     |
|  Directory Browser                       |  Results Tab | Logs Tab             |
|                                          |                                     |
|  Breadcrumbs: / > home                   |  Statistics:                        |
|  [Path Input] [Go] [Home]                |    Files: 15  Folders: 8            |
|                                          |                                     |
|  Directories:                            |  Cleanup History Graph              |
|    folder1/                              |    [Chart visualization]            |
|    folder2/                              |                                     |
|    folder3/                              |  Directory Structure:               |
|                                          |    > pdf/ (NEW)                     |
|  Files:                                  |      - document1.pdf                |
|    file1.txt                             |      - document2.pdf                |
|    file2.pdf                             |    > jpg/ (NEW)                     |
|    image.jpg                             |      - photo1.jpg                   |
|                                          |    > txt/ (EXISTING)                |
|  Options:                                |      - notes.txt                    |
|    [x] Non-interactive                   |                                     |
|    [ ] Overwrite                         |  [Expand All] [Collapse All]        |
|                                          |                                     |
|  [Organize Files]                        |                                     |
|                                          |                                     |
+==========================================+=====================================+
```

**Left Panel - Directory Browser**:
- Navigate directories with breadcrumb navigation
- Click folders to browse, or use path input field
- View files and subdirectories in a scrollable list
- Auto-refresh indicator (green dot) shows when polling is active
- Home and Up buttons for quick navigation
- Options for non-interactive mode and overwrite behavior

**Right Panel - Results & Logs**:
- **Results Tab**: 
  - Statistics cards showing Files Organized, Folders Created, and Verification Status
  - Cleanup history graph (Chart.js) showing trends over time
  - Detailed file organization results with folder status (NEW/EXISTING)
  - Expandable/collapsible directory tree view
    - NEW folders (created during cleanup) start expanded
    - EXISTING folders start collapsed
    - Expand All / Collapse All buttons
    - Visual indicators for folder status
- **Logs Tab**: 
  - View organization logs for the current directory
  - Syntax-highlighted log display
  - Refresh button to reload logs

**Header Controls**:
- Server button (⚙️) for server management:
  - View server status (host, port, security mode)
  - Stop server gracefully
  - Restart server (with instructions)

**Design Features**:
- Modern gradient header with purple/blue theme
- Responsive layout (adapts to screen size)
- Smooth animations and transitions
- Color-coded status indicators
- Intuitive icons and visual feedback

### Terminal User Interface (TUI) - ncurses Directory Browser

For users who prefer a terminal-based interface, the application includes a powerful ncurses-based directory browser (similar to 'nnn' or 'ranger'). 

**Launch the TUI**:
```bash
# Direct launch with --tui flag (recommended)
python3 Easy-File-Cleanup.py --tui

# Start TUI from a specific directory
python3 Easy-File-Cleanup.py --tui ~/Downloads

# Alternative: Run without arguments and choose option [2] Browse directories
python3 Easy-File-Cleanup.py
# When prompted, choose option [2] Browse directories
```

**Features**:
- 🖥️ **Full-Screen Terminal Interface**: Beautiful ncurses-based UI (macOS/Linux)
- ⌨️ **Keyboard Navigation**: Fast, keyboard-driven directory browsing
- 📍 **Breadcrumb Navigation**: Quick jump to parent directories with number keys (1-9)
- 🔍 **Smart Path Input**: Type paths manually while browsing
- 🏠 **Quick Navigation**: Jump to home directory instantly
- 🪟 **Windows Support**: Falls back to simple numbered menu on Windows

**Navigation Controls** (macOS/Linux with ncurses):

| Key | Action |
|-----|--------|
| `↑` `↓` | Navigate up/down through directories |
| `Enter` | Enter selected directory |
| `s` | **Select** current directory for cleanup |
| `←` or `b` | Go up one directory level |
| `1-9` | Jump directly to parent levels (1=parent, 2=grandparent, etc.) |
| `t` | Type path manually |
| `h` | Jump to home directory |
| `q` or `ESC` | Cancel and exit |

**Breadcrumb Shortcuts**:
The TUI displays breadcrumb shortcuts at the top showing which number key (1-9) corresponds to which parent directory level. This allows instant navigation to any ancestor directory without multiple "up" commands.

**Example Usage**:
```bash
$ python3 Easy-File-Cleanup.py

Enter directory path (or press Enter for current directory):
Path: NonexistentPath

✗ Could not find directory matching: NonexistentPath

Would you like to:
  [1] Try browsing directories
  [2] Cancel

Enter choice: 1

[Full-screen ncurses directory browser opens]
[Navigate with arrow keys, press 's' to select, 'q' to cancel]
```

**Windows Users**:
On Windows (where ncurses is not available), the TUI automatically falls back to a simple numbered menu interface that provides the same functionality with a different presentation.

**When to Use TUI vs Web Interface**:
- **Use TUI** when: Working in terminal, prefer keyboard navigation, no browser needed, minimal dependencies
- **Use Web Interface** when: Want visual graphs, prefer mouse navigation, need to view logs in browser, want to see directory tree visualization

### Command-Line Usage

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
- **Path not found**: Option to browse directories using the **ncurses TUI** (full-screen terminal browser) or cancel

When you choose to browse directories, the ncurses directory browser will open automatically (on macOS/Linux) or a simple numbered menu (on Windows). See the [Terminal User Interface (TUI)](#terminal-user-interface-tui---ncurses-directory-browser) section for navigation details.

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

The script is **fully automatable** and designed for use in scripts, cron jobs, CI/CD pipelines, and automation workflows. All interactive prompts can be bypassed with command-line flags.

**Fully Automated Examples**:
```bash
# Fully automated (for scripts, cron jobs, automation)
python3 Easy-File-Cleanup.py ~/Downloads --yes --quiet

# Auto-create copies for duplicates (safe for automation)
python3 Easy-File-Cleanup.py Downloads --non-interactive

# Auto-overwrite duplicates (use with caution)
python3 Easy-File-Cleanup.py Downloads --overwrite --quiet

# Minimal output (useful for automation)
python3 Easy-File-Cleanup.py Downloads --quiet --yes
```

**Automation Features**:
- ✅ **No Interactive Prompts**: All user prompts bypassed with `--yes`, `--non-interactive`, or `--overwrite`
- ✅ **Silent Operation**: `--quiet` flag suppresses all output (errors still go to stderr)
- ✅ **Consistent Exit Codes**: Reliable exit codes for automation scripts
- ✅ **Fast Failure**: Invalid directories fail immediately with proper exit codes
- ✅ **Flag Validation**: Prevents conflicting flags (automation + interactive)
- ✅ **Error Handling**: All errors return proper exit codes, no hanging

**Available Flags**:
- `--yes` / `--non-interactive`: Automatically create copies for duplicates (no prompts)
- `--overwrite`: Automatically overwrite duplicate files (use with caution)
- `--quiet`: Minimal output (useful for automation scripts)
- `--html`: Launch web-based GUI interface (requires Flask) - *Not for automation*
- `--tui`: Launch terminal user interface (ncurses directory browser) - *Not for automation*
- `--help` / `-h`: Display comprehensive help documentation

**Exit Codes** (for automation):
- `0`: Success (files organized successfully)
- `1`: Error (invalid directory, organization failed, verification failed, etc.)
- `2`: Invalid arguments or flag conflicts
- `130`: Interrupted by user (Ctrl+C)

**Automation Best Practices**:
1. **Always provide a directory path** when using automation flags
2. **Use `--quiet`** for cron jobs and scripts to suppress output
3. **Use `--yes` or `--non-interactive`** to avoid duplicate file prompts
4. **Check exit codes** in your automation scripts
5. **Never combine automation flags with `--html` or `--tui`** (will error)

**Example Automation Script**:
```bash
#!/bin/bash
# Example cron job script

DIRECTORY="$HOME/Downloads"
SCRIPT="/path/to/Easy-File-Cleanup.py"

# Run cleanup with full automation
if python3 "$SCRIPT" "$DIRECTORY" --yes --quiet; then
    echo "$(date): Cleanup successful" >> /var/log/file-cleanup.log
else
    echo "$(date): Cleanup failed (exit code: $?)" >> /var/log/file-cleanup.log
    exit 1
fi
```

**Cron Job Example**:
```bash
# Run cleanup every day at 2 AM
0 2 * * * /usr/bin/python3 /path/to/Easy-File-Cleanup.py ~/Downloads --yes --quiet
```

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
   python3 Easy-File-Cleanup.py --help
   ```

5. **Web Interface**: Launch the modern web-based GUI
   ```bash
   python3 Easy-File-Cleanup.py --html
   ```
   - Automatically opens browser (or shows URL)
   - Directory browsing with breadcrumb navigation
   - File organization with visual feedback
   - Cleanup history graphs
   - Directory structure tree view
   - Log viewing
   - Server controls

6. **Terminal User Interface (TUI)**: Launch the ncurses directory browser
   ```bash
   python3 Easy-File-Cleanup.py --tui
   python3 Easy-File-Cleanup.py --tui ~/Downloads  # Start from specific directory
   ```
   - Direct launch of full-screen terminal directory browser
   - See the [Terminal User Interface (TUI)](#terminal-user-interface-tui---ncurses-directory-browser) section above for full details
   - Full-screen terminal interface with keyboard navigation
   - Breadcrumb shortcuts for quick parent directory access

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

### Web Interface Tests

The project also includes comprehensive tests for the Flask web interface:

```bash
# Run web interface tests (requires Flask)
python3 test_web_interface.py
```

**Test Coverage** (18 tests):
- ✅ API endpoint functionality
- ✅ Directory browsing and navigation
- ✅ File cleanup operations
- ✅ Server status and controls
- ✅ Security features (localhost-only binding)
- ✅ Integration workflows

**Note**: Web interface tests gracefully skip if Flask is not installed, allowing the test suite to run on systems without Flask.

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

**Version**: 2.0  
**Last Updated**: December 2025

### Recent Updates

**v2.0** (Latest):
- 🌐 **Web GUI Interface**: Modern web-based interface with full directory browsing
- 📊 **Cleanup History Graph**: Visual timeline of cleanup operations using Chart.js
- 📂 **Directory Tree View**: Expandable/collapsible directory structure with NEW/EXISTING indicators
- 🔄 **Auto-Refresh**: Intelligent polling with exponential backoff to detect directory changes
- 🔒 **Security**: Localhost-only binding enforced for safe local access
- ⚙️ **Server Controls**: Stop and restart server from web interface
- 🔍 **Port Detection**: Automatic port conflict detection and resolution
- 📝 **Comprehensive Documentation**: Full docstrings for all functions
- 🧪 **Web Interface Tests**: Complete test suite for Flask GUI (18 tests)
- 📋 **Enhanced Help**: Improved --help flag with installation and examples

**v1.2**:
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

