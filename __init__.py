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

def draw_assembly_properties(self, context):
    layout = self.layout
    layout.operator_context = 'INVOKE_AREA'
    obj = context.object
    prompt_id = ""
    menu_id = ""
    if obj and "PROMPT_ID" in obj and obj["PROMPT_ID"] != "":
        prompt_id = obj["PROMPT_ID"]
    if obj and "MENU_ID" in obj and obj["MENU_ID"] != "":
        menu_id = obj["MENU_ID"]

    if prompt_id:
        layout.operator(prompt_id,icon='WINDOW')
        if not menu_id:
            layout.separator()
    if menu_id:
        layout.menu(menu_id)
        layout.separator()

@persistent
def load_cabinet_builder_library(dummy):
    """
    Load Asset Libraries
    """
    path = cb_paths.get_active_library_path(bpy.context)
    cabinet_builder_library = cb_paths.get_cabinet_builder_asset_library(bpy.context)
    cabinet_builder_library.path = path

    mat_path = cb_paths.get_active_material_library_path(bpy.context)
    cabinet_builder_material_library = cb_paths.get_cabinet_builder_material_library(bpy.context)
    cabinet_builder_material_library.path = mat_path

def register():
    cb_props.register()
    cb_ui.register()
    cb_ops.register()

    bpy.app.handlers.load_post.append(load_cabinet_builder_library)

    bpy.types.VIEW3D_MT_object_context_menu.prepend(draw_assembly_properties)    

def unregister():
    cb_props.register()
    cb_ui.unregister()
    cb_ops.unregister()

    bpy.app.handlers.load_post.remove(load_cabinet_builder_library)
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_assembly_properties)   