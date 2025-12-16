# macOS First Run Instructions

If you see a security warning when trying to open `Mac File Cleanup.app`, macOS is blocking the unsigned app. Follow these steps to allow it.

## Method 1: System Settings (Recommended)

1. **Download and unzip** `Mac-File-Cleanup.zip` to get `Mac File Cleanup.app`

2. **Try to open the app** by double-clicking `Mac File Cleanup.app` (you'll see a security warning)

3. **Open System Settings**:
   - Click the Apple menu (🍎) in the top-left corner
   - Select **System Settings** (or **System Preferences** on older macOS versions)

4. **Go to Privacy & Security**:
   - In the sidebar, click **Privacy & Security**
   - Scroll down to the **Security** section

5. **Click "Open Anyway"**:
   - You should see a message about `Mac File Cleanup.app` being blocked
   - Click the **"Open Anyway"** button next to the message

6. **Confirm in the popup**:
   - A popup window will appear asking you to confirm
   - Click **"Allow Anyway"** (or **"Open"** depending on your macOS version)

7. **Run the app**:
   - After confirming, you can now double-click `Mac File Cleanup.app` normally
   - The app will open and launch the web UI in your browser

**Note**: You only need to do this once. After the first run, you can double-click the app normally without any security prompts.

## Method 2: Terminal (Alternative)

If you prefer using Terminal, you can remove the quarantine attribute:

```bash
# Option 1: Navigate to the app's directory first
cd ~/Downloads  # or wherever you unzipped the app
xattr -d com.apple.quarantine "Mac File Cleanup.app"

# Option 2: Use the full path (replace ~/Downloads with your actual path)
xattr -d com.apple.quarantine "~/Downloads/Mac File Cleanup.app"
```

**Option 3** (drag and drop): Type `xattr -d com.apple.quarantine ` (with a space at the end), then drag `Mac File Cleanup.app` from Finder into Terminal, and press Enter.

## Why does this happen?

macOS Gatekeeper blocks apps that aren't signed with an Apple Developer ID certificate. Since this is an open-source tool distributed via GitHub, it's not signed. The steps above tell macOS that you trust the app and want to run it.

## Navigation

- [← Back to README](../README.md)
- [Web Interface Guide](web.md)
- [TUI Guide](tui.md)




