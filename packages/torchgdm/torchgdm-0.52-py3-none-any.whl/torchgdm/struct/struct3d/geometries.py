# -*- coding: utf-8 -*-
"""volume discretization: geometry-definitions and discretizer"""
import warnings

import torch

from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX
from torchgdm.tools.misc import get_default_device


# ==============================================================================
# geometry definitions
# ==============================================================================
def cuboid(l: int, w: int, h: int):
    """cuboid with dimensions `l` along x, `w` along y, `h` along z

    Args:
        l (int): length (units of step)
        w (int): width (units of step)
        h (int): height (units of step)

    Returns:
        func: condition(x,y,z): whether to put or not a mesh-cell at coordinate
        tuple: discretizer walk limits necessary to contain full structure
    """

    def condition(xi, yi, zi):
        in_cuboid = (
            -l / 2.0 < xi <= l / 2.0
            and -w / 2.0 < yi <= w / 2.0
            and 0 <= zi < h - (1 / 2) ** 0.5
        )
        return in_cuboid

    mesh_limits = (-int(l), int(l) + 1, -int(w), int(w) + 1, -1, 2 * int(h) + 1)

    return condition, mesh_limits


def cube(l: int):
    """cube with side length `l`

    Args:
        l (int): side length (units of step)

    Returns:
        func: condition(x,y,z): whether to put or not a mesh-cell at coordinate
        tuple: discretizer walk limits necessary to contain full structure
    """
    return cuboid(l, l, l)


def spheroid(r_x: float, r_y: float, r_z: float):
    """spheroid with radii r_x, r_y, r_z along X, Y, Z axis

    - if r_z > r_y = r_x --> prolate spheroid
    - if r_z < r_y = r_x --> oblate spheroid
    - if r_z = r_y = r_x --> sphere

    contributed by C. Majorel.

    Args:
        r_x (float): X semi-axes length (units of step)
        r_y (float): Y semi-axes length (units of step)
        r_z (float): Z semi-axes length (units of step)

    Returns:
        func: condition(x,y,z): whether to put or not a mesh-cell at coordinate
        tuple: discretizer walk limits necessary to contain full structure
    """

    def condition(xi, yi, zi):
        return (
            ((xi / (r_x + 0.2)) ** 2)
            + ((yi / (r_y + 0.2)) ** 2)
            + (zi / (r_z + 0.2)) ** 2
        ) <= 1

    mesh_limits = (
        -2 * int(r_x),
        2 * int(r_x) + 1,
        -2 * int(r_y),
        2 * int(r_y) + 1,
        -2 * int(r_z),
        2 * int(r_z) + 1,
    )

    return condition, mesh_limits


def sphere(r: float):
    """sphere of radius `r` (units of step)"""
    return spheroid(r, r, r)


def ellipse(r1: float, r2: float, h: int):
    """elliptical cylinder with radii `r1`, `r2` (x, y) and height `h` (z)

    Args:
        r1 (float): semi-axis length along `x` (units of step)
        r2 (float): semi-axis length along `y` (units of step)
        h (int):  height along `z` (units of step)

    Returns:
        func: condition(x,y,z): whether to put or not a mesh-cell at coordinate
        tuple: discretizer walk limits necessary to contain full structure
    """

    def condition(xi, yi, zi):
        in_disc = (
            (xi / (r1 + 0.1)) ** 2 + (yi / (r2 + 0.1)) ** 2 <= 1
        ) and 0 <= zi < h - (1 / 2) ** 0.5
        return in_disc

    mesh_limits = (
        -int(r1) - 2,
        int(r1) + 2,
        -int(r2) - 2,
        int(r2) + 2,
        -1,
        2 * int(h) + 1,
    )

    return condition, mesh_limits


def disc(r: float, h: int):
    """cylinder with radius `r` in x and y, and height `h` along z

    Args:
        r (float): radius (units of step)
        h (int): height along z (units of step)

    Returns:
        func: condition(x,y,z): whether to put or not a mesh-cell at coordinate
        tuple: discretizer walk limits necessary to contain full structure
    """
    return ellipse(r, r, h)


def split_ring(r_out: float, r_in: float, h: int, alpha_g: float = 0):
    """split ring

    Args:
        r_out (float): outer radius (units of step)
        r_in (float): inner radius (units of step)
        h (int): height (units of step)
        alpha_g (float, optional): split gap angle (units of rad). Defaults to 0.

    Returns:
        func: condition(x,y,z): whether to put or not a mesh-cell at coordinate
        tuple: discretizer walk limits necessary to contain full structure
    """

    def condition(xi, yi, zi):
        C1 = r_out**2 >= (xi**2 + yi**2) >= r_in**2
        if yi > 0 and alpha_g != 0:
            C2 = not (
                torch.arctan2(torch.as_tensor(abs(xi)), torch.as_tensor(abs(yi)))
                <= alpha_g / 2.0
            )
        else:
            C2 = True

        C3 = 0 <= zi < h - 1 / 2**0.5

        return (C1 and C2) and C3

    mesh_limits = (
        -int(r_out * 2**0.5) - 2,
        int(r_out * 2**0.5) + 2,
        -int(r_out * 2**0.5) - 2,
        int(r_out * 2**0.5) + 2,
        -1,
        1.5 * int(h),
    )

    return condition, mesh_limits


def lshape(l1, l2, w1, w2, h, gap=0):

    def condition(xi, yi, zi):
        in_cuboid1 = (
            (gap < xi <= gap + l1)
            and (-1 * gap > yi >= -1 * gap - w1)
            and (0 <= zi < h - 1 / 2**0.5)
        )
        in_cuboid2 = (
            (-1 * gap > xi >= -1 * gap - w2)
            and (gap < yi <= gap + l2)
            and (0 <= zi < h - 1 / 2**0.5)
        )

        return in_cuboid1 or in_cuboid2

    dx = l1 + w2
    dy = w1 + l2
    mesh_limits = (
        -1 * abs(gap) - dy - 1,
        dx + abs(gap) + 2,
        -1 * abs(gap) - dy - 1,
        dx + abs(gap) + 2,
        0,
        h + 2,
    )
    return condition, mesh_limits


def prism_trigonal(d: int, h: int, truncate_edge: float = 0.0):
    """uniform right triangular prism with side length d and height h

    Args:
        d (int): side length  (units of step)
        h (int): height (units of step)
        truncate_edge (float, optional): truncation ratio for the top triangle edge. Defaults to 0.0.

    Returns:
        func: condition(x,y,z): whether to put or not a mesh-cell at coordinate
        tuple: discretizer walk limits necessary to contain full structure
    """
    sqrt3 = 3**0.5
    n_l = d / 2.0
    h_s = truncate_edge * n_l * sqrt3 / 2.0
    h_abs = (sqrt3 / 2.0) * n_l

    def condition(xi, yi, zi):
        in_prism = (
            (abs(xi) <= (h_abs - (yi + 0.5)) / sqrt3)
            and (
                abs(xi)
                <= (((3 * h_abs - sqrt3 * n_l * truncate_edge) + (yi + 0.5)) / sqrt3)
            )
            and (yi <= h_abs - h_s)
            and (yi >= -h_abs)
            and (0 <= zi < h - 1 / (2**0.5))
        )

        return in_prism

    mesh_limits = (
        -1 * int(n_l) - 5,
        int(n_l) + 5,
        -1 * int(n_l) - 5,
        int(n_l) + 5,
        -1 * int(h) - 5,
        int(h) + 5,
    )

    return condition, mesh_limits


def from_image(
    img_file_name,
    pixels_per_step=1,
    h=1,
    threshold=100,
    positive_contrast=True,
    return_image=False,
    center_structure=True,
):
    """planar structure from image based on contrast

    *Caution:* This is not auto-diff compatible!

    Args:
        img_file_name (string): path to image-file, or numpy array containing image. If numpy array, values should range from 0 to 255.
        pixels_per_step (int, optional): number of pixels in the image corresponding to one discretization step. This is essentially a resize factor. Defaults to 1.
        h (int, optional): height of the planar structure (units of stepsize). Defaults to 1.
        threshold (int, optional): threshold value between [0, 255] to declare a pixel as *structure*. all darker pixels will be interpreted as structure. Defaults to 100.
        positive_contrast (bool, optional): whether to interpret dark (deault) or bright pixels as structure material. Defaults to True.
        return_image (bool, optional): if True, returns a 2D numpy array corresponding to the image AND the structure. Defaults to False.
        center_structure (bool, optional): whether to automatically center structure. Defaults to True.

    Returns:
        if return_image==True:
            numpy ndarray: image pixel values

        if return_image==False, returns:
            func: condition(x,y,z): whether to put or not a mesh-cell at coordinate
            tuple: discretizer walk limits necessary to contain full structure

    """
    from PIL import Image
    import numpy as np

    # - load image
    if type(img_file_name) == str:
        img = Image.open(img_file_name)
        img.load()
    else:
        img = Image.fromarray(img_file_name)

    # - remove alpha channel, if exists
    if len(img.split()) == 4:
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])  # 3 is the alpha channel
    else:
        # RGB data --> no alpha channel
        background = img

    # - rescale image to N pixels per step
    X0 = background.size[0]
    basewidth = int(round(X0 * pixels_per_step))
    hsize = int(
        (float(background.size[1]) * float((basewidth / float(background.size[0]))))
    )
    img = background.resize((basewidth, hsize), Image.LANCZOS)
    img = img.convert("L")

    data = np.asarray(img.getdata()).reshape(img.size[::-1])
    data = np.rot90(data, 3)  # adapt to torchgdm convention: rotate by 270 degrees

    # - mesh size limits
    if center_structure:
        x_min = -(data.shape[0] // 2)
        y_min = -(data.shape[1] // 2)
        x_max = (data.shape[0] + 1) // 2
        y_max = (data.shape[1] + 1) // 2
    else:
        x_min = 0
        y_min = 0
        x_max = data.shape[0]
        y_max = data.shape[1]
    mesh_limits = (x_min - 1, x_max + 1, y_min - 1, y_max + 1, 0, h)

    # - generate structure condition for pixels above threshold
    if positive_contrast:
        data[data <= threshold] = threshold
        data[data > threshold] = 0
    else:
        data[data >= threshold] = threshold
        data[data < threshold] = 0

    def condition(xi, yi, zi):
        x_idx = int(xi - x_min)
        y_idx = int(yi - y_min)
        if x_idx < 0 or x_idx >= data.shape[0]:
            return False  # x outside data range
        elif y_idx < 0 or y_idx >= data.shape[1]:
            return False  # y outside data range
        else:
            return data[x_idx][y_idx] != 0

    if return_image:
        # original image to return
        img_orig = background.convert("L")
        data_img = np.asarray(img_orig.getdata()).reshape(img_orig.size[::-1])
        return data_img
    else:
        print(mesh_limits)
        return condition, mesh_limits


# ==============================================================================
# discretizer
# ==============================================================================
def discretizer_cubic(
    condition_func, limits: tuple, z_offset: float = 0.5, step: float = 1.0
):
    """discretize volume of a 3D structure on a cubic grid

    discretize by evaluating a boolean condition function at each
    position on a 3D grid within given spatial limits

    Args:
        condition_func (func): functional, returning the condition as function of coordinate indices. 'condition_func(xi,yi,zi)', returns a bool. (True: put a meshpoint, False: no meshpoint)
        limits (tuple): discretizer walk range. tuple of 6  ints (x0, x1, y0, y1, z0, z1)
        z_offset (float, optional): additional z-offset, to avoid placing dipoles at z=0 (units of step). Defaults to 0.5.
        step (float, optional): nominal stepsize in nm. Defaults to 1.0.

    Returns:
        torch.Tensor: 3d coordinates of discretization. shape (N, 3) for `N` meshpoints.
    """
    sp = []
    for xi in range(int(limits[0]), int(limits[1])):
        for yi in range(int(limits[2]), int(limits[3])):
            for zi in range(int(limits[4]), int(limits[5])):
                if condition_func(xi, yi, zi):
                    sp.append([xi, yi, zi + z_offset])

    return torch.as_tensor(sp, dtype=DTYPE_FLOAT) * step


def discretizer_hexagonalcompact(
    condition_func,
    limits,
    z_offset=0.5,
    step=1.0,
    orientation=1,
    auto_expand_range=True,
):
    """discretize volume of a 3D structure on a hexagonal compact grid

    discretize by evaluating a boolean condition function at each
    position on a 3D grid within given spatial limits

    Args:
        condition_func (func): functional, returning the condition as function of coordinate indices. 'condition_func(xi,yi,zi)', returns a bool. (True: put a meshpoint, False: no meshpoint)
        limits (tuple): discretizer walk range. tuple of 6  ints (x0, x1, y0, y1, z0, z1)
        z_offset (float, optional): additional z-offset, to avoid placing dipoles at z=0 (units of step). Defaults to 0.5.
        step (float, optional): nominal stepsize in nm. Defaults to 1.0.
        auto_expand_range (bool, optional): expand the discretization volume to account for possible non-integer position values. Defaults to True.

    Returns:
        torch.Tensor: 3d coordinates of discretization. shape (N, 3) for `N` meshpoints.
    """
    sp = []
    x_lim = list(limits[0:2])
    y_lim = list(limits[2:4])
    z_lim = list(limits[4:6])

    # expand discretization volume wrt hexagonal unit cell volume
    # useful e.g. for non-integer position values
    if auto_expand_range:
        vol_scale = 2 / 3**0.5 - 1
        x_lim[0] = x_lim[0] - vol_scale
        x_lim[1] = x_lim[1] + vol_scale

        y_lim[0] = y_lim[0] - vol_scale
        y_lim[1] = y_lim[1] + vol_scale

        z_lim[0] = z_lim[0] - vol_scale
        z_lim[1] = z_lim[1] + vol_scale

    # discretizer orientation 1
    if orientation == 1:
        for zi in range(int(z_lim[0]), int(z_lim[1])):
            z = zi * (2.0 / 3.0) ** 0.5
            for yi in range(int(y_lim[0]), int(y_lim[1])):
                y = yi * 3**0.5 / 2.0 + 2.0 * abs(zi / 2.0 - int(zi / 2.0)) / 3**0.5
                for xi in range(int(x_lim[0]), int(x_lim[1])):
                    x = xi + abs(yi / 2.0 - int(yi / 2.0))
                    if condition_func(x, y, z):
                        sp.append([x, y, z + z_offset])

    # discretizer orientation 2
    else:
        for xi in range(int(x_lim[0]), int(x_lim[1])):
            x = xi * (2.0 / 3.0) ** 0.5
            for yi in range(int(y_lim[0]), int(y_lim[1])):
                y = yi * 3**0.5 / 2.0 + 2.0 * abs(xi / 2.0 - int(xi / 2.0)) / 3**0.5
                for zi in range(int(z_lim[0]), int(z_lim[1])):
                    z = zi + abs(yi / 2.0 - int(yi / 2.0))
                    if condition_func(x, y, z):
                        sp.append([x, y, z + z_offset])

    return torch.as_tensor(sp, dtype=DTYPE_FLOAT) * step


# ==============================================================================
# Transformations - TODO
# ==============================================================================


# %%
if __name__ == "__main__":

    step = 20.0

    # geometry_pos = discretizer_cubic(*spheroid(9,4,4), step=step)
    geometry_pos = discretizer_cubic(*split_ring(10, 7, 2, torch.pi / 4), step=step)

    import matplotlib.pyplot as plt

    plt.scatter(geometry_pos.T[0], geometry_pos.T[1])
