import numpy as np


def radial_grid(start_radius, radius_step, end_radius, degree_resolution):
    """
    A function to define a radial interpolation grid based on a unit circle,
    and centered on a geographic (lat, lon) point of interest. This methodology
    was developed by Loikith & Broccoli 2012* and was originally written in
    MATLAB. This Python implementation was developed as part of my M.S. thesis
    at Portland State University.

    -Dmitri Kalashnikov (dmitrik1357@gmail.com)

    * Loikith, P. C., and A. J. Broccoli, 2012: Characteristics of Observed
      Atmospheric Circulation Patterns Associated with Temperature Extremes
      over North America. J. Climate, 25, 7266–7281,
      https://doi.org/10.1175/JCLI-D-11-00709.1

    Parameters
    ----------
    start_radius : int or float
        Radius distance in km (from origin) of first (innermost)
        interpolation ring. If `start_radius` = 0, interpolation at
        origin and at 0 degree azimuth will be duplicated in order
        to produce a continuous contourf plot for visualization. If
        `start_radius` is set to any value higher than zero, both the
        origin and 0 degree azimuth will be interpolated only once.
        Use this version if computing statistics as all
        interpolation points will be unique. Use version with
        `start_radius` = 0 for plotting, as otherwise the plot will
        show no values around center and no values in a vertical
        slice at 0 degrees from center.
    radius_step : int or float
        Radius distance in km between each interpolation ring. When
        `start_radius` != 0, `radius_step` will be equal to `start_radius`.
    end_radius : int or float
        Radius distance in km (from origin) of last (outermost)
        interpolation ring; this distance defines the radius of the
        full circle and the outer edge of interpolated values relative
        to the origin latitude/longitude point (e.g. 2500 km).
    degree_resolution : int or float
        Spacing, in degrees, between each interpolation point
        on unit circle. For example, specifying a value of 1
        will yield 360 interpolation points on each
        interpolation ring, one point for each degree increment.

    Returns
    -------
    radius_steps, degree_steps : ndarrays
        Vectors of polar coordinates (kilometers, degrees) defining the
        radial interpolation grid in geographic space.
    """

    assert start_radius >= 0, "Radius values must not be negative"
    assert radius_step < (end_radius - start_radius),"""
Radius steps must be less than full radius"""
    assert 0 < degree_resolution <= 90,"""
Degree resolution should be positive value not exceeding 90"""

    # If start_radius is set to zero, will duplicate interpolation of origin
    # and 0-degree (360-degree) azimuth. This is done to create smooth contourf
    # plot for visualization.
    if start_radius == 0:
        radius_steps = np.arange(start_radius,end_radius+1,radius_step)
        degree_steps = np.arange(0,361,degree_resolution)

    # Version without duplication, for computing statistics.
    else:
        radius_steps = np.arange(start_radius,end_radius+1,radius_step)
        degree_steps = np.arange(0+degree_resolution,361,degree_resolution)

    return radius_steps, degree_steps

