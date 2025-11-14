# File Cleanup

A Python utility that automatically organizes files by their extension into dedicated folders. Perfect for cleaning up cluttered directories and maintaining an organized file structure.

## Features

- 🗂️ **Automatic Organization**: Sorts files by extension into dedicated folders
- 🔄 **Duplicate Handling**: Interactive prompts for handling duplicate files
- ✅ **Verification**: Automatically verifies that all files are correctly organized
- 📝 **Logging**: Maintains a detailed log of all organization activities
- 🖥️ **Cross-Platform**: Works on Windows, macOS, and Linux
- 🚫 **Safe**: Ignores hidden files and preserves existing folder structures

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
2. When prompted, enter the directory path you want to organize:
   - Enter a full path: `/Users/username/Documents/Downloads`
   - Enter a relative path: `./Downloads` or `../Documents`
   - Press Enter or type `.` to use the current directory
3. The program will:
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

Enter directory path to organize (or '.' for current): ./Downloads

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
3. **Make your changes** and test thoroughly
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
- Unit tests and test coverage
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

