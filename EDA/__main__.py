"""
Main script of the EDA tool. Most of the executing code can be found here while several functions are also imported externaly
"""

# general python libraries
import numpy as np
import argparse
import os
import pandas as pd
import scipy.stats

# plugins for the tool
from bin import data_reader

"""
needed functions: 
read all files in a directory. 
import either tab seperated data matrixes or matlab files. 
get data properties such as: 
    Uniq values y
    min y
    max y
    n zeroes y
    mean y
    median y 
    std y  
    variance y
    skewness? y
    number of values in matrix y
    SNR ratio y

plot heatmap on values 
plot distrubutions 

get common values 

get top 5 min and max values for comparison. 

dbscan + isolation forest?

PCA like? 

Once this is all done print the whole thing to html with a page for each data set and a joint distrubution image. 
"""

# SNR calculation based on a now depricated scipy function called signaltonoise 
def snr(a, axis=0, ddof=0):
    a = np.asanyarray(a)
    m = a.mean(axis)
    sd = a.std(axis=axis, ddof=ddof)
    return np.where(sd == 0, 0, m/sd)
    
# capture command line input.
parser = argparse.ArgumentParser(description="Expresion dataset analysis tool. The tool is aimed at capturing and displaying several data properties in a human readble way allowing for greater understanding of the data.")
parser.add_argument("inpt", action="store", help="file or directory with input data. Will read all files in directory ending with .tsv, .csv or .mat. Each file should contain 1 and only 1 gene expression data set")
parser.add_argument("out", action="store", help="Give a name for the HTML report that will be created.")
parser.add_argument("--delim",dest="delimiter", action="store", default="\t", help="Give delimiter to seperate data with if it is not tab")
parser.add_argument("--row_name", dest="row_name", action="store", default="False", help="Set to true to remove row names from tsv or csv file")
parser.add_argument("--col_name", dest="col_name", action="store", default="None", help="Set to true to remove col names from tsv or csv file.")


args = parser.parse_args()

inpt = args.inpt
out = args.out
rm_row_name = args.row_name
rm_col_name = args.col_name
delim = args.delimiter

# check if the input is a directory or a file 
if os.path.isdir(inpt) == True:
    # if it is a directory add all .mat/.csv/.tsv files to the run list 
    file_list = [inpt+f for f in os.listdir(inpt) if f.endswith(".mat") or f.endswith(".csv") or f.endswith(".tsv")]
else:
    # if not simply add the input file to the run list
    file_list = [inpt]

# loop over all files we want to look at here 
for f in file_list:
    # if file is matlab read it using the data reader tool
    if f.endswith(".mat"):
        # read data in to a 2D numpy array 
        data = data_reader.read(f)
    # else use the numpy loadtxt module to move the data to a 2D numpy array

    elif f.endswith(".csv") or f.endswith(".tsv"):

        nrow = None
        if rm_row_name:
            nrow = 0
        ncol = None
        if rm_col_name:
            ncol = 0
        
        df = pd.read_csv(f, sep=delim, header=ncol, index_col=nrow)

        data = df.values
            
        
    # If somehow a file gets past the initial sorting skip it here and print a warning
    else:
        print ("The file",f,"does not look like a .mat, .csv or .tsv file and should have been filtered out.\nStrange things might be going on with the code.")
        continue


    # now do things to the data:
    mean = np.mean(data)
    std = np.std(data)
    median = np.median(data)
    fmax = np.amax(data)
    fmin = np.amin(data)
    fsnr = snr(data)
    uniq = len(np.unique(data))
    counts = data.shape[0]*data.shape[1]
    zeroes = len(np.where(data == 0))
    var = np.var(data)
    skew = scipy.stats.skew(data).mean()
    

    
