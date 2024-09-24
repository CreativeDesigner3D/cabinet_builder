import bpy
from bpy.types import PropertyGroup
from bpy.props import (
        BoolProperty,
        FloatProperty,
        FloatVectorProperty,
        IntProperty,
        PointerProperty,
        StringProperty,
        CollectionProperty,
        EnumProperty,
        )

class Variable():

    obj = None
    data_path = ""
    name = ""

    def __init__(self,obj,data_path,name):
        self.obj = obj
        self.data_path = data_path
        self.name = name

class Scene_Cabinet_Builder(PropertyGroup):  

    main_tabs: EnumProperty(name="Main Tabs",
                          items=[('BUILD',"Build","Show the Build Tools"),
                                 ('LIBRARY',"Library","Show the Library")],
                          default='BUILD')# type: ignore  
    
    children_tabs: EnumProperty(name="Children Tabs",
                          items=[('SHOW_ALL',"Show All","Show All Children"),
                                 ('SHOW_SELECTED',"Show Selected","Show the Selected Child")],
                          default='SHOW_ALL')# type: ignore  

    selected_tabs: EnumProperty(name="Selected Tabs",
                          items=[('MAIN',"Main","Show the Main UI"),
                                 ('PROPERTIES',"Properties","Show the Properties"),
                                 ('CHILDREN',"Children","Show the Children"),
                                 ('DRIVERS',"Drivers","Show the Drivers")],
                          default='MAIN')# type: ignore  

    selected_object_tabs: EnumProperty(name="Selected Object Tabs",
                          items=[('MAIN',"Main","Show the Main UI"),
                                 ('MATERIALS',"Materials","Show the Material Properties"),
                                 ('MODIFIERS',"Modifiers","Show the Modifiers")],
                          default='MAIN')# type: ignore  
    
    variable_object: PointerProperty(name="Variable Object",type=bpy.types.Object)# type: ignore

    active_library_category: StringProperty(name="Active Library Category")# type: ignore

    finished_surface_material: PointerProperty(name="Finish Surface Material",type=bpy.types.Material)# type: ignore
    unfinished_surface_material: PointerProperty(name="Finish Surface Material",type=bpy.types.Material)# type: ignore
    semi_finished_surface_material: PointerProperty(name="Semi Finish Surface Material",type=bpy.types.Material)# type: ignore

    finished_edge_material: PointerProperty(name="Finish Edge Material",type=bpy.types.Material)# type: ignore
    unfinished_edge_material: PointerProperty(name="Finish Edge Material",type=bpy.types.Material)# type: ignore
    semi_finished_edge_material: PointerProperty(name="Semi Finish Edge Material",type=bpy.types.Material)# type: ignore
    
    @classmethod
    def register(cls):
        bpy.types.Scene.cabinet_builder = PointerProperty(
            name="Cabinet Builder Props",
            description="Cabinet Builder Props",
            type=cls,
        )
        
    @classmethod
    def unregister(cls):
        del bpy.types.Scene.home_builder   


class Object_Cabinet_Builder(PropertyGroup):  

    expand_object_info: BoolProperty(name="Expand Object Info",default=False)# type: ignore

    def get_var(self,data_path,name):
        return Variable(self.id_data,data_path,name)
    
    def add_driver_variables(self,driver,variables):
        for var in variables:
            new_var = driver.driver.variables.new()
            new_var.type = 'SINGLE_PROP'
            new_var.name = var.name
            new_var.targets[0].data_path = var.data_path
            new_var.targets[0].id = var.obj

    def get_drivers(self):
        obj = self.id_data
        drivers = []
        if obj.animation_data:
            for driver in obj.animation_data.drivers:
                drivers.append(driver)

        if obj.data and hasattr(obj.data,'animation_data') and obj.data.animation_data:
            for driver in obj.data.animation_data.drivers:
                drivers.append(driver)

        if hasattr(obj.data,'shape_keys'):
            if obj.data and obj.data.shape_keys and obj.data.shape_keys.animation_data:
                for driver in obj.data.shape_keys.animation_data.drivers:
                    drivers.append(driver)

        return drivers

    def draw_driver(self,layout,context,driver):
        scene_cb = context.scene.cabinet_builder

        col = layout.column(align=True)
        box = col.box()
        row = box.row()        
        obj = self.id_data
        driver_name = driver.data_path
        if '"]["Input_2"]' in driver_name:
            driver_name = "Length"
        if '"]["Input_3"]' in driver_name:
            driver_name = "Width"
        if '"]["Input_4"]' in driver_name:
            driver_name = "Thickness"                
        if driver_name in {"location","rotation_euler","dimensions" ,"lock_scale",'lock_location','lock_rotation'}:
            if driver.array_index == 0:
                driver_name = driver_name + " X"
            if driver.array_index == 1:
                driver_name = driver_name + " Y"
            if driver.array_index == 2:
                driver_name = driver_name + " Z"    
        try:
            value = eval('bpy.data.objects["' + obj.name + '"].' + driver.data_path)
        except:
            if "key_blocks" in driver.data_path:
                value = eval('bpy.data.objects["' + obj.name + '"].data.shape_keys.' + driver.data_path)
            else:
                value = eval('bpy.data.objects["' + obj.name + '"].data.' + driver.data_path)
        if type(value).__name__ == 'str':
            row.label(text=driver_name + " = " + str(value),icon='AUTO')
        elif type(value).__name__ == 'float':
            row.label(text=driver_name + " = " + str(value),icon='AUTO')
        elif type(value).__name__ == 'int':
            row.label(text=driver_name + " = " + str(value),icon='AUTO')
        elif type(value).__name__ == 'bool':
            row.label(text=driver_name + " = " + str(value),icon='AUTO')
        elif type(value).__name__ == 'bpy_prop_array':
            row.label(text=driver_name + " = " + str(value[driver.array_index]),icon='AUTO')
        elif type(value).__name__ == 'Vector':
            row.label(text=driver_name + " = " + str(value[driver.array_index]),icon='AUTO')
        elif type(value).__name__ == 'Euler':
            row.label(text=driver_name + " = " + str(value[driver.array_index]),icon='AUTO')
        else:
            row.label(text=driver_name + " = " + str(type(value)),icon='AUTO')            

        props = row.operator('cabinet_builder.get_vars_from_object',text="Add Variables",icon='DRIVER')
        props.object_name = obj.name
        props.data_path = driver.data_path
        props.array_index = driver.array_index 

        row = box.row(align=True)
        row.prop(driver.driver,"expression",text="",expand=True,icon='DECORATE' if driver.driver.is_valid else 'ERROR')
        box = col.box()
        self.draw_driver_variables(box,driver)

    def draw_driver_variables(self,layout,driver):
        obj = self.id_data
        for var in driver.driver.variables:
            col = layout.column()
            boxvar = col.box()
            row = boxvar.row(align=True)
            row.label(text="",icon='BLANK1')
            row.prop(var,"name",text="",icon='FORWARD')
            
            props = row.operator("cabinet_builder.remove_variable",text="",icon='X',emboss=False)
            props.object_name = obj.name
            props.data_path = driver.data_path
            props.array_index = driver.array_index
            props.var_name = var.name

    @classmethod
    def register(cls):
        bpy.types.Object.cabinet_builder = PointerProperty(
            name="Cabinet Builder Props",
            description="Cabinet Builder Props",
            type=cls,
        )
        
    @classmethod
    def unregister(cls):
        del bpy.types.Object.home_builder   

class Window_Manager_Cabinet_Builder(PropertyGroup):

    cabinet_builder_library_index: IntProperty(name="Cabinet Builder Index",description="",default=0)# type: ignore
    cabinet_builder_library_assets: bpy.props.CollectionProperty(
        type=bpy.types.AssetHandle,
        description="Current Set of Assets In Asset Browser")# type: ignore  
    
    @classmethod
    def register(cls):
        bpy.types.WindowManager.cabinet_builder = PointerProperty(
            name="Cabinet Builder Props",
            description="Cabinet Builder Props",
            type=cls,
        )
        
    @classmethod
    def unregister(cls):
        del bpy.types.WindowManager.cabinet_builder  

classes = (
    Scene_Cabinet_Builder,
    Object_Cabinet_Builder,
    Window_Manager_Cabinet_Builder,
)

register, unregister = bpy.utils.register_classes_factory(classes)      