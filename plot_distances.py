import math
import matplotlib.pyplot as plt
import numpy as np

c = np.genfromtxt('./processed_data/dist_matrix.csv', delimiter=',')
x = np.arange(0, 21, 1)
y = np.arange(0, 21, 1)
fig = plt.figure()
ax = plt.subplot(111)
pc = ax.pcolor(x, y, c.T)
ax.set_xlim(x[0], x[-1])
ax.set_ylim(y[0], y[-1])
plt.colorbar(pc)
plt.ylabel('Sample number')
plt.xlabel('Sample number')
#plt.title('Heat map of L2 distances between rank functions and the average rank function')
plt.title('Colormap of q=1 Wasserstein distances between persistence diagrams')
plt.draw()
plt.savefig('./img/distances.pdf', bbox_inches='tight')
