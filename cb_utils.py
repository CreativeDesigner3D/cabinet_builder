import bpy
import math
import os

def get_unfinished_material(context):
    scene_cb = context.scene.cabinet_builder
    if scene_cb.unfinished_surface_material:
        return scene_cb.unfinished_surface_material
    path = os.path.join(os.path.dirname(__file__),'materials.blend')
    mat = get_material(path,'Particle Board')
    scene_cb.unfinished_surface_material = mat
    return get_material(path,'Particle Board')

def get_finished_material(context):
    scene_cb = context.scene.cabinet_builder
    if scene_cb.finished_surface_material:
        return scene_cb.finished_surface_material
    path = os.path.join(os.path.dirname(__file__),'materials.blend')
    mat = get_material(path,'Wood')
    finished_material = mat.copy()
    finished_material.name = 'Finished Cabinet Surface'
    scene_cb.finished_surface_material = finished_material    
    return scene_cb.finished_surface_material

def get_finished_edge_material(context):
    scene_cb = context.scene.cabinet_builder
    if scene_cb.finished_edge_material:
        return scene_cb.finished_edge_material
    path = os.path.join(os.path.dirname(__file__),'materials.blend')
    mat = get_material(path,'Wood')
    finished_material = mat.copy()
    node = None
    for n in finished_material.node_tree.nodes:
        if n.label == 'Wood':
            node = n    
    for input in node.inputs:
        if input.name == 'Rotation':
            input.default_value[1] = math.radians(90)   
            input.default_value[2] = math.radians(0)  
    finished_material.name = 'Finished Cabinet Edge'
    scene_cb.finished_edge_material = finished_material    
    return scene_cb.finished_edge_material

def get_semi_exposed_material(context):
    scene_cb = context.scene.cabinet_builder
    if scene_cb.semi_exposed_surface_material:
        return scene_cb.semi_exposed_surface_material
    path = os.path.join(os.path.dirname(__file__),'materials.blend')
    mat = get_material(path,'Solid')
    finished_material = mat.copy()
    finished_material.name = 'Semi Exposed Cabinet Surface'
    scene_cb.semi_exposed_surface_material = finished_material    
    return scene_cb.semi_exposed_surface_material

def get_front_material(context):
    scene_cb = context.scene.cabinet_builder
    if scene_cb.front_surface_material:
        return scene_cb.front_surface_material
    path = os.path.join(os.path.dirname(__file__),'materials.blend')
    mat = get_material(path,'Wood')
    finished_material = mat.copy()
    finished_material.name = 'Front Cabinet Surface'
    scene_cb.front_surface_material = finished_material    
    return scene_cb.front_surface_material

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