import numpy as np
import geopy
import geopy.distance as gd
import scipy.interpolate as si


def radial_interp(a, a_lats, a_lons, center_lat, center_lon, radius_steps,
                  degree_steps, return_coordinates=False):
    """
    A function to interpolate continuous, geographic data using a unit circle
    centered on a geographic (lat, lon) point of interest. This methodology was
    developed by Loikith & Broccoli 2012* and was originally written in MATLAB.
    This Python implementation was developed as part of my M.S. thesis at
    Portland State University.

    -Dmitri Kalashnikov (dmitrik1357@gmail.com)

    * Loikith, P. C., and A. J. Broccoli, 2012: Characteristics of Observed
      Atmospheric Circulation Patterns Associated with Temperature Extremes
      over North America. J. Climate, 25, 7266–7281,
      https://doi.org/10.1175/JCLI-D-11-00709.1

    Parameters
    ----------
    a : ndarray
        2D or 3D input array of values from which to interpolate (data should
        be spatial and continuous on a regular grid, e.g. raster, reanalysis,
        climate model output, etc); with 3rd dimension representing time.
    a_lats : int or float
        Vector of latitude values defining input data array.
    a_lons : int or float
        Vector of longitude values defining input data array.
    center_lat : int or float
        Latitude coordinate of origin, around which the unit circle
        interpolator will be built.
    center_lon : int or float
        Longitude coordinate of origin, around which the unit circle
        interpolator will be built.
    radius_steps : int or float
        Distance (km) between interpolation rings.
    degree_steps : int or float
        Azimuth resolution (degrees) between interpolation
        points on each interpolation ring.
    return_coordinates : True, optional
        Boolean to indicate whether lat & lon interpolation
        coordinates should be returned, default is "False" for
        Matplotlib.pyplot contourf plotting. Set to "True" if mapping on
        geographically projected axes.

    Returns
    -------
    interp_vals : ndarray
        For 2D input array: returns vector of interpolated values
        extracted from input array at every (lat,lon) point on radial grid.
        For 3D input arrary: returns 2D array of (interpolated values,
        timesteps).
    interp_lat : ndarray
        The latitude coordinates of interpolated points.
    interp_lon : ndarray
        The longitude coordinates of interpolated points.
    """

    assert 2 <= a.ndim <= 3, "Input array must be 2D or 3D"
    assert radius_steps[0] >= 0, "Starting radius must not be negative"

    if np.size(center_lat) != 1:
        raise ValueError("Must provide single value for latitude")
    if np.size(center_lon) != 1:
        raise ValueError("Must provide single value for longitude")

    interp_lat = []
    interp_lon = []

    if radius_steps[0] == 0:
        for km in radius_steps:
            for deg in degree_steps:
                start = geopy.Point(center_lat,center_lon)
                transect = gd.distance(kilometers = km)
                dest = transect.destination(point = start, bearing = deg)
                interp_lat.append(dest[0])
                interp_lon.append(dest[1])

    else:
        for km in radius_steps:
            for deg in degree_steps:
                start = geopy.Point(center_lat,center_lon)
                transect = gd.distance(kilometers = km)
                dest = transect.destination(point = start, bearing = deg)
                interp_lat.append(dest[0])
                interp_lon.append(dest[1])
        # Add lat & lon of origin
        interp_lat = np.hstack([center_lat, interp_lat])
        interp_lon = np.hstack([center_lon, interp_lon])

    interp_vals = si.interpn((a_lons,a_lats),a,(interp_lon,interp_lat))

    # For mapping on geographic projection, can use the interpolated (lat,
    # lon) values
    if return_coordinates == True:
        return interp_vals, interp_lat, interp_lon
    # For non-projected contourf plot, lat & lon values will not be needed
    else:
        return interp_vals


