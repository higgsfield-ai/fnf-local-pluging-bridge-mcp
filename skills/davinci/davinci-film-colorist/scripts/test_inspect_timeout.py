"""Process-boundary regressions. Every SDK module is a temporary Python fake.

No native SDK import, Resolve connection, application operation, or network call.
"""
import importlib.util
from contextlib import redirect_stderr, redirect_stdout
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

BASE = Path(__file__).resolve().parent
HELPER = BASE / "inspect_resolve.py"
spec = importlib.util.spec_from_file_location("timeout_candidate", str(HELPER))
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)

FAKE_SDK = '''import os, sys, time, signal
from pathlib import Path
Path(os.environ["FAKE_IMPORT_MARKER"]).write_text("fake imported")
class Resolve:
    def GetCurrentPage(self):
        if os.environ.get("FAKE_MODE") == "snapshot_hang":
            print("getter-before-wait", file=sys.stderr, flush=True)
            time.sleep(120)
        return "edit"
def scriptapp(name):
    mode = os.environ.get("FAKE_MODE", "ok")
    if mode in ("warning", "warning_error"):
        print("simulated vendor warning", file=sys.stderr, flush=True)
    if mode in ("error", "warning_error"):
        raise RuntimeError("simulated connect failure")
    if mode == "exit":
        sys.exit(7)
    if mode in ("hang", "ignore_term"):
        if mode == "ignore_term":
            signal.signal(signal.SIGTERM, signal.SIG_IGN)
        print("diagnostic-before-wait", file=sys.stderr, flush=True)
        time.sleep(120)
    return Resolve()
'''


class TimeoutProcessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fake SDK ", dir=str(BASE))
        self.root = Path(self.temp.name)
        modules = self.root / "Modules"
        modules.mkdir()
        (modules / "DaVinciResolveScript.py").write_text(FAKE_SDK, encoding="utf-8")
        self.marker = self.root / "import-marker.txt"
        self.env = os.environ.copy()
        self.env.update(RESOLVE_SCRIPT_API=str(self.root),
                        FAKE_IMPORT_MARKER=str(self.marker),
                        PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
        self.env.pop("FAKE_MODE", None)

    def tearDown(self):
        self.temp.cleanup()

    def run_cli(self, *args, **options):
        env = self.env.copy()
        env["FAKE_MODE"] = options.get("mode", "ok")
        return subprocess.run([sys.executable, "-B", str(HELPER)] + list(args),
                              cwd=str(self.root), env=env,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              universal_newlines=True, timeout=10)

    def assert_child_gone(self, pid):
        # Successful wait/reaping is the portable assertion; on POSIX independently
        # confirm that the exact PID no longer exists (no process-name matching).
        if os.name == "posix":
            with self.assertRaises(ProcessLookupError):
                os.kill(pid, 0)

    def test_normal_json_and_output_modes_from_unrelated_cwd(self):
        normal = self.run_cli("--timeout", "5")
        self.assertEqual(normal.returncode, 0, normal.stderr)
        data = json.loads(normal.stdout)
        self.assertEqual(data["schema"], "film-colorist-readonly-snapshot-2")
        self.assertEqual(data["status"], "not_color_page")
        self.assertEqual(normal.stderr, "")
        output = self.root / "new report.json"
        saved = self.run_cli("--output", str(output), "--timeout", "5")
        self.assertEqual(saved.returncode, 0, saved.stderr)
        self.assertEqual(saved.stdout, "")
        self.assertEqual(saved.stderr, "")
        self.assertEqual(json.loads(output.read_text())["status"], "not_color_page")

    def test_error_preserves_original_single_json_diagnostic(self):
        result = self.run_cli(mode="error")
        direct_env = self.env.copy()
        direct_env["FAKE_MODE"] = "error"
        direct = subprocess.run([sys.executable, "-B", str(HELPER),
                                 "--_inspect_worker", str(self.root / "direct-phases.jsonl")],
                                env=direct_env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                universal_newlines=True, timeout=5)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, direct.stderr)
        self.assertEqual(json.loads(result.stderr)["code"], "SESSION_CONNECTION_FAILED")

    def test_scriptapp_hang_has_flushed_phase_diagnostic_and_reaped_child(self):
        started = time.monotonic()
        result = self.run_cli("--timeout", "0.5", mode="hang")
        self.assertLess(time.monotonic() - started, 6)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        error = json.loads(result.stderr)
        self.assertEqual(error["code"], "INSPECT_TIMEOUT")
        self.assertEqual(error["stage"], "before_scriptapp")
        self.assertIn("diagnostic-before-wait", error["child_stderr"])
        self.assertTrue(error["cleanup_completed"])
        self.assertIsNotNone(error["child_returncode"])
        self.assert_child_gone(error["child_pid"])

    def test_snapshot_hang_is_covered_and_never_creates_output(self):
        output = self.root / "timeout.json"
        result = self.run_cli("--timeout", "0.5", "--output", str(output), mode="snapshot_hang")
        error = json.loads(result.stderr)
        self.assertEqual(error["stage"], "before_snapshot")
        self.assertIn("getter-before-wait", error["child_stderr"])
        self.assertFalse(output.exists())
        self.assertEqual(result.stdout, "")
        self.assertTrue(error["cleanup_completed"])
        self.assert_child_gone(error["child_pid"])

    @unittest.skipUnless(os.name == "posix", "POSIX SIGTERM-ignore simulation")
    def test_term_resistant_child_is_killed_without_stopping_unrelated_peer(self):
        peer = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"],
                                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
        try:
            result = self.run_cli("--timeout", "0.5", mode="ignore_term")
            error = json.loads(result.stderr)
            self.assertEqual(error["child_returncode"], -9)
            self.assertTrue(error["cleanup_completed"])
            self.assertIsNone(peer.poll())
            self.assert_child_gone(error["child_pid"])
        finally:
            peer.terminate()
            peer.wait(timeout=3)

    def test_existing_output_rejected_before_child_vendor_import(self):
        output = self.root / "existing.json"
        output.write_text("preserve me")
        result = self.run_cli("--output", str(output))
        self.assertEqual(json.loads(result.stderr)["code"], "OUTPUT_EXISTS")
        self.assertEqual(output.read_text(), "preserve me")
        self.assertFalse(self.marker.exists())

    def test_abnormal_child_exit_keeps_phase_and_returncode(self):
        result = self.run_cli(mode="exit")
        error = json.loads(result.stderr)
        self.assertEqual(error["code"], "INSPECT_CHILD_FAILED")
        self.assertEqual(error["child_returncode"], 7)
        self.assertEqual(error["last_phase"]["phase"], "before_scriptapp")
        self.assertEqual(result.stdout, "")

    def test_nonfinite_or_nonpositive_timeout_rejected_before_import(self):
        for value in ("nan", "inf", "0", "-1"):
            with self.subTest(value=value):
                result = self.run_cli("--timeout", value)
                self.assertEqual(json.loads(result.stderr)["code"], "TIMEOUT_INVALID")
                self.assertFalse(self.marker.exists())

    def test_parent_interruption_attempts_own_child_cleanup(self):
        child = unittest.mock.Mock()
        child.returncode = None
        child.poll.return_value = None
        child.wait.side_effect = KeyboardInterrupt()
        with patch.object(helper.subprocess, "Popen", return_value=child), \
             patch.object(helper, "stop_child", return_value={"cleanup_completed": False,
                 "child_returncode": None, "cleanup_errors": ["simulated denied cleanup"]}) as stop:
            outcome = helper.supervise(["fake-child"], 1, self.root / "phase.jsonl")
            self.assertTrue(outcome["interrupted"])
            self.assertFalse(outcome["cleanup_completed"])
            self.assertIn("simulated denied cleanup", outcome["cleanup_errors"])
            stop.assert_called_once_with(child)

    def test_interrupt_during_cleanup_does_not_skip_kill(self):
        child = unittest.mock.Mock()
        child.poll.return_value = None
        child.returncode = None
        def finish(timeout):
            if not child.kill.called:
                raise KeyboardInterrupt()
            child.returncode = -9
        child.wait.side_effect = finish
        outcome = helper.stop_child(child)
        child.terminate.assert_called_once_with()
        child.kill.assert_called_once_with()
        self.assertTrue(outcome["cleanup_completed"])
        self.assertTrue(any("KeyboardInterrupt" in e for e in outcome["cleanup_errors"]))

    def fake_outcome(self, **changes):
        data = {"stdout": "", "stderr": "diagnostic-before-wait\n", "timed_out": True,
                "interrupted": False, "supervisor_error": None, "child_pid": 123,
                "elapsed_seconds": 1, "last_phase": {"phase": "before_scriptapp"},
                "cleanup_completed": False, "child_returncode": None, "cleanup_errors": []}
        data.update(changes)
        return data

    def test_temp_cleanup_failure_preserves_timeout_and_child_diagnostic(self):
        folder = self.root / "transport"
        folder.mkdir()
        stderr = io.StringIO()
        with patch.object(helper, "supervise", return_value=self.fake_outcome()), \
             patch.object(helper.tempfile, "mkdtemp", return_value=str(folder)), \
             patch.object(helper.shutil, "rmtree", side_effect=PermissionError("open Windows handle")), \
             redirect_stderr(stderr):
            self.assertEqual(helper.cli([]), 2)
        error = json.loads(stderr.getvalue())
        self.assertEqual(error["code"], "INSPECT_TIMEOUT")
        self.assertFalse(error["cleanup_completed"])
        self.assertEqual(error["child_pid"], 123)
        self.assertIn("open Windows handle", error["transport_cleanup_error"])

    def test_interruption_json_keeps_cleanup_result(self):
        stderr = io.StringIO()
        outcome = self.fake_outcome(timed_out=False, interrupted=True)
        with patch.object(helper, "supervise", return_value=outcome), redirect_stderr(stderr):
            self.assertEqual(helper.cli([]), 2)
        error = json.loads(stderr.getvalue())
        self.assertEqual(error["code"], "INSPECT_INTERRUPTED")
        self.assertEqual(error["stage"], "before_scriptapp")
        self.assertEqual(error["child_pid"], 123)
        self.assertFalse(error["cleanup_completed"])

    def test_vendor_warning_survives_success_and_preserves_error_code(self):
        normal = self.run_cli(mode="warning")
        self.assertEqual(normal.returncode, 0)
        self.assertEqual(json.loads(normal.stdout)["status"], "not_color_page")
        self.assertEqual(normal.stderr, "simulated vendor warning\n")
        failed = self.run_cli(mode="warning_error")
        self.assertEqual(failed.returncode, 2)
        self.assertEqual(failed.stdout, "")
        lines = failed.stderr.splitlines()
        self.assertEqual(lines[0], "simulated vendor warning")
        self.assertEqual(json.loads(lines[1])["code"], "SESSION_CONNECTION_FAILED")

    def test_completed_unicode_json_is_forwarded_exactly(self):
        payload = '{"name":"\u041a\u0430\u0434\u0440","status":"ok"}\n'
        outcome = self.fake_outcome(stdout=payload, stderr="", timed_out=False,
                                    cleanup_completed=True, child_returncode=0)
        stdout = io.StringIO()
        with patch.object(helper, "supervise", return_value=outcome), redirect_stdout(stdout):
            self.assertEqual(helper.cli([]), 0)
        self.assertEqual(stdout.getvalue(), payload)

    def test_unicode_vendor_warning_cannot_mask_error_on_ascii_stderr(self):
        class AsciiSink(io.StringIO):
            def write(self, text):
                text.encode("ascii")
                return super().write(text)
        error = {"status": "error", "code": "SESSION_UNAVAILABLE", "stage": "session_connect",
                 "message": "No session"}
        text = "\u041f\u0440\u0435\u0434\u0443\u043f\u0440\u0435\u0436\u0434\u0435\u043d\u0438\u0435\n" + json.dumps(error) + "\n"
        outcome = self.fake_outcome(stderr=text, timed_out=False, cleanup_completed=True,
                                    child_returncode=2)
        stderr = AsciiSink()
        with patch.object(helper, "supervise", return_value=outcome), redirect_stderr(stderr):
            self.assertEqual(helper.cli([]), 2)
        self.assertEqual(json.loads(stderr.getvalue().splitlines()[1]), error)

    def test_parent_exclusive_output_commit_survives_race(self):
        output = self.root / "raced.json"
        def completed(*args):
            output.write_text("concurrent data")
            return self.fake_outcome(stdout='{"status":"ok"}\n', stderr="", timed_out=False,
                                     cleanup_completed=True, child_returncode=0)
        stderr = io.StringIO()
        with patch.object(helper, "supervise", side_effect=completed), redirect_stderr(stderr):
            self.assertEqual(helper.cli(["--output", str(output)]), 2)
        self.assertEqual(json.loads(stderr.getvalue())["code"], "OUTPUT_EXISTS")
        self.assertEqual(output.read_text(), "concurrent data")


if __name__ == "__main__":
    unittest.main()
