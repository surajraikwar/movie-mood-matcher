#!/usr/bin/env python
"""Minimal test server to verify Railway deployment."""

import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

print("=== Starting Test Server ===")
print(f"Python version: {sys.version}")
print(f"PORT env var: {os.environ.get('PORT', 'Not set')}")

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                'status': 'healthy',
                'message': 'Test server is running',
                'python_version': sys.version,
                'port': os.environ.get('PORT', 'Not set')
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting test server on port {port}")
    
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    print(f"Test server listening on 0.0.0.0:{port}")
    print("Health check endpoint: /health")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.shutdown()
