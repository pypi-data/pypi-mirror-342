# -*- coding: utf-8 -*-
"""
exact multipole decomposition post-processing tools for torchgdm
"""
# %%
import warnings

import torch

from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX
from torchgdm.tools.misc import get_default_device


# --- double factorial via recursion (used as fixed value below)
def _doublefactorial(n):
    if n <= 0:
        return 1
    else:
        return n * _doublefactorial(n - 2)


# --- first 4 spherical Bessel functions in pytorch
def sph_j0(x: torch.Tensor, asymptotic_threshold=0.001):
    """spherical Bessel function of zero order

    for numerical stability, use asymptotic solutions at small arguments.

    Args:
        x (torch.Tensor): argument of Bessel function
        asymptotic_threshold (float, optional): threshold below which to use small argument asymptotic approximation. Defaults to 0.001.

    Returns:
        float: bessel result
    """
    x = torch.as_tensor(x, dtype=DTYPE_COMPLEX)
    j0 = torch.where(torch.abs(x) > asymptotic_threshold, torch.sin(x) / x, 1)
    return j0


def sph_j1(x: torch.Tensor, asymptotic_threshold=0.01):
    """spherical Bessel function of first order

    for numerical stability, use asymptotic solutions at small arguments.

    Args:
        x (torch.Tensor): argument of Bessel function
        asymptotic_threshold (float, optional): threshold below which to use small argument asymptotic approximation. Defaults to 0.01.

    Returns:
        float: bessel result
    """
    x = torch.as_tensor(x, dtype=DTYPE_COMPLEX)
    _sin_term = torch.sin(x) / x**2
    _cos_term = torch.cos(x) / x
    j1 = torch.where(torch.abs(x) > asymptotic_threshold, _sin_term - _cos_term, x / 3)
    return j1


def sph_j2(x: torch.Tensor, asymptotic_threshold=0.1):
    """spherical Bessel function of second order

    for numerical stability, use asymptotic solutions at small arguments.

    Args:
        x (torch.Tensor): argument of Bessel function
        asymptotic_threshold (float, optional): threshold below which to use small argument asymptotic approximation. Defaults to 0.1.

    Returns:
        float: bessel result
    """
    x = torch.as_tensor(x, dtype=DTYPE_COMPLEX)
    _sin_term = (3 / x**2 - 1) * (torch.sin(x) / x)
    _cos_term = 3 * torch.cos(x) / x**2
    j2 = torch.where(
        torch.abs(x) > asymptotic_threshold, _sin_term - _cos_term, x**2 / 15
    )
    return j2


def sph_j3(x: torch.Tensor, asymptotic_threshold=0.5):
    """spherical Bessel function of third order

    for numerical stability, use asymptotic solutions at small arguments.

    Args:
        x (torch.Tensor): argument of Bessel function
        asymptotic_threshold (float, optional): threshold below which to use small argument asymptotic approximation. Defaults to 0.5.

    Returns:
        float: bessel result
    """
    x = torch.as_tensor(x, dtype=DTYPE_COMPLEX)
    _sin_term = (15 / x**3 - 6 / x) * (torch.sin(x) / x)
    _cos_term = (15 / x**2 - 1) * (torch.cos(x) / x)
    j3 = torch.where(
        torch.abs(x) > asymptotic_threshold, _sin_term - _cos_term, x**3 / 105
    )
    return j3


# Bessel functions of first kind
def Jn(n: int, z: torch.Tensor):
    """integer order Bessel functions of first kind via recurrence formula

    Notes:
        - For pure real arguments, use recurrence: J_n+1 = (2n/z) J_n - J_n-1
        - for purely imaginary arguments, use identity via modif. Bessel of first kind
          Jn(1j*z) = exp(n*1j*np.pi/2) * In(z) = (j^n) * In(z)
        - the recurrence relation numerically breaks down for large n and small z due to numerical errors.

    Args:
        n (int): integer order
        z (torch.Tensor): complex argument

    Raises:
        Exception: mixed real, imag argument

    Returns:
        torch.Tensor: result
    """
    z = torch.as_tensor(z, dtype=DTYPE_COMPLEX)

    # pure real arg: use recurrence
    if torch.count_nonzero(z.imag) == 0:
        if n < 0:
            return ((-1) ** n) * Jn(-n, z.real)
        elif n == 0:
            return torch.special.bessel_j0(z.real)
        elif n == 1:
            return torch.special.bessel_j1(z.real)
        else:
            J_nm1 = Jn(n - 1, z.real)
            J_nm2 = Jn(n - 2, z.real)
            return (2 * (n - 1) / z.real) * J_nm1 - J_nm2

    # pure imaginary arg: use modified Bessel functions
    elif torch.count_nonzero(z.real) == 0:
        return (1j**n) * In(n, z.imag)

    # mixed complex args not supported
    else:
        raise Exception(
            "Implementation of Bessel functions supports "
            + "only purely real or purely imaginary argument."
        )


# Bessel functions of second kind
def Yn(n: int, z: torch.Tensor):
    """integer order Bessel functions of second kind via recurrence formula

    Notes:
        - For pure real arguments, use recurrence: Y_n+1 = (2n/z) Y_n - Y_n-1
        - for purely imaginary arguments, use identity via modif. Bessel of first kind
          Yn(1j*z) = exp((n+1)*1j*np.pi/2) * In(z) - 2/np.pi * exp(-1*n*1j*np.pi/2) * Kn(z)
        - the recurrence relation numerically breaks down for large n and small z due to numerical errors.

    Args:
        n (int): integer order
        z (torch.Tensor): complex argument

    Raises:
        Exception: mixed real, imag argument

    Returns:
        torch.Tensor: result
    """
    z = torch.as_tensor(z, dtype=DTYPE_COMPLEX)

    # pure real arg: use recurrence
    if torch.count_nonzero(z.imag) == 0:
        if n < 0:
            return ((-1) ** n) * Yn(-n, z.real)
        elif n == 0:
            return torch.special.bessel_y0(z.real)
        elif n == 1:
            return torch.special.bessel_y1(z.real)
        else:
            Y_nm1 = Yn(n - 1, z.real)
            Y_nm2 = Yn(n - 2, z.real)
            return (2 * (n - 1) / z.real) * Y_nm1 - Y_nm2

    # pure imaginary arg: use modified Bessel functions
    elif torch.count_nonzero(z.real) == 0:
        fact_exp2 = torch.exp(torch.as_tensor((n + 1) * 1j * torch.pi / 2))
        _Yn_t1 = fact_exp2 * In(n, z.imag)

        fact_exp3 = torch.exp(torch.as_tensor(-1 * n * 1j * torch.pi / 2))
        _Yn_t2 = -2 / torch.pi * fact_exp3 * Kn(n, z.imag)

        ynz = _Yn_t1 + _Yn_t2
        return ynz

    # mixed complex args not supported
    else:
        raise Exception(
            "Implementation of Bessel functions supports "
            + "only purely real or purely imaginary argument."
        )


# modified Bessel functions of first kind
def In(n: int, z: torch.Tensor):
    """integer order modified Bessel functions of first kind via recurrence formula

    Notes:
        - use recurrence: I_n+1 = -(2n/z) I_n + I_n-1
        - supports only purely real or purely imaginary arguments
        - the recurrence relation numerically breaks down for large n and small z due to numerical errors.

    Args:
        n (int): integer order
        z (torch.Tensor): complex argument

    Returns:
        torch.Tensor: result
    """
    if n < 0:
        return In(-n, z)
    elif n == 0:
        return torch.special.modified_bessel_i0(z)
    elif n == 1:
        return torch.special.modified_bessel_i1(z)
    else:
        I_nm1 = In(n - 1, z)
        I_nm2 = In(n - 2, z)
        return (-2 * (n - 1) / z) * I_nm1 + I_nm2


# modified Bessel functions of second kind
def Kn(n: int, z: torch.Tensor):
    """integer order modified Bessel functions of second kind via recurrence formula

    Notes:
        - use recurrence: K_n+1 = (2n/z) K_n + K_n-1
        - supports only purely real or purely imaginary arguments
        - the recurrence relation numerically breaks down for large n and small z due to numerical errors.

    Args:
        n (int): integer order
        z (torch.Tensor): complex argument

    Returns:
        torch.Tensor: result
    """
    if n < 0:
        return Kn(-n, z)
    elif n == 0:
        return torch.special.modified_bessel_k0(z)
    elif n == 1:
        return torch.special.modified_bessel_k1(z)
    else:
        K_nm1 = Kn(n - 1, z)
        K_nm2 = Kn(n - 2, z)
        return ((2 * (n - 1)) / z) * K_nm1 + K_nm2


def H1n(n: int, z: torch.Tensor):
    """integer order Hankel functions of first kind

    Notes:
        - use: H1_n = J_n + 1j * Y_n
        - supports only purely real or purely imaginary arguments
        - the recurrence relations used in the Bessel functions numerically break down for large n and small z due to numerical errors.

    Args:
        n (int): integer order
        z (torch.Tensor): complex argument

    Returns:
        torch.Tensor: result
    """
    z = torch.as_tensor(z, dtype=DTYPE_COMPLEX)

    return Jn(n, z) + 1j * Yn(n, z)


def H2n(n: int, z: torch.Tensor):
    """integer order Hankel functions of second kind

    Notes:
        - use: H2_n = J_n - 1j * Y_n
        - supports only purely real or purely imaginary arguments
        - the recurrence relations used in the Bessel functions numerically break down for large n and small z due to numerical errors.

    Args:
        n (int): integer order
        z (torch.Tensor): complex argument

    Returns:
        torch.Tensor: result
    """
    z = torch.as_tensor(z, dtype=DTYPE_COMPLEX)

    return Jn(n, z) - 1j * Yn(n, z)


if __name__ == "__main__":
    from scipy.special import jv, yv, iv, kv, hankel1, hankel2
    import matplotlib.pyplot as plt

    n = -2
    z = torch.linspace(0.1, 1, 500, dtype=torch.float32)

    # compare with scipy
    # bessel
    j_scipy = jv(n, z.numpy())
    j_torch = Jn(n, z)
    y_scipy = yv(n, z.numpy())
    y_torch = Yn(n, z)

    # modified bessel
    i_scipy = iv(n, z.numpy())
    i_torch = In(n, z)
    k_scipy = kv(n, z.numpy())
    k_torch = Kn(n, z)

    # hankel
    h1_scipy = hankel1(n, z.numpy())
    h1_torch = H1n(n, z)
    h2_scipy = hankel2(n, z.numpy())
    h2_torch = H2n(n, z)

    # - plot
    plt.figure(figsize=(10, 4))
    plt.subplot(231)
    plt.plot(z.numpy(), j_scipy, label="scipy")
    plt.plot(z.numpy(), j_torch.numpy(), dashes=[2, 2], label="J - torch")
    plt.legend()

    plt.subplot(232)
    plt.plot(z.numpy(), y_scipy, label="scipy")
    plt.plot(z.numpy(), y_torch.numpy(), dashes=[2, 2], label="Y - torch")
    plt.legend()

    plt.subplot(234)
    plt.plot(z.numpy(), i_scipy, label="scipy")
    plt.plot(z.numpy(), i_torch.numpy(), dashes=[2, 2], label="I - torch")
    plt.legend()

    plt.subplot(235)
    plt.plot(z.numpy(), k_scipy, label="scipy")
    plt.plot(z.numpy(), k_torch.numpy(), dashes=[2, 2], label="K - torch")
    plt.legend()

    plt.subplot(233)
    plt.plot(z.numpy(), h1_scipy, label="scipy")
    plt.plot(z.numpy(), h1_torch.numpy(), dashes=[2, 2], label="H1 - torch")
    plt.legend()

    plt.subplot(236)
    plt.plot(z.numpy(), h2_scipy, label="scipy")
    plt.plot(z.numpy(), h2_torch.numpy(), dashes=[2, 2], label="H2 - torch")

    plt.legend()

    plt.show()
