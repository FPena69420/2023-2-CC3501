# import sys
# import os
import trimesh as tm
# No es necesaria la siguiente línea si el archivo está en el root del repositorio
#sys.path.append(os.path.dirname(os.path.dirname((os.path.abspath(__file__)))))
from grafica import transformations as tr
from fpena_t1_res import X_Model as Model

class Mesh(Model):
    def __init__(self, asset_path):
        mesh_data = tm.load(asset_path)
        mesh_scale = tr.uniformScale(2.0 / mesh_data.scale)
        mesh_translate = tr.translate(*-mesh_data.centroid)
        mesh_data.apply_transform( mesh_scale @ mesh_translate)
        vertex_data = tm.rendering.mesh_to_vertexlist(mesh_data)
        indices = vertex_data[3]
        positions = vertex_data[4][1]

        super().__init__(positions, indices)