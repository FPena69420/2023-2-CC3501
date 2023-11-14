from pyglet.graphics.shader import ShaderProgram as pipe
from OpenGL import GL
import trimesh as tm
import numpy as np
import os
#import sys
from pathlib import Path

from fpena_t2_res import X_SceneGraph2 as sgraph
from fpena_t2_res import X_Model as model
from fpena_t2_res import X_Controller2 as cont  #modified for t2
from grafica import transformations as tr

# if sys.path[0] != "":
#     sys.path.insert(0, "")
# sys.path.append('../../')

# import grafica.transformations as tr

class Car_Colored:

    def __init__(self, controller: cont.Controller, pipeline: pipe, 
                 color1: int= [0.95, 0.05, 0.05], 
                 color2: int= [0.95, 0.95, 0.95]) -> sgraph:
        
        # trimesh carga los archivo .glb como una escena con una lista de 
        # geometrias. De revisar el archivo .blend, notamos que estas vienen
        # en el orden en el que fueron creadas:
        #   -Cube (auto)
        #       -carcass (chasis)
        #       -accessory (ventanas, manillas, espejos y radiador)
        #   -Cylinder (rueda)
        #       -tire (llanta)
        #       -frame (aro)

        scene= tm.load(Path(os.path.dirname(__file__)) / "car_tired.glb")
        geometries= list(scene.geometry.values())

        #ADD MATERIAL
        #ADD NORMALS

        #MAYBE THE TWO MODELS DO NOT INTERACT WITH EACH OTHER, SO 

        geometry0= geometries[0]
        geometry1= geometries[1]
        geometry2= geometries[2]
        geometry3= geometries[3]

        geometry3.apply_transform(
                                  tr.scale(0.3, 1, 1) @ 
                                  tr.uniformScale(0.2/geometry3.scale) @ 
                                  tr.rotationZ(np.pi/2)
                                  )
        geometry3_vertex_data= tm.rendering.mesh_to_vertexlist(geometry3)

        geometry2.apply_transform(
                                  tr.scale(0.3, 1, 1) @ 
                                  tr.uniformScale(0.3/geometry2.scale) @ 
                                  tr.rotationZ(np.pi/2)
                                  )
        geometry2_vertex_data= tm.rendering.mesh_to_vertexlist(geometry2)

        geometry0.apply_transform(
                                  tr.uniformScale(1.0/geometry0.scale)
                                  )
        geometry0_vertex_data= tm.rendering.mesh_to_vertexlist(geometry0)

        geometry1.apply_transform(
                                  tr.uniformScale(1.0/geometry1.scale)
                                  )
        geometry1_vertex_data= tm.rendering.mesh_to_vertexlist(geometry1)

        chasis_left= model.Model(geometry0_vertex_data[4][1], 
                                 geometry0_vertex_data[3])
        chasis_left.init_gpu_data(pipeline)

        chasis_left_accessory= model.Model(geometry1_vertex_data[4][1], 
                                           geometry1_vertex_data[3])
        chasis_left_accessory.init_gpu_data(pipeline)

        # se invierten los indices para que las caras miren hacia afuera,
        # asi el face culling funciona de manera correcta.
        chasis_right= model.Model(geometry0_vertex_data[4][1], 
                                  geometry0_vertex_data[3][::-1])
        chasis_right.init_gpu_data(pipeline)

        # se invierten los indices para que las caras miren hacia afuera,
        # asi el face culling funciona de manera correcta.
        chasis_right_accessory= model.Model(geometry1_vertex_data[4][1], 
                                            geometry1_vertex_data[3][::-1])
        chasis_right_accessory.init_gpu_data(pipeline)



        wheel_right_tire= model.Model(geometry2_vertex_data[4][1], 
                                      geometry2_vertex_data[3])
        wheel_right_tire.init_gpu_data(pipeline)

        wheel_right_frame= model.Model(geometry3_vertex_data[4][1], 
                                       geometry3_vertex_data[3])
        wheel_right_frame.init_gpu_data(pipeline)
        
        # se invierten los indices para que las caras miren hacia afuera,
        # asi el face culling funciona de manera correcta.
        wheel_left_tire= model.Model(geometry2_vertex_data[4][1], 
                                     geometry2_vertex_data[3][::-1])
        wheel_left_tire.init_gpu_data(pipeline)

        # se invierten los indices para que las caras miren hacia afuera,
        # asi el face culling funciona de manera correcta.
        wheel_left_frame= model.Model(geometry3_vertex_data[4][1], 
                                      geometry3_vertex_data[3][::-1])
        wheel_left_frame.init_gpu_data(pipeline)

        move_up= abs(min(wheel_left_tire.position_data[x] for x in 
                         range(1, len(wheel_left_tire.position_data), 3)))

        self.graph= sgraph.SceneGraph(controller) #modified for t2
        self.graph.add_node("chasis",
                            position= [0.0, move_up, 0.0]
                            #scale= [0.5, 1.3, 1.8]
                            )

        self.graph.add_node("chasis_left", attach_to= "chasis")
        self.graph.add_node("chasis_left_carcass",
                            attach_to= "chasis_left",
                            mesh= chasis_left,
                            color= color1)
        self.graph.add_node("chasis_left_accessory",
                            attach_to= "chasis_left",
                            mesh= chasis_left_accessory,
                            color= color2)
        
        # notese que los nodos instanciados con los indices invertidos han
        # de reflejar sus vertices con respecto al eje X
        self.graph.add_node("chasis_right", attach_to= "chasis")
        self.graph.add_node("chasis_right_carcass",
                            attach_to= "chasis_right",
                            scale= (-1,1,1),
                            mesh= chasis_right,
                            color= color1)
        self.graph.add_node("chasis_right_accessory", 
                            attach_to= "chasis_right",
                            scale= (-1,1,1),
                            mesh= chasis_right_accessory,
                            color= color2)
        

        
        # por alguna razon la rueda se instancio reflejada al lado del eje X contrario al del 
        # chasis. Esto solo lo supe una vez que la trate de graficar
        self.graph.add_node("tire_right_front",
                            attach_to= "chasis",
                            mesh= wheel_right_tire,
                            color= [0, 0, 0],
                            position= [-0.17, 0.045, -0.28])
        self.graph.add_node("frame_right_front",
                            attach_to= "chasis",
                            mesh= wheel_right_frame, 
                            color= [1, 1, 1],
                            position= [-0.17, 0.045, -0.28])
        
        self.graph.add_node("tire_right_back",
                            attach_to= "chasis",
                            mesh= wheel_right_tire,
                            color= [0, 0, 0],
                            position= [-0.17, 0.045, 0.26])
        self.graph.add_node("frame_right_back",
                            attach_to= "chasis",
                            mesh= wheel_right_frame, 
                            color= [1, 1, 1],
                            position= [-0.17, 0.045, 0.26])
        
        # notese que los nodos instanciados con los indices invertidos han
        # de reflejar sus vertices con respecto al eje X
        self.graph.add_node("tire_left_front",
                            attach_to= "chasis",
                            mesh= wheel_left_tire,
                            color= [0, 0, 0],
                            position= [0.17, 0.045, -0.28],
                            scale= (-1, 1, 1))
        self.graph.add_node("frame_left_front",
                            attach_to= "chasis",
                            mesh= wheel_left_frame, 
                            color= [1, 1, 1],
                            position= [0.17, 0.045, -0.28],
                            scale= (-1, 1, 1))
        
        self.graph.add_node("tire_left_back",
                            attach_to= "chasis",
                            mesh= wheel_left_tire,
                            color= [0, 0, 0],
                            position= [0.17, 0.045, 0.26],
                            scale= (-1, 1, 1))
        self.graph.add_node("frame_left_back",
                            attach_to= "chasis",
                            mesh= wheel_left_frame, 
                            color= [1, 1, 1],
                            position= [0.17, 0.045, 0.26],
                            scale= (-1, 1, 1))
        
        
    def draw(self):
        self.graph.draw()

    def update(self, t_time):
        self.graph["chasis"]["transform"]= tr.rotationY(1.8 * t_time)
        
        self.graph["tire_right_front"]["rotation"]= [1.6 * t_time, 0, 0]
        self.graph["frame_right_front"]["rotation"]= [1.6 * t_time, 0, 0]

        self.graph["tire_right_back"]["rotation"]= [1.6 * t_time, 0, 0]
        self.graph["frame_right_back"]["rotation"]= [1.6 * t_time, 0, 0]

        self.graph["tire_left_front"]["rotation"]= [1.6 * t_time, 0, 0]
        self.graph["frame_left_front"]["rotation"]= [1.6 * t_time, 0, 0]

        self.graph["tire_left_back"]["rotation"]= [1.6 * t_time, 0, 0]
        self.graph["frame_left_back"]["rotation"]= [1.6 * t_time, 0, 0]