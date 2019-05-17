"""
Main script of the EDA tool. Most of the executing code can be found here while several functions are also imported externaly
"""

import numpy as np
from bin import data_reader
import argparse
import os

"""
needed functions: 
read all files in a directory. 
import either tab seperated data matrixes or matlab files. 
get data properties such as: 
    Distinct counts
    Uniq values 
    min 
    max 
    n zeroes 
    mean 
    median 
    5h and 95th percentile
    range 
    std 
    cof variation 
    variance 
    Mean Absolute Deviation
    skewness? 
    number of values in matrix 
    SNR ratio
    iaa 

plot heatmap on values 
plot distrubutions 

get common values 

get top 5 min and max values for comparison. 

dbscan + isolation forest?

PCA like? 

Once this is all done print the whole thing to html with a page for each data set and a joint distrubution image. 
"""

# capture command line input.
parser = argparse.ArgumentParser(description="Expresion dataset analysis tool. The tool is aimed at capturing and displaying several data properties in a human readble way allowing for greater understanding of the data.")
parser.add_argument("inpt", action="store", help="file or directory with input data. Will read all files in directory ending with .tsv, .csv or .mat. Each file should contain 1 and only 1 gene expression data set")
parser.add_argument("out", action="store", help="Give a name for the HTML report that will be created.")

args = parser.parse_args()

inpt = args.inpt
out = args.out

# check if the input is a directory or a file 
if os.path.isdir(inpt):
    # if it is a directory add all .mat/.csv/.tsv files to the run list 
    file_list = [f for f in os.listdir(inpt) if f.endswith(".mat") or f.endswith(".csv") or f.endswith(".tsv")]
else:
    # if not simply add the input file to the run list
    file_list = inpt

# loop over all files we want to look at here 
for f in file_list:
    # if file is matlab read it using the data reader tool
    if f.endswith(".mat"):
        # read data in to a 2D numpy array 
        data = data_reader.read(f)
    # else use the numpy loadtxt module to move the data to a 2D numpy array
    elif f.endswith(".csv") or f.endswith(".tsv"):
        data = np.loadtxt(f, delimiter="\t")
        print (data)
        # If somehow a file gets past the initial sorting skip it here and print a warning
    else:
        print ("The file",f,"does not look like a .mat, .csv or .tsv file and should have been filtered out.\nStrange things might be going on with the code.")
        continue


    #now do things to the data:
    

    
