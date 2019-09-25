import numpy as np


def pol2cart(theta, rho):
    """
    A simple function to convert from polar to cartesian (x,y) coordinates, in the style
    of MATLAB 'pol2cart' function.

    Parameters
    ----------
    theta : Theta coordinates (in radians) on polar coordinate grid.
    rho : Rho coordinates (0-1) on polar coordinate grid.

    Returns
    -------
    x, y :  Cartesian (x,y) coordinates corresponding to input polar coordinates.
    """

    x = rho * np.cos(theta)
    y = rho * np.sin(theta)
    return(x,y)



