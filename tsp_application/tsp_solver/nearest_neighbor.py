from abstract_tsp_solver import AbstractTSPSolver


class NearstNeighbor(AbstractTSPSolver):
    """



    """

    def options(self):
        return {}

    def info(self):
        return "https://en.wikipedia.org/wiki/Travelling_salesman_problem#Heuristic_and_approximation_algorithms"


    def __init__(self):
        """

        Creates new Christofides instance

        """
        super(NearstNeighbor, self).__init__()
        pass

    def solve(self, s, instance, **options):


        TSP = [s]

        cur = s

        l = 0

        open = [u for u in instance]

        while len(open)>0:
            cur, w = min([(v,w) for v, w in instance[cur].items() if v in open], key = lambda (v, w): w)

            l += w

            TSP.append(cur)

            open.remove(cur)

        l += instance[cur][s]

        return l, TSP