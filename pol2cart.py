import numpy as np


def pol2cart(theta, rho):
    """
    A simple function to convert from polar to cartesian (x,y) coordinates, in
    the style of MATLAB `pol2cart` function.

    Parameters
    ----------
    theta : int or float
        Theta coordinates (in radians) on polar coordinate grid.
    rho : int or float
        Rho coordinates (between 0 and 1) on polar coordinate grid.

    Returns
    -------
    x, y : ndarrays
        Arrays of Cartesian coordinates (x & y) corresponding to input polar
        coordinates.
    """

    x = rho * np.cos(theta)
    y = rho * np.sin(theta)
    return(x,y)
