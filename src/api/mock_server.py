"""
Simple API Mock Server (no external deps)
Endpoints:
  - POST /telemetry/heartbeat
  - GET  /auth/status?nick=...&gm=...
  - POST /guild/verify
  - POST /location/state
"""
from __future__ import annotations
from http.server import BaseHTTPRequestHandler, HTTPServer
import json, urllib.parse, sys

def _json_response(handler: BaseHTTPRequestHandler, code: int, data: dict):
    body = json.dumps(data).encode("utf-8")
    handler.send_response(code)
    handler.send_header("Content-Type", "application/json; charset=UTF-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/auth/status":
            qs = urllib.parse.parse_qs(parsed.query)
            nick = (qs.get("nick") or [""])[0]
            gm = (qs.get("gm") or [""])[0]
            state = "GM_VERIFIED" if nick and gm and nick.strip().lower() == gm.strip().lower() else "SELF_VERIFIED"
            return _json_response(self, 200, {"state": state})
        return _json_response(self, 404, {"error": "not found"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        try:
            payload = json.loads(self.rfile.read(length) or b"{}")
        except Exception:
            return _json_response(self, 400, {"error": "invalid json"})
        if self.path == "/telemetry/heartbeat":
            required = ["v","ts_ms","app","session_id","nick_id","node_id","status","hb_seq"]
            if not all(k in payload for k in required):
                return _json_response(self, 400, {"error": "missing fields", "required": required})
            return _json_response(self, 200, {"ok": True})
        if self.path == "/guild/verify":
            nick = (payload.get("nick") or "").strip().lower()
            gm = (payload.get("gm") or "").strip().lower()
            return _json_response(self, 200, {"gm": bool(nick and gm and nick == gm)})
        if self.path == "/location/state":
            if "node_id" not in payload:
                return _json_response(self, 400, {"error": "missing node_id"})
            return _json_response(self, 200, {"ok": True})
        return _json_response(self, 404, {"error": "not found"})

def main(argv=None):
    port = 8787
    if argv and len(argv) >= 2 and argv[0] == "--port":
        try:
            port = int(argv[1])
        except Exception:
            pass
    server = HTTPServer(("127.0.0.1", port), Handler)
    print(f"[mock] serving on http://127.0.0.1:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[mock] stopped")

if __name__ == "__main__":
    main(sys.argv[1:])
