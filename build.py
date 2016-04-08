INFINITY = float('infinity')	# infinity constant

def bisecting_kmeans(records, k):
	n = len(records)	# number of records

	if 0 < k <= n:	# k is valid
		clusters = [records]	# list of clusters
		centroids = find_centroids(records, clusters)	# centroids for clusters

		while len(clusters) < k:	# clusters does not have k elements
			best_centroids = None	# centroids for best_clusters
			best_clusters = None	# best bisection of clusters
			min_sse = INFINITY 	# sse of best_clusters
			target = None	# cluster to be bisected
			max_sse = 0	# largest sse of a single cluster

			# all centroid cluster pairs and their indexes
			for i, pair in enumerate( zip(centroids, clusters) ):
				centroid, cluster = pair	# decompose pair
				s = sse(centroid, cluster)	# the pair's sse

				if s > max_sse:	# larger sse found
					max_sse = s	# update max_sse
					target = i	# update target

			centroids.pop(target)	# remove the worst cluster's centroid
			target = clusters.pop(target)	# remove the worst cluster

			for _ in range(10):	# ten trials
				# bisect target with k-means 
				new_centroids, new_clusters = kmeans(target, 2)
				# find the bisection's sse
				s = sum( map(sse, new_centroids, new_clusters) )

				if s < min_sse:	# smaller sse found
					best_centroids = new_centroids	# update best_centroids
					best_clusters = new_clusters	# update best_clusters
					min_sse = s	# update min_sse

			# add the bisection's centroids to centroids
			centroids.extend(best_centroids)
			# add the bisection's clusters to clusters
			clusters.extend(best_clusters)

		return centroids, clusters
		
def sse(centroid, cluster):
	# the squared error from point p to centroid
	f = lambda p: distance(centroid.itervalues(), p.itervalues()) ** 2

	return sum( map(f, cluster) )	# sum of f for each point in cluster

def kmeans(records, k):
	from random import SystemRandom

	# pick n unique random points from sequence using the random generator gen
	def sample(sequence, n, gen = SystemRandom()):
		return gen.sample(sequence, n)

	n = len(records)	# number of records

	if 0 < k <= n:	# k is valid
		clusters = None	# generated clusters
		prevoius_centroids = None	# previous iteration's centroids
		centroids = sample(records, k)	# centroids for clusters

		while centroids != prevoius_centroids:	# centroids changed
			prevoius_centroids = centroids	# update previous_centroids
			# reassign records into clusters according to centroids
			clusters = assign_clusters(records, centroids)
			# update centroids according to clusters
			centroids = find_centroids(records, clusters)

		return centroids, clusters

def assign_clusters(records, centroids):
	clusters = map(lambda x: [], centroids)	# assigned clusters

	for record in records:	# each record
		min_distance = INFINITY	# smallest distance to some centroid
		min_index = None	# index of the closest centroid

		# each centroid and its index
		for i, centroid in enumerate(centroids):
			# the distance between record and centroid
			d = distance(record.itervalues(), centroid.itervalues())

			if d < min_distance:	# closer centroid found
				min_distance = d	# update min_distance
				min_index = i 	# update min_index

		# add record to the cluster min_index
		clusters[min_index].append(record)

	return clusters

def find_centroids(records, clusters):
	d = len(records[0])	# number of dimensions per record
	centroids = []	# centroids for the given clusters

	for cluster in clusters:	# each cluster
		m = len(cluster)	# size of cluster
		centroid = [0] * d	# cluster's centroid

		for point in cluster:	# each point
			# add the value for each coordinate of point to the corresponding
			# coordinate in centroid
			centroid = map(lambda x, y: x + y, centroid, point.itervalues())

		# divide each of centroids coordinates by m to get average
		centroid = map(lambda c: float(c) / m, centroid)
		# add centroid to centroids after mapping the appropriate keys from records
		centroids.append( dict( zip(records[0].iterkeys(), centroid) ) )

	return centroids

def distance(p1, p2):
	from math import sqrt

	# the square root of the sum of the square of each difference of
	# corresponding coordinates
	return sqrt( sum( map(lambda c1, c2: (c2 - c1) ** 2, p1, p2) ) )