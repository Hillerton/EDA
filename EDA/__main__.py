"""
Main script of the EDA tool. Most of the executing code can be found here while several functions are also imported externaly
"""

# general python libraries
import numpy as np
import argparse
import os
import pandas as pd 
import scipy.stats # used to get a number of statistics out from the data
from jinja2 import FileSystemLoader, Environment # used to generate the html report based on manualy created template files

# plugins for the tool
from bin import data_reader
from bin import make_hist
from bin import make_heatmap
from bin import make_PCA


"""
needed functions: 
 
dbscan

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
parser.add_argument("-t", dest="title", action="store", default="", help="Set title for html file.")
parser.add_argument("-n", dest="limit", action="store", default=False, help="Give a value to limit columns and rows by.")

args = parser.parse_args()

inpt = args.inpt
out = args.out
rm_row_name = args.row_name
rm_col_name = args.col_name
delim = args.delimiter
title=args.title
n = args.limit

script_path = os.path.abspath(__file__) # get the path to where this script is to find templates
script_path = script_path[0:-11]

# Configure Jinja and ready the loader
env = Environment(loader=FileSystemLoader(searchpath=script_path+"templates"))

# set up the templates used for adding to the file
base = env.get_template("base_report.html")
stat_section = env.get_template("stats_and_images.html")


# check if the input is a directory or a file 
if os.path.isdir(inpt) == True:
    # if it is a directory add all .mat/.csv/.tsv files to the run list 
    file_list = [inpt+f for f in os.listdir(inpt) if f.endswith(".mat") or f.endswith(".csv") or f.endswith(".tsv")]
else:
    # if not simply add the input file to the run list
    file_list = [inpt]

tables = list() # create an empty list to store the html objects with stats for each file in file list. This will later be added to the report in a for loop based fashion. 

c = 0
# loop over all files we want to look at here 
for f in file_list:
    # if file is matlab read it using the data reader tool
    if f.endswith(".mat"):
        # read data in to a 2D numpy array 
        #data = data_reader.read(f)
        continue

    elif f.endswith(".csv") or f.endswith(".tsv"):

        nrow = None
        if rm_row_name:
            nrow = 0
        ncol = None
        if rm_col_name:
            ncol = 0
        
        df = pd.read_csv(f, sep=delim, header=ncol, index_col=nrow)

        df = df.replace([np.inf, -np.inf], 0) #remove any inf or -inf as these can not be ploted due to unlimited axises not being allowed in python

        if n:
            print ("cutting down array to size",str(n)+" by "+str(n))
            df = df.head(int(n)) # get the first n rows
           
            df = df[df.columns[1:int(n)+1]] #get the first n columns OBS as this is none inclusive add +1 to n to get n columns. Else returns n-1 columns 
        
        data = df.values
            
        
    # If somehow a file gets past the initial sorting skip it here and print a warning
    else:
        print ("The file",f,"does not look like a .mat, .csv or .tsv file and should have been filtered out.\nStrange things might be going on with the code.")
        continue

    distrubution = None
    heat = None
    pca = None
    
    # plot figs for data and store as str64 to later add to the html file 
    distrubution = make_hist.plot(data) # returns a base64 encoded html object depicting a histogram over distrubtutions
    heat = make_heatmap.plot(df) # returns a base64 html object contaning a heatmap over value distrubtutions in data
    pca = make_PCA.plot(df)# returns a 2D pca plot as a base64 html object for printing

    
    
    # now do things to the data:
    stats1 = {"value":[
        np.mean(data), # "mean"
        np.median(data), # "median"
        np.amax(data), # "max"
        np.amin(data), # "min"
        ]
    }

    stats1_df = pd.DataFrame(stats1, index=['mean', 'median', 'max', 'min',])
    stats1_html = stats1_df.to_html()

    stats2 = {"value":[
        np.std(data), # "std"
        np.var(data), # "variance"
        scipy.stats.skew(data).mean(), #"skew"
        snr(data).mean(), # "snr"
        ]
    }

    stats2_df = pd.DataFrame(stats2, index=['standard deviation', 'variance', 'skewness',  'signal to noise',])
    stats2_html = stats2_df.to_html()
    
    
    mat_params = {"value":[
        data.shape[0]*data.shape[1], # "elems"
        len(np.unique(data)), # "uniq"     
        len(np.where(data == 0)), # "zeroes"
        (data.shape[0]*data.shape[1])-len(np.where(data == 0)), # "nozero"
        ],
        "%":[
            "",
            len(np.unique(data))/data.shape[0]*data.shape[1], # "elems" "uniq"     
            len(np.where(data == 0))/data.shape[0]*data.shape[1], # "elems" "zeroes"
            (data.shape[0]*data.shape[1])-len(np.where(data == 0))/data.shape[0]*data.shape[1], # "elems" "nozero"
        ]
    } 

    mat_df = pd.DataFrame(mat_params, index=('elems', 'uniq', 'zeroes', 'nozero',))
    mat_html = mat_df.to_html()
    
    hist_html = None
    heat_html = None
    pca_html = None
      
    hist_html = '<img src="data:image/png;base64, {}">'.format(distrubution.decode('utf-8'))
    heat_html = '<img src="data:image/png;base64, {}">'.format(heat.decode('utf-8'))
    pca_html = '<img src="data:image/png;base64, {}">'.format(pca.decode('utf-8'))
    # pearson 
    # spearman 

    # add stats and plots to html list one for each file in file_list
    tables.append(stat_section.render(
        file=f,
        t1=mat_html,
        t2=stats1_html,
        t3=stats2_html,
        hist=hist_html,
        heat=heat_html,
        pca=pca_html,
        c=c
    ))
    c+=1


writer = open(out, "w+") # open output file for writing
    
# once all files are looped over and printed to html close and write html
writer.write(base.render(
    title=title,
    sections=tables
))

writer.close() # close output fiel before exiting as I am paranoid. 
