import bpy
from . import cb_types, cb_unit
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

classes = (
    cabinet_builder_OT_add_cabinet_container,
    cabinet_builder_OT_add_cabinet_part,
    cabinet_builder_OT_add_property,
    Variables,
    cabinet_builder_OT_get_vars_from_object,
    cabinet_builder_OT_remove_variable,
    cabinet_builder_OT_select_object,
)

register, unregister = bpy.utils.register_classes_factory(classes)    