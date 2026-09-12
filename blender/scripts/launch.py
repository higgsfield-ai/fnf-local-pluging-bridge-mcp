"""Load the bundled bridge in a new Blender session without changing preferences."""
import sys
from pathlib import Path
import bpy

if bpy.app.version < (4, 2, 0):
    raise RuntimeError("Higgsfield use Blender requires Blender 4.2+")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "addon"))
import higgsfield_use_blender
higgsfield_use_blender.register()
