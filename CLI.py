from tsp_application import GoogleDistanceMatrixFactory
from tsp_application import algorithms
import sys

factory = GoogleDistanceMatrixFactory("AIzaSyAhv0XHIwkULVVFQFxTDIAFpFxHBB7YHH4")

print "Welcome to the TSP Solver"
print 'Your queries are', str(sys.argv[1:])

matrix = factory.create(sys.argv[1:])
if not matrix:
    print "Google didn't find the places"
    sys.exit(0)

start = matrix.keys()[0]


for algo in algorithms:
    print algo, " started"
    l, p = algorithms[algo].solve(start, matrix)
    print algo, " computed length ", l
    print algo, " computed path ", p
