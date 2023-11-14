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

        scene= tm.load(Path(os.path.dirname(__file__)) / "car_normalized.glb")
        geometries= list(scene.geometry.values())

        #ADD MATERIAL
        #ADD NORMALS
        #ADD LIGHTS

        #MAYBE THE TWO MODELS DO NOT INTERACT WITH EACH OTHER, SO PUT ALL OF THEM HERE

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

        chasis_left= dwbles.Model(geometry0_vertex_data[4][1], 
                                  index_data= geometry0_vertex_data[3],
                                  normal_data= geometry0_vertex_data[5][1])
        chasis_left.init_gpu_data(pipeline)

        chasis_left_accessory= dwbles.Model(geometry1_vertex_data[4][1], 
                                            index_data= geometry1_vertex_data[3],
                                            normal_data= geometry1_vertex_data[5][1])
        chasis_left_accessory.init_gpu_data(pipeline)

        # se invierten los indices para que las caras miren hacia afuera,
        # asi el face culling funciona de manera correcta.
        chasis_right= dwbles.Model(geometry0_vertex_data[4][1], 
                                  index_data= geometry0_vertex_data[3][::-1],
                                  normal_data= geometry0_vertex_data[5][1])
        chasis_right.init_gpu_data(pipeline)

        # se invierten los indices para que las caras miren hacia afuera,
        # asi el face culling funciona de manera correcta.
        chasis_right_accessory= dwbles.Model(geometry1_vertex_data[4][1], 
                                            index_data= geometry1_vertex_data[3][::-1],
                                            normal_data= geometry1_vertex_data[5][1])
        chasis_right_accessory.init_gpu_data(pipeline)



        wheel_right_tire= dwbles.Model(geometry2_vertex_data[4][1], 
                                      index_data= geometry2_vertex_data[3],
                                      normal_data= geometry2_vertex_data[5][1])
        wheel_right_tire.init_gpu_data(pipeline)

        wheel_right_frame= dwbles.Model(geometry3_vertex_data[4][1], 
                                       index_data= geometry3_vertex_data[3],
                                       normal_data= geometry3_vertex_data[5][1])
        wheel_right_frame.init_gpu_data(pipeline)
        
        # se invierten los indices para que las caras miren hacia afuera,
        # asi el face culling funciona de manera correcta.
        wheel_left_tire= dwbles.Model(geometry2_vertex_data[4][1], 
                                     index_data= geometry2_vertex_data[3][::-1],
                                     normal_data= geometry2_vertex_data[5][1])
        wheel_left_tire.init_gpu_data(pipeline)

        # se invierten los indices para que las caras miren hacia afuera,
        # asi el face culling funciona de manera correcta.
        wheel_left_frame= dwbles.Model(geometry3_vertex_data[4][1], 
                                      index_data= geometry3_vertex_data[3][::-1],
                                      normal_data= geometry3_vertex_data[5][1])
        wheel_left_frame.init_gpu_data(pipeline)

        move_up= abs(min(wheel_left_tire.position_data[x] for x in 
                         range(1, len(wheel_left_tire.position_data), 3)))
        
        self.car_materials= [dwbles.Material(ambient= [0.03, 0.12, 0.67],
                                             diffuse= [0.67, 0.0, 0.56],
                                             specular= [0.995, 0.99, 0.89],
                                             shininess= 30.0),
                             dwbles.Material(ambient= [0.5, 0.12, 0.32],
                                             diffuse= [0.87, 0.88, 0.08],
                                             specular= [0.12, 0.32, 0.12],
                                             shininess= 3.0),
                             dwbles.Material(ambient= [0.55, 0.76, 0.44],
                                             diffuse= [0.13, 0.01, 0.18],
                                             specular= [0.3, 0.3, 0.88],
                                             shininess= 12.0)
                             ]
        self.current_material_index= 0

        self.const_material= dwbles.Material([0.18, 0.9, 0.9],
                                             [0.01, 0.02, 0.01],
                                             [0.97, 0.95, 0.98],
                                             16)

        ##EVERY NODE SHOULD HAVE MATERIAL

        self.graph= sgraph.SceneGraph(controller) #modified for t2
        self.graph.add_node("chasis",
                            position= [0.0, move_up, 0.0],
                            )

        self.graph.add_node("chasis_left", attach_to= "chasis")
        self.graph.add_node("chasis_left_carcass",
                            attach_to= "chasis_left",
                            mesh= chasis_left,
                            material= self.car_materials[self.current_material_index],
                            pipeline= pipeline,
                            color= color1)
        self.graph.add_node("chasis_left_accessory",
                            attach_to= "chasis_left",
                            mesh= chasis_left_accessory,
                            material= self.const_material,
                            pipeline= pipeline,
                            color= color2)
        
        # notese que los nodos instanciados con los indices invertidos han
        # de reflejar sus vertices con respecto al eje X
        self.graph.add_node("chasis_right", attach_to= "chasis")
        self.graph.add_node("chasis_right_carcass",
                            attach_to= "chasis_right",
                            scale= (-1,1,1),
                            mesh= chasis_right,
                            material= self.car_materials[self.current_material_index],
                            pipeline= pipeline,
                            color= color1)
        self.graph.add_node("chasis_right_accessory", 
                            attach_to= "chasis_right",
                            scale= (-1,1,1),
                            mesh= chasis_right_accessory,
                            material= self.const_material,
                            pipeline= pipeline,
                            color= color2)
        

        
        # por alguna razon la rueda se instancio reflejada al lado del eje X contrario al del 
        # chasis. Esto solo lo supe una vez que la trate de graficar
        self.graph.add_node("tire_right_front",
                            attach_to= "chasis",
                            mesh= wheel_right_tire,
                            material= self.const_material,
                            pipeline= pipeline,
                            color= [0, 0, 0],
                            position= [-0.17, 0.045, -0.28])
        self.graph.add_node("frame_right_front",
                            attach_to= "chasis",
                            mesh= wheel_right_frame,
                            material= self.car_materials[self.current_material_index],
                            pipeline= pipeline,
                            color= [1, 1, 1],
                            position= [-0.17, 0.045, -0.28])
        
        self.graph.add_node("tire_right_back",
                            attach_to= "chasis",
                            mesh= wheel_right_tire,
                            material= self.const_material,
                            pipeline= pipeline,
                            color= [0, 0, 0],
                            position= [-0.17, 0.045, 0.26])
        self.graph.add_node("frame_right_back",
                            attach_to= "chasis",
                            mesh= wheel_right_frame,
                            material= self.car_materials[self.current_material_index],
                            pipeline= pipeline,
                            color= [1, 1, 1],
                            position= [-0.17, 0.045, 0.26])
        
        # notese que los nodos instanciados con los indices invertidos han
        # de reflejar sus vertices con respecto al eje X
        self.graph.add_node("tire_left_front",
                            attach_to= "chasis",
                            mesh= wheel_left_tire,
                            material= self.const_material,
                            pipeline= pipeline,
                            color= [0, 0, 0],
                            position= [0.17, 0.045, -0.28],
                            scale= (-1, 1, 1))
        self.graph.add_node("frame_left_front",
                            attach_to= "chasis",
                            mesh= wheel_left_frame, 
                            material= self.car_materials[self.current_material_index],
                            pipeline= pipeline,
                            color= [1, 1, 1],
                            position= [0.17, 0.045, -0.28],
                            scale= (-1, 1, 1))
        
        self.graph.add_node("tire_left_back",
                            attach_to= "chasis",
                            mesh= wheel_left_tire,
                            material= self.const_material,
                            pipeline= pipeline,
                            color= [0, 0, 0],
                            position= [0.17, 0.045, 0.26],
                            scale= (-1, 1, 1))
        self.graph.add_node("frame_left_back",
                            attach_to= "chasis",
                            mesh= wheel_left_frame, 
                            material= self.car_materials[self.current_material_index],
                            pipeline= pipeline,
                            color= [1, 1, 1],
                            position= [0.17, 0.045, 0.26],
                            scale= (-1, 1, 1))
        
        self.graph.add_node("garage")
        
        self.graph.add_node("spotlight1",
                   pipeline= pipeline,
                   position=[0.0, 0.8, -0.02],
                   rotation= [- (4 * np.pi)/9, 0, 0],
                   light= dwbles.SpotLight(diffuse= [0.89, 0.12, 0.12],
                                           specular= [0.3, 0.0, 0.0]))
        
        self.graph.add_node("spotlight2",
                   pipeline= pipeline,
                   position=[0.0, 0.5, 0.2],
                   rotation= [-np.pi/2, 0, 0],
                   light= dwbles.SpotLight(diffuse= [0.0, 0.67, 0.55],
                                            specular= [0.0, 0.67, 0.43]))
        
        self.graph.add_node("spotlight3",
                   pipeline= pipeline,
                   position=[0.3, 0.5, 0.0],
                   rotation= [-np.pi/2, 0,0, np.pi/4],
                   light= dwbles.SpotLight(diffuse= [0.0, 0.0, 0.93],
                                            specular= [0.0, 0.0, 0.93]))
        
        self.graph.add_node("sun",
                            pipeline= pipeline,
                            light= dwbles.DirectionalLight())

        wall_1_data= shapes.wall_1_geometry(1)
        
        wall_1= dwbles.Model(wall_1_data["position"],
                             normal_data= wall_1_data["normal"],
                             index_data= wall_1_data["indices"])

        self.graph.add_node("wall_1",
                            attach_to= "garage",
                            pipeline= pipeline,
                            position= [0,0,-1], 
                            mesh= wall_1,
                            material= self.const_material,
                            color= [0.5, 0.5, 0,5])
        
        wall_2_data= shapes.wall_2_geometry(1)
        
        wall_2= dwbles.Model(wall_2_data["position"],
                             normal_data= wall_2_data["normal"],
                             index_data= wall_2_data["indices"])

        self.graph.add_node("wall_2",
                            attach_to= "garage",
                            pipeline= pipeline,
                            position= [-1,0,0], 
                            mesh= wall_2,
                            material= self.const_material,
                            color= [0.3, 0.3, 0,3])
        
        floor_data= shapes.floor_geometry(1)
        
        floor= dwbles.Model(floor_data["position"],
                             normal_data= floor_data["normal"],
                             index_data= floor_data["indices"])

        self.graph.add_node("floor",
                            attach_to= "garage",
                            pipeline= pipeline,
                            mesh= floor,
                            material= self.const_material,
                            color= [0.5, 0.5, 0,5])
        
    def draw(self):
        self.graph.draw()

    def update(self, t_time, car_number):
        self.current_material_index= car_number

        self.graph["chasis"]["transform"]= tr.rotationY(1.8 * t_time)

        self.graph["chasis_left_carcass"]["material"]= self.car_materials[self.current_material_index]
        self.graph["chasis_right_carcass"]["material"]= self.car_materials[self.current_material_index]
        self.graph["frame_right_front"]["material"]= self.car_materials[self.current_material_index]
        self.graph["frame_right_back"]["material"]= self.car_materials[self.current_material_index]
        self.graph["frame_left_front"]["material"]= self.car_materials[self.current_material_index]
        self.graph["frame_left_back"]["material"]= self.car_materials[self.current_material_index]  
        
        self.graph["tire_right_front"]["rotation"]= [1.6 * t_time, 0, 0]
        self.graph["frame_right_front"]["rotation"]= [1.6 * t_time, 0, 0]

        self.graph["tire_right_back"]["rotation"]= [1.6 * t_time, 0, 0]
        self.graph["frame_right_back"]["rotation"]= [1.6 * t_time, 0, 0]

        self.graph["tire_left_front"]["rotation"]= [1.6 * t_time, 0, 0]
        self.graph["frame_left_front"]["rotation"]= [1.6 * t_time, 0, 0]

        self.graph["tire_left_back"]["rotation"]= [1.6 * t_time, 0, 0]
        self.graph["frame_left_back"]["rotation"]= [1.6 * t_time, 0, 0]

    # def change_car(self):
    #     self.current_material_index= (self.current_material_index + 1) % 3