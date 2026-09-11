"""Authenticated loopback transport; Blender data is accessed only by pump()."""

import contextlib
import hmac
import io
import json
import os
from pathlib import Path
import queue
import secrets
import threading
import time
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PROTOCOL = "higgsfield-blender/1"
MAX_BODY = 1_100_000
MAX_RESULT = 4 * 1024 * 1024


class CappedOutput(io.StringIO):
    def write(self, text):
        remaining = max(0, 65536 - self.tell())
        super().write(text[:remaining])
        return len(text)


class Job:
    def __init__(self, code, timeout):
        self.id = secrets.token_hex(16)
        self.code = code
        self.deadline = time.monotonic() + timeout
        self.state = "queued"
        self.response = None
        self.completed = threading.Event()


class Bridge:
    def __init__(self, runtime_dir=None, namespace=None):
        self.directory = Path(runtime_dir or os.environ.get("BLENDER_MCP_RUNTIME_DIR", "") or Path.home() / ".higgsfield" / "blender")
        self.namespace = namespace or (lambda: {})
        self.token = secrets.token_hex(32)
        self.jobs = {}
        self.pending = queue.Queue(maxsize=32)
        self.lock = threading.Lock()
        self.server = None
        self.discovery = self.directory / ("bridge-%s.json" % os.getpid())

    def start(self):
        self.directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        bridge = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_args):
                pass

            def setup(self):
                super().setup()
                self.connection.settimeout(10)

            def send_json(self, status, value):
                data = json.dumps(value, allow_nan=False).encode("utf-8")
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                try:
                    self.wfile.write(data)
                except (BrokenPipeError, ConnectionResetError):
                    pass

            def authorized(self):
                expected_host = "127.0.0.1:%s" % self.server.server_port
                if self.headers.get("Origin") is not None or self.headers.get("Host") != expected_host:
                    self.send_json(403, {"error": "Local clients only"})
                    return False
                expected = "Bearer " + bridge.token
                if not hmac.compare_digest(self.headers.get("Authorization", "").encode(), expected.encode()):
                    self.send_json(401, {"error": "Invalid bridge token"})
                    return False
                return True

            def do_GET(self):
                if not self.authorized():
                    return
                if self.path == "/health":
                    self.send_json(200, {"protocol": PROTOCOL, "pid": os.getpid()})
                    return
                if self.path.startswith("/jobs/"):
                    with bridge.lock:
                        job = bridge.jobs.get(self.path[len("/jobs/"):])
                        value = bridge.snapshot(job) if job else None
                    self.send_json(200 if value else 404, value or {"error": "Unknown or expired job"})
                    return
                self.send_json(404, {"error": "Unknown endpoint"})

            def do_POST(self):
                if not self.authorized():
                    return
                if self.path != "/execute":
                    self.send_json(404, {"error": "Unknown endpoint"})
                    return
                if self.headers.get("Content-Type", "").split(";")[0] != "application/json":
                    self.send_json(415, {"error": "Expected application/json"})
                    return
                try:
                    length = int(self.headers.get("Content-Length", "0"))
                    if not 0 < length <= MAX_BODY:
                        raise ValueError("Request body must be 1..1100000 bytes")
                    body = json.loads(self.rfile.read(length))
                    code = body.get("code")
                    timeout = body.get("timeout_seconds", 120)
                    if not isinstance(code, str) or not code or len(code) > 1_000_000:
                        raise ValueError("code must be a non-empty string up to 1000000 characters")
                    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or not 1 <= timeout <= 600:
                        raise ValueError("timeout_seconds must be 1..600")
                except (ValueError, AttributeError, UnicodeError) as exc:
                    self.send_json(400, {"error": str(exc)})
                    return
                with bridge.lock:
                    if len(bridge.jobs) >= 128:
                        for job_id, old in list(bridge.jobs.items()):
                            if old.completed.is_set():
                                del bridge.jobs[job_id]
                                break
                    job = Job(code, timeout)
                    try:
                        bridge.pending.put_nowait(job)
                    except queue.Full:
                        self.send_json(503, {"error": "Execution queue is full; request was not accepted"})
                        return
                    bridge.jobs[job.id] = job
                self.send_json(202, {"job_id": job.id, "state": "queued"})

        class Server(ThreadingHTTPServer):
            daemon_threads = True

        self.server = Server(("127.0.0.1", 0), Handler)
        record = {"protocol": PROTOCOL, "pid": os.getpid(), "port": self.server.server_port, "token": self.token}
        try:
            fd = os.open(self.discovery, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, "w") as handle:
                json.dump(record, handle)
        except Exception:
            self.server.server_close()
            self.server = None
            raise
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    @staticmethod
    def snapshot(job):
        return {"job_id": job.id, "state": job.state, **(job.response or {})}

    def pump(self):
        try:
            job = self.pending.get_nowait()
        except queue.Empty:
            return 0.05
        with self.lock:
            if time.monotonic() > job.deadline:
                job.state = "expired"
                job.response = {"ok": False, "error": "Expired before execution; no code ran"}
                job.completed.set()
                return 0.05
            job.state = "running"
        stdout, stderr = CappedOutput(), CappedOutput()
        try:
            namespace = {"__name__": "__blender_mcp__", **self.namespace()}
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                exec(compile(job.code, "<blender-mcp>", "exec"), namespace)
            response = {"ok": True, "result": namespace.get("result"), "stdout": stdout.getvalue(), "stderr": stderr.getvalue()}
            encoded = json.dumps(response, allow_nan=False)
            if len(encoded.encode("utf-8")) > MAX_RESULT:
                raise ValueError("Result exceeds 4 MiB; return a file path or smaller result")
        except BaseException:
            response = {"ok": False, "error": traceback.format_exc(), "stdout": stdout.getvalue(), "stderr": stderr.getvalue()}
        with self.lock:
            job.response = response
            job.state = "completed"
            job.code = ""
            job.completed.set()
        return 0.05

    def stop(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.thread.join(timeout=2)
            self.server = None
            try:
                record = json.loads(self.discovery.read_text())
                if record.get("token") == self.token:
                    self.discovery.unlink()
            except (FileNotFoundError, ValueError):
                pass
