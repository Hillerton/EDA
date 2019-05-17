"""
Small script that is aimed at reading a datafile and passing it on to another script. 
Is built to be imported in to another python script. 
"""

import numpy as np
import h5py

def read(fil, target):

    f = h5py.File(fil,'r')

    data = f.get(target)
    data = np.array(data)

    return (data)
