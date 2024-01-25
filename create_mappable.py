import numpy as np
from pol2cart import pol2cart


def create_mappable(radius_steps, degree_steps, interp_vals):
    """
    A function to create mappable inputs to contourf plot, for visualizing data
    obtained from radial interpolation.

    Parameters
    ----------
    radius_steps : ndarray
        Distance (km) between interpolation rings on unit circle
        interpolator.
    degree_steps : ndarray
        Azimuth resolution (degrees) between interpolation points on unit
        circle interpolator.
    interp_vals : ndarray
        Interpolated values corresponding to above (km, deg) coordinates.

    Returns
    -------
    x, y : ndarrays
        Cartesian coordinates on unit circle, corresponding to (km, deg)
        coordinates obtained from radial interpolation.
    array : ndarray
        Interpolated values corresponding to Cartesian (x,y) coordinates above
        for contourf plotting.
    """

    assert interp_vals.ndim == 1, "Input data values must be 1D"
    assert radius_steps[0] == 0, """
Starting radius must be zero for contourf mappable"""

    rho = radius_steps/radius_steps[-1] # radius values on unit circle (r = 1)
    theta = np.deg2rad(degree_steps) # convert to radians
    array = np.reshape(interp_vals,(len(radius_steps),len(degree_steps))) # reshape to match coordinates
    (th, rh) = np.meshgrid(theta, rho) # create meshgrid on polar coordinates
    (x, y) = pol2cart(th, rh) # convert meshgrid to cartesian (x,y) coordinates

    # Return 3 vectors - the array values, the x-coordinates, and the
    # y-coordinates for input into contourf plot.
    return array, x, y
