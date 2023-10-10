import pyglet
import numpy as np
import os
from pathlib import Path 
from OpenGL import GL


with open(Path(os.path.dirname(__file__)) / "fpena_t1_res" / "B_shader.vert") as f:
        vertex_source_code_B= f.read()

with open(Path(os.path.dirname(__file__)) / "fpena_t1_res" / "B_shader.frag") as f:
    fragment_source_code_B= f.read()

vert_shader_B = pyglet.graphics.shader.Shader(vertex_source_code_B, "vertex")
frag_shader_B = pyglet.graphics.shader.Shader(fragment_source_code_B, "fragment")
pipeline_B= pyglet.graphics.shader.ShaderProgram(vert_shader_B, frag_shader_B)

vertexes_B= np.array([
    -0.5, -0.5, 0.0,
        0.5, -0.5, 0.0,
    -0.5,  0.5, 0.0,
    
    -0.5,  0.5, 0.0,
        0.5, -0.5, 0.0,
        0.5,  0.5, 0.0,
], dtype= np.float32)

indexes_B= np.array([0, 1, 2, 3, 4, 5], dtype= np.int32)

colors_B= np.array([0.5, 0.5, 0.5,
                    0.5, 0.5, 0.5,
                    0.5, 0.5, 0.5,
                    
                    0.5, 0.5, 0.5,
                    0.5, 0.5, 0.5,
                    0.5, 0.5, 0.5,], dtype= np.float32)

lane_gpu= pipeline_B.vertex_list_indexed(6, GL.GL_TRIANGLES, indexes_B)
lane_gpu.position[:]= vertexes_B
lane_gpu.color[:]= colors_B