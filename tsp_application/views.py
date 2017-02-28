from flask import render_template

from tsp_application import algorithms
from tsp_application import tsp_application as app


@app.route('/')
def main():
    return render_template('map.html',
                           algos=algorithms.values())


