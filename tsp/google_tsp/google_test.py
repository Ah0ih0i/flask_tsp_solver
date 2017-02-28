import unittest

from tsp.google_tsp.google_distance_matrix import GoogleDistanceMatrixFactory


class GoogleTest(unittest.TestCase):

    origins = ["Perth, Australia", "Sydney, Australia",
               "Melbourne, Australia", "Adelaide, Australia",
               "Brisbane, Australia", "Darwin, Australia",
               "Hobart, Australia", "Canberra, Australia"]



    def setUp(self):
        self.matrix = GoogleDistanceMatrixFactory("AIzaSyC8XnrBVpMr5b_rAS-ZbWIzUFsix6Gh7aY")

    def testDistanceMatrix(self):
        rc = self.matrix.create(GoogleTest.origins)
        assert rc




if __name__ == '__main__':
    unittest.main()
