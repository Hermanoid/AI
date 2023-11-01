import numpy as np
def num_parameters(shape):
    return int(np.dot(shape[:-1], shape[1:]) + np.sum(shape[1:]))
