
# Setup LOGGING
import logging
logging.basicConfig(level=logging.INFO)

from flask import Flask


#Create Flask application
tsp_application = Flask(__name__)


from tsp_application.google_tsp import GoogleDistanceMatrixFactory

matrix = GoogleDistanceMatrixFactory("AIzaSyC8XnrBVpMr5b_rAS-ZbWIzUFsix6Gh7aY")

import tsp_application.views
import tsp_application.commands