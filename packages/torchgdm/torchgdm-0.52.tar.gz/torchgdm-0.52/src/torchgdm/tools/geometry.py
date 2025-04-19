# -*- coding: utf-8 -*-
"""
torchgdm tools for geometry data
"""
# %%
from typing import Optional
import warnings

import torch

from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX
from torchgdm.tools.misc import get_default_device


# --- Cartesian <--> spherical
def transform_spherical_to_xyz(r, teta, phi):
    x = r * torch.sin(teta) * torch.cos(phi)
    y = r * torch.sin(teta) * torch.sin(phi)
    z = r * torch.cos(teta)
    return x, y, z


def transform_xyz_to_spherical(x, y, z):
    r = torch.sqrt(x**2 + y**2 + z**2)
    teta = torch.acos(z / r)
    phi = torch.atan2(y, x)
    return r, teta, phi


# --- coordinate list tools
def coordinate_map_1d(
    lim_r1, n_step_r1=20, r2=0.0, r3=0.0, direction="x", device="cpu"
):
    """Generate Cartesian equidistant coordinates along a line

    Args:
        lim_r1 (tuple of float): run limits coordinate 1. If float, use [-lim_r1, +lim_r1]
        n_step1 (int, optional): nr of steps coord 1. Defaults to 20.
        r2, r3 (float, optional): fixed value for coord 2 and 3. Defaults to 0.0. Coord order: x,y,z
        direction (str, optional): along which axis. Defaults to 'x'

    Returns:
        dict: contains positions and line elements. keys:
            - "r_probe": torch.Tensor: coordinate list, shape (n_step_r1, 3)
            - "ds": torch.Tensor: list of line elements ("dl") of each position, shape (n_step_r1)
    """
    if type(lim_r1) in [float, int]:
        lim_r1 = [-lim_r1, lim_r1]
    r1s = torch.linspace(
        lim_r1[0], lim_r1[1], steps=n_step_r1, dtype=DTYPE_FLOAT, device=device
    )

    # point grid
    r2s = r2 * torch.ones_like(r1s)
    r3s = r3 * torch.ones_like(r1s)

    # line elements
    dl = abs(lim_r1[1] - lim_r1[0]) / n_step_r1
    dl = torch.ones_like(r1s) * dl

    # stack x/y/z
    if direction.lower() == "x":
        r_probe = torch.stack([r1s, r2s, r3s], dim=1)
    elif direction.lower() == "y":
        r_probe = torch.stack([r2s, r1s, r3s], dim=1)
    elif direction.lower() == "z":
        r_probe = torch.stack([r2s, r3s, r1s], dim=1)
    else:
        raise ValueError("Unknown direction. Must be one of: x, y, z.")

    dict_surface = dict(r_probe=r_probe, ds=dl)
    return dict_surface


def coordinate_map_1d_circular(
    r=100000.0,
    lim_phi=(0, 2 * torch.pi),
    n_phi=72,
    y0=0,
    device="cpu",
):
    """Generate Cartesian coordinates on a circle in the xz plane

    Equidistant solid angles.
    By default, create coordinates around full circle with radius `r`

    Args:
        r (float, optional): radius of sphere in nm (distance to origin). Defaults to 100000nm (=100 microns). Defaults to 100000.0.
        lim_phi (tuple, optional): minimum and maximum angle in radians, excluding last position (in linear steps from `phimin` to `phimax`). Defaults to (0, 2 * torch.pi).
        n_phi (int, optional): number of angle steps. Defaults to 72.
        y0 (float, optional): y-position of the circle. Defaults to 0.
        device (str, optional): Defaults to "cpu".

    Returns:
        dict: contains positions and line elements. keys:
            - "r_probe": torch.Tensor: coordinate list, shape (n_phi, 3)
            - "ds": torch.Tensor: list of line elements of each position, shape (n_phi)
    """
    to_kws = dict(dtype=DTYPE_FLOAT, device=device)

    # polar angle: exclude endpoint
    phi = (
        torch.ones(int(n_phi), **to_kws)
        * torch.linspace(lim_phi[0], lim_phi[1], int(n_phi) + 1, **to_kws)[:-1]
    )  # .unsqueeze(0)

    # Cartesian points
    x, y, z = transform_spherical_to_xyz(r, torch.ones_like(phi) * torch.pi / 2.0, phi)
    r_probe = torch.stack([x.flatten(), z.flatten(), y.flatten()], axis=1)
    r_probe[:, 1] = y0

    # surface elements
    dphi = abs(lim_phi[1] - lim_phi[0]) / float(n_phi)
    dl = torch.ones_like(phi) * r * dphi

    dict_surface = dict(r_probe=r_probe, ds=dl, phi=phi)
    return dict_surface


def coordinate_map_1d_circular_upper(
    r=100000.0,
    n_phi=72,
    y0=0,
    device="cpu",
):
    """1D Cartesian coordinates in xz plane on the upper half-circle

    teta: pi - 2pi.
    see :func:`coordinate_map_1d_circular` for more detailed documentation.

    Args:
        r (float, optional): radius of circle in nm (distance to origin). Defaults to 100000nm (=100 microns). Defaults to 100000.0.
        n_phi (int, optional): number of angle steps. Defaults to 72.
        y0 (float, optional): y-position of the circle. Defaults to 0.
        device (str, optional): Defaults to "cpu".

    Returns:
        dict: contains positions and line elements. keys:
            - "r_probe": torch.Tensor: coordinate list, shape (n_phi, 3)
            - "ds": torch.Tensor: list of line elements of each position, shape (n_phi)
    """
    return coordinate_map_1d_circular(
        r=r,
        lim_phi=(0, torch.pi),
        n_phi=n_phi,
        y0=y0,
        device=device,
    )


def coordinate_map_1d_circular_lower(
    r=100000.0,
    n_phi=72,
    y0=0,
    device="cpu",
):
    """1D Cartesian coordinates in xz plane on the lower half-circle

    phi: 0 - pi.
    see :func:`coordinate_map_1d_circular` for more detailed documentation.

    Args:
        r (float, optional): radius of circle in nm (distance to origin). Defaults to 100000nm (=100 microns). Defaults to 100000.0.
        n_phi (int, optional): number of angle steps. Defaults to 72.
        y0 (float, optional): y-position of the circle. Defaults to 0.
        device (str, optional): Defaults to "cpu".

    Returns:
        dict: contains positions and line elements. keys:
            - "r_probe": torch.Tensor: coordinate list, shape (n_phi, 3)
            - "ds": torch.Tensor: list of line elements of each position, shape (n_phi)
    """
    return coordinate_map_1d_circular(
        r=r,
        lim_phi=(torch.pi, 2 * torch.pi),
        n_phi=n_phi,
        y0=y0,
        device=device,
    )


def coordinate_map_2d(
    lim_r1,
    lim_r2,
    n_step_r1=20,
    n_step_r2=20,
    r3=0.0,
    projection="xy",
    device="cpu",
):
    """Generate Cartesian equidistant coordinates on rectangular 2d area

    Args:
        lim_r1 (tuple of float): run limits coordinate 1. If float, use [-lim_r1, +lim_r1]
        lim_r2 (tuple of float): run limits coordinate 2. If float, use [-lim_r2, +lim_r2]
        n_step1 (int, optional): nr of steps coord 1. Defaults to 20.
        n_step2 (int, optional): nr of steps coord 2. Defaults to 20.
        r3 (float, optional): fixed value for coord 3. Defaults to 0.0.
        projection (str, optional): parallel to which plane. Defaults to 'xy'

    Returns:
        dict: contains positions and surface elements. keys:
            - "r_probe": torch.Tensor: coordinate list, shape (n_step_r1 * n_step_r2, 3)
            - "ds": torch.Tensor: list of surface elements of each position, shape (n_step_r1 * n_step_r2)
    """
    if type(lim_r1) in [float, int]:
        lim_r1 = [-lim_r1, lim_r1]
    if type(lim_r2) in [float, int]:
        lim_r2 = [-lim_r2, lim_r2]

    r1s = torch.linspace(
        lim_r1[0], lim_r1[1], steps=n_step_r1, dtype=DTYPE_FLOAT, device=device
    )
    r2s = torch.linspace(
        lim_r2[0], lim_r2[1], steps=n_step_r2, dtype=DTYPE_FLOAT, device=device
    )

    # point grid
    r1f, r2f = torch.meshgrid(r1s, r2s, indexing="xy")
    r1f = r1f.flatten()
    r2f = r2f.flatten()
    r_const = r3 * torch.ones_like(r1f)

    # surface elements
    ds = (abs(lim_r1[1] - lim_r1[0]) / n_step_r1) * (
        abs(lim_r2[1] - lim_r2[0]) / n_step_r2
    )
    ds = torch.ones_like(r1f) * ds

    # stack x/y/z
    if projection.lower() == "xy":
        r_probe = torch.stack([r1f, r2f, r_const], dim=1)
    if projection.lower() == "xz":
        r_probe = torch.stack([r1f, r_const, r2f], dim=1)
    if projection.lower() == "yz":
        r_probe = torch.stack([r_const, r1f, r2f], dim=1)

    dict_surface = dict(r_probe=r_probe, ds=ds)
    return dict_surface


def coordinate_map_2d_square(
    d, n=20, r3=0.0, delta1=0.0, delta2=0.0, projection="xy", device="cpu"
):
    """Generate Cartesian equidistant coordinates on square 2d area

    square map with extents [-d, d] centered at position (delta1, delta2)

    Args:
        d (float): upper and lower limit (useing the negative) for map
        n (int, optional): nr of steps coords 1 and 2. Defaults to 20.
        r3 (float, optional): fixed value for coord 3. Defaults to 0.0.
        delta1, delta2 (float, optional): offsets (shift) for coordinates 1 and 2. Default to 0.0.
        projection (str, optional): parallel to which plane. Defaults to 'xy'
        device (str, optional): which torch device. Defaults to 'cpu'

    Returns:
        dict: contains positions and surface elements. keys:
            - "r_probe": torch.Tensor: coordinate list, shape (n * n, 3)
            - "ds": torch.Tensor: list of surface elements of each position, shape (n * n)
    """
    dict_surface = coordinate_map_2d(
        lim_r1=[-d + delta1, d + delta1],
        lim_r2=[-d + delta2, d + delta2],
        n_step_r1=n,
        n_step_r2=n,
        r3=r3,
        projection=projection,
        device=device,
    )
    return dict_surface


def coordinate_map_2d_spherical(
    r=100000.0,
    lim_teta=(0, torch.pi),
    lim_phi=(0, 2 * torch.pi),
    n_teta=18,
    n_phi=36,
    device="cpu",
):
    """Generate Cartesian coordinate list on a spherical screen with equidistant solid angles

    by default, create coordinates on surface of full sphere with radius `r`

    Args:
        r (float, optional): radius of sphere in nm (distance to origin). Defaults to 100000nm (=100 microns). Defaults to 100000.0.
        lim_teta (tuple, optional): minimum and maximum polar angle in radians (in linear steps from `tetamin` to `tetamax`). Defaults to (0, torch.pi).
        lim_phi (tuple, optional): minimum and maximum azimuth angle in radians, excluding last position (in linear steps from `phimin` to `phimax`). Defaults to (0, 2 * torch.pi).
        n_teta (int, optional): number of polar angle steps. Defaults to 18.
        n_phi (int, optional): number of azimuthal angle steps. Defaults to 36.
        device (str, optional): Defaults to "cpu".

    Returns:
        dict: contains positions and surface elements. keys:
            - "r_probe": torch.Tensor: coordinate list, shape (n_teta * n_phi, 3)
            - "ds": torch.Tensor: list of surface elements of each position, shape (n_teta * n_phi)
    """
    to_kws = dict(dtype=DTYPE_FLOAT, device=device)

    # azimuth
    teta = torch.ones((int(n_teta), int(n_phi)), **to_kws) * torch.linspace(
        lim_teta[0], lim_teta[1], int(n_teta), **to_kws
    ).unsqueeze(1)

    # polar: exclude endpoint
    phi = torch.ones((int(n_teta), int(n_phi)), **to_kws) * torch.linspace(
        lim_phi[0], lim_phi[1], int(n_phi) + 1, **to_kws
    )[:-1].unsqueeze(0)

    # Cartesian points
    x, y, z = transform_spherical_to_xyz(r, teta, phi)
    r_probe = torch.stack([x.flatten(), y.flatten(), z.flatten()], axis=1)

    # surface elements
    dteta = abs(lim_teta[1] - lim_teta[0]) / float(n_teta - 1)
    dphi = abs(lim_phi[1] - lim_phi[0]) / float(n_phi)
    ds = r**2 * torch.sin(teta.flatten()) * dteta * dphi

    dict_surface = dict(r_probe=r_probe, ds=ds, phi=phi, teta=teta)
    return dict_surface


def coordinate_map_2d_spherical_upper(
    r=100000.0,
    n_teta=18,
    n_phi=72,
    device="cpu",
):
    """Generate Cartesian coordinates with equidistant solid angles on the upper half-sphere

    teta: 0 - pi/2, phi: 0 - 2pi.
    see :func:`coordinate_map_2d_spherical` for more detailed documentation.

    Args:
        r (float, optional): radius of sphere in nm (distance to origin). Defaults to 100000nm (=100 microns). Defaults to 100000.0.
        n_teta (int, optional): number of polar angle steps. Defaults to 18.
        n_phi (int, optional): number of azimuthal angle steps. Defaults to 72.
        device (str, optional): Defaults to "cpu".

    Returns:
        dict: contains positions and surface elements. keys:
            - "r_probe": torch.Tensor: coordinate list, shape (n_teta * n_phi, 3)
            - "ds": torch.Tensor: list of surface elements of each position, shape (n_teta * n_phi)
    """
    return coordinate_map_2d_spherical(
        r=r,
        lim_teta=(0, torch.pi / 2),
        lim_phi=(0, 2 * torch.pi),
        n_teta=n_teta,
        n_phi=n_phi,
        device=device,
    )


def coordinate_map_2d_spherical_lower(
    r=100000.0,
    n_teta=18,
    n_phi=72,
    device="cpu",
):
    """Generate Cartesian coordinates with equidistant solid angles on the lower half-sphere

    teta: pi/2 - pi, phi: 0 - 2pi.
    see :func:`coordinate_map_2d_spherical` for more detailed documentation.

    Args:
        r (float, optional): radius of sphere in nm (distance to origin). Defaults to 100000nm (=100 microns). Defaults to 100000.0.
        n_teta (int, optional): number of polar angle steps. Defaults to 18.
        n_phi (int, optional): number of azimuthal angle steps. Defaults to 72.
        device (str, optional): Defaults to "cpu".

    Returns:
        dict: contains positions and surface elements. keys:
            - "r_probe": torch.Tensor: coordinate list, shape (n_teta * n_phi, 3)
            - "ds": torch.Tensor: list of surface elements of each position, shape (n_teta * n_phi)
    """
    return coordinate_map_2d_spherical(
        r=r,
        lim_teta=(torch.pi / 2, torch.pi),
        lim_phi=(0, 2 * torch.pi),
        n_teta=n_teta,
        n_phi=n_phi,
        device=device,
    )


def sample_random_spherical(npoints, device="cpu"):
    """random positions on R=1 sphere"""
    ndim = 3
    vec = torch.rand(npoints, ndim, device=device) - 0.5
    vec /= torch.linalg.norm(vec, axis=1).unsqueeze(1)
    return vec


def sample_random_circular(npoints, projection="xz", device="cpu"):
    """random positions on R=1 circle"""
    if projection.lower() == "xz":
        plane_dim = 1
    elif projection.lower() == "xy":
        plane_dim = 2
    elif projection.lower() == "yz":
        plane_dim = 0
    else:
        raise ValueError

    ndim = 3
    vec = torch.rand(npoints, ndim, device=device) - 0.5
    vec[:, plane_dim] = vec[:, plane_dim] * 0
    vec /= torch.linalg.norm(vec, axis=1).unsqueeze(1)
    return vec


# ----- volume discretization tools
def get_step_from_geometry(positions: torch.Tensor, max_meshpoints: int = 2000):
    """obtain step from a list of coordinates that define a nano-structure

    returns closest distance occuring between two meshpoints in `positions`.
    Uses :func:`torch.cdist`.

    Args:
        positions (torch.Tensor): list of positions to evaluate
        max_meshpoints (int, optional): maximum number of meshpoints to consider for step-calculation (to limit memory requirement). Defaults to 2000.

    Returns:
        float: stepsize between mesh-points
    """
    if len(positions) == 1:
        warnings.warn("Structure consists of a single dipole. Returning `1`.")
        step = 1.0
    elif len(positions) == 0:
        warnings.warn("Empty structure. Returning `1`.")
        step = 1.0
    else:
        if len(positions) > max_meshpoints:
            _geo = positions[:max_meshpoints]
        else:
            _geo = positions
        dists = torch.cdist(_geo, _geo)
        step = torch.sort(torch.flatten(dists))[0][len(_geo)]

    return step


def unique_rows(positions_xy: torch.Tensor, return_inverse: bool = False):
    """delete all duplicates with same x/y coordinates

    Args:
        positions_xy (torch.Tensor): list of (x,y) coordinates with partially redunant (x,y) values.
        return_inverse (bool, optional): return indices of original values which ended up in the unique tensor. Defaults to False.

    Raises:
        ValueError: invalid shape of input positions

    Returns:
        torch.Tensor: tensor containing all unique positions. If `return_inverse` is `True`, return a second torch.Tensor containing the indices in the original tensor of the unique elements
    """
    if positions_xy.shape[1] != 2:
        raise ValueError("Coordinate list must consist of (x,y) 2-tuples.")

    unique_a, idx = torch.unique(positions_xy, dim=0, sorted=True, return_inverse=True)

    if return_inverse:
        # return also indices of unique tensor for each element in the full tensor
        # warning: this is not deterministic, it will return the indices of arbitrarily chosen ones of multiple duplicates
        idx_unique = torch.zeros(
            len(unique_a), dtype=int, device=positions_xy.device
        ).scatter_(0, idx, torch.arange(len(positions_xy), device=positions_xy.device))
        idx_unique.to(unique_a.device)
        return unique_a, idx_unique
    else:
        return unique_a


def get_projection(positions, projection="xy", unique=True, return_inverse=False):
    """get projection of coordinates onto a Cartesian plane

    Args:
        positions (torch.Tensor): _description_
        projection (str, optional): Cartesian plane to project on. One of ["xy", "xz" , "yz"]. Defaults to "xy".
        unique (bool, optional): If True, remove duplicate projected coordinates. Defaults to True.
        return_inverse (bool, optional): return indices of original values which ended up in the unique tensor. Defaults to False.

    Raises:
        ValueError: Invalid projection argument

    Returns:
        torch.Tensor: coordinate list of projected positions. If `return_inverse` is `True`, return a second torch.Tensor containing the indices in the original tensor of the unique elements
    """
    if projection.lower() == "xy":
        twodim_coords = positions[:, [0, 1]]
    elif projection.lower() == "yz":
        twodim_coords = positions[:, [1, 2]]
    elif projection.lower() == "xz":
        twodim_coords = positions[:, [0, 2]]
    else:
        raise ValueError("Invalid projection parameter!")

    if unique and return_inverse:
        pos_proj, idx = unique_rows(twodim_coords, return_inverse=return_inverse)
        return pos_proj, idx
    if unique and not return_inverse:
        pos_proj = unique_rows(twodim_coords)
        return pos_proj
    if not unique:
        return twodim_coords


def get_geometric_crosssection(struct, projection="xy"):
    """return the geometric cross sections ("footprint") projected onto a Cartesian plane

    Args:
        struct (structure instance): instance of structure
        projection (str, optional): Cartesian plane to project on. One of ["xy", "xz" , "yz"]. Defaults to "xy".

    Returns:
        float: geometric cross section in nm^2
    """

    # TODO: calculate this better using alpha shapes?
    step = struct.step
    _pos_proj, idx = get_projection(
        positions=struct.get_all_positions(), projection=projection, return_inverse=True
    )
    step = step[idx] / struct.mesh_normalization_factor
    cs_geo = torch.sum(step**2)  # * len(pos_proj)
    return cs_geo


def _get_geo_cs_positions_steps(pos, steps, projection="xy"):
    """geometric cross section from list of pos and steps"""
    # TODO: calculate this better using alpha shapes?
    _pos_proj, idx = get_projection(
        positions=pos, projection=projection, return_inverse=True
    )
    steps_visible = steps[idx]
    cs_geo = torch.sum(steps_visible**2)
    return cs_geo


def get_enclosing_sphere_radius(positions: torch.Tensor):
    """get radius of enclosing sphere, that totally contains the full structure

    Args:
        positions (torch.Tensor): (x,y,z) tuples of meshpoints describing the structure

    Returns:
        float: radius of circumscribing sphere
    """
    r0 = torch.mean(positions, axis=0)
    step = get_step_from_geometry(positions)

    geo_center_abs = torch.abs(positions - r0)
    geo_origin_abs = geo_center_abs - torch.min(geo_center_abs, dim=0)[0].unsqueeze(0)
    dist_to_origin = torch.linalg.norm(geo_origin_abs, dim=1)
    dist_to_edge = torch.max(dist_to_origin) + step

    return dist_to_edge


def get_surface_meshpoints(
    positions,
    NN_bulk=6,
    max_bound=1.2,
    NN_surface=None,
    max_bound_sf=5.0,
    return_sfvec_all_points=False,
):
    """get surface elements and normal surface vectors of structure

    Calculate normal vectors using next-neighbor counting.

    To use outmost surface layer only, parameters are:
     - 2D: NN_bulk=4, max_bound=1.1
     - 3D: NN_bulk=6, max_bound=1.1

    **Caution:** Not auto-differentiable. This is using scipy.


    Args:
        positions (torch.Tensor): shape (N, 3) with N number of positions.
        NN_bulk (int, optional): Number of Next neighbors of a bulk lattice point. Defaults to 6.
        max_bound (float, optional): Max. distance in step-units to search for next neighbors. Defaults to 1.2.
        NN_surface (int, optional): different number of neighbours to consider for normal surfacevectors. Defaults to None ( = value of NN_bulk).
        max_bound_sf (float, optional): different calculation range for normal surfacevectors. By default, use search radius of up to 5 steps. If a large number of neighbours should be considered for vector calculation, it might be necessary to increased this limit, which might however slow down the KD-tree queries. Defaults to 5.0.
        return_sfvec_all_points (bool, optional): if True, return vector list for all meshpoints, with zero length if bulk. Defaults to False.

    Returns:
        tuple of 2 torch.Tensor: list of surface meshpoint coordinates, list of normal surface vectors
    """
    import numpy as np
    from scipy.spatial import cKDTree as KDTree
    from torchgdm import to_np

    assert len(positions.shape) == 2
    assert positions.shape[1] == 3

    geo_pos = to_np(positions)
    step = get_step_from_geometry(positions=positions)

    if NN_surface is None:
        NN_surface = NN_bulk

    # Find number and positions of next neigbours using KD-Tree queries
    kdtree = KDTree(geo_pos)

    surface_pos, sf_normal_vec = [], []
    for i, pos in enumerate(geo_pos):
        # query for nearest neighbors
        resultNNbulk = kdtree.query(
            pos, k=NN_bulk + 1, distance_upper_bound=max_bound * step
        )
        if NN_surface != NN_bulk:
            resultNNsurface = kdtree.query(
                pos, k=NN_surface + 1, distance_upper_bound=max_bound_sf * step
            )
        else:
            resultNNsurface = resultNNbulk

        # exclude center and "empty" positions, get number of neighbors
        IDX = (resultNNbulk[0] != 0) & (resultNNbulk[0] != np.inf)
        NN = len(resultNNbulk[0][IDX])
        IDXsf = (resultNNsurface[0] != 0) & (resultNNsurface[0] != np.inf)

        # surface-positions
        if NN < NN_bulk:
            x, y, z = geo_pos[i]
            # calculate normal surface vector using nearest neighbors
            Nvec = [(pos[:3] - geo_pos[j][:3]) for j in resultNNsurface[1][IDXsf]]
            Nvec = np.sum(Nvec, axis=0)
            if np.linalg.norm(Nvec) == 0:
                warnings.warn(
                    "Indefinite surface element (meshpoint is part of two surfaces)! Using one of two possible sides for normal vector direction!"
                )
                if pos[:3][0] != 0:
                    Nvec = np.array([0, 1, 0])
                elif pos[:3][1] != 0:
                    Nvec = np.array([1, 0, 0])
                elif pos[:3][2] != 0:
                    Nvec = np.array([0, 1, 0])
            else:
                Nvec = Nvec / np.linalg.norm(Nvec)
            surface_pos.append(geo_pos[i])
            sf_normal_vec.append(Nvec)
        else:
            if return_sfvec_all_points:
                sf_normal_vec.append(np.array([0, 0, 0]))

    return (
        torch.as_tensor(
            np.array(surface_pos), dtype=DTYPE_FLOAT, device=positions.device
        ),
        torch.as_tensor(
            np.array(sf_normal_vec), dtype=DTYPE_FLOAT, device=positions.device
        ),
    )


def get_positions_outside_struct(
    struct, pos_spacing, min_dist_to_struct=2.0, nn_sf_averaging=[6, 10, 20, 50]
):
    """Get positions and surface normal vectors around structure

    Args:
        struct (torchgdm `structure` instance): structure outside of which positions are seeked
        pos_spacing (float): distance to surface (in units of step).
        min_dist_to_struct (float, optional): minimum distance to other surfaces (in units of step). Defaults to 2.0.
        nn_sf_averaging (list, optional): numbers of next neighbors to use for surface normal calculations. Multiple elements possible. Defaults to [6, 10, 20, 50].

    Returns:
        (torch.Tensor, torch.Tensor): positions outside and surface normals used to obtain. Both of shape (N_pts, 3)
    """
    n_dim = struct.n_dim
    device = struct.device
    step_max = torch.max(struct.step)
    spacing_nm = pos_spacing * step_max

    # - get outside positions using surface normal vectors
    if n_dim == 2:
        NN_bulk, max_bound = 4, 1.1
    elif n_dim == 3:
        NN_bulk, max_bound = 6, 1.1

    sf_pos = []
    sf_vec_n = []
    for nn_sf in nn_sf_averaging:
        _sf_pos, _sf_vec = get_surface_meshpoints(
            struct.get_all_positions(),
            NN_bulk=NN_bulk,
            max_bound=max_bound,
            NN_surface=nn_sf,
        )
        sf_pos.append(_sf_pos)
        sf_vec_n.append(_sf_vec)
    sf_pos = torch.cat(sf_pos, dim=0)
    sf_vec_n = torch.cat(sf_vec_n, dim=0)

    sf_pos = sf_pos + spacing_nm * sf_vec_n

    # - remove positions that intersect with the structure
    from torchgdm.tools.batch import batched

    @batched(batch_kwarg="pos_step_1", arg_position=0, default_batch_size=1024)
    def get_violated_distances(pos_step_1, pos_step_2):
        pos1 = pos_step_1[..., :3]
        pos2 = pos_step_2[..., :3]
        steps1 = pos_step_1[..., 3]
        steps2 = pos_step_2[..., 3]
        dp = torch.norm(pos1.unsqueeze(0) - pos2.unsqueeze(1), dim=-1)
        dp_step1 = torch.where(dp < (steps1.unsqueeze(0) / 2 + steps2.unsqueeze(1) / 2))

        return dp_step1[0]

    # - test mutual distances between structure and outside positions
    pos1 = struct.get_all_positions()
    pos2 = sf_pos
    step_r1 = struct.get_source_validity_radius() * min_dist_to_struct
    step_r2 = torch.ones(len(pos2), device=device) * step_r1.max() * min_dist_to_struct
    pos_step_1 = torch.cat([pos1, step_r1.unsqueeze(1)], dim=1)
    pos_step_2 = torch.cat([pos2, step_r2.unsqueeze(1)], dim=1)

    idx_valid_pos2 = get_violated_distances(
        pos_step_1=pos_step_1, pos_step_2=pos_step_2
    )

    # - indices of positions to keep
    idx_invalid = torch.unique(idx_valid_pos2)
    mask_keep = torch.ones(len(sf_pos), dtype=torch.bool, device=device)
    mask_keep[idx_invalid] = False
    idx_valid = torch.arange(len(sf_pos), device=device)[mask_keep]

    return sf_pos[idx_valid], sf_vec_n[idx_valid]


def test_structure_distances(s1, s2, return_counts=True, on_distance_violation="warn"):
    """test if two structures have intersecting elements

    Args:
        s1 (structure-like): torchgdm structure or simulation instance
        s2 (structure-like): torchgdm structure or simulation instance
        return_counts (bool, optional): if True, returns counts of structure 1 and 2 distance-violated positions. Defaults to True.
        on_distance_violation (str, optional): behavior on distance violation. can be "error", "warn" or `None` (do nothing). Defaults to "warn".

    Raises:
        ValueError: on intersection, if `on_distance_violation="error"`

    Returns:
        tuple: return values depend on the `return_counts` kwarg.
            - if `True`: return just 2 numbers: intersecting positions for each struct.
            - if `False`: return 2 lists of positions of distance-violated dipoles in structure 1, respectively 2
    """
    from torchgdm.tools.batch import batched

    @batched(batch_kwarg="pos_step_2", arg_position=1)
    def get_violated_distances(pos_step_1, pos_step_2):
        pos1 = pos_step_1[..., :3]
        pos2 = pos_step_2[..., :3]
        steps1 = pos_step_1[..., 3]
        steps2 = pos_step_2[..., 3]
        dp = torch.norm(pos1.unsqueeze(0) - pos2.unsqueeze(1), dim=-1)
        dp_step1 = torch.where(dp < steps1.unsqueeze(0) / 2 + steps2.unsqueeze(1) / 2)
        dp_step2 = torch.where(dp < steps2.unsqueeze(1) / 2 + steps1.unsqueeze(0) / 2)

        return pos1[torch.unique(dp_step1[1])], pos2[torch.unique(dp_step2[0])]

    pos1 = s1.get_all_positions()
    pos2 = s2.get_all_positions()
    step_r1 = s1.get_source_validity_radius()
    step_r2 = s2.get_source_validity_radius()

    pos1_violation, pos2_violation = get_violated_distances(
        pos_step_1=torch.cat([pos1, step_r1.unsqueeze(1)], dim=1),
        pos_step_2=torch.cat([pos2, step_r2.unsqueeze(1)], dim=1),
    )

    N_dist1, N_dist2 = len(pos1_violation), len(pos2_violation)
    message = "Several meshpoints in structures are too close (s1: {}, s2: {})!".format(
        N_dist1, N_dist2
    )
    if on_distance_violation == "error" and (N_dist1 + N_dist2 > 0):
        raise ValueError(message)
    elif on_distance_violation == "warn" and (N_dist1 + N_dist2 > 0):
        warnings.warn(message)

    if return_counts:
        return N_dist1, N_dist2
    else:
        return pos1_violation, pos2_violation


def rotation_x(alpha, device="cpu"):
    """matrix for clockwise rotation around x-axis by angle `alpha` (in radian)"""
    alpha = torch.as_tensor(alpha, dtype=DTYPE_FLOAT, device=device)
    s = torch.sin(alpha)
    c = torch.cos(alpha)
    rot_x = torch.as_tensor(
        [[1, 0, 0], [0, c, -s], [0, s, c]],
        dtype=DTYPE_FLOAT,
        device=device,
    )
    return rot_x


def rotation_y(alpha, device="cpu"):
    """matrix for clockwise rotation around y-axis by angle `alpha` (in radian)"""
    alpha = torch.as_tensor(alpha, dtype=DTYPE_FLOAT, device=device)
    s = torch.sin(alpha)
    c = torch.cos(alpha)
    rot_y = torch.as_tensor(
        [[c, 0, s], [0, 1, 0], [-s, 0, c]],
        dtype=DTYPE_FLOAT,
        device=device,
    )
    return rot_y


def rotation_z(alpha, device="cpu"):
    """matrix for clockwise rotation around z-axis by angle alpha (in radian)"""
    alpha = torch.as_tensor(alpha, dtype=DTYPE_FLOAT, device=device)
    s = torch.sin(alpha)
    c = torch.cos(alpha)
    rot_z = torch.as_tensor(
        [[c, -s, 0], [s, c, 0], [0, 0, 1]],
        dtype=DTYPE_FLOAT,
        device=device,
    )
    return rot_z


# %%
if __name__ == "__main__":
    import torchgdm as tg

    # - discretized structure
    struct1 = tg.struct3d.StructDiscretizedCubic3D(
        tg.struct3d.cube(l=4), step=25, materials=tg.materials.MatDatabase("Si")
    )
    struct1 = struct1 + [0, 0, 70]
    struct2 = tg.struct3d.StructDiscretizedCubic3D(
        tg.struct3d.disc(r=3, h=4),
        step=15,
        materials=tg.materials.MatDatabase("Si"),
    )

    env = tg.env.freespace_3d.EnvHomogeneous3D(
        env_material=tg.materials.MatConstant(eps=1.0)
    )
    # struct2 = struct2.convert_to_effective_polarizability_pair([500], env)
    # struct2 = struct2.copy([[0, 0, 100], [50, 10, 50]])

    print(test_structure_distances(struct1, struct2, True))

# %%
