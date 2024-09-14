bl_info = {
    "name": "Cabinet Builder",
    "author": "Andrew Peel",
    "version": (2, 1, 15),
    "blender": (4, 1, 0),
    "location": "3D Viewport Sidebar",
    "description": "Tools for designing cabinetry",
    "warning": "",
    "wiki_url": "",
    "category": "Asset Library",
}

from . import cb_props
from . import cb_ops
from . import cb_ui

def register():
    cb_props.register()
    cb_ui.register()
    cb_ops.register()

def unregister():
    cb_props.register()
    cb_ui.unregister()
    cb_ops.unregister()