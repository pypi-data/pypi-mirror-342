# Inertial Navigation Utilities

## Key Design Concepts

### Functions

This library provides forward mechanization of inertial measurement unit sensor
values (accelerometer and gyroscope readings) to get position, velocity, and
attitude as well as inverse mechanization to get sensor values from position,
velocity, and attitude. It also includes tools to calculate velocity from
geodetic position over time, to estimate attitude from velocity, and to estimate
wind velocity from ground-track velocity and yaw angle.

### Accuracy

The mechanization algorithms in this library make no simplifying assumptions.
The Earth is defined as an ellipsoid. Any deviations of the truth from this
simple shape can be captured by more complex gravity models. The algorithms use
a single frequency update structure which is much simpler than the common
two-frequency update structure and just as, if not more, accurate.

### Duality

The forward and inverse mechanization functions are perfect duals of each other.
This means that if you started with a profile of position, velocity, and
attitude and passed these into the inverse mechanization algorithm to get sensor
values and then passed those sensor values into the forward mechanization
algorithm, you would get back the original position, velocity, and attitude
profiles. The only error would be due to finite-precision rounding.

### Vectorization

When possible, the functions are vectorized in order to handle processing
batches of values. A set of scalars is a 1D array. A set of vectors is a 2D
array, with each vector in a column. So, a (3, 7) array is a set of seven
vectors, each with 3 elements. If an input matrix does not have 3 rows, it will
be assumed that the rows of the matrix are vectors.

An example of the vectorization in this library is the `inv_mech` (inverse
mechanization) algorithm. There is no `for` loop to iterate through time; rather
the entire algorithm has been vectorized. This results in an over 100x speed
increase.

### Extended Kalman Filter

An extended Kalman filter can be implemented using this library. The `mech_step`
function applies the mechanization equations to a single time step. It returns
the time derivatives of the states. The `jacobian` function calculates the
continuous-domain Jacobian of the dynamics function. While this does mean that
the user must then manually integrate the derivatives and discretize the
Jacobian, this gives the user greater flexibility to decide how to discretize
them.

The example code below is meant to run within a `for` loop stepping through
time, where `k` is the time index:

```python
# Inputs
fbbi = fbbi_t[:, k] # specific forces (m/s^2)
wbbi = wbbi_t[:, k] # rotation rates (rad/s)
z = z_t[:, k] # GPS position (rad, rad, m)

# Update
S = H @ Ph @ H.T + R # innovation covariance (3, 3)
Si = np.linalg.inv(S) # inverse (3, 3)
Kg = Ph @ H.T @ Si # Kalman gain (9, 3)
Ph -= Kg @ H @ Ph # update to state covariance (9, 9)
r = z - llh # innovation (3,)
dx = Kg @ r # changes to states (9,)
llh += dx[:3] # add change in position
vne += dx[3:6] # add change in velocity
# matrix exponential of skew-symmetric matrix
Psi = inu.rodrigues_rotation(dx[6:])
Cnb = Psi.T @ Cnb

# Save results.
tllh_t[:, k] = llh
tvne_t[:, k] = vne
trpy_t[:, k] = inu.dcm_to_rpy(Cnb.T)

# Get the Jacobian and propagate the state covariance.
F = inu.jacobian(fbbi, llh, vne, Cnb)
Phi = I + (F*T)@(I + (F*T/2)) # 2nd-order expm(F T)
Ph = Phi @ Ph @ Phi.T + Qd

# Get the state derivatives.
Dllh, Dvne, wbbn = inu.mech_step(fbbi, wbbi, llh, vne, Cnb)

# Integrate (forward Euler).
llh += Dllh * T # change applies linearly
vne += Dvne * T # change applies linearly
Cnb[:, :] = Cnb @ inu.rodrigues_rotation(wbbn * T)
inu.orthonormalize_dcm(Cnb)

# Update progress bar.
inu.progress(k, K, tic)
```

In the example above, `H` should be a (3, 9) matrix with ones along the
diagonal. The `Qd` should be the (9, 9) discretized dynamics noise covariance
matrix. The `R` should be the (3, 3) measurement noise covariance matrix. Note
that forward Euler integration has been performed on the state derivatives and a
second-order approximation to the matrix exponential has been implemented to
discretize the continuous-time Jacobian.

## Functions

### Mechanization: `mech` and `mech_step`

```python
llh_t, vne_t, rpy_t = inu.mech(fbbi_t, wbbi_t,
        llh0, vne0, rpy0, T, hae_t=None,
        grav_model=somigliana, show_progress=True)
Dllh, Dvne, wbbn = inu.mech_step(fbbi, wbbi,
        llh, vne, Cnb, grav_model=somigliana)
```

The `mech` function performs forward mechanization of accelerometer and
gyroscope sensor values, given the initial conditions for position, velocity,
and attitude. This function processes an entire time-history profile of sensor
values and returns the path solution for the corresponding span of time. If you
would prefer to mechanize only one step at a time, you can call the `mech_step`
function instead. Actually, the `mech` function does call the `mech_step`
function within a `for` loop.

### Inverse Mechanization: `inv_mech`

```python
fbbi_t, wbbi_t = inu.inv_mech(llh_t, rpy_t, T, grav_model=somigliana)
```

The `inv_mech` function performs inverse mechanization, meaning it takes path
information in the form of position, velocity, and attitude over time and
estimates the corresponding sensor values for an accelerometer and gyroscope.
This function is fully vectorized, so there is no `for` loop internally. Note
that the velocity should be the exact forward Euler derivative of position:

![](https://gitlab.com/davidwoodburn/inu/-/raw/main/figures/fig_forward_euler.svg)

where *v* is the velocity, *p* is the position, and *T* is the sampling period.
Of course, to get North, East, down velocity from latitude, longitude, and
height above ellipsoid requires some coordinate conversion. If you do not
already have velocity values which are exactly equal to the forward Euler
derivative of position, use can use the `llh_to_vne` function.

In addition to generating velocity from position, you can also generate likely
attitude values from velocity assuming coordinated turns. The `vne_to_rpy`
function serves this purpose.

### Jacobian: `jacobian`

```python
F = inu.jacobian(fbbi, llh, vne, Cnb)
```

The Jacobian of the dynamics is calculated using the `jacobian` function. This
is a square matrix whose elements are the derivatives with respect to state of
the continuous-domain, time-derivatives of states. For example, the time
derivative of latitude is

![](https://gitlab.com/davidwoodburn/inu/-/raw/main/figures/fig_lat_rate.svg)

So, the derivative of this with respect to height above ellipsoid is

![](https://gitlab.com/davidwoodburn/inu/-/raw/main/figures/fig_partial.svg)

The order of the states is position (latitude, longitude, height), velocity
(North, East, down), and attitude. So, the above partial derivative would be
found in element (1,3) (base-1 indexing) of the Jacobian matrix.

The representation of attitude is complicated. This library uses 3x3 direction
cosine matrices (DCMs) to process attitude. The rate of change in attitude is
represented by a tilt error vector. So, the last three states in the Jacobian
are the *x*, *y*, and *z* tilt errors. This makes a grand total of 9 states, so
the Jacobian is a 9x9 matrix.

The above code example (and the `ekf.py` script in the `examples` folder) shows
how to use the Jacobian.

### Discretization: `vanloan`

```python
Phi, Bd, Qd = inu.vanloan(F, B=None, Q=None, T=None)
```

The extended Kalman filter (EKF) example above shows a reduced-order
approximation to the matrix exponential of the Jacobian. The ***Q*** dynamics
noise covariance matrix also needs to be discretized. This was done with a
first-order approximation by just multiplying it by the sampling period *T*.
This is reasonably accurate and computationally fast. However, it is an
approximation. The mathematically accurate way to discretize the Jacobian and
***Q*** is to use the van Loan method. This is implemented with the `vanloan`
function.

### Orientation: `ned_enu`

```python
vec = inu.ned_enu(vec)
```

This library assumes all local-level coordinates are in the North, East, down
orientation. If your coordinates are in the East, North, up orientation or you
wish for the final results to be converted to that orientation, use the
`ned_enu` function.

### Estimate Horizontal Winds: `est_wind`

```python
wind_t = inu.est_wind(vne_t, yaw_t)
```

If you have heading information as well as velocity information, then you can
calculate the velocity vector due to wind using the `est_wind` function.
