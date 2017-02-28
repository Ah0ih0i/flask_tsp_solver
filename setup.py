
from setuptools import setup

setup(
    name = "tsp",
    version = "0.0.1",
    author = "Thorsten Goette",
    author_email = "thgoette@mail.upb.de",
    description = ("A Tsp Solver for IT Talents"),
    license = "BSD",
    packages=['tsp', 'tests'],
    package_data={'tests': ['testsets/*.pickle'],
                  'tsp.tsp_application': ['templates/*.html']},
    install_requires=[
        'Flask',
        'networkx',
        'googlemaps',
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)