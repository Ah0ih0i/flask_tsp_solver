from flask import render_template

from tsp.tsp_application import tsp_application as app
from tsp.tsp_solver import algorithms


@app.route('/')
def main():
    return render_template('map.html',
                           algos=algorithms.values())


