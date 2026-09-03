#!/usr/bin/env python3
"""IHS Practice Files photo-bridge.

Signaling only for a same-WiFi WebRTC datachannel. Never writes photos.
Never logs SDP or request bodies. In-memory mailbox only.

Desktop Chrome (GitHub Pages) fetches http://127.0.0.1:17831 only.
The phone must not fetch LAN HTTP from the HTTPS page (mixed content).
The phone may window.open this origin from a user gesture and postMessage
the answer SDP so this page POSTs to itself.

Bind: 0.0.0.0:17831 (accepts 127.0.0.1 and LAN IPv4).
"""

from __future__ import annotations

import json
import re
import socket
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

PORT = 17831
TTL_SEC = 600
MAX_BODY = 48 * 1024
CODE_RE = re.compile(r"^[A-Za-z0-9]{4,8}$")

ALLOWED_EXACT = {
    "https://in-housesystems.com",
    "http://localhost",
    "http://127.0.0.1",
}

_mailbox = {}
_lock = threading.Lock()


def is_private_ipv4(ip):
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    try:
        n = [int(x) for x in parts]
    except ValueError:
        return False
    if any(x < 0 or x > 255 for x in n):
        return False
    if n[0] == 10:
        return True
    if n[0] == 172 and 16 <= n[1] <= 31:
        return True
    if n[0] == 192 and n[1] == 168:
        return True
    return False


def lan_ipv4():
    found = []

    def add(ip):
        if not ip or ip.startswith("127."):
            return
        if is_private_ipv4(ip) and ip not in found:
            found.append(ip)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.connect(("192.0.2.1", 1))
            add(sock.getsockname()[0])
        finally:
            sock.close()
    except OSError:
        pass

    try:
        host = socket.gethostname()
        for info in socket.getaddrinfo(host, None, socket.AF_INET):
            add(info[4][0])
    except OSError:
        pass

    return found


def origin_ok(origin):
    if not origin:
        return False
    if origin in ALLOWED_EXACT:
        return True
    if origin.startswith("http://localhost:"):
        return origin[len("http://localhost:") :].isdigit()
    if origin.startswith("http://127.0.0.1:"):
        return origin[len("http://127.0.0.1:") :].isdigit()
    return False


def sweep_mailbox():
    now = time.time()
    dead = [k for k, v in _mailbox.items() if now - v["ts"] > TTL_SEC]
    for k in dead:
        _mailbox.pop(k, None)


STATUS_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>IHS photo-bridge</title>
<style>
:root { --bone:#f3eee4; --navy:#10141c; --mint:#7fe0b8; --ink:#111; --muted:#5a574e; }
body { margin:0; font-family: system-ui, sans-serif; background:#f3eee4; color:#111; line-height:1.45; }
main { max-width: 36rem; margin: 0 auto; padding: 28px 16px; }
h1 { font-family: Georgia, "Times New Roman", serif; font-weight:400; }
.card { background:#ebe4d6; border-radius:12px; padding:18px; border-left:5px solid #10141c; }
code { font-size: 0.95em; }
</style>
</head>
<body>
<main>
<h1>IHS photo-bridge</h1>
<div class="card">
<p>Signaling only. This process never writes photos and never stores them on disk.</p>
<p>Desktop Pages should fetch <code>http://127.0.0.1:17831</code> only.</p>
<p>Keep this window open while pairing a phone on the same Wi‑Fi.</p>
</div>
</main>
</body>
</html>
"""

RELAY_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'; img-src 'none'; font-src 'none'; object-src 'none'; frame-src 'none'; form-action 'none'; base-uri 'none'">
<title>IHS photo-bridge</title>
<style>
:root { --bone:#f3eee4; --navy:#10141c; --mint:#7fe0b8; --ink:#111; }
body { margin:0; font-family: system-ui, sans-serif; background:#f3eee4; color:#111; line-height:1.45; }
main { max-width: 36rem; margin: 0 auto; padding: 28px 16px; }
h1 { font-family: Georgia, "Times New Roman", serif; font-weight:400; }
.card { background:#ebe4d6; border-radius:12px; padding:18px; border-left:5px solid #10141c; }
</style>
</head>
<body>
<main>
<h1>IHS photo-bridge</h1>
<div class="card" id="msg">Waiting for pairing data from the camera page…</div>
</main>
<script>
(function () {
  'use strict';
  function allowed(origin) {
    if (origin === 'https://in-housesystems.com') return true;
    if (origin === 'http://localhost' || origin === 'http://127.0.0.1') return true;
    if (/^http:\\/\\/localhost:\\d+$/.test(origin)) return true;
    if (/^http:\\/\\/127\\.0\\.0\\.1:\\d+$/.test(origin)) return true;
    return false;
  }
  function setMsg(t) {
    var el = document.getElementById('msg');
    if (el) el.textContent = t;
  }
  window.addEventListener('message', function (e) {
    if (!allowed(e.origin)) return;
    var data = e.data;
    if (!data || data.type !== 'sdp-answer') return;
    if (typeof data.code !== 'string' || !data.answer) return;
    fetch('/pull', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code: data.code, answer: data.answer })
    }).then(function (r) {
      if (r.ok) {
        setMsg('Paired. You can close this window and return to the camera.');
        if (window.opener) window.opener.postMessage({ type: 'relay-ok' }, e.origin);
      } else {
        setMsg('Pairing failed. Close this window and tap Connect on the camera page again.');
        if (window.opener) window.opener.postMessage({ type: 'relay-fail' }, e.origin);
      }
    }).catch(function () {
      setMsg('Pairing failed. Close this window and tap Connect on the camera page again.');
      if (window.opener) window.opener.postMessage({ type: 'relay-fail' }, e.origin);
    });
  });
  if (window.opener) {
    try { window.opener.postMessage({ type: 'relay-ready' }, '*'); } catch (err) {}
  } else {
    setMsg('Open this window from the camera page Connect button.');
  }
})();
</script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        path = (self.path or "/").split("?", 1)[0]
        sys.stderr.write("photo-bridge %s %s\n" % (self.command, path))

    def cors(self):
        origin = self.headers.get("Origin", "")
        if origin_ok(origin):
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Private-Network", "true")
        self.send_header("Access-Control-Max-Age", "600")
        self.send_header("Cache-Control", "no-store")

    def send_bytes(self, status, body, content_type):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.cors()
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def send_empty(self, status):
        self.send_response(status)
        self.send_header("Content-Length", "0")
        self.cors()
        self.end_headers()

    def do_OPTIONS(self):
        self.send_empty(204)

    def do_HEAD(self):
        self.do_GET(head=True)

    def do_GET(self, head=False):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        if path in ("/", "/index.html"):
            self.send_bytes(200, STATUS_PAGE, "text/html; charset=utf-8")
            return
        if path == "/relay":
            self.send_bytes(200, RELAY_PAGE, "text/html; charset=utf-8")
            return
        if path == "/info":
            payload = json.dumps(
                {"ok": True, "port": PORT, "lan": lan_ipv4()},
                separators=(",", ":"),
            )
            self.send_bytes(200, payload, "application/json")
            return
        if path == "/pull":
            code = (query.get("c") or query.get("code") or [""])[0]
            if not CODE_RE.match(code):
                self.send_empty(400)
                return
            with _lock:
                sweep_mailbox()
                item = _mailbox.pop(code, None)
            if not item:
                self.send_empty(204)
                return
            payload = json.dumps({"answer": item["answer"]}, separators=(",", ":"))
            self.send_bytes(200, payload, "application/json")
            return
        self.send_empty(404)

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != "/pull":
            self.send_empty(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self.send_empty(400)
            return
        if length < 1 or length > MAX_BODY:
            self.send_empty(400)
            return
        raw = self.rfile.read(length)
        try:
            data = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
            self.send_empty(400)
            return
        code = data.get("code") if isinstance(data, dict) else None
        answer = data.get("answer") if isinstance(data, dict) else None
        if not isinstance(code, str) or not CODE_RE.match(code):
            self.send_empty(400)
            return
        if not isinstance(answer, dict):
            self.send_empty(400)
            return
        if answer.get("type") != "answer" or not isinstance(answer.get("sdp"), str):
            self.send_empty(400)
            return
        if len(answer["sdp"]) < 20 or len(answer["sdp"]) > 40000:
            self.send_empty(400)
            return
        with _lock:
            sweep_mailbox()
            if len(_mailbox) >= 32:
                oldest = sorted(_mailbox.items(), key=lambda kv: kv[1]["ts"])
                for k, _ in oldest[:8]:
                    _mailbox.pop(k, None)
            _mailbox[code] = {"answer": {"type": "answer", "sdp": answer["sdp"]}, "ts": time.time()}
        self.send_empty(204)


class BridgeServer(ThreadingHTTPServer):
    allow_reuse_address = True
    daemon_threads = True


def main():
    lan = lan_ipv4()
    try:
        httpd = BridgeServer(("0.0.0.0", PORT), Handler)
    except OSError as e:
        sys.stderr.write(
            "photo-bridge could not bind 0.0.0.0:%s (also used as 127.0.0.1:%s): %s\n"
            % (PORT, PORT, e)
        )
        return 1
    sys.stderr.write(
        "photo-bridge listening on 127.0.0.1:%s and 0.0.0.0:%s (signaling only, no photos)\n"
        % (PORT, PORT)
    )
    if lan:
        sys.stderr.write("LAN IPv4: %s\n" % ", ".join(lan))
    else:
        sys.stderr.write("No private IPv4 found. Connect this PC to Wi‑Fi and restart the bridge.\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        sys.stderr.write("\nphoto-bridge stopped\n")
    finally:
        httpd.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
