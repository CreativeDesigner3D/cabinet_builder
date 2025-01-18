import bpy
import math
import cabinet_door
import cabinet_carcass
from cabinet_builder import cb_unit
from cabinet_builder import cb_types


class Cabinet_Base_1_Door(cb_types.GeoNodeContainer):
    
    def draw(self):
        self.create("Base 1 Door")
        self.set_input("Mirror Y",True)
        self.set_input("Dim X",cb_unit.inch(18))
        self.set_input("Dim Y",cb_unit.inch(23))
        self.set_input("Dim Z",cb_unit.inch(34))

        x = self.get_var_input('Dim X','x')
        y = self.get_var_input('Dim Y','y')
        z = self.get_var_input('Dim Z','z')

        carcass = cabinet_carcass.CabinetCarcass()
        carcass.draw()
        carcass.obj.parent = self.obj
        carcass.driver_input('Dim X','x',[x])
        carcass.driver_input('Dim Y','y',[y])
        carcass.driver_input('Dim Z','z',[z]) 

        carcass_props = carcass.obj.cabinet_builder

        carcass_x = carcass.get_var_input('Dim X','carcass_x')
        carcass_y = carcass.get_var_input('Dim Y','carcass_y')
        carcass_z = carcass.get_var_input('Dim Z','carcass_z')

        carcass_mt = carcass_props.get_var('["Material Thickness"]','carcass_mt')
        carcass_tkh = carcass_props.get_var('["Toe Kick Height"]','carcass_tkh')

        door = cabinet_door.CabinetDoor()
        door.draw()
        door.obj.parent = carcass.obj
        door.driver('location',0,'carcass_mt',[carcass_mt])
        door.driver('location',1,'-carcass_y',[carcass_y])
        door.driver('location',2,'carcass_tkh+carcass_mt',[carcass_tkh,carcass_mt])
        door.driver_input('Dim X','carcass_x-(carcass_mt*2)',[carcass_x,carcass_mt])
        door.driver_input('Dim Y','carcass_y',[carcass_y])
        door.driver_input('Dim Z','carcass_z-carcass_tkh-(carcass_mt*2)',[carcass_z,carcass_tkh,carcass_mt]) 

        bpy.ops.cabinet_builder.assign_cabinet_materials()        
