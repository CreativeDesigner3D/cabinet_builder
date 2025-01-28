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
        box.operator('cabinet_builder.set_recommended_settings')
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
        layout = self.layout

        workspace = context.workspace
        cb_scene = context.scene.cabinet_builder

        box = layout.box()
        row = box.row()
        row.label(text="Cabinet Materials")
        row.operator('cabinet_builder.assign_cabinet_materials',text="Update")
        
        col = box.column(align=True)
        row = col.row()
        row.label(text=" ")
        row.label(text="Surface")
        row.label(text="Edge")
        row = col.row(align=True)
        row.label(text="Finish")
        row.prop(cb_scene,'finished_surface_material',text="")
        row.prop(cb_scene,'finished_edge_material',text="")  
        row = col.row(align=True)
        row.label(text="Semi Exposed")
        row.prop(cb_scene,'semi_exposed_surface_material',text="")
        row.prop(cb_scene,'semi_exposed_edge_material',text="")
        row = col.row(align=True)
        row.label(text="Fronts")
        row.prop(cb_scene,'front_surface_material',text="")
        row.prop(cb_scene,'front_edge_material',text="")
        row = col.row(align=True)
        row.label(text="Unfinished")
        row.prop(cb_scene,'unfinished_surface_material',text="")
        row.prop(cb_scene,'unfinished_edge_material',text="")

        # row = col.row()
        # row.label(text="Door Edgebanding")
        # row.prop(self,'door_edgebanding',text="")

        # layout.prop(cb_scene,'finished_surface_material')

        if 'cabinet_builder_material_library' in workspace.asset_library_reference:
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
        cb_wm = context.window_manager.cabinet_builder
        add_on_prefs = cb_wm.get_user_preferences(context)
        layout = self.layout

        if cb_scene.active_script_library_name == "":
            name = "Select Library"
        else:
            name = cb_scene.active_script_library_name

        row = layout.row()
        row.scale_y = 1.3
        row.menu('CABINET_BUILDER_MT_script_library_categories',text=name)
        for script_library in cb_wm.script_libraries:
            if script_library.name == cb_scene.active_script_library_name:
                if hasattr(context.scene,script_library.namespace):
                    props = eval("context.scene." + script_library.namespace)
                    props.draw_ui(layout,context)
                else:
                    layout.label(text=script_library.namespace + " not found in scene.")


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


class CABINET_BUILDER_MT_script_library_categories(bpy.types.Menu):
    bl_label = "Script Libraries"

    def draw(self, context):
        layout = self.layout
        cb_wm = context.window_manager.cabinet_builder
        for script_library in cb_wm.script_libraries:
            layout.operator('cabinet_builder.set_active_script_path',text=script_library.name).name = script_library.name


classes = (
    CABINET_BUILDER_MT_temp_menu,
    CABINET_BUILDER_PT_cabinet_builder,
    CABINET_BUILDER_PT_cabinet_library,
    CABINET_BUILDER_PT_cabinet_materials,
    CABINET_BUILDER_PT_cabinet_objects,
    CABINET_BUILDER_PT_cabinet_scripts,
    CABINET_BUILDER_MT_library_categories,
    CABINET_BUILDER_MT_add_cabinet_part_modifier,
    CABINET_BUILDER_MT_script_library_categories
)

register, unregister = bpy.utils.register_classes_factory(classes)     