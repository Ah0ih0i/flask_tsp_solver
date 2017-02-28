from abstract_tsp_solver import AbstractTSPSolver
from antcolony import AntColony
from christofides import Christofides
from furthest_neighbor import FurthestNeighbor
from nearest_neighbor import NearstNeighbor

algorithms = { algo.name: algo
               for algo in
               [
                Christofides(),
                AntColony(),
                NearstNeighbor(),
                FurthestNeighbor()
                ]
}