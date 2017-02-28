import json
import os
import pickle
import unittest
from decimal import Decimal as d
from  random import choice
from random import uniform

import networkx as nx
from datetime import datetime

from tsp_application import Christofides, AntColony
from tsp_application import GoogleDistanceMatrixFactory
from tsp_application import algorithms


def mock_shortest_path_metric(n=10, low=1000, hi=5000):

    # A complete Graph with diameter 1
    G = nx.complete_graph(n)

    # Each edge gets a random weight
    for u, v in G.edges_iter():
        G[u][v]["weight"] = int(uniform(low, hi))

    # Compute shortest path for each pair (u,v)
    P = nx.floyd_warshall(G)

    M = {u: dict() for u in G.nodes_iter()}

    # Transform weights into shortest path metric
    for u, v in G.edges_iter():
        M[u][v] = P[u][v]

    return M




class FullStackTest(unittest.TestCase):

    def setUp(self):
        self.factory = GoogleDistanceMatrixFactory("AIzaSyAhv0XHIwkULVVFQFxTDIAFpFxHBB7YHH4")
        self.christo = Christofides()
        self.ants = AntColony()



#    def testPickleAustralia(self):
#        origins = ["Perth, Australia",
#                   "Sydney, Australia",
#                   "Melbourne, Australia", "Adelaide, Australia",
#                   "Brisbane, Australia", "Darwin, Australia",
#                   "Hobart, Australia", "Canberra, Australia"]
#
#        aussis = self.factory.create(origins)
#        assert aussis
#
#        import pickle
#
#        pickle.dump(aussis, open("Australia.pickle", "wb"))


    def testAll(self):

        path = './testsets'

        for fn in os.listdir(path):

                testset = pickle.load(open(os.path.join(path, fn), "rb"))
                assert testset

                start = choice(testset.keys())
                assert start

                results = {
                    "__Meta__": {
                        "Matix": fn,
                        "Start": start
                    }

                }
                for algo in algorithms:
                    l, p = algorithms[algo].solve(start, testset)
                    results[algo] = float(d(l))


                date = datetime.now()

                json.dump(results, open("results/json/%s-%s.json" % (fn,date), "wb"), indent=4, sort_keys=True)
                pickle.dump(results, open("results/pickle/%s-%s.pickle" % (fn,date), "wb"))
                print results



    def OnMockData(self):

        testset = mock_shortest_path_metric()
        assert testset

        start = choice(testset.keys())
        assert start

        results = {
            "__Meta__": {
                "Matix": "Random",
            }

        }
        for algo in algorithms:
            l, p = algorithms[algo].solve(start, testset)
            results[algo] = float(d(l))

        date = datetime.now()

        json.dump(results, open("results/jsonRandom-%s.json" % (date), "wb"), indent=4, sort_keys=True)
        pickle.dump(results, open("results/pickle/Random-%s.pickle" % (date), "wb"))
        print results

if __name__ == '__main__':

    unittest.main()
