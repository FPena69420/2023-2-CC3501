import numpy as np
from OpenGL import GL
# import sys

# if sys.path[0] != "":
#     sys.path.insert(0, "")
# sys.path.append('../../')

class Model():
    def __init__(self, position_data, index_data=None):
        self.position_data = position_data

        self.index_data = index_data
        if index_data is not None:
            self.index_data = np.array(index_data, dtype=np.uint32)

        self.gpu_data = None

    def init_gpu_data(self, pipeline):
        self.pipeline = pipeline
        if self.index_data is not None:
            self.gpu_data = pipeline.vertex_list_indexed(len(self.position_data) // 3, GL.GL_TRIANGLES, self.index_data)
        else:
            self.gpu_data = pipeline.vertex_list(len(self.position_data) // 3, GL.GL_TRIANGLES)
        
        self.gpu_data.position[:] = self.position_data

    def draw(self, mode = GL.GL_TRIANGLES):
        self.gpu_data.draw(mode)