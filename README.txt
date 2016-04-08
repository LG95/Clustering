To run the code, use 'python main.py' with one, two or three command line arguments.

This code was developed on Ubuntu 14.04.4 LTS and its default python verion (2.7.x) is the most compatible.

Execution requires two files: attribute file, a simple text file containing the name and domain of each attribute, and training file, a simple text file containg any number of lines, each line having one value for each of the attributes described in the attribute file. An attribute's domain may be a sequence with all possible values or the word continuous for real numbers.

A single argument, name, means attribute file and training file are, respectively, name-attr.txt and name.txt.
Two arguments means to normalize and use the second argument as name like above if the first argument is the word normalize (case insensitive). Otherwise, the names for attribute and training file, respectively.
Three arguments specify to normalize and the names for attribute and training file, respectively, only if the first argument is the word normalize (case insensitive).

main.py contains treats the command line arguments, reads the necessary files, reads the k from stdin, calls kmeans and bissecting_kmeans, they displays their output.
build.py contains contains kmeans' and bissecting_kmeans' implementation and the implementation of every helper function they use.
debug.py contains functions to visualize 2D data and clusters formed with it to aid debugging.
