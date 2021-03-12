"""
Script used to generate a heatmap over distrubution in a numpy 2D matrix. 
takes a numpy 2D array and bins as input and returnes a base64 html discription of the figure
"""

def plot(array):

    import seaborn as sns
    import matplotlib.pylab as plt
    import numpy as np
    import base64
    from io import BytesIO

    byte_file = BytesIO()

    data = np.corrcoef(array)

    figure = plt.figure()
    ax = sns.heatmap(data, linewidths=0)

    figure.savefig(byte_file, format="png")

    encod = base64.b64encode(byte_file.getvalue())
    byte_file.close()
    plt.close()
    return(encod)
    
