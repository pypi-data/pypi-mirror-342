# analyzers.py

import numpy as np
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from sklearn.decomposition import PCA


def rodriguez_rotation(zeta, u, k):
    """
    Compute the Rodriguez rotation formula.
    
    Parameters
    ----------
    zeta : float
        Rotation angle in radians.
    u : array_like
        Vector to be rotated.
    k : array_like
        Axis of rotation (unit vector).
    
    Returns
    -------
    ndarray
        The rotated vector.
    """
    a = u * np.cos(zeta)
    b = np.cross(k, u) * np.sin(zeta)
    c = k * (np.dot(k, u)) * (1 - np.cos(zeta))
    return a + b + c


def loss(zeta, u_rot, u, k):
    """
    Calculate the squared error between the rotated vector and the target vector.
    
    Parameters
    ----------
    zeta : float
        Rotation angle in radians.
    u_rot : array_like
        Target vector after rotation.
    u : array_like
        Original vector before rotation.
    k : array_like
        Axis of rotation (unit vector).
    
    Returns
    -------
    float
        The squared error between the rotated vector and the target vector.
    """
    rotated_vector = rodriguez_rotation(zeta, u, k)
    return np.linalg.norm(rotated_vector - u_rot)**2


def gradient(zeta, u_rot, u, k):
    """
    Compute the numerical gradient of the loss function with respect to zeta.
    
    Parameters
    ----------
    zeta : float
        Rotation angle in radians.
    u_rot : array_like
        Target vector after rotation.
    u : array_like
        Original vector before rotation.
    k : array_like
        Axis of rotation (unit vector).
    
    Returns
    -------
    float
        The gradient of the loss function at the given zeta.
    """
    epsilon = 1e-6
    grad = (loss(zeta + epsilon, u_rot, u, k) - loss(zeta - epsilon, u_rot, u, k)) / (2 * epsilon)
    return grad


def gradient_descent(zeta_initial, u_rot, u, k, learning_rate, num_iterations):
    """
    Perform gradient descent to find the optimal rotation angle.
    
    Parameters
    ----------
    zeta_initial : float
        Initial rotation angle in radians.
    u_rot : array_like
        Target vector after rotation.
    u : array_like
        Original vector before rotation.
    k : array_like
        Axis of rotation (unit vector).
    learning_rate : float
        Step size for gradient descent.
    num_iterations : int
        Number of iterations for gradient descent.
    
    Returns
    -------
    float
        The optimized rotation angle in radians.
    """
    zeta = zeta_initial
    for _ in range(num_iterations):
        zeta -= learning_rate * gradient(zeta, u_rot, u, k)
    return zeta


def find_center(x_values, y_values, z_values):
    """
    Calculate the center point from lists of coordinates.
    
    Parameters
    ----------
    x_values : array_like
        List of x coordinates.
    y_values : array_like
        List of y coordinates.
    z_values : array_like
        List of z coordinates.
        
    Returns
    -------
    tuple or None
        (center_x, center_y, center_z) or None if inputs are invalid.
    
    Examples
    --------
    >>> x = [1, 2, 3]
    >>> y = [4, 5, 6]
    >>> z = [7, 8, 9]
    >>> find_center(x, y, z)
    (2.0, 5.0, 8.0)
    """
    n = len(x_values)
    if n == 0 or len(y_values) != n or len(z_values) != n:
        return None
    sum_x = sum_y = sum_z = 0
    for i in range(n):
        sum_x += x_values[i]
        sum_y += y_values[i]
        sum_z += z_values[i]
    center_x = sum_x / n
    center_y = sum_y / n
    center_z = sum_z / n
    return center_x, center_y, center_z


def adjust_periodic(x, L):
    """
    Adjust an array for periodic boundary conditions in-place.
    
    This function modifies the input array directly to ensure that consecutive
    points don't jump across periodic boundaries.
    
    Parameters
    ----------
    x : array_like
        List of position values to be adjusted in-place.
    L : float
        System size in this dimension (period length).
    
    Returns
    -------
    None
        The input array is modified in-place.
    
    Examples
    --------
    >>> positions = [0.1, 0.9, 0.1, 0.9]
    >>> adjust_periodic(positions, 1.0)
    >>> positions
    [0.1, 0.9, 0.1, 0.9]
    
    >>> positions = [0.1, 0.9, 1.8, 1.9]
    >>> adjust_periodic(positions, 1.0)
    >>> positions
    [0.1, 0.9, 0.8, 0.9]
    """
    for i in range(len(x)-1):
        if x[i+1] - x[i] > L/2:
            x[i+1] -= (x[i+1] - x[i]+L/2)//L*L
        if x[i+1] - x[i] < -L/2:
            x[i+1] += (x[i] - x[i+1]+L/2)//L*L


def adjust_periodic_single(x, prev_x, L):
    """
    Adjust a single point based on previous point for periodic boundaries.
    
    Parameters
    ----------
    x : float
        Current position.
    prev_x : float
        Previous position.
    L : float
        System size in this dimension (period length).
        
    Returns
    -------
    float
        Adjusted position.
    
    Examples
    --------
    >>> adjust_periodic_single(0.9, 0.1, 1.0)
    0.9
    >>> adjust_periodic_single(0.1, 0.9, 1.0)
    1.1
    """
    if x - prev_x > L/2:
        return x - L
    elif x - prev_x < -L/2:
        return x + L
    return x


def adjust_periodic_array(arr, L):
    """
    Adjust an entire array for periodic boundary conditions.
    
    Parameters
    ----------
    arr : numpy.ndarray
        Array of position values.
    L : float
        System size in this dimension (period length).
        
    Returns
    -------
    numpy.ndarray
        A new array with adjusted positions.
    
    Examples
    --------
    >>> import numpy as np
    >>> positions = np.array([0.1, 0.9, 0.1, 0.9])
    >>> adjust_periodic_array(positions, 1.0)
    array([0.1, 0.9, 1.9, 2.9])
    """
    adjusted = arr.copy()  # Make a copy to avoid modifying original
    for i in range(1, len(adjusted)):
        diff = adjusted[i] - adjusted[i-1]
        if diff > L/2:
            adjusted[i] -= L
        elif diff < -L/2:
            adjusted[i] += L
    return adjusted


def calculate_e2e(center, end0, end1, n_frames):
    """
    Calculate end-to-end vector components and magnitude for each frame.
    
    Parameters
    ----------
    center : array_like
        3D array of coordinates with shape (n_frames, n_particles, 3).
    end0 : int
        Index of the first end particle.
    end1 : int
        Index of the second end particle.
    n_frames : int
        Number of frames to process.
        
    Returns
    -------
    tuple
        (endvx, endvy, endvz, end2end) where:
        - endvx, endvy, endvz are arrays of normalized vector components.
        - end2end is an array of end-to-end distances.
    
    Examples
    --------
    >>> center = [[[0, 0, 0], [1, 1, 1]], [[0, 0, 0], [2, 0, 0]]]
    >>> calculate_e2e(center, 0, 1, 2)
    (array([0.57735027, 1.        ]), 
     array([0.57735027, 0.        ]), 
     array([0.57735027, 0.        ]), 
     array([1.73205081, 2.        ]))
    """
    endvx = np.zeros(n_frames)
    endvy = np.zeros(n_frames)
    endvz = np.zeros(n_frames)
    end2end = np.zeros(n_frames)

    for i in range(0, n_frames):
        distx = center[i][end1][0] - center[i][end0][0]
        disty = center[i][end1][1] - center[i][end0][1]
        distz = center[i][end1][2] - center[i][end0][2]

        dist2 = distx ** 2 + disty ** 2 + distz ** 2
        dist = np.sqrt(dist2)

        endvx[i] = distx / dist
        endvy[i] = disty / dist
        endvz[i] = distz / dist

        end2end[i] = np.sqrt(distx**2 + disty**2 + distz**2)

    return endvx, endvy, endvz, end2end


def calculate_rot_axis_and_vec_list(endvx, endvy, endvz, x_values_0, y_values_0, z_values_0, center):
    """
    Calculate rotation axis list and vector list for rotation analysis.
    
    Parameters
    ----------
    endvx : array_like
        Array of x-components of end-to-end vectors.
    endvy : array_like
        Array of y-components of end-to-end vectors.
    endvz : array_like
        Array of z-components of end-to-end vectors.
    x_values_0 : array_like
        Array of x coordinates for a specific particle.
    y_values_0 : array_like
        Array of y coordinates for a specific particle.
    z_values_0 : array_like
        Array of z coordinates for a specific particle.
    center : array_like
        3D array of coordinates with shape (n_frames, n_particles, 3).
        
    Returns
    -------
    tuple
        (rot_axis_list, vec_list) where:
        - rot_axis_list is a 2D array of rotation axes.
        - vec_list is a 2D array of normalized vectors.
    """
    rot_axis_list = []
    for i in range(len(endvx)):
        rot_axis = [endvx[i], endvy[i], endvz[i]]
        rot_axis_list.append(rot_axis)
    rot_axis_list = np.array(rot_axis_list)

    vec_list = []
    for i in range(len(endvx)):
        x = (x_values_0[i][50] - center[i][5][0])
        y = (y_values_0[i][50] - center[i][5][1])
        z = (z_values_0[i][50] - center[i][5][2])

        vec_len = np.sqrt(x**2 + y**2 + z**2)

        x_norm = x / vec_len
        y_norm = y / vec_len
        z_norm = z / vec_len

        vec = [x_norm, y_norm, z_norm]

        vec_list.append(vec)

    vec_list = np.array(vec_list)

    return rot_axis_list, vec_list


def sliding_average(data, window_size):
    """
    Calculate sliding averages for a time series.
    
    For each point, calculates the average of all previous points up to window_size.
    The window grows until it reaches the specified window_size.
    
    Parameters
    ----------
    data : array_like
        Input data array.
    window_size : int
        Maximum number of previous points to include in the average.
        
    Returns
    -------
    list
        List of sliding averages with the same length as the input data.
    
    Examples
    --------
    >>> sliding_average([1, 2, 3, 4, 5], 3)
    [1.0, 1.5, 2.0, 3.0, 4.0]
    """
    averages = []
    for i in range(len(data)):
        start = max(0, i - window_size + 1)
        end = i + 1
        window = data[start:end]
        average = np.mean(window)
        averages.append(average)
    return averages


def compute_angles_and_cos(endvx, rot_axis_list, vec_list, learning_rate, num_iterations, initial_angle):
    """
    Compute rotation angles and cosines between consecutive frames.
    
    Parameters
    ----------
    endvx : array_like
        Array of x-components of end-to-end vectors.
    rot_axis_list : array_like
        List of rotation axes.
    vec_list : array_like
        List of vectors to rotate.
    learning_rate : float
        Learning rate for the gradient descent optimization.
    num_iterations : int
        Number of iterations for the gradient descent optimization.
    initial_angle : float
        Initial guess for the rotation angle in radians.
        
    Returns
    -------
    tuple
        (angles, cosines) where:
        - angles is a list of cumulative rotation angles in degrees.
        - cosines is a list of cosines of the cumulative angles.
    
    Examples
    --------
    >>> angles, cosines = compute_angles_and_cos(endvx, rot_axis_list, vec_list, 0.01, 100, 0.1)
    """
    angles = []
    cosines = []
    zeta_0 = 0.0

    for i in range(len(endvx) - 1):
        zeta = gradient_descent(initial_angle, vec_list[i + 1], vec_list[i], rot_axis_list[i], learning_rate, num_iterations)
        zeta_0 += zeta
        cos = np.cos(zeta_0)
        cosines.append(cos)
        angles.append(np.degrees(zeta_0))

    return angles, cosines


def find_peak_properties(sliding_avg_rot_head, time_values_av, omega, dist, condition_omit_end=False, condition_omit_other=False, omited_peaks_end=0, middle_peak_omited=None):
    """
    Find peaks in a time series and compute related properties.
    
    Parameters
    ----------
    sliding_avg_rot_head : array_like
        Sliding average of rotational data.
    time_values_av : array_like
        Corresponding time values.
    omega : float
        Angular frequency of the body rotation.
    dist : int
        Minimum distance between peaks.
    condition_omit_end : bool, optional
        Whether to omit peaks at the end, by default False.
    condition_omit_other : bool, optional
        Whether to omit specific peaks, by default False.
    omited_peaks_end : int, optional
        Number of peaks to omit at the end, by default 0.
    middle_peak_omited : int or list, optional
        Index or indices of specific peaks to omit, by default None.
        
    Returns
    -------
    tuple
        (peaks, formatted_beats_per_rot) where:
        - peaks is an array of peak indices.
        - formatted_beats_per_rot is a string with the number of beats per body rotation.
    
    Examples
    --------
    >>> peaks, beats = find_peak_properties(data, time_values, 2.0, 10)
    """
    peaks, _ = find_peaks(sliding_avg_rot_head, distance=dist)
    if condition_omit_end == True:
        peaks = peaks[:-omited_peaks_end]
    if condition_omit_other == True:
        mask = np.ones(len(peaks), dtype=bool)
        mask[middle_peak_omited] = False
        peaks = peaks[mask]
    peak_times = np.array(time_values_av)[peaks]
    peak_distances = np.diff(peak_times)
    average_distance = np.mean(peak_distances)
    peak_frequency = 1 / average_distance
    beats_per_body_rot = omega / peak_frequency
    formatted_beats_per_rot = "{:.2f}".format(beats_per_body_rot)
    return peaks, formatted_beats_per_rot


def calc_msd_fft(x):
    """
    Calculate Mean Square Displacement using FFT method.
    
    The MSD is calculated using the Fast Fourier Transform method as described in:
    "nMoldyn - Interfacing spectroscopic experiments, molecular dynamics simulations 
    and models for time correlation functions."
    
    Parameters
    ----------
    x : array_like
        Time series data (positions).
        
    Returns
    -------
    numpy.ndarray
        Mean Square Displacement values for the first quarter of lags.
    
    Examples
    --------
    >>> trajectory = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> msd = calc_msd_fft(trajectory)
    >>> len(msd)
    2
    """
    if isinstance(x, list):
        x = np.array(x)  # Convert to a NumPy array for element-wise operations
    
    n = len(x)
    fk = np.fft.fft(x, n=2*n)
    power = fk * fk.conjugate()
    res = np.fft.ifft(power)[:n].real
    s2 = res / (n * np.ones(n) - np.arange(0, n))
    
    x2 = x ** 2 
    
    s1 = np.zeros(n)
    s1[0] = np.average(x2) * 2.0
    
    for m in range(1, n):
        s1[m] = np.average(x2[m:] + x2[:-m])
    
    msd = s1 - 2 * s2
    
    return msd[:n//4]   # integer division, in this case only looks at the first quarter


def velocity(dr_i, dr_e, delta_t):
    """
    Calculate velocity from displacement.
    
    Parameters
    ----------
    dr_i : float or array_like
        Initial displacement.
    dr_e : float or array_like
        Final displacement.
    delta_t : float
        Time interval.
        
    Returns
    -------
    float or array_like
        Absolute velocity.
    
    Examples
    --------
    >>> velocity(0, 10, 5)
    2.0
    """
    v_cell = np.abs(dr_e - dr_i) / delta_t
    return v_cell


def vel_msd(msd, t):
    """
    Calculate velocity from MSD.
    
    Parameters
    ----------
    msd : array_like
        Mean Square Displacement values.
    t : array_like
        Corresponding time values.
        
    Returns
    -------
    array_like
        Velocities calculated as sqrt(MSD)/t.
    
    Examples
    --------
    >>> vel_msd([4, 16], [2, 4])
    array([1., 1.])
    """
    v_cell = np.sqrt(msd) / t
    return v_cell


def linear_fit(t, a, b):
    """
    Linear function for curve fitting.
    
    Parameters
    ----------
    t : array_like
        Independent variable (usually time).
    a : float
        Slope.
    b : float
        Intercept.
        
    Returns
    -------
    array_like
        a*t + b
    
    Examples
    --------
    >>> linear_fit([1, 2, 3], 2, 1)
    array([3, 5, 7])
    """
    return a * t + b


def perform_linear_fit(time_values, coord_values):
    """
    Perform linear regression on time series data.
    
    Parameters
    ----------
    time_values : array_like
        Independent variable (time).
    coord_values : array_like
        Dependent variable (coordinates).
        
    Returns
    -------
    tuple
        (slope, intercept) of the fitted line.
    
    Examples
    --------
    >>> perform_linear_fit([0, 1, 2, 3], [1, 3, 5, 7])
    (2.0, 1.0)
    """
    params, _ = curve_fit(linear_fit, time_values, coord_values)
    slope, intercept = params
    return slope, intercept


def fit_msd_quadratic(msd, time_values):
    """
    Fit MSD data to a quadratic function.
    
    Parameters
    ----------
    msd : array_like
        Mean Square Displacement values.
    time_values : array_like
        Corresponding time values.
        
    Returns
    -------
    tuple
        (a_fit, msd_fit) where:
        - a_fit is the fitted quadratic coefficient.
        - msd_fit is the array of fitted MSD values.
    
    Examples
    --------
    >>> a, fitted_values = fit_msd_quadratic([0, 1, 4, 9], [0, 1, 2, 3])
    >>> a
    1.0
    """
    def quadratic_fit(t, a):
        return a * t**2
    # Perform the curve fitting
    popt, pcov = curve_fit(quadratic_fit, time_values, msd)
    # Extract the fitted parameter
    a_fit = popt[0]
    # Generate the fitted curve
    msd_fit = quadratic_fit(time_values, a_fit)
    return a_fit, msd_fit


def fit_msd(msd, time_values, fixed_D=None):
    """
    Fit MSD data to a model with diffusion and drift.
    
    The model is: MSD = 6*D*t + (v^2)*(t^2)
    where D is the diffusion coefficient and v is the drift velocity.
    
    Parameters
    ----------
    msd : array_like
        Mean Square Displacement values.
    time_values : array_like
        Corresponding time values.
    fixed_D : float, optional
        Fixed diffusion coefficient if known, by default None.
        
    Returns
    -------
    tuple
        If fixed_D is provided: (fixed_D, v_fit, msd_fit)
        If fixed_D is None: (D_fit, v_fit, msd_fit)
        where:
        - D_fit is the fitted diffusion coefficient.
        - v_fit is the fitted drift velocity.
        - msd_fit is the array of fitted MSD values.
    
    Examples
    --------
    >>> D, v, fitted_values = fit_msd([6, 24, 54], [1, 2, 3])
    >>> round(D, 2)
    1.0
    >>> round(v, 2)
    2.0
    """
    if fixed_D is not None:
        # If D is fixed, define a fitting function with only v as a parameter
        def msd_fit_func_fixed_D(t, v):
            return 6 * fixed_D * t + (v ** 2) * t ** 2

        # Perform the curve fitting for v only
        popt, pcov = curve_fit(msd_fit_func_fixed_D, time_values, msd)

        # Extract the fitted parameter
        v_fit = popt[0]

        # Generate the fitted curve
        msd_fit = msd_fit_func_fixed_D(time_values, v_fit)

        return fixed_D, v_fit, msd_fit

    else:
        # If D is not fixed, define a fitting function with both D and v as parameters
        def msd_fit_func(t, D, v):
            return 6 * D * t + (v ** 2) * t ** 2

        # Set the bounds for the parameters: D must be >= 0, v is unbounded
        bounds = (0, [np.inf, np.inf])

        # Perform the curve fitting for both D and v
        popt, pcov = curve_fit(msd_fit_func, time_values, msd, bounds=bounds)

        # Extract the fitted parameters
        D_fit, v_fit = popt

        # Generate the fitted curve
        msd_fit = msd_fit_func(time_values, D_fit, v_fit)

        return D_fit, v_fit, msd_fit


def calculate_average_path(x, y, z, n_total, av_over):
    """
    Calculate average trajectory by averaging over blocks of points.
    
    Parameters
    ----------
    x : array_like
        X coordinates.
    y : array_like
        Y coordinates.
    z : array_like
        Z coordinates.
    n_total : int
        Total number of points.
    av_over : int
        Number of points to average over.
        
    Returns
    -------
    tuple
        (avg_x, avg_y, avg_z) where each is a list of averaged coordinates.
    
    Examples
    --------
    >>> x = [1, 2, 3, 4, 5, 6]
    >>> y = [1, 1, 1, 2, 2, 2]
    >>> z = [0, 0, 0, 0, 0, 0]
    >>> calculate_average_path(x, y, z, 6, 3)
    ([2.0, 5.0], [1.0, 2.0], [0.0, 0.0])
    """
    avg_x = []
    avg_y = []
    avg_z = []
    for i in range(0, n_total, av_over):
        avg_x.append(np.mean(x[i:i+av_over]))
        avg_y.append(np.mean(y[i:i+av_over]))
        avg_z.append(np.mean(z[i:i+av_over]))
    return avg_x, avg_y, avg_z


def helix_radius(x, y, z, window_size=10):
    """
    Estimate the radius of a helical trajectory with a potentially curved axis.
    
    Parameters
    ----------
    x : array_like
        X coordinates of the trajectory.
    y : array_like
        Y coordinates of the trajectory.
    z : array_like
        Z coordinates of the trajectory.
    window_size : int, optional
        The number of neighboring points to use for local tangent calculation,
        by default 10. Adjust based on the curvature and resolution of the data.
    
    Returns
    -------
    tuple
        (R_mean, R_median), where R_mean is the mean radius and R_median is the median radius.
    
    Examples
    --------
    >>> import numpy as np
    >>> t = np.linspace(0, 4*np.pi, 100)
    >>> x = np.cos(t)
    >>> y = np.sin(t)
    >>> z = 0.1*t
    >>> R_mean, R_median = helix_radius(x, y, z)
    >>> round(R_mean, 1)
    1.0
    """
    # Combine x, y, z coordinates into an array of (x, y, z) points
    coords = np.vstack((x, y, z)).T
    
    # Initialize an array to store radius values
    radii = []
    
    # Loop through each point in the trajectory
    for i in range(len(coords)):
        # Select a local window of points around the current point
        start = max(0, i - window_size)
        end = min(len(coords), i + window_size + 1)
        local_points = coords[start:end]
        
        # Step 1: Calculate the local tangent vector using PCA
        pca = PCA(n_components=3)
        pca.fit(local_points)
        local_axis = pca.components_[0]  # Local tangent direction
        local_center = np.mean(local_points, axis=0)  # Approximate local center
        
        # Step 2: Calculate the distance from the point to the local axis
        d = coords[i] - local_center  # Vector from the local center to the point
        d_parallel = np.dot(d, local_axis) * local_axis  # Projection onto local axis
        d_perp = d - d_parallel  # Perpendicular component
        r = np.linalg.norm(d_perp)  # Distance from axis to point (radius)
        
        # Store the radius
        radii.append(r)
    
    # Step 3: Calculate the mean and median radius
    R_mean = np.mean(radii)
    R_median = np.median(radii)
    
    # Return the results
    return R_mean, R_median


def helix_msd(x, y, z, window_size=100, max_lag=50):
    """
    Calculate the parallel and perpendicular components of the Mean Square Displacement
    for a helical trajectory.
    
    Parameters
    ----------
    x : array_like
        X coordinates of the trajectory.
    y : array_like
        Y coordinates of the trajectory.
    z : array_like
        Z coordinates of the trajectory.
    window_size : int, optional
        Size of the window for local axis determination, by default 100.
    max_lag : int, optional
        Maximum lag time for MSD calculation, by default 50.
        
    Returns
    -------
    tuple
        (msd_parallel, msd_perpendicular) Mean Square Displacement components.
    """
    coords = np.vstack((x, y, z)).T
    n_points = len(coords)
    local_axes = []

    # Calculate local helix axis at each point
    for i in range(n_points):
        start = max(0, i - window_size)
        end = min(n_points, i + window_size + 1)
        local_points = coords[start:end]
        # PCA to get local axis
        pca = PCA(n_components=1)
        pca.fit(local_points)
        local_axis = pca.components_[0]  # Local tangent direction
        local_axes.append(local_axis)
    
    # Initialize MSD arrays for parallel and perpendicular components
    msd_parallel = np.zeros(max_lag)
    msd_perpendicular = np.zeros(max_lag)
    counts = np.zeros(max_lag)  # To count valid pairs for each lag

    # Calculate MSD for each lag time
    for lag in range(1, max_lag + 1):
        for i in range(n_points - lag):
            j = i + lag
            displacement = coords[j] - coords[i]
            
            # Decompose displacement into parallel and perpendicular components
            local_axis = local_axes[i]
            disp_parallel = np.dot(displacement, local_axis) * local_axis
            disp_perpendicular = displacement - disp_parallel
            
            # Accumulate squared displacements
            msd_parallel[lag - 1] += np.dot(disp_parallel, disp_parallel)
            msd_perpendicular[lag - 1] += np.dot(disp_perpendicular, disp_perpendicular)
            counts[lag - 1] += 1

    # Normalize by the number of pairs for each lag to get the mean
    msd_parallel /= counts
    msd_perpendicular /= counts

    return msd_parallel, msd_perpendicular