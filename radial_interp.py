import numpy as np
import geopy
import geopy.distance as gd
import scipy.interpolate as si


def radial_grid(start_radius, radius_step, end_radius, degree_resolution):
    """
    A function to define a radial interpolation grid based on a unit circle, and centered
    on a geographic (lat, lon) point of interest. This methodology was developed by Loikith
    & Broccoli 2012* and was originally written in MATLAB. This Python implementation was
    developed as part of my M.S. thesis at Portland State University.

    -Dmitri Kalashnikov (dmitrik1357@gmail.com)

    * Loikith, P. C., and A. J. Broccoli, 2012: Characteristics of Observed Atmospheric
     Circulation Patterns Associated with Temperature Extremes over North America. J. Climate, 25,
     7266–7281, https://doi.org/10.1175/JCLI-D-11-00709.1

    Parameters
    ----------
    start_radius : Radius distance in km (from origin) of first (innermost) interpolation ring.
                   If start_radius = 0, interpolation at origin and at 0 degree azimuth
                   will be duplicated in order to produce a continous contourf plot for visualization.
                   If start_radius is set to any value higher than zero, both the origin and
                   0 degree azimuth will be interpolated only once. Use this version if computing
                   statistics as all interpolation points will be unique. Use version with
                   start_radius = 0 for plotting, as otherwise the plot will show no values
                   around center and no values in a vertical slice at 0 degrees from center.
    radius_step : Radius distance in km between each interpolation ring. When start_radius != 0,
                  radius_step will be equal to start_radius.
    end_radius : Radius distance in km (from origin) of last (outermost) interpolation ring;
                 this distance defines the radius of the full circle and the outer edge of
                 interpolated values relative to the origin latitude/longitude point (e.g. 2500 km).
    degree_resolution : Spacing, in degrees, between each interpolation point on unit circle.
                        For example, specifying a value of 1 will yield 360 interpolation points
                        on each interpolation ring.

    Returns
    -------
    radius_steps, degree_steps : Vectors of polar coordinates (kilometers, degrees) defining the radial
                                 interpolation grid in geographic space.
    """

    assert start_radius >= 0, "radius values must not be negative"
    assert radius_step < (end_radius - start_radius),"""
radius steps must be less than full radius"""
    assert 0 < degree_resolution <= 90,"""
degree resolution should be positive value not exceeding 90"""

    # If start_radius is set to zero, will duplicate interpolation of origin and 0-degree
    # (360-degree) azimuth. This is done to create smooth contourf plot for visualization.
    if start_radius == 0:
        radius_steps = np.arange(start_radius,end_radius+1,radius_step)
        degree_steps = np.arange(0,360+1,degree_resolution)

    # Version without duplication, for computing statistics.
    else:
        radius_steps = np.arange(start_radius,end_radius+1,radius_step)
        degree_steps = np.arange(0+degree_resolution,360+1,degree_resolution)

    return radius_steps, degree_steps


def radial_interp(a, a_lats, a_lons, center_lat, center_lon, radius_steps, degree_steps,
                  return_coordinates=False):
    """
    A function to interpolate continuous, geographic data using a unit circle centered
    on a geographic (lat, lon) point of interest. This methodology was developed by Loikith
    & Broccoli 2012* and was originally written in MATLAB. This Python implementation was
    developed as part of my M.S. thesis at Portland State University.

    -Dmitri Kalashnikov (dmitrik1357@gmail.com)

    * Loikith, P. C., and A. J. Broccoli, 2012: Characteristics of Observed Atmospheric
     Circulation Patterns Associated with Temperature Extremes over North America. J. Climate, 25,
     7266–7281, https://doi.org/10.1175/JCLI-D-11-00709.1

    Parameters
    ----------
    a : 2D or 3D input array of values from which to interpolate (data should be spatial
            and continuous on a regular grid, e.g. raster, reanalysis, climate model output, etc);
            with 3rd dimension representing time.
    a_lats : Vector of latitude values defining input data array.
    a_lons : Vector of longitude values defining input data array.
    center_lat : Latitude defining origin around which the unit circle interpolator
                       will be built.
    center_lon : Longitude defining origin around which the unit circle interpolator
                       will be built.
    radius_steps : Distance (km) between interpolation rings.
    degree_steps : Azimuth resolution (degrees) between interpolation points.
    return_coordinates : Boolean to indicate whether lat & lon interpolation coordinates
                         should be returned, default is "False" for contourf plotting. Set
                         to "True" if mapping on geographically projected axes.

    Returns
    -------
    interp_vals :  For 2D input array: returns vector of interpolated values drawn from input
                   array at every (lat,lon) point on radial grid. For 3D input arrary, returns 2D array
                   of (interpolated values, timesteps).
    interp_lats :  The latitude coordinates of interpolated points.
    interp_lons :  The longitude coordinates of interpolated points.
    """

    assert radius_steps[0] >= 0, "starting radius must not be negative"

    interp_lats = []
    interp_lons = []

    if radius_steps[0] == 0:
        for km in radius_steps:
            for deg in degree_steps:
                start = geopy.Point(center_lat,center_lon)
                transect = gd.distance(kilometers = km)
                dest = transect.destination(point = start, bearing = deg)
                interp_lats.append(dest[0])
                interp_lons.append(dest[1])

    else:
        for km in radius_steps:
            for deg in degree_steps:
                start = geopy.Point(center_lat,center_lon)
                transect = gd.distance(kilometers = km)
                dest = transect.destination(point = start, bearing = deg)
                interp_lats.append(dest[0])
                interp_lons.append(dest[1])
        # Add lat & lon of origin
        interp_lats = np.hstack([center_lat, interp_lats])
        interp_lons = np.hstack([center_lon, interp_lons])

    interp_vals = si.interpn((a_lons,a_lats),a,(interp_lons,interp_lats))

    # For mapping on geographic projection, can use the interpolated (lat,lon) values
    if return_coordinates == True:
        return interp_vals, interp_lats, interp_lons
    # For non-projected contourf plot, lat & lon values will not be needed
    else:
        return interp_vals



