import logging

from flask import request, jsonify

from tsp_application import algorithms
from tsp_application import matrix, tsp_application


@tsp_application.route("/ajax/solve")
def ajax_solve():
    """
    Serves the AJAX Request to solve the TSP.

    The Request consists of:

    {
        "waypoints": <- A list of waypoints either strings or LatLng-dicts
        "origin": <- The starting point
        "algo": <- The algorithm to use
        "options": <- key/value pairs as arguments for the algorithm (optional)
        "travel_mode": <- Mode of travel
    }

    The result looks as follows

   {
        "status": <- Status code,
        "length": <- length of the path (iff path is found)
        "start": <- The starting point (iff path is found)
        "algo": <- The used algorithm (iff path is found)
        "path": <- A list in which order to visit the endpoints (iff path is found)
        "msg": <- An optional message
    }


    :return:
    """

    # The possible errors and their human-readable messages
    ERRORS = {
        403: "Google Directions could not find a path",
        404: "Google Directions did not send response",
        405: "You did not specify a start",
        406: "You need to specify at least two waypoints",
        407: "You did not specify a valid algorithm",
        408: "Internal Algorithm Error",

    }


    def to_tuple(waypoint):
        """
        Converts LatLng dicts to tuples.

        :param waypoint: A waypoint as string, tuple or LatLng dict
        :return: waypoint, if waypoint is string or tuple,
                 a tuple of the lat and lng values, if dict

        """
        if isinstance(waypoint, dict):
            return (waypoint["lat"], waypoint["lng"])
        else:
            return waypoint

    def to_dict(waypoint):
        """
        Converts to tuples to LatLng dicts.

        :param waypoint: A waypoint as string or tuple
        :return: waypoint, if waypoint is string or tuple,
                 a LatNg dict, if tuple
        """
        if isinstance(waypoint, tuple):
            return {"lat": waypoint[0], "lng": waypoint[1]}
        else:
            return waypoint



    # Get the arguments
    json = request.args

    # Check that a start point is supplied
    start = json.get("origin")
    if not start:
        return jsonify(status=406, msg=ERRORS[405])

    # Convert to tuple if necessary
    # This is needed to store waypoints as keys in a dict
    start = to_tuple(start)



    waypoints = json.getlist("waypoints[]")
    if not waypoints:
        return jsonify(status=406, msg=ERRORS[406])

    # We need to have at least two points for a path
    if len(waypoints) < 2:
        return jsonify(status=406, msg=ERRORS[406])

    # Convert to tuple if necessary
    # This is needed to store waypoints as keys in a dict
    waypoints = map(to_tuple, waypoints)

    # Get the algorithm
    algorithm = algorithms[json["algo"]]
    if not algorithm:
        return jsonify(status=407, msg=ERRORS[407])

    # Get the options
    options = {}
    for option in algorithm.options():
        options[option] = float(json.get("options[%s]" % option))

    try:
        distances = matrix.create(waypoints)
    except BaseException as e:
        logging.warning("Exception %s while creating matrix for %s" % (e, waypoints))
        return jsonify(status=404, msg=ERRORS[404])
    else:
        if distances:

            try:
                # Call the algorithm
                l, path = algorithm.solve(start, distances, **options)
            except BaseException as e:
                logging.warning("Exception %s while executing %s with %s" % (e, algorithm.name, options))
                return jsonify(status=408, msg=ERRORS[408])
            else:
                # Pack result
                result = {
                    "status": 200,
                    "length": l,
                    "start": start,
                    "algo": json["algo"],
                    "path": map(to_dict, path),
                    "msg": "SUCCESS"
                }

            # Return the result
            return jsonify(result)
        else:
            return jsonify(status=403, msg=ERRORS[403])


