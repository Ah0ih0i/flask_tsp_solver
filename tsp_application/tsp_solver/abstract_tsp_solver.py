from abc import abstractmethod



class AbstractTSPSolver(object):
    """
    Abstract base class for an algorithm, that solves the TSP problem
    """
    def __init__(self):
        pass


    @abstractmethod
    def solve(self, s, distance_graph, **kwargs):
        """
        Solves the TSP Problem for the given instance

        An instance is two-dimenational dict, which represents distance matrix

        s must be any key in that dict

        :param s: The starting point
        :param distance_graph: A datastructure that contains nodes and their distances to other nodes
        :param kwargs: additional key-word arguments for implemtations
        :return: A tuple (d,p) where
                 - d is the path's length
                 - p is the path represented as a list nodes
        """
        pass

    @abstractmethod
    def info(self):
        """
        :return: A human readable description of the algorithm
        """
        return ""

    @abstractmethod
    def options(self):
        """
        Returns a dict with additional information about this algorithms options.

        Each option must look like this

        {
            "key": {
                "default" : # <- Default value
                "min": , # <- Min value
                "max": , # <- Max. value
                "step": , # <- Step size
                "name":  # <- Human readable name
            },
        }

        Note: these dicts are used to create the forms in the GUI

        :return: A dict of options
        """
        return {}

    @property
    def name(self):
        """
        :return: This algorithm's name
        """
        return self.__class__.__name__
