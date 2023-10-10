import glfw
import pyglet
from OpenGL import GL
import trimesh as tm
import numpy as np
import os
from pathlib import Path

if __name__== "__main__":
    win= pyglet.window.Window(800,600)

    vertexes= np.array([
        #  0.5, -0.5, 0.0,   vertex 0 #
        # -0.5, -0.5, 0.0,   vertex 1 #
        #  0.0,  0.5, 0.0,   vertex 2 #
        #  0.0,  0.0, 0.5,   vertex 3 #
        ###############################

         0.5, -0.5, 0.0,
        -0.5, -0.5, 0.0,
         0.0,  0.5, 0.0,

         0.5, -0.5, 0.0,
        -0.5, -0.5, 0.0,
         0.0,  0.0, 0.5,

         0.5, -0.5, 0.0,
         0.0,  0.5, 0.0,
         0.0,  0.0, 0.5,

         -0.5, -0.5, 0.0,
         0.0,  0.5, 0.0,
         0.0,  0.0, 0.5,

        ], dtype= np.float32)

    colors= np.array([
        255, 0, 0,     255, 0, 0,     255, 0, 0,
        0, 0, 255,     0, 0, 255,     0, 0, 255,
        0, 255, 0,     0, 255, 0,     0, 255, 0,
        125, 0, 125,   125, 0, 125,   125, 0, 123,
    ], dtype= np.float32)

    ## 0, 1, 2 Roja
    ## 0, 2, 3, azul

    with open(Path(os.path.dirname(__file__)) / "examples/hello_world/vertex_program.glsl") as f:
        vertex_source_code = f.read()

    with open(Path(os.path.dirname(__file__)) / "examples/hello_world/fragment_program.glsl") as f:
        fragment_source_code = f.read()

    vert_shader = pyglet.graphics.shader.Shader(vertex_source_code, "vertex")
    frag_shader = pyglet.graphics.shader.Shader(fragment_source_code, "fragment")
    pipeline = pyglet.graphics.shader.ShaderProgram(vert_shader, frag_shader)

    gpu_data= pipeline.vertex_list(12, GL.GL_TRIANGLES)

    gpu_data.position[:]= vertexes
    gpu_data.color[:]= colors

    @win.event
    def on_draw():
        GL.glClearColor(0.5, 0.5, 0.5, 1.0)
        win.clear()
        pipeline.use()
        gpu_data.draw(GL.GL_TRIANGLES)

        ##Como dibujamos el triangulo 012 en rojo primero, y los demas
        ##triángulos encima de este, tenemos que nunca se ve el rojo.

    pyglet.app.run()