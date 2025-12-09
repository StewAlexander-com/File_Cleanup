# Easy File Cleanup

Organizes files by extension into dedicated folders. Perfect for cleaning up cluttered directories.

## At a Glance

- **What it does**: Automatically sorts files into folders by their extension (pdf/, jpg/, txt/, etc.)
- **Who it's for**: Non-technical users (web UI), terminal users (TUI), and developers/devops (automation)
- **Quick start**: Download the app and double-click (Flask already bundled)  
  - macOS: [Mac File Cleanup](https://github.com/StewAlexander-com/File_Cleanup/releases/download/v2.5/Mac%20File%20Cleanup)  
  - Windows: [Win-File-Cleanup.exe](https://github.com/StewAlexander-com/File_Cleanup/releases/download/v2.5/Win-File-Cleanup.exe)  
  - Or CLI: `python3 Easy-File-Cleanup.py --html` (needs Flask installed) / `python3 Easy-File-Cleanup.py ~/Downloads`

## Table of Contents

- [Easy File Cleanup](#easy-file-cleanup)
  - [At a Glance](#at-a-glance)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Quick Start](#quick-start)
    - [Web Interface (Recommended for beginners)](#web-interface-recommended-for-beginners)
    - [Terminal Interface (TUI)](#terminal-interface-tui)
    - [Command Line (Automation)](#command-line-automation)
  - [Desktop Apps (PyInstaller)](#desktop-apps-pyinstaller)
  - [Features](#features)
    - [Core Functionality](#core-functionality)
    - [Interface Options](#interface-options)
    - [Automation](#automation)
  - [How It Works](#how-it-works)
  - [Usage](#usage)
    - [Basic Command Line](#basic-command-line)
    - [Interactive Mode](#interactive-mode)
    - [Available Flags](#available-flags)
  - [Automation \& Scripting](#automation--scripting)
  - [Testing](#testing)
  - [Documentation](#documentation)
  - [Contributing](#contributing)
  - [License](#license)
  - [Contact](#contact)

## Installation

**Requirements**: Python 3.6+

```bash
git clone https://github.com/StewAlexander-com/File_Cleanup.git
cd File_Cleanup
chmod +x Easy-File-Cleanup.py  # macOS/Linux only
```

**Optional**: For web interface, install Flask:
```bash
pip install Flask
```

## Quick Start

### Web Interface (Recommended for beginners)
```bash
python3 Easy-File-Cleanup.py --html
```
Opens in your browser automatically. See [Web Interface Guide](docs/web.md) for details, features, and troubleshooting.

### Terminal Interface (TUI)
```bash
python3 Easy-File-Cleanup.py --tui ~/Downloads
```
Full-screen terminal browser. See [TUI Guide](docs/tui.md) for keyboard shortcuts and navigation.

### Command Line (Automation)
```bash
python3 Easy-File-Cleanup.py ~/Downloads --yes --quiet
```
Fully automated, no prompts. See [Automation Guide](#automation--scripting) below or [example script](examples/automation.sh).

## Desktop Apps (PyInstaller)

Prefer double-click over the command line? Build or download a small desktop launcher for the web UI. The CLI/TUI stay exactly the same.

- **Download ready-to-run apps (recommended)**:
  - macOS: [Mac File Cleanup](https://github.com/StewAlexander-com/File_Cleanup/releases/download/v2.5/Mac%20File%20Cleanup)
  - Windows: [Win-File-Cleanup.exe](https://github.com/StewAlexander-com/File_Cleanup/releases/download/v2.5/Win-File-Cleanup.exe)
  - Source zip: [EasyFileCleanup-2.5-source.zip](https://github.com/StewAlexander-com/File_Cleanup/releases/download/v2.5/EasyFileCleanup-2.5-source.zip)
- **Run**: Double-click the downloaded file; the web UI opens on `http://127.0.0.1:<port>` (browser auto-opens).
- **Dependencies**: Flask is already bundled in the apps; no install needed. For CLI `--html`, install Flask: `pip install Flask`.
- **Security**: Localhost-only (no external access).
- **Build yourself (optional)**:
  - Requirements: Python 3.x, Flask (`pip install Flask`), PyInstaller (`pip install pyinstaller`)
  - macOS: `./scripts/build_gui_mac.sh`
  - Windows (via GitHub Actions): `gh workflow run build-windows.yml` then download the artifact
  - Windows (native): `powershell -ExecutionPolicy Bypass -File scripts/build_gui_windows.ps1`

## Features

### Core Functionality
- Automatic file organization by extension
- Duplicate handling (interactive or automatic)
- Verification of organization
- Detailed logging
- Cross-platform (Windows, macOS, Linux)

### Interface Options
- **Web UI**: Point-and-click interface with visual feedback, graphs, and directory tree ([see guide](docs/web.md))
- **TUI**: Full-screen terminal browser with keyboard navigation ([see guide](docs/tui.md))
- **CLI**: Direct command-line operation for automation

### Automation
- Non-interactive flags for scripts and cron jobs
- Consistent exit codes
- Silent operation mode
- Fast failure on errors

## How It Works

1. Scans directory for files (ignores hidden files)
2. Creates folders by extension (pdf/, jpg/, txt/, etc.)
3. Moves files into matching folders
4. Handles duplicates (prompts or auto-creates copies)
5. Verifies organization
6. Creates/updates `organization_log.txt`

**Example output structure**:
```
Downloads/
├── pdf/
│   ├── document1.pdf
│   └── report.pdf
├── jpg/
│   └── photo.jpg
└── organization_log.txt
```

## Usage

### Basic Command Line

```bash
# Organize specific directory
python3 Easy-File-Cleanup.py ~/Downloads

# Partial path matching
python3 Easy-File-Cleanup.py Downloads

# Current directory
python3 Easy-File-Cleanup.py .
```

### Interactive Mode

Run without arguments for guided selection:
```bash
python3 Easy-File-Cleanup.py
```

### Available Flags

| Flag | Description |
|------|-------------|
| `--html` | Launch web interface (requires Flask) |
| `--tui` | Launch terminal interface |
| `--yes` / `--non-interactive` | Auto-create copies for duplicates |
| `--overwrite` | Auto-overwrite duplicates (use with caution) |
| `--quiet` | Minimal output (for automation) |
| `--help` | Show full help |

## Automation & Scripting

Fully automatable for cron jobs, CI/CD, and scripts.

**Basic automation**:
```bash
python3 Easy-File-Cleanup.py ~/Downloads --yes --quiet
```

**Cron example**:
```bash
0 2 * * * /usr/bin/python3 /path/to/Easy-File-Cleanup.py ~/Downloads --yes --quiet
```

**Exit codes**:
- `0`: Success
- `1`: Error (invalid directory, organization failed)
- `2`: Invalid arguments
- `130`: Interrupted (Ctrl+C)

See [examples/automation.sh](examples/automation.sh) for a complete automation script example.

**Automation features**:
- No interactive prompts with `--yes`/`--non-interactive`/`--overwrite`
- Silent operation with `--quiet` (errors to stderr)
- Fast failure on invalid inputs
- Flag validation prevents conflicts

## Testing

Run the test suite:
```bash
python3 test_file_cleanup.py
```

**Test coverage**: 9 core tests + 18 web interface tests. All tests pass ✅

For detailed testing information, see [TEST_PLAN.md](TEST_PLAN.md).

## Documentation

**User Guides**:
- [Web Interface Guide](docs/web.md) - Detailed web UI documentation, features, and troubleshooting
- [TUI Guide](docs/tui.md) - Terminal interface navigation, keyboard shortcuts, and usage

**Reference**:
- [Test Plan](TEST_PLAN.md) - Testing strategy, coverage, and how to run tests
- [CHANGELOG.md](CHANGELOG.md) - Version history, updates, and release notes
- [Contributing Guidelines](CONTRIBUTING.md) - How to contribute to the project

**Examples**:
- [Automation Script](examples/automation.sh) - Complete automation example for cron jobs

## Contributing

Contributions welcome! See [Contributing Guidelines](CONTRIBUTING.md) for details.

**Quick start**:
1. Fork the repository
2. Create a feature branch
3. Make changes and test
4. Submit a pull request

## License

Open source - available for use and modification.

## Contact

- **GitHub**: [@StewAlexander-com](https://github.com/StewAlexander-com)
- **Repository**: [File_Cleanup](https://github.com/StewAlexander-com/File_Cleanup)
- **Issues**: Open an issue on GitHub

---

**Version**: 2.5 | **Last Updated**: December 2025
