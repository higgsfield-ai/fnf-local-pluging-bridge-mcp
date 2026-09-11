"""Install source files only; never reset or save the user's preferences."""
import shutil
from pathlib import Path
import bpy

if bpy.app.version < (4, 2, 0):
    raise RuntimeError("Higgsfield use Blender requires Blender 4.2+")
source = Path(__file__).resolve().parent.parent / "addon" / "higgsfield_use_blender"
target = Path(bpy.utils.user_resource("SCRIPTS", path="addons", create=True)) / source.name
marker = target / ".higgsfield-use-blender"
if target.exists() and not marker.is_file():
    raise RuntimeError("Refusing to overwrite an unrecognized add-on directory: %s" % target)
target.mkdir(parents=True, exist_ok=True)
for name in ("__init__.py", "bridge.py"):
    shutil.copy2(source / name, target / name)
marker.write_text("fnf-blender-mcp\n")
print("Installed: %s" % target)
print("Enable Higgsfield use Blender in Preferences > Add-ons, then save preferences for automatic startup.")
