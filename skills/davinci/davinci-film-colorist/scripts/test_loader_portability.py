"""Mocked portability tests; no real vendor import, filesystem probe or session.

The standalone helper is imported with vendor imports guarded. Its own platform,
environment, pathlib, importlib, struct and session dependencies are then fake.
"""

import builtins
from contextlib import ExitStack, redirect_stderr, redirect_stdout
import importlib.util
import io
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import stat
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch


def load_standalone_helper():
    original_import = builtins.__import__

    def deny_vendor(name, *args, **kwargs):
        if name.split(".", 1)[0] in {"DaVinciResolveScript", "DaVinciResolve", "fusionscript"}:
            raise AssertionError("Real vendor imports are forbidden")
        return original_import(name, *args, **kwargs)

    path = Path(__file__).with_name("inspect_resolve.py")
    spec = importlib.util.spec_from_file_location("_offline_portability_helper", path)
    module = importlib.util.module_from_spec(spec)
    with patch("builtins.__import__", deny_vendor):
        spec.loader.exec_module(module)
    return module


helper = load_standalone_helper()
WRAPPER = "DaVinciResolveScript.py"
MAC_MODULES = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules"
WIN_MODULES = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules"
OPT_MODULES = "/opt/resolve/Developer/Scripting/Modules"
HOME_MODULES = "/home/resolve/Developer/Scripting/Modules"


class FakePath:
    def __init__(self, fs, value):
        self.fs = fs
        self.path = fs.pure(str(value))

    def __str__(self):
        return str(self.path)

    def __fspath__(self):
        return str(self)

    def __truediv__(self, other):
        return FakePath(self.fs, self.path / str(other))

    @property
    def suffix(self):
        return self.path.suffix

    @property
    def parent(self):
        return FakePath(self.fs, self.path.parent)

    def expanduser(self):
        if self.fs.expand_error is not None:
            raise self.fs.expand_error
        if self.path.parts and self.path.parts[0] == "~":
            return FakePath(self.fs, self.fs.pure(self.fs.home).joinpath(*self.path.parts[1:]))
        return self

    def is_file(self):
        self.fs.probes.append((str(self), "is_file"))
        if self.fs.probe_error is not None:
            raise self.fs.probe_error
        return str(self) in self.fs.files

    def is_dir(self):
        self.fs.probes.append((str(self), "is_dir"))
        return str(self) in self.fs.dirs

    def exists(self):
        self.fs.probes.append((str(self), "exists"))
        return str(self) in self.fs.files or str(self) in self.fs.dirs

    def stat(self):
        self.fs.probes.append((str(self), "stat"))
        if self.fs.stat_error is not None:
            raise self.fs.stat_error
        if str(self) in self.fs.dirs:
            return SimpleNamespace(st_mode=stat.S_IFDIR | 0o755)
        if str(self) in self.fs.files:
            return SimpleNamespace(st_mode=stat.S_IFREG | 0o644)
        raise FileNotFoundError(str(self))

    def lstat(self):
        self.fs.probes.append((str(self), "lstat"))
        if str(self) in self.fs.symlinks:
            return SimpleNamespace(st_mode=stat.S_IFLNK | 0o777)
        return self.stat()

    def open(self, mode, encoding=None):
        self.fs.opens.append((str(self), mode, encoding))
        if mode != "x":
            raise AssertionError("Only exclusive output creation is permitted")
        if self.fs.open_error is not None:
            raise self.fs.open_error
        if str(self) in self.fs.files:
            raise FileExistsError(str(self))
        if str(self.parent) not in self.fs.dirs:
            raise FileNotFoundError(str(self.parent))
        self.fs.files.add(str(self))
        self.fs.texts[str(self)] = ""
        return FakeWriter(self.fs, str(self))


class FakeWriter:
    def __init__(self, fs, path):
        self.fs, self.path = fs, path

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def write(self, value):
        self.fs.texts[self.path] += value


class FakeFS:
    def __init__(self, platform):
        self.pure = PureWindowsPath if platform.startswith("win") else PurePosixPath
        self.home = r"C:\Users\Tester" if platform.startswith("win") else "/fake-user"
        self.files, self.dirs, self.symlinks, self.texts = set(), set(), set(), {}
        self.probes, self.opens = [], []
        self.open_error = self.stat_error = self.probe_error = self.expand_error = None

    def Path(self, value):
        return FakePath(self, value)

    def add_wrapper(self, modules):
        self.files.add(str(self.pure(modules) / WRAPPER))


class Harness:
    def __init__(self, platform="darwin", env=None, pointer_bytes=8, version=(3, 12, 0)):
        self.fs = FakeFS(platform)
        self.env = dict(env or {})
        self.stdout, self.stderr = io.StringIO(), io.StringIO()
        self.runtime = SimpleNamespace(platform=platform, path=["already-configured"],
                                       dont_write_bytecode=False, version_info=version,
                                       stderr=self.stderr, stdout=self.stdout)
        self.pointer_bytes = pointer_bytes
        self.imports, self.connections = [], []
        self.import_error, self.connect_error = None, None
        self.session = object()
        self.wrapper = SimpleNamespace(scriptapp=self.connect)

    def import_module(self, name):
        if name != "DaVinciResolveScript":
            raise AssertionError("Unexpected module import: " + name)
        self.imports.append({"name": name, "path": tuple(self.runtime.path),
                             "library": self.env.get("RESOLVE_SCRIPT_LIB")})
        if self.import_error is not None:
            raise self.import_error
        return self.wrapper

    def connect(self, name):
        self.connections.append(name)
        if self.connect_error is not None:
            raise self.connect_error
        return self.session

    def patches(self):
        stack = ExitStack()
        stack.enter_context(patch.object(helper, "sys", self.runtime))
        stack.enter_context(patch.object(helper, "os", SimpleNamespace(environ=self.env)))
        stack.enter_context(patch.object(helper, "Path", self.fs.Path))
        stack.enter_context(patch.object(helper, "importlib",
                                         SimpleNamespace(import_module=self.import_module)))
        stack.enter_context(patch.object(helper, "struct", SimpleNamespace(
            calcsize=lambda format_code: self.pointer_bytes)))
        return stack

    def load(self):
        before_env, before_files = self.env.copy(), self.fs.files.copy()
        try:
            with self.patches():
                return helper.load_resolve_module()
        finally:
            if self.env != before_env or self.fs.files != before_files or self.fs.opens:
                raise AssertionError("Loader changed environment or files")

    def main(self, output=None, result=None, snapshot_error=None):
        argv = ["inspect_resolve.py"]
        if output is not None:
            argv += ["--output", output]
        self.runtime.argv = argv
        if result is None:
            result = {"status": "ok", "current_page": "color"}
        with self.patches(), patch.object(sys, "argv", argv), \
             patch.object(helper, "snapshot", return_value=result, side_effect=snapshot_error) as snapshot, \
             redirect_stdout(self.stdout), redirect_stderr(self.stderr):
            code = helper.main()
        return code, snapshot


class AsciiOnlySink(io.StringIO):
    def __init__(self):
        super().__init__()
        self.reconfigures = []

    @property
    def encoding(self):
        return "ascii"

    def write(self, text):
        text.encode("ascii", errors="strict")
        return super().write(text)

    def reconfigure(self, **options):
        self.reconfigures.append(options)
        raise AssertionError("Helper must not reconfigure the caller's stream")


class BrokenStdout(io.StringIO):
    def write(self, text):
        raise BrokenPipeError("mocked stdout pipe is closed")


class LoaderPortabilityTests(unittest.TestCase):
    def assert_selected(self, h, modules):
        self.assertIs(h.load(), h.wrapper)
        self.assertEqual(len(h.imports), 1)
        self.assertEqual(h.imports[0]["path"][0], str(h.fs.pure(modules)))
        self.assertTrue(h.runtime.dont_write_bytecode)
        self.assertEqual(h.connections, [], "Module discovery connected to Resolve")

    def test_macos_default_sdk(self):
        h = Harness("darwin")
        h.fs.add_wrapper(MAC_MODULES)
        self.assert_selected(h, MAC_MODULES)

    def test_windows_default_sdk_uses_native_windows_paths(self):
        h = Harness("win32")
        h.fs.add_wrapper(WIN_MODULES)
        self.assert_selected(h, WIN_MODULES)

    def test_windows_programdata_override_preserves_drive_and_spaces(self):
        h = Harness("win32", {"PROGRAMDATA": r"D:\Shared App Data"})
        modules = r"D:\Shared App Data\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules"
        h.fs.add_wrapper(modules)
        self.assert_selected(h, modules)

    def test_linux_standard_and_iso_fallback_locations(self):
        for modules in (OPT_MODULES, HOME_MODULES):
            with self.subTest(modules=modules):
                h = Harness("linux")
                h.fs.add_wrapper(modules)
                self.assert_selected(h, modules)

    def test_explicit_sdk_precedes_also_available_default_sdk(self):
        h = Harness("darwin", {"RESOLVE_SCRIPT_API": "/chosen/sdk"})
        h.fs.add_wrapper("/chosen/sdk/Modules")
        h.fs.add_wrapper(MAC_MODULES)
        self.assert_selected(h, "/chosen/sdk/Modules")

    def test_tilde_sdk_uses_current_mocked_user(self):
        h = Harness("darwin", {"RESOLVE_SCRIPT_API": "~/portable-sdk"})
        h.fs.add_wrapper("/fake-user/portable-sdk/Modules")
        self.assert_selected(h, "/fake-user/portable-sdk/Modules")

    def test_missing_override_can_use_declared_default_fallback(self):
        h = Harness("darwin", {"RESOLVE_SCRIPT_API": "/not-installed/sdk"})
        h.fs.add_wrapper(MAC_MODULES)
        self.assert_selected(h, MAC_MODULES)

    def test_preconfigured_import_path_works_without_standard_sdk_file(self):
        h = Harness("darwin")
        self.assertIs(h.load(), h.wrapper)
        self.assertEqual(h.imports[0]["path"], ("already-configured",))
        self.assertEqual(len(h.imports), 1)

    def test_native_library_override_is_left_to_vendor_wrapper(self):
        library = "/chosen/native-library/fusionscript.so"
        h = Harness("darwin", {"RESOLVE_SCRIPT_LIB": library})
        h.fs.add_wrapper(MAC_MODULES)
        self.assert_selected(h, MAC_MODULES)
        self.assertEqual(h.imports[0]["library"], library)
        self.assertFalse(any(path == library for path, _ in h.fs.probes))

    def test_missing_wrapper_is_distinct_from_missing_transitive_dependency(self):
        for missing_name, expected in (("DaVinciResolveScript", "WRAPPER_NOT_FOUND"),
                                       ("fusionscript", "WRAPPER_IMPORT_FAILED")):
            with self.subTest(missing_name=missing_name):
                h = Harness()
                h.import_error = ModuleNotFoundError("mocked missing module", name=missing_name)
                with self.assertRaises(helper.SnapshotError) as raised:
                    h.load()
                self.assertEqual(raised.exception.code, expected)
                self.assertEqual(raised.exception.stage, "wrapper_import")
                self.assertEqual(len(h.imports), 1)

    def test_found_wrapper_import_failure_does_not_try_lower_priority_wrapper(self):
        h = Harness("darwin", {"RESOLVE_SCRIPT_API": "/chosen/sdk"})
        h.fs.add_wrapper("/chosen/sdk/Modules")
        h.fs.add_wrapper(MAC_MODULES)
        h.import_error = ImportError("mocked native ABI mismatch")
        with self.assertRaises(helper.SnapshotError) as raised:
            h.load()
        self.assertEqual(raised.exception.code, "WRAPPER_IMPORT_FAILED")
        self.assertEqual(raised.exception.stage, "wrapper_import")
        self.assertEqual(len(h.imports), 1)
        self.assertEqual(h.imports[0]["path"][0], "/chosen/sdk/Modules")

    def test_generic_fallback_import_failure_is_not_reported_as_sdk_absent(self):
        h = Harness()
        h.import_error = RuntimeError("mocked wrapper initialization failure")
        with self.assertRaises(helper.SnapshotError) as raised:
            h.load()
        self.assertEqual(raised.exception.code, "WRAPPER_IMPORT_FAILED")

    def test_32bit_runtime_rejects_before_import(self):
        h = Harness(pointer_bytes=4)
        h.fs.add_wrapper(MAC_MODULES)
        with self.assertRaises(helper.SnapshotError) as raised:
            h.load()
        self.assertEqual(raised.exception.code, "PYTHON_BITNESS_UNSUPPORTED")
        self.assertEqual(raised.exception.stage, "runtime")
        self.assertEqual(h.imports, [])

    def test_older_runtime_rejects_before_import_when_module_is_already_parsed(self):
        h = Harness(version=(3, 5, 10))
        h.fs.add_wrapper(MAC_MODULES)
        with self.assertRaises(helper.SnapshotError) as raised:
            h.load()
        self.assertEqual(raised.exception.code, "PYTHON_UNSUPPORTED")
        self.assertEqual(raised.exception.stage, "runtime")
        self.assertEqual(h.imports, [])

    def test_sdk_path_read_error_is_not_reported_as_sdk_absent(self):
        h = Harness()
        h.fs.probe_error = PermissionError("mocked SDK directory access error")
        with self.assertRaises(helper.SnapshotError) as raised:
            h.load()
        self.assertEqual(raised.exception.code, "WRAPPER_DISCOVERY_FAILED")
        self.assertEqual(raised.exception.stage, "wrapper_discovery")
        self.assertEqual(h.imports, [])

    def test_sdk_path_expansion_error_is_reported_before_import(self):
        h = Harness(env={"RESOLVE_SCRIPT_API": "~unavailable-user/sdk"})
        h.fs.expand_error = RuntimeError("mocked user directory cannot be expanded")
        with self.assertRaises(helper.SnapshotError) as raised:
            h.load()
        self.assertEqual(raised.exception.code, "WRAPPER_DISCOVERY_FAILED")
        self.assertEqual(raised.exception.stage, "wrapper_discovery")
        self.assertEqual(h.imports, [])


class MainFailureTests(unittest.TestCase):
    def harness(self):
        h = Harness()
        h.fs.add_wrapper(MAC_MODULES)
        h.fs.dirs.add("/reports")
        return h

    def assert_error(self, h, code, stage=None, expected_code=None):
        self.assertEqual(code, 2)
        self.assertEqual(h.stdout.getvalue(), "")
        payload = json.loads(h.stderr.getvalue())
        self.assertEqual(payload["status"], "error")
        self.assertTrue(payload["code"])
        self.assertTrue(payload["stage"])
        self.assertIsInstance(payload["message"], str)
        self.assertTrue(any("А" <= ch <= "я" or ch in "Ёё" for ch in payload["message"]))
        if stage is not None:
            self.assertEqual(payload["stage"], stage)
        if expected_code is not None:
            self.assertEqual(payload["code"], expected_code)
        return payload

    def test_existing_output_is_rejected_before_import_and_preserved(self):
        h = self.harness()
        h.fs.files.add("/reports/existing.json")
        h.fs.texts["/reports/existing.json"] = "original user report"
        code, _ = h.main("/reports/existing.json")
        self.assert_error(h, code, "output_preflight", "OUTPUT_EXISTS")
        self.assertEqual(h.imports, [])
        self.assertEqual(h.fs.opens, [])
        self.assertEqual(h.fs.texts["/reports/existing.json"], "original user report")

    def test_missing_parent_is_rejected_before_import(self):
        h = self.harness()
        code, _ = h.main("/missing-parent/report.json")
        self.assert_error(h, code, "output_preflight", "OUTPUT_PARENT_MISSING")
        self.assertEqual(h.imports, [])
        self.assertEqual(h.fs.opens, [])

    def test_parent_that_is_file_is_rejected_before_import(self):
        h = self.harness()
        h.fs.files.add("/file-parent")
        code, _ = h.main("/file-parent/report.json")
        self.assert_error(h, code, "output_preflight", "OUTPUT_PARENT_NOT_DIRECTORY")
        self.assertEqual(h.imports, [])

    def test_bad_output_extension_is_rejected_before_import(self):
        h = self.harness()
        code, _ = h.main("/reports/report.txt")
        self.assert_error(h, code, "output_preflight", "OUTPUT_SUFFIX_INVALID")
        self.assertEqual(h.imports, [])

    def test_broken_symlink_output_is_existing_and_never_replaced(self):
        h = self.harness()
        h.fs.symlinks.add("/reports/dangling.json")
        code, _ = h.main("/reports/dangling.json")
        self.assert_error(h, code, "output_preflight", "OUTPUT_EXISTS")
        self.assertEqual(h.imports, [])
        self.assertEqual(h.fs.opens, [])
        self.assertIn("/reports/dangling.json", h.fs.symlinks)

    def test_output_precheck_denial_is_distinct_from_missing_directory(self):
        h = self.harness()
        h.fs.stat_error = PermissionError("mocked stat denied")
        code, _ = h.main("/reports/blocked.json")
        self.assert_error(h, code, "output_preflight", "OUTPUT_PRECHECK_FAILED")
        self.assertEqual(h.imports, [])

    def test_exclusive_create_handles_race_without_overwrite(self):
        h = self.harness()
        h.fs.open_error = FileExistsError("file appeared after preflight")
        h.fs.texts["/reports/raced.json"] = "concurrent writer data"
        code, _ = h.main("/reports/raced.json")
        self.assert_error(h, code, "output_write", "OUTPUT_EXISTS")
        self.assertEqual(h.fs.opens, [("/reports/raced.json", "x", "utf-8")])
        self.assertEqual(h.fs.texts["/reports/raced.json"], "concurrent writer data")

    def test_write_permission_error_is_not_reported_as_session_or_import_failure(self):
        h = self.harness()
        h.fs.open_error = PermissionError("mocked write denial")
        code, _ = h.main("/reports/denied.json")
        self.assert_error(h, code, "output_write", "OUTPUT_WRITE_FAILED")
        self.assertEqual(h.connections, ["Resolve"])

    def test_missing_session_does_not_call_snapshot(self):
        h = self.harness()
        h.session = None
        code, snapshot = h.main()
        self.assert_error(h, code, "session_connect", "SESSION_UNAVAILABLE")
        snapshot.assert_not_called()
        self.assertEqual(h.connections, ["Resolve"])
        self.assertEqual(h.fs.opens, [])

    def test_session_exception_is_reported_before_snapshot(self):
        h = self.harness()
        h.connect_error = OSError("mocked session transport failure")
        code, snapshot = h.main()
        self.assert_error(h, code, "session_connect", "SESSION_CONNECTION_FAILED")
        snapshot.assert_not_called()

    def test_snapshot_exception_has_its_own_error_stage(self):
        h = self.harness()
        code, _ = h.main(snapshot_error=OSError("mocked read failure"))
        self.assert_error(h, code, "snapshot_read", "SNAPSHOT_READ_FAILED")

    def test_unserializable_result_has_its_own_error_stage(self):
        h = self.harness()
        code, _ = h.main(result={"status": "ok", "invalid": float("nan")})
        self.assert_error(h, code, "json_serialize", "SNAPSHOT_SERIALIZE_FAILED")
        self.assertEqual(h.fs.opens, [])

    def test_requested_new_output_is_exclusively_created(self):
        h = self.harness()
        code, _ = h.main("/reports/new.json")
        self.assertEqual(code, 0, h.stderr.getvalue())
        self.assertEqual(h.fs.opens, [("/reports/new.json", "x", "utf-8")])
        self.assertEqual(json.loads(h.fs.texts["/reports/new.json"])["status"], "ok")
        self.assertEqual(h.stdout.getvalue(), "")
        self.assertEqual(h.stderr.getvalue(), "")

    def test_nonready_context_status_is_preserved_as_json(self):
        for status in ("not_color_page", "page_unavailable", "no_current_project"):
            with self.subTest(status=status):
                h = self.harness()
                code, _ = h.main(result={"status": status})
                self.assertEqual(code, 0)
                self.assertEqual(json.loads(h.stdout.getvalue())["status"], status)
                self.assertEqual(h.stderr.getvalue(), "")

    def test_ascii_stderr_preserves_russian_runtime_message_without_reconfiguration(self):
        h = Harness(pointer_bytes=4)
        h.stderr = AsciiOnlySink()
        h.runtime.stderr = h.stderr
        code, _ = h.main()
        self.assert_error(h, code, "runtime", "PYTHON_BITNESS_UNSUPPORTED")
        h.stderr.getvalue().encode("ascii", errors="strict")
        self.assertEqual(h.stderr.reconfigures, [])
        self.assertEqual(h.stderr.encoding, "ascii")
        self.assertEqual(h.imports, [])

    def test_stdout_failure_uses_distinct_code_and_still_reports_on_ascii_stderr(self):
        h = self.harness()
        h.stdout, h.stderr = BrokenStdout(), AsciiOnlySink()
        h.runtime.stdout, h.runtime.stderr = h.stdout, h.stderr
        code, _ = h.main()
        self.assert_error(h, code, "output_write", "STDOUT_WRITE_FAILED")
        h.stderr.getvalue().encode("ascii", errors="strict")
        self.assertEqual(h.stderr.reconfigures, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
