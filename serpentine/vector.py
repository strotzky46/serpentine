# 

import numpy as np

def norm(vector):
    v = np.atleast_2d(vector)
    abs_v = np.sqrt(np.sum(v**2, axis=1))
    if vector.ndim == 1:
        return abs_v[0]
    else:
        return abs_v

def normalized(vector):
    v = np.atleast_2d(vector)
    v_unit = v / norm(v)[..., np.newaxis]
    if vector.ndim == 1:
        return v_unit[0]
    else:
        return v_unit
    
def dot(vector1, vector2):
    v1 = np.atleast_2d(vector1)
    v2 = np.atleast_2d(vector2)
    dot_product = np.sum(v1*v2, axis=1)
    if (vector1.ndim == 1) and (vector2.ndim == 1):
        return dot_product[0]
    else:
        return dot_product
    
def cross(vector1, vector2):
    v1 = np.atleast_2d(vector1)
    v2 = np.atleast_2d(vector2)
    cross_product = np.array([
        v1[:,1]*v2[:,2] - v1[:,2]*v2[:,1],
        v1[:,2]*v2[:,0] - v1[:,0]*v2[:,2],
        v1[:,0]*v2[:,1] - v1[:,1]*v2[:,0]
    ]).T
    if (vector1.ndim == 1) and (vector2.ndim == 1):
        return cross_product[0]
    else:
        return cross_product