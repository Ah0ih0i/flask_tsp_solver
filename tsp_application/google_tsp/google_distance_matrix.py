from itertools import izip

import googlemaps
import googlemaps.distance_matrix as dm


class GoogleDistanceMatrixFactory(object):
    """
        A factory class that uses Google Maps to create distance matrices
    """


    def __init__(self, key):
        """

        Creates a new instance

        :param key: The API-Key for Google Maps
        """
        self.key = key
        self.client = googlemaps.Client(self.key)


    def create(self, places, data=u"duration"):
        """

        Creates a new distance matrix

        :param places:
        :param data:
        :return:
        """

        # Make sure, we have list of entries
        if not isinstance(places, list):
            return None

        # Make sure, that we use a valid metric supported by Google Maps
        if not unicode(data) in [u"duration", u"distance"]:
            return None

        # Response is HTTP from Google
        response = dm.distance_matrix(self.client, places, places)


        # Check if response was successful
        if response[u"status"] == u"OK":

            # Variable for return value
            matrix = dict()

            # Iterate over each place and its corresponding row in the response
            for start, row in izip(places, response[u"rows"]):

                # Wrap dict
                # start = GoogleDistanceMatrixFactory.Place(start)

                # Create entry for starting place
                matrix[start] = dict()

                # Iterate over all possible destinations and their indvidual responses
                for dest, element in izip(places,row[u"elements"]):

                    # Check if a path was found
                    if element[u"status"] != u"OK":
                        return None

                    # Create entry for start and destination
                    matrix[start][dest] = element[unicode(data)][u"value"]

            return matrix
        else:
            return None


