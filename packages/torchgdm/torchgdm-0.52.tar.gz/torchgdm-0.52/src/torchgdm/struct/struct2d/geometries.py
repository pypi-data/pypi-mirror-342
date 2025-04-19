# -*- coding: utf-8 -*-
"""surface discretization for infinitely long 2D geometries

geometry-definitions and discretizer
"""
import warnings

import torch

from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX
from torchgdm.tools.misc import get_default_device


# ==============================================================================
# geometry definitions
# ==============================================================================
def rectangle(l: int, h: int):
    """rectangle with dimensions `l` along x, `h` along z

    Args:
        l (int): length (units of step)
        h (int): height (units of step)

    Returns:
        func: discretization condition
        tuple of int: discretizer walk limits
    """
    from torchgdm.struct.struct3d.geometries import cuboid

    condition_3d, lim_3d = cuboid(l=l, w=1, h=h)

    def condition(xi, zi):
        return condition_3d(xi, 0, zi)

    mesh_limits = (lim_3d[0], lim_3d[1], lim_3d[4], lim_3d[5])

    return condition, mesh_limits


def square(l: int):
    """square with side length `l` (units of step)"""
    return rectangle(l, l)


def circle(r: float):
    """circle with radius `r` (units of step)"""
    from torchgdm.struct.struct3d.geometries import disc

    condition_3d, lim_3d = disc(r=r, h=1)

    def condition(xi, zi):
        return condition_3d(xi, zi, 0)

    mesh_limits = (lim_3d[0], lim_3d[1], lim_3d[2], lim_3d[3])

    return condition, mesh_limits


def split_ring(r_out: float, r_in: float, alpha_g: int = 0):
    """split ring

    Args:
        r_out (float): outer radius (units of step)
        r_in (float): inner radius (units of step)
        alpha_g (int, optional): split gap angle (rad). Defaults to 0.

    Returns:
        func: discretization condition
        tuple of int: discretizer walk limits
    """

    def condition(xi, zi):
        C1 = r_out**2 >= (xi**2 + zi**2) >= r_in**2
        if zi > 0 and alpha_g != 0:
            C2 = not (
                torch.arctan2(torch.as_tensor(abs(xi)), torch.as_tensor(abs(zi)))
                <= alpha_g / 2.0
            )
        else:
            C2 = True

        return C1 and C2

    mesh_limits = (
        -int(r_out) - 2,
        int(r_out) + 2,
        -int(r_out) - 2,
        int(r_out) + 2,
    )

    return condition, mesh_limits


def triangle_equilateral(d: int, truncate_edge: float = 0.0):
    """Generate uniform right triangular prism

    Args:
        d (int): side length (units of step)
        truncate_edge (float, optional): truncation ratio for the top triangle edge. Defaults to 0.0.

    Returns:
        func: condition(x,z): whether to put or not a mesh-cell at coordinate
        tuple: discretizer walk limits necessary to contain full structure
    """
    from torchgdm.struct.struct3d.geometries import prism_trigonal

    condition_3d, lim_3d = prism_trigonal(d=d, h=1, truncate_edge=truncate_edge)

    def condition(xi, zi):
        return condition_3d(xi, zi, 0)

    mesh_limits = (lim_3d[0], lim_3d[1], lim_3d[2], lim_3d[3])

    return condition, mesh_limits


# ==============================================================================
# discretizer
# ==============================================================================
def discretizer_square(
    condition_func, limits: tuple, z_offset: float = 0.5, step: float = 1.0
):
    """discretize surface of a 2D structure on a square grid

    Args:
        condition_func (_type_): functional, returning the condition as function of coordinate indices. 'condition_func(xi,zi)', returns a bool. (True: put a meshpoint, False: no meshpoint)
        limits (tuple): discretizer walk range. tuple of 6  ints (x0, x1, z0, z1)
        z_offset (float, optional): additional z-offset, to avoid placing dipoles at z=0 (units of step). Defaults to 0.5.
        step (float, optional): nominal stepsize in nm. Defaults to 1.0.

    Returns:
        torch.Tensor: 3d coordinates ([x, 0, z]) of discretization, where y=0. shape (N, 3) for `N` meshpoints.
    """

    sp = []
    for xi in range(int(limits[0]), int(limits[1])):
        for zi in range(int(limits[2]), int(limits[3])):
            if condition_func(xi, zi):
                sp.append([xi, 0, zi + z_offset])

    return torch.as_tensor(sp, dtype=DTYPE_FLOAT) * step


# %%
if __name__ == "__main__":

    l = 10
    w = 7
    h = 3
    step = 10.0
    cond, lim = split_ring(10, 7, torch.pi / 4)
    geometry_pos = discretizer_square(cond, lim, step=step)

    import matplotlib.pyplot as plt

    plt.subplot(aspect="equal")
    plt.scatter(geometry_pos[:, 0], geometry_pos[:, 2])
    plt.show()
    print(len(geometry_pos))
