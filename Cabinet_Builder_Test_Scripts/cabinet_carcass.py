import bpy
import math
from cabinet_builder import cb_unit
from cabinet_builder import cb_types

class CabinetCarcass(cb_types.GeoNodeContainer):
    
    def draw(self):
        self.create("Cabinet Carcass")
        self.set_input("Mirror Y",True)

        self.obj["Material Thickness"] = cb_unit.inch(.75)
        self.obj.id_properties_ensure()
        pm = self.obj.id_properties_ui("Material Thickness")
        pm.update(subtype='DISTANCE',description='CABINET_BUILDER_PROP')

        mat_var = self.obj.cabinet_builder.get_var('["Material Thickness"]','mat_var')
        z = self.get_var_input('Dim Z','z')
        y = self.get_var_input('Dim Y','y')

        left_side = cb_types.GeoNodeCabinetPart()
        left_side.create("Left Side")
        left_side.obj.parent = self.obj
        left_side.obj.rotation_euler = (0,math.radians(-90),0)
        left_side.driver_input('Length','z',[z])
        left_side.driver_input('Width','y',[y])
        left_side.driver_input('Thickness','mat_var',[mat_var])
        left_side.set_input('Mirror Y',True)
        left_side.set_input('Mirror Z',True)


# class CabinetCarcass(cb_types.GeoNodeContainer):
#     """Creates a cabinet carcass geometry node object"""
    
#     def __init__(self):
#         super().__init__()
#         self.type_name = "Cabinet Carcass"
#         self.node_group_name = "Cabinet Carcass"
#         self.show_in_viewport = True
#         self.show_in_render = True
#         self.use_fake_user = True

#     def draw(self):
#         self.create("Cabinet Carcass")
