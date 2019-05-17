# Expresion dataset analysis (EDA)

Properties of GeneSPIDER synthetic data compared to real data
Starting date: 2019-05
responsible: Thomas Hillerton

Project that aims at comparing gene spider generated data to real data (most likely L1000 data). 

The project idea was formulated around that methods seemed to perform better on geneSPIDER data than real data. Along with that gs data is linear something that likely is not true for actual gene expression data. 

The goal is to check what properties are in common and what are different to determine if the generated data is a good enough model of real data to be usefull as a reprsenative data set.

A good example of what to test can be found here https://nbviewer.jupyter.org/github/JosPolfliet/pandas-profiling/blob/master/examples/meteorites.ipynb.

In addition I would like heatmaps to look for:
- human recognitiable paterns and distrubution over matrix.
- Possibly some metrics for iaa if possible.
- Some form of outlier analysis to see how this looks between the two datasets (possibly dbscan + isolation forest?).
- Maybe a PCA for looking at patterns? 

As a later stage part we can hopefully adjust the gs data to mimic properties that we find differ and that could be relevant to GRNI.
