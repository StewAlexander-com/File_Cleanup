#!/bin/bash
# Example automation script for Easy File Cleanup
# 
# This script demonstrates how to use Easy-File-Cleanup.py in automation
# scenarios such as cron jobs, scheduled tasks, or CI/CD pipelines.

# Configuration
DIRECTORY="${1:-$HOME/Downloads}"  # Use first argument or default to Downloads
SCRIPT_PATH="$(dirname "$0")/../Easy-File-Cleanup.py"
LOG_FILE="${HOME}/.file_cleanup_automation.log"

# Ensure script exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "Error: Script not found at $SCRIPT_PATH" >&2
    exit 1
fi

# Run cleanup with full automation
# --yes: Auto-create copies for duplicates (no prompts)
# --quiet: Minimal output (errors still go to stderr)
if python3 "$SCRIPT_PATH" "$DIRECTORY" --yes --quiet; then
    EXIT_CODE=$?
    echo "$(date '+%Y-%m-%d %H:%M:%S'): Cleanup successful for $DIRECTORY" >> "$LOG_FILE"
    exit 0
else
    EXIT_CODE=$?
    echo "$(date '+%Y-%m-%d %H:%M:%S'): Cleanup failed for $DIRECTORY (exit code: $EXIT_CODE)" >> "$LOG_FILE"
    exit $EXIT_CODE
fi

