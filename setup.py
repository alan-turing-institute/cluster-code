"""
This is the project specification for setuptools
"""

import os
from setuptools import setup


def read(fname):
    """
    Read a file relative the current directory and return its contents
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


AUTHORS = ["James Hetherington",
           "James Baker",
           "Mike Jackson",
           "Rosa Filgueira"]

EMAILS = ["j.hetherington@ucl.ac.uk",
          "james.baker@bl.uk",
          "michaelj@epcc.ed.ac.uk",
          "rosa.filgueira@ed.ac.uk"]

setup(
    name="bluclobber",
    version="0.0.1",
    authors=", ".join(AUTHORS),
    author_email=", ".join(EMAILS),
    description=(
        "Harness for Apache Spark analysis of ALTO books corpus"),
    license="MIT",
    keywords="digital humanities research books",
    url="https://github.com/alan-turing-institute/cluster-code",
    packages=['bluclobber'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Research :: Humanities",
        "License :: OSI Approved :: MIT License",
    ]
)
