# Changelog

All notable changes to this project will be documented in this file.

**Navigation**: [← Back to README](README.md) | [Web Interface](docs/web.md) | [TUI Guide](docs/tui.md) | [Test Plan](TEST_PLAN.md)

## [2.0] - December 2025

### Added
- Web GUI interface with directory browsing, cleanup operations, and visualization
- Cleanup history graph using Chart.js
- Directory tree view with expandable/collapsible folders
- Auto-refresh with intelligent polling and exponential backoff
- Server controls (stop/restart) from web interface
- Automatic port conflict detection and resolution
- Terminal User Interface (TUI) with `--tui` flag
- Comprehensive docstrings for all functions
- Web interface test suite (18 tests)
- Enhanced help flag with installation and examples
- Custom error handler for invalid flags with helpful suggestions
- Full automation support with proper exit codes

### Changed
- Improved error handling with proper stderr output in quiet mode
- Enhanced flag validation to prevent automation/interactive conflicts
- Updated documentation structure for better scannability

### Security
- Localhost-only binding enforced for web interface
- Secure headers for browser compatibility

## [1.2] - 2025

### Added
- Full scriptability with `--yes`, `--non-interactive`, `--overwrite`, and `--quiet` flags
- Enhanced CLI help with comprehensive documentation
- Automation-ready exit codes for cron jobs and scripts
- Quiet mode for automation pipelines

## [1.1] - 2025

### Added
- Command-line arguments for directory paths
- Partial path matching for directory search
- Simplified interface with smart defaults
- Refactored test suite with automatic mock file generation

### Changed
- Improved performance and user experience

---

**Related Documentation**:
- [README](README.md) - Main documentation
- [Web Interface Guide](docs/web.md) - Web UI features
- [TUI Guide](docs/tui.md) - Terminal interface
- [Contributing Guidelines](CONTRIBUTING.md) - How to contribute

