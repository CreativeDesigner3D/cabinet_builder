import bpy
import math
import cabinet_door
import cabinet_carcass
from cabinet_builder import cb_unit
from cabinet_builder import cb_types


class Cabinet_Base_1_Door(cabinet_carcass.CabinetCarcass):
    LIBRARY_ITEM_NAME = "Base 1 Door"

    def draw(self):
        self.use_stretchers = True
        self.create_carcass(self.LIBRARY_ITEM_NAME)
        door = cabinet_door.CabinetDoor()
        self.add_insert(door)
        bpy.ops.cabinet_builder.assign_cabinet_materials(search_obj_name=self.obj.name)        


class Cabinet_Tall_1_Door(cabinet_carcass.CabinetCarcass):
    LIBRARY_ITEM_NAME = "Tall 1 Door"

    def draw(self):
        self.height = cb_unit.inch(86)
        self.use_stretchers = False
        self.create_carcass(self.LIBRARY_ITEM_NAME)
        self.add_doors()
        bpy.ops.cabinet_builder.assign_cabinet_materials(search_obj_name=self.obj.name)    
