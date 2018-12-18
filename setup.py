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


setup(
    name="bluclobber",
    version="0.0.1",
    author="James Hetherington",
    author_email="j.hetherington@ucl.ac.uk",
    description=(
        "Harness for Apache Spark analysis of ALTO books corpus"),
    license="MIT",
    keywords="digital humanities research books",
    url="https://github.com/alan-turing-institute/cluster-code",
    packages=['bluclobber'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Research :: Humanities",
        "License :: OSI Approved :: MIT License",
    ]
)
