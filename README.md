# Easy File Cleanup

Organizes files by extension into dedicated folders to quickly clean up messy directories (like Downloads) on any OS. **Files are moved only within your chosen directory, and an `organization_log.txt` tracks every change so you can review what happened.**

**Why this tool?**
- **No network access** — runs entirely locally, your files never leave your machine
- **Reversible** — complete log file tracks every move for easy review and undo
- **Automation-friendly** — works great in cron jobs and CI/CD pipelines
- **Multiple interfaces** — choose web UI, terminal UI, or command-line automation
- **Cross-platform** — works on Windows, macOS, and Linux

## At a Glance

- **What it does**: Automatically sorts files into folders by their extension (pdf/, jpg/, txt/, etc.)
- **Who it's for**: Non-technical users (web browser UI), terminal users (full-screen keyboard interface), and developers/power users (automation/cron/CI)
- **Quick start**: Recommended for most: download and double-click (no Python/Flask needed)  
  - macOS: [Mac-File-Cleanup.zip](https://github.com/StewAlexander-com/File_Cleanup/releases/download/v3.0/Mac-File-Cleanup.zip) (unzip, then double-click the `.app`)  
    ⚠️ **First run**: If you see a security warning, see [First Run Instructions (macOS)](#first-run-instructions-macos) below.
  - Windows: [Win-File-Cleanup.exe](https://github.com/StewAlexander-com/File_Cleanup/releases/download/v3.0/Win-File-Cleanup.exe)  
  - CLI (web UI):  
    `python3 Easy-File-Cleanup.py --html`  # needs Flask installed  
  - CLI (organize a folder):  
    `python3 Easy-File-Cleanup.py ~/Downloads`

## Table of Contents

- [Easy File Cleanup](#easy-file-cleanup)
  - [At a Glance](#at-a-glance)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Quick Start](#quick-start)
    - [Web Interface (CLI)](#web-interface-cli)
    - [Terminal Interface (TUI)](#terminal-interface-tui)
    - [Command Line (Automation)](#command-line-automation)
  - [Desktop Apps (PyInstaller)](#desktop-apps-pyinstaller)
    - [First Run Instructions (macOS)](#first-run-instructions-macos)
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

chmod +x Easy-File-Cleanup.py

# Only needed for CLI --html; desktop apps already bundle Flask
pip install Flask
```

## Quick Start

Fastest path: download the desktop app for your OS (no Python/Flask needed):
- macOS: [Mac-File-Cleanup.zip](https://github.com/StewAlexander-com/File_Cleanup/releases/download/v3.0/Mac-File-Cleanup.zip) — unzip, then double-click `Mac File Cleanup.app`  
  ⚠️ **First run**: If you see a security warning, see [First Run Instructions (macOS)](#first-run-instructions-macos) below.
- Windows: [Win-File-Cleanup.exe](https://github.com/StewAlexander-com/File_Cleanup/releases/download/v3.0/Win-File-Cleanup.exe) — double-click to run

Prefer the CLI instead? Use the commands below.

### Web Interface (CLI)
Runs in your browser with a visual directory tree. Requires Flask to be installed:
```bash
pip install Flask
python3 Easy-File-Cleanup.py --html
```
Opens in your browser automatically. See [Web Interface Guide](docs/web.md) for details, features, and troubleshooting.

### Terminal Interface (TUI)
For terminal users who like keyboard navigation and a full-screen text UI.
```bash
# Launch the TUI and start in your Downloads folder
python3 Easy-File-Cleanup.py --tui ~/Downloads
```
This opens a full-screen terminal browser. See [TUI Guide](docs/tui.md) for keyboard shortcuts and navigation.

### Command Line (Automation)
For scripts, cron jobs, and power users who want non-interactive runs.
```bash
python3 Easy-File-Cleanup.py ~/Downloads --yes --quiet
```
Fully automated, no prompts. See [Automation Guide](#automation--scripting) below or [example script](examples/automation.sh).

## Desktop Apps (PyInstaller)

**Standalone apps with Python and Flask bundled — no installation required.**

Prefer double-click over the command line? Build or download a small desktop launcher for the web UI. The CLI/TUI stay exactly the same.

- **Download ready-to-run apps (no Python needed)**:
  - macOS: [Mac-File-Cleanup.zip](https://github.com/StewAlexander-com/File_Cleanup/releases/download/v3.0/Mac-File-Cleanup.zip) (contains `Mac File Cleanup.app` — unzip first, then double-click the `.app`)
  - Windows: [Win-File-Cleanup.exe](https://github.com/StewAlexander-com/File_Cleanup/releases/download/v3.0/Win-File-Cleanup.exe)
  - Source zip: [EasyFileCleanup-3.0-source.zip](https://github.com/StewAlexander-com/File_Cleanup/releases/download/v3.0/EasyFileCleanup-3.0-source.zip)
- **First run (macOS)**: See [First Run Instructions (macOS)](#first-run-instructions-macos) below for step-by-step instructions.
- **Run**: Double-click; the web UI opens on `http://127.0.0.1:<port>` and your default browser opens automatically.
- **Dependencies**: Python and Flask are already bundled in the apps; CLI `--html` still needs `pip install Flask`.
- **Security**: Localhost-only; the app never exposes your files over the network or internet.
- **Build yourself (optional)**:
  - Requirements: Python 3.x, Flask (`pip install Flask`), PyInstaller (`pip install pyinstaller`)
  - macOS: `./scripts/build_gui_mac.sh`
  - Windows (via GitHub Actions): `gh workflow run build-windows.yml` then download the artifact
  - Windows (native): `powershell -ExecutionPolicy Bypass -File scripts/build_gui_windows.ps1`

### First Run Instructions (macOS)

If you see a security warning when trying to open `Mac File Cleanup.app`, macOS is blocking the unsigned app.

**Quick summary**: Download and unzip the app, try to open it (you'll see a warning), then go to **System Settings → Privacy & Security** and click **"Open Anyway"** next to the blocked app message. Confirm in the popup, then you can run the app normally.

For detailed step-by-step instructions with screenshots and alternative methods, see the [macOS First Run Guide](docs/macos-first-run.md).

## Features

### Core Functionality
- Automatic file organization by extension
- Duplicate handling (interactive or automatic) — prompts you to overwrite, create copies, or keep both versions
- Verification of organization — checks moves and logs actions
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
4. Files without extensions go to `no_extension/` folder
5. Handles duplicates (prompts or auto-creates copies)
6. Verifies organization
7. Creates/updates `organization_log.txt`

**Example output structure**:
```text
Downloads/
├── pdf/
│   ├── document1.pdf
│   └── report.pdf
├── jpg/
│   └── photo.jpg
├── no_extension/
│   └── README
└── organization_log.txt
```

## Usage

### Basic Command Line

```bash
# Organize specific directory (full path)
python3 Easy-File-Cleanup.py /Users/name/Downloads

# Use home shortcut
python3 Easy-File-Cleanup.py ~/Downloads

# Use partial path matching (searches current directory and home)
python3 Easy-File-Cleanup.py Downloads

# Organize the current directory
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
| `--yes` / `--non-interactive` | Auto-create copies for duplicates (recommended for scripts) |
| `--overwrite` | Auto-overwrite duplicates (⚠️ use only if you're certain) |
| `--quiet` | Minimal output (for automation and cron jobs) |
| `--help` | Show full help |

## Automation & Scripting

Fully automatable for cron jobs, CI/CD, and scripts.

**Basic automation**:
```bash
python3 Easy-File-Cleanup.py ~/Downloads --yes --quiet
```

**Cron example** (Linux/macOS only):
```bash
# Runs daily at 2 AM
0 2 * * * /usr/bin/python3 /path/to/Easy-File-Cleanup.py ~/Downloads --yes --quiet
```

**Exit codes** (suitable for CI/CD pipelines and monitoring tools):
- `0`: Success
- `1`: Error (invalid directory, organization failed)
- `2`: Invalid arguments
- `130`: Interrupted (Ctrl+C)

See [examples/automation.sh](examples/automation.sh) for a complete automation script example.

**Automation features**:
- No interactive prompts with `--yes`/`--non-interactive`/`--overwrite`
- Silent operation with `--quiet` (errors to stderr)
- Fast failure on invalid inputs
- Flag validation prevents conflicts: automation flags (`--yes`, `--non-interactive`, `--overwrite`, `--quiet`) cannot be combined with interactive flags (`--html`, `--tui`)

## Testing

Run the test suite:
```bash
python3 test_file_cleanup.py
```

All tests run locally without network access — safe to run on any machine. ✅  
**Test coverage**: 9 core tests + 18 web interface tests. All tests pass ✅

For detailed testing information, see [TEST_PLAN.md](TEST_PLAN.md).

## Documentation

**New users**: Start with the Web Interface Guide. Terminal users should check the TUI Guide.

**User Guides** (start here):
- [Web Interface Guide](docs/web.md) - Detailed web UI documentation, features, and troubleshooting
- [TUI Guide](docs/tui.md) - Terminal interface navigation, keyboard shortcuts, and usage
- [macOS First Run Guide](docs/macos-first-run.md) - Step-by-step instructions for allowing the Mac app to run

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

MIT License — free to use and modify. See [LICENSE](LICENSE) for full terms.

## Contact

- **GitHub**: [@StewAlexander-com](https://github.com/StewAlexander-com)
- **Repository**: [File_Cleanup](https://github.com/StewAlexander-com/File_Cleanup)
- **Issues**: Open an issue on GitHub (support is best-effort in spare time)

---

**Version**: 3.0 | **Last Updated**: December 2025
