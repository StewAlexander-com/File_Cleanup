# Web Interface Guide

The web interface provides a point-and-click way to organize files with visual feedback and real-time updates.

**Navigation**: [← Back to README](../README.md) | [TUI Guide](tui.md) | [Test Plan](../TEST_PLAN.md)

## Launching

```bash
python3 Easy-File-Cleanup.py --html
```

The server will:
- Automatically find an available port (starts from 5000)
- Open your browser automatically
- Display the URL if auto-open fails
- Run securely on localhost only (127.0.0.1)

## Interface Overview

The interface has two main panels:

**Left Panel - Directory Browser**:
- Navigate directories with breadcrumb navigation
- Click folders to browse, or use path input field
- View files and subdirectories in a scrollable list
- Auto-refresh indicator shows when polling is active
- Options for non-interactive mode and overwrite behavior

**Right Panel - Results & Logs**:
- **Results Tab**: Statistics, cleanup history graph, directory tree
- **Logs Tab**: View organization logs for the current directory

## Features

### Directory Browsing
- Breadcrumb navigation for quick path access
- Path input field for direct navigation
- Home and Up buttons for quick navigation
- Auto-refresh detects directory changes automatically

### Cleanup Results
- Statistics cards (Files Organized, Folders Created, Verification Status)
- Cleanup history graph showing trends over time
- Expandable/collapsible directory tree view
  - NEW folders (created during cleanup) start expanded
  - EXISTING folders start collapsed
  - Visual indicators for folder status

### Logs
- View organization logs for the current directory
- Syntax-highlighted log display
- Refresh button to reload logs

### Server Controls
Access via the ⚙️ Server button in the header:
- View server status (host, port, security mode)
- Stop server gracefully
- Restart server (with instructions)

## Usage

1. **Navigate** to the directory you want to organize
2. **Select options**:
   - Non-interactive mode: Auto-create copies for duplicates
   - Overwrite: Auto-overwrite duplicates (use with caution)
3. **Click "Organize Files"** to start cleanup
4. **View results** in the Results tab (auto-switches after cleanup)
5. **Check logs** in the Logs tab if needed

## Security

The web interface is secured by:
- Localhost-only binding (127.0.0.1)
- No external network access
- Secure headers for browser compatibility

## Troubleshooting

**Port already in use**: The server automatically finds an available port. Check the console output for the actual port number.

**Browser doesn't open**: Copy the URL from the console and paste it into your browser.

**Access denied errors**: 
- Make sure no other process is using the port
- Try `http://localhost:PORT` instead of `127.0.0.1:PORT`
- Check browser security settings

---

**Related Documentation**:
- [README](../README.md) - Main documentation and quick start
- [TUI Guide](tui.md) - Terminal interface alternative
- [Automation Guide](../README.md#automation--scripting) - For scripted usage
- [CHANGELOG](../CHANGELOG.md) - Version history

