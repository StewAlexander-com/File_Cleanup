#!/usr/bin/env python3
"""
Flask Web Interface for File Cleanup

This module provides a web-based GUI for the file cleanup application.
It includes a directory browser, file organization interface, cleanup history
tracking, and server management controls.

Features:
    - Directory browsing and navigation
    - File organization by extension
    - Cleanup history visualization with graphs
    - Directory structure tree view
    - Log viewing
    - Server control (stop/restart)
    - Automatic port conflict detection
    - Localhost-only security binding

Security:
    - Server always binds to 127.0.0.1 (localhost) only
    - No external network access allowed
    - Secure headers for browser compatibility

Dependencies:
    - Flask: Web framework
    - file_cleanup: Core file organization module
"""

import os
import sys
import json
import threading
import hashlib
import time
import signal
import socket
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from functools import wraps

# Check for Flask dependency
try:
    from flask import Flask, render_template, jsonify, request
except ImportError:
    raise ImportError(
        "Flask is required for the web interface. "
        "Please install it with: pip install Flask"
    )

from file_cleanup import (
    organize_files,
    verify_organization,
    create_log,
    find_directory_by_partial_path
)


def get_base_dir() -> Path:
    """
    Resolve the base directory for locating bundled assets (templates).

    When packaged with PyInstaller, files are extracted to a temporary
    directory available via sys._MEIPASS. In normal execution, this falls
    back to the directory containing this file.
    """
    if hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS)  # PyInstaller extraction dir
    return Path(__file__).parent


# Template directory works for both source and PyInstaller bundles
BASE_DIR = get_base_dir()
TEMPLATE_DIR = BASE_DIR / "templates"
app = Flask(__name__, template_folder=str(TEMPLATE_DIR))
app.config['SECRET_KEY'] = os.urandom(24)

# Add headers to prevent browser security issues
@app.after_request
def after_request(response):
    """
    Add security headers to all responses.
    
    This function is called after each request to add security headers
    that prevent common browser security issues while maintaining
    localhost accessibility.
    
    Args:
        response: Flask response object to modify
    
    Returns:
        Flask response object with security headers added
    """
    # Allow localhost access
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    # Don't add restrictive headers that might block localhost
    return response

# Store cleanup results in memory (in production, use a database or file)
cleanup_results = {}
cleanup_history = []  # Track cleanup history over time
cleanup_lock = threading.Lock()

# Server control
shutdown_event = threading.Event()
restart_signal_file = Path.home() / '.file_cleanup_restart_signal'
current_server_port = 5000  # Track actual port being used


@app.route('/')
def index():
    """
    Render the main web interface page.
    
    Returns:
        HTML response: Rendered index.html template, or error page if template
        loading fails.
    
    Status Codes:
        200: Success
        500: Template rendering error
    """
    try:
        return render_template('index.html')
    except Exception as e:
        # If template rendering fails, return a simple error page
        return f"""
        <html>
        <head><title>File Cleanup - Error</title></head>
        <body>
            <h1>Template Error</h1>
            <p>Error loading template: {str(e)}</p>
            <p>Please check that templates/index.html exists.</p>
        </body>
        </html>
        """, 500


@app.route('/api/directory')
def get_directory():
    """
    Get directory listing with files and subdirectories.
    
    Query Parameters:
        path (str, optional): Directory path to list. Defaults to home directory
            if not provided. Can be absolute or relative path.
    
    Returns:
        JSON response containing:
            - current_path (str): Full path of current directory
            - parent_path (str): Path of parent directory, or None if root
            - directories (list): List of subdirectories with name and path
            - files (list): List of files with name, path, and size
            - breadcrumbs (list): Navigation breadcrumb trail
    
    Status Codes:
        200: Success
        400: Invalid directory path
        403: Permission denied
        500: Server error
    """
    path_str = request.args.get('path', '')
    
    if not path_str:
        # Default to home directory
        current_path = Path.home()
    else:
        try:
            current_path = Path(path_str).expanduser().resolve()
            if not current_path.exists() or not current_path.is_dir():
                return jsonify({'error': 'Invalid directory path'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    try:
        items = sorted(current_path.iterdir())
        directories = []
        files = []
        
        for item in items:
            try:
                if item.is_dir() and not item.name.startswith('.'):
                    directories.append({
                        'name': item.name,
                        'path': str(item),
                        'type': 'directory'
                    })
                elif item.is_file():
                    files.append({
                        'name': item.name,
                        'path': str(item),
                        'type': 'file',
                        'size': item.stat().st_size
                    })
            except (PermissionError, OSError):
                continue
        
        # Get breadcrumbs
        breadcrumbs = []
        path = current_path
        while path != path.parent:
            breadcrumbs.insert(0, {
                'name': path.name if path.name else '/',
                'path': str(path)
            })
            path = path.parent
        breadcrumbs.insert(0, {'name': '/', 'path': str(path)})
        
        return jsonify({
            'current_path': str(current_path),
            'parent_path': str(current_path.parent) if current_path.parent != current_path else None,
            'directories': directories,
            'files': files,
            'breadcrumbs': breadcrumbs
        })
    except PermissionError:
        return jsonify({'error': 'Permission denied'}), 403
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/logs')
def get_logs():
    """
    Get organization log file content for a directory.
    
    Query Parameters:
        path (str, required): Directory path to get logs for
    
    Returns:
        JSON response containing:
            - exists (bool): Whether log file exists
            - content (str): Log file content, or message if not found
            - path (str): Full path to log file
    
    Status Codes:
        200: Success
        400: Path not provided
        500: Server error
    """
    path_str = request.args.get('path', '')
    
    if not path_str:
        return jsonify({'error': 'Path required'}), 400
    
    try:
        directory = Path(path_str).expanduser().resolve()
        log_path = directory / "organization_log.txt"
        
        if log_path.exists():
            with open(log_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return jsonify({
                'exists': True,
                'content': content,
                'path': str(log_path)
            })
        else:
            return jsonify({
                'exists': False,
                'content': 'No log file found for this directory.',
                'path': str(log_path)
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/cleanup', methods=['POST'])
def run_cleanup():
    """
    Execute file cleanup operation on a directory.
    
    Request Body (JSON):
        path (str, required): Directory path to organize
        non_interactive (bool, optional): Auto-create copies for duplicates.
            Defaults to True.
        overwrite (bool, optional): Overwrite duplicate files. Defaults to False.
            Note: overwrite takes precedence over non_interactive.
    
    Returns:
        JSON response containing:
            - success (bool): Whether operation succeeded
            - result_id (str): Unique identifier for this cleanup result
            - directory (str): Path of organized directory
            - moved_files (dict): Files moved, grouped by extension folder
            - folder_status (dict): Whether each folder was NEW or EXISTING
            - is_organized (bool): Verification result
            - file_count (int): Total number of files organized
            - timestamp (str): ISO format timestamp of operation
    
    Status Codes:
        200: Success
        400: Invalid path or missing required parameters
        500: Server error during cleanup
    """
    data = request.json
    path_str = data.get('path', '')
    non_interactive = data.get('non_interactive', True)
    overwrite = data.get('overwrite', False)
    
    if not path_str:
        return jsonify({'error': 'Path required'}), 400
    
    try:
        directory = Path(path_str).expanduser().resolve()
        if not directory.exists() or not directory.is_dir():
            return jsonify({'error': 'Invalid directory path'}), 400
        
        # Run cleanup in a thread-safe manner
        with cleanup_lock:
            # Organize files
            moved_files, folder_status = organize_files(
                directory,
                non_interactive=non_interactive,
                overwrite=overwrite
            )
            
            # Verify organization
            is_organized = verify_organization(directory, quiet=True)
            
            # Create log
            create_log(directory, moved_files, folder_status, quiet=True)
            
            # Convert defaultdict to regular dict for JSON serialization
            moved_files_dict = dict(moved_files)
            folder_status_dict = dict(folder_status)
            file_count = sum(len(files) for files in moved_files_dict.values())
            timestamp = datetime.now().isoformat()
            
            # Store results
            result_id = f"{directory}_{os.urandom(4).hex()}"
            cleanup_results[result_id] = {
                'directory': str(directory),
                'moved_files': moved_files_dict,
                'folder_status': folder_status_dict,
                'is_organized': is_organized,
                'file_count': file_count,
                'timestamp': timestamp
            }
            
            # Add to history
            cleanup_history.append({
                'timestamp': timestamp,
                'directory': str(directory),
                'file_count': file_count,
                'folder_count': len(moved_files_dict),
                'is_organized': is_organized
            })
            
            return jsonify({
                'success': True,
                'result_id': result_id,
                'directory': str(directory),
                'moved_files': moved_files_dict,
                'folder_status': folder_status_dict,
                'is_organized': is_organized,
                'file_count': file_count,
                'timestamp': timestamp
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/cleanup-result/<result_id>')
def get_cleanup_result(result_id):
    """
    Retrieve a previously stored cleanup result by its ID.
    
    URL Parameters:
        result_id (str): Unique identifier for the cleanup result
    
    Returns:
        JSON response containing the cleanup result data, or error if not found.
    
    Status Codes:
        200: Success
        404: Result not found
    """
    if result_id in cleanup_results:
        return jsonify(cleanup_results[result_id])
    else:
        return jsonify({'error': 'Result not found'}), 404


@app.route('/api/cleanup-history')
def get_cleanup_history():
    """
    Get cleanup operation history for graph visualization.
    
    Returns:
        JSON response containing:
            - history (list): List of cleanup operations with timestamps,
              file counts, folder counts, and organization status
            - total_operations (int): Total number of cleanup operations
    
    Status Codes:
        200: Success
    """
    return jsonify({
        'history': cleanup_history,
        'total_operations': len(cleanup_history)
    })


@app.route('/api/server/status')
def get_server_status():
    """
    Get current server status and configuration.
    
    Returns:
        JSON response containing:
            - status (str): Server status ('running')
            - host (str): Server host address (always '127.0.0.1')
            - port (int): Port number server is listening on
            - security (str): Security mode ('localhost-only')
    
    Status Codes:
        200: Success
    """
    global current_server_port
    return jsonify({
        'status': 'running',
        'host': '127.0.0.1',  # Always localhost for security
        'port': current_server_port,
        'security': 'localhost-only'
    })


@app.route('/api/server/stop', methods=['POST'])
def stop_server():
    """
    Gracefully stop the Flask server.
    
    This endpoint initiates a graceful shutdown of the server. The response
    is sent immediately, then the server stops after a short delay to ensure
    the response reaches the client.
    
    Returns:
        JSON response containing:
            - success (bool): Whether stop signal was sent
            - message (str): Status message
            - note (str): Additional information about manual restart
    
    Status Codes:
        200: Stop signal sent successfully
    
    Note:
        After calling this endpoint, the server will stop and the web interface
        will become unavailable. The server must be restarted manually.
    """
    def shutdown():
        # Give time for response to be sent to client
        time.sleep(2)
        # Use os._exit for immediate termination after response is sent
        os._exit(0)
    
    # Start shutdown in a separate thread
    shutdown_thread = threading.Thread(target=shutdown, daemon=False)
    shutdown_thread.start()
    
    # Return response immediately
    response = jsonify({
        'success': True,
        'message': 'Server shutting down...',
        'note': 'The server will stop in a few seconds. You may need to restart it manually.'
    })
    return response


@app.route('/api/server/restart', methods=['POST'])
def restart_server():
    """
    Signal server restart by creating a restart signal file.
    
    This endpoint creates a signal file that can be detected by process
    managers or wrapper scripts. The server stops after sending the response,
    and must be restarted manually.
    
    Returns:
        JSON response containing:
            - success (bool): Whether restart signal was sent
            - message (str): Status message
            - note (str): Instructions for manual restart
            - restart_command (str): Command to restart the server
    
    Status Codes:
        200: Restart signal sent successfully
        500: Error creating restart signal
    
    Note:
        The server will stop after sending the response. Use the provided
        restart_command to start the server again.
    """
    try:
        # Create restart signal file
        restart_signal_file.touch()
        restart_signal_file.write_text(str(time.time()))
        
        def shutdown_and_restart():
            # Give time for response to be sent to client
            time.sleep(2)
            # Use os._exit for immediate termination after response is sent
            os._exit(0)
        
        # Start shutdown in a separate thread
        shutdown_thread = threading.Thread(target=shutdown_and_restart, daemon=False)
        shutdown_thread.start()
        
        # Return response immediately
        response = jsonify({
            'success': True,
            'message': 'Server restart signal sent...',
            'note': 'The server will stop in a few seconds. Please restart it manually using: python3 Easy-File-Cleanup.py --html',
            'restart_command': 'python3 Easy-File-Cleanup.py --html'
        })
        return response
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/directory-state')
def get_directory_state():
    """
    Get directory state hash for lightweight change detection.
    
    This endpoint provides a lightweight way to detect if a directory has
    changed by returning a hash based on file counts, directory counts, and
    modification times. Used by the polling system to detect changes.
    
    Query Parameters:
        path (str, required): Directory path to check
    
    Returns:
        JSON response containing:
            - path (str): Directory path that was checked
            - hash (str): MD5 hash of directory state
            - file_count (int): Number of files in directory
            - dir_count (int): Number of subdirectories
            - timestamp (float): Unix timestamp of check
    
    Status Codes:
        200: Success
        400: Invalid path or path not provided
        500: Server error
    """
    path_str = request.args.get('path', '')
    
    if not path_str:
        return jsonify({'error': 'Path required'}), 400
    
    try:
        directory = Path(path_str).expanduser().resolve()
        if not directory.exists() or not directory.is_dir():
            return jsonify({'error': 'Invalid directory path'}), 400
        
        # Create a lightweight hash of directory state
        # Uses modification times and file counts for efficiency
        state_parts = []
        file_count = 0
        dir_count = 0
        max_mtime = 0
        
        try:
            for item in directory.iterdir():
                try:
                    stat = item.stat()
                    mtime = stat.st_mtime
                    max_mtime = max(max_mtime, mtime)
                    
                    if item.is_dir() and not item.name.startswith('.'):
                        dir_count += 1
                    elif item.is_file():
                        file_count += 1
                except (PermissionError, OSError):
                    continue
        except (PermissionError, OSError):
            pass
        
        # Create hash from state information
        state_string = f"{dir_count}:{file_count}:{max_mtime}"
        state_hash = hashlib.md5(state_string.encode()).hexdigest()
        
        return jsonify({
            'path': str(directory),
            'hash': state_hash,
            'file_count': file_count,
            'dir_count': dir_count,
            'timestamp': time.time()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/directory-structure')
def get_directory_structure():
    """
    Get hierarchical directory structure tree.
    
    Returns a tree representation of the directory structure, useful for
    displaying the organized file structure after cleanup operations.
    
    Query Parameters:
        path (str, required): Directory path to build tree for
    
    Returns:
        JSON response containing:
            - structure (dict): Tree structure with directories and files
            - directory (str): Root directory path
    
    Status Codes:
        200: Success
        400: Invalid path or path not provided
        500: Server error
    
    Note:
        Tree depth is limited to 3 levels to prevent excessive data transfer.
    """
    path_str = request.args.get('path', '')
    
    if not path_str:
        return jsonify({'error': 'Path required'}), 400
    
    try:
        directory = Path(path_str).expanduser().resolve()
        if not directory.exists() or not directory.is_dir():
            return jsonify({'error': 'Invalid directory path'}), 400
        
        def build_tree(path, max_depth=3, current_depth=0):
            """Recursively build directory tree structure."""
            if current_depth >= max_depth:
                return None
            
            try:
                items = sorted(path.iterdir())
                structure = {
                    'name': path.name if path.name else '/',
                    'path': str(path),
                    'type': 'directory',
                    'children': []
                }
                
                for item in items:
                    try:
                        if item.is_dir() and not item.name.startswith('.'):
                            child = build_tree(item, max_depth, current_depth + 1)
                            if child:
                                structure['children'].append(child)
                        elif item.is_file() and not item.name.startswith('.'):
                            structure['children'].append({
                                'name': item.name,
                                'path': str(item),
                                'type': 'file',
                                'size': item.stat().st_size
                            })
                    except (PermissionError, OSError):
                        continue
                
                return structure
            except (PermissionError, OSError):
                return None
        
        tree = build_tree(directory)
        
        return jsonify({
            'structure': tree,
            'directory': str(directory)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def is_port_available(host, port):
    """
    Check if a port is available for binding.
    
    This function checks both if something is already listening on the port
    and if we can successfully bind to it. This ensures accurate port
    availability detection.
    
    Args:
        host (str): Host address to check (typically '127.0.0.1')
        port (int): Port number to check
    
    Returns:
        bool: True if port is available, False if in use or cannot bind
    """
    # First, try to connect to see if something is already listening
    try:
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.settimeout(0.1)
        result = test_socket.connect_ex((host, port))
        test_socket.close()
        if result == 0:
            # Port is already in use (something is listening)
            return False
    except Exception:
        pass
    
    # Then try to bind to the port
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            s.listen(1)
            return True
    except (OSError, socket.error) as e:
        # Port is in use
        return False


def find_available_port(host, start_port=5001, max_attempts=20):
    """
    Find an available port starting from a given port number.
    
    Searches sequentially through ports starting from start_port until
    an available port is found or max_attempts is reached.
    
    Args:
        host (str): Host address to check ports on (typically '127.0.0.1')
        start_port (int, optional): First port to try. Defaults to 5001.
        max_attempts (int, optional): Maximum number of ports to try.
            Defaults to 20.
    
    Returns:
        int or None: Available port number if found, None if no available
            port found within max_attempts
    """
    for i in range(max_attempts):
        port = start_port + i
        if is_port_available(host, port):
            return port
    return None


def run_server(host='127.0.0.1', port=5000, debug=False):
    """
    Run the Flask development server with automatic port conflict detection.
    
    This function starts the Flask web server with the following features:
    - Automatic port conflict detection and resolution
    - Localhost-only binding for security
    - Automatic browser opening
    - Clear startup messages with access instructions
    
    Args:
        host (str, optional): Host address to bind to. Defaults to '127.0.0.1'.
            Note: For security, this is always forced to '127.0.0.1' regardless
            of input value.
        port (int, optional): Port number to use. Defaults to 5000. If this
            port is in use, an available port will be automatically selected.
        debug (bool, optional): Enable Flask debug mode. Defaults to False.
    
    Security:
        The server always binds to 127.0.0.1 (localhost) only, preventing
        external network access. This ensures the server is only accessible
        from the same machine.
    
    Port Handling:
        If the requested port is in use (e.g., by macOS AirPlay Receiver on
        port 5000), the function will automatically find and use an available
        port, starting from port + 1.
    
    Browser:
        Attempts to automatically open the web interface in the default
        browser after a short delay to ensure the server is ready.
    
    Exits:
        sys.exit(1): If no available port can be found
        sys.exit(1): If server binding fails
        Normal exit: On KeyboardInterrupt (Ctrl+C) or other exceptions
    
    Note:
        This is a development server. For production use, deploy with a
        proper WSGI server like Gunicorn or uWSGI.
    """
    # Security: Force localhost-only binding
    if host != '127.0.0.1' and host != 'localhost':
        print(f"⚠️  Security: Forcing host to 127.0.0.1 (was: {host})")
        host = '127.0.0.1'
    
    # Check if requested port is available, find alternative if not
    original_port = port
    print(f"🔍 Checking if port {port} is available...")
    if not is_port_available(host, port):
        print(f"⚠️  Port {port} is already in use (likely by macOS AirPlay Receiver).")
        print(f"    Searching for available port...")
        available_port = find_available_port(host, port + 1, max_attempts=20)  # Start from 5001
        if available_port:
            port = available_port
            print(f"✓ Found available port: {port}")
        else:
            print(f"✗ Error: Could not find an available port starting from {original_port + 1}")
            print(f"  Please stop other services using ports {original_port + 1}-{original_port + 20}")
            sys.exit(1)
    else:
        print(f"✓ Port {port} is available")
    
    # Store the actual port being used
    global current_server_port
    current_server_port = port
    
    url = f"http://{host}:{port}"
    
    print(f"\n{'=' * 70}")
    print(" " * 15 + "File Cleanup Web Interface")
    print(f"{'=' * 70}")
    print(f"\n🌐 Server starting...")
    if port != original_port:
        print(f"⚠️  Note: Using port {port} instead of {original_port} (port was in use)")
    print(f"\n{'─' * 70}")
    print(f"📍 ACCESS THE WEB INTERFACE:")
    print(f"   {url}")
    print(f"{'─' * 70}")
    print(f"\n🔒 Security: Localhost-only access (127.0.0.1)")
    print(f"   The server is only accessible from this machine.")
    print(f"\n💡 TIP: Your browser should open automatically.")
    print(f"   If not, copy and paste the URL above into your browser.")
    print(f"\n⚠️  If you see 'Access denied' errors:")
    print(f"   • Make sure no other process is using port {port}")
    print(f"   • Try: http://localhost:{port} instead of 127.0.0.1")
    print(f"   • Check browser security settings")
    print(f"\n{'─' * 70}")
    print(f"\n⌨️  CONTROLS:")
    print(f"   • Press Ctrl+C to stop the server")
    print(f"   • Use the ⚙️ Server button in the web interface for controls")
    print(f"\n{'=' * 70}\n")
    
    # Try to open browser automatically
    try:
        import webbrowser
        # Small delay to ensure server is ready
        import threading
        def open_browser():
            time.sleep(1.5)  # Wait for server to start
            webbrowser.open(url)
        
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        print("🚀 Opening browser automatically...\n")
    except Exception:
        # If browser opening fails, that's okay - user can manually navigate
        pass
    
    try:
        # Verify we can bind before starting
        print(f"✓ Binding to {host}:{port}...")
        app.run(host=host, port=port, debug=debug, threaded=True, use_reloader=False)
    except OSError as e:
        if "Address already in use" in str(e) or "address is already in use" in str(e).lower():
            print(f"\n✗ Error: Port {port} is already in use.")
            print(f"  Another process is using this port.")
            print(f"\n  Solutions:")
            print(f"  1. Stop the other process using port {port}")
            print(f"  2. Kill existing Flask processes: pkill -f 'Easy-File-Cleanup.py --html'")
            print(f"  3. Use a different port (modify the code)")
        else:
            print(f"\n✗ Server binding error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Server stopped by user")
    except Exception as e:
        print(f"\n✗ Server error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

