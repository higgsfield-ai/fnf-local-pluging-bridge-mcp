import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("runner", Path(__file__).resolve().parents[1] / "scripts/background_runner.py")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class RunnerTests(unittest.TestCase):
    def run_code(self, code):
        return runner.execute({"job_id": "a" * 32, "code": code})

    def test_errors_and_system_exit_are_results(self):
        for code in ["raise ValueError('expected')", "raise SystemExit(0)", "result = float('nan')", "result = object()"]:
            self.assertFalse(self.run_code(code)["ok"])
        self.assertEqual(self.run_code("result = 42")["result"], 42)

    def test_output_and_result_limits(self):
        result = self.run_code("print('x' * 100000)\nresult = 42")
        self.assertEqual(len(result["stdout"]), 65536)
        self.assertFalse(self.run_code("result = 'x' * (4 * 1024 * 1024)")["ok"])

    def test_main_thread_and_namespace_isolation(self):
        result = self.run_code("import threading\nresult = threading.current_thread() is threading.main_thread()")
        self.assertTrue(result["result"])
        self.run_code("leftover = 42")
        self.assertFalse(self.run_code("result = leftover")["ok"])

    def test_request_validation(self):
        for request in [{"job_id": "bad", "code": "pass"}, {"job_id": "a" * 32, "code": ""}]:
            with self.assertRaises(ValueError):
                runner.execute(request)


if __name__ == "__main__":
    unittest.main()
