import numpy as np
from accum import accum
from pol2cart import pol2cart


def create_mappable(radius_steps, degree_steps, interp_vals):
    """
    A function to create mappable inputs to contourf plot, for visualizing data obtained
    from radial interpolation.

    Parameters
    ----------
    radius_steps : Distance (km) between interpolation rings on unit circle interpolator.
    degree_steps : Azimuth resolution (degrees) between interpolation points.
    interp_vals : Interpolated values corresponding to above (km, deg) coordinates.

    Returns
    -------
    x, y : Cartesian coordinates on unit circle, corresponding to (km, deg) coordinates
           obtained from radial interpolation
    array : Interpolated values referenced to cartesian (x,y) coordinates above for contourf plotting.
    """

    assert radius_steps[0] == 0, "starting radius must be zero for contour mappable"

    rho = radius_steps/radius_steps[-1] # standardize radius values to unit circle (r = 1)
    rho_vec = np.repeat(rho,len(degree_steps)) # vector of rho values corresponding to lat & lon points
    theta = np.deg2rad(degree_steps) # convert to radians
    theta_vec = np.tile(theta,len(radius_steps)) # vector of theta values corresponding to lat & lon points

    # Calculate index for all (x,y) coordinates.
    xi = np.tile(degree_steps,len(radius_steps))
    yi = np.repeat(np.arange(len(radius_steps)),len(degree_steps))

    # Accmap of (x,y) index values used to build array.
    subs = np.vstack([yi, xi]).T

    # Build mappable array from interp_vals using (x,y) index values.
    array = accum(subs, interp_vals)
    (th, rh) = np.meshgrid(theta,rho)
    (x,y) = pol2cart(th, rh)

    # Return 3 vectors - the array values, the x-coordinates, and the y-coordinates
    # for input into contourf plot.
    return array, x, y