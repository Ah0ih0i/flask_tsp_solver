from itertools import product
from math import fmod

import networkx as nx

from abstract_tsp_solver import AbstractTSPSolver


class Christofides(AbstractTSPSolver):
    """

    Solves metric instances of the TSP problem in O(n^3)
    time with worst case approximation ratio of 1.5

    """

    def options(self):
        return {}

    def info(self):
        return "https://en.wikipedia.org/wiki/christofides_algorithm"


    def __init__(self):
        """

        Creates new Christofides instance

        """
        super(Christofides, self).__init__()
        pass

    def solve(self, s, instance, **options):

        #
        # Christofides' Heuristic works as follows:
        #
        # Given a Graph G it computes the Minimum Spanning Tree T
        #
        # Then all of T's nodes with odd degree are matched.
        # That means, that each odd node is connected with another, s.t. the sum of all these paths is minimal
        # Since there must be an even number of odd nodes, each has a partner.
        #
        # Now all nodes have an even degree and an Euler Circle can be computed (cf. Handshake Lemma)
        # An Euler Circle is a path that uses every edge exactly once
        # (Note, that this is possible iff each degree is even).
        #
        # Lastly any node that appears twice is removed.
        #
        # The resulting path is at most 1.5 times the length of the optimum
        #
        # The algorithm run in O(n^3) where n is the input size
        #


        #Transform instance to nxgraph G
        G = nx.Graph()

        # Iterate over all nodes and their connections
        for u, u_neighbors in instance.items():

            # Add each connection to Graph
            G.add_weighted_edges_from([(u, v, w) for v, w in u_neighbors.items() if u != v])




        # Create Spanning Tree T
        T = nx.minimum_spanning_tree(G)

        # Find all nodes with odd degree.
        V = [u for u in T.nodes() if fmod(T.degree(u), 2) == 1]

        # Reduce G to the Nodes in V:
        # That means all paths that contain nodes, which are not in V, are replaced by a edge with the paths' weight
        G_V = nx.Graph()

        for v, w in product(V, V):
            if v != w:
                weight = nx.dijkstra_path_length(G, v, w)
                # We need the negative weight for the matching in the next step
                G_V.add_edge(v, w, weight=-weight)

        #
        # Since the weights are negated, max_weight_matching  will actually create a min-weight-matching
        # However, we need to set maxcardinality= True,
        # otherwise it will return the empty matching (which has a weight of zero and is therefore the maximum matching)
        #

        # M is a dict of nodes and their matching partners
        M = nx.max_weight_matching(G_V, maxcardinality=True)

        #
        # TuM is the conjunction of T and M
        # It has to be MultiGraph, otherwise we cannot assure its eulerian
        #
        # Example:
        # Assume nodes u and v are of odd degree and the edge {u,v} exists in both T and M
        #
        #

        TuM = nx.MultiGraph(selfloops=False)

        # Add all edges from the matching
        for u, v in M.items():
            weight = G_V.get_edge_data(u, v)["weight"]

            # Only add edges once
            if u not in G_V.neighbors(v):

                # Don't forget to revert weight back to positive value
                TuM.add_edge(u, v, weight= -weight)

        # Add all edges from the matching
        for u in T.nodes_iter():
            for v in T.neighbors_iter(u):
                weight = T.get_edge_data(u, v)["weight"]

                TuM.add_edge(u, v, weight=weight)


        # Construct the Euler Circut on TuM
        Euler = [u for u, v in nx.eulerian_circuit(TuM, source=s)]

        # TSP holds our solution path
        TSP = [s]

        #length of the solution path
        l = 0

        # Current Node in the Hamilton Path
        current = s

        # Iterate over each edge in the path
        for v in Euler:

            # Compute shortcut for each node we've not yet visited
            if v not in TSP:

                # Always take the shortest path from the current position
                # Dijkstra runs in O(n^2) and we execute it n times, so this says in bound
                l += nx.dijkstra_path_length(TuM, current, v)

                # Update Path and current location
                current = v
                TSP.append(v)

        # Lastly, go back to start!
        l += nx.dijkstra_path_length(TuM, current, s)

        return l, TSP

