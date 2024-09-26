import bpy
import os

def get_particle_board_material():
    if 'Particle Board' in bpy.data.materials:
        return bpy.data.materials['Particle Board']
    path = os.path.join(os.path.dirname(__file__),'materials.blend')
    return get_material(path,'Particle Board')

def get_material(library_path,material_name):
    if material_name in bpy.data.materials:
        return bpy.data.materials[material_name]

    if os.path.exists(library_path):

        with bpy.data.libraries.load(library_path) as (data_from, data_to):
            for mat in data_from.materials:
                if mat == material_name:
                    data_to.materials = [mat]
                    break    
        
        for mat in data_to.materials:
            return mat