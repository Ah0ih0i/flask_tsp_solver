from flask import render_template

from tsp_application import app, algorithms

@app.route('/')
def main():
    return render_template('map.html',
                           algos=algorithms.values())


