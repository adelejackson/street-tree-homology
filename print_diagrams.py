import diode
import dionysus as d
import math
import matplotlib.pyplot as plt
import numpy as np

def plot_diagram(dgm, show = False):
    inf = float('inf')
    min_birth = min(p.birth for p in dgm if p.birth != inf)
    max_birth = max(p.birth for p in dgm if p.birth != inf)
    min_death = min(p.death for p in dgm if p.death != inf)
    max_death = max(p.death for p in dgm if p.death != inf)

    plt.axes().set_aspect('equal', 'datalim')

    min_diag = min(min_birth, min_death)
    max_diag = max(max_birth, max_death)

    plt.scatter([p.birth for p in dgm], [p.death for p in dgm], c='k', marker='.')
    plt.plot([min_diag, max_diag], [min_diag, max_diag], c='k')        # diagonal

    ## clip the view
    margin = (max_birth-min_birth+max_death-min_death)/100
    plt.axes().set_xlim([min_birth-margin, max_birth+margin])
    plt.axes().set_ylim([min_death-margin, max_death+margin])

    if show:
        plt.show()

def plot_bars(dgm, order = 'birth', show = False):
    """Plot the barcode."""

    import matplotlib.pyplot as plt

    if order == 'death':
        generator = enumerate(sorted(dgm, key = lambda p: p.death))
    else:
        generator = enumerate(dgm)

    for i,p in generator:
        plt.plot([p.birth, p.death], [i,i], color = 'b')

    if show:
        plt.show()

num_sam1 = num_sam2 = 10
samples = []
dgms_list = []

for i in range(num_sam1 + num_sam2):
    print(i)
    filename = './samples/samples{:d}.csv'.format(i)
    samples.append(np.genfromtxt(filename, delimiter=','))
    simplices = diode.fill_alpha_shapes(samples[-1])
    f = d.Filtration(simplices)
    m = d.homology_persistence(f)
    dgms = d.init_diagrams(m, f)
    for hom_dim in [0, 1]:
        plot_diagram(dgms[hom_dim], show = False)
        plt.ylabel('Death times')
        plt.xlabel('Birth times')
        plt.title('Persistence diagram for sample {:d}, homology group {:d}'.format(i, hom_dim))
        plt.savefig('./img/dgms/dgm{:d}hom{:d}.pdf'.format(i, hom_dim), bbox_inches='tight')
        plt.clf()
    plot_bars(dgms[1], show = False)
    plt.xlabel('Birth and death times')
    plt.title('Barcode for sample {:d}, first homology group'.format(i))
    plt.savefig('./img/dgms/bars{:d}.pdf'.format(i), bbox_inches='tight')
    plt.clf()
