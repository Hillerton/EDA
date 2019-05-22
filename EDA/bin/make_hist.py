"""
Script used to generate a histogram over distrubution in a numpy 2D matrix. 
takes a numpy 2D array and bins as input and returnes a base64 html discription of the figure
"""

def plot(array):

    import matplotlib.pyplot as plt
    import numpy as np
    import math
    import base64
    from io import BytesIO
    
    plot_ray = array.flatten() # make 2D array 1D 
    bins = math.ceil(len(plot_ray)*0.25) #make % of total numbers as bins

    byte_file = BytesIO()

    plt.hist(plot_ray, bins=bins)
    # plt.show()
    plt.savefig(byte_file, format="png")
    byte_file.seek(0)
    
    encoded = base64.b64encode(byte_file.getvalue())
    byte_file.close()
    plt.close()
    return(encoded)
