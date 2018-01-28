import numpy as np
import diode as diode
import dionysus as d
import math
import matplotlib.pyplot as plt

num_samples = 10
num_points = 1000
homology_dimension = 1

def get_distance(origin, destination):
    return math.sqrt(np.sum([(origin[i]-destination[i])**2 for i in range(3)]))

def polar_to_cartesian(lat_deg, lng_deg):
    r = 6371
    lat = math.radians(lat_deg)
    lng = math.radians(lng_deg)
    x = r*math.cos(lat)*math.cos(lng)
    y = r*math.cos(lat)*math.sin(lng)
    z = r*math.sin(lat)
    return [x, y, z]

samples = []

for sf in [False, True]:
    print(sf)
    if sf:
        tree_file = './san_francisco_street_trees.csv'
    else:
        tree_file = './new_york_tree_census_2015.csv'

    polar_trees = np.genfromtxt(tree_file, delimiter=',', comments='!')
    polar_trees = polar_trees[~np.isnan(polar_trees).any(axis=1)]

    if sf:
        polar_trees = polar_trees[(polar_trees[:,0] > 37.6) & (polar_trees[:,0] < 40)]

    trees = []
    for tree in polar_trees:
        trees.append(polar_to_cartesian(tree[0], tree[1]))
    trees = np.array(trees)
    print(len(trees))
    base_points = []
    while len(base_points) < num_samples:
        tree = trees[np.random.choice(len(trees))]
        if len(base_points) == 0 or np.min([get_distance(other_point, tree) for other_point in base_points]) > 0.45:
            base_points.append(tree)
    base_points = np.array(base_points)

    for point in base_points:
        distances = [get_distance(other_point, point) for other_point in trees]
        trees = trees[np.argpartition(distances, num_points)]
        samples.append(trees[:num_points])
        print (np.max([get_distance(other_point, point) for other_point in trees[:num_points]]))

samples = np.asarray(samples)

for i in range(len(samples)):
    np.savetxt('./samples/samples{:d}.csv'.format(i), samples[i], delimiter=',')

dgms_list = []
for i in range(len(samples)):
    sample_set = samples[i]
    simplices = diode.fill_alpha_shapes(sample_set)
    f = d.Filtration(simplices)
    m = d.homology_persistence(f)
    dgms = d.init_diagrams(m, f)
    dgms_list.append(dgms[homology_dimension])
print(dgms_list)

distance_matrix = np.zeros((len(dgms_list), len(dgms_list)))
for i in range(len(dgms_list)):
    print(i)
    for j in range(i):
        dist = d.wasserstein_distance(dgms_list[i], dgms_list[j], q=1)
        distance_matrix[i, j] = dist
        distance_matrix[j, i] = distance_matrix[i, j]

np.savetxt('./processed_data/dist_matrix.csv', distance_matrix, delimiter=',')
