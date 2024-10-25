import bpy
import os
import math
import rna_prop_ui
from . import cb_unit, cb_utils, cb_paths

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

    def get_var_input(self,input_name,name):
        node = self.mod.node_group      
        input_identifier = "" 
        for input in node.interface.items_tree:
            if input.name == input_name:
                input_identifier = input.identifier
                break        
        data_path = 'modifiers["' + self.mod.name + '"]["' + input_identifier + '"]'
        return self.obj.cabinet_builder.get_var(data_path,name)
    
    def get_var_prop(self,name,var_name):
        return self.obj.cabinet_builder.get_var('["' + name + '"]',var_name)

    def draw_input(self,layout,name,text,icon=''):
        '''
            This draws a geometry node group input on a blender ui layout
        '''
        if name in self.mod.node_group.interface.items_tree:
            node_input = self.mod.node_group.interface.items_tree[name]
            if str(node_input.socket_type) == 'NodeSocketMaterial':
                layout.prop_search(self.mod,'["' + node_input.identifier + '"]',bpy.data,'materials',text=text)
            else:
                if icon == '':
                    layout.prop(self.mod,'["' + node_input.identifier + '"]',text=text)
                else:
                    layout.prop(self.mod,'["' + node_input.identifier + '"]',text=text,icon=icon)

    def driver_input(self,name,expression="",variables=[]):
        input_identifier = ""
        if name in self.mod.node_group.interface.items_tree:
            node_input = self.mod.node_group.interface.items_tree[name]  
            input_identifier = node_input.identifier
        driver = self.obj.driver_add('modifiers["' + self.mod.name + '"]["' + input_identifier + '"]')
        self.obj.cabinet_builder.add_driver_variables(driver,variables)
        driver.driver.expression = expression

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
        self.obj['PROMPT_ID'] = "cabinet_builder.container_prompts"
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
            add_box = box.box()
            row = add_box.row()
            row.label(text="Add")
            row.operator('cabinet_builder.add_cabinet_part',text="Cabinet Part").parent_name = self.obj.name
            row.operator('cabinet_builder.add_object',text="Object").parent_name = self.obj.name
            row.operator('cabinet_builder.add_opening',text="Opening").parent_name = self.obj.name
            row = box.row()
            row.prop(scene_cb,'children_tabs',expand=True)
            if scene_cb.children_tabs == 'SHOW_SELECTED':
                obj = context.object
                col = box.column(align=True)
                if obj and 'IS_GeoNodeCabinetPart' in obj:
                    part = GeoNodeCabinetPart(obj)
                    part.draw_ui(col,context)
                if obj and 'IS_GeoNodeObject' in obj:
                    part = GeoNodeObject(obj)
                    part.draw_ui(col,context)
            else:
                mesh_col = box.column(align=True)
                for child in self.obj.children:
                    row = mesh_col.row(align=True)
                    if child == context.object:
                        icon = 'RADIOBUT_ON'
                    elif child in context.selected_objects:
                        icon = 'DECORATE'
                    else:
                        icon = 'RADIOBUT_OFF'
                    row.operator('cabinet_builder.select_object',text=child.name,icon=icon).obj_name = child.name
                    row.prop(child.cabinet_builder,'expand_object_info',text="",icon='DISCLOSURE_TRI_DOWN' if child.cabinet_builder.expand_object_info else 'DISCLOSURE_TRI_RIGHT')
                    if child.cabinet_builder.expand_object_info:
                        if child and 'IS_GeoNodeCabinetPart' in child:
                            part = GeoNodeCabinetPart(child)
                            part.draw_ui(mesh_col,context)                        
                        if child and 'IS_GeoNodeObject' in child:
                            part = GeoNodeObject(child)
                            part.draw_ui(mesh_col,context)

        if scene_cb.selected_tabs == 'DRIVERS':
            obj = context.object
            row = box.row()
            row.label(text="Current Object:" + obj.name)
            row.prop(scene_cb,'variable_object',text="",icon='DRIVER')
            drivers = obj.cabinet_builder.get_drivers()
            for driver in drivers:
                obj.cabinet_builder.draw_driver(box,context,driver)
                # box.label(text="Driver: " + driver.data_path)


class GeoNodeObject(GeoNodeMeshObject):

    geo_node_name = "GeoNodeHardware"

    mod = None
    coll = None

    def create(self,name=""):
        class_name = self.__class__.__name__
        path = os.path.join(GEO_NODE_PATH,class_name + ".blend")
        self.get_geo_node(path,class_name)                
        self.obj.name = name
        self.obj["IS_GeoNodeObject"] = class_name
        self.mod.node_group.interface_update(bpy.context)
        bpy.context.view_layer.active_layer_collection.collection.objects.link(self.obj)
        self.obj.color = (.5,.5,.5,1)

    def get_geo_object_from_name(self,obj,name):
        self.obj = obj
        for mod in self.obj.modifiers:
            if mod.type == 'NODES' and mod.name == name:
                self.mod = mod
                break     

    def draw_ui(self,layout,context):
        scene_cb = context.scene.cabinet_builder

        box = layout.box()
        row = box.row()
        row.label(text="Part Name:")
        row.prop(self.obj,'name',text="")
        self.draw_input(box,'Object',text="Object")

        self.draw_transform_ui(box) 


class GeoNodeCabinetPart(GeoNodeMeshObject):
    
    def create(self,name="Cabinet Part"):
        class_name = self.__class__.__name__
        path = os.path.join(GEO_NODE_PATH,class_name + ".blend")
        self.get_geo_node(path,class_name)
        self.obj['IS_GeoNodeCabinetPart'] = True
        self.obj.name = name       
        self.obj.color = (1,1,1,1)
        bpy.context.view_layer.active_layer_collection.collection.objects.link(self.obj)
        pb = cb_utils.get_particle_board_material()
        self.set_input('Top Surface',pb)
        self.set_input('Bottom Surface',pb)
        self.set_input('Edge W1',pb)
        self.set_input('Edge W2',pb)
        self.set_input('Edge L1',pb)
        self.set_input('Edge L2',pb)
    
    def draw_ui(self,layout,context):
        scene_cb = context.scene.cabinet_builder

        box = layout.box()
        row = box.row()
        row.label(text="Part Name:")
        row.prop(self.obj,'name',text="")

        row = box.row()
        row.prop(scene_cb,'selected_object_tabs',expand=True)

        if scene_cb.selected_object_tabs == 'MAIN':
            # row.label(text="",icon='BLANK1')
                    
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

        if scene_cb.selected_object_tabs == 'MATERIALS':
            col = box.column(align=True)
            self.draw_input(col,'Top Surface',text="Top Surface")   
            self.draw_input(col,'Bottom Surface',text="Bottom Surface") 
            self.draw_input(col,'Edge W1',text="Edge W1") 
            self.draw_input(col,'Edge W2',text="Edge W2") 
            self.draw_input(col,'Edge L1',text="Edge L1") 
            self.draw_input(col,'Edge L2',text="Edge L2") 

        if scene_cb.selected_object_tabs == 'MODIFIERS':
            col = box.column(align=True)
            col.label(text="Add Modifier")
            col.menu('CABINET_BUILDER_MT_add_cabinet_part_modifier')

            for mod in self.obj.modifiers:
                if mod.type == 'NODES':
                    node = mod.node_group
                    if 'CPM_' in node.name:
                        cpm = CabinetPartModifier(self.obj,mod)
                        cpm.draw_ui(col,self)

class CabinetPartModifier(GeoNodeMeshObject):
    
    obj = None
    mod = None
    node_group = None

    def __init__(self,obj=None,mod=None):
        if obj:
            self.obj = obj
            if mod:
                self.mod = mod
                self.node_group = mod.node_group            

    def get_node(self,token_type):
        path = cb_paths.get_cabinet_part_modifier_path()
        token_path = os.path.join(path,token_type + ".blend")

        if token_type in bpy.data.node_groups:
            return bpy.data.node_groups[token_type]

        if os.path.exists(token_path):

            with bpy.data.libraries.load(token_path) as (data_from, data_to):
                for ng in data_from.node_groups:
                    if ng == token_type:
                        data_to.node_groups = [ng]
                        break    
            
            for ng in data_to.node_groups:
                return ng    

    def add_node(self,token_type,token_name):
        node_group = self.get_node(token_type)
        self.mod = self.obj.modifiers.new(name=token_name,type='NODES')
        self.mod.node_group = node_group
        self.node_group = node_group
        self.mod.show_expanded = False

    def draw_ui(self,layout,part):
        token_type = self.node_group.name.replace("CPM_","")
        t_box = layout.box()
        row = t_box.row()
        row.prop(self.mod,'show_expanded',text="",emboss=False)
        row.label(text=token_type)
        row.prop(self.mod,'name',text="")
        row.prop(self.mod,'show_viewport',text="",emboss=False)
        row.operator('cabinet_builder.remove_cabinet_part_modifier',text="",icon='X',emboss=False).modifier_name = self.mod.name
        if self.mod.show_expanded:
            for n_input in self.node_group.interface.items_tree:
                if n_input.identifier in self.mod:
                    t_box.prop(self.mod,'["' + n_input.identifier + '"]',text=n_input.name)#                    