import bpy
import math
from cabinet_builder import cb_unit
from cabinet_builder import cb_types

class CabinetCarcass(cb_types.GeoNodeContainer):
    
    def draw(self):
        self.create("Cabinet Carcass")
        self.set_input("Mirror Y",True)
        self.set_input("Dim X",cb_unit.inch(18))
        self.set_input("Dim Y",cb_unit.inch(23))
        self.set_input("Dim Z",cb_unit.inch(34))

        self.obj.cabinet_builder.add_property("Material Thickness","DISTANCE",cb_unit.inch(.75))
        self.obj.cabinet_builder.add_property("Toe Kick Height","DISTANCE",cb_unit.inch(4))

        mt = self.obj.cabinet_builder.get_var('["Material Thickness"]','mt')
        tkh = self.obj.cabinet_builder.get_var('["Toe Kick Height"]','tkh')
        x = self.get_var_input('Dim X','x')
        z = self.get_var_input('Dim Z','z')
        y = self.get_var_input('Dim Y','y')

        left_side = cb_types.GeoNodeCabinetPart()
        left_side.create("Left Side")
        left_side.obj.parent = self.obj
        left_side.obj.rotation_euler = (0,math.radians(-90),0)
        left_side.driver_input('Length','z',[z])
        left_side.driver_input('Width','y',[y])
        left_side.driver_input('Thickness','mt',[mt])
        left_side.set_input('Mirror Y',True)
        left_side.set_input('Mirror Z',True)

        tk_notch = cb_types.CabinetPartModifier(left_side.obj)
        tk_notch.add_node('CPM_CORNERNOTCH','Toe Kick Notch')
        tk_notch.mod.show_viewport = True
        tk_notch.driver_input('X','tkh',[tkh])
        tk_notch.set_input('Y',cb_unit.inch(3))
        tk_notch.set_input('Route Depth',cb_unit.inch(.76))
        tk_notch.set_input('Flip Y',True)
        # tk_notch.set_input('Material',pb) 

        right_side = cb_types.GeoNodeCabinetPart()
        right_side.create("Right Side")
        right_side.obj.parent = self.obj
        right_side.obj.rotation_euler = (0,math.radians(-90),0)
        right_side.driver('location',0,'x',[x])
        right_side.driver_input('Length','z',[z])
        right_side.driver_input('Width','y',[y])
        right_side.driver_input('Thickness','mt',[mt])
        right_side.set_input('Mirror Y',True)
        right_side.set_input('Mirror Z',False)

        bottom = cb_types.GeoNodeCabinetPart()
        bottom.create("Bottom")
        bottom.obj.parent = self.obj
        bottom.obj.rotation_euler = (0,0,0)
        bottom.driver('location',0,'mt',[mt])
        bottom.driver('location',2,'tkh',[tkh])
        bottom.driver_input('Length','x-mt*2',[x,mt])
        bottom.driver_input('Width','y',[y])
        bottom.driver_input('Thickness','mt',[mt])
        bottom.set_input('Mirror Y',True)
        bottom.set_input('Mirror Z',False)

        top = cb_types.GeoNodeCabinetPart()
        top.create("Top")
        top.obj.parent = self.obj
        top.obj.rotation_euler = (0,0,0)
        top.driver('location',0,'mt',[mt])
        top.driver('location',2,'z',[z])
        top.driver_input('Length','x-mt*2',[x,mt])
        top.driver_input('Width','y',[y])
        top.driver_input('Thickness','mt',[mt])
        top.set_input('Mirror Y',True)
        top.set_input('Mirror Z',True)

        back = cb_types.GeoNodeCabinetPart()
        back.create("Back")
        back.obj.parent = self.obj
        back.obj.rotation_euler = (0,math.radians(-90),math.radians(90))
        back.driver('location',0,'mt',[mt])
        back.driver('location',2,'tkh+mt',[tkh,mt])
        back.driver_input('Length','z-tkh-mt*2',[z,tkh,mt])
        back.driver_input('Width','x-mt*2',[x,mt])
        back.driver_input('Thickness','mt',[mt])
        back.set_input('Mirror Y',True)
        back.set_input('Mirror Z',False)        