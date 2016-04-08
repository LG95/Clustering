#! /usr/bin/python

from build import bisecting_kmeans, kmeans, INFINITY

def separate(original):
	"""
	Separates words by blanks (space, tab or newline).

	Returns a iteator over each word.

	Input:
		original - string containing the separated words.
	"""

	original += '\n' # ensuring a final word is not forgotten
	word = ''	# currently found word

	for char in original:	# checking each character in original
		if char not in [' ', '\t', '\n']:	# char is not a blank
			word += char	# add char to word

		elif word != '':	# word has characters in it
			yield word 
			word = ''	# reset word

def show_clusters(clusters, records, training, title, id):
	print(title)

	for n, cluster in enumerate(clusters):
		print('Cluster ' + str(n + 1) + ':'),

		for point in cluster:
			print( records[ training.index(point) ][1][id] ),

		print('')
		
	print('')

def main(normalize, filenames):
	"""
	Read attribute description and training set from files. Use them to build
	clusters.

	Input:
		normalize - flag indicating whether training data will be normalized;
		filenames - list with the names of files containing the attribute
	description and the training set.
	"""

	attributes = []	# set of attributes
	records = []	# complete dataset
	training = []	# training set (records with only continuous attributes)

	# extracting the name of each file from filenames
	attribute_filename, train_filename  = filenames

	try:
		with open(attribute_filename) as file:	# on attribute file
			for line in file:	# each line in the file
				words = tuple( separate(line) )	# separate the words on that line
				# add the attribute (name, continuous?, values) to attributes
				attributes.append( (words[0], words[1] == 'continuous', words[1:]) )

	except IOError:	# treat error opening attribute file
		print('Cannot read records without knowing their attributes. ' + attribute_filename + ' could not be opened.')

	try:
		with open(train_filename) as file:	# on training file
			for line in file:	# each line in the file
				train = {}	# training set version of record on this line
				rest = {}	# information not in train

				# match each word in this line to its respective 
				# attribute (based on position), treating word as the
				# value for this attribute in this record
				for attribute, value in zip(attributes, separate(line)):
					# decompose the attribute
					name, continuous, values = attribute

					if continuous:	# continuous attribute
						train[name] = float(value)	# store as float in train

					else:
						rest[name] = value	# store as string in rest

				records.append( (train, rest) )	# add record to records
				training.append(train)	# add train to training

	except IOError:	# treat error opening file
		print('Cannot build clusters without training records. ' + training_filename + ' could not be opened.')

	if attributes != [] and training != []:	# attributes and training set were read
		print('Number of clusters:'),
		k = int( raw_input() )

		if normalize:
			d = len(training[0])	# number of dimensions of training's records
			min_values = [INFINITY] * d	# smallest value for each attribute
			max_values = [-INFINITY] * d	# largest value for each attribute

			for record in training:	# each record
				# value for each attribute and its index
				for i, value in enumerate( record.itervalues() ):
					if value < min_values[i]:	# smaller value found
						min_values[i] = value	# update min_values

					if value > max_values[i]:	# larger value found
						max_values[i] = value	# update max_values

			for record in training:	# each record
				# each element in max_values, min_values and records key value pairs
				for maxv, minv, item in zip(max_values, min_values, record.iteritems()):
					key, value = item	# decompose the key value pair
					record[key] = (value - minv) / (maxv - minv)	# normalize value

		clss = False
		for name, continuous, values in attributes:
			if 'ID' in values:
				id = name

			if name == 'class':
				clss = True

		cs, clusters = kmeans(training, k)
		show_clusters(clusters, records, training, 'K-means', id)

		cs, clusters = bisecting_kmeans(training, k)
		show_clusters(clusters, records, training, 'Bisecting K-means', id)

if __name__ == '__main__':
	from sys import argv

	if len(argv) == 2:	# a single word was passed as an argument
		# add the necessary suffixes to the word
		main(False, [ argv[1] + end for end in ['-attr.txt', '.txt'] ])
		
	# a single word was passed as an argument preceded by normalize or each
	# filename was passed individually
	elif len(argv) == 3:
		if argv[1].lower() == 'normalize':	# first argument is normalize
			# add the necessary suffixes to the word
			main(True, [ argv[2] + end for end in ['-attr.txt', '.txt'] ])

		else:
			main(False, argv[1:])
			

	# each filename was passed individually preceded by normalize
	elif len(argv) == 4:
		main(argv[1].lower() == 'normalize', argv[2:])

	else:	# show help message
		print('Usage: ' + argv[0] + ' [normalize] name')
		print('       ' + argv[0] + ' [normalize] attribute_file training_file\n')
		print('       name: attribute file and training file are, respectively, name-attr.txt and name.txt')