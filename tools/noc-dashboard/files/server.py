"""
NOC Dashboard — Local Proxy Server
Serves static files + proxies Anthropic API calls so the browser never
needs to talk to Anthropic directly (avoids CORS restrictions).

Usage:
    python server.py YOUR_API_KEY_HERE
    
Then open: http://localhost:8080/noc-dashboard-p6.html
"""

import sys
import os
import json
import urllib.request
import urllib.error
from http.server import HTTPServer, SimpleHTTPRequestHandler

# ── Get API key from command-line arg or environment variable ──────────────
API_KEY = ''
if len(sys.argv) > 1:
    API_KEY = sys.argv[1].strip()
elif os.environ.get('ANTHROPIC_API_KEY'):
    API_KEY = os.environ.get('ANTHROPIC_API_KEY')

ANTHROPIC_URL = 'https://api.anthropic.com/v1/messages'
PORT = 8080


class NocHandler(SimpleHTTPRequestHandler):

    # ── Handle CORS preflight from browser ────────────────────────────────
    def do_OPTIONS(self):
        self.send_response(200)
        self._cors_headers()
        self.end_headers()

    # ── Handle AI Assist API proxy ────────────────────────────────────────
    def do_POST(self):
        if self.path == '/api/analyze':
            if not API_KEY:
                self._json_error(500, 'No API key set. Restart server with: python server.py sk-ant-...')
                return

            # Read request body from browser
            length = int(self.headers.get('Content-Length', 0))
            body   = self.rfile.read(length)

            # Forward to Anthropic (server-to-server — no CORS issues)
            req = urllib.request.Request(
                ANTHROPIC_URL,
                data=body,
                headers={
                    'Content-Type':      'application/json',
                    'x-api-key':         API_KEY,
                    'anthropic-version': '2023-06-01',
                },
                method='POST'
            )

            try:
                with urllib.request.urlopen(req) as resp:
                    result = resp.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self._cors_headers()
                    self.end_headers()
                    self.wfile.write(result)

            except urllib.error.HTTPError as e:
                error_body = e.read()
                self.send_response(e.code)
                self.send_header('Content-Type', 'application/json')
                self._cors_headers()
                self.end_headers()
                self.wfile.write(error_body)

            except Exception as e:
                self._json_error(500, str(e))
        else:
            self._json_error(404, 'Not found')

    # ── Serve static files (html, js, css) ────────────────────────────────
    def do_GET(self):
        super().do_GET()

    # ── Helpers ───────────────────────────────────────────────────────────
    def _cors_headers(self):
        self.send_header('Access-Control-Allow-Origin',  '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def _json_error(self, code, message):
        body = json.dumps({'error': {'message': message}}).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self._cors_headers()
        self.end_headers()
        self.wfile.write(body)

    # ── Suppress request logs cluttering the terminal ─────────────────────
    def log_message(self, fmt, *args):
        status = args[1] if len(args) > 1 else '?'
        path   = args[0].split(' ')[1] if args else '?'
        color  = '\033[92m' if status == '200' else '\033[93m' if status == '304' else '\033[91m'
        reset  = '\033[0m'
        print(f"  {color}{status}{reset}  {path}")


# ── Start ──────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    if not API_KEY:
        print("\n  ⚠  No API key provided.")
        print("     Start with:  python server.py sk-ant-api03-YOUR-KEY-HERE\n")
    else:
        masked = API_KEY[:12] + '...' + API_KEY[-4:]
        print(f"\n  ✓  API key loaded: {masked}")

    print(f"  ✓  Serving at:    http://localhost:{PORT}/noc-dashboard-p6.html")
    print(f"     Press Ctrl+C to stop.\n")

    server = HTTPServer(('', PORT), NocHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")
