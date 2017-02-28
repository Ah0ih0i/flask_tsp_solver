
# Setup LOGGING
import logging
logging.basicConfig(level=logging.INFO)

from flask import Flask

#Create Flask application
from tsp.google_tsp import GoogleDistanceMatrixFactory

tsp_application = Flask(__name__)

#Set configuration
tsp_application.config.from_object('config')

matrix = GoogleDistanceMatrixFactory("AIzaSyC8XnrBVpMr5b_rAS-ZbWIzUFsix6Gh7aY")

from tsp.tsp_application import views
from tsp.tsp_application import commands