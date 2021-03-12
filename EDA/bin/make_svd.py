"""
Script used to generate a histogram over distrubution in a numpy 2D matrix. 
takes a numpy 2D array and bins as input and returnes a base64 html discription of the figure
"""

def plot(array):
    

    import numpy as np
    import pandas as pd

    # caluclate the singular values for the input data
    plot_ray = np.linalg.svd(array, compute_uv=False)

    svd = plot_ray
    
    # calculate how many columns will be needed 
    cols_needed=(len(plot_ray)%100)
    
    # if we can not get a int number for columns continue adding an empty cell untill we can 
    if cols_needed == 0:
        cols_needed = 1
        
    while len(plot_ray)%cols_needed != 0:
            apends = [" "]
            plot_ray = np.append(plot_ray, apends)
            cols_needed=(len(plot_ray)%100)
    
    # based on the calculted number of columns reshape the data in as many rows need, columns
    plot_ray= plot_ray.reshape(-1,cols_needed)

    # make a pandas dataframe to convert the whole thing to html easily 
    df = pd.DataFrame(plot_ray)
    # conver to html and return the html object 
    df = df.to_html()

    return (df,svd)
