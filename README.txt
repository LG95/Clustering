To run the code, use 'python main.py' with one, two or three command line arguments. Python version 2.7.x is assumed.
A single argument, name, means attribute file and training file are, respectively, name-attr.txt and name.txt.
Two arguments means to normalize and use the second argument as name like above if the first argument is the word normalize (case insensitive). Otherwise, the names for attribute and training file, respectively.
Three arguments specify to normalize and the names for attribute and training file, respectively, only if the first argument is the word normalize (case insensitive).

main.py contains treats the command line arguments, reads the necessary files, reads the k from stdin, calls kmeans and bissecting_kmeans, they displays their output.
build.py contains contains kmeans' and bissecting_kmeans' implementation and the implementation of every helper function they use.