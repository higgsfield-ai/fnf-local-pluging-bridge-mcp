"""CLI fixture: exercises pipes and runner behavior, not Blender's scene engine."""
import os
import runpy
import sys
import types

assert sys.argv[1:6] == ["--background", "--factory-startup", "--disable-autoexec", "--python-exit-code", "1"]
assert sys.argv[6] == "--python"
mode = os.environ.get("HF_FIXTURE_MODE")
if mode == "crash":
    sys.exit(3)
if mode == "hang":
    import time
    time.sleep(60)
bpy = types.ModuleType("bpy")
bpy.app = types.SimpleNamespace(version=(4, 2, 0), version_string="fixture-4.2", background=True)
bpy.data = types.SimpleNamespace(filepath="", is_dirty=False)
bpy.context = types.SimpleNamespace(scene=types.SimpleNamespace(name="Scene"))
sys.modules["bpy"] = bpy
print("Fixture startup noise", flush=True)
runpy.run_path(sys.argv[7], run_name="__main__")
