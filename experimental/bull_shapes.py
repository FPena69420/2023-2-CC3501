import numpy as np

class Bull_shape:
    def __init__(self, vertices, colores, indices):
        self.vertices = vertices
        self.vertices_num= np.uint32(len(vertices)/3.0)
        self.colores= colores
        self.colores_num= np.uint32(len(colores)/3.0)
        self.indices = indices

    def __str__(self):
        return f'{self.vertices_num} vertices: {self.vertices}\n \
            {self.colores_num} colores: {self.colores}\n \
                indices: {self.indices}'
    
def createFacetedCube():

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #    positions        colors
        -0.5, -0.5,  0.5, 
         0.5,  0.5,  0.5,   
        -0.5,  0.5,  0.5,   ###BACK
        -0.5, -0.5,  0.5, 
         0.5, -0.5,  0.5, 
         0.5,  0.5,  0.5, 

         0.5, -0.5,  0.5,   ###RIGHT
         0.5,  0.5, -0.5, 
         0.5,  0.5,  0.5, 
         0.5, -0.5,  0.5, 
         0.5, -0.5, -0.5, 
         0.5,  0.5, -0.5,

         0.5,  0.5,  -0.5, 
        -0.5,  0.5, -0.5,   ###UP
         0.5,  0.5,  0.5, 
         0.5,  0.5,  0.5, 
        -0.5,  0.5, -0.5, 
        -0.5,  0.5,  0.5,

        -0.5, -0.5, -0.5,   ###FRONT
         0.5,  0.5, -0.5, 
        -0.5,  0.5, -0.5, 
        -0.5, -0.5, -0.5, 
         0.5, -0.5, -0.5, 
         0.5,  0.5, -0.5,

        -0.5, -0.5,  0.5, 
        -0.5,  0.5, -0.5,    ###LEFT
        -0.5,  0.5,  0.5, 
        -0.5, -0.5,  0.5, 
        -0.5, -0.5, -0.5, 
        -0.5,  0.5, -0.5,

         0.5, -0.5,  -0.5, 
        -0.5, -0.5, -0.5,    ##DOWN
         0.5, -0.5,  0.5, 
         0.5, -0.5,  0.5, 
        -0.5, -0.5, -0.5, 
        -0.5, -0.5,  0.5]
    
    colores= [
        1.0, 0.0, 0.0,
        1.0, 0.0, 0.0,
        1.0, 0.0, 0.0,
        1.0, 0.0, 0.0,
        1.0, 0.0, 0.0,
        1.0, 0.0, 0.0,

        0.0, 1.0, 0.0,
        0.0, 1.0, 0.0,
        0.0, 1.0, 0.0,
        0.0, 1.0, 0.0,
        0.0, 1.0, 0.0,
        0.0, 1.0, 0.0,

        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,

        0.0, 0.0, 0.0,
        0.0, 0.0, 0.0,
        0.0, 0.0, 0.0,
        0.0, 0.0, 0.0,
        0.0, 0.0, 0.0,
        0.0, 0.0, 0.0,

        0.5, 0.0, 0.5,
        0.5, 0.0, 0.5,
        0.5, 0.0, 0.5,
        0.5, 0.0, 0.5,
        0.5, 0.0, 0.5,
        0.5, 0.0, 0.5,

        0.0, 0.5, 0.5,
        0.0, 0.5, 0.5,
        0.0, 0.5, 0.5,
        0.0, 0.5, 0.5,
        0.0, 0.5, 0.5,
        0.0, 0.5, 0.5]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = range(36)

    return Bull_shape(vertices, colores, indices)