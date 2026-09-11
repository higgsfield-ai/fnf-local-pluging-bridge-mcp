from pathlib import Path
import runpy
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/install_addon.py"


class InstallerTests(unittest.TestCase):
    def test_install_is_repeatable_and_preserves_other_addons(self):
        with tempfile.TemporaryDirectory() as directory:
            other = Path(directory) / "other.py"
            other.write_text("existing")
            bpy = types.SimpleNamespace(app=types.SimpleNamespace(version=(4, 2, 0)), utils=types.SimpleNamespace(user_resource=lambda *args, **kwargs: directory))
            with patch.dict(sys.modules, {"bpy": bpy}):
                runpy.run_path(str(SCRIPT))
                runpy.run_path(str(SCRIPT))
            self.assertTrue((Path(directory) / "higgsfield_use_blender/bridge.py").is_file())
            self.assertEqual(other.read_text(), "existing")

    def test_installer_refuses_an_unrecognized_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "higgsfield_use_blender"
            target.mkdir()
            existing = target / "__init__.py"
            existing.write_text("unrelated")
            bpy = types.SimpleNamespace(app=types.SimpleNamespace(version=(4, 2, 0)), utils=types.SimpleNamespace(user_resource=lambda *args, **kwargs: directory))
            with patch.dict(sys.modules, {"bpy": bpy}), self.assertRaisesRegex(RuntimeError, "unrecognized"):
                runpy.run_path(str(SCRIPT))
            self.assertEqual(existing.read_text(), "unrelated")
