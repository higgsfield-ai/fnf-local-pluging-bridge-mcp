"""Real transport with a minimal bpy fixture; this is not a live Blender test."""
import importlib.util
from pathlib import Path
import signal
import sys
import time
import types

spec = importlib.util.spec_from_file_location("bridge", Path(__file__).resolve().parents[1] / "addon/higgsfield_use_blender/bridge.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
bpy = types.ModuleType("bpy")
bpy.app = types.SimpleNamespace(version_string="fixture-4.2", background=True)
bpy.data = types.SimpleNamespace(filepath="fixture.blend", is_dirty=False)
bpy.context = types.SimpleNamespace(scene=types.SimpleNamespace(name="Fixture Scene"))
sys.modules["bpy"] = bpy
bridge = module.Bridge(namespace=lambda: {"bpy": bpy})
bridge.start()
stopped = False


def stop(*_args):
    global stopped
    stopped = True


signal.signal(signal.SIGTERM, stop)
print("ready", flush=True)
try:
    while not stopped:
        time.sleep(bridge.pump())
finally:
    bridge.stop()
