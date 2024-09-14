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

import bpy
import os
from . import cb_props
from . import cb_ops
from . import cb_ui
from . import cb_paths
from bpy.app.handlers import persistent

@persistent
def load_cabinet_builder_library(dummy):
    """
    Load Asset Libraries
    """
    path = cb_paths.get_active_library_path(bpy.context)
    cabinet_builder_library = cb_paths.get_cabinet_builder_asset_library(bpy.context)
    cabinet_builder_library.path = path

def register():
    cb_props.register()
    cb_ui.register()
    cb_ops.register()

    bpy.app.handlers.load_post.append(load_cabinet_builder_library)

def unregister():
    cb_props.register()
    cb_ui.unregister()
    cb_ops.unregister()

    bpy.app.handlers.load_post.remove(load_cabinet_builder_library)