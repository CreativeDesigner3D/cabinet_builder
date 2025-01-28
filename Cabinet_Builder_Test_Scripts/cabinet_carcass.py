import bpy
import math
from cabinet_builder import cb_unit
from cabinet_builder import cb_types
from cabinet_builder import cb_utils

class CabinetCarcass(cb_types.GeoNodeContainer):
    
    width = cb_unit.inch(18)
    height = cb_unit.inch(34)
    depth = cb_unit.inch(23)
    use_stretchers = False

    def create_carcass(self,name="Cabinet Carcass"):
        self.create(name)
        self.set_input("Mirror Y",True)
        self.set_input("Dim X",self.width)
        self.set_input("Dim Y",self.depth)
        self.set_input("Dim Z",self.height)

        cb_obj = self.obj.cabinet_builder
        cb_obj.add_property("Material Thickness","DISTANCE",cb_unit.inch(.75))
        cb_obj.add_property("Toe Kick Height","DISTANCE",cb_unit.inch(4))
        cb_obj.add_property("Toe Kick Setback","DISTANCE",cb_unit.inch(2.5))
        cb_obj.add_property("Stretcher Width","DISTANCE",cb_unit.inch(4))

        mt = self.get_var_prop('Material Thickness','mt')
        tkh = self.get_var_prop('Toe Kick Height','tkh')
        tks = self.get_var_prop('Toe Kick Setback','tks')
        sw = self.get_var_prop('Stretcher Width','sw')
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
        left_side.obj['Edge L2 Finish'] = 1
        left_side.obj['Top Finish'] = 2
        left_side.obj['Bottom Finish'] = 1

        tk_notch = cb_types.CabinetPartModifier(left_side.obj)
        tk_notch.add_node('CPM_CORNERNOTCH','Toe Kick Notch')
        tk_notch.mod.show_viewport = True
        tk_notch.driver_input('X','tkh',[tkh])
        tk_notch.driver_input('Y','tks',[tks])
        tk_notch.driver_input('Route Depth','mt+.01',[mt])
        tk_notch.set_input('Flip Y',True)
        tk_notch.set_input('Material',cb_utils.get_unfinished_material(bpy.context))

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
        right_side.obj['Edge L2 Finish'] = 1
        right_side.obj['Top Finish'] = 2
        right_side.obj['Bottom Finish'] = 1

        tk_notch = cb_types.CabinetPartModifier(right_side.obj)
        tk_notch.add_node('CPM_CORNERNOTCH','Toe Kick Notch')
        tk_notch.mod.show_viewport = True
        tk_notch.driver_input('X','tkh',[tkh])
        tk_notch.driver_input('Y','tks',[tks])
        tk_notch.driver_input('Route Depth','mt+.01',[mt])
        tk_notch.set_input('Flip Y',True)
        tk_notch.set_input('Material',cb_utils.get_unfinished_material(bpy.context))

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
        bottom.obj['Edge L2 Finish'] = 1
        bottom.obj['Top Finish'] = 2
        bottom.obj['Bottom Finish'] = 1

        if self.use_stretchers:
            f_stretcher = cb_types.GeoNodeCabinetPart()
            f_stretcher.create("Front Stretcher")
            f_stretcher.obj.parent = self.obj
            f_stretcher.obj.rotation_euler = (0,0,0)
            f_stretcher.driver('location',0,'mt',[mt])
            f_stretcher.driver('location',1,'-y',[y])
            f_stretcher.driver('location',2,'z',[z])
            f_stretcher.driver_input('Length','x-mt*2',[x,mt])
            f_stretcher.driver_input('Width','sw',[sw])
            f_stretcher.driver_input('Thickness','mt',[mt])
            f_stretcher.set_input('Mirror Y',False)
            f_stretcher.set_input('Mirror Z',True)
            f_stretcher.obj['Edge L1 Finish'] = 1
            f_stretcher.obj['Top Finish'] = 2

            r_stretcher = cb_types.GeoNodeCabinetPart()
            r_stretcher.create("Rear Stretcher")
            r_stretcher.obj.parent = self.obj
            r_stretcher.obj.rotation_euler = (0,0,0)
            r_stretcher.driver('location',0,'mt',[mt])
            r_stretcher.driver('location',2,'z',[z])
            r_stretcher.driver_input('Length','x-mt*2',[x,mt])
            r_stretcher.driver_input('Width','sw',[sw])
            r_stretcher.driver_input('Thickness','mt',[mt])
            r_stretcher.set_input('Mirror Y',True)
            r_stretcher.set_input('Mirror Z',True)
            r_stretcher.obj['Top Finish'] = 2
        else:
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
            top.obj['Edge L2 Finish'] = 1
            top.obj['Top Finish'] = 2
            top.obj['Bottom Finish'] = 1

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
        back.obj['Top Finish'] = 2
        back.obj['Bottom Finish'] = 1

        toe_kick = cb_types.GeoNodeCabinetPart()
        toe_kick.create("Toe Kick")
        toe_kick.obj.parent = self.obj
        toe_kick.driver('location',0,'mt',[mt])
        toe_kick.driver('location',1,'-y+tks',[y,tks])
        toe_kick.obj.location.z = 0
        toe_kick.obj.rotation_euler = (math.radians(-90),0,0)
        toe_kick.driver_input('Length','x-mt*2',[x,mt])
        toe_kick.driver_input('Width','tkh',[tkh])
        toe_kick.driver_input('Thickness','mt',[mt])
        toe_kick.set_input('Mirror Y',True)
        toe_kick.set_input('Mirror Z',False)
        # toe_kick.obj['Top Finish'] = 2
        # toe_kick.obj['Bottom Finish'] = 1

    def add_doors(self):
        cb_obj = self.obj.cabinet_builder
        cb_obj.add_property("Front Thickness","DISTANCE",cb_unit.inch(.75))
        cb_obj.add_property("Door Rotation","ANGLE",math.radians(120))
        cb_obj.add_property("Open Door","PERCENTAGE",0)
        cb_obj.add_property("Inset Reveal","DISTANCE",cb_unit.inch(.125))

        mt = self.get_var_prop('Material Thickness','mt')
        tkh = self.get_var_prop('Toe Kick Height','tkh')
        ir = self.get_var_prop('Inset Reveal','ir')
        ft = self.get_var_prop('Front Thickness','ft')
        open = self.get_var_prop('Open Door','open')
        rot = self.get_var_prop('Door Rotation','rot')
        x = self.get_var_input('Dim X','x')
        z = self.get_var_input('Dim Z','z')
        y = self.get_var_input('Dim Y','y')

        l_door = cb_types.GeoNodeCabinetPart()
        l_door.create("Left Door")
        l_door.obj.parent = self.obj
        l_door.driver('location',0,'mt+ir',[mt,ir])
        l_door.driver('location',1,'-y',[y])
        l_door.driver('location',2,'tkh+mt+ir',[tkh,mt,ir])
        l_door.obj.rotation_euler.y = math.radians(-90)
        l_door.obj.rotation_euler.z = math.radians(90)
        l_door.driver('rotation_euler',2,'radians(90)-rot*(open/100)',[rot,open])
        l_door.driver_input('Length','z-tkh-mt*2-(ir*2)',[z,tkh,mt,ir])
        l_door.driver_input('Width','x-mt*2-(ir*2)',[x,mt,ir])
        l_door.driver_input('Thickness','ft',[ft])         
        l_door.set_input('Mirror Y',True) 
        l_door.set_input('Mirror Z',True) 
        l_door.obj['Edge W1 Finish'] = 3
        l_door.obj['Edge W2 Finish'] = 3
        l_door.obj['Edge L1 Finish'] = 3  
        l_door.obj['Edge L2 Finish'] = 3
        l_door.obj['Top Finish'] = 3
        l_door.obj['Bottom Finish'] = 3

    def add_insert(self,insert):
        x = self.get_var_input('Dim X','x')
        z = self.get_var_input('Dim Z','z')
        y = self.get_var_input('Dim Y','y')  
        mt = self.get_var_prop('Material Thickness','mt')
        tkh = self.get_var_prop('Toe Kick Height','tkh')        

        insert.draw()
        insert.obj.parent = self.obj
        insert.driver('location',0,'mt',[mt])
        insert.driver('location',1,'-y',[y])
        insert.driver('location',2,'tkh+mt',[tkh,mt])
        insert.driver_input('Dim X','x-mt*2',[x,mt])
        insert.driver_input('Dim Y','y',[y])
        insert.driver_input('Dim Z','z-tkh-mt*2',[z,tkh,mt])