import os
import sys
from pathlib import Path
import pyglet
import pyglet.gl as GL

if sys.path[0] != "":
    sys.path.insert(0, "")
sys.path.append('../../')

import grafica.transformations as tr
import bull_shapes as bs

if __name__== "__main__":
    window = pyglet.window.Window(960, 960)

    colorcube= bs.createFacetedCube()


    with open(Path(os.path.dirname(__file__)) / "script0_vertex.glsl") as f:
        vertex_source_code = f.read()

    with open(Path(os.path.dirname(__file__)) / "script0_fragment.glsl") as f:
        fragment_source_code = f.read()

    
    pyramid_vert= pyglet.graphics.shader.Shader(vertex_source_code, "vertex")
    pyramid_frag= pyglet.graphics.shader.Shader(fragment_source_code, "fragment")
    pyramid_pipe= pyglet.graphics.shader.ShaderProgram(pyramid_vert, pyramid_frag)

    pyramid_gpu_data= pyramid_pipe.vertex_list_indexed(colorcube.vertices_num, GL.GL_TRIANGLES, colorcube.indices)
    pyramid_gpu_data.position[:]= colorcube.vertices
    pyramid_gpu_data.color[:]= colorcube.colores

    window.program_state = {
        "pyramid": tr.identity(),
        "total_time": 0.0,
    }

    @window.event
    def on_draw():
        GL.glClearColor(0.5, 0.5, 0.5, 1.0)
        window.clear()

        pyramid_pipe.use()

        pyramid_pipe["view_transform"]= window.program_state["pyramid"].reshape(16, 1, order= "F")
        pyramid_gpu_data.draw(GL.GL_TRIANGLES)

    def update_world(dt, window):
        window.program_state["total_time"]+= dt
        total_time= window.program_state["total_time"]

        window.program_state["pyramid"]= tr.rotationZ(total_time * 0.6)

    pyglet.clock.schedule_interval(update_world, 1 / 60.0, window)
    pyglet.app.run(1 / 60.0)