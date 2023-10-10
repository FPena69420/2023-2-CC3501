import numpy as np
# import sys

# if sys.path[0] != "":
#     sys.path.insert(0, "")
# sys.path.append('../../')

from grafica import transformations as tr

class Camera:
    def __init__(self, width= 600, height= 600, 
                 position= [1, 0, 0], focus= [0, 0, 0],
                 camera_type = "perspective"):
        self.position = np.array(position, dtype=np.float32)
        self.focus = np.array(focus, dtype=np.float32)
        self.type = camera_type
        self.width = width
        self.height = height

    def update(self):
        pass

    def get_view(self):
        lookAt_matrix = tr.lookAt(self.position, self.focus, np.array([0, 1, 0], dtype=np.float32))
        return np.reshape(lookAt_matrix, (16, 1), order="F")

    def get_projection(self):
        if self.type == "perspective":
            #print(f'width: {self.width}, height: {self.height}')
            perspective_matrix = tr.perspective(90, self.width / self.height, 0.01, 100)
        elif self.type == "orthographic":
            depth = self.position - self.focus
            depth = np.linalg.norm(depth)
            perspective_matrix = tr.ortho(-(self.width/self.height) * depth, (self.width/self.height) * depth, -1 * depth, 1 * depth, 0.01, 100)
        return np.reshape(perspective_matrix, (16, 1), order="F")
    
    def resize(self, width, height):
        self.width = width
        self.height = height

class OrbitCamera(Camera):
    def __init__(self, distance, camera_type = "perspective"):
        super().__init__(camera_type)
        self.distance = distance
        self.phi = 0
        self.theta = np.pi / 2
        self.update()

    def update(self):
        if self.theta > np.pi:
            self.theta = np.pi
        elif self.theta < 0:
            self.theta = 0.0001

        self.position[0] = self.distance * np.sin(self.theta) * np.sin(self.phi)
        self.position[1] = self.distance * np.cos(self.theta)
        self.position[2] = self.distance * np.sin(self.theta) * np.cos(self.phi)