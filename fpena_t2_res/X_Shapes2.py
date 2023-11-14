import numpy as np

def floor_geometry(size):
    return {
    'position': np.array([
    -size, 0.0, -size,
     size, 0.0, -size,
    -size, 0.0,  size,
    
    -size, 0.0,  size,
     size, 0.0, -size,
     size, 0.0,  size,
    ], dtype= np.float32),
    
    'normal': np.array([0,1,0]*6, dtype= np.int32),

    'uv': [0, 0, 1, 0, 1, 1, 0, 1],

    'indices': np.array([5,4,3,2,1,0], dtype= np.int32)
    }

def wall_1_geometry(size):
    return {
    'position': np.array([
    -size,  0.0, 0.0, 
     size,  0.0, 0.0, 
    -size, size, 0.0,

    -size, size, 0.0, 
     size,  0.0, 0.0, 
     size, size, 0.0, 
    ], dtype= np.float32),
    
    'normal': np.array([0,0,1]*6, dtype= np.int32),

    'uv': [0, 0, 1, 0, 1, 1, 0, 1],

    'indices': np.array([0,1,2,3,4,5], dtype= np.int32)
    }

def wall_2_geometry(size):
    return {
    'position': np.array([
    0.0,   0.0, -size,
    0.0,  size, -size,
    0.0,   0.0,  size,

    0.0,   0.0,  size,
    0.0,  size, -size,
    0.0,  size,  size,
    ], dtype= np.float32),
    
    'normal': np.array([1,0,0]*6, dtype= np.int32),

    'uv': [0, 0, 1, 0, 1, 1, 0, 1],

    'indices': np.array([0,1,2,3,4,5], dtype= np.int32)
    }