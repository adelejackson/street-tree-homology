import numpy as np

# Set filename to './processed_data/average_rank_dist_matrix.csv to 
# assess functional summary.
filename = './processed_data/dist_matrix.csv'
num_perms = 2000
n = m = 10

def compute_cost(permutation, distances, n, m):
    """ Compute joint loss function of two sets of samples.
    Joint loss function is sum of squared distances in each subset."""
    cost1 = sum((distances[permutation[i], permutation[j]]) for i in range(n) for j in range(n))
    cost2 = sum((distances[permutation[i], permutation[j]]) for i in range(n, n+m) for j in range(n, n+m))
    return cost1 + cost2

distance_matrix = np.genfromtxt(filename, delimiter=',')
if n+m != len(distance_matrix):
    raise ValueError('As n and m partition the distance matrix, their sum must be equal to its length.')

rank = 1.0

perm = [[k] for k in range(n+m)]
originalcost = compute_cost(perm, distance_matrix, n, m)

for k in range(num_perms-1):
    np.random.shuffle(perm)
    cost = compute_cost(perm, distance_matrix, n, m)
    if cost <= originalcost:
        rank += 1
    if k%1000 == 0:
        print(k) # for monitoring progress

rank /= num_perms
print(rank)
