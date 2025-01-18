import bpy
import math
from cabinet_builder import cb_unit
from cabinet_builder import cb_types

class CabinetDoor(cb_types.GeoNodeContainer):
    
    def draw(self):
        self.create("Cabinet Doors")
        self.set_input("Dim X",cb_unit.inch(18))
        self.set_input("Dim Y",cb_unit.inch(23))
        self.set_input("Dim Z",cb_unit.inch(34))

        cb_obj = self.obj.cabinet_builder
        cb_obj.add_property("Front Thickness","DISTANCE",cb_unit.inch(.75))
        cb_obj.add_property("Door to Cabinet Gap","DISTANCE",cb_unit.inch(.125))
        cb_obj.add_property("Door Rotation","ANGLE",math.radians(90))
        cb_obj.add_property("Open Door","PERCENTAGE",0)
        cb_obj.add_property('Door Swing','COMBOBOX',0,combo_items=['Left','Right','Double'])
        cb_obj.add_property('Pull Location','COMBOBOX',0,combo_items=['Base','Tall','Upper'])  

        cb_obj.add_property('Half Overlay Left','CHECKBOX',False)
        cb_obj.add_property('Half Overlay Right','CHECKBOX',False)  
        cb_obj.add_property('Half Overlay Top','CHECKBOX',False)  
        cb_obj.add_property('Half Overlay Bottom','CHECKBOX',False)  

        cb_obj.add_property("Left Thickness","DISTANCE",cb_unit.inch(.75))
        cb_obj.add_property("Right Thickness","DISTANCE",cb_unit.inch(.75))
        cb_obj.add_property("Top Thickness","DISTANCE",cb_unit.inch(.75))
        cb_obj.add_property("Bottom Thickness","DISTANCE",cb_unit.inch(.75))

        cb_obj.add_property("Left Reveal","DISTANCE",cb_unit.inch(.0625))
        cb_obj.add_property("Right Reveal","DISTANCE",cb_unit.inch(.0625))
        cb_obj.add_property("Top Reveal","DISTANCE",cb_unit.inch(.0625))
        cb_obj.add_property("Bottom Reveal","DISTANCE",cb_unit.inch(.0625))
        cb_obj.add_property("Vertical Gap","DISTANCE",cb_unit.inch(.125))
        cb_obj.add_property("Horizontal Gap","DISTANCE",cb_unit.inch(.125))
        cb_obj.add_property("Inset Reveal","DISTANCE",cb_unit.inch(.125))

        door_to_cabinet_gap = self.get_var_prop('Door to Cabinet Gap','door_to_cabinet_gap')
        swing = self.get_var_prop('Door Swing','swing')
        pl = self.get_var_prop('Pull Location','pl')

        lt = self.get_var_prop('Left Thickness','lt')
        rt = self.get_var_prop('Right Thickness','rt')
        tt = self.get_var_prop('Top Thickness','tt')
        bt = self.get_var_prop('Bottom Thickness','bt')

        ft = self.get_var_prop('Front Thickness','ft')
        lr = self.get_var_prop('Left Reveal','lr')
        rr = self.get_var_prop('Right Reveal','rr')
        tr = self.get_var_prop('Top Reveal','tr')
        br = self.get_var_prop('Bottom Reveal','br')
        vg = self.get_var_prop('Vertical Gap','vg')
        hg = self.get_var_prop('Horizontal Gap','hg')
        ir = self.get_var_prop('Inset Reveal','ir')

        x = self.get_var_input('Dim X','x')
        y = self.get_var_input('Dim Y','y')
        z = self.get_var_input('Dim Z','z')

        l_door = cb_types.GeoNodeCabinetPart()
        l_door.create("Left Door")
        l_door.obj.parent = self.obj
        l_door.driver('location',0,'ir',[ir])
        l_door.obj.location.y = 0
        l_door.driver('location',2,'ir',[ir])
        l_door.obj.rotation_euler.y = math.radians(-90)
        l_door.obj.rotation_euler.z = math.radians(90)
        l_door.driver_input('Length','z-(ir*2)',[z,ir])
        l_door.driver_input('Width','x-(ir*2)',[x,ir])
        l_door.driver_input('Thickness','ft',[ft])         
        l_door.set_input('Mirror Y',True) 
        l_door.set_input('Mirror Z',True) 
        l_door.obj['Edge W1 Finish'] = 3
        l_door.obj['Edge W2 Finish'] = 3
        l_door.obj['Edge L1 Finish'] = 3  
        l_door.obj['Edge L2 Finish'] = 3
        l_door.obj['Top Finish'] = 3
        l_door.obj['Bottom Finish'] = 3