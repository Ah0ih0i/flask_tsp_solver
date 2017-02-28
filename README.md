# flask_tsp_solver
A simple set of solvers for the TSP. 

Main purpose of this project was to learn JavaScript and Python Webservices 

# CLI (Linuc)

For quick tests, you can use the CLI.
Therefore install all dependencies via

```make```

Then activate the Virtual Environment via:

```./venv/bin/activate```

Then execute the CLI script via

```python CLI.py arg0, ..., arg8```

where ```arg0, ..., arg8``` are places to want to visit and ```arg0``` is the start


# Quickstart Webserver (Linux)

To run the server in a virtual environment, just type

```make && make run```

in the root directory.

This will setup a virtualenv with all dependencies and start the server

You need to have Python, pip and virtualenv installed!

On Ubuntu and Debian may also can execute

```make bootstrap```

to Python, pip and virtualenv.

It will ask for your sudoer's password

You can then access the webpage via http://127.0.0.1:5000

# Installation

To install the package in your python environment use

```python setup.py install```
