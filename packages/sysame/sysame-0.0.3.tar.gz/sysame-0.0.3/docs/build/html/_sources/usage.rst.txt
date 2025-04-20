Usage
=====

This page provides basic examples of how to use the SysAME library.

Basic Usage
----------

Import SysAME and its modules:

.. code-block:: python

    import sysame
    from sysame import matrix, cube, saturn, matsim, plotting

Matrix Operations
---------------

.. code-block:: python

    from sysame.matrix import mx
    
    # Create a matrix
    matrix = mx.Matrix(data=[[1, 2], [3, 4]], zones=['A', 'B'])
    
    # Perform operations
    result = matrix * 2
    print(result)

CUBE Integration
--------------

.. code-block:: python

    from sysame.cube import cube
    
    # Load a CUBE network
    network = cube.load_network("path/to/network.net")
    
    # Process network data
    nodes = network.get_nodes()
    links = network.get_links()

MATSim Integration
----------------

.. code-block:: python

    from sysame.matsim import matsim_network
    
    # Load a MATSim network
    network = matsim_network.load_network("path/to/network.xml")
    
    # Access network elements
    nodes = network.get_nodes()
    links = network.get_links()

Plotting
-------

.. code-block:: python

    from sysame.plotting import plotting
    
    # Plot a matrix as a heatmap
    plotting.plot_matrix_heatmap(matrix, title="Matrix Heatmap")
    
    # Plot a network
    plotting.plot_network(network)
