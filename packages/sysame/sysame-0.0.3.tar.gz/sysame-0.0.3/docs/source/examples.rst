Examples
========

This section provides more comprehensive examples of how to use SysAME for various transportation modeling tasks.

Reading and Processing Matrix Data
--------------------------------

This example shows how to read matrices, perform operations, and export them:

.. code-block:: python

    from sysame.matrix import mx
    import numpy as np
    
    # Read matrix from file
    matrix = mx.read_matrix("path/to/matrix.csv")
    
    # Apply growth factors
    growth = 1.2
    future_matrix = matrix * growth
    
    # Apply proportional fitting (IPF)
    row_targets = np.sum(matrix.data, axis=1) * 1.5
    col_targets = np.sum(matrix.data, axis=0) * 1.3
    balanced_matrix = mx.ipf(matrix, row_targets, col_targets)
    
    # Save results
    balanced_matrix.save("path/to/output.csv")

Working with CUBE Networks
-------------------------

This example demonstrates how to load a CUBE network, analyze it, and make modifications:

.. code-block:: python

    from sysame.cube import cube
    
    # Load a network
    network = cube.load_network("path/to/network.net")
    
    # Find links with high congestion
    congested_links = [link for link in network.links 
                      if link.volume / link.capacity > 0.85]
    
    # Calculate statistics
    total_delay = sum(link.calculate_delay() for link in network.links)
    print(f"Total network delay: {total_delay} hours")
    
    # Make network modifications and save
    for link in congested_links:
        link.capacity *= 1.5  # Increase capacity by 50%
    
    network.save("path/to/modified_network.net")

MATSim Simulation Analysis
------------------------

This example shows how to analyze MATSim simulation results:

.. code-block:: python

    from sysame.matsim import matsim_network
    
    # Load network and events
    network = matsim_network.load_network("path/to/network.xml")
    events = matsim_network.load_events("path/to/events.xml")
    
    # Analyze travel times by time of day
    time_bins = matsim_network.create_time_bins(events, bin_size_minutes=30)
    travel_times = matsim_network.calculate_travel_times(events, time_bins)
    
    # Plot results
    from sysame.plotting import plotting
    plotting.plot_travel_times_by_time(travel_times, time_bins)
