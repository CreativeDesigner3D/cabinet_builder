import bpy
import math
import os
from . import cb_types, cb_unit, cb_paths

class CABINET_BUILDER_MT_temp_menu(bpy.types.Menu):
    bl_label = "Temporary Menu"

    def draw(self, context):
        layout = self.layout

class CABINET_BUILDER_PT_cabinet_builder(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Cabinet Builder"
    bl_category = "Cabinets"    
    # bl_options = {'HIDE_HEADER'}

    def draw(self, context):
        cb_scene = context.scene.cabinet_builder

        layout = self.layout

        col = layout.column(align=True)

        box = col.box()
        row = box.row()
        row.label(text="Add:",icon='ADD')
        row.operator('cabinet_builder.add_cabinet_container',text="Container")

        obj = context.object
        if obj:
            container = None
            if 'IS_GeoNodeContainer' in obj:
                container = obj
            elif obj.parent and 'IS_GeoNodeContainer' in obj.parent:
                container = obj.parent

            if container:
                container = cb_types.GeoNodeContainer(container)
                container.draw_ui(col,context)



class CABINET_BUILDER_PT_cabinet_materials(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Cabinet Materials"
    bl_category = "Cabinets"    
    # bl_options = {'HIDE_HEADER'}

    def draw(self, context):
        cb_scene = context.scene.cabinet_builder

        layout = self.layout
        layout.prop(cb_scene,'finished_surface_material')

        workspace = context.workspace
        wm = context.window_manager 
        workspace.asset_library_reference = 'cabinet_builder_material_library'
        activate_op_props, drag_op_props = layout.template_asset_view(
            'cabinet_builder_material_library',
            workspace,
            "asset_library_reference",
            wm.cabinet_builder,
            "cabinet_builder_material_assets",
            wm.cabinet_builder,
            'cabinet_builder_material_index',
            # filter_id_types={"filter_object"},
            display_options={'NO_LIBRARY'},
            # display_options={'NO_FILTER','NO_LIBRARY'},
            activate_operator='cabinet_builder.click_library_item',
            drag_operator='cabinet_builder.drop_material',            
        )        


class CABINET_BUILDER_PT_cabinet_library(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Cabinet Library"
    bl_category = "Cabinets"    
    # bl_options = {'HIDE_HEADER'}

    def draw(self, context):
        cb_scene = context.scene.cabinet_builder

        layout = self.layout

        layout.menu('CABINET_BUILDER_MT_library_categories',text=cb_scene.active_library_category)
        layout.operator('cabinet_builder.save_cabinet')

        workspace = context.workspace
        wm = context.window_manager 
        workspace.asset_library_reference = 'cabinet_builder_library'
        activate_op_props, drag_op_props = layout.template_asset_view(
            'cabinet_builder_library',
            workspace,
            "asset_library_reference",
            wm.cabinet_builder,
            "cabinet_builder_library_assets",
            wm.cabinet_builder,
            'cabinet_builder_library_index',
            # filter_id_types={"filter_object"},
            display_options={'NO_LIBRARY'},
            # display_options={'NO_FILTER','NO_LIBRARY'},
            activate_operator='cabinet_builder.click_library_item',
            drag_operator='cabinet_builder.drag_library_item',            
        )
        

class CABINET_BUILDER_PT_cabinet_objects(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Cabinet Objects"
    bl_category = "Cabinets"    
    # bl_options = {'HIDE_HEADER'}

    def draw(self, context):
        cb_scene = context.scene.cabinet_builder

        layout = self.layout

        workspace = context.workspace
        wm = context.window_manager 
        workspace.asset_library_reference = 'cabinet_builder_object_library'
        activate_op_props, drag_op_props = layout.template_asset_view(
            'cabinet_builder_object_library',
            workspace,
            "asset_library_reference",
            wm.cabinet_builder,
            "cabinet_builder_object_assets",
            wm.cabinet_builder,
            'cabinet_builder_object_index',
            # filter_id_types={"filter_object"},
            display_options={'NO_LIBRARY'},
            # display_options={'NO_FILTER','NO_LIBRARY'},
            activate_operator='cabinet_builder.click_library_item',
            drag_operator='cabinet_builder.drop_object',            
        )        


class CABINET_BUILDER_PT_cabinet_scripts(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Cabinet Scripts"
    bl_category = "Cabinets"    
    # bl_options = {'HIDE_HEADER'}

    def draw(self, context):
        cb_scene = context.scene.cabinet_builder

        layout = self.layout

        script_path = cb_paths.get_user_script_library_path()
        script_files = os.listdir(script_path)
        for script_file in script_files:
            file_name, file_ext = os.path.splitext(script_file)
            if file_ext == '.py':
                script_path = os.path.join(script_path,script_file)
                layout.operator('cabinet_builder.draw_class_from_script',text=file_name).script_path = script_path


class CABINET_BUILDER_MT_library_categories(bpy.types.Menu):
    bl_label = "Custom User Library Categories"

    def draw(self, context):
        user_library_path = cb_paths.get_user_library_path()

        layout = self.layout

        user_folders = os.listdir(user_library_path)
        for folder in user_folders:
            folder_path = os.path.join(user_library_path,folder)
            if os.path.isdir(folder_path):
                layout.operator('cabinet_builder.change_library_category',text=folder).category_path = folder_path

        layout.separator()
        layout.operator('cabinet_builder.add_user_library_category',text="Add New Category",icon='ADD')


class CABINET_BUILDER_MT_add_cabinet_part_modifier(bpy.types.Menu):
    bl_label = "Add Cabinet Part Modifier"

    def draw(self, context):
        layout = self.layout
        path = cb_paths.get_cabinet_part_modifier_path()
        tokens = os.listdir(path)
        for token_file in tokens:
            filename, ext = os.path.splitext(token_file)
            if ext == '.blend':
                layout.operator('cabinet_builder.add_cabinet_part_modifier',text=filename).modifier_type = filename

classes = (
    CABINET_BUILDER_MT_temp_menu,
    CABINET_BUILDER_PT_cabinet_builder,
    CABINET_BUILDER_PT_cabinet_library,
    CABINET_BUILDER_PT_cabinet_materials,
    CABINET_BUILDER_PT_cabinet_objects,
    CABINET_BUILDER_PT_cabinet_scripts,
    CABINET_BUILDER_MT_library_categories,
    CABINET_BUILDER_MT_add_cabinet_part_modifier
)

register, unregister = bpy.utils.register_classes_factory(classes)     