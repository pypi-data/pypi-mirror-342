"""
SysAME setup script for installing the package.

This script sets up the SysAME (System Agent Modelling Environment) package,
which is a framework for Transport Agent-Based Modelling.
"""

# Standard imports
import os
import codecs

# Third party imports
from setuptools import setup, find_packages  # type: ignore

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "0.0.3"
DESCRIPTION = "Transport Modelling Helper Package"
LONG_DESCRIPTION = "A package for Transport Modelling supporting various tools."

# Setting up
setup(
    name="sysame",  # noqa: cspell
    version=VERSION,
    author="sysame.com",
    author_email="<help@sysame.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "opencv-python",
        "numpy>=2.2.0",
        "scipy>=1.15.2",
        "matplotlib>=3.10.1",
        "pandas>=2.2.3",
        "openmatrix>=0.3.5.0",
        "polars>=1.26.0",
        "pyarrow>=19.0.1",
        "py7zr>=0.22.0",
        "geopandas>=1.0.1",
        "networkx>=3.4.2",
        "shapely>=2.1.0",
        "seaborn>=0.13.2",
        "contextily>=1.6.2",
    ],
    keywords=["python", "abm", "transport", "modelling", "environment"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
