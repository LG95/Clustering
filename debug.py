from build import *
from matplotlib.pyplot import plot, show

def show_graph(clusters, centroids):
	for color, centroid, points in zip('rgbcymk', centroids, clusters):
		xs = map(lambda e: e['x'], points)
		ys = map(lambda e: e['y'], points)
		plot(xs, ys, color + 'o')
		plot(centroid['x'], centroid['y'], color + 'x', ms = 10)

	show()