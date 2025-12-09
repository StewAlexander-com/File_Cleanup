<# 
Build a double-clickable Windows app for the web UI using PyInstaller.
This does not change the CLI/TUI experience. Output: dist/EasyFileCleanupGUI.exe
#>

param(
    [string]$Name = "EasyFileCleanupGUI"
)

$ErrorActionPreference = "Stop"

# Move to repo root
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$Root = Resolve-Path (Join-Path $ScriptDir "..")
Set-Location $Root

if (-not (Get-Command pyinstaller -ErrorAction SilentlyContinue)) {
    Write-Error "PyInstaller is not installed. Install with: pip install pyinstaller"
}

pyinstaller `
  --onefile `
  --windowed `
  --name "$Name" `
  --add-data "templates;templates" `
  gui_launcher.py

Write-Output ""
Write-Output "Build complete."
Write-Output "Launch via: dist\\$Name.exe"
Write-Output "(double-clickable app that starts the web UI on localhost)"

