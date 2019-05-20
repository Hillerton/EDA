"""
Script used to generate a heatmap over distrubution in a numpy 2D matrix. 
takes a numpy 2D array and bins as input and returnes a base64 html discription of the figure
"""

def plot(array):

    import matplotlib.pylab as plt
    import numpy as np
    from sklearn.decomposition import PCA
    import base64
    from io import BytesIO
    import pandas as pd
    
    pca = PCA(n_components=2)
    pcomp = pca.fit_transform(array)

    compDf = pd.DataFrame(data = pcomp, columns = ['principal component 1', 'principal component 2'])

    fig = plt.figure(figsize = (8,8))
    ax = fig.add_subplot(1,1,1) 
    ax.set_xlabel('Principal Component 1', fontsize = 15)
    ax.set_ylabel('Principal Component 2', fontsize = 15)
    ax.set_title('2 component PCA', fontsize = 20)

    color = 'black'

    ax.scatter(compDf['principal component 1'],
               compDf['principal component 2'],
               c = color,
               s = 50
    )
    ax.grid()
    
    byte_file = BytesIO()
    plt.savefig(byte_file,format="png")
    
    encod = base64.b64encode(byte_file.getvalue())
    
    return(encod)
