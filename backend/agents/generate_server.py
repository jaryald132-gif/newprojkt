# backend/agents/generate_server.py
import json
from pathlib import Path

FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"

PACKAGE_JSON = {
  "name": "ascendant-agents-frontend",
  "version": "1.0.0",
  "private": True,
  "description": "Tactical UI for ASCENDANT AGENTS Multi-Agent Disaster Response System",
  "scripts": {
    "dev": "vite --port 5173 --host",
    "serve": "python server.py"
  },
  "devDependencies": {
    "vite": "^5.0.0"
  }
}

with open(FRONTEND_DIR / "package.json", "w", encoding="utf-8") as f:
    json.dump(PACKAGE_JSON, f, indent=2)

SERVER_PY = """# frontend/server.py
import http.server
import socketserver
import os
from pathlib import Path

PORT = 5173
DIRECTORY = Path(__file__).resolve().parent

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"ASCENDANT AGENTS Frontend running at: http://localhost:{PORT}")
        httpd.serve_forever()
"""

with open(FRONTEND_DIR / "server.py", "w", encoding="utf-8") as f:
    f.write(SERVER_PY)

print("Generated frontend/package.json and frontend/server.py successfully.")
