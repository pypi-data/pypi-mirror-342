# Run `pytest` in the terminal.

import time
import numpy as np
import scipy as sp
import inu
import itrm


def fake_path(T, axis=1):
    # Define time.
    K = round(360.0/T) + 1
    t = np.arange(K)*T

    # Define a figure eight.
    R = 0.000156784 # radians
    theta = np.linspace(0, 2*np.pi, K)
    lat = (R/4)*np.sin(2*theta)
    lon = R*(np.cos(theta) - 1)
    hae = 50.0*(1 - np.cos(theta))
    llh_t = np.vstack((lat, lon, hae))

    # Transpose.
    if axis == 0:
        llh_t = llh_t.T

    return t, llh_t


def test_somigliana():
    # lists
    llh_t = [[np.pi/4, 0, 0],
        [np.pi/5, 0.01, 100.0]]
    gam_t = inu.somigliana(llh_t)
    assert np.allclose(np.linalg.norm(gam_t, axis=1),
        np.array([9.80619777, 9.79788193]))
    # horizontal time variance
    gam_t = inu.somigliana(np.array(llh_t).T)
    assert np.allclose(np.linalg.norm(gam_t, axis=0),
        np.array([9.80619777, 9.79788193]))


def test_rpy_dcm():
    # multiple single duals
    N = 5
    RPY = np.zeros((3, N))
    RPY[0, :] = np.random.uniform(-np.pi, np.pi, N)
    RPY[1, :] = np.random.uniform(-np.pi/2 + 1e-15, np.pi/2 - 1e-15, N)
    RPY[2, :] = np.random.uniform(-np.pi, np.pi, N)
    for n in range(N):
        C = inu.rpy_to_dcm(RPY[:, n])
        rpy = inu.dcm_to_rpy(C)
        assert np.allclose(rpy, RPY[:, n])


def test_orthonormalize_dcm():
    # Run many random tests.
    K = 1000
    N = 10
    nn = np.zeros(K)
    for k in range(K):
        C = np.random.randn(3, 3)
        for n in range(N):
            inu.orthonormalize_dcm(C)
            Z = np.abs(C @ C.T - np.eye(3))
            if np.max(Z) < 1e-15:
                break
        nn[k] = n + 1
    n_max = np.max(nn)
    assert (n_max <= 2)


def test_rodrigues_rotation():
    N = 1000
    for n in range(N):
        # Build a proper rotation vector.
        theta = np.random.randn(3)
        nm = np.linalg.norm(theta)
        if nm > np.pi:
            theta = -theta*(2*np.pi - nm)/nm

        # Convert to a rotation matrix.
        Delta = inu.rodrigues_rotation(theta)

        # Convert back to a rotation vector.
        Theta = inu.inverse_rodrigues_rotation(Delta)
        assert np.allclose(theta, Theta)


def test_mech():
    # --------------
    # Test Jacobian.
    # --------------

    fbbi = np.array([1e-6, 1e-6, 1e-6])
    llh = np.array([0, 0, 0])
    vne = np.array([100, 0, 0])
    Cnb = np.array([
         [0.9999, -0.00989934, 0.01009883],
         [0.00999933, 0.999901, -0.00989934],
         [-0.00999983, 0.00999933, 0.9999]])
    J = inu.jacobian(fbbi, llh, vne, Cnb)

    # ------------------------------------
    # Test with time varying along axis 1.
    # ------------------------------------

    # Build path.
    T = 0.01
    t, llh = fake_path(T)
    vne = inu.llh_to_vne(llh, T)
    gam = inu.somigliana(llh)
    rpy = inu.vne_to_rpy(vne, gam[2, :], T)

    # Inverse and forward mechanize.
    tic = time.perf_counter()
    hfbbi, hwbbi = inu.inv_mech(llh, rpy, T)

    Cnb = inu.rpy_to_dcm(rpy[:, 0]).T
    # M = np.hstack((hfbbi.T, hwbbi.T))
    # M.tofile("dat_fbbi_wbbi_10ms.bin")
    print(time.perf_counter() - tic)
    tllh, tvne, trpy = inu.mech(hfbbi, hwbbi,
        llh[:, 0], vne[:, 0], rpy[:, 0], T, show_progress=False)

    assert np.allclose(llh, tllh)
    assert np.allclose(vne, tvne)
    assert np.allclose(rpy, trpy)

    # ------------------------------------
    # Test with time varying along axis 0.
    # ------------------------------------

    # Build path.
    T = 0.01
    t, llh = fake_path(T, axis=0)
    vne = inu.llh_to_vne(llh, T)
    gam = inu.somigliana(llh)
    rpy = inu.vne_to_rpy(vne, gam[:, 2], T)

    # Inverse and forward mechanize.
    tic = time.perf_counter()
    hfbbi, hwbbi = inu.inv_mech(llh, rpy, T)
    print(time.perf_counter() - tic)
    tllh, tvne, trpy = inu.mech(hfbbi, hwbbi,
        llh[0, :], vne[0, :], rpy[0, :], T, show_progress=False)

    #import itrm
    #itrm.iplot(t, (llh - tllh).T)
    #itrm.iplot(t, (vne - tvne).T)
    #itrm.iplot(t, (rpy - trpy).T)

    assert np.allclose(llh, tllh)
    assert np.allclose(vne, tvne)
    assert np.allclose(rpy, trpy)

test_mech()
