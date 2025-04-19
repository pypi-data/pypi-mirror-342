# encoding=utf-8
"""
3D visualization tools for geometries
"""
# %%
import copy
import warnings
import itertools

import torch

from torchgdm.constants import COLORS_DEFAULT
from torchgdm.tools.misc import to_np
from torchgdm import tools


# global color handling
COLOR_ITERATOR = itertools.cycle(COLORS_DEFAULT)
LEGEND_ENTRIES_LOOKUP = dict()


# reset color iterator and materials lookup
def _reset_color_iterator():
    global COLOR_ITERATOR, LEGEND_ENTRIES_LOOKUP
    COLOR_ITERATOR = itertools.cycle(COLORS_DEFAULT)
    LEGEND_ENTRIES_LOOKUP = dict()


def _return_next_color():
    return next(COLOR_ITERATOR)


_reset_color_iterator()


def _generate_legend(pl):
    global LEGEND_ENTRIES_LOOKUP

    if len(LEGEND_ENTRIES_LOOKUP) != 0:
        labels = LEGEND_ENTRIES_LOOKUP.keys()
    else:
        labels = []

    pv_labels = []
    for i_s, label in enumerate(labels):
        legend_dict = LEGEND_ENTRIES_LOOKUP[label]
        pv_labels.append([label, legend_dict["fc"]])

    pl.add_legend(labels=pv_labels, bcolor="w", face=None)

    return pl.legend


def _plot_structure_discretized(
    struct,
    scale=1.0,
    color="auto",
    show_grid=True,
    legend=True,
    alpha=1.0,
    show="auto",
    pl=None,
    reset_color_cycle=True,
    struct_dim="auto",
    infinite_axis_length=1000,
    **kwargs,
):
    global COLOR_ITERATOR, LEGEND_ENTRIES_LOOKUP
    import numpy as np

    try:
        import pyvista as pv
    except ModuleNotFoundError:
        raise ModuleNotFoundError(
            "`pyvista` not found. Required for 3D plotting. Install with: "
            + "pip install 'jupyterlab>=3' ipywidgets 'pyvista[all,trame]'"
        )

    if "projection" in kwargs:
        kwargs.pop("projection")

    if struct_dim.lower() == "auto":
        struct_dim = struct.n_dim
    else:
        if struct_dim not in [2, 3]:
            raise ValueError(
                "3D geometry plot: Structure dimension must be either 2 or 3."
            )

    if reset_color_cycle:
        _reset_color_iterator()

    # get mesh positions and step sizes, cut in multi-materials
    pos = to_np(struct.get_all_positions())
    step = to_np(struct.step)

    if type(show) == str:
        if show.lower() == "auto" and pl is None:
            show = True
        else:
            False

    if pl is None:
        pl = pv.Plotter()

    if color == "auto":
        # colors = COLORS_DEFAULT
        diff_mat_names = [s.__name__ for s in struct.materials]
        mat_names = np.array(diff_mat_names)

        different_materials = np.unique(mat_names)

        mat_pos_subset_idx = []
        for pos_single_mat in different_materials:
            mat_pos_subset_idx.append(
                np.arange(len(mat_names))[mat_names == pos_single_mat]
            )
    else:
        different_materials = ["struct. id:{}".format(struct.id)]
        mat_pos_subset_idx = [np.arange(len(pos))]  # all pos
        # colors = [color]

    # the actual plot
    mesh_list = []
    for i_s, pos_idx in enumerate(mat_pos_subset_idx):
        pos_mat = pos[pos_idx]
        steplist_mat = step[pos_idx]

        # 3D plot
        if struct_dim == 3:
            pts = pv.PolyData(pos_mat)
            pts["steps"] = steplist_mat
            pts.set_active_scalars("steps")
            mesh_list.append(
                pts.glyph(geom=pv.Cube(), scale="steps", factor=scale, orient=False)
            )
        # 2D plot (plot very long "infinite" axis)
        elif struct_dim == 2:
            _b = []
            for i, _s in enumerate(steplist_mat):
                pts = pv.PolyData([pos_mat[i]])
                _b.append(
                    pts.glyph(
                        geom=pv.Box(
                            bounds=(
                                -0.5 * _s,
                                0.5 * _s,
                                -0.5,
                                infinite_axis_length,
                                -0.5 * _s,
                                0.5 * _s,
                            ),
                            level=0,
                        ),
                        orient=False,
                    )
                )
            mesh_list.append(pv.merge(_b))

    for i_s, mesh in enumerate(mesh_list):
        # chose color
        if color == "auto":
            # if material already used, re-use its color. otherwise use next color
            if different_materials[i_s] in LEGEND_ENTRIES_LOOKUP:
                _col = LEGEND_ENTRIES_LOOKUP[different_materials[i_s]]["color"]
            else:
                _col = next(COLOR_ITERATOR)
        elif type(color) in [list, tuple]:
            _col = color[i_s]
        else:
            _col = color

        # add legend entry:
        LEGEND_ENTRIES_LOOKUP[different_materials[i_s]] = dict(
            color=_col,
            fc=_col,
            ec=_col,
            marker="s",
            markersize=10,
        )

        label = different_materials[i_s]
        pl.add_mesh(
            mesh,
            color=_col,
            show_edges=show_grid,
            edge_color="black",
            line_width=0.5,
            opacity=alpha,
            edge_opacity=alpha,
            label=label,
        )

    if legend:
        _generate_legend(pl)

    if show:
        pl.show()
        pl.camera.azimuth = 180.0  # convention: x-axis to the right

    return mesh_list


def _plot_structure_eff_3dpola(
    struct,
    scale=1.0,
    center_marker_scale=10,
    color="auto",
    sphere_style="wireframe",
    color_sphere="auto",
    theta_resolution=20,
    phi_resolution=20,
    alpha=0.1,
    show_grid=True,
    color_grid="auto",
    alpha_grid=0.5,
    show="auto",
    pl=None,
    legend=False,
    reset_color_cycle=True,
    struct_dim="auto",
    infinite_axis_length=1000,
    **kwargs,
):
    global COLOR_ITERATOR, LEGEND_ENTRIES_LOOKUP
    from torchgdm import tools
    import numpy as np

    try:
        import pyvista as pv
    except ModuleNotFoundError:
        raise ModuleNotFoundError(
            "`pyvista` not found. Required for 3D plotting. Install with: "
            + "pip install 'jupyterlab>=3' ipywidgets 'pyvista[all,trame]'"
        )

    if "projection" in kwargs:
        kwargs.pop("projection")

    if struct_dim.lower() == "auto":
        struct_dim = struct.n_dim
    else:
        if struct_dim not in [2, 3]:
            raise ValueError(
                "3D geometry plot: Structure dimension must be either 2 or 3."
            )

    if reset_color_cycle:
        _reset_color_iterator()

    if type(show) == str:
        if show.lower() == "auto" and pl is None:
            show = True
        else:
            show = False

    if pl is None:
        pl = pv.Plotter()

    # legend label based on structure ID
    legend_label = "eff.pola. (id: {})".format(struct.id)

    # automatic next color
    if color == "auto":
        if legend_label in LEGEND_ENTRIES_LOOKUP:
            _col = LEGEND_ENTRIES_LOOKUP[legend_label]["color"]
        else:
            _col = next(COLOR_ITERATOR)
    else:
        _col = color

    if color_grid == "auto":
        color_grid = _col
    if color_sphere == "auto":
        color_sphere = _col

    # add / update legend entry
    LEGEND_ENTRIES_LOOKUP[legend_label] = dict(
        color=_col,
        fc=color_sphere,
        ec=_col,
        marker="o",
        markersize=10,
    )

    # geometry data to numpy
    pos_a = to_np(struct.get_all_positions())
    enclosing_radius = to_np(struct.step) / 2.0

    # create the actual plot: iterate over polarizabilities
    mesh_sphere_list = []
    mesh_center_list = []
    mesh_fullgeo_list = []

    # full mesh (if available)
    for i, _geo in enumerate(struct.full_geometries):
        pos_mesh = to_np(_geo)
        step_mesh = to_np(tools.geometry.get_step_from_geometry(_geo))

        # 3D
        if struct_dim == 3:
            # full geometry mesh = 3D
            pts = pv.PolyData(pos_mesh)
            pts["steps"] = np.ones(len(pos_mesh)) * step_mesh
            pts.set_active_scalars("steps")

            mesh_fullgeo_list.append(
                pts.glyph(geom=pv.Cube(), scale="steps", factor=scale, orient=False)
            )
        # 2D
        elif struct_dim == 2:
            # full geometry mesh
            if len(struct.full_geometries) > 0:
                _b = []
                _s = step_mesh
                for i, _pos in enumerate(pos_mesh):
                    pts = pv.PolyData([_pos])
                    _b.append(
                        pts.glyph(
                            geom=pv.Box(
                                bounds=(
                                    -0.5 * _s,
                                    0.5 * _s,
                                    -0.5,
                                    infinite_axis_length,
                                    -0.5 * _s,
                                    0.5 * _s,
                                ),
                                level=0,
                            ),
                            orient=False,
                        )
                    )
                mesh_fullgeo_list.append(pv.merge(_b))

    # effective dipoles locations
    for i, pos in enumerate(pos_a):
        if len(struct.full_geometries) == len(pos_a):
            _geo = struct.full_geometries[i]
            step_mesh = to_np(tools.geometry.get_step_from_geometry(_geo))
        else:
            step_mesh = 0.0
        r = enclosing_radius[i]

        # 3D: spheres
        if struct_dim == 3:
            # plot enclosing sphere
            mesh_sphere_list.append(
                pv.Sphere(
                    r + step_mesh / 2.0,
                    pos,
                    theta_resolution=theta_resolution,
                    phi_resolution=phi_resolution,
                )
            )

            # center pos. "marker" sphere
            mesh_center_list.append(pv.Sphere(center_marker_scale, pos))

        # 2D: very long "infinite" cylinder
        elif struct_dim == 2:
            _p = pos.copy()
            _p[1] += infinite_axis_length / 2
            # plot enclosing circle
            mesh_sphere_list.append(
                pv.Cylinder(
                    center=_p,
                    direction=[0, 1, 0],
                    radius=r + step_mesh / 2.0,
                    height=infinite_axis_length,
                    resolution=theta_resolution,
                )
            )

            # center pos. "marker" cylinder
            mesh_center_list.append(
                pv.Cylinder(
                    center=_p,
                    direction=[0, 1, 0],
                    radius=center_marker_scale,
                    height=infinite_axis_length,
                )
            )

    # plot enclosing sphere wireframe
    for i_s, mesh in enumerate(mesh_sphere_list):
        pl.add_mesh(
            mesh,
            color=color_sphere,
            show_edges=False,
            line_width=0.5,
            edge_opacity=alpha,
            opacity=alpha,
            style=sphere_style,
        )

    # plot dipole position
    for i_s, mesh in enumerate(mesh_center_list):
        pl.add_mesh(mesh, color=_col)

    # optionally plot the replaced full geometry mesh
    if show_grid and len(struct.full_geometries) > 0:
        for i_s, mesh in enumerate(mesh_fullgeo_list):
            pl.add_mesh(
                mesh,
                color=color_grid,
                show_edges=True,
                edge_color="black",
                line_width=0.5,
                opacity=alpha_grid * alpha,
                edge_opacity=alpha_grid * alpha * 0.1,
            )

    # optional legend additions
    if legend:
        _generate_legend(pl)

    if show:
        pl.show()
        pl.camera.azimuth = 180.0  # convention: x-axis to the right

    return mesh_sphere_list, mesh_center_list, mesh_fullgeo_list


def structure(
    struct,
    color="auto",
    scale=1,
    legend=True,
    reset_color_cycle=True,
    pl=None,
    show="auto",
    struct_dim="auto",
    infinite_axis_length=1000,
    **kwargs,
):
    """plot structure in 3D

    Args:
        struct (struct): simulation or structure
        color (str, optional): color of the structure. If "auto", cycle through materials. Defaults to "auto".
        scale (int, optional): global scaling factor. Defaults to 1.
        legend (bool, optional): Whether to show a material legend. Defaults to True.
        reset_color_cycle (bool, optional): restart color cycle relative to former plots. Defaults to True.
        pl (pvista plotter, optional): pvista plotter to plot in. If not given, start new one. Defaults to None.
        show (str, optional): whether to show the figure. If auto, will only show if a new plotter is created. Defaults to "auto".
        struct_dim (str, optional): structure dimension: 2 or 3. in 2D structures, plot long cylinders along the infite axis. Defaults to "auto".
        infinite_axis_length (int, optional): absolute length of infinite axis in 2D plots (in nm!). Defaults to 1000.

    Raises:
        ValueError: incorrect configurations

    Returns:
        pyvista meshes
    """
    try:
        import pyvista as pv
    except ModuleNotFoundError:
        raise ModuleNotFoundError(
            "`pyvista` not found. Required for 3D plotting. Install with: "
            + "pip install 'jupyterlab>=3' ipywidgets 'pyvista[all,trame]'"
        )
    from torchgdm.simulation import SimulationBase, Simulation
    from torchgdm.struct.struct3d import StructDiscretized3D
    from torchgdm.struct.struct3d import StructDiscretizedCubic3D
    from torchgdm.struct.struct3d import StructDiscretizedHexagonal3D
    from torchgdm.struct.struct3d import StructEffPola3D

    if reset_color_cycle:
        _reset_color_iterator()

    # got a structure instance:
    if (
        issubclass(type(struct), StructDiscretized3D)
        or issubclass(type(struct), StructDiscretizedCubic3D)
        or issubclass(type(struct), StructDiscretizedHexagonal3D)
    ):
        pl_res = _plot_structure_discretized(
            struct,
            color=color,
            scale=scale,
            show=show,
            pl=pl,
            struct_dim=struct_dim,
            infinite_axis_length=infinite_axis_length,
            **kwargs,
        )
    elif issubclass(type(struct), StructEffPola3D):
        pl_res = _plot_structure_eff_3dpola(
            struct,
            color=color,
            scale=scale,
            show=show,
            pl=pl,
            struct_dim=struct_dim,
            infinite_axis_length=infinite_axis_length,
            **kwargs,
        )
    elif issubclass(type(struct), Simulation) or issubclass(
        type(struct), SimulationBase
    ):
        # -- prep
        sim = struct

        if type(show) == str:
            if show.lower() == "auto" and pl is None:
                show = True
            else:
                show = False

        if pl is None:
            pl = pv.Plotter()

        # -- call all structure's plot functions
        pl_res = []  # collect results
        for i_s, _st in enumerate(sim.structures):
            pl_res.append(
                _st.plot3d(
                    color=color,
                    scale=scale,
                    pl=pl,
                    legend=False,
                    reset_color_cycle=False,
                    show=False,
                    struct_dim=struct_dim,
                    infinite_axis_length=infinite_axis_length,
                    **kwargs,
                )
            )

        # -- finalize: config global plot
        if legend:
            _generate_legend(pl)
        if show:
            pl.show()
            pl.camera.azimuth = 180.0  # convention: x-axis to the right
    else:
        raise ValueError("Unknown structure input")

    if reset_color_cycle:
        _reset_color_iterator()

    return pl_res
