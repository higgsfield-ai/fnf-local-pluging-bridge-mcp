bl_info = {
    "name": "Higgsfield use Blender",
    "author": "Higgsfield",
    "version": (0, 1, 0),
    "blender": (4, 2, 0),
    "category": "Interface",
    "description": "Local MCP control over authenticated loopback HTTP",
}

import bpy
import atexit
from .bridge import Bridge

_bridge = None


def _pump():
    return _bridge.pump() if _bridge else None


def register():
    global _bridge
    if _bridge:
        return
    bridge = Bridge(namespace=lambda: {"bpy": bpy})
    bridge.start()
    _bridge = bridge
    atexit.register(bridge.stop)
    bpy.app.timers.register(_pump, first_interval=0.05, persistent=True)


def unregister():
    global _bridge
    if bpy.app.timers.is_registered(_pump):
        bpy.app.timers.unregister(_pump)
    if _bridge:
        atexit.unregister(_bridge.stop)
        _bridge.stop()
        _bridge = None
