import bpy
import os
import subprocess
import codecs
from mathutils import Vector
from . import cb_types, cb_unit, cb_paths, cb_snap
from rna_prop_ui import rna_idprop_quote_path

class cabinet_builder_OT_temp_operator(bpy.types.Operator):
    bl_idname = "cabinet_builder.temp_operator"
    bl_label = "Temp Operator"
    bl_description = "Temp Operator"

    temp_prop: bpy.props.StringProperty(name="Temp Property")# type: ignore

    def invoke(self,context,event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=500)

    def execute(self, context):  
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout


class cabinet_builder_OT_container_prompts(bpy.types.Operator):
    bl_idname = "cabinet_builder.container_prompts"
    bl_label = "Container Prompts"
    bl_description = "This will show the container prompts"

    container = None

    def invoke(self,context,event):
        self.container = cb_types.GeoNodeContainer(context.object)
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=300)

    def execute(self, context):  
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        self.container.draw_ui(layout,context)


class cabinet_builder_OT_add_cabinet_container(bpy.types.Operator):
    bl_idname = "cabinet_builder.add_cabinet_container"
    bl_label = "Add Cabinet Container"
    bl_description = "This will add a cabinet container"

    cabinet_name: bpy.props.StringProperty(name="Cabinet Name")# type: ignore

    container_width: bpy.props.FloatProperty(name="Container Width",
                                             description="Default container width",
                                             default=cb_unit.inch(18.0),
                                             unit='LENGTH')# type: ignore
    
    container_height: bpy.props.FloatProperty(name="Container Height",
                                             description="Default container height",
                                             default=cb_unit.inch(34.0),
                                             unit='LENGTH')# type: ignore    

    container_depth: bpy.props.FloatProperty(name="Container Depth",
                                             description="Default container depth",
                                             default=cb_unit.inch(24.0),
                                             unit='LENGTH')# type: ignore   
    
    mirror_y: bpy.props.BoolProperty(name="Mirror Y",
                                     description="Mirror the Y Dimension of the cabinet",
                                     default=True)# type: ignore   
    
    def invoke(self,context,event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=300)

    def execute(self, context):  
        container = cb_types.GeoNodeContainer()
        container.create(self.cabinet_name)
        container.set_input('Dim X',self.container_width)
        container.set_input('Dim Y',self.container_depth)
        container.set_input('Dim Z',self.container_height)
        container.set_input('Mirror Y',self.mirror_y)
        context.view_layer.objects.active = container.obj
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.prop(self,'cabinet_name')
        layout.prop(self,'container_width')
        layout.prop(self,'container_height')
        layout.prop(self,'container_depth')
        layout.prop(self,'mirror_y')


class cabinet_builder_OT_add_cabinet_part(bpy.types.Operator):
    bl_idname = "cabinet_builder.add_cabinet_part"
    bl_label = "Add Cabinet Part"
    bl_description = "This will add a cabinet part"

    parent_name: bpy.props.StringProperty(name="Parent Name")# type: ignore

    part_name: bpy.props.StringProperty(name="Part Name")# type: ignore

    part_length: bpy.props.FloatProperty(name="Part Length",
                                             description="Default part length",
                                             default=cb_unit.inch(34.0),
                                             unit='LENGTH')# type: ignore
    
    part_thickness: bpy.props.FloatProperty(name="Part Thickness",
                                             description="Default part thickness",
                                             default=cb_unit.inch(.75),
                                             unit='LENGTH')# type: ignore    

    part_width: bpy.props.FloatProperty(name="Part Width",
                                             description="Default part width",
                                             default=cb_unit.inch(18.0),
                                             unit='LENGTH')# type: ignore   
    

    def invoke(self,context,event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=300)

    def execute(self, context):  
        if self.parent_name == "":
            parent = None
        else:
            parent = bpy.data.objects[self.parent_name]
        part = cb_types.GeoNodeCabinetPart()
        part.create(self.part_name)
        part.obj.parent = parent
        part.set_input('Length',self.part_length)
        part.set_input('Width',self.part_width)
        part.set_input('Thickness',self.part_thickness)
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.prop(self,'part_name')
        layout.prop(self,'part_length')
        layout.prop(self,'part_width')
        layout.prop(self,'part_thickness')


class cabinet_builder_OT_add_opening(bpy.types.Operator):
    bl_idname = "cabinet_builder.add_opening"
    bl_label = "Add Opening"
    bl_description = "This will add an opening"

    parent_name: bpy.props.StringProperty(name="Parent Name")# type: ignore

    opening_name: bpy.props.StringProperty(name="Opening Name")# type: ignore

    opening_width: bpy.props.FloatProperty(name="Opening Width",
                                             description="Default opening width",
                                             default=cb_unit.inch(18.0),
                                             unit='LENGTH')# type: ignore
    
    opening_height: bpy.props.FloatProperty(name="Opening Height",
                                             description="Default opening height",
                                             default=cb_unit.inch(34.0),
                                             unit='LENGTH')# type: ignore    

    opening_depth: bpy.props.FloatProperty(name="Opening Depth",
                                             description="Default opening depth",
                                             default=cb_unit.inch(24.0),
                                             unit='LENGTH')# type: ignore    
    

    def invoke(self,context,event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=300)

    def execute(self, context):  
        if self.parent_name == "":
            parent = None
        else:
            parent = bpy.data.objects[self.parent_name]
        part = cb_types.GeoNodeContainer()
        part.create(self.opening_name)
        part.obj.parent = parent
        part.set_input('Dim X',self.opening_width)
        part.set_input('Dim Y',self.opening_depth)
        part.set_input('Dim Z',self.opening_height)
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.prop(self,'opening_name')
        layout.prop(self,'opening_width')
        layout.prop(self,'opening_height')
        layout.prop(self,'opening_depth')


class cabinet_builder_OT_add_property(bpy.types.Operator):
    bl_idname = "cabinet_builder.add_property"
    bl_label = "Add Property"
    bl_description = "Add Property"

    obj_name: bpy.props.StringProperty(name="Object Name")# type: ignore

    property_name: bpy.props.StringProperty(name="Property Name")# type: ignore

    property_type: bpy.props.EnumProperty(name="Property Type",
                          items=[('FLOAT',"Float","A Number Value"),
                                 ('DISTANCE',"Distance","A Distance Value"),
                                 ('INTEGER',"Integer","An Integer Value"),
                                 ('ANGLE',"Angle","An Angle Value"),
                                 ('CHECKBOX',"Checkbox","A Checkbox Value"),
                                 ('COMBOBOX',"Combo Box","A Combo Box Drop Down"),
                                 ('PERCENTAGE',"Percentage","A Percentage Value"),
                                 ('STRING',"String","A String Value")],
                          default='DISTANCE')# type: ignore 
    
    float_value: bpy.props.FloatProperty(name="Float Value")# type: ignore
    angle_value: bpy.props.FloatProperty(name="Angle Value",subtype='ANGLE')# type: ignore
    int_value: bpy.props.IntProperty(name="Int Value")# type: ignore
    distance_value: bpy.props.FloatProperty(name="Float Value",unit='LENGTH')# type: ignore
    checkbox_value: bpy.props.BoolProperty(name="Checkbox Value")# type: ignore
    percentage_value: bpy.props.FloatProperty(name="Percentage Value",subtype='PERCENTAGE',min=0,max=100)# type: ignore
    text_value: bpy.props.StringProperty(name="Text Value", description="")# type: ignore

    def invoke(self,context,event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=300)

    def execute(self, context):  
        obj = bpy.data.objects[self.obj_name]
        
        if self.property_type == 'CHECKBOX':
            obj[self.property_name] = self.checkbox_value
            obj.id_properties_ensure()
            pm = obj.id_properties_ui(self.property_name)
            pm.update(description='CABINET_BUILDER_PROP')

        if self.property_type == 'DISTANCE':
            obj[self.property_name] = self.distance_value
            obj.id_properties_ensure()
            pm = obj.id_properties_ui(self.property_name)
            pm.update(subtype='DISTANCE',description='CABINET_BUILDER_PROP')

        if self.property_type == 'COMBOBOX':
            obj[self.property_name] = self.int_value
            cb_list = []
            tup_item_1 = ("Item 1","Item 1",'Item 1')
            tup_item_2 = ("Item 2","Item 2",'Item 2')
            tup_item_3 = ("Item 3","Item 3",'Item 3')
            cb_list.append(tup_item_1)
            cb_list.append(tup_item_2)
            cb_list.append(tup_item_3)
            pm = obj.id_properties_ui(self.property_name)
            pm.update(description='CABINET_BUILDER_PROP',items=cb_list)
            # pm.update(items=cb_list)

        #This seems to fix issue with property not evaluating in formulas with refresh
        obj.location = obj.location
        obj.id_properties_ensure()

        context.area.tag_redraw()       
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.prop(self,'property_name')
        layout.prop(self,'property_type')
        if self.property_type == 'FLOAT':
            layout.prop(self,'float_value')
        if self.property_type == 'DISTANCE':
            layout.prop(self,'distance_value')
        if self.property_type == 'INTEGER':
            layout.prop(self,'int_value')            
        if self.property_type == 'ANGLE':
            layout.prop(self,'angle_value')
        if self.property_type == 'CHECKBOX':
            layout.prop(self,'checkbox_value')
        if self.property_type == 'COMBOBOX':
            layout.prop(self,'int_value')
        if self.property_type == 'PERCENTAGE':
            layout.prop(self,'percentage_value')
        if self.property_type == 'STRING':
            layout.prop(self,'text_value')   


class Variables(bpy.types.PropertyGroup):
    add: bpy.props.BoolProperty(name="Add") # type: ignore
    identifier: bpy.props.StringProperty(name="Identifier") # type: ignore


class cabinet_builder_OT_get_vars_from_object(bpy.types.Operator):
    bl_idname = "cabinet_builder.get_vars_from_object"
    bl_label = "Quick Variables"
    bl_description = "This gets the available variables from an object"
    bl_options = {'UNDO'}
    
    object_name: bpy.props.StringProperty(name='Object Name') # type: ignore
    data_path: bpy.props.StringProperty(name='Data Path') # type: ignore
    array_index: bpy.props.IntProperty(name='Array Index') # type: ignore
    
    x_loc: bpy.props.BoolProperty(name='X Location',default=False) # type: ignore
    y_loc: bpy.props.BoolProperty(name='Y Location',default=False) # type: ignore
    z_loc: bpy.props.BoolProperty(name='Z Location',default=False) # type: ignore
    x_rot: bpy.props.BoolProperty(name='X Rotation',default=False) # type: ignore
    y_rot: bpy.props.BoolProperty(name='Y Rotation',default=False) # type: ignore
    z_rot: bpy.props.BoolProperty(name='Z Rotation',default=False) # type: ignore
    
    geo_inputs: bpy.props.CollectionProperty(name='Geo Node Inputs',type=Variables) # type: ignore
    properties: bpy.props.CollectionProperty(name='Collection Properties',type=Variables) # type: ignore
    
    obj = None
    assembly = None
    cage = None
    mod_name = ""
    
    @classmethod
    def poll(cls, context):
        if context.scene.cabinet_builder.variable_object:
            return True
        else:
            return False

    def get_properties(self,context):
        for old_prop in self.properties:
            self.properties.remove(0)
        for old_prop in self.geo_inputs:
            self.geo_inputs.remove(0)

        scene_cb = context.scene.cabinet_builder
        var_obj = scene_cb.variable_object
        items = list(var_obj.items())
        for key, value in items:   
            if str(type(value)) != "<class 'IDPropertyGroup'>":
                pm = var_obj.id_properties_ui(key)
                rna_data = pm.as_dict()
                description = rna_data.get("description", "")  
                if 'CABINET_BUILDER_PROP' in description:              
                    prop = self.properties.add()  
                    prop.name = key

        geo_obj = cb_types.GeoNodeMeshObject(var_obj)
        self.mod_name = geo_obj.mod.name
        for input in geo_obj.mod.node_group.interface.items_tree:
            prop = self.geo_inputs.add()
            prop.name = input.name
            prop.identifier = input.identifier

    def execute(self, context):
        scene_cb = context.scene.cabinet_builder
        drivers = self.obj.cabinet_builder.get_drivers()
        for driver in drivers:
            if self.data_path in driver.data_path and driver.array_index == self.array_index:
                for prop in self.properties:
                    if prop.add:
                        var = driver.driver.variables.new()
                        var.name = prop.name.replace(" ","")
                        var.targets[0].id = scene_cb.variable_object
                        var.targets[0].data_path = '["' + prop.name + '"]'
                        var.type = 'SINGLE_PROP'

                for prop in self.geo_inputs:
                    if prop.add:
                        var = driver.driver.variables.new()
                        var.name = prop.name.replace(" ","")
                        var.targets[0].id = scene_cb.variable_object
                        var.targets[0].data_path = 'modifiers["' + self.mod_name + '"]["' + prop.identifier + '"]'
                        var.type = 'SINGLE_PROP'

                for target in var.targets:
                    target.transform_space = 'LOCAL_SPACE'

        self.obj.tag = True
        self.obj.update_tag(refresh={'OBJECT', 'DATA', 'TIME'})
        context.view_layer.update()
        return {'FINISHED'}

    def invoke(self,context,event):
        self.obj = bpy.data.objects[self.object_name]
        self.get_properties(context)
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=400)

    def draw(self, context):
        scene_cb = context.scene.cabinet_builder
        layout = self.layout
        box = layout.box()
        box.label(text='Main Properties - ' + scene_cb.variable_object.name)
        col = box.column(align=True)
        for prop in self.geo_inputs:
            row = col.row()
            row.label(text=prop.name)
            row.prop(prop,'add')

        box = layout.box()
        box.label(text='Properties')
        col = box.column(align=True)
        for prop in self.properties:
            row = col.row()
            row.label(text=prop.name)
            row.prop(prop,'add')


class cabinet_builder_OT_remove_variable(bpy.types.Operator):
    bl_idname = "cabinet_builder.remove_variable"
    bl_label = "Remove Variable"
    bl_description = "This removes a variable"
    bl_options = {'UNDO'}
    
    object_name: bpy.props.StringProperty(name='Object Name') # type: ignore
    data_path: bpy.props.StringProperty(name='Data Path') # type: ignore
    var_name: bpy.props.StringProperty(name='Variable Name') # type: ignore
    array_index: bpy.props.IntProperty(name='Array Index') # type: ignore

    def execute(self, context):
        obj = bpy.data.objects[self.object_name]
        drivers = obj.cabinet_builder.get_drivers()
        for driver in drivers:
            if driver.data_path == self.data_path:
                if driver.array_index == self.array_index:
                    for var in driver.driver.variables:
                        if var.name == self.var_name:
                            driver.driver.variables.remove(var)
        return {'FINISHED'}
    

class cabinet_builder_OT_select_object(bpy.types.Operator):
    bl_idname = "cabinet_builder.select_object"
    bl_label = "Select Object"
    bl_description = "This selects an object and sets it as an active object"
    bl_options = {'UNDO'}

    obj_name: bpy.props.StringProperty(name='Object Name') # type: ignore

    @classmethod
    def poll(cls, context):
        if context.mode != 'OBJECT':
            return False
        return True

    def execute(self, context):
        if self.obj_name in context.scene.objects:
            bpy.ops.object.select_all(action = 'DESELECT')
            obj = context.scene.objects[self.obj_name]
            obj.select_set(True)
            context.view_layer.objects.active = obj
        return {'FINISHED'}


class cabinet_builder_OT_drag_library_item(cb_snap.Drop_Operator):
    bl_idname = "cabinet_builder.drag_library_item"
    bl_label = "Drag Library Item"
    bl_description = "This is called when an item from the library is dragged"
    bl_options = {'UNDO'}

    parent = None
    container = None

    @classmethod
    def poll(cls, context):
        if context.mode != 'OBJECT':
            return False
        return True

    def execute(self, context):
        self.setup_drop_operator(context)
        self.parent = None
        path = os.path.join(os.path.dirname(context.asset.full_library_path),'assets',context.asset.name + ".blend")
        with bpy.data.libraries.load(path) as (data_from, data_to):
                data_to.objects = data_from.objects
        for obj in data_to.objects:
            if obj.parent == None:
                self.parent = obj
            context.view_layer.active_layer_collection.collection.objects.link(obj) 

        self.container = cb_types.GeoNodeContainer(self.parent)
        # context.view_layer.active_layer_collection.collection.objects.link(self.parent) 
        self.parent.hide_viewport = False
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
    
    def hide_objects(self,hide):   
        self.parent.hide_set(hide)
        for child in self.parent.children_recursive:
            if child.name in bpy.context.view_layer.active_layer_collection.collection.objects:
                child.hide_set(hide)

    def modal(self, context, event):

        self.hide_objects(True)
        self.mouse_pos = Vector((event.mouse_x - self.region.x, event.mouse_y - self.region.y))  
        context.view_layer.update()          
        cb_snap.main(self, event.ctrl, context)
        self.hide_objects(False)

        sel_container = None
        if self.hit_object and 'IS_GeoNodeContainer' in self.hit_object:
            sel_container = cb_types.GeoNodeContainer(self.hit_object)
            self.container.obj.location = (0,0,0)
            self.container.obj.parent = self.hit_object
            self.container.set_input("Dim X",sel_container.get_input('Dim X'))
            self.container.set_input("Dim Y",sel_container.get_input('Dim Y'))
            self.container.set_input("Dim Z",sel_container.get_input('Dim Z'))
        else:
            self.container.obj.parent = None
            self.parent.location = self.hit_location

        if self.event_is_place_asset(event):
            if sel_container:
                dim_x = sel_container.get_var_input("Dim X",'dim_x')
                dim_y = sel_container.get_var_input("Dim Y",'dim_y')
                dim_z = sel_container.get_var_input("Dim Z",'dim_z')
                self.container.driver_input('Dim X','dim_x',[dim_x])
                self.container.driver_input('Dim Y','dim_y',[dim_y])
                self.container.driver_input('Dim Z','dim_z',[dim_z])
            return {'FINISHED'}

        if event.type in {'RIGHTMOUSE', 'ESC'}:
            #---DELETE DATA
            for child in self.cabinet.obj.children_recursive:
                bpy.data.objects.remove(child, do_unlink=True)
            bpy.data.objects.remove(self.cabinet.obj, do_unlink=True) 
            return {'CANCELLED'}      
          
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}

        return {'RUNNING_MODAL'}  


class cabinet_builder_OT_click_library_item(bpy.types.Operator):
    bl_idname = "cabinet_builder.click_library_item"
    bl_label = "Click Library Item"
    bl_description = "This is called when an item from the library is clicked"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        if context.mode != 'OBJECT':
            return False
        return True

    def execute(self, context):
        print(context.asset)
        return {'FINISHED'}
    

class cabinet_builder_OT_add_user_library_category(bpy.types.Operator):
    bl_idname = "cabinet_builder.add_user_library_category"
    bl_label = "Add User Library Category"

    category_name: bpy.props.StringProperty(name="Category Name")# type: ignore

    def invoke(self,context,event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=400)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self,'category_name')

    def execute(self, context):
        path = cb_paths.get_user_library_path()
        custom_library_path = os.path.join(path,self.category_name)
        if not os.path.exists(custom_library_path):
            os.makedirs(custom_library_path)
        context.scene.cabinet_builder.active_library_category = self.category_name
        return {'FINISHED'}

class cabinet_builder_OT_change_library_category(bpy.types.Operator):
    bl_idname = "cabinet_builder.change_library_category"
    bl_label = "Change Library Category"

    category_path: bpy.props.StringProperty(name="Category Name")# type: ignore

    def execute(self, context):
        category_name = os.path.basename(self.category_path)
        context.scene.cabinet_builder.active_library_category = category_name
        user_closet_library = cb_paths.get_cabinet_builder_asset_library(context)
        user_closet_library.path = self.category_path
        if bpy.ops.asset.library_refresh.poll():
            bpy.ops.asset.library_refresh()
        return {'FINISHED'}
    
class Save_Operator(bpy.types.Operator):
    
    def get_current_view_rotation(self,context):
        '''
        Gets the current view rotation for creating thumbnails
        '''
        for window in context.window_manager.windows:
            screen = window.screen

            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    for space in area.spaces:
                        if space.type == 'VIEW_3D':
                            return space.region_3d.view_rotation

        return (0,0,0)

    def create_empty_library_script(self,library_path):
        file = codecs.open(os.path.join(bpy.app.tempdir,"save_library_temp.py"),'w',encoding='utf-8')
        file.write("import bpy\n")

        file.write("for mat in bpy.data.materials:\n")
        file.write("    bpy.data.materials.remove(mat,do_unlink=True)\n")
        file.write("for obj in bpy.data.objects:\n")
        file.write("    bpy.data.objects.remove(obj,do_unlink=True)\n")               
        file.write("bpy.context.preferences.filepaths.save_version = 0\n")

        file.write("bpy.ops.wm.save_as_mainfile(filepath=r'" + library_path + "')\n")
        file.close()
        return os.path.join(bpy.app.tempdir,'save_library_temp.py')

    def create_assembly_thumbnail_script(self,source_dir,source_file,assembly_name,obj_list,view_rotation):
        file = codecs.open(os.path.join(bpy.app.tempdir,"thumb_temp.py"),'w',encoding='utf-8')
        file.write("import bpy\n")
        file.write("with bpy.data.libraries.load(r'" + source_file + "') as (data_from, data_to):\n")
        file.write("    data_to.objects = " + str(obj_list) + "\n")    

        file.write("for obj in data_to.objects:\n")
        file.write("    bpy.context.view_layer.active_layer_collection.collection.objects.link(obj)\n")
        file.write("    obj.select_set(True)\n")
        
        file.write("bpy.context.scene.camera.rotation_euler = " + str(view_rotation) + "\n")  
        file.write("bpy.ops.view3d.camera_to_view_selected()\n")

        file.write("render = bpy.context.scene.render\n")
        file.write("render.use_file_extension = True\n")
        file.write("render.filepath = r'" + os.path.join(source_dir,assembly_name) + "'\n")
        file.write("bpy.ops.render.render(write_still=True)\n")
        file.close()

        return os.path.join(bpy.app.tempdir,'thumb_temp.py')
    
    def create_assembly_save_script(self,source_dir,source_file,assembly_name,obj_list):
        file = codecs.open(os.path.join(bpy.app.tempdir,"save_temp.py"),'w',encoding='utf-8')
        file.write("import bpy\n")
        file.write("import os\n")

        file.write("for mat in bpy.data.materials:\n")
        file.write("    bpy.data.materials.remove(mat,do_unlink=True)\n")
        file.write("for obj in bpy.data.objects:\n")
        file.write("    bpy.data.objects.remove(obj,do_unlink=True)\n")               
        file.write("bpy.context.preferences.filepaths.save_version = 0\n")
        
        file.write("with bpy.data.libraries.load(r'" + source_file + "') as (data_from, data_to):\n")
        file.write("    data_to.objects = " + str(obj_list) + "\n")        

        file.write("parent_obj = None\n")
        file.write("for obj in data_to.objects:\n")
        file.write("    bpy.context.view_layer.active_layer_collection.collection.objects.link(obj)\n")
        file.write("    if obj.parent == None:\n")
        file.write("        parent_obj = obj\n")

        file.write("if parent_obj:\n")
        file.write("    parent_obj.location = (0,0,0)\n")
        file.write("    parent_obj.rotation_euler = (0,0,0)\n")

        file.write("for mat in bpy.data.materials:\n")
        file.write("    mat.asset_clear()\n")

        file.write("bpy.ops.wm.save_as_mainfile(filepath=r'" + os.path.join(source_dir,assembly_name) + ".blend')\n")
        file.close()
        return os.path.join(bpy.app.tempdir,'save_temp.py')

    def create_asset_script(self,asset_name,thumbnail_path,is_insert=False):
        file = codecs.open(os.path.join(bpy.app.tempdir,"asset_temp.py"),'w',encoding='utf-8')
        file.write("import bpy\n")
        file.write("bpy.context.preferences.filepaths.save_version = 0\n")
        file.write("bpy.ops.mesh.primitive_cube_add()\n")
        file.write("obj = bpy.context.view_layer.objects.active\n")
        file.write("obj.name = '" + asset_name + "'\n")
        file.write("obj.asset_mark()\n")
        if is_insert:
            file.write("obj.asset_data.tags.new('IS_INSERT')\n")
        file.write("override = bpy.context.copy()\n")
        file.write("override['id'] = obj\n")
        file.write("test_path = r'" + thumbnail_path + "'\n")
        file.write("with bpy.context.temp_override(**override):\n")
        file.write("    bpy.ops.ed.lib_id_load_custom_preview(filepath=test_path)\n")

        file.write("bpy.ops.wm.save_mainfile()\n")
        file.close()
        return os.path.join(bpy.app.tempdir,'asset_temp.py')
    
    def get_children_list(self,obj):
        obj_list = []
        obj_list.append(obj.name)
        for child in obj.children_recursive:
            obj_list.append(child.name)
        return obj_list

    def get_thumbnail_path(self):
        return os.path.join(os.path.dirname(__file__),'thumbnail.blend')
    
    def save_asset(self,context,obj_list,asset_name,is_insert=False):
        path = cb_paths.get_cabinet_builder_asset_library(context).path
        custom_user_library_path = os.path.join(path,"library.blend")
        assets_folder_path = os.path.join(path,'assets')

        if bpy.data.filepath == "":
            bpy.ops.wm.save_as_mainfile(filepath=os.path.join(bpy.app.tempdir,"temp_blend.blend"))

        if not os.path.exists(custom_user_library_path):
            library_script_path = self.create_empty_library_script(custom_user_library_path)
            create_library_command = [bpy.app.binary_path,"-b","--python",library_script_path]
            subprocess.call(create_library_command)

        if not os.path.exists(assets_folder_path):
            os.makedirs(assets_folder_path)

        # obj_list = self.get_children_list(context)

        current_rotation = self.get_current_view_rotation(context)
        rotation = (current_rotation.to_euler().x,current_rotation.to_euler().y,current_rotation.to_euler().z)

        thumbnail_script_path = self.create_assembly_thumbnail_script(assets_folder_path, bpy.data.filepath, asset_name, obj_list, rotation)
        save_script_path = self.create_assembly_save_script(assets_folder_path, bpy.data.filepath, asset_name, obj_list)
        asset_script_path = self.create_asset_script(asset_name,os.path.join(assets_folder_path,asset_name + ".png"),is_insert=is_insert)

        tn_command = [bpy.app.binary_path,self.get_thumbnail_path(),"-b","--python",thumbnail_script_path]
        save_command = [bpy.app.binary_path,"-b","--python",save_script_path]
        asset_command = [bpy.app.binary_path,custom_user_library_path,"-b","--python",asset_script_path]
        
        subprocess.call(save_command)
        subprocess.call(tn_command)
        subprocess.call(asset_command)

        user_library = cb_paths.get_cabinet_builder_asset_library(context)

        workspace = context.workspace  
        workspace.asset_library_reference = user_library.name


class cabinet_builder_OT_save_cabinet(Save_Operator):
    """Save New Face Frame Cabinet"""
    bl_idname = "cabinet_builder.save_cabinet"
    bl_label = 'Save Cabinet'

    library_item_name: bpy.props.StringProperty(name="Library Item Name") # type: ignore

    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
        if 'IS_GeoNodeContainer' in context.object:
            return True
        return False

    def draw(self, context):
        layout = self.layout
        layout.prop(self,'library_item_name',text="Name")

    def invoke(self,context,event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=400)

    def execute(self, context):
        if 'IS_GeoNodeContainer' in context.object:
            obj = context.object  
            obj_list = self.get_children_list(obj)
            self.save_asset(context,obj_list,self.library_item_name,is_insert=False)
        return {'FINISHED'}


class cabinet_builder_OT_add_cabinet_part_modifier(bpy.types.Operator):
    bl_idname = "cabinet_builder.add_cabinet_part_modifier"
    bl_label = "Add Cabinet Part Modifier"
    bl_description = "This will add a cabinet part modifier"

    token_type: bpy.props.StringProperty(name="Token Type") # type: ignore

    token_name: bpy.props.StringProperty(name="Token Name",default="Token Name") # type: ignore

    def invoke(self,context,event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=300)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self,'token_name')

    def execute(self, context):
        obj = context.object
        cpm = cb_types.CabinetPartModifier(obj)
        cpm.add_token(self.token_type,self.token_name)
        cpm.mod.show_viewport = True
        if self.token_type == '3SIDEDNOTCH':
            cpm.set_input('X',cb_unit.inch(5))
            cpm.set_input('Y',cb_unit.inch(3))
            cpm.set_input('Route Depth',cb_unit.inch(.75))        
        if self.token_type == 'CORNERNOTCH':
            cpm.set_input('X',cb_unit.inch(5))
            cpm.set_input('Y',cb_unit.inch(3))
            cpm.set_input('Route Depth',cb_unit.inch(.75))
        if self.token_type == 'CUTOUT':
            mat = None
            if 'PB' in bpy.data.materials:
                mat = bpy.data.materials['PB']            
            cpm.set_input('X',cb_unit.inch(1))    
            cpm.set_input('Y',cb_unit.inch(1))      
            cpm.set_input('Route Depth',cb_unit.inch(.76))   
            cpm.set_input('End X',cb_unit.inch(5))
            cpm.set_input('End Y',cb_unit.inch(5))   
            cpm.set_input('Material',mat)  
        return {'FINISHED'}


class cabinet_builder_OT_remove_cabinet_part_modifier(bpy.types.Operator):
    bl_idname = "cabinet_builder.remove_cabinet_part_modifier"
    bl_label = "Remove Cabinet Part Modifier"
    bl_description = "This will remove a cabinet part modifier"

    modifier_name: bpy.props.StringProperty(name="Modifer Name") # type: ignore

    def execute(self, context):
        obj = context.object
        
        for mod in obj.modifiers:
            if mod.name == self.modifier_name:
                obj.modifiers.remove(mod)
                break
        
        return {'FINISHED'}
    

classes = (
    cabinet_builder_OT_container_prompts,
    cabinet_builder_OT_add_cabinet_container,
    cabinet_builder_OT_add_cabinet_part,
    cabinet_builder_OT_add_opening,
    cabinet_builder_OT_add_property,
    Variables,
    cabinet_builder_OT_get_vars_from_object,
    cabinet_builder_OT_remove_variable,
    cabinet_builder_OT_select_object,
    cabinet_builder_OT_drag_library_item,
    cabinet_builder_OT_click_library_item,
    cabinet_builder_OT_add_user_library_category,
    cabinet_builder_OT_change_library_category,
    cabinet_builder_OT_save_cabinet,
    cabinet_builder_OT_add_cabinet_part_modifier,
    cabinet_builder_OT_remove_cabinet_part_modifier,
)

register, unregister = bpy.utils.register_classes_factory(classes)    