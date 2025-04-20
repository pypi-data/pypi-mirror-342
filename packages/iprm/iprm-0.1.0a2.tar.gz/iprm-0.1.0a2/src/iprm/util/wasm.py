def run_html_wasm_script(target: str):
    return f"""import http.server
import socketserver
import os
import sys
import webbrowser
import threading
import time
import signal
import argparse


def signal_handler(sig, frame):
    print("\\nShutting down server...")
    sys.exit(0)


def start_server(port, file_dir):
    os.chdir(file_dir)

    class MyHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            print(f"[Server] {{self.address_string()}} - {{format % args}}")

    server = None
    actual_port = port

    for attempt_port in range(port, port + 10):
        try:
            server = socketserver.TCPServer(("", attempt_port), MyHandler)
            actual_port = attempt_port
            break
        except OSError:
            print(f"Port {{attempt_port}} is in use, trying another port...")

    if server is None:
        print("Failed to find an available port. Please close some applications and try again.")
        sys.exit(1)

    print(f"Starting server at http://localhost:{{actual_port}}")
    return server, actual_port


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Run {target} in a browser with a local server')
    parser.add_argument('html_file', help='Path to the HTML file to serve')
    parser.add_argument('-p', '--port', type=int, default=8000, 
                        help='Port to use for the local server (default: 8000)')
    parser.add_argument('--no-browser', action='store_true',
                        help='Do not open a browser automatically')
    parser.add_argument('--address', default='localhost',
                        help='Address to bind the server to (default: localhost)')
    
    args = parser.parse_args()
    
    html_file = args.html_file
    port = args.port
    
    file_dir = os.path.dirname(os.path.abspath(html_file))
    file_name = os.path.basename(html_file)

    signal.signal(signal.SIGINT, signal_handler)

    server, actual_port = start_server(port, file_dir)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    import socket

    max_attempts = 10
    for attempt in range(max_attempts):
        try:
            with socket.create_connection(("localhost", actual_port), timeout=0.5):
                break
        except (socket.error, ConnectionRefusedError):
            if attempt < max_attempts - 1:
                print(f"Waiting for server to start (attempt {{attempt + 1}}/{{max_attempts}})...")
                time.sleep(0.2)
            else:
                print("Warning: Could not confirm server startup, attempting to open browser anyway.")

    url = f"http://localhost:{{actual_port}}/{{file_name}}"
    print(f"Opening {{url}} in the default browser")
    webbrowser.open(url)

    print("Server is running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\\nShutting down server...")
"""
