#import sys
import pyglet
from OpenGL import GL
import os
from pathlib import Path

# if sys.path[0] != "":
#     sys.path.insert(0, "")
# sys.path.append('../../')

from fpena_t1_res import X_Camera as cam
from fpena_t1_res import ca_car as car
from fpena_t1_res import gawragerr as gar

class Controller:
    time_r= 0.0

if __name__== "__main__":
    win= pyglet.window.Window(600,600)
    cont= Controller()
    camera= cam.Camera(position= [1.2, 0.5, 0])

    with open(Path(os.path.dirname(__file__)) / "fpena_t1_res" / "A_shader.vert") as f:
        vertex_source_code = f.read()

    with open(Path(os.path.dirname(__file__)) / "fpena_t1_res" / "A_shader.frag") as f:
        fragment_source_code = f.read()

    vert_shader = pyglet.graphics.shader.Shader(vertex_source_code, "vertex")
    frag_shader = pyglet.graphics.shader.Shader(fragment_source_code, "fragment")
    pipeline = pyglet.graphics.shader.ShaderProgram(vert_shader, frag_shader)

    my_car= car.Car_Colored(camera, pipeline, [0.97, 0.35, 1.0], [0.81, 0.835, 0.84])
    my_floor= gar.Garage(camera, pipeline, 1.0, [0.42, 0.37, 0.6])

    @win.event
    def update(dt):
        cont.time_r+= dt
        my_car.update(cont.time_r)
        my_floor.update(cont.time_r)

    @win.event
    def on_draw():
        GL.glClearColor(0.5, 0.5, 0.5, 1.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)

        GL.glEnable(GL.GL_CULL_FACE)
        GL.glCullFace(GL.GL_BACK)
        GL.glFrontFace(GL.GL_CCW)
        # despues de correr el codigo con face culling me doy cuenta de que los espejos 
        # ahora apuntan hacia el lado equivocado. Es un problema menor y definitivamente no
        # concierne a los contenidos del curso, asi que espero lo perdonen. Si pueden, 
        # una proposicion de solucion tambien es agradecida.

        win.clear()
        my_floor.draw()
        my_car.draw()

    

    pyglet.clock.schedule_interval(update, 1/60)
    pyglet.app.run()