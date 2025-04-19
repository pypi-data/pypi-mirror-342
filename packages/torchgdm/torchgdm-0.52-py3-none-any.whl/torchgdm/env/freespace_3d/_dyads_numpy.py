# -*- coding: utf-8 -*-
"""
numba implementations as well as vectorized numpy versions of 
free space Green's dyads for dipole and quadrupole sources
@authors: C. Majorel, P. R Wiecha
"""
#%%
import time
import math
import cmath

import numpy as np


def test_positional_input(R1: np.array, R2: np.array):
    if R1.shape != R2.shape:
        raise ValueError("R1 and R2 need same shape")
    if len(R1.shape) == 1:
        if R1.shape[0] != 3:
            raise ValueError(
                "single point needs to be cartesian coordinate with 3 values."
            )
        # expand dim
        R1 = R1[None, :]
        R2 = R2[None, :]
    elif len(R1.shape) == 2:
        if R1.shape[1] != 3:
            raise ValueError("points need to be cartesian coordinates with 3 values.")
    elif len(R1.shape) > 2:
        raise ValueError(
            "single point or list of points required, but got higher dimensional input data."
        )

    return R1, R2


## --- free space propagator dipole - numpy-vec
def G0_Ep_vec(
    R1: np.array,
    R2: np.array,
    wavelength: float,
    eps_env: float,
    dp_radius: float = 1e-20,
):
    R1, R2 = test_positional_input(R1, R2)

    R = R2 - R1
    I = np.identity(3)[None, :]  # , dtype='c16')

    lR2 = np.sum(R**2, axis=-1)
    lR = np.sqrt(lR2)
    lR[
        lR < dp_radius
    ] = 1.0  # add 1 to diag to avoid div by zero (treat self-terms separately later)

    k0 = 2 * math.pi / wavelength
    k = k0 * np.sqrt(eps_env)

    RR = np.einsum("...i,...j", R, R)

    R2diag = I * lR2[..., None, None]
    T1 = np.divide((RR - R2diag), np.power(lR, 3)[..., None, None])
    T2 = np.divide((3 * RR - R2diag), np.power(lR, 4)[..., None, None])
    T3 = np.divide((3 * RR - R2diag), np.power(lR, 5)[..., None, None])

    # phase term
    sG0 = np.exp(1j * k * lR) / eps_env

    G0 = (-np.power(k, 2) * T1 - 1j * k * T2 + T3) * sG0[..., None, None]

    return G0


def G0_Hp_vec(
    R1: np.array,
    R2: np.array,
    wavelength: float,
    eps_env: float,
    dp_radius: float = 1e-20,
):
    R1, R2 = test_positional_input(R1, R2)

    R = R2 - R1
    lR2 = np.sum(R**2, axis=-1)
    lR = np.sqrt(lR2)
    lR[
        lR < dp_radius
    ] = 1.0  # add 1 to diag to avoid div by zero (treat self-terms separately later)

    k0 = 2 * np.pi / wavelength
    k02n = np.sqrt(eps_env) * k0**2

    Dz = R[..., 2]
    Dy = R[..., 1]
    Dx = R[..., 0]

    T2XY = Dz / lR2
    T3XY = Dz / (lR**3)
    T2XZ = -Dy / lR2
    T3XZ = -Dy / (lR**3)
    T2YZ = Dx / lR2
    T3YZ = Dx / (lR**3)

    # Initialize and fill tensor
    G0 = np.zeros((*R.shape[:-1], 3, 3), dtype=np.complex_)
    G0[..., 0, 1] = 1j * k0 * T3XY + k02n * T2XY
    G0[..., 0, 2] = 1j * k0 * T3XZ + k02n * T2XZ
    G0[..., 1, 2] = 1j * k0 * T3YZ + k02n * T2YZ
    G0[..., 1, 0] = -G0[..., 0, 1]
    G0[..., 2, 0] = -G0[..., 0, 2]
    G0[..., 2, 1] = -G0[..., 1, 2]

    # phase term
    cG0 = -1 * np.exp(1j * k0 * np.sqrt(eps_env) * lR)
    G0 *= cG0[..., None, None]

    return G0


def G0_Hm_vec(R1, R2, wavelength, eps_env, dp_radius: float = 1e-20):
    return G0_Ep_vec(R1, R2, wavelength, eps_env, dp_radius)


def G0_Em_vec(R1, R2, wavelength, eps_env, dp_radius: float = 1e-20):
    return -1 * G0_Hp_vec(R1, R2, wavelength, eps_env, dp_radius)


## --- free space propagator dipole
def G0_Ep(R1, R2, wavelength, eps):
    """
    R1: dipole position
    R2: evaluation position
    """
    Dx = R2[0] - R1[0]
    Dy = R2[1] - R1[1]
    Dz = R2[2] - R1[2]
    lR = math.sqrt(Dx**2 + Dy**2 + Dz**2)

    k = 2 * np.pi / wavelength
    cn = cmath.sqrt(eps)
    ck0 = 1j * k * cn
    k2 = k * k * eps

    r25 = math.pow((Dx * Dx + Dy * Dy + Dz * Dz), 2.5)
    r2 = math.pow((Dx * Dx + Dy * Dy + Dz * Dz), 2.0)
    r15 = math.pow((Dx * Dx + Dy * Dy + Dz * Dz), 1.5)

    #!C-------------------------------------------------------------------
    T1XX = -1 * (Dy * Dy + Dz * Dz) / r15
    T2XX = (2 * Dx * Dx - Dy * Dy - Dz * Dz) / r2
    T3XX = (2 * Dx * Dx - Dy * Dy - Dz * Dz) / r25
    #!C-------------------------------------------------------------------
    T1XY = Dx * Dy / r15
    T2XY = 3 * Dx * Dy / r2
    T3XY = 3 * Dx * Dy / r25
    #!C-------------------------------------------------------------------
    T1XZ = Dx * Dz / r15
    T2XZ = 3 * Dx * Dz / r2
    T3XZ = 3 * Dx * Dz / r25
    #!C-------------------------------------------------------------------
    T1YY = -(Dx * Dx + Dz * Dz) / r15
    T2YY = (2 * Dy * Dy - Dx * Dx - Dz * Dz) / r2
    T3YY = (2 * Dy * Dy - Dx * Dx - Dz * Dz) / r25
    #!C-------------------------------------------------------------------
    T1YZ = Dy * Dz / r15
    T2YZ = 3 * Dy * Dz / r2
    T3YZ = 3 * Dy * Dz / r25
    #!C------------------------------------------------------------------
    T1ZZ = -(Dx * Dx + Dy * Dy) / r15
    T2ZZ = (2 * Dz * Dz - Dx * Dx - Dy * Dy) / r2
    T3ZZ = (2 * Dz * Dz - Dx * Dx - Dy * Dy) / r25

    CFEXP = cmath.exp(1j * k * cn * lR)

    ## setting up the tensor
    xx = CFEXP * (T3XX - ck0 * T2XX - k2 * T1XX) / eps
    yy = CFEXP * (T3YY - ck0 * T2YY - k2 * T1YY) / eps
    zz = CFEXP * (T3ZZ - ck0 * T2ZZ - k2 * T1ZZ) / eps

    xy = CFEXP * (T3XY - ck0 * T2XY - k2 * T1XY) / eps
    xz = CFEXP * (T3XZ - ck0 * T2XZ - k2 * T1XZ) / eps

    yz = CFEXP * (T3YZ - ck0 * T2YZ - k2 * T1YZ) / eps

    yx = xy
    zx = xz
    zy = yz

    G = np.array([[xx, xy, xz], [yx, yy, yz], [zx, zy, zz]], dtype=np.complex64)

    return G


def G0_Hp(R1, R2, wavelength, eps):
    """
    R1: dipole position
    R2: evaluation position
    """
    # eps: environment index
    Dx = R2[0] - R1[0]
    Dy = R2[1] - R1[1]
    Dz = R2[2] - R1[2]
    lR2 = Dx**2 + Dy**2 + Dz**2

    k0 = 2 * np.pi / wavelength
    k02n = cmath.sqrt(eps) * k0**2
    # -----------------------------------------------------------------
    T2XY = Dz / lR2
    T3XY = Dz / lR2**1.5
    # -----------------------------------------------------------------
    T2XZ = -Dy / lR2
    T3XZ = -Dy / lR2**1.5
    # -----------------------------------------------------------------
    T2YZ = Dx / lR2
    T3YZ = Dx / lR2**1.5
    # -----------------------------------------------------------------
    CFEXP = -1 * cmath.exp(1j * k0 * cmath.sqrt(eps) * math.sqrt(lR2))

    xx = 0
    yy = 0
    zz = 0

    xy = CFEXP * (1j * k0 * T3XY + k02n * T2XY)
    xz = CFEXP * (1j * k0 * T3XZ + k02n * T2XZ)
    yz = CFEXP * (1j * k0 * T3YZ + k02n * T2YZ)

    yx = -xy
    zx = -xz
    zy = -yz

    G = np.array([[xx, xy, xz], [yx, yy, yz], [zx, zy, zz]], dtype=np.complex64)

    return G


def G0_Hm(R1, R2, wavelength, eps):
    return G0_Ep(R1, R2, wavelength, eps)


def G0_Em(R1, R2, wavelength, eps):
    return -1 * np.array(G0_Hp(R1, R2, wavelength, eps))


# =============================================================================
# Quadrupole propagator
# =============================================================================


## --- free space propagator electric quadrupole
def G0_Eqe(R1, R2, wavelength, eps):
    """
    R1: dipole position
    R2: evaluation position
    """
    Dx = R2[0] - R1[0]
    Dy = R2[1] - R1[1]
    Dz = R2[2] - R1[2]
    lR = math.sqrt(Dx**2 + Dy**2 + Dz**2)

    k = 2 * np.pi / wavelength
    cn = cmath.sqrt(eps)
    ck0 = 1j * k * cn
    k2 = k * k * eps

    r3 = math.pow((Dx * Dx + Dy * Dy + Dz * Dz), 3)
    r25 = math.pow((Dx * Dx + Dy * Dy + Dz * Dz), 2.5)
    r2 = math.pow((Dx * Dx + Dy * Dy + Dz * Dz), 2.0)
    r15 = math.pow((Dx * Dx + Dy * Dy + Dz * Dz), 1.5)

    #!C-------------------------------------------------------------------
    T1XX = -1 * (Dy * Dy + Dz * Dz) / r15
    T2XX = (3 * Dx * Dx - 3 * Dy * Dy - 3 * Dz * Dz) / r2
    T3XX = (9 * Dx * Dx - 6 * Dy * Dy - 6 * Dz * Dz) / r25
    T4XX = (9 * Dx * Dx - 6 * Dy * Dy - 6 * Dz * Dz) / r3
    #!C-------------------------------------------------------------------
    T1XY = Dx * Dy / r15
    T2XY = 6 * Dx * Dy / r2
    T3XY = 15 * Dx * Dy / r25
    T4XY = 15 * Dx * Dy / r3
    #!C-------------------------------------------------------------------
    T1XZ = Dx * Dz / r15
    T2XZ = 6 * Dx * Dz / r2
    T3XZ = 15 * Dx * Dz / r25
    T4XZ = 15 * Dx * Dz / r3
    #!C-------------------------------------------------------------------
    T1YY = -(Dx * Dx + Dz * Dz) / r15
    T2YY = (3 * Dy * Dy - 3 * Dx * Dx - 3 * Dz * Dz) / r2
    T3YY = (9 * Dy * Dy - 6 * Dx * Dx - 6 * Dz * Dz) / r25
    T4YY = (9 * Dy * Dy - 6 * Dx * Dx - 6 * Dz * Dz) / r3
    #!C-------------------------------------------------------------------
    T1YZ = Dy * Dz / r15
    T2YZ = 6 * Dy * Dz / r2
    T3YZ = 15 * Dy * Dz / r25
    T4YZ = 15 * Dy * Dz / r3
    #!C------------------------------------------------------------------
    T1ZZ = -(Dx * Dx + Dy * Dy) / r15
    T2ZZ = (3 * Dz * Dz - 3 * Dx * Dx - 3 * Dy * Dy) / r2
    T3ZZ = (9 * Dz * Dz - 6 * Dx * Dx - 6 * Dy * Dy) / r25
    T4ZZ = (9 * Dz * Dz - 6 * Dx * Dx - 6 * Dy * Dy) / r3

    CFEXP = cmath.exp(1j * k * cn * lR)

    ## setting up the tensor
    xx = CFEXP * (T4XX - ck0 * T3XX - k2 * T2XX + ck0 * k2 * T1XX) / (6 * eps)
    yy = CFEXP * (T4YY - ck0 * T3YY - k2 * T2YY + ck0 * k2 * T1YY) / (6 * eps)
    zz = CFEXP * (T4ZZ - ck0 * T3ZZ - k2 * T2ZZ + ck0 * k2 * T1ZZ) / (6 * eps)

    xy = CFEXP * (T4XY - ck0 * T3XY - k2 * T2XY + ck0 * k2 * T1XY) / (6 * eps)
    xz = CFEXP * (T4XZ - ck0 * T3XZ - k2 * T2XZ + ck0 * k2 * T1XZ) / (6 * eps)

    yz = CFEXP * (T4YZ - ck0 * T3YZ - k2 * T2YZ + ck0 * k2 * T1YZ) / (6 * eps)

    yx = xy
    zx = xz
    zy = yz

    G = np.array([[xx, xy, xz], [yx, yy, yz], [zx, zy, zz]], dtype=np.complex64)

    return G


def G0_Hqe(R1, R2, wavelength, eps):
    """
    R1: dipole position
    R2: evaluation position
    """
    # eps: environment index
    Dx = R2[0] - R1[0]
    Dy = R2[1] - R1[1]
    Dz = R2[2] - R1[2]
    lR2 = Dx**2 + Dy**2 + Dz**2

    k0 = 2 * np.pi / wavelength
    k02n = cmath.sqrt(eps) * k0**2
    k2 = eps * k0**2
    # -----------------------------------------------------------------
    T2XY = -Dz / lR2
    T3XY = -Dz / lR2**1.5
    T4XY = -Dz / lR2**2
    # -----------------------------------------------------------------
    T2XZ = Dy / lR2
    T3XZ = Dy / lR2**1.5
    T4XZ = Dy / lR2**2
    # -----------------------------------------------------------------
    T2YZ = -Dx / lR2
    T3YZ = -Dx / lR2**1.5
    T4YZ = -Dx / lR2**2
    # -----------------------------------------------------------------
    CFEXP = cmath.exp(1j * k0 * cmath.sqrt(eps) * math.sqrt(lR2))

    xx = 0
    yy = 0
    zz = 0

    xy = CFEXP * (-1j * k0 * k2 * T2XY + 3 * k02n * T3XY + 3j * k0 * T4XY) / 6
    xz = CFEXP * (-1j * k0 * k2 * T2XZ + 3 * k02n * T3XZ + 3j * k0 * T4XZ) / 6
    yz = CFEXP * (-1j * k0 * k2 * T2YZ + 3 * k02n * T3YZ + 3j * k0 * T4YZ) / 6

    yx = -xy
    zx = -xz
    zy = -yz

    G = np.array([[xx, xy, xz], [yx, yy, yz], [zx, zy, zz]], dtype=np.complex64)

    return G


def G0_Hqm(R1, R2, wavelength, eps):
    return G0_Eqe(R1, R2, wavelength, eps)


def G0_Eqm(R1, R2, wavelength, eps):
    return -1 * G0_Hqe(R1, R2, wavelength, eps)


# %%

if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    import copy

    from pyGDM2 import tools

    func_vec = G0_Ep_vec
    func_seq = G0_Ep

    # func_vec = G0_Hp_vec
    # func_seq = G0_Hp

    # test:
    r1 = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    r2 = np.array([[50, 0, 20], [100, 30, 10], [500, 0, 0]])

    g0 = func_vec(r1, r2, wavelength=500, eps_env=1)
    print(g0.shape)

    ##%%

    eps_env = 1
    wl = 500

    DX, NX = 300, 201
    Z0 = 50
    r_probe = tools.generate_NF_map_XY(-DX, DX, NX, -DX, DX, NX, Z0)
    r0 = np.zeros_like(r_probe)

    t0 = time.time()
    G0_vec1 = func_vec(r0, r_probe, wl, eps_env)
    t1 = time.time()
    print(t1 - t0)

    G0_vec2 = np.zeros([len(r_probe), 3, 3], dtype=np.complex64)
    for i, _r in enumerate(r_probe):
        G0_vec2[i] = func_seq(r0[i], _r, wl, eps_env)
    t2 = time.time()
    print(t2 - t1, (t2 - t1) / (t1 - t0))

    G0_vec1 = G0_vec1.reshape(NX, NX, 3, 3)
    G0_vec2 = G0_vec2.reshape(NX, NX, 3, 3)

    print(np.abs(G0_vec1).mean())
    print((np.abs(G0_vec1) - np.abs(G0_vec2)).mean())

    i1, i2 = 2, 1
    plt.subplot(221)
    plt.title("vectorized")
    plt.imshow(G0_vec1[..., i1, i2].real)
    plt.colorbar()
    plt.subplot(222)
    plt.title("scalar")
    plt.imshow(G0_vec2[..., i1, i2].real)
    plt.colorbar()
    plt.subplot(223)
    plt.imshow(G0_vec1[..., i1, i2].imag)
    plt.colorbar()
    plt.subplot(224)
    plt.imshow(G0_vec2[..., i1, i2].imag)
    plt.colorbar()

    plt.show()
