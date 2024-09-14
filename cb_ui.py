import bpy
import math
from . import cb_types, cb_unit

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

                # if obj and 'IS_GeoNodeContainer' in obj:
  

                # if obj and 'IS_GeoNodeCabinetPart' in obj:
                #     part = cb_types.GeoNodeCabinetPart(obj)
                #     part.draw_ui(col,context)


classes = (
    CABINET_BUILDER_MT_temp_menu,
    CABINET_BUILDER_PT_main_panel,
)

register, unregister = bpy.utils.register_classes_factory(classes)     