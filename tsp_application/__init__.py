
# Setup LOGGING
import logging
logging.basicConfig(level=logging.INFO)

from flask import Flask


#Create Flask application
app = Flask(__name__)


from google_tsp import GoogleDistanceMatrixFactory
from tsp_solver import algorithms

matrix = GoogleDistanceMatrixFactory("AIzaSyC8XnrBVpMr5b_rAS-ZbWIzUFsix6Gh7aY")

import tsp_application.views
import tsp_application.commands