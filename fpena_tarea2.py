#import sys
import pyglet
from OpenGL import GL
import os
from pathlib import Path
from pyglet.window import key

# if sys.path[0] != "":
#     sys.path.insert(0, "")
# sys.path.append('../../')

from fpena_t2_res import X_Camera2 as cam
from fpena_t2_res import X_Controller2 as cont
from fpena_t2_res import fpena_stage as car
# from fpena_t1_res import ca_car as car
# from fpena_t1_res import gawragerr as gar

# class Controller:
#     time_r= 0.0

if __name__== "__main__":
    #win= pyglet.window.Window(600,600)
    controller= cont.Controller("fpena_t2")

    camera= controller.program_state["camera"] 
    #camera= cam.Camera(position= [1.2, 0.5, 0])

    #CHANGE CONTROLLER AND CAMERA --DONE

    with open(Path(os.path.dirname(__file__)) / "fpena_t2_res" / "x_color_mesh_lit.vert") as f:
        vertex_source_code = f.read()

    with open(Path(os.path.dirname(__file__)) / "fpena_t2_res" / "x_color_mesh_lit.frag") as f:
        fragment_source_code = f.read()

    #CHANGE SHADERS! --DONE

    vert_shader = pyglet.graphics.shader.Shader(vertex_source_code, "vertex")
    frag_shader = pyglet.graphics.shader.Shader(fragment_source_code, "fragment")
    pipeline = pyglet.graphics.shader.ShaderProgram(vert_shader, frag_shader)

    my_car= car.Car_Colored(controller, pipeline, [0.97, 0.35, 1.0], [0.81, 0.835, 0.84])
    # my_floor= gar.Garage(camera, pipeline, 1.0, [0.42, 0.37, 0.6])

    @controller.event
    def on_key_press(symbol, modifiers):
        if symbol == key.W:
            controller.program_state["car"]= (controller.program_state["car"] + 1) % 3
            print("CAMBIAR AUTO")

    @controller.event
    def update(dt):
        controller.program_state["total_time"] += dt
        my_car.update(controller.program_state["total_time"], controller.program_state["car"])
        # my_floor.update(cont.time_r)

    @controller.event
    def on_draw():
            
        controller.clear()
        my_car.draw()

    

    pyglet.clock.schedule_interval(update, 1/60)
    pyglet.app.run()