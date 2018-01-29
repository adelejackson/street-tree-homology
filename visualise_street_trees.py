import numpy as np
import holoviews as hv
import math
hv.extension('matplotlib')
hv.opts("Scatter [xaxis=None yaxis=None] (color='k' marker='.' s=1)")
renderer = hv.renderer('matplotlib').instance(fig='pdf', holomap='gif')

sf = False 

if sf:
    tree_file = './san_francisco_street_trees.csv'
else:
    tree_file = './new_york_tree_census_2015.csv'

trees = np.genfromtxt(tree_file, delimiter=',', comments='!')
trees = trees[~np.isnan(trees).any(axis=1)]

# Filter SF trees to just get the inner city
if sf:
    trees = trees[(trees[:,0] > 37.6) & (trees[:,0] < 40)]

# Want to print scatter plot of (longitude, latitude)
for tree in trees:
    tmp = tree[0]
    tree[0] = tree[1]
    tree[1] = tmp

image = hv.Scatter(trees)

filename = ''
if sf:
    filename = './img/sf_scatter'
else:
    filename= './img/ny_scatter'
renderer.save(image, filename)
