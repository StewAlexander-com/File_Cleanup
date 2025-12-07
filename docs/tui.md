# Terminal User Interface (TUI) Guide

The TUI provides a full-screen terminal interface for directory browsing, similar to 'nnn' or 'ranger'.

**Navigation**: [← Back to README](../README.md) | [Web Interface Guide](web.md) | [Test Plan](../TEST_PLAN.md)

## Launching

```bash
# Direct launch
python3 Easy-File-Cleanup.py --tui

# Start from specific directory
python3 Easy-File-Cleanup.py --tui ~/Downloads
```

## Navigation Controls

### macOS/Linux (ncurses)

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

### Windows

On Windows, the TUI automatically falls back to a simple numbered menu interface that provides the same functionality with a different presentation.

## Features

- **Full-Screen Terminal Interface**: Beautiful ncurses-based UI (macOS/Linux)
- **Keyboard Navigation**: Fast, keyboard-driven directory browsing
- **Breadcrumb Navigation**: Quick jump to parent directories with number keys (1-9)
- **Smart Path Input**: Type paths manually while browsing
- **Quick Navigation**: Jump to home directory instantly

## Breadcrumb Shortcuts

The TUI displays breadcrumb shortcuts at the top showing which number key (1-9) corresponds to which parent directory level. This allows instant navigation to any ancestor directory without multiple "up" commands.

## Usage Flow

1. Launch TUI with `--tui` flag
2. Navigate directories with arrow keys
3. Press `s` to select a directory for cleanup
4. The script proceeds with file organization automatically

## When to Use TUI vs Web Interface

**Use TUI when**:
- Working in terminal
- Prefer keyboard navigation
- No browser needed
- Minimal dependencies

**Use Web Interface when**:
- Want visual graphs
- Prefer mouse navigation
- Need to view logs in browser
- Want to see directory tree visualization

---

**Related Documentation**:
- [README](../README.md) - Main documentation and quick start
- [Web Interface Guide](web.md) - Web-based alternative
- [Automation Guide](../README.md#automation--scripting) - For scripted usage
- [CHANGELOG](../CHANGELOG.md) - Version history

