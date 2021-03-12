# need to add:
# way to show SVD
# way to show correlation (some form of heatmap maybe?)

"""
Main script of the EDA tool. Most of the executing code can be found here while several functions are also imported externaly
"""

# general python libraries
import numpy as np
import argparse
import os
import pandas as pd 
import scipy.stats # used to get a number of statistics out from the data
import scipy.io #used to read .mat files 
import json

from jinja2 import FileSystemLoader, Environment # used to generate the html report based on manualy created template files

# plugins for the tool
from bin import data_reader
from bin import make_hist
from bin import make_heatmap
from bin import make_PCA
from bin import make_svd
from bin import make_corr

"""
needed functions: 
 
dbscan

Once this is all done print the whole thing to html with a page for each data set and a joint distrubution image. 
"""

# SNR calculation based on the SNR_wiki function from genespider
def snr(y,p):


    sd = np.zeros(y.shape[0])
    m = np.zeros(y.shape[0])

    for i in range(y.shape[0]):
        cols = np.nonzero(p[i,:])
        work_data = y[:,cols[0]]

        sd[i] = abs(np.std(work_data))
        m[i] = abs(np.mean(work_data))
        
    SNR = round((np.median(m)/np.median(sd)),4)

    return(SNR)
    
# capture command line input.
parser = argparse.ArgumentParser(description="Expresion dataset analysis tool. The tool is aimed at capturing and displaying several data properties in a human readble way allowing for greater understanding of the data.")
parser.add_argument("inpt", action="store", help="file or directory with input data. Will read all files in directory ending with .tsv, .csv or .mat. Each file should contain 1 and only 1 gene expression data set")
parser.add_argument("out", action="store", help="Give a name for the HTML report that will be created.")
parser.add_argument("--delim",dest="delimiter", action="store", default="\t", help="Give delimiter to seperate data with if it is not tab")
parser.add_argument("--row_name", dest="row_name", action="store", default="False", help="Set to true to remove row names from tsv or csv file")
parser.add_argument("--col_name", dest="col_name", action="store", default="None", help="Set to true to remove col names from tsv or csv file.")
parser.add_argument("--form", dest="mat_format", action="store", default="None", help="Set format of any .mat files. Should be h5 or mat.")
parser.add_argument("--desc", dest="description", action="store", default="None", help="Set which data set should be lifted from the matlab file. EG \"Y\" for sub dataset Y")
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
mat_formt = args.mat_format
mat_dataset = args.description


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
    file_list = [inpt+f for f in os.listdir(inpt) if f.endswith(".mat") or f.endswith(".csv") or f.endswith(".tsv") or f.endswith(".json")]
else:
    # if not simply add the input file to the run list
    file_list = [inpt]

tables = list() # create an empty list to store the html objects with stats for each file in file list. This will later be added to the report in a for loop based fashion. 

c = 0
# loop over all files we want to look at here 
for f in file_list:
    with open(f, "r") as json_file:                                                                                                    
        in_data = json.load(json_file)
        # the json files are stored in the format of a nested dict same as for example the Network structure works in genespider 
        express = in_data["obj_data"]["Y"]
        P_mat = np.array(in_data["obj_data"]["P"])    
        df = pd.DataFrame(express)
        data = np.array(express)

        
    #!# parallel testing pretty this up later #!# 
    from multiprocessing import Pool
    pool = Pool(processes=5)
    p1 = pool.apply_async(make_hist.plot, [data])
    p2 = pool.apply_async(make_heatmap.plot, [df])
    p3 = pool.apply_async(make_PCA.plot, [df])
    p4 = pool.apply_async(make_svd.plot, [data])
    p5 = pool.apply_async(make_corr.plot, [data])
    
    pool.close()
    pool.join()
    distrubution = p1.get()
    heat = p2.get()
    pca = p3.get()
    corr = p5.get()

    (svd_tab,svd) = p4.get()
    
    hist_html = None
    heat_html = None
    pca_html = None
    corr_html = None
    
    hist_html = '<img src="data:image/png;base64, {}">'.format(distrubution.decode('utf-8'))
    heat_html = '<img src="data:image/png;base64, {}">'.format(heat.decode('utf-8'))
    pca_html = '<img src="data:image/png;base64, {}">'.format(pca.decode('utf-8'))
    corr_html = '<img src="data:image/png;base64, {}">'.format(corr.decode('utf-8'))
    
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
        snr(data, P_mat), # "snr"
        ]
    }
    stats2_df = pd.DataFrame(stats2, index=['standard deviation', 'variance', 'skewness',  'signal to noise',])
    stats2_html = stats2_df.to_html()

    max_svd = np.max(svd)
    min_svd = np.min(svd)
    med_svd = np.median(svd)

    stats3 = {"value":[
        np.linalg.cond(data),
        max_svd,
        med_svd,
        min_svd
        ]
    }
    stats3_df = pd.DataFrame(stats3, index=['condition value', 'max svd value','median svd value','min svd value'])
    stats3_html = stats3_df.to_html()
    
    
    mat_params = {"value":[
        data.shape[0]*data.shape[1], # "elems"
        len(np.unique(data)), # "uniq"     
        np.count_nonzero(data==0), # "zeroes"
        np.count_nonzero(data), # "nozero"
        ],
        "%":[
            "",
            (len(np.unique(data))/(data.shape[0]*data.shape[1]))*100, # "elems" "uniq"     
            (np.count_nonzero(data==0)/(data.shape[0]*data.shape[1]))*100, # "elems" "zeroes"
            (np.count_nonzero(data)/(data.shape[0]*data.shape[1]))*100, # "elems" "nozero"
        ]
    } 

    mat_df = pd.DataFrame(mat_params, index=('elems', 'uniq', 'zeroes', 'nozero',))
    mat_html = mat_df.to_html()
    
    # add stats and plots to html list one for each file in file_list
    tables.append(stat_section.render(
        file=f,
        t1=mat_html,
        t2=stats1_html,
        t3=stats2_html,
        t4=stats3_html,
        hist=hist_html,
        heat=heat_html,
        pca=pca_html,
        svd=svd_tab,
        corr=corr_html,
        c=c
    ))
    c+=1


writer = open(out, "w+") # open output file for writing
    
# once all files are looped over and printed to html close and write html
writer.write(base.render(
    title=title,
    sections=tables
))

writer.close() # close output file before exiting as I am paranoid. 
