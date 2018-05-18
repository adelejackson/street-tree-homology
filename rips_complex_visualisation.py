#!/usr/bin/env python3

from matplotlib import pyplot as plt
from matplotlib import patches as ptch
from matplotlib.widgets import Slider
from math import sqrt
import numpy as np

# Use tableau 20 colors
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r/255., g/255., b/255.)

class RipsComplex:
    """Class to track a rips complex.
    https://en.wikipedia.org/wiki/Vietoris%E2%80%93Rips_complex """
    def __init__(self, points, ax, radius=0, point_colour=tableau20[4],
            edge_colour=tableau20[0], circle_colour=tableau20[1],
            fill_colour=tableau20[9]):
        self.ax = ax
        self.point_colour = point_colour
        self.edge_colour = edge_colour
        self.circle_colour = circle_colour
        self.fill_colour = fill_colour
        self.points = list()
        self.circles = list()
        self.edges = list()
        self.triangles = list()
        self.radius = radius
        for i in range(len(points.get_xdata())):
            self.add_point(points.get_xdata[i], points.get_ydata[i])
        self.cid = points.figure.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        if event.inaxes!=self.ax.axes: return
        self.add_point(event.xdata, event.ydata)

    def add_point(self, x, y):
        new_circle = ptch.Circle((x, y), self.radius, fc=self.circle_colour,
                alpha=0.3)
        self.circles.append(new_circle)
        self.ax.add_patch(new_circle)
        for edge in self.edges:
            triangle = ptch.Polygon(np.vstack((edge.get_xydata(),
                np.array([x, y]))), color='none', alpha=0.4, ec='none')
            self.triangles.append(triangle)
            self._update_triangle(triangle)
            self.ax.add_patch(triangle)
        for point in self.points:
            edge, = self.ax.plot([point[0], x], [point[1], y], c='none',ls='-')
            self.edges.append(edge)
            self._update_edge(edge)
        self.ax.plot([x], [y], c=self.point_colour, marker='o', ls=None)
        self.points.append((x, y))
        plt.draw()

    def set_radius(self, r):
        self.radius = r
        for edge in self.edges:
            self._update_edge(edge)
        for triangle in self.triangles:
            self._update_triangle(triangle)
        for circle in self.circles:
            self._update_circle(circle)

    def _update_triangle(self, triangle):
        if self._check_triangle_valid(triangle):
            triangle.set_color(self.fill_colour)
        else:
            triangle.set_color('none')

    def _update_edge(self, edge):
        if self._edge_length(edge.get_xydata()) < 2*self.radius:
            edge.set_c(self.edge_colour)
        else:
            edge.set_c('none')

    def _update_circle(self, circle):
        circle.set_radius(self.radius)

    def _edge_length(self, xy):
        return sqrt((xy[0][0]-xy[1][0])**2 + (xy[0][1]-xy[1][1])**2)
    
    def _check_triangle_valid(self, triangle):
        points = triangle.get_xy()
        for i in range(3):
            if self._edge_length(np.vstack((points[i], 
                points[i+1]))) > 2*self.radius:
                return False
        return True


fig = plt.figure(figsize=(7.5, 7.5))
ax = fig.add_subplot(111)
ax.set_aspect('equal')
ax.set_xlim([0, 5])
ax.set_ylim([0, 5])
fig.subplots_adjust(left=0.15, bottom=0.25)

for i in ax.spines.values():
    i.set_color(tableau20[15])
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)

axRadius = plt.axes([0.15, 0.1, 0.65, 0.03])

ax.set_title('Click to add points')
ax.autoscale(enable=False)
points, = ax.plot([], [], 'o', c=tableau20[4])  # empty 
pointbuilder = RipsComplex(points, ax)

sRadius = Slider(axRadius, 'Radius', 0.0, 
        abs(ax.axes.get_ylim()[0]-ax.axes.get_ylim()[1])/2, valinit=0)
sRadius.on_changed(pointbuilder.set_radius)

plt.show()
