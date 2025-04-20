Installation
===========

You can install SysAME using pip:

.. code-block:: bash

    pip install sysame

Development Installation
----------------------

If you want to install SysAME for development:

1. Clone the repository:

.. code-block:: bash

    git clone https://github.com/yourusername/sysame.git
    cd sysame

2. Install development dependencies:

.. code-block:: bash

    pip install -e ".[dev]"

Requirements
----------

SysAME has the following dependencies:

* Python >= 3.8
* NumPy
* Pandas
* Matplotlib
* NetworkX (for network operations)

Optional Dependencies
------------------

* PyTables (for HDF5 storage)
* Geopandas (for GIS functionality)
* Folium (for interactive maps)
