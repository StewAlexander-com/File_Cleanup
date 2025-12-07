# Contributing to Easy File Cleanup

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

**Navigation**: [← Back to README](README.md) | [Test Plan](TEST_PLAN.md) | [CHANGELOG](CHANGELOG.md)

## How to Contribute

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

## Areas for Contribution

- Additional file type recognition and categorization
- Configuration file support for custom organization rules
- Performance optimizations for large directories
- Additional logging and reporting features
- Additional test cases and edge case coverage
- Documentation improvements
- UI/UX improvements for web interface and TUI

## Code Style

- Follow PEP 8 Python style guidelines
- Include docstrings for all functions
- Add comments for complex logic
- Maintain backward compatibility when possible
- Write tests for new features

## Testing

All contributions should include appropriate tests. Run the test suite before submitting:

```bash
python3 test_file_cleanup.py
python3 test_web_interface.py  # If Flask is installed
```

## Documentation

- Update README.md for user-facing changes
- Add docstrings for new functions
- Update CHANGELOG.md for significant changes
- Keep examples up to date

## Questions?

Open an issue on GitHub for questions, bug reports, or feature requests.

---

**Related Documentation**:
- [README](README.md) - Main documentation and project overview
- [Test Plan](TEST_PLAN.md) - Testing strategy and guidelines
- [CHANGELOG](CHANGELOG.md) - Version history
- [Web Interface Guide](docs/web.md) - Web UI documentation
- [TUI Guide](docs/tui.md) - Terminal interface documentation

