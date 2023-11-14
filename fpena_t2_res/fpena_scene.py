from pyglet.graphics.shader import ShaderProgram as pipe
from OpenGL import GL
import trimesh as tm
import numpy as np
import os
import pyglet
from pathlib import Path

# from fpena_t2_res import X_Shapes as shapes
from fpena_t2_res import X_SceneGraph2 as sgraph
from fpena_t2_res import X_Drawables2 as dwbles
from fpena_t2_res import X_Controller2 as cont  #modified for t2
from fpena_t2_res import X_Shapes2 as shapes
from auxiliares.utils import shapes as the_shapes
from grafica import transformations as tr

class X_Scene:

    def __init__(self,
                 arg_controller: cont.Controller,
                 arg_pipeline: pipe,
                 arg_quad_color= [0.1, 0.1, 0.8]) -> sgraph:
        
        self.graph= sgraph.SceneGraph(arg_controller)

        self.graph.add_node("sun",
                            pipeline= arg_pipeline,
                            light= dwbles.DirectionalLight(),
                            rotation=[-np.pi/4, 0, 0],)
