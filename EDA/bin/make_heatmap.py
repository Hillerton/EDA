"""
Script used to generate a heatmap over distrubution in a numpy 2D matrix. 
takes a numpy 2D array and bins as input and returnes a base64 html discription of the figure
"""

def plot(array):

    import matplotlib.pylab as plt
    import numpy as np
    import seaborn as sns
    import base64
    from io import BytesIO

    # array = np.random.rand(10,10)
    
    byte_file = BytesIO()

    figure = plt.figure()
    ax = sns.heatmap(array, linewidths=0)

    figure.savefig(byte_file, format="png")

    encod = base64.b64encode(byte_file.getvalue())
    byte_file.close()
    plt.close()
    return(encod)
