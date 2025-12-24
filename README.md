# Easy File Cleanup

> **⚠️ Important Security Notice (Version 4.0)**: The pre-built Windows `.exe` file has been removed due to false positive security warnings from Windows 11 and Sentinel One. These warnings occur because the executable is unsigned (not code-signed with a certificate), not because the software is malicious. Unsigned executables from unknown publishers often trigger security alerts, but the code itself is open-source and safe. Windows users should build the executable from source (see [Building Windows Releases](#building-windows-releases)) or use the CLI/TUI interfaces directly with Python to avoid these warnings entirely.

Organizes files by extension into dedicated folders to quickly clean up messy directories (like Downloads) on any OS. **Files are moved only within your chosen directory, and an `organization_log.txt` tracks every change so you can review what happened.**

## Why This Tool?

- **No network access** — runs entirely locally, your files never leave your machine
- **Reversible** — complete log file tracks every move for easy review and undo
- **Automation-friendly** — works great in cron jobs and CI/CD pipelines
- **Multiple interfaces** — choose web UI, terminal UI, or command-line automation
- **Cross-platform** — works on Windows, macOS, and Linux

## Quick Start

### Option 1: Desktop App (Recommended for most users)

**macOS**: Download [Mac-File-Cleanup.zip](https://github.com/StewAlexander-com/File_Cleanup/releases/download/v4.0/Mac-File-Cleanup.zip), unzip, and double-click `Mac File Cleanup.app`
- ⚠️ **First run**: If you see a security warning, see [First Run Instructions (macOS)](#first-run-instructions-macos) below

**Windows**: Unfortunately, we're unable to provide pre-built Windows executables at this time due to false positive security warnings from unsigned binaries. You can either build from source (see [Building Windows Releases](#building-windows-releases)) for a signed executable, or run the Python script directly.

On Windows with Python installed, you can launch the web interface directly:
```powershell
pip install Flask
python Easy-File-Cleanup.py --html
```

### Option 2: Command Line

**Web Interface** (requires Flask):
```bash
pip install Flask
python3 Easy-File-Cleanup.py --html
```

**Terminal Interface**:
```bash
python3 Easy-File-Cleanup.py --tui ~/Downloads
```

**Direct Organization**:
```bash
python3 Easy-File-Cleanup.py ~/Downloads
```

## Installation

Only needed if using the command-line interface. Desktop apps bundle everything.

**Requirements**: Python 3.6+

### macOS/Linux

```bash
git clone https://github.com/StewAlexander-com/File_Cleanup.git
cd File_Cleanup
chmod +x Easy-File-Cleanup.py
pip install Flask  # Only needed for --html flag
```

### Windows

```powershell
git clone https://github.com/StewAlexander-com/File_Cleanup.git
cd File_Cleanup
pip install Flask  # Only needed for --html flag
```

**Note**: On Windows, you may need to use `python` instead of `python3` and `pip` instead of `pip3`. If you encounter issues, try `py -m pip install Flask` or `python -m pip install Flask`.

## Desktop Apps

Standalone apps with Python and Flask bundled — no installation required. Double-click to launch the web UI.

### Download

- **macOS**: [Mac-File-Cleanup.zip](https://github.com/StewAlexander-com/File_Cleanup/releases/download/v4.0/Mac-File-Cleanup.zip) (Universal app for Intel + Apple Silicon)
- **Windows**: Not available at this time (due to unsigned binary warnings — see [Building Windows Releases](#building-windows-releases) to build from source)
- **Source**: [EasyFileCleanup-4.0-source.zip](https://github.com/StewAlexander-com/File_Cleanup/releases/download/v4.0/EasyFileCleanup-4.0-source.zip)

### Building Windows Releases

**⚠️ Important**: Due to Windows 11 security restrictions and Sentinel One false positives, pre-built Windows executables are not provided.

**Option 1: Build Locally (Recommended)**

1. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   pip install pyinstaller
   ```

2. Build the executable:
   ```powershell
   powershell -ExecutionPolicy Bypass -File scripts/build_gui_windows.ps1
   ```

3. **Code Signing (Strongly Recommended)**: To prevent Windows Defender and security software from flagging the executable:
   - Obtain a code signing certificate (Extended Validation recommended)
   - Sign the executable:
     ```powershell
     signtool sign /f "path\to\certificate.pfx" /p "password" /t "http://timestamp.digicert.com" /fd sha256 "dist\Win-File-Cleanup.exe"
     ```
   - See [Microsoft's Code Signing Guide](https://learn.microsoft.com/en-us/windows/win32/win_cert/sign) for details

4. **Alternative**: Use Python directly to avoid all security issues (requires Flask installed — see [Option 2: Command Line](#option-2-command-line) above for details):
   ```powershell
   python Easy-File-Cleanup.py --html
   ```

**Option 2: GitHub Actions Build**

1. Run: `gh workflow run build-windows.yml`
2. Download the artifact from the Actions tab
3. **Note**: Code signing is still required to avoid security warnings

**Resources**:
- [PyInstaller Windows Guide](https://pyinstaller.org/en/stable/when-things-go-wrong.html#code-signing-on-windows)
- [Microsoft Code Signing Documentation](https://learn.microsoft.com/en-us/windows/win32/win_cert/sign)
- [Windows Defender False Positives](https://learn.microsoft.com/en-us/microsoft-365/security/intelligence/false-positives-negatives)

### First Run Instructions (macOS)

If you see a security warning when opening `Mac File Cleanup.app`, macOS is blocking the unsigned app.

**Quick fix**: Download and unzip the app, try to open it (you'll see a warning), then go to **System Settings → Privacy & Security** and click **"Open Anyway"** next to the blocked app message. Confirm in the popup.

**Note for Intel Mac users**: If the app won't open after following security steps, you may have an older build. See the [macOS First Run Guide](docs/macos-first-run.md) for troubleshooting.

For detailed step-by-step instructions with screenshots, see the [macOS First Run Guide](docs/macos-first-run.md).

## Usage

### Command Line Options

| Flag | Description |
|------|-------------|
| `--html` | Launch web interface (requires Flask) |
| `--tui` | Launch terminal interface |
| `--yes` / `--non-interactive` | Auto-create copies for duplicates (recommended for scripts) |
| `--overwrite` | Auto-overwrite duplicates (⚠️ use only if you're certain) |
| `--quiet` | Minimal output (for automation and cron jobs) |
| `--help` | Show full help |

### Examples

```bash
# Organize specific directory
python3 Easy-File-Cleanup.py ~/Downloads

# Use partial path matching
python3 Easy-File-Cleanup.py Downloads

# Organize current directory
python3 Easy-File-Cleanup.py .

# Interactive mode (guided selection)
python3 Easy-File-Cleanup.py

# Automated (no prompts)
python3 Easy-File-Cleanup.py ~/Downloads --yes --quiet
```

## How It Works

1. Scans directory for files (ignores hidden files)
2. Creates folders by extension (pdf/, jpg/, txt/, etc.)
3. Moves files into matching folders
4. Files without extensions go to `no_extension/` folder
5. Handles duplicates (prompts or auto-creates copies)
6. Verifies organization
7. Creates/updates `organization_log.txt`

**Example output**:
```
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

## Features

- **Multiple Interfaces**: Web UI (point-and-click), TUI (keyboard navigation), CLI (automation)
- **Duplicate Handling**: Interactive prompts or automatic copy creation
- **Verification**: Checks moves and logs all actions
- **Automation Ready**: Non-interactive flags, consistent exit codes, silent mode
- **Detailed Logging**: Complete record of all file movements in `organization_log.txt`
- **Cross-platform**: Windows, macOS, and Linux

## Automation & Scripting

Fully automatable for cron jobs, CI/CD, and scripts.

**Basic automation**:
```bash
python3 Easy-File-Cleanup.py ~/Downloads --yes --quiet
```

**Cron example** (Linux/macOS):
```bash
# Runs daily at 2 AM
0 2 * * * /usr/bin/python3 /path/to/Easy-File-Cleanup.py ~/Downloads --yes --quiet
```

**Exit codes**:
- `0`: Success
- `1`: Error (invalid directory, organization failed)
- `2`: Invalid arguments
- `130`: Interrupted (Ctrl+C)

**Automation features**:
- No interactive prompts with `--yes`/`--non-interactive`/`--overwrite`
- Silent operation with `--quiet` (errors to stderr)
- Fast failure on invalid inputs
- Flag validation prevents conflicts: automation flags cannot be combined with interactive flags (`--html`, `--tui`)

See [examples/automation.sh](examples/automation.sh) for a complete automation script example.

## Testing

```bash
python3 test_file_cleanup.py
```

All tests run locally without network access. ✅  
**Test coverage**: 9 core tests + 18 web interface tests. All tests pass ✅

For detailed testing information, see [TEST_PLAN.md](TEST_PLAN.md).

## Documentation

**User Guides**:
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

**Version**: 4.0 | **Last Updated**: December 2025
