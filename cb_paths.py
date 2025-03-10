import bpy
import os

def get_cabinet_part_modifier_path():
    return os.path.join(os.path.dirname(__file__),'GeometryNodes','CabinetPartModifiers')

def get_cabinet_builder_asset_library(context):
    prefs = bpy.context.preferences
    cabinet_builder_library = prefs.filepaths.asset_libraries.get("cabinet_builder_library")
    if not cabinet_builder_library:
        cabinet_builder_library = prefs.filepaths.asset_libraries.new(name="cabinet_builder_library")
        cabinet_builder_library.name = "cabinet_builder_library"
    return cabinet_builder_library

def get_cabinet_builder_material_library(context):
    prefs = bpy.context.preferences
    cabinet_builder_material_library = prefs.filepaths.asset_libraries.get("cabinet_builder_material_library")
    if not cabinet_builder_material_library:
        cabinet_builder_material_library = prefs.filepaths.asset_libraries.new(name="cabinet_builder_material_library")
        cabinet_builder_material_library.name = "cabinet_builder_material_library"
    return cabinet_builder_material_library

def get_cabinet_builder_object_library(context):
    prefs = bpy.context.preferences
    cabinet_builder_object_library = prefs.filepaths.asset_libraries.get("cabinet_builder_object_library")
    if not cabinet_builder_object_library:
        cabinet_builder_object_library = prefs.filepaths.asset_libraries.new(name="cabinet_builder_object_library")
        cabinet_builder_object_library.name = "cabinet_builder_object_library"
    return cabinet_builder_object_library

def get_user_library_path():
    path = os.path.expanduser('~\\Documents\\Cabinet Builder Library')
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def get_active_library_path(context):
    scene_cb = context.scene.cabinet_builder
    lib_path = get_user_library_path()
    if scene_cb.active_library_category == "":
        categories = os.listdir(lib_path)
        if len(categories) > 0:
            first_category = categories[0]
            category_path = os.path.join(lib_path,first_category)
            if os.path.isdir(category_path):
                scene_cb.active_library_category = first_category
                return category_path
    else:
        active_path = os.path.join(lib_path,scene_cb.active_library_category)
        return active_path
    
def get_user_material_library_path():
    path = os.path.expanduser('~\\Documents\\Cabinet Builder Material Library')
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def get_active_material_library_path(context):
    scene_cb = context.scene.cabinet_builder
    lib_path = get_user_material_library_path()
    if scene_cb.active_material_library_category == "":
        categories = os.listdir(lib_path)
        if len(categories) > 0:
            first_category = categories[0]
            category_path = os.path.join(lib_path,first_category)
            if os.path.isdir(category_path):
                scene_cb.active_material_library_category = first_category
                return category_path
        return lib_path
    else:
        active_path = os.path.join(lib_path,scene_cb.active_material_library_category)
        return active_path    
    
def get_user_object_library_path():
    path = os.path.expanduser('~\\Documents\\Cabinet Builder Object Library')
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def get_active_object_library_path(context):
    scene_cb = context.scene.cabinet_builder
    lib_path = get_user_object_library_path()
    if scene_cb.active_object_library_category == "":
        categories = os.listdir(lib_path)
        if len(categories) > 0:
            first_category = categories[0]
            category_path = os.path.join(lib_path,first_category)
            if os.path.isdir(category_path):
                scene_cb.active_object_library_category = first_category
                return category_path
        return lib_path
    else:
        active_path = os.path.join(lib_path,scene_cb.active_object_library_category)
        return active_path  

def get_user_script_library_path():
    path = os.path.join(os.path.dirname(__file__),'Cabinet_Builder_Test_Scripts')
    if not os.path.exists(path):
        os.makedirs(path)
    return path          