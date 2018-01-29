import diode
import dionysus as d
import math
import matplotlib.pyplot as plt
import numpy as np

samples = []
dgms_list = []
homology_dimension = 1
num_sam1 = 10
num_sam2 = 10

birth_max = 0.0
death_max = 0.0

def get_rankval(rankfun, key):
    """ Allows for compression of rankfun by dropping zero-valued points"""
    if key in rankfun:
        return rankfun[key]
    else:
        return 0

def eval_rank_fun(bvals, dvals, dgm):
    countKeys = [(b,d) for b in bvals for d in dvals if d >= b ]
    rankfun = { ck: 0 for ck in countKeys }
    for pt in dgm:
        for (b, d) in countKeys:
            if (b >= pt.birth and d <= pt.death):
                rankfun[(b,d)] += 1
    return rankfun

def weight_fun(bvals, dvals, grid):
    countKeys = [(b,d) for b in bvals for d in dvals if d >= b ]
    box_area = grid*grid
    A = 1e5
    weightfun ={(b,d): box_area*math.exp(A*(b-d)) for (b,d) in countKeys } 
    max_death = max(dvals)
    weightfun.update({(b,max_death): box_area*math.exp(b-max_death)/(1-math.exp(-grid)) for b in bvals})
    return weightfun

def plot_rank(rankFunc,**kwargs):
    # rankFunc is a dictionary of {(birth,death) : number } form

    births = set([b for (b,d) in rankFunc.keys()])
    deaths = set([d for (b,d) in rankFunc.keys()])

    bvals = list(births)
    dvals = list(deaths)
    bvals.sort()
    dvals.sort()

    x_bin_length = bvals[1] - bvals[0]  # this recovers the grid size
    x_offset = x_bin_length/2.0
    y_bin_length = dvals[1] - dvals[0]
    y_offset = y_bin_length/2.0

    x = np.arange(bvals[0]-x_offset,bvals[-1]+x_bin_length,x_bin_length)
    y = np.arange(dvals[0]-y_offset,dvals[-1]+y_bin_length,y_bin_length)

    c = np.zeros((len(bvals),len(dvals)))
    for i in range(len(bvals)):
        for j in range(len(dvals)):
            if dvals[j] >= bvals[i]:
                c[i,j] = rankFunc[(bvals[i],dvals[j])]

    fig = plt.figure()
    ax  = plt.subplot(111)
    pc = ax.pcolormesh(x,y,c.T,**kwargs)
    ax.set_xlim(x[0],x[-1])
    ax.set_ylim(y[0],y[-1])
    plt.colorbar(pc)
    plt.draw()
    return pc

def L2RankDist(rankA, rankB, weightfun):
    diff = {key: get_rankval(rankA, key)-get_rankval(rankB, key) for key in weightfun}
    return sum( math.pow(diff[key],2)*weightfun[key] for key in weightfun)

for i in range(num_sam1 + num_sam2):
    filename = './samples/samples{:d}.csv'.format(i)
    samples.append(np.genfromtxt(filename, delimiter=','))
    simplices = diode.fill_alpha_shapes(samples[-1])
    f = d.Filtration(simplices)
    m = d.homology_persistence(f)
    dgms = d.init_diagrams(m, f)
    dgms_list.append(dgms[homology_dimension])
    local_birth_max = np.max([pt.birth for pt in dgms[homology_dimension]])
    birth_max = max(birth_max, local_birth_max)
    local_death_max = np.max([pt.death for pt in dgms[homology_dimension]])
    death_max = max(death_max, local_death_max)

grid = (birth_max+death_max)/100
rankfuns = []

for dgm in dgms_list:
    print(dgm)
    bvals = np.arange(0.0, np.max([pt.birth for pt in dgm]), grid)
    dvals = np.arange(0.0, np.max([pt.death for pt in dgm]), grid)
    print(len(bvals), len(dvals))
    rankfun = eval_rank_fun(bvals, dvals, dgm)
    rankfuns.append(rankfun)
    print(np.max([value for key, value in rankfun.items()]))
    #pr = plot_rank(rankfun,cmap='Reds',vmin=0, vmax=30)
    #plt.show()

samples = np.array(samples)

averagerankfuns = []
bvals = np.arange(0.0, birth_max, grid)
dvals = np.arange(0.0, death_max, grid)

for i in [0, num_sam1]:
    countKeys = [(b,d) for b in bvals for d in dvals if d >= b ]
    print(rankfun[countKeys[0]])
    averagerankfun = { ck: np.mean([get_rankval(rankfun, ck) for rankfun in rankfuns[i:i+num_sam2]]) for ck in countKeys }
    averagerankfuns.append(averagerankfun)

weightfun = weight_fun(bvals, dvals, grid)
distance_matrix = np.zeros((len(rankfuns), len(rankfuns)))
for i in range(len(rankfuns)):
    print(i)
    for j in range(i):
        dist = L2RankDist(rankfuns[i], rankfuns[j], weightfun)
        distance_matrix[i, j] = dist
        distance_matrix[j, i] = distance_matrix[i, j]

np.savetxt('./processed_data/rank_dist_matrix.csv', distance_matrix, delimiter=',')

dist_to_average = np.zeros((len(rankfuns), len(averagerankfuns)))
for j in range(len(averagerankfuns)):
    for i in range(len(rankfuns)):
        dist = L2RankDist(averagerankfuns[j], rankfuns[i], weightfun)
        dist_to_average[i, j] = dist

np.savetxt('./processed_data/average_rank_dist_matrix.csv', dist_to_average, delimiter=',')

