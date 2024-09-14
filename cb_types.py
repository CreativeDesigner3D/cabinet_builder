import bpy
import os
import math
import rna_prop_ui
from . import cb_unit

GEO_NODE_PATH = os.path.join(os.path.dirname(__file__),'GeometryNodes')

class GeoNodeMeshObject():
    obj = None
    mod = None

    def __init__(self,obj=None):
        if obj:
            self.obj = obj
            for mod in self.obj.modifiers:
                if mod.type == 'NODES':
                    self.mod = mod
                    break    

    def get_geo_node(self,path,geo_node_name):
        '''
            This will get a geometry node group. If the group is already
            in the data it will use that group and assign it to a new mesh
            object.
        '''
        if geo_node_name in bpy.data.node_groups:
            node = bpy.data.node_groups[geo_node_name]
            cage = bpy.data.meshes.new(geo_node_name)
            self.obj = bpy.data.objects.new(geo_node_name,cage)
            self.mod = self.obj.modifiers.new('GeometryNodes','NODES')
            self.mod.node_group = node
        else:
            with bpy.data.libraries.load(path) as (data_from, data_to):
                data_to.objects = data_from.objects
            for obj in data_to.objects:
                self.obj = obj
            self.obj.name = geo_node_name
            for mod in self.obj.modifiers:
                if mod.type == 'NODES':
                    self.mod = mod
                    break  

    def set_input(self,name,value=None):
        '''
            This allows you to set an input on a geometry node group
            based on the name
        '''
        if name in self.mod.node_group.interface.items_tree:
            node_input = self.mod.node_group.interface.items_tree[name]    
            self.mod.node_group.interface_update(bpy.context)
            if hasattr(node_input,'subtype'):
                node_input.subtype = node_input.subtype            
            exec('self.mod["' + node_input.identifier + '"] = value')    

    def get_input(self,name):
        '''
            This gets a value from a geometry node group input
            based on the name
        '''        
        if name in self.mod.node_group.interface.items_tree:
            node_input = self.mod.node_group.interface.items_tree[name]
            return eval('self.mod["' + node_input.identifier + '"]')

    def draw_input(self,layout,name,text,icon=''):
        '''
            This draws a geometry node group input on a blender ui layout
        '''
        if name in self.mod.node_group.interface.items_tree:
            node_input = self.mod.node_group.interface.items_tree[name]
            if icon == '':
                layout.prop(self.mod,'["' + node_input.identifier + '"]',text=text)
            else:
                layout.prop(self.mod,'["' + node_input.identifier + '"]',text=text,icon=icon)

    def draw_transform_ui(self,layout):
        col1 = layout.row()
        col2 = col1.split()
        col = col2.column(align=True)
        col.label(text='Location:')
        #X
        row = col.row(align=True)
        row.prop(self.obj,"lock_location",index=0,text="")
        if self.obj.lock_location[0]:
            row.label(text="X: " + str(round(cb_unit.meter_to_active_unit(self.obj.location.x),4)))
        else:
            row.prop(self.obj,"location",index=0,text="X")
        #Y    
        row = col.row(align=True)
        row.prop(self.obj,"lock_location",index=1,text="")
        if self.obj.lock_location[1]:
            row.label(text="Y: " + str(round(cb_unit.meter_to_active_unit(self.obj.location.y),4)))
        else:
            row.prop(self.obj,"location",index=1,text="Y")
        #Z    
        row = col.row(align=True)
        row.prop(self.obj,"lock_location",index=2,text="")
        if self.obj.lock_location[2]:
            row.label(text="Z: " + str(round(cb_unit.meter_to_active_unit(self.obj.location.z),4)))
        else:
            row.prop(self.obj,"location",index=2,text="Z")
            
        col2 = col1.split()
        col = col2.column(align=True)
        col.label(text='Rotation:')
        #X
        row = col.row(align=True)
        row.prop(self.obj,"lock_rotation",index=0,text="")
        if self.obj.lock_rotation[0]:
            row.label(text="X: " + str(round(math.degrees(self.obj.rotation_euler.x),4)))
        else:
            row.prop(self.obj,"rotation_euler",index=0,text="X")
        #Y    
        row = col.row(align=True)
        row.prop(self.obj,"lock_rotation",index=1,text="")
        if self.obj.lock_rotation[1]:
            row.label(text="Y: " + str(round(math.degrees(self.obj.rotation_euler.y),4)))
        else:
            row.prop(self.obj,"rotation_euler",index=1,text="Y")
        #Z    
        row = col.row(align=True)
        row.prop(self.obj,"lock_rotation",index=2,text="")
        if self.obj.lock_rotation[2]:
            row.label(text="Y: " + str(round(math.degrees(self.obj.rotation_euler.z),4)))
        else:
            row.prop(self.obj,"rotation_euler",index=2,text="Z")  


class GeoNodeContainer(GeoNodeMeshObject):
    
    def create(self,name="Container"):
        class_name = self.__class__.__name__
        path = os.path.join(GEO_NODE_PATH,class_name + ".blend")
        self.get_geo_node(path,class_name)
        self.obj['IS_GeoNodeContainer'] = True
        self.obj.name = name
        self.obj.hide_render = True
        self.coll = bpy.context.view_layer.active_layer_collection.collection
        self.coll.objects.link(self.obj)
        self.obj.display.show_shadows = False
        self.obj.display_type = 'WIRE'
        self.obj.color = (0,0,0,1)
        self.obj.visible_camera = False
        self.obj.visible_shadow = False
        self.obj.hide_probe_volume = False
        self.obj.hide_probe_sphere = False
        self.obj.hide_probe_plane = False

    def draw_ui(self,layout,context):
        scene_cb = context.scene.cabinet_builder

        box = layout.box()
        row = box.row()
        row.label(text="Active Container: " + self.obj.name)
        row = box.row()
        row.prop(scene_cb,'selected_tabs',expand=True)
        
        if scene_cb.selected_tabs == 'MAIN':
            col = box.column(align=True)
            row = col.row(align=True)
            self.draw_input(row,'Dim X',text="Dim X")
            self.draw_input(row,'Mirror X',text="",icon='MOD_MIRROR')
            row = col.row(align=True)
            self.draw_input(row,'Dim Y',text="Dim Y")
            self.draw_input(row,'Mirror Y',text="",icon='MOD_MIRROR')
            row = col.row(align=True)
            self.draw_input(row,'Dim Z',text="Dim Z")
            self.draw_input(row,'Mirror Z',text="",icon='MOD_MIRROR')
            self.draw_transform_ui(box)

        if scene_cb.selected_tabs == 'PROPERTIES':
            box.operator('cabinet_builder.add_property').obj_name = self.obj.name
            items = list(self.obj.items())
            for key, value in items:
                if str(type(value)) != "<class 'IDPropertyGroup'>":
                    pm = self.obj.id_properties_ui(key)
                    rna_data = pm.as_dict()
                    description = rna_data.get("description", "")  
                    if 'CABINET_BUILDER_PROP' in description:                              
                        row = box.row()
                        row.label(text=key)
                        row.prop(self.obj, rna_prop_ui.rna_idprop_quote_path(key), text="")
                        props = row.operator("wm.properties_edit", text="", icon='PREFERENCES', emboss=False)
                        props.data_path = 'object'
                        props.property_name = key
                        props = row.operator("wm.properties_remove", text="", icon='X', emboss=False)
                        props.data_path = 'object'
                        props.property_name = key

        if scene_cb.selected_tabs == 'CHILDREN':
            row = box.row()
            row.label(text="Add")
            row.operator('cabinet_builder.add_cabinet_part',text="Cabinet Part").parent_name = self.obj.name
            row = box.row()
            row.prop(scene_cb,'children_tabs',expand=True)
            if scene_cb.children_tabs == 'SHOW_SELECTED':
                obj = context.object
                col = box.column(align=True)
                if obj and 'IS_GeoNodeCabinetPart' in obj:
                    part = GeoNodeCabinetPart(obj)
                    part.draw_ui(col,context)
            else:
                mesh_col = box.column(align=True)
                for child in self.obj.children:
                    row = mesh_col.row(align=True)
                    if child == context.object:
                        icon = 'RADIOBUT_ON'
                        # row.label(text="",icon='RADIOBUT_ON')
                    elif child in context.selected_objects:
                        icon = 'DECORATE'
                        # row.label(text="",icon='DECORATE')
                    else:
                        icon = 'RADIOBUT_OFF'
                        # row.label(text="",icon='RADIOBUT_OFF')
                    row.operator('cabinet_builder.select_object',text=child.name,icon=icon).obj_name = child.name
                    row.prop(child.cabinet_builder,'expand_object_info',text="",icon='DISCLOSURE_TRI_DOWN' if child.cabinet_builder.expand_object_info else 'DISCLOSURE_TRI_RIGHT')
                    if child.cabinet_builder.expand_object_info:
                        part = GeoNodeCabinetPart(child)
                        part.draw_ui(mesh_col,context)                        
                        # row = mesh_col.row()
                        # row.label(text="",icon='BLANK1')
                        # col = row.column(align=True)
                        # box = col.box()
                        # row = box.row()
                        # row.prop(context.scene.pyclone,'object_tabs',expand=True)
                        # box = col.box()
                        # draw_object_properties(context,box,child)

                # col = box.column(align=True)
                # for child in self.obj.children:
                #     if 'IS_GeoNodeCabinetPart' in child:
                #         part = GeoNodeCabinetPart(child)
                #         part.draw_ui(col,context)

        if scene_cb.selected_tabs == 'DRIVERS':
            obj = context.object
            row = box.row()
            row.label(text="Current Object:" + obj.name)
            row.prop(scene_cb,'variable_object',text="",icon='DRIVER')
            drivers = obj.cabinet_builder.get_drivers()
            for driver in drivers:
                obj.cabinet_builder.draw_driver(box,context,driver)
                # box.label(text="Driver: " + driver.data_path)


class GeoNodeCabinetPart(GeoNodeMeshObject):
    
    def create(self,name="Cabinet Part"):
        class_name = self.__class__.__name__
        path = os.path.join(GEO_NODE_PATH,class_name + ".blend")
        self.get_geo_node(path,class_name)
        self.obj['IS_GeoNodeCabinetPart'] = True
        self.obj.name = name       
        self.obj.color = (1,1,1,1)
        bpy.context.view_layer.active_layer_collection.collection.objects.link(self.obj)

    def draw_ui(self,layout,context):
        box = layout.box()
        row = box.row()
        row.label(text="Part Name:")
        row.prop(self.obj,'name',text="")
        col = box.column(align=True)
        row = col.row(align=True)
        self.draw_input(row,'Length',text="Length")
        self.draw_input(row,'Mirror X',text="",icon='MOD_MIRROR')
        row = col.row(align=True)
        self.draw_input(row,'Width',text="Width")
        self.draw_input(row,'Mirror Y',text="",icon='MOD_MIRROR')
        row = col.row(align=True)
        self.draw_input(row,'Thickness',text="Thickness")
        self.draw_input(row,'Mirror Z',text="",icon='MOD_MIRROR')

        self.draw_transform_ui(box)

      