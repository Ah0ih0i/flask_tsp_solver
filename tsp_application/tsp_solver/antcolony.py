import logging
import random
from decimal import Decimal as d
from multiprocessing import Pool, cpu_count
from sys import maxint

import networkx as nx

from abstract_tsp_solver import AbstractTSPSolver

# Default Values for parameters
RHO_DEFAULT = d(0.4)
ITERATIONS_DEFAULT = 1000
BETA_DEFAULT = d(15)
SMALL_Q_DEFAULT = 0.3

#
# Metaparameters,
# We need to fix some parameters to optimize the rest
# Hence these parameters are set in the constructor

Q_DEFAULT = d(10)
ALPHA_DEFAULT = d(10)
COLONY_SIZE_DEFAULT = d(10)

# Fixed initial values
TAU_INITIAL = d(1)


class AntColony(AbstractTSPSolver):
    """
    This class implements an ACO algorithm to approximate the TSP
    """


    def options(self):
        return {
            "beta": {
                "default" : int(BETA_DEFAULT),
                "min": 1,
                "max": 1000,
                "step": 0.5,
                "name": "Pheromone Weight"
            },
            "rho": {
                "default" : float(RHO_DEFAULT),
                "min": 0,
                "max": 1,
                "step": 0.1,
                "name": "Evaporation Factor"
            },
            "q": {
                "default" : float(SMALL_Q_DEFAULT),
                "min": 0,
                "max": 1,
                "step": 0.1,
                "name": "Exploration Factor"
            },
            "iterations": {
                "default": int(ITERATIONS_DEFAULT),
                "min": 100,
                "max": 1000000,
                "step": 10,
                "name": "Iterations"
            }
        }

    def info(self):
        return "https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms"

    def update_G(self, G, P, rho):
        """
        Updates pherome

        :param G:
        :param P:
        :return:
        """

        assert isinstance(G, nx.Graph)

        #
        # First each egdes gets some pheromone depending on the number of ants which crossed it
        #

        # Iterate over all paths
        for l, path in P:

            # Iterate over all edges in the path
            for e in path:

                # Get data
                edge_ctx = G.get_edge_data(*e)[EdgeContext.KEY]

                # Add pheromone according to path length
                edge_ctx.addPheromone(self.Q/d(l), refresh=False)

        #
        # Then a constant factor evapoates
        #

        # Iterate over all edges in the graph
        for u, v, edge_ctx in G.edges_iter(data=EdgeContext.KEY):

            # Ignore self-edges
            if(u != v):

                assert edge_ctx

                # Let some pheromone evaporate
                edge_ctx.evaporate(rho)


    def __init__(self,
                 alpha=ALPHA_DEFAULT,
                 size=COLONY_SIZE_DEFAULT,
                 Q = Q_DEFAULT
            ):
        super(AntColony, self).__init__()
        self.size = size
        self.alpha = alpha
        self.Q = Q



    def solve(self, s, instance,
              beta=BETA_DEFAULT,
              rho=RHO_DEFAULT,
              q=0.3,
              iterations=ITERATIONS_DEFAULT):

        # Transform instance to proper nxgraph G
        G = nx.Graph()
        for node, neigbors in instance.items():
            G.add_edges_from([
                              (node, n, {
                                  "weight": d(w),
                                  EdgeContext.KEY: EdgeContext(w, self.alpha, beta)
                              }
                               ) for n, w in neigbors.items() if n != node
                            ])

        # Path with minimal length
        p_min = None

        # Length of minimal path
        l_min = maxint

        # Open process pool
        pool = Pool(cpu_count() - 1)

        # I
        for i in range(int(iterations)):

            # Log progress
            logging.info("%s started iteration %d" % (self.name, i))

            # Stores path of each ant
            P = []

            # Stores async results
            futures = []

            # Start 10 async computations
            for i in range(10):
                futures.append(pool.apply_async(Ant, args=(G, s, q, )))


            # Wait for all compuations to stop
            for future in futures:

                # Wait 'till done
                future.wait()

                # Get result
                P.append(future.get())

            # Update Pheromone
            self.update_G(G, P, rho)

            # Update shortest path
            for l, p in P:
                if l < l_min:
                    l_min = l
                    p_min = p

        # Close process pool
        pool.close()

        # Wait for pool to properly shut down
        pool.join()

        # Return best path
        return l_min, [u for u, v in p_min]



def Ant(G,s,q=0.3):
        """

        An Ant is a visitor that searches for the TSP path in the given Graph.

        :param G: A Graph for which we want to solve the TSP. Each edge must have an instance of EdgeContext as an attribute
        :param s: The starting point for the TSP
        :param q: The exploration/expoitation parameter.
        :return:
        """

        def pick_random(edges):
            """
            Picks a random edge according to its weight.

            :param edges: A list of edges together with their edge context
            :return:
            """

            #
            #
            # Here's how it works:
            #
            # First we compute the probability of each element.
            # This is its weight divided by the sum of all weights
            #
            # Now we imagine all these weights summed up in the [0,1] interval.
            #
            # It looks something like this:
            #
            # ++++++++++++++++++++++++++++++++++++++++
            # |         0.5          | 0.25  | 0.25  |
            # ++++++++++++++++++++++++++++++++++++++++
            # 0                                      1
            #
            # If we now randomly pick a number in the interval,
            # the probility that the number is in a certain interval is
            # exactly the probability of the corresponidng element
            #
            # ++++++++++++++++++++++++++++++++++++++++
            # |         0.5          | 0.25  | 0.25  |
            # ++++++++++++++++++++++++++++++++++++++++
            # 0      ^                               1
            #        |
            #        With p=0.5 we pick a point from the first element's interval

            # Sum of all weights
            sum_weights = sum([d(ctx.attractiveness) for u, v, ctx in edges])

            # Variable that stores the cumulative Probability
            cum_prob = 0

            # Generate a random number between 0 and 1
            r = random.random()

            # Iterate over all edges, order does not matter
            for u, v, ctx in edges:

                # Increase cumulative
                cum_prob += ctx.attractiveness / sum_weights

                # Check if value is in interval
                if cum_prob >= r:
                    # Return edge
                    return u, v, ctx

                # Continue otherwise

            # We may reach this point due to rounding errors
            # Just return a random element
            return random.choice(edges)

        assert isinstance(G, nx.Graph)
        assert 0.0 <= q <= 1.0

        # The path, which the ant took
        path = list()

        # Length of the path
        length = 0

        # Nodes, which need to be visited
        open = [u for u in G.nodes_iter() if u != s]

        # Current Node
        current = s

        while len(open)>0:

            # Grab all admissible edges whose targets have not been visited
            candidates = [(u, v, w) for (u, v, w) in G.edges(current, data=EdgeContext.KEY) if v in open]


            if random.random() < q:
                # Pick uniformly at random -> Exploration
                u, v, w = random.choice(candidates)
            else:
                # Pick random edge according to weight -> Exploitation
                u, v , w = pick_random(candidates)

            # Append new edge to path
            path.append((u, v))

            # Update path length
            length += w.distance

            # Update current node
            current = v

            # Remove next node from open list
            open.remove(v)

        # Add distance back to start
        length += G[current][s]["weight"]
        path.append((current, s))

        return length, path


class EdgeContext(object):

    KEY = "ACO_EDGE_CTX"

    def __init__(self, distance, alpha, beta):

        #Set distance
        self._distance = distance

        # Set alpha
        self._alpha = alpha

        # Set beat
        self._beta = d(beta)

        # Set initial TAU
        self._tau = TAU_INITIAL

        # Compute eta
        self._eta = d(1) / self.distance

        self._phi = self._eta

        # Compute initial attractiveness
        self._updateAttractiveness()

    def _updateAttractiveness(self):
        """
        Updates the attractiveness according to ACO's formula:

            phi = eta**alpha * tau**beta

        :return:
        """

        def assertBiggerZero(n):
            """

            Checks if the given value is bigger than 0.

            If it is, it returns the value, otherwise the next bigger value

            :param n: A number or Decimal
            :return: n, is n > d(0)
                     n.next_plus(), otherwise
            """

            # Assert that n is Decimal
            n = d(n)

            # Check if zero
            if n == d(0):
                # Return the next bigger number,
                # Actual step size is defined by Decimal.Context
                return n.next_plus()
            else:
                return n

        #
        # The products below are possibly very(!) small and hence rounded to 0 -> bad
        # if that's the case, we assign the smallest possible value -> not so bad
        #

        t_eta = assertBiggerZero(self._eta ** self._alpha)

        t_tau = assertBiggerZero(self._tau ** self._beta)

        self._phi = assertBiggerZero(t_eta * t_tau)

    @property
    def pheromone(self):
        """
        :return: The current level of pheromone on this edge
        """
        return self._tau

    @property
    def distance(self):
        """
        :return: The length of this edge
        """
        return self._distance

    @property
    def attractiveness(self):
        """
        :return: The edge's attractivness
        """
        return self._phi

    def addPheromone(self, delta_tau, refresh = True):
        """
        Adds the given amount of pheromone

        :param delta_tau: a positive number
        :param refresh: Refresh the pheromone value
        """
        self._tau = self._tau + delta_tau
        if refresh:
            self._updateAttractiveness()

    def evaporate(self, rho):
        """
        Reduces pheromone by factor rho

        :param rho: a real number between 0 and 1 (inclusive)
        """

        assert 0 <= rho <= 1
        self._tau = d(rho) * self._tau
        self._updateAttractiveness()
