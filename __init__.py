bl_info = {
    "name": "Cabinet Builder",
    "author": "Andrew Peel",
    "version": (2, 1, 15),
    "blender": (4, 1, 0),
    "location": "3D Viewport Sidebar",
    "description": "Tools for designing cabinetry to be use with Home Builder.",
    "warning": "",
    "wiki_url": "",
    "category": "Asset Library",
}

import bpy
import os
import sys
from . import cb_props
from . import cb_ops
from . import cb_ui
from . import cb_paths
from bpy.app.handlers import persistent

class External_Path(bpy.types.PropertyGroup):
    path: bpy.props.StringProperty(name="Path",description="The path to the external folder",subtype='DIR_PATH') # type: ignore

class Cabinet_Builder_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    # active_script_path: bpy.props.StringProperty(name="Active Script Path",description="The active script path",subtype='DIR_PATH') # type: ignore
    script_paths: bpy.props.CollectionProperty(type=External_Path) # type: ignore

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text="Script Libraries")
        box.operator('cabinet_builder.add_external_script_path',text="Add Script Library Path",icon='ADD')
        for script_library in self.script_paths:
            row = box.row()
            row.prop(script_library,'path',text="Path")
            row.operator('cabinet_builder.delete_script_path',text="",icon='X')

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

    obj_path = cb_paths.get_active_object_library_path(bpy.context)
    cabinet_builder_object_library = cb_paths.get_cabinet_builder_object_library(bpy.context)
    cabinet_builder_object_library.path = obj_path

@persistent
def load_script_libraries(dummy):
    cb_wm = bpy.context.window_manager.cabinet_builder
    add_on_prefs = cb_wm.get_user_preferences(bpy.context)
    for external_script in add_on_prefs.script_paths:
        if not os.path.exists(external_script.path):
            continue
        files = os.listdir(external_script.path) 
        for file in files:
            if file == '__init__.py':
                parent_folder = os.path.dirname(os.path.normpath(external_script.path))
                sys.path.append(parent_folder)
                folder = os.path.basename(os.path.normpath(external_script.path))
                mod = __import__(folder)
                if hasattr(mod,'register'):
                    #If register fails the module is already registered
                    try:
                        mod.register()
                    except:
                        pass
                    if hasattr(mod,'NAMESPACE'):
                        product_lib = cb_wm.script_libraries.add()
                        product_lib.name = folder
                        product_lib.library_path = external_script.path
                        product_lib.namespace = mod.NAMESPACE         

def register():
    bpy.utils.register_class(External_Path)
    bpy.utils.register_class(Cabinet_Builder_AddonPreferences)

    cb_props.register()
    cb_ui.register()
    cb_ops.register()

    bpy.app.handlers.load_post.append(load_cabinet_builder_library)
    bpy.app.handlers.load_post.append(load_script_libraries)

    bpy.types.VIEW3D_MT_object_context_menu.prepend(draw_assembly_properties)    

def unregister():
    bpy.utils.unregister_class(External_Path)
    bpy.utils.unregister_class(Cabinet_Builder_AddonPreferences)

    cb_props.unregister()
    cb_ui.unregister()
    cb_ops.unregister()

    bpy.app.handlers.load_post.remove(load_cabinet_builder_library)
    bpy.app.handlers.load_post.remove(load_script_libraries)

    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_assembly_properties)   