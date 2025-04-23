"""
Constants
=========

# WGS84 constants (IS-GPS-200M and NIMA TR8350.2)
A_E = 6378137.0             # Earth's semi-major axis (m) (p. 109)
E2 = 6.694379990141317e-3   # Earth's eccentricity squared (ND) (derived)
W_EI = 7.2921151467e-5      # sidereal Earth rate (rad/s) (p. 106)

# gravity coefficients
GRAV_E = 9.7803253359       # gravity at equator (m/s^2)
GRAV_K = 1.93185265241e-3
GRAV_F = 3.35281066475e-3   # ellipsoidal flattening
GRAV_M = 3.44978650684e-3

Functions and methods
=====================

Support Functions
-----------------

class Baro:
    def __init__(self, baro_name=None, er_int=0.0):
    def reset(self, er_int=0.0):

def time_str(t_seconds):

def progress(k, K, width=None):

def rpy_to_dcm(rpy, degs=False):

def dcm_to_rpy(C, degs=False):

def orthonormalize_dcm(C):

def rodrigues_rotation(theta):

def inverse_rodrigues_rotation(Delta):

def wrap(Y):

def ned_enu(vec):

def vanloan(F, B=None, Q=None, T=None):

Path Generation
---------------

def path_still(T, t_dur=3600.0, llh=None):

def path_eight(T, t_dur=3600.0, R=1000.0, H=100.0):

class path_waypoints:
    def __init__(self, points, velocity, R_min, T,
            ax=None, plot=True, res=0.01):

def llh_to_vne(llh_t, T):

def vne_to_rpy(vne_t, grav_t, T, alpha=0.06, wind=None):

def est_wind(vne_t, yaw_t):

def noise_fogm(T, tau, var, K):

Gravity
-------

def somigliana(llh):

Inertial Mechanization
----------------------

def inv_mech(llh_t, rpy_t, T, grav_model=somigliana):

def mech(fbbi_t, wbbi_t, llh0, vne0, rpy0, T, hae_t=None,
        baro_name=None, grav_model=somigliana, show_progress=True):

def mech_step(fbbi, wbbi, llh, vne, Cnb, grav_model=somigliana):

def jacobian(fbbi, llh, vne, Cnb):
"""

import os
import math
import time
import numpy as np
import matplotlib.pyplot as plt

# WGS84 constants (IS-GPS-200M and NIMA TR8350.2)
A_E = 6378137.0             # Earth's semi-major axis (m) (p. 109)
E2 = 6.694379990141317e-3   # Earth's eccentricity squared (ND) (derived)
W_EI = 7.2921151467e-5      # sidereal Earth rate (rad/s) (p. 106)

# gravity coefficients
GRAV_E = 9.7803253359       # gravity at equator (m/s^2)
GRAV_K = 1.93185265241e-3
GRAV_F = 3.35281066475e-3   # ellipsoidal flattening
GRAV_M = 3.44978650684e-3

# -----------------
# Support Functions
# -----------------

class Persistent:
    t_init = None
    t_last = None


class Baro:
    """
    Barometric altitude aiding model.

    Attributes
    ----------
    name : str
        The name of the barometric altitude aiding model. This must be one of
        'savage', 'rogers', 'widnall', 'silva', 'iae', 'ise', 'itae', or 'itse'.
    K : list
        List of feedback coefficients.
    er : float
        Error between the mechanization algorithm's altitude and the barometric
        altitude (m).
    er_int : float
        Integral of the error between the mechanization algorithm's altitude and
        the barometric altitude (m s).
    """

    # Dictionary of barometric altitude aiding coefficients
    K_dict = {
        "savage":   [3e-1, 3e-2, 1e-3],
        "rogers":   [3e-2, 4e-4, 2e-6],
        "widnall":  [1.003, 4.17e-3, 4.39e-6],
        "silva":    [1.46e-1, 1.84e-2, 4.46e-4],
        "iae":      [1.0, 1e-3, 1e-6],
        "ise":      [1.0, 5e-3, 1e-6],
        "itae":     [1.0, 1.0, 1e-6],
        "itse":     [1.0, 1e-3, 1e-6]}

    def __init__(self, baro_name=None, er_int=0.0):
        """
        Initialize the barometric altitude aiding model.

        Parameters
        ----------
        baro_name : str, default None
            The name of the barometric altitude aiding model. This must be one
            of 'savage', 'rogers', 'widnall', 'silva', 'iae', 'ise', 'itae', or
            'itse'.
        er_int : float, default 0.0
            The initial integral of integrated error, where error is defined as
            the integral of the error between the mechanization algorithm's
            altitude and the barometric altitude (m s).
        """

        if baro_name in Baro.K_dict:
            self.name = baro_name
            self.K = Baro.K_dict[baro_name]
            self.er = 0.0
            self.er_int = er_int
        else:
            raise ValueError(f"{baro_name} is not a valid model name!")

    def reset(self, er_int=0.0):
        """ Reset the baro model's state. """

        self.er = 0.0
        self.er_int = er_int


def time_str(t_seconds):
    """ Convert time in seconds to a clock string of the form
    `HH:MM:SS.S`. """
    t_seconds = abs(t_seconds)
    hours = int(t_seconds/3600)
    minutes = int((t_seconds - hours*3600)//60)
    seconds = (t_seconds % 60)
    clock_str = "%02d:%02d:%04.1f" % (hours, minutes, seconds)
    return clock_str


def progress(k, K, width=None):
    """
    Output a simple progress bar with percent complete to the terminal. When `k`
    equals `K - 1`, the progress bar will complete and start a new line.

    Parameters
    ----------
    k : int
        Index which should grow monotonically from 0 to K - 1.
    K : int
        Final index value of `k` plus 1.
    width : int, default None
        Width of the full string, including the percent complete, the bar, and
        the clock. If not given, the width of the terminal window will be used.
    """

    # Skip this call if the bar is not done but not enough time has passed.
    t_now = time.perf_counter()
    if k == 0:
        Persistent.t_init = t_now
    else:
        if (k < K - 1) and (Persistent.t_last is not None) and \
                (t_now - Persistent.t_last < 0.1):
            return
    Persistent.t_last = t_now

    # Default the width to the terminal width or 60.
    if width is None:
        try: # Try to get the true size.
            width, _ = os.get_terminal_size()
            use_esc = True
        except: # If getting terminal size fails, use default values.
            width = 60
            use_esc = False

    # Get the ratio.
    ratio = (k + 1)/K

    # Get the clock string.
    if k > 0:
        t_elapsed = t_now - Persistent.t_init
        if K > 1:
            t_elapsed *= K/(K - 1)
        if k == K - 1:
            clk_str = "  " + time_str(t_elapsed)
        else:
            t_remaining = t_elapsed*(1.0 - ratio)/ratio
            clk_str = " -" + time_str(t_remaining)
    else:
        clk_str = ""

    # Define the color commands.
    if use_esc:
        gray = "\x1b[37m"
        reset = "\x1b[39m"
    else:
        gray = ""
        reset = ""

    # Get the component lengths.
    N = width - 6 - len(clk_str) # maximum length of bar
    n = min(int(N*ratio), N) # filled-bar length
    m = max(0, N - n)
    if k < K - 1:
        print(f"\r{int(100*ratio):3d}% " # percentage
            + "="*n # filled bar
            + gray + "-"*m + reset # unfilled bar
            + clk_str, end='', flush=True)
    else:
        print(f"\r{int(100*ratio):3d}% " # percentage
            + "="*n # filled bar
            + gray + "-"*m + reset # unfilled bar
            + clk_str, flush=True)


def rpy_to_dcm(rpy, degs=False):
    """
    Convert roll, pitch, and yaw Euler angles to a direction cosine matrix that
    represents a zyx sequence of right-handed rotations.

    Parameters
    ----------
    rpy : (3,) or (3, K) or (K, 3) list, tuple, or np.ndarray
        Roll, pitch, and yaw Euler angle.
    degs : bool, default False
        Flag to interpret angles as degrees.

    Returns
    -------
    C : (3, 3) or (K, 3, 3) np.ndarray
        Rotation matrix or stack of K rotation matrices.

    See Also
    --------
    dcm_to_rpy
    rot

    Notes
    -----
    This is equivalent to generating a rotation matrix for the rotation from the
    navigation frame to the body frame. However, if you want to rotate from the
    body frame to the navigation frame (an xyz sequence of right-handed
    rotations), transpose the result of this function. This is a convenience
    function. You could instead use the `rot` function as follows:

        C = rot([yaw, pitch, roll], [2, 1, 0])

    However, the `rpy_to_dcm` function will compute faster than the `rot`
    function.
    """

    # Check input.
    if isinstance(rpy, (list, tuple)):
        rpy = np.array(rpy)
    trs = (rpy.ndim == 2 and rpy.shape[0] != 3)
    s = np.pi/180 if degs else 1.0

    # Tranpose input.
    if trs:
        rpy = rpy.T

    if rpy.ndim == 1:
        # Get the cosine and sine functions.
        r, p, y = rpy
        cr = math.cos(s*r)
        sr = math.sin(s*r)
        cp = math.cos(s*p)
        sp = math.sin(s*p)
        cy = math.cos(s*y)
        sy = math.sin(s*y)

        # Build the output matrix.
        C = np.array([
            [            cp*cy,             cp*sy,   -sp],
            [-cr*sy + sr*sp*cy,  cr*cy + sr*sp*sy, sr*cp],
            [ sr*sy + cr*sp*cy, -sr*cy + cr*sp*sy, cr*cp]])
    else:
        # Get the cosine and sine functions.
        cr = np.cos(s*rpy[0])
        sr = np.sin(s*rpy[0])
        cp = np.cos(s*rpy[1])
        sp = np.sin(s*rpy[1])
        cy = np.cos(s*rpy[2])
        sy = np.sin(s*rpy[2])

        # Build the output matrix.
        C = np.zeros((rpy.shape[1], 3, 3))
        C[:, 0, 0] = cp*cy
        C[:, 0, 1] = cp*sy
        C[:, 0, 2] = -sp
        C[:, 1, 0] = -cr*sy + sr*sp*cy
        C[:, 1, 1] = cr*cy + sr*sp*sy
        C[:, 1, 2] = sr*cp
        C[:, 2, 0] = sr*sy + cr*sp*cy
        C[:, 2, 1] = -sr*cy + cr*sp*sy
        C[:, 2, 2] = cr*cp

    return C


def dcm_to_rpy(C, degs=False):
    """
    Convert the direction cosine matrix, `C`, to vectors of `roll`, `pitch`,
    and `yaw` (in that order) Euler angles.

    This `C` represents the z, y, x sequence of right-handed rotations. For
    example, if the DCM converted vectors from the navigation frame to the body
    frame, the roll, pitch, and yaw Euler angles would be the consecutive angles
    by which the vector would be rotated from the navigation frame to the body
    frame. This is as opposed to the Euler angles required to rotate the vector
    from the body frame back to the navigation frame.

    Parameters
    ----------
    C : (3, 3) or (K, 3, 3) list, tuple, or np.ndarray
        Rotation direction cosine matrix or stack of K such matrices.
    degs : bool, default False
        Flag to convert angles to degrees.

    Returns
    -------
    rpy : (3,) or (3, K) np.ndarray
        Roll, pitch, and yaw Euler angle.

    See Also
    --------
    rpy_to_dcm

    Notes
    -----
    If we define `C` as

            .-             -.
            |  c11 c12 c13  |
        C = |  c21 c22 c23  |
            |  c31 c32 c33  |
            '-             -'
            .-                                                 -.
            |       (cy cp)             (sy cp)          -sp    |
          = |  (cy sp sr - sy cr)  (sy sp sr + cy cr)  (cp sr)  |
            |  (sy sr + cy sp sr)  (sy sp cr - cy sr)  (cp cr)  |
            '-                                                 -'

    where `c` and `s` mean cosine and sine, respectively, and `r`, `p`, and `y`
    mean roll, pitch, and yaw, respectively, then we can see that

                                        .- cp sr -.
        r = arctan2(c23, c33) => arctan | ------- |
                                        '- cp cr -'

                                        .- sy cp -.
        y = arctan2(c12, c11) => arctan | ------- |
                                        '- cy cp -'

    where the cp values cancel in both cases. The value for pitch could be found
    from c13 alone:

        p = arcsin(-c13)

    However, this tends to suffer from numerical error around +- pi/2. So,
    instead, we will use the fact that

          2     2               2     2
        cy  + sy  = 1   and   cr  + sr  = 1 .

    Therefore, we can use the fact that

           .------------------------
          /   2      2      2      2     .--
        `/ c11  + c12  + c23  + c33  = `/ 2  cos( |p| )

    to solve for pitch. We can use the negative of the sign of c13 to give the
    proper sign to pitch. The advantage is that in using more values from the
    DCM matrix, we can can get a value which is more accurate. This works well
    until we get close to a pitch value of zero. Then, the simple formula for
    pitch is actually better. So, we will use both and do a weighted average of
    the two, based on pitch.

    References
    ----------
    .. [1]  Titterton & Weston, "Strapdown Inertial Navigation Technology"
    """

    # Check input.
    if isinstance(C, (list, tuple)):
        C = np.array(C)
    s = np.pi/180 if degs else 1.0
    SQ2 = math.sqrt(2)

    if C.ndim == 2:
        # Parse out the elements of the DCM that are needed.
        c11 = C[0, 0]
        c33 = C[2, 2]
        c12 = C[0, 1]
        c13 = C[0, 2]
        c23 = C[1, 2]

        # Get roll.
        rpy = np.zeros(3)
        rpy[0] = math.atan2(c23, c33)

        # Get pitch.
        sp = min(max(-c13, -1.0), 1.0)
        pa = math.asin(sp)
        nm = math.sqrt(c11**2 + c12**2 + c23**2 + c33**2)
        nm = min(max(nm, -SQ2), SQ2)
        pb = math.acos(nm/SQ2)
        rpy[1] = (1.0 - abs(sp))*pa + sp*pb

        # Get yaw.
        rpy[2] = math.atan2(c12, c11)
    else:
        # Parse out the elements of the DCM that are needed.
        c11 = C[:, 0, 0]
        c33 = C[:, 2, 2]
        c12 = C[:, 0, 1]
        c13 = C[:, 0, 2]
        c23 = C[:, 1, 2]

        # Get roll.
        r = np.arctan2(c23, c33)

        # Get pitch.
        sp = np.clip(-c13, -1.0, 1.0)
        pa = np.arcsin(sp)
        nm = np.sqrt(c11**2 + c12**2 + c23**2 + c33**2)
        nm = np.clip(nm, -SQ2, SQ2)
        pb = np.arccos(nm/SQ2)
        p = (1.0 - np.abs(sp))*pa + sp*pb

        # Get yaw.
        y = np.arctan2(c12, c11)

        # Build the output.
        rpy = np.array([r, p ,y])/s

    return rpy


def orthonormalize_dcm(C):
    """
    Orthonormalize the rotation matrix using the Modified Gram-Schmidt
    algorithm. This function modifies the matrix in-place. Note that this
    algorithm only moves the matrix towards orthonormality; it does not
    guarantee that after one function call the returned matrix will be
    orthonormal. However, with a 1e-15 tolerance, orthonormality can be
    acheived typically within at most 2 function calls.

    Parameters
    ----------
    C : (3, 3) np.ndarray
        Square matrix.
    """

    # Orthonormalize a single matrix.
    C[:, 0] /= math.sqrt(C[0, 0]**2 + C[1, 0]**2 + C[2, 0]**2)
    C[:, 1] -= C[:, 0].dot(C[:, 1])*C[:, 0]
    C[:, 1] /= math.sqrt(C[0, 1]**2 + C[1, 1]**2 + C[2, 1]**2)
    C[:, 2] -= C[:, 0].dot(C[:, 2])*C[:, 0]
    C[:, 2] -= C[:, 1].dot(C[:, 2])*C[:, 1]
    C[:, 2] /= math.sqrt(C[0, 2]**2 + C[1, 2]**2 + C[2, 2]**2)


def rodrigues_rotation(theta):
    """
    Get the matrix exponential of the skew-symmetric matrix of the rotation
    vector `theta`.

        Delta = exp([theta] )
                           x

    The rotation vector should not have a norm greater than pi. If it does,
    scale the vector by `-(2 pi - n)/n`, where `n` is the norm of the rotation
    vector.

    Parameters
    ----------
    theta : (3,) list or np.ndarray
        Three-element vector of angles in radians.

    Returns
    -------
    Delta : (3, 3) np.ndarray
        Three-by-three matrix.
    """

    # Get the vector norm.
    x2 = theta[0]*theta[0]
    y2 = theta[1]*theta[1]
    z2 = theta[2]*theta[2]
    nm2 = x2 + y2 + z2
    nm = math.sqrt(nm2)

    # Get the sine and cosine factors.
    if nm < 0.04e-6:
        s = 1.0
    else:
        s = math.sin(nm)/nm
    if nm < 0.2e-3:
        c = 0.5
    else:
        c = (1 - math.cos(nm))/nm2

    # Get the rotation matrix.
    Delta = np.array([
        [1.0 - c*(y2 + z2),
            c*theta[0]*theta[1] - s*theta[2],
            c*theta[0]*theta[2] + s*theta[1]],
        [c*theta[0]*theta[1] + s*theta[2],
            1.0 - c*(x2 + z2),
            c*theta[1]*theta[2] - s*theta[0]],
        [c*theta[0]*theta[2] - s*theta[1],
            c*theta[1]*theta[2] + s*theta[0],
            1.0 - c*(x2 + y2)]])

    return Delta


def inverse_rodrigues_rotation(Delta):
    """
    Get the rotation vector `theta` from the skew-symmetric matrix that is the
    matrix logarithm of the rotation matrix `Delta`:

        [theta]  = ln(Delta)
               x

    The rotation vector will not have a norm greater than pi.

    Parameters
    ----------
    Delta : (3, 3) np.ndarray
        Three-by-three matrix.

    Returns
    -------
    theta : (3,) np.ndarray
        Three-element vector of angles in radians.
    """

    # Get the trace of the matrix and limit its value.
    q = Delta[0, 0] + Delta[1, 1] + Delta[2, 2]
    q_min = 2*np.cos(3.1415926) + 1
    q = max(min(q, 3.0), q_min)

    # Get the scaling factor of the vector.
    ang = math.acos((q-1)/2)
    s = ang/math.sqrt(3 + 2*q - q**2) if (q <= 2.9996) \
            else (q**2 - 11*q + 54)/60

    # Build the vector.
    theta = s*np.array([
        Delta[2, 1] - Delta[1, 2],
        Delta[0, 2] - Delta[2, 0],
        Delta[1, 0] - Delta[0, 1]])

    # Check the output.
    if q == q_min:
        raise ValueError("The provided output is incorrectly all zeros \n"
                + "because the input is very close to a 180 degree rotation.")

    return theta


def wrap(Y):
    """
    Wrap angles to a -pi to pi range. This function is vectorized.
    """
    return Y - np.round(Y/math.tau)*math.tau


def ned_enu(vec):
    """
    Swap between North, East, Down (NED) orientation and East, North, Up (ENU)
    orientation. This operation changes the array in place.

    Parameters
    ----------
    vec : (3,) or (3, K) or (K, 3) np.ndarray
        Three-element vector or matrix of such vectors.

    Returns
    -------
    vec : (3,) or (3, K) or (K, 3) np.ndarray
        Three-element vector or matrix of such vectors.
    """

    # Check input.
    if isinstance(vec, (list, tuple)):
        vec = np.array(vec)
    trs = (vec.ndim == 2 and vec.shape[0] != 3)

    # Transpose input.
    if trs:
        vec = vec.T

    # Flip sign of z axis.
    vec[2] = -vec[2]

    # Swap the x and y axes.
    x = vec[0].copy()
    vec[0] = vec[1].copy()
    vec[1] = x

    # Transpose output.
    if trs:
        vec = vec.T

    return vec


def vanloan(F, B=None, Q=None, T=None):
    """
    Discretize the dynamics, stochastic matrices in the equation

        .                 .--
        x = F x + B u + `/ Q  w

    where `F` is the dynamics matrix, `B` is the input matrix, and `Q` is the
    noise covariance matrix.

    Parameters
    ----------
    F : 2D np.ndarray
        Continuous-domain dynamics matrix.
    B : 2D np.ndarray, default None
        Continuous-domain dynamics input matrix.  To omit this input, provide
        `None`.
    Q : 2D np.ndarray, default None
        Continuous-domain dynamics noise covariance matrix.  To omit this input,
        provide `None`.
    T : float, default 1.0
        Sampling period in seconds.

    Returns
    -------
    Phi : 2D np.ndarray
        Discrete-domain dynamics matrix.
    Bd : 2D np.ndarray
        Discrete-domain dynamics input matrix.
    Qd : 2D np.ndarray
        Discrete-domain dynamics noise covariance matrix.

    Notes
    -----
    The Van Loan method, named after Charles Van Loan, is one way of
    discretizing the matrices of a state-space system.  Suppose that you have
    the following state-space system:

        .                 .--
        x = F x + B u + `/ Q  w

        y = C x + D u + R v

    where `x` is the state vector, `u` is the input vector, and `w` is a white,
    Gaussian noise vector with means of zero and variances of one.  Then, to get
    the discrete form of this equation, we would need to find `Phi`, `Bd`, and
    `Qd` such that

                             .--
        x = Phi x + Bd u + `/ Qd w

        y = C x + D u + Rd v

    `Rd` is simply `R`.  `C` and `D` are unaffected by the discretization
    process.  We can find `Phi` and `Qd` by doing the following:

            .-      -.                    .-          -.
            | -F  Q  |                    |  M11  M12  |
        L = |        |    M = expm(L T) = |            |
            |  0  F' |                    |  M21  M22  |
            '-      -'                    '-          -'
        Phi = M22'        Qd = Phi M12 .

    Note that `F` must be square and `Q` must have the same size as `F`.  To
    find `Bd`, we do the following:

            .-      -.                    .-         -.
            |  F  B  |                    |  Phi  Bd  |
        G = |        |    H = expm(G T) = |           |
            |  0  0  |                    |   0   I   |
            '-      -'                    '-         -'

    Note that for `Bd` to be calculated, `B` must have the same number of rows
    as `F`, but need not have the same number of columns.  For `Qd` to be
    calculated, `F` and `Q` must have the same shape.  If these conditions are
    not met, the function will fault.

    We can also express Phi, Bd, and Qd in terms of their infinite series:

                         1   2  2    1   3  3
        Phi = I + F T + --- F  T  + --- F  T  + ...
                         2!          3!

                    1       2    1   2    3    1   3    4
        Bd = B T + --- F B T  + --- F  B T  + --- F  B T  + ...
                    2!           3!            4!
        
                     2                      3
                    T  .-          T -.    T  .- 2           T      T 2 -.
        Qd = Q T + --- | F Q +  Q F   | + --- | F Q + 2 F Q F  + Q F     | + ...
                    2! '-            -'    3! '-                        -'

                            2
                 .-        T  .-          T -.       -.
           = Phi |  Q T + --- |  F Q + Q F   | + ...  |
                 '-        2  '-            -'       -'

    The forward Euler method approximations to these are

        Phi = I + F T
        Bd  = B T
        Qd  = Q T

    The bilinear approximation to Phi is

                                         -1/2
        Phi = (I + 0.5 A T) (I - 0.5 A T)

    References
    ----------
    .. [1]  C. Van Loan, "Computing Integrals Involving the Matrix Exponential,"
            1976.
    .. [2]  Brown, R. and Phil Hwang. "Introduction to Random Signals and
            Applied Kalman Filtering (4th ed.)" (2012).
    .. [3]  https://en.wikipedia.org/wiki/Discretization
    """

    import scipy as sp

    # Get Phi.
    N = F.shape[1] # number of states
    Phi = sp.linalg.expm(F*T)

    # Get Bd.
    if B is not None:
        M = B.shape[1] # number of inputs
        G = np.vstack(( np.hstack((F, B)), np.zeros((M, N + M)) ))
        H = sp.linalg.expm(G*T)
        Bd = H[0:N, N:(N + M)]
    else:
        Bd = None

    # Get Qd.
    if Q is not None:
        L = np.vstack((
            np.hstack((-F, Q)),
            np.hstack(( np.zeros((N, N)), F.T)) ))
        H = sp.linalg.expm(L*T)
        Qd = Phi @ H[0:N, N:(2*N)]
    else:
        Qd = None

    return Phi, Bd, Qd

# ---------------
# Path Generation
# ---------------

def path_still(T, t_dur=3600.0, llh=None):
    """
    Generate a motionless path.

    Parameters
    ----------
    T : float
        Sampling period (s).
    t_dur : float, default 3600.0
        Duration of flight (s).
    llh : (3,) np.ndarray, default None
        Position vector in geodetic coordinates (rad, rad, m). If the input is
        `None`, a position of 0 degrees latitude, 0 degrees longitude, and 0 m
        above ellipsoid will be used.

    Returns
    -------
    t : (K,) np.ndarray
        Array of time values (s).
    llh_t : (3, K) np.ndarray
        Matrix of columns of position vectors (rad, rad, m).
    vne_t : (3, K) np.ndarray
        Matrix of columns of velocity vectors (m/s).
    rpy_t : (3, K) np.ndarray
        Matrix of columns of roll, pitch, and yaw attitude vectors (rad).
    """

    # Define time.
    K = round(t_dur/T) + 1
    t = np.arange(K)*T

    # Define position.
    if llh is None:
        llh = np.array([0.0, 0, 0])
    llh_t = llh[:, None] * np.ones((3, K))

    # Estimate velocity and attitude.
    vne_t = np.zeros((3, K))
    rpy_t = np.zeros((3, K))

    return t, llh_t, vne_t, rpy_t


def path_eight(T, t_dur=3600.0, R=1000.0, H=100.0):
    """
    Generate a fake flight path in the shape of a figure eight on its side. The
    flight starts by heading north and then west, along the right-most edge of
    the figure eight. The radius `R` is the half-width of the figure eight path.
    The height (in the north-south direction) of the path is half of the
    radius.

    Parameters
    ----------
    T : float
        Sampling period (s).
    t_dur : float, default 3600.0
        Duration of flight (s).
    R : float, default 1000.0
        Radius of figure eight path.
    H : float, default 100.0
        Change in height above ellipsoidal surface (m).

    Returns
    -------
    t : (K,) np.ndarray
        Array of time values (s).
    llh_t : (3, K) np.ndarray
        Matrix of columns of position vectors (rad, rad, m).
    vne_t : (3, K) np.ndarray
        Matrix of columns of velocity vectors (m/s).
    rpy_t : (3, K) np.ndarray
        Matrix of columns of roll, pitch, and yaw attitude vectors (rad).
    """

    # Define time.
    K = round(t_dur/T) + 1
    t = np.arange(K)*T

    # Define a figure eight.
    theta = np.linspace(0, 2*np.pi, K)
    lat = R/(4.0*A_E)*np.sin(2.0*theta)
    lon = R/A_E*(np.cos(theta) - 1.0)
    hae = H*(1.0 - np.cos(theta))/2.0
    llh_t = np.array((lat, lon, hae))

    # Estimate velocity and attitude.
    vne_t = llh_to_vne(llh_t, T)
    grav_t = somigliana(llh_t)
    rpy_t = vne_to_rpy(vne_t, grav_t[2, :], T)

    return t, llh_t, vne_t, rpy_t


class path_waypoints:
    """
    Path generation using Bezier curves from waypoints. This will create an
    interactive plot with control points and Bezier curves. When the plot is
    closed, the returned object will include the full path joining the Bezier
    curves. This path will be defined such that the given velocity and sampling
    period are observed.

    Attributes
    ----------
    p : (2, Np) or (Np, 2) np.ndarray
        Control points in local-level x and y coordinates.
    B : (2, K) or (K, 2) np.ndarray
        Local-level x and y coordinates of Bezier paths.
    """

    def __init__(self, points, velocity, R_min, T,
            ax=None, plot=True, res=0.01):
        """
        Initialize the path and plot.

        Parameters
        ----------
        points : (2, Np) or (Np, 2) np.ndarray
            Control points in local-level x and y coordinates (m).
        velocity : float
            Constant velocity during navigation path (m/s)
        R_min : float
            Minimum radius of curvature (m).
        T : float
            Sampling period (s).
        ax : matplotlib.axes._axes.Axes, default None
            MatPlotLib axes object. If none is provided, one will be generated.
        plot : bool, default True
            Flag to make an interactive plot, versus just calculate the Bezier
            curve.
        res : float, default 0.01
            Resolution of control points (m).
        """

        # Save the points.
        self.p = points
        self.tp = (points.shape[0] > 2)
        if self.tp:
            self.p = self.p.T

        # Save the remaining parameters.
        self.vel = velocity
        self.R_min = R_min
        self.T = T
        self.ax = ax
        self.res = res

        # Define array lengths.
        self.Np = self.p.shape[1]   # number of points
        self.Nb = self.Np - 2       # number of Bezier curves
        self.Nt = 100               # number of parametric values

        # Initialize the selected control point.
        self.sel = None

        # Define the parametric coefficients for Bezier curves.
        self.t = np.linspace(0, 1, self.Nt)
        self.t0 = (1 - self.t)**2
        self.t1 = 2*(1 - self.t)*self.t
        self.t2 = self.t**2

        # Initialize the midpoints.
        self.m = (self.p[:, :-1] + self.p[:, 1:])/2
        self.m[:, 0] = self.p[:, 0] # first midpoint
        self.m[:, -1] = self.p[:, -1] # last midpoint

        # Define the Bezier curves and radii of curvature.
        self.b = np.zeros((self.Nb, 2, self.Nt))
        self.r = np.zeros((self.Nb, self.Nt))
        for j in range(self.Nb):
            self.bezier(j)

        # If not plot should be made, just join the Bezier curves.
        if not plot:
            self.join()
            return

        # Generate a plot axis object if needed.
        if self.ax is None:
            _, self.ax = plt.subplots()

        # Plot and save the control lines.
        self.plot_cl, = self.ax.plot(self.p[1], self.p[0],
            color="#BBBBBB", linewidth=0.5)

        # Plot and save the control points.
        self.plot_cp, = self.ax.plot(self.p[1], self.p[0],
            'o', color="#BBBBBB", markerfacecolor='none')

        # Initialize the Bezier plot curves.
        self.plot_bc = [] # main Bezier curves
        self.plot_bf = [] # failure curves (less than min radius of curvature)
        for j in range(self.Nb):
            bc, = self.ax.plot([], [], 'b-')
            bf, = self.ax.plot([], [], 'r-')
            self.plot_bc.append(bc)
            self.plot_bf.append(bf)
            self.update_bezier_curve(j)

        # Link mouse events to methods.
        self.canvas = self.ax.figure.canvas
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        self.canvas.mpl_connect('close_event', self.on_close)

        # Set the view limits, aspect ratio, axis labels, and grid.
        self.ax.margins(x=0.50, y=0.50)
        self.ax.set_aspect('equal')
        self.ax.set_xlabel("Easting, $y_c$ (m)")
        self.ax.set_ylabel("Northing, $x_c$ (m)")
        self.ax.grid(True, color='#CCCCCC', linewidth=0.2)

        # Render.
        plt.show()

    def bezier(self, j):
        """ Calculate the jth Bezier curve and its radius of curvature. """

        # Define start, control, and end points for this segment.
        P0 = self.m[:, j]      # previous midpoint
        P1 = self.p[:, j + 1]  # control point
        P2 = self.m[:, j + 1]  # next midpoint

        # Define the Bezier curve segment.
        self.b[j, 0] = self.t0 * P0[0] + self.t1 * P1[0] + self.t2 * P2[0]
        self.b[j, 1] = self.t0 * P0[1] + self.t1 * P1[1] + self.t2 * P2[1]

        # Define the radius of curvature.
        Dx = 2*(1 - self.t)*(P1[0] - P0[0]) + 2*self.t*(P2[0] - P1[0])
        Dy = 2*(1 - self.t)*(P1[1] - P0[1]) + 2*self.t*(P2[1] - P1[1])
        Dx2 = 2*(P2[0] - 2*P1[0] + P0[0])
        Dy2 = 2*(P2[1] - 2*P1[1] + P0[1])
        Dxy = np.sqrt(Dx**2 + Dy**2)
        self.r[j] = np.abs(Dxy**3/(Dx*Dy2 - Dy*Dx2))

    def update_bezier_curve(self, j):
        """ Update the jth Bezier curve plot. """

        # Get the data.
        x = self.b[j, 0]
        y = self.b[j, 1]
        r = self.r[j]

        # Get the points of low radii of curvature.
        is_fail = (r < self.R_min)

        # Update the plot data.
        self.plot_bc[j].set_data(y, x)
        self.plot_bf[j].set_data(y[is_fail], x[is_fail])

    def join(self):
        """ Join the several Bezier curves together into one path. """

        # Concatenate the Bezier curves together.
        x = np.zeros(self.Nb*self.Nt)
        y = np.zeros(self.Nb*self.Nt)
        for j in range(self.Nb):
            na = j*self.Nt
            nb = (j+1)*self.Nt
            x[na:nb] = self.b[j, 0]
            y[na:nb] = self.b[j, 1]

        # Get distance traveled.
        dx = np.insert(np.diff(x), 0, 0.0)
        dy = np.insert(np.diff(y), 0, 0.0)
        dr = np.sqrt(dx**2 + dy**2)
        r = np.cumsum(dr)

        # Reinterpolate to get uniform spacing.
        t_tot = r[-1]/self.vel
        K = round(t_tot/self.T) + 1
        rr = np.linspace(0, r[-1], K)
        x = np.interp(rr, r, x)
        y = np.interp(rr, r, y)

        # Save to self.
        self.B = np.array((x, y))
        if self.tp:
            self.B = self.B.T

    def on_press(self, event):
        """ Identify the closest control point to the mouse click. """

        # Exit if mouse is outside canvas.
        if event.inaxes != self.ax:
            return

        # Find the point closest to the mouse.
        dx = event.ydata - self.p[0]
        dy = event.xdata - self.p[1]
        r = np.sqrt(dx**2 + dy**2)
        self.sel = np.argmin(r)

        # Move the point to the mouse.
        self.on_motion(event)

    def on_motion(self, event):
        """ Move the selected control point with the mouse and update the middle
        and adjacent Bezier curves. """

        # Exit if nothing is selected or mouse is outside canvas.
        i = self.sel
        if i is None or event.inaxes != self.ax:
            return

        # Move point to the mouse location.
        y_mouse = np.round(event.ydata/self.res) * self.res
        x_mouse = np.round(event.xdata/self.res) * self.res
        self.p[:, i] = [y_mouse, x_mouse]

        # Update the adjacent midpoints.
        if i == 0:
            self.m[:, 0] = self.p[:, 0]
        elif i == 1:
            self.m[:, 1] = (self.p[:, 1] + self.p[:, 2])/2
        elif i == self.Np - 2:
            self.m[:, -2] = (self.p[:, -3] + self.p[:, -2])/2
        elif i == self.Np - 1:
            self.m[:, -1] = self.p[:, -1]
        else:
            self.m[:, i - 1] = (self.p[:, i - 1] + self.p[:, i])/2
            self.m[:, i] = (self.p[:, i] + self.p[:, i + 1])/2

        # Update the sets of control points and lines.
        self.plot_cp.set_data(self.p[1], self.p[0])
        self.plot_cl.set_data(self.p[1], self.p[0])

        # Update the middle and adjacent Bezier curves.
        for j in [i - 2, i - 1, i]:
            if (j < 0) or (j >= self.Nb):
                continue
            self.bezier(j)
            self.update_bezier_curve(j)

        # Refresh the drawing.
        self.canvas.draw_idle()

    def on_release(self, event):
        """ Unselect the selected control point. """
        self.sel = None

    def on_close(self, event):
        """ Join the Bezier curves when closing the plot. """
        self.join()


def llh_to_vne(llh_t, T):
    """
    Convert geodetic position over time to velocity of the navigation frame
    relative to the earth frame over time. Geodetic position is quadratically
    extrapolated by one sample.

    Parameters
    ----------
    llh_t : (3, K) or (K, 3) np.ndarray
        Matrix of geodetic position vectors of latitude (radians), longitude
        (radians), and height above ellipsoid (meters).
    T : float
        Sampling period in seconds.

    Returns
    -------
    vne_t : (3, K) or (K, 3) np.ndarray
        Matrix of velocity vectors.
    """

    # Check input.
    if isinstance(llh_t, (list, tuple)):
        llh_t = np.array(llh_t)
    trs = (llh_t.ndim == 2 and llh_t.shape[0] != 3)

    # Transpose input.
    if trs:
        llh_t = llh_t.T

    # Parse geodetic position.
    lat = llh_t[0]
    lon = llh_t[1]
    hae = llh_t[2]

    # Extended derivatives
    lat_ext = 3*lat[-1] - 3*lat[-2] + lat[-3]
    lon_ext = 3*lon[-1] - 3*lon[-2] + lon[-3]
    hae_ext = 3*hae[-1] - 3*hae[-2] + hae[-3]
    Dlat = np.diff(np.append(lat, lat_ext))/T
    Dlon = np.diff(np.append(lon, lon_ext))/T
    Dhae = np.diff(np.append(hae, hae_ext))/T

    # Trig of latitude
    clat = np.cos(llh_t[0]) # (K,)
    slat = np.sin(llh_t[0]) # (K,)

    # Rotation rate of navigation frame relative to earth frame,
    # referenced in the navigation frame
    wnne_x = clat*Dlon
    wnne_y = -Dlat

    # Velocity of the navigation frame relative to the earth frame,
    # referenced in the navigation frame
    klat = np.sqrt(1 - E2*slat**2)
    Rt = A_E/klat
    Rm = (Rt/klat**2)*(1 - E2)
    vN = -wnne_y*(Rm + hae)
    vE =  wnne_x*(Rt + hae)
    vD = -Dhae
    vne_t = np.array((vN, vE, vD))

    # Transpose output.
    if trs:
        vne_t = vne_t.T

    return vne_t


def vne_to_rpy(vne_t, grav_t, T, alpha=0.06, wind=None):
    """
    Estimate the attitude angles in radians based on velocity.

    Parameters
    ----------
    vne_t : (3, K) or (K, 3) np.ndarray
        Matrix of vectors of velocity of the navigation frame relative to the
        ECEF frame (meters per second).
    grav_t : float or (K,) np.ndarray
        Local acceleration of gravity magnitude in meters per second
        squared. If grav_t is 2D, the vector norm will be used.
    T : float
        Sampling period in seconds.
    alpha : float, default 0.06
        Angle of attack in radians.
    wind : (2,) or (2, K) np.ndarray, default None
        Horizontal velocity vector of wind in meters per second.

    Returns
    -------
    rpy_t : (3, K) or (K, 3) np.ndarray
        Matrix of vectors of attitude angles roll, pitch, and yaw, all in
        radians. These angles are applied in the context of a North, East, Down
        navigation frame to produce the body frame in a zyx sequence of passive
        rotations.
    """

    # Check input.
    if isinstance(vne_t, (list, tuple)):
        vne_t = np.array(vne_t)
    if isinstance(grav_t, (list, tuple)):
        grav_t = np.array(grav_t)
    trs = (vne_t.ndim == 2 and vne_t.shape[0] != 3)
    if grav_t.ndim == 2:
        if grav_t.shape[0] == 3:
            grav_t = np.linalg.norm(grav_t, axis=0)
        else:
            grav_t = np.linalg.norm(grav_t, axis=1)

    # Transpose input.
    if trs:
        vne_t = vne_t.T

    # Filter the velocity.
    vN, vE, vD = vne_t

    # Get the horizontal velocity.
    vH = np.sqrt(vN**2 + vE**2)

    # Check if there is horizontal motion.
    isH = np.clip(1 - np.exp(-vH), 0.0, 1.0)

    # Estimate the yaw.
    if wind is None:
        yaw = np.arctan2(vE, vN)*isH
    else:
        yaw = np.arctan2(vE - wind[1], vN - wind[0])*isH

    # Estimate the pitch.
    pit = np.arctan(-(vD * isH)/(vH + (1 - isH))) + alpha * isH

    # Estimate the roll.
    aN = np.gradient(vN)/T # x-axis acceleration
    aE = np.gradient(vE)/T # y-axis acceleration
    ac = (vN*aE - vE*aN)/(vH + 1e-4) # cross product vH with axy
    rol = np.arctan(ac/grav_t) * isH

    # Assemble.
    rpy_t = np.vstack((rol, pit, yaw))

    # Transpose output.
    if trs:
        rpy_t = rpy_t.T

    return rpy_t


def est_wind(vne_t, yaw_t):
    """
    Estimate the time-varying wind by comparing the ground travel velocity to
    the yaw (heading) angle.

    Parameters
    ----------
    vne_t : (3,) or (3, K) or (K, 3) np.ndarray
        North, East, and Down velocity vector of the navigation frame relative
        to the ECEF frame (meters per second).
    yaw_t : (K,) np.ndarray
        Yaw angle clockwise from north in radians.

    Returns
    -------
    wind_t : (2,) or (2, K) or (K, 2) np.ndarray
        North and East components of wind vector in meters per second.
    """

    # Check input.
    if isinstance(vne_t, (list, tuple)):
        vne_t = np.array(vne_t)
    if isinstance(yaw_t, (list, tuple)):
        yaw_t = np.array(yaw_t)
    trs = (vne_t.ndim == 2 and vne_t.shape[0] != 3)

    # Transpose input.
    if trs:
        vne_t = vne_t.T

    # Get the horizontal speed.
    sH_t = math.sqrt(vne_t[0]**2 + vne_t[1]**2)

    # Get the estimated wind.
    wind_t = np.array([
        vne_t[0] - sH_t*math.cos(yaw_t),
        vne_t[1] - sH_t*math.sin(yaw_t)])

    # Transpose output.
    if trs:
        wind_t = wind_t.T

    return wind_t


def noise_fogm(T, tau, var, K):
    """
    Generate first-order, Gauss-Markov (FOGM) noise.

    Parameters
    ----------
    T : float
        Sampling period (s).
    tau : float
        Time constant (s).
    var : float
        Variance.
    K : int
        Number of noise samples.
    """

    # Define scaling factors.
    ka = math.exp(-T/tau)
    kb = math.sqrt(var*(1 - math.exp(-2*T/tau)))

    # Define the noise array.
    eta = kb*np.random.randn(K)

    # Initialize the state.
    x = np.sqrt(var)*eta[-1] # state

    # Process through time.
    y = np.zeros(K)
    for k in range(K):
        y[k] = x
        x = ka*x + eta[k]

    return y

# -------
# Gravity
# -------

def somigliana(llh):
    """
    Calculate the local acceleration of gravity vector in the navigation frame
    using the Somigliana equation. The navigation frame here has the North,
    East, Down (NED) orientation.

    Parameters
    ----------
    llh : (3,) or (3, K) or (K, 3) np.ndarray
        Geodetic position vector of latitude (radians), longitude (radians), and
        height above ellipsoid (meters) or matrix of such vectors.

    Returns
    -------
    gamma : (3,) or (3, K) or (K, 3) np.ndarray
        Acceleration of gravity in meters per second squared.
    """

    # Check input.
    if isinstance(llh, (list, tuple)):
        llh = np.array(llh)
    trs = (llh.ndim == 2 and llh.shape[0] != 3)

    # Transpose input.
    if trs:
        llh = llh.T

    # Get local acceleration of gravity for height equal to zero.
    slat2 = np.sin(llh[0])**2
    klat = np.sqrt(1 - E2*slat2)
    grav_z0 = GRAV_E*(1 + GRAV_K*slat2)/klat

    # Calculate gamma for the given height.
    grav_z = grav_z0*(1 + (3/A_E**2)*llh[2]**2
        - 2/A_E*(1 + GRAV_F + GRAV_M - 2*GRAV_F*slat2)*llh[2])

    # Form vector.
    if np.ndim(grav_z) > 0:
        K = len(grav_z)
        grav = np.zeros((3, K))
        grav[2, :] = grav_z
    else:
        grav = np.array([0.0, 0.0, grav_z])

    # Transpose output.
    if trs:
        grav = grav.T

    return grav

# -------------
# Mechanization
# -------------

def inv_mech(llh_t, rpy_t, T, grav_model=somigliana):
    """
    Compute the inverse mechanization of pose to get inertial measurement unit
    sensor values.

    Parameters
    ----------
    llh_t : (3, K) or (K, 3) np.ndarray
        Matrix of geodetic positions in terms of latitude (radians), longitude
        (radians), and height above ellipsoid (meters).
    rpy_t : (3, K) or (K, 3) np.ndarray
        Matrix of vectors of attitude angles roll, pitch, and yaw, all in
        radians. These angles are applied in the context of a North, East, Down
        navigation frame to produce the body frame in a zyx sequence of passive
        rotations.
    T : float
        Sampling period in seconds.
    grav_model : function, default somigliana
        The gravity model function to use. This function should be able to take
        a matrix of position vectors in terms of latitude (radians), longitude
        (radians), and height above ellipsoid (meters) and return a matrix of
        the same shape representing the local acceleration of gravity vectors
        (meters per second squared) in the navigation frame with a North, East,
        Down (NED) orientation.

    Returns
    -------
    fbbi_t : (3, K) or (K, 3) np.ndarray
        Matrix of specific force vectors (meters per second squared) of the body
        frame relative to the inertial frame, referenced in the body frame.
    wbbi_t : (3, K) or (K, 3) np.ndarray
        Matrix of rotation rate vectors (radians per second) of the body frame
        relative to the inertial frame, referenced in the body frame.

    Notes
    -----
    The function internally calculates the velocity vector from the position
    vector.

    This algorithm uses the forward Euler differential in order to be a perfect
    dual with the forward mechanization algorithm which uses the forward Euler
    integral. As a consequence, the estimated sensor values lead the pose
    (position, velocity, and attitude) values by a small amount of time because
    they are informed by future pose values. Specifically, the rotation rates
    will lead by half a sampling period and the specific forces will lead by a
    full sampling period.

    This function is not a perfect dual of the forward mechanization algorithm
    if a barometric altitude aiding model was used.
    """

    # Check input.
    if isinstance(llh_t, (list, tuple)):
        llh_t = np.array(llh_t)
    if isinstance(rpy_t, (list, tuple)):
        rpy_t = np.array(rpy_t)
    trs = (llh_t.ndim == 2 and llh_t.shape[0] != 3)

    # Transpose input.
    if trs:
        llh_t = llh_t.T
        rpy_t = rpy_t.T

    # Number of points in time
    K = llh_t.shape[1]

    # Trig of latitude
    clat = np.cos(llh_t[0]) # (K,)
    slat = np.sin(llh_t[0]) # (K,)

    # Unwrap the attitude angles so that
    # the extrapolation below works correctly.
    rpy_t = np.unwrap(rpy_t, axis=1)

    # Derivative of position
    llh_ext = 3*llh_t[:, -1] - 3*llh_t[:, -2] + llh_t[:, -3] # (3,)
    Dllh = np.diff(np.column_stack((llh_t, llh_ext)), axis=1)/T # (3, K)

    # Rotation rate of navigation frame relative to earth frame,
    # referenced in the navigation frame
    wnne = np.array([
        clat*Dllh[1],
        -Dllh[0],
        -slat*Dllh[1]]) # (3, K)

    # Velocity of the navigation frame relative to the earth frame,
    # referenced in the navigation frame
    klat = np.sqrt(1 - E2*slat**2) # (K,)
    Rt = A_E/klat # (K,)
    Rm = (Rt/klat**2)*(1 - E2) # (K,)
    vne = np.array([
        -wnne[1]*(Rm + llh_t[2]),
        wnne[0]*(Rt + llh_t[2]),
        -Dllh[2]]) # (3, K)

    # Derivative of velocity
    vne_ext = 3*vne[:, -1] - 3*vne[:, -2] + vne[:, -3] # (3,)
    Dvne = np.diff(np.column_stack((vne, vne_ext)), axis=1)/T # (3, K)

    # Rotation matrices
    Cbn = rpy_to_dcm(rpy_t) # (K, 3, 3)
    Cbn_ext = Cbn[K-1] @ Cbn[K-2].T @ Cbn[K-1] # (3, 3)
    Cbn = np.concatenate((Cbn, Cbn_ext[None, :, :]), axis=0) # (K+1, 3, 3)
    Cnb = np.transpose(Cbn, (0,2,1)) # (K+1, 3, 3)

    # Navigation to body rotation rate via inverse Rodrigues rotation
    D = Cbn[:-1] @ Cnb[1:] # (K, 3, 3)
    d11 = D[:, 0, 0];   d12 = D[:, 0, 1];   d13 = D[:, 0, 2] # (K,)
    d21 = D[:, 1, 0];   d22 = D[:, 1, 1];   d23 = D[:, 1, 2] # (K,)
    d31 = D[:, 2, 0];   d32 = D[:, 2, 1];   d33 = D[:, 2, 2] # (K,)
    q = d11 + d22 + d33 # trace of D (K,)
    q_min = 2*math.cos(3.1415926) + 1
    q = q*(q <= 3)*(q >= q_min) + 3.0*(q > 3) + q_min*(q < q_min) # (K,)
    ang = np.arccos((q-1)/2) # angle of rotation (K,)
    k = ang/np.sqrt(3 + 2*q - q**2 + (q > 2.9995))*(q <= 2.9995) \
        + (q**2 - 11*q + 54)/60*(q > 2.9995) # scaling factor (K,)
    # This is really wbbn, but it will be used to build wbbi.
    wbbi_t = k*np.array([d32 - d23, d13 - d31, d21 - d12])/T # (3, K)

    # Rotation rates
    wnei = np.array([
        W_EI*clat,
        np.zeros(K),
        -W_EI*slat]) # (3, K)
    w = wnne + wnei
    # Matrix product of Cbn with w. This is now truly wbbi.
    wbbi_t[0] += Cbn[:-1, 0, 0]*w[0] + Cbn[:-1, 0, 1]*w[1] + Cbn[:-1, 0, 2]*w[2]
    wbbi_t[1] += Cbn[:-1, 1, 0]*w[0] + Cbn[:-1, 1, 1]*w[1] + Cbn[:-1, 1, 2]*w[2]
    wbbi_t[2] += Cbn[:-1, 2, 0]*w[0] + Cbn[:-1, 2, 1]*w[1] + Cbn[:-1, 2, 2]*w[2]

    # Specific force
    w += wnei
    grav = grav_model(llh_t) # (3, K)
    fnbi = Dvne - grav # (3, K)
    # Cross product of w with vne
    fnbi[0] += w[1]*vne[2] - w[2]*vne[1]
    fnbi[1] += w[2]*vne[0] - w[0]*vne[2]
    fnbi[2] += w[0]*vne[1] - w[1]*vne[0]
    fbbi_t = np.zeros((3, K))
    # Matrix product of Cbn with fnbi
    fbbi_t[0, :] = Cbn[:-1, 0, 0]*fnbi[0] \
        + Cbn[:-1, 0, 1]*fnbi[1] \
        + Cbn[:-1, 0, 2]*fnbi[2]
    fbbi_t[1, :] = Cbn[:-1, 1, 0]*fnbi[0] \
        + Cbn[:-1, 1, 1]*fnbi[1] \
        + Cbn[:-1, 1, 2]*fnbi[2]
    fbbi_t[2, :] = Cbn[:-1, 2, 0]*fnbi[0] \
        + Cbn[:-1, 2, 1]*fnbi[1] \
        + Cbn[:-1, 2, 2]*fnbi[2]

    # Transpose output.
    if trs:
        fbbi_t = fbbi_t.T
        wbbi_t = wbbi_t.T

    return fbbi_t, wbbi_t


def mech(fbbi_t, wbbi_t, llh0, vne0, rpy0, T, hae_t=None,
        baro_name=None, grav_model=somigliana, show_progress=True):
    """
    Compute the forward mechanization of inertial measurement unit sensor values
    to get pose.

    Parameters
    ----------
    fbbi_t : (3, K) or (K, 3) np.ndarray
        Matrix of specific force vectors (meters per second squared) of the body
        frame relative to the inertial frame, referenced in the body frame.
    wbbi_t : (3, K) or (K, 3) np.ndarray
        Matrix of rotation rate vectors (radians per second) of the body frame
        relative to the inertial frame, referenced in the body frame.
    llh0 : (3,) np.ndarray
        Initial geodetic position of latitude (radians), longitude (radians),
        and height above ellipsoid (meters).
    vne0 : (3,) np.ndarray
        Initial velocity vector (meters per second) in North, East, and Down
        (NED) directions.
    rpy0 : (3,) np.ndarray
        Initial roll, pitch, and yaw angles in radians. These angles are applied
        in the context of a North, East, Down (NED) navigation frame to produce
        the body frame in a zyx sequence of passive rotations.
    T : float
        Sampling period in seconds.
    hae_t : (K,) np.ndarray, default None
        External source of altitude. If `baro_name` is `None`, `hae_t` directly
        overrides the height. If `baro_name` is any of the accepted strings,
        `hae_t` represents the barometric altimeter data.
    baro_name : str, default None
        The name of the barometric altitude aiding model. Current models are
        third-order with specific tuning coefficients: 'savage', 'rogers',
        'widnall', 'silva', 'iae', 'ise', 'itae', and 'itse'. If the
        `baro_name` is `None`, the height is directly overridden using `hae_t`.
    grav_model : function, default somigliana
        The gravity model function to use. This function should take a position
        vector of latitude (radians), longitude (radians), and height above
        ellipsoid (meters) and return the local acceleration of gravity vector
        (meters per second squared) in the navigation frame with a North, East,
        Down (NED) orientation.
    show_progress : bool, default True
        Flag to show the progress bar in the terminal.

    Returns
    -------
    llh_t : (3, K) or (K, 3) np.ndarray
        Matrix of geodetic positions in terms of latitude (radians), longitude
        (radians), and height above ellipsoid (meters).
    vne_t : (3, K) or (K, 3) np.ndarray
        Matrix of vectors of velocity of the navigation frame relative to the
        ECEF frame (meters per second).
    rpy_t : (3, K) or (K, 3) np.ndarray
        Matrix of vectors of attitude angles roll, pitch, and yaw, all in
        radians. These angles are applied in the context of a North, East, Down
        navigation frame to produce the body frame in a zyx sequence of passive
        rotations.
    """

    # Check the inputs.
    if isinstance(fbbi_t, (list, tuple)):
        fbbi_t = np.array(fbbi_t)
    if isinstance(wbbi_t, (list, tuple)):
        wbbi_t = np.array(wbbi_t)
    if isinstance(llh0, (list, tuple)):
        llh0 = np.array(llh0)
    if isinstance(vne0, (list, tuple)):
        vne0 = np.array(vne0)
    if isinstance(rpy0, (list, tuple)):
        rpy0 = np.array(rpy0)
    trs = (fbbi_t.ndim == 2 and fbbi_t.shape[0] != 3)

    # Initialize states.
    llh = llh0.copy()
    vne = vne0.copy()
    Cnb = rpy_to_dcm(rpy0).T

    # Transpose input.
    if trs:
        fbbi_t = fbbi_t.T
        wbbi_t = wbbi_t.T

    # Precalculate vertical velocity override or init baro model.
    override = False
    baro = None
    if hae_t is not None:
        if baro_name is None:
            override = True
            vD_t = np.zeros(len(hae_t))
            vD_t[:-1] = -np.diff(hae_t)/T
            # Second-order extrapolation
            vD_t[-1] = 2*vD_t[-2] - vD_t[-3]
        else:
            baro = Baro(baro_name)

    # Storage
    K = fbbi_t.shape[1]
    llh_t = np.zeros((3, K))
    vne_t = np.zeros((3, K))
    rpy_t = np.zeros((3, K))

    # Time loop
    for k in range(K):
        # Inputs
        fbbi = fbbi_t[:, k]
        wbbi = wbbi_t[:, k]

        # Override height and velocity.
        if override:
            llh[2] = hae_t[k]
            vne[2] = vD_t[k]

        # Results storage
        llh_t[:, k] = llh
        vne_t[:, k] = vne
        rpy_t[:, k] = dcm_to_rpy(Cnb.T)

        # Get the derivatives.
        if baro is None:
            Dllh, Dvne, wbbn = mech_step(fbbi, wbbi,
                llh, vne, Cnb, grav_model=grav_model)
        else:
            Dllh, Dvne, wbbn = mech_step(fbbi, wbbi,
                llh, vne, Cnb, hae_t[k], baro, grav_model=grav_model)

        # Integrate.
        llh += Dllh * T
        vne += Dvne * T
        Cnb[:, :] = Cnb @ rodrigues_rotation(wbbn * T)
        orthonormalize_dcm(Cnb)
        if baro is not None:
            baro.er_int += baro.er*T

        # Progress bar
        if show_progress:
            progress(k, K)

    # Transpose output.
    if trs:
        llh_t = llh_t.T
        vne_t = vne_t.T
        rpy_t = rpy_t.T

    return llh_t, vne_t, rpy_t


def mech_step(fbbi, wbbi, llh, vne, Cnb,
        hb=None, baro=None, grav_model=somigliana):
    """
    Get the derivatives of position, velocity, and attitude for one time step.

    Parameters
    ----------
    fbbi : (3,) np.ndarray
        Vector of specific forces (meters per second squared) of the body frame
        relative to the inertial frame, referenced in the body frame.
    wbbi : (3,) np.ndarray
        Vector of rotation rates (radians per second) of the body frame relative
        to the inertial frame, referenced in the body frame.
    llh : (3,) np.ndarray
        Vector of geodetic position in terms of latitude (radians), longitude
        (radians), and height above ellipsoid (meters).
    vne : (3,) np.ndarray
        Vector of velocity of the navigation frame relative to the ECEF frame
        (meters per second).
    Cnb : (3, 3) np.ndarray
        Passive rotation matrix from the body frame to the NED navigation frame.
    hb : float, default None
        Barometric altitude (m).
    baro : Baro object, default None
        The barometric altitude aiding object.
    grav_model : function, default somigliana
        The gravity model function to use. This function should take a position
        vector of latitude (radians), longitude (radians), and height above
        ellipsoid (meters) and return the local acceleration of gravity vector
        (meters per second squared) in the navigation frame with a North, East,
        Down (NED) orientation.

    Returns
    -------
    Dllh : (3,) np.ndarray
        Derivative of the vector of the geodetic position.
    Dvne : (3,) np.ndarray
        Derivative of the vector of the navigation frame velocity.
    wbbn : (3,) np.ndarray
        Derivative of the vector of the rotation rate of the body frame relative
        to the navigation frame.
    """

    # Trig of latitude
    clat = math.cos(llh[0])
    slat = math.sin(llh[0])
    tlat = math.tan(llh[0])

    # Rotation rate of earth relative to inertial
    wneix = W_EI*clat
    wneiz = -W_EI*slat

    # Rotation rate of navigation relative to earth
    klat = math.sqrt(1 - E2*slat**2)
    Rt = A_E/klat
    Rm = (Rt/klat**2)*(1 - E2)
    wnnex = vne[1]/(Rt + llh[2])
    wnney = -vne[0]/(Rm + llh[2])
    wnnez = -vne[1]*tlat/(Rt + llh[2])

    # Rotation rate of body relative to navigation
    wx = wnnex + wneix
    wy = wnney
    wz = wnnez + wneiz
    Dllh = np.array([wx, wy, wz]) # temp use
    wbbn = wbbi - Cnb.T @ Dllh

    # Position derivatives
    Dllh[0] = -wnney
    Dllh[1] = wnnex/clat
    Dllh[2] = -vne[2]

    # Velocity derivatives
    wx += wneix
    wz += wneiz
    Dvne = Cnb @ fbbi + grav_model(llh)
    Dvne[0] -= wy * vne[2] - wz * vne[1]
    Dvne[1] -= wz * vne[0] - wx * vne[2]
    Dvne[2] -= wx * vne[1] - wy * vne[0]

    # Baro model (all third-order)
    if baro is not None:
        baro.er = llh[2] - hb
        Dllh[2] += -baro.K[0]*baro.er
        Dvne[2] += baro.K[1]*baro.er + baro.K[2]*baro.er_int

    return Dllh, Dvne, wbbn


def jacobian(fbbi, llh, vne, Cnb, baro=None):
    """
    Calculate the continuous-domain Jacobian matrix of the propagation function.
    The attitude change is handled via a tilt error vector. Note that this
    matrix must be discretized along with the dynamics noise covariance matrix.
    This can be done with the Van Loan method:

        Phi, _, Qd = inu.vanloan(F, None, Q)

    where `F` is the Jacobian returned by this function and `Q` is the dynamics
    noise covariance matrix. The `Phi` and `Qd` matrices are then the matrices
    you would use in your Bayesian estimation filter.

    Parameters
    ----------
    fbbi : (3,) np.ndarray
        Vector of specific forces (meters per second squared) of the body frame
        relative to the inertial frame, referenced in the body frame.
    llh : (3,) np.ndarray
        Vector of geodetic position in terms of latitude (radians), longitude
        (radians), and height above ellipsoid (meters).
    vne : (3,) np.ndarray
        Vector of velocity of the navigation frame relative to the ECEF frame
        (meters per second).
    Cnb : (3, 3) np.ndarray
        Passive rotation matrix from the body frame to the NED navigation frame.
    baro : Baro object, default None
        The barometric altitude aiding object.

    Returns
    -------
    F : (9, 9) np.ndarray
        Jacobian matrix.

    Notes
    -----
    The order of states are

        latitude, longitude, height above ellipsoid,
        North velocity, East velocity, down velocity,
        x tilt error, y tilt error, z tilt error

    The tilt error vector, psi, is applied to a true body to NED navigation
    frame rotation matrix, Cnb, to produce a tilted rotation matrix:

        ~              T
        Cnb = exp([psi] ) Cnb
                       x
    """

    # Parse the forces, positions, and velocities.
    fN, fE, fD = Cnb @ fbbi
    lat, _, hae = llh
    vN, vE, vD = vne

    # Trig of latitude
    clat = math.cos(lat)
    slat = math.sin(lat)
    clat2 = clat**2
    slat2 = slat**2
    tlat = math.tan(lat)

    # Rotation rate of earth relative to inertial
    wx = W_EI*clat
    wz = -W_EI*slat

    # Distance from Earth
    klat = math.sqrt(1 - E2*slat2)
    Rt = A_E/klat
    Rm = (Rt/klat**2)*(1 - E2)
    lt = Rt + hae
    lm = Rm + hae

    # Get the partial derivatives with respect to latitude and height.
    y0 = GRAV_E*(1.0 + GRAV_K*slat2)/klat
    nu = 2.0/A_E*(1.0 + GRAV_F + GRAV_M - 2*GRAV_F*slat2)
    eta = 1 + (3/A_E**2)*hae**2 - nu*hae
    Dyl = ((2*GRAV_K*GRAV_E + E2*y0/klat)*eta/klat
        + 8*GRAV_F*y0*hae/A_E)*slat*clat
    Dyh = -y0*nu + y0*6*hae / A_E**2

    # Define the Jacobian matrix.
    F = np.zeros((9, 9))

    # dp_dp
    F[0, 2] = -vN/lm**2
    F[1, 0] = vE*tlat/(lt*clat)
    F[1, 2] = -vE/(lt**2*clat)

    # dp_dv
    F[0, 3] = 1/lm
    F[1, 4] = 1/(lt*clat)
    F[2, 5] = -1

    # dv_dp
    F[3, 0] = -2*vE*wx - vE**2/(lt*clat2)
    F[3, 2] = vE**2*tlat/lt**2 - vN*vD/lm**2
    F[4, 0] = 2*vN*wx + 2*vD*wz + vN*vE/(lt*clat2)
    F[4, 2] = -vE*(vN*tlat + vD)/lt**2
    F[5, 0] = -2*vE*wz + Dyl
    F[5, 2] = (vN/lm)**2 + (vE/lt)**2 + Dyh

    # dv_dv
    F[3, 3] = vD/lm
    F[3, 4] = 2*wz - 2*vE*tlat/lt
    F[3, 5] = vN/lm
    F[4, 3] = -2*wz + vE*tlat/lt
    F[4, 4] = (vN*tlat + vD)/lt
    F[4, 5] = 2*wx + vE/lt
    F[5, 3] = -2*vN/lm
    F[5, 4] = -2*wx - 2*vE/lt

    # dv_dq
    F[3, 7] = -fD
    F[3, 8] = fE
    F[4, 6] = fD
    F[4, 8] = -fN
    F[5, 6] = -fE
    F[5, 7] = fN

    # dq_dp
    F[6, 0] = wz
    F[6, 2] = -vE/lt**2
    F[7, 2] = vN/lm**2
    F[8, 0] = -wx - vE/(lt*clat2)
    F[8, 2] = vE*tlat/lt**2

    # dq_dv
    F[6, 4] = 1/lt
    F[7, 3] = -1/lm
    F[8, 4] = -tlat/lt
    
    # dq_dq
    F[6, 7] = wz - vE*tlat/lt
    F[6, 8] = vN/lm
    F[7, 6] = -wz + vE*tlat/lt
    F[7, 8] = wx + vE/lt
    F[8, 6] = -vN/lm
    F[8, 7] = -wx - vE/lt

    # Baro model (all third-order)
    if baro is not None:
        F[2, 2] += -baro.K[0]
        F[5, 2] += baro.K[1]

    return F
