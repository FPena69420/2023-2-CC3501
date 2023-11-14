from pyglet.graphics.shader import ShaderProgram as pipe
from OpenGL import GL
import trimesh as tm
import numpy as np
import os
from pathlib import Path

from fpena_t1_res import X_SceneGraph as sgraph
from fpena_t1_res import X_Model as model
from fpena_t1_res import X_Camera as cam
from grafica import transformations as tr

class Garage:

    def __init__(self, camera: cam.Camera, pipeline: pipe,
                 size: float= 0.5, 
                 color1: float= [1.0, 1.0, 1.0]) -> sgraph:
        
        #ADD LIGHTS
        
        floor_vertices= np.array([
            -size, 0.0, -size,
             size, 0.0, -size,
            -size, 0.0,  size,
            
            -size, 0.0,  size,
             size, 0.0, -size,
             size, 0.0,  size,
             ], dtype= np.float32)
        
        wall_1_vertices= np.array([
            -size, 0.0,  0.0, 
             size, 0.0,  0.0, 
            -size, size, 0.0, 
            -size, size, 0.0, 
             size, 0.0,  0.0, 
             size, size, 0.0, 
             ], dtype= np.float32)
        
        wall_2_vertices= np.array([
            0.0,  0.0,  -size,
            0.0,  size, -size,
            0.0,  0.0,   size,
            0.0,  0.0,   size,
            0.0,  size, -size,
            0.0,  size,  size,
             ], dtype= np.float32)
        
        # np.array([
        #     0.0,   -size,  0.0,  
        #     0.0,    size,  0.0,  
        #     0.0,   -size,  size, 
        #     0.0,   -size,  size, 
        #     0.0,    size,  0.0,  
        #     0.0,    size,  size, 
        #      ], dtype= np.float32)

        floor_indexes= np.array([5,4,3,2,1,0], dtype= np.int32)

        floor= model.Model(floor_vertices, floor_indexes)
        floor.init_gpu_data(pipeline)

        wall1= model.Model(wall_1_vertices, floor_indexes[::-1])
        wall1.init_gpu_data(pipeline)

        wall2= model.Model(wall_2_vertices, floor_indexes[::-1])
        wall2.init_gpu_data(pipeline)

        self.graph= sgraph.SceneGraph(camera)
        self.graph.add_node("floor")

        self.graph.add_node("floor_down", 
                            attach_to= "floor",
                            mesh= floor, 
                            color= color1)
        self.graph.add_node("wall1",
                            attach_to= "floor",
                            mesh= wall1,
                            color= [0.3, 0.1, 0.1],
                            position= [0.0, 0.0, -size])
        self.graph.add_node("wall2",
                            attach_to= "floor",
                            mesh= wall2,
                            color= [0.1, 0.1, 0.3],
                            position= [-size, 0.0, 0.0])
        
        
    def draw(self):
        self.graph.draw()

    def update(self, t_time):
        self.graph["floor"]["rotation"]= [0.0, - 0.76 * t_time, 0.0]

