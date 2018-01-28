import numpy as np

filename = './processed_data/rank_dist_matrix.csv'
distance_matrix = np.genfromtxt(filename, delimiter=',')

def compute_cost(permutation, distances, n, m):
    cost1 = sum((distances[permutation[i], permutation[j]]) for i in range(n) for j in range(n))
    cost2 = sum((distances[permutation[i], permutation[j]]) for i in range(n, n+m) for j in range(n, n+m))
    return cost1 + cost2

num_perms = 2000
n = m = 10
if n+m != len(distance_matrix):
    raise ValueError('As n and m partition the distance matrix, their sum must be equal to its length.')

rank = 1.0

Perm = [[k] for k in range(n+m)]
originalcost = compute_cost(Perm, distance_matrix, n, m)
print(originalcost)

shuffledTotalDistance = []

for k in range(num_perms-1):
    np.random.shuffle(Perm)
    cost = compute_cost(Perm, distance_matrix, n, m)
    if cost <= originalcost:
        rank += 1
    if k%1000 == 0:
        print(k)

rank /= num_perms
print(rank)
