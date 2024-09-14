import bpy
import math
import os
from . import cb_types, cb_unit, cb_paths

class CABINET_BUILDER_MT_temp_menu(bpy.types.Menu):
    bl_label = "Temporary Menu"

    def draw(self, context):
        layout = self.layout

class CABINET_BUILDER_PT_main_panel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Cabinet Builder"
    bl_category = "Cabinets"    
    # bl_options = {'HIDE_HEADER'}

    def draw(self, context):
        cb_scene = context.scene.cabinet_builder

        layout = self.layout

        col = layout.column(align=True)
        row = col.row(align=True)
        row.scale_y = 1.3
        row.prop_enum(cb_scene, "main_tabs", 'BUILD', icon='MOD_BUILD') #MOD_EDGESPLIT
        row.prop_enum(cb_scene, "main_tabs", 'LIBRARY', icon='ASSET_MANAGER') 

        if cb_scene.main_tabs == 'BUILD':
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

        else:

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


classes = (
    CABINET_BUILDER_MT_temp_menu,
    CABINET_BUILDER_PT_main_panel,
    CABINET_BUILDER_MT_library_categories,
)

register, unregister = bpy.utils.register_classes_factory(classes)     