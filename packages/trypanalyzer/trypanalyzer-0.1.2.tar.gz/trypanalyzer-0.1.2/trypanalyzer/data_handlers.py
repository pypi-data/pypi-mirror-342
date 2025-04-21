# data_handlers.py

import h5py
import numpy as np
from .analyzers import adjust_periodic_single, adjust_periodic_array, find_center


def read_organize_data(file_path_brownian, n_total, Lx, Ly, Lz, sim_type):
    """
    Read and organize data from HDF5 file with appropriate boundary adjustments.
    
    Parameters
    ----------
    file_path_brownian : str
        Path to the HDF5 file containing simulation data.
    n_total : int
        Total number of time steps to process.
    Lx : float
        System size in x dimension.
    Ly : float
        System size in y dimension.
    Lz : float
        System size in z dimension.
    sim_type : str
        Simulation type ('bulk', 'plates', 'channel') determining boundary conditions.
        
    Returns
    -------
    tuple
        (X_adjusted, Y_adjusted, Z_adjusted, x_cm, y_cm, z_cm) where:
        - X_adjusted, Y_adjusted, Z_adjusted: Lists of shape data coordinates.
        - x_cm, y_cm, z_cm: Lists of center of mass coordinates.
    
    Notes
    -----
    The function applies different periodic boundary adjustments based on the
    simulation type:
    - 'bulk': periodic in all dimensions
    - 'plates': periodic in x and y dimensions
    - 'channel': periodic in x dimension only
    
    Examples
    --------
    >>> X, Y, Z, x_cm, y_cm, z_cm = read_organize_data('sim.h5', 100, 75.0, 75.0, 75.0, 'bulk')
    """
    x_cm, y_cm, z_cm = [], [], []
    time_series_list_tryp_shape_0 = []

    coordinate_system_offset = 37.5
    
    with h5py.File(file_path_brownian, 'r') as hdf:
        tryp_state_dat = hdf.get('trypanosome_state_timeseries')
        tryp_shape_dat = hdf.get('trypanosome_shape_timeseries')
        sorted_tryp_state_keys = sorted(tryp_state_dat.keys(), key=int)
        sorted_tryp_shape_keys = sorted(tryp_shape_dat.keys(), key=int)
        
        # Process CM data
        for i, key in enumerate(sorted_tryp_state_keys):
            state_data = tryp_state_dat[key]
            curr_x = state_data[0] + 0.5 * Lx + coordinate_system_offset
            curr_y = state_data[1] + 0.5 * Ly + coordinate_system_offset
            curr_z = state_data[2] + 0.5 * Lz + coordinate_system_offset
            
            if i > 0:  # If not first point
                if sim_type in ['bulk', 'plates', 'channel']:
                    curr_x = adjust_periodic_single(curr_x, x_cm[-1], Lx)
                if sim_type in ['bulk', 'plates']:
                    curr_y = adjust_periodic_single(curr_y, y_cm[-1], Ly)
                if sim_type == 'bulk':
                    curr_z = adjust_periodic_single(curr_z, z_cm[-1], Lz)
                    
            x_cm.append(curr_x)
            y_cm.append(curr_y)
            z_cm.append(curr_z)
            
        # Process shape data
        for key in sorted_tryp_shape_keys:
            shape_data = tryp_shape_dat[key]
            time_series_list_tryp_shape_0.extend(shape_data[:780])

    # Process XYZ data
    composite_tryp_shape_time_series_0 = [time_series_list_tryp_shape_0[x:x+780] for x in range(0, len(time_series_list_tryp_shape_0), 780)]
    composite_tryp_shape_0 = [[sublist[n:n+30] for n in range(0, len(sublist), 30)] for sublist in composite_tryp_shape_time_series_0]

    x_values_0 = [[] for _ in range(n_total)]
    y_values_0 = [[] for _ in range(n_total)]
    z_values_0 = [[] for _ in range(n_total)]

    for k in range(n_total):
        for sublist in composite_tryp_shape_0[k]:
            for j in range(0, 30, 3):
                x_values_0[k].append(sublist[j] + 0.5 * Lx)
                y_values_0[k].append(sublist[j+1] + 0.5 * Ly)
                z_values_0[k].append(sublist[j+2] + 0.5 * Lz)

    X_transposed = list(map(list, zip(*x_values_0)))
    Y_transposed = list(map(list, zip(*y_values_0)))
    Z_transposed = list(map(list, zip(*z_values_0)))

    # Apply periodic boundaries
    if sim_type == 'bulk':
        X_transposed = [adjust_periodic_array(col, Lx) for col in X_transposed]
        Y_transposed = [adjust_periodic_array(col, Ly) for col in Y_transposed]
        Z_transposed = [adjust_periodic_array(col, Lz) for col in Z_transposed]
    elif sim_type == 'plates':
        X_transposed = [adjust_periodic_array(col, Lx) for col in X_transposed]
        Y_transposed = [adjust_periodic_array(col, Ly) for col in Y_transposed]
    elif sim_type == 'channel':
        X_transposed = [adjust_periodic_array(col, Lx) for col in X_transposed]
            
    X_adjusted = list(map(list, zip(*X_transposed)))
    Y_adjusted = list(map(list, zip(*Y_transposed)))
    Z_adjusted = list(map(list, zip(*Z_transposed)))

    return X_adjusted, Y_adjusted, Z_adjusted, x_cm, y_cm, z_cm


def process_circle_data(n_total, num_cross_sections, num_nodes_per_cross_sec, x_values_0, y_values_0, z_values_0):
    """
    Process coordinate data to extract cross-sectional information for trypanosome model.
    
    Parameters
    ----------
    n_total : int
        Total number of time steps to process.
    num_cross_sections : int
        Number of cross-sections in the trypanosome model.
    num_nodes_per_cross_sec : int
        Number of nodes per cross-section.
    x_values_0 : list of list
        X coordinates for all nodes at each time step.
    y_values_0 : list of list
        Y coordinates for all nodes at each time step.
    z_values_0 : list of list
        Z coordinates for all nodes at each time step.
       
    Returns
    -------
    tuple
        (circle_data_x, circle_data_y, circle_data_z, center) where:
        
        - circle_data_x, circle_data_y, circle_data_z: 3D lists containing coordinates
          organized by [timestep][cross_section][node].
        - center: List of centers for each cross-section at each time step.
   
    Examples
    --------
    >>> circle_x, circle_y, circle_z, centers = process_circle_data(
    ...     100, 26, 10, x_values, y_values, z_values)
    
    >>> # Access coordinates of first cross-section at first timestep
    >>> first_cross_section_x = circle_x[0][0]
    
    >>> # Access center of last cross-section at last timestep
    >>> last_center = centers[-1][-1]
    """
    circle_data_x = [[[] for _ in range(num_cross_sections)] for _ in range(n_total)]
    circle_data_y = [[[] for _ in range(num_cross_sections)] for _ in range(n_total)]
    circle_data_z = [[[] for _ in range(num_cross_sections)] for _ in range(n_total)]
    center = [[] for _ in range(n_total)]
    
    for n in range(n_total):
        for j in range(num_cross_sections):
            for i in range(num_nodes_per_cross_sec):
                circle_data_x[n][j].append(x_values_0[n][i + j * 10])
                circle_data_y[n][j].append(y_values_0[n][i + j * 10])
                circle_data_z[n][j].append(z_values_0[n][i + j * 10])
            circle_data_x[n][j].append(x_values_0[n][j * 10])
            circle_data_y[n][j].append(y_values_0[n][j * 10])
            circle_data_z[n][j].append(z_values_0[n][j * 10])
            
    for j in range(n_total):
        for i in range(num_cross_sections):
            center[j].append(find_center(circle_data_x[j][i], circle_data_y[j][i], circle_data_z[j][i]))
            
    return circle_data_x, circle_data_y, circle_data_z, center


def save_combined_data(file_path, n_total, Lx, Ly, Lz, sim_type, cm_interval=1, xyz_interval=50):
    """
    Process HDF5 simulation data and save to multiple text files for analysis.
    
    This function extracts data from an HDF5 file, processes it to handle
    periodic boundaries, calculates centers of cross-sections and center of mass,
    and saves the results to several text files.
    
    Parameters
    ----------
    file_path : str
        Path to the HDF5 file containing simulation data.
    n_total : int
        Total number of time steps to process.
    Lx : float
        System size in x dimension.
    Ly : float
        System size in y dimension.
    Lz : float
        System size in z dimension.
    sim_type : str
        Simulation type identifier ('bulk', 'plates', 'channel').
    cm_interval : int, optional
        Interval for center of mass data sampling, by default 1.
    xyz_interval : int, optional
        Interval for coordinate data sampling, by default 50.
    
    Returns
    -------
    None
        The function saves results to text files instead of returning values.
    
    Notes
    -----
    The function creates the following output files:
    - nodes_cm_data_{sim_type}.txt: Center of mass calculated from all nodes
    - center_data_{sim_type}.txt: Center of first cross-section
    - center_last_data_{sim_type}.txt: Center of last cross-section
    - cm_data_{sim_type}.txt: Center of mass from state data
    - xyz_data_{sim_type}.txt: Coordinates of all nodes at specified intervals
    
    Examples
    --------
    >>> save_combined_data('simulation.h5', 1000, 75.0, 75.0, 75.0, 'bulk')
    Nodes-based CM data has been saved to nodes_cm_data_bulk.txt
    First cross-section center data has been saved to center_data_bulk.txt
    Last cross-section center data has been saved to center_last_data_bulk.txt
    Center of mass data has been saved to cm_data_bulk.txt
    XYZ data has been saved to xyz_data_bulk.txt
    """
    # Get organized data
    X_adjusted, Y_adjusted, Z_adjusted, x_cm, y_cm, z_cm = read_organize_data(
        file_path, n_total, Lx, Ly, Lz, sim_type
    )
    
    # Calculate CM from nodes for comparison
    nodes_cm_x = []
    nodes_cm_y = []
    nodes_cm_z = []
    
    for k in range(min(len(X_adjusted), n_total)):
        # Calculate CM as average of all nodes for this timestep
        nodes_cm_x.append(np.mean(X_adjusted[k]))
        nodes_cm_y.append(np.mean(Y_adjusted[k]))
        nodes_cm_z.append(np.mean(Z_adjusted[k]))
    
    # Save nodes-based CM data
    nodes_cm_output_file = f'nodes_cm_data_{sim_type}.txt'
    with open(nodes_cm_output_file, 'w') as f:
        for k in range(len(nodes_cm_x)):
            f.write(f"Step {k}:\n")
            f.write(f"x_cm: {nodes_cm_x[k]}\n")
            f.write(f"y_cm: {nodes_cm_y[k]}\n")
            f.write(f"z_cm: {nodes_cm_z[k]}\n")
            f.write("\n")
    print(f"Nodes-based CM data has been saved to {nodes_cm_output_file}")
    
    # Process circle data
    num_cross_sections = 26
    num_nodes_per_cross_sec = 10
    circle_data_x, circle_data_y, circle_data_z, center = process_circle_data(
        n_total, num_cross_sections, num_nodes_per_cross_sec, 
        X_adjusted, Y_adjusted, Z_adjusted
    )
    
    # Save center data for first cross-section (index 0)
    center_output_file = f'center_data_{sim_type}.txt'
    with open(center_output_file, 'w') as f:
        for k in range(min(len(center), n_total)):
            f.write(f"Step {k}:\n")
            f.write(f"x_center: {center[k][0][0]}\n")
            f.write(f"y_center: {center[k][0][1]}\n")
            f.write(f"z_center: {center[k][0][2]}\n")
            f.write("\n")
    print(f"First cross-section center data has been saved to {center_output_file}")
    
    # Save center data for last cross-section (index 25)
    center_last_output_file = f'center_last_data_{sim_type}.txt'
    with open(center_last_output_file, 'w') as f:
        for k in range(min(len(center), n_total)):
            f.write(f"Step {k}:\n")
            f.write(f"x_center: {center[k][25][0]}\n")
            f.write(f"y_center: {center[k][25][1]}\n")
            f.write(f"z_center: {center[k][25][2]}\n")
            f.write("\n")
    print(f"Last cross-section center data has been saved to {center_last_output_file}")
    
    # Save CM data
    cm_output_file = f'cm_data_{sim_type}.txt'
    with open(cm_output_file, 'w') as f:
        collected_x = []
        collected_y = []
        collected_z = []
        
        for k in range(min(len(x_cm), n_total)):
            collected_x.append(x_cm[k])
            collected_y.append(y_cm[k])
            collected_z.append(z_cm[k])
            
            if (k + 1) % cm_interval == 0 or k == min(len(x_cm), n_total) - 1:
                f.write(f"Steps {k-len(collected_x)+1} to {k+1}:\n")
                f.write(f"x_cm: {', '.join(map(str, collected_x))}\n")
                f.write(f"y_cm: {', '.join(map(str, collected_y))}\n")
                f.write(f"z_cm: {', '.join(map(str, collected_z))}\n")
                f.write("\n")
                collected_x = []
                collected_y = []
                collected_z = []
                
    print(f"Center of mass data has been saved to {cm_output_file}")
    
    # Save XYZ data
    xyz_output_file = f'xyz_data_{sim_type}.txt'
    with open(xyz_output_file, 'w') as f:
        for k in range(min(len(X_adjusted), n_total)):
            if k % xyz_interval == 0:
                f.write(f"Step {k}:\n")
                f.write(f"x_values: {', '.join(map(str, X_adjusted[k]))}\n")
                f.write(f"y_values: {', '.join(map(str, Y_adjusted[k]))}\n")
                f.write(f"z_values: {', '.join(map(str, Z_adjusted[k]))}\n")
                f.write("\n")
    print(f"XYZ data has been saved to {xyz_output_file}")


def export_trypanosome_trajectory_VMD(file_path, output_filename, nof, rpc, nov):
    """
    Extract and export trypanosome trajectory data from HDF5 simulation files.
    
    This function reads simulation data from an HDF5 file, processes both the
    trypanosome state (center of mass) and shape timeseries data, and exports
    the complete trajectory to an XYZ file for visualization.
    
    Parameters
    ----------
    file_path : str
        Path to the simulation data HDF5 file
    output_filename : str
        Name for the output XYZ file (must end with .xyz)
    nof : int
        Number of frames
    rpc : int
        Number of vertices per circle (resolution parameter)
    nov : int
        Number of vertices
        
    Returns
    -------
    None
        The function writes the output to an XYZ file but does not return any value
    
    Notes
    -----
    The function extracts both center of mass and shape coordinates from the HDF5 file
    and writes them to an XYZ file for visualization with molecular dynamics software.
    """
    # Validate output filename
    if not output_filename.endswith('.xyz'):
        raise ValueError("Output filename must end with .xyz")
    
    # Derived parameters
    nofp = nof + 1
    rpc3 = 3 * rpc
    nov3 = 3 * nov
    
    # Lists to store position, velocity, and displacement data
    x_0, y_0, z_0 = [], [], []
    vx_0, vy_0, vz_0 = [], [], []
    dx_0, dy_0, dz_0 = [], [], []
    
    # List to store shape data
    time_series_list_tryp_shape_0 = []
    
    # Open the HDF file for simulation data
    with h5py.File(file_path, 'r') as hdf:
        # Retrieve trypanosome state and shape timeseries datasets
        tryp_state_dat = hdf.get('trypanosome_state_timeseries')  # center of mass trajectory
        tryp_shape_dat = hdf.get('trypanosome_shape_timeseries')  # trajectories of vertices
        
        # Sort the keys of trypanosome state and shape datasets
        sorted_tryp_state_keys = sorted(tryp_state_dat.keys(), key=int)
        sorted_tryp_shape_keys = sorted(tryp_shape_dat.keys(), key=int)
        
        # Extract state data and append to respective lists
        for key in sorted_tryp_state_keys:
            state_data = tryp_state_dat[key]
            x_0.append(state_data[0])
            y_0.append(state_data[1])
            z_0.append(state_data[2])
            vx_0.append(state_data[3])
            vy_0.append(state_data[4])
            vz_0.append(state_data[5])
            dx_0.append(state_data[6])
            dy_0.append(state_data[7])
            dz_0.append(state_data[8])
        
        # Extract shape data and append to time_series_list_tryp_shape_0
        for key in sorted_tryp_shape_keys:
            shape_data = tryp_shape_dat[key]
            time_series_list_tryp_shape_0.extend(shape_data[:nov3])
    
    # Divide shape data into sublists of length nov3
    composite_tryp_shape_time_series_0 = [
        time_series_list_tryp_shape_0[x:x+nov3] 
        for x in range(0, len(time_series_list_tryp_shape_0), nov3)
    ]
    
    # Further divide shape data into nested sublists
    composite_tryp_shape_0 = [
        [sublist[n:n+rpc3] for n in range(0, len(sublist), rpc3)] 
        for sublist in composite_tryp_shape_time_series_0
    ]
    
    # Lists to store organized x, y, and z values
    x_values_0 = [[] for _ in range(nofp)]
    y_values_0 = [[] for _ in range(nofp)]
    z_values_0 = [[] for _ in range(nofp)]
    
    # Create the output XYZ file
    with open(output_filename, 'w') as f:
        # Iterate over time steps
        for k in range(nofp):
            # Write header for each frame
            f.write(f"{nov}\n")
            f.write("coordinate: X Y Z\n")
            
            # Iterate over sub-sublists within composite_tryp_shape_0
            for sublist in composite_tryp_shape_0[k]:
                # Extract x, y, and z coordinates and write to file
                for j in range(0, rpc3, 3):
                    x_values_0[k].append(sublist[j])
                    y_values_0[k].append(sublist[j+1])
                    z_values_0[k].append(sublist[j+2])
                    
                    f.write("O\t")
                    rx, ry, rz = (sublist[j], sublist[j+1], sublist[j+2])
                    f.write("%f %f %f\n" % (rx, ry, rz))


def export_flagellum_trajectory_VMD(file_path, output_filename, nof, rpc, nov, flagstart, helix_start, winding):
    """
    Extract and export flagellum trajectory data from HDF5 simulation files.
    
    This function reads simulation data from an HDF5 file, processes the trypanosome
    shape timeseries data, and exports the flagellum trajectory to an XYZ file for
    visualization with VMD or similar tools.
    
    Parameters
    ----------
    file_path : str
        Path to the simulation data HDF5 file
    output_filename : str
        Name for the output XYZ file (must end with .xyz)
    nof : int
        Number of frames
    rpc : int
        Number of vertices per circle (resolution parameter)
    nov : int
        Number of vertices
    flagstart : int
        Starting index for flagellum
    helix_start : int
        Starting index for helix
    winding : int
        Number of winding segments
        
    Returns
    -------
    None
        The function writes the output to an XYZ file but does not return any value
    
    Notes
    -----
    The function extracts coordinates from the HDF5 file and writes them to an XYZ
    file format that can be used for visualization with molecular dynamics software.
    """
    # Validate output filename
    if not output_filename.endswith('.xyz'):
        raise ValueError("Output filename must end with .xyz")
    
    # Derived parameters
    nofp = nof + 1
    rpc3 = 3 * rpc
    nov3 = 3 * nov
    bendstart = helix_start + flagstart
    bendend = bendstart + winding
    
    # List to store shape data
    time_series_list_tryp_shape_0 = []
    
    # Open the HDF file for simulation data
    with h5py.File(file_path, 'r') as hdf:
        # Retrieve trypanosome shape timeseries dataset
        tryp_shape_dat = hdf.get('trypanosome_shape_timeseries')
        
        # Sort the keys of trypanosome shape dataset
        sorted_tryp_shape_keys = sorted(tryp_shape_dat.keys(), key=int)
        
        # Extract shape data and append to time_series_list_tryp_shape_0
        for key in sorted_tryp_shape_keys:
            shape_data = tryp_shape_dat[key]
            time_series_list_tryp_shape_0.extend(shape_data[:nov3])
    
    # Divide shape data into sublists of length nov3
    composite_tryp_shape_time_series_0 = [
        time_series_list_tryp_shape_0[x:x+nov3] 
        for x in range(0, len(time_series_list_tryp_shape_0), nov3)
    ]
    
    # Further divide shape data into nested sublists
    composite_tryp_shape_0 = [
        [sublist[n:n+rpc3] for n in range(0, len(sublist), rpc3)] 
        for sublist in composite_tryp_shape_time_series_0
    ]
    
    # Create the output XYZ file
    with open(output_filename, 'w') as f:
        # Iterate over time steps
        for k in range(nofp):
            # Write header for each frame
            f.write("23\n")
            f.write("coordinate: X Y Z\n")
            
            # Iterate over points in the flagellum
            for flag in range(len(composite_tryp_shape_0[k])):
                if flag >= flagstart:
                    if flag < bendstart:
                        base = 0
                    elif flag >= bendstart and flag < bendend:
                        base = 3 * (flag - bendstart)
                    else:
                        base = 3 * winding
                    
                    # Write coordinates to the file
                    f.write("H\t")
                    f.write("%f\t%f\t%f\n" % (
                        composite_tryp_shape_0[k][flag][base],
                        composite_tryp_shape_0[k][flag][base+1],
                        composite_tryp_shape_0[k][flag][base+2]
                    ))