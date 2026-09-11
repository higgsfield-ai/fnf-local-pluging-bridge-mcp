import importlib.util
import json
import os
from pathlib import Path
import tempfile
import threading
import unittest
import urllib.error
import urllib.request

spec = importlib.util.spec_from_file_location("bridge", Path(__file__).resolve().parents[1] / "addon/higgsfield_use_blender/bridge.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.bridge = module.Bridge(self.temp.name)
        self.bridge.start()
        self.base = "http://127.0.0.1:%s" % self.bridge.server.server_port

    def tearDown(self):
        self.bridge.stop()
        self.assertFalse(self.bridge.discovery.exists())
        self.temp.cleanup()

    def request(self, path, body=None, headers=None):
        values = {"Authorization": "Bearer " + self.bridge.token, "Content-Type": "application/json"}
        values.update(headers or {})
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(self.base + path, data=data, headers=values)
        with urllib.request.urlopen(req, timeout=2) as response:
            return json.load(response)

    def execute(self, code):
        job = self.request("/execute", {"code": code})
        self.bridge.pump()
        return self.request("/jobs/" + job["job_id"])

    def test_auth_and_origin(self):
        for headers, status in [({"Authorization": "Bearer wrong"}, 401), ({"Origin": "https://example.com"}, 403), ({"Host": "evil.test"}, 403)]:
            with self.assertRaises(urllib.error.HTTPError) as caught:
                self.request("/health", headers=headers)
            self.assertEqual(caught.exception.code, status)
            caught.exception.close()
        self.assertEqual(self.request("/health")["protocol"], module.PROTOCOL)
        if os.name != "nt":
            self.assertEqual(self.bridge.discovery.stat().st_mode & 0o777, 0o600)

    def test_main_thread_and_structured_output(self):
        job = self.request("/execute", {"code": "import threading\nprint('hello')\nresult = {'thread': threading.get_ident(), 'value': 6 * 7}"})
        self.assertEqual(self.request("/jobs/" + job["job_id"])["state"], "queued")
        self.bridge.pump()
        result = self.request("/jobs/" + job["job_id"])
        self.assertTrue(result["ok"])
        self.assertEqual(result["result"], {"thread": threading.get_ident(), "value": 42})
        self.assertEqual(result["stdout"], "hello\n")

    def test_expired_job_never_executes(self):
        job = self.request("/execute", {"code": "raise RuntimeError('should not run')"})
        self.bridge.jobs[job["job_id"]].deadline = 0
        self.bridge.pump()
        result = self.request("/jobs/" + job["job_id"])
        self.assertEqual(result["state"], "expired")
        self.assertNotIn("should not run", result["error"])

    def test_errors_and_non_json_results(self):
        for code in ["raise ValueError('expected failure')", "result = object()", "result = float('nan')", "raise SystemExit(1)"]:
            result = self.execute(code)
            self.assertFalse(result["ok"])
            self.assertIn("error", result)
        self.assertEqual(self.execute("result = 42")["result"], 42)

    def test_logs_and_result_size_limits(self):
        self.assertEqual(len(self.execute("print('x' * 100000)")["stdout"]), 65536)
        result = self.execute("result = 'x' * (17 * 1024 * 1024)")
        self.assertFalse(result["ok"])
        self.assertIn("exceeds 4 MiB", result["error"])

    def test_queue_overload_and_validation(self):
        for body in [{"code": ""}, {"code": "result=1", "timeout_seconds": -1}, [], {"code": 123}]:
            with self.assertRaises(urllib.error.HTTPError) as caught:
                self.request("/execute", body)
            self.assertEqual(caught.exception.code, 400)
            caught.exception.close()
        for _ in range(32):
            self.request("/execute", {"code": "result=1"})
        with self.assertRaises(urllib.error.HTTPError) as caught:
            self.request("/execute", {"code": "result=2"})
        self.assertEqual(caught.exception.code, 503)
        caught.exception.close()

    def test_result_can_be_polled_without_reexecution(self):
        values = []
        self.bridge.namespace = lambda: {"values": values}
        result = self.execute("values.append('once')\nresult = len(values)")
        for _ in range(3):
            self.assertEqual(self.request("/jobs/" + result["job_id"])["result"], 1)
        self.assertEqual(values, ["once"])


if __name__ == "__main__":
    unittest.main()
