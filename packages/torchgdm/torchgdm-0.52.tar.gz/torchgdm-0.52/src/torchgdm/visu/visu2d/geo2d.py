# encoding=utf-8
"""
2D visualization tools for geometries

"""
# %%
import copy
import itertools
import warnings

import torch

from torchgdm.constants import COLORS_DEFAULT
from torchgdm.tools.misc import to_np
from torchgdm.tools.geometry import get_projection, get_step_from_geometry
from torchgdm.visu.visu2d._tools import (
    _get_axis_existing_or_new,
    _automatic_projection,
    _optimize_alpha_value,
)


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


def _generate_legend(ax):
    import matplotlib.pyplot as plt

    global LEGEND_ENTRIES_LOOKUP

    if len(LEGEND_ENTRIES_LOOKUP) != 0:
        labels = LEGEND_ENTRIES_LOOKUP.keys()
    else:
        labels = []

    for i_s, label in enumerate(labels):
        legend_dict = LEGEND_ENTRIES_LOOKUP[label]
        plt.plot(
            [],
            [],
            marker=legend_dict["marker"],
            lw=0,
            markerfacecolor=legend_dict["fc"],
            markeredgecolor=legend_dict["ec"],
            markersize=legend_dict["markersize"],
            label=label,
        )

    return ax.legend()


def _plot_structure_discretized(
    struct,
    projection="auto",
    scale=1.0,
    color="auto",
    show_grid=True,
    legend=False,
    set_ax_aspect=True,
    alpha=1.0,
    reset_color_cycle=True,
    **kwargs,
):
    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np

    global COLOR_ITERATOR, LEGEND_ENTRIES_LOOKUP

    if reset_color_cycle:
        _reset_color_iterator()

    # prep
    grid_kwargs = dict(ec="k", lw=0.5) if show_grid else dict()
    ax, show = _get_axis_existing_or_new()
    if set_ax_aspect:
        ax.set_aspect("equal")

    # get geometry projection
    if projection.lower() == "auto":
        projection = _automatic_projection(struct.get_all_positions())
    pos_proj, idx_proj = get_projection(
        struct.get_all_positions(), projection, return_inverse=True
    )

    if struct.step.dim() == 0:
        steplist = torch.tile(struct.step, (len(struct.get_all_positions()),))
    else:
        steplist = struct.step
    steplist_proj = steplist[idx_proj]

    # convert to numpy
    pos_proj = to_np(pos_proj)
    idx_proj = to_np(idx_proj)
    steplist_proj = to_np(steplist_proj)

    # multi-material: different colors for parts of same material
    if color == "auto":
        diff_mat_names = [s.__name__ for s in struct.materials]
        mat_names = np.array(diff_mat_names)[idx_proj]

        different_materials = np.unique(mat_names)

        mat_pos_subset_idx = []
        for pos_single_mat in different_materials:
            mat_pos_subset_idx.append(
                np.arange(len(mat_names))[mat_names == pos_single_mat]
            )

    else:
        different_materials = ["struct. id:{}".format(struct.id)]
        mat_pos_subset_idx = [np.arange(len(pos_proj))]

    # the actual plot: create square patches for each meshcell
    # colors_for_legend = []
    for i_s, pos_idx in enumerate(mat_pos_subset_idx):
        x, y = pos_proj[pos_idx].T[:2]
        steplist_sub = steplist_proj[pos_idx]
        patches = []

        # rectangles for each mesh-cell
        for i_pt, [xi, yi] in enumerate(zip(x, y)):
            step = scale * steplist_sub[i_pt]
            step_plt = float(step / struct.mesh_normalization_factor)
            xis = xi - step_plt / 2
            yis = yi - step_plt / 2

            # TODO: plot actual hex mesh as hexagons
            patches.append(
                plt.Rectangle((xis, yis), width=step_plt, height=step_plt, linewidth=0)
            )

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

        # add patch collection to plot
        kwargs.pop("color_circle", None)
        c = matplotlib.collections.PatchCollection(
            patches, fc=_col, alpha=alpha, **grid_kwargs, **kwargs
        )
        ax.add_collection(c)

    # optional plot legend
    if legend:
        _generate_legend(ax)

    # config axes
    plt.autoscale(tight=False)
    plt.xlabel("{} (nm)".format(projection[0]))
    plt.ylabel("{} (nm)".format(projection[1]))

    if show:
        plt.show()
    else:
        return ax


def _plot_contour_discretized(
    struct,
    projection="auto",
    color="auto",
    set_ax_aspect=True,
    alpha=1.0,
    alpha_value=None,
    **kwargs,
):
    """plot the concave hull around 2D projection of a structure discretization

    Args:
        struct (struct or torch.Tensor): structure or torch.Tensor of discretized object
        projection (str, optional): Which 2D projection plane to use. Defaults to "auto".
        color (str, optional): optional matplotlib compatible color. Defaults to "auto".
        set_ax_aspect (bool, optional): If True, will set aspect of plot to equal. Defaults to True.
        alpha (float, optional): matplotlib transparency value. Defaults to 1.0.
        alpha_value (str or float, optional): alpha_value for concave hull calculation. If None, use 1/step. If "opt", or "optimize", use a simple optimization scheme. Defaults to None.

    Raises:
        ValueError: no solution found

    Returns:
        matplotlib axes
    """
    import matplotlib.pyplot as plt
    import alphashape
    import logging

    global COLOR_ITERATOR, LEGEND_ENTRIES_LOOKUP

    # prep
    ax, show = _get_axis_existing_or_new()
    if set_ax_aspect:
        ax.set_aspect("equal")

    # automatic next color
    if color == "auto":
        color = next(COLOR_ITERATOR)

    if type(struct) == torch.Tensor:
        positions = struct.to("cpu")
        mesh_norm_factor = 1.0
    else:
        positions = struct.get_all_positions().to("cpu")
        mesh_norm_factor = struct.mesh_normalization_factor.to("cpu")

    # get geometry projection
    if projection.lower() == "auto":
        projection = _automatic_projection(positions)
    pos_proj, idx_proj = get_projection(positions, projection, return_inverse=True)

    # expand geometry by a half-step (outer points)
    step = get_step_from_geometry(pos_proj)
    step_plt = step / mesh_norm_factor
    pos_px = pos_proj + torch.as_tensor([[step_plt / 2, step_plt / 2]])
    pos_mx = pos_proj + torch.as_tensor([[-step_plt / 2, step_plt / 2]])
    pos_py = pos_proj + torch.as_tensor([[step_plt / 2, -step_plt / 2]])
    pos_my = pos_proj + torch.as_tensor([[-step_plt / 2, -step_plt / 2]])
    pos2d_exp = torch.concatenate([pos_px, pos_mx, pos_py, pos_my])

    # concave hull (alpha shape) - ignore warnings
    if alpha_value is None:
        alpha_value = 1.0 / step
    if type(alpha_value) == str:
        if alpha_value.lower() in ["opt", "optimize"]:
            alpha_value = _optimize_alpha_value(pos2d_exp)

    original_log_level = logging.getLogger().getEffectiveLevel()
    logging.disable(logging.WARN)
    geo_alpha = alphashape.alphashape(pos2d_exp, alpha_value)
    logging.disable(original_log_level)
    # in future: maybe replace by a simple local implementation to avoid dependencies
    # edges = _alpha_shape(pos2d_exp, alpha_value)

    if geo_alpha.geom_type == "Polygon":
        g_a_list = [geo_alpha]
    elif geo_alpha.geom_type == "MultiPolygon":
        g_a_list = [_g for _g in geo_alpha.geoms]
    else:
        raise ValueError("Unexpected error: Unknown alphashape geometry.")

    for _geo_a in g_a_list:
        # plot every sub geometry
        xx, yy = _geo_a.exterior.coords.xy
        xx, yy = xx.tolist(), yy.tolist()
        ax.plot(xx, yy, color=color, alpha=alpha, **kwargs)

    ax.autoscale(tight=False)
    ax.set_xlabel("{} (nm)".format(projection[0]))
    ax.set_ylabel("{} (nm)".format(projection[1]))

    if show:
        plt.show()

    return ax


def _plot_structure_eff_pola(
    struct,
    projection="auto",
    scale=1.0,
    color="auto",
    linestyle_circle=(0, (2, 2)),
    color_circle="auto",
    color_circle_fill=None,
    alpha=1,
    show_grid=True,
    color_grid="auto",
    alpha_grid=0.25,
    legend=False,
    set_ax_aspect=True,
    reset_color_cycle=True,
    **kwargs,
):
    import matplotlib
    import matplotlib.pyplot as plt

    global COLOR_ITERATOR, LEGEND_ENTRIES_LOOKUP

    if reset_color_cycle:
        _reset_color_iterator()

    ax, show = _get_axis_existing_or_new()
    if set_ax_aspect:
        ax.set_aspect("equal")

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
    if color_circle == "auto":
        color_circle = _col
    if color_circle_fill is None:
        color_circle_fill = (1, 1, 1, 0.0)

    # add / update legend entry
    LEGEND_ENTRIES_LOOKUP[legend_label] = dict(
        color=_col,
        fc=color_circle_fill,
        ec=_col,
        marker="o",
        markersize=10,
    )

    # get geometry projection
    all_pos = struct.get_all_positions()
    if projection.lower() == "auto":
        projection = _automatic_projection(all_pos)
    pos_proj = get_projection(all_pos, projection, unique=False)

    steplist = struct.step

    # convert to numpy
    pos_proj = to_np(pos_proj)
    steplist = to_np(steplist)

    # plot enclosing spheres for eff. polas. structures
    if len(steplist) == len(pos_proj):
        patches = []
        for i_s, [xi, yi] in enumerate(zip(*pos_proj.T)):
            patches.append(
                plt.Circle((xi, yi), radius=steplist[i_s] / 2.0, fc=color_circle_fill)
            )
        c = matplotlib.collections.PatchCollection(
            patches,
            fc=color_circle_fill,
            ec=color_circle,
            linestyle=linestyle_circle,
            linewidth=1,
        )
        ax.add_collection(c)

    # optionally, plot all points of represented geometries
    if show_grid:
        for subgeo in struct.full_geometries:
            geo_step = to_np(get_step_from_geometry(torch.as_tensor(subgeo)))
            subgeo_proj, idx_proj = get_projection(
                subgeo, projection, return_inverse=True
            )
            Xsg, Ysg = to_np(subgeo_proj).T[:2]

            patches2 = []
            for i_pt, [xi, yi] in enumerate(zip(Xsg, Ysg)):
                step = scale * geo_step
                xis = xi - step / 2
                yis = yi - step / 2
                patches2.append(plt.Rectangle((xis, yis), width=step, height=step))
            c2 = matplotlib.collections.PatchCollection(
                patches2,
                color=color_grid,
                ec="k",
                lw=0.5,
                alpha=alpha * alpha_grid,
                **kwargs,
            )
            ax.add_collection(c2)

    # optional legend additions
    if legend:
        _generate_legend(ax)

    # plot centers of mass
    plt.scatter(*pos_proj.T, s=scale * 25, marker="x", c="k", alpha=alpha, **kwargs)

    # config axes
    plt.autoscale(tight=False)
    plt.xlabel("{} (nm)".format(projection[0]))
    plt.ylabel("{} (nm)".format(projection[1]))

    return ax


def structure(
    struct,
    projection="auto",
    color="auto",
    legend=True,
    reset_color_cycle=True,
    **kwargs,
):
    """plot 2D projection of structure

    plot the structure `struct` as a scatter projection to a carthesian plane.
    Either from a structure instance, or using a simulation as input.

    kwargs are passed to individual structure plotting and / or to matplotlib's `scatter`

    Parameters
    ----------
    struct : simulation or structure
          either a simulation or a structure instance

    projection : str, default: 'auto'
        which 2D projection to plot: "auto", "XY", "YZ", "XZ"

    color : str or matplotlib color, default: "auto"
            Color of scatterplot. Either "auto", or matplotlib-compatible color.
            "auto": automatic color selection (multi-color for multiple materials).

    legend : bool, default: True
        whether to add a legend if multi-material structure (requires auto-color enabled)


    Returns
    -------
    result returned by matplotlib's `scatter`

    """
    import matplotlib.pyplot as plt
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
        im = _plot_structure_discretized(
            struct,
            projection=projection,
            color=color,
            legend=legend,
            reset_color_cycle=False,
            **kwargs,
        )

    # got a structure effective pola. instance
    elif issubclass(type(struct), StructEffPola3D):
        im = _plot_structure_eff_pola(
            struct,
            projection=projection,
            color=color,
            legend=legend,
            reset_color_cycle=False,
            **kwargs,
        )

    # got a simulation instance
    elif issubclass(type(struct), Simulation) or issubclass(
        type(struct), SimulationBase
    ):
        # -- prep
        sim = struct
        ax, show = _get_axis_existing_or_new()

        if projection.lower() == "auto":
            if len(sim.get_all_positions()) > 1:
                projection = _automatic_projection(sim.get_all_positions())

        # -- call each structure's plot functions
        for i_s, _st in enumerate(sim.structures):
            im = _st.plot(
                projection=projection,
                color=color,
                legend=False,
                reset_color_cycle=False,
                **kwargs,
            )

        # -- finalize: config global plot
        if legend:
            _generate_legend(ax)
        if show:
            plt.show()
    else:
        raise ValueError("Unknown structure input")

    if reset_color_cycle:
        _reset_color_iterator()

    return im


def contour(
    struct,
    projection="auto",
    color="auto",
    set_ax_aspect=True,
    alpha=1.0,
    alpha_value=None,
    reset_color_cycle=True,
    **kwargs,
):
    """plot contour of a structure's 2D projection

    plot the contour of structure `struct` as a scatter projection to a carthesian plane.
    Either from list of coordinates, structure object or a simulation instance.
    For effective polarizability structures, will try to use the full mesh if available.

    Note: Doesn't support legend entries so far.

    Args:
        struct (Simulation, Structure): either a simulation or a structure instance
        projection (str, optional): which cartesian plane to project onto. Defaults to "auto".
        color (str, optional): optional matplotlib compatible color. Defaults to "auto".
        set_ax_aspect (bool, optional): If True, will set aspect of plot to equal. Defaults to True.
        alpha (float, optional): matplotlib transparency value. Defaults to 1.0.
        alpha_value (float, optional): alphashape value. If `None`, try to automatically optimize for best enclosing of structure. Defaults to None.
        reset_color_cycle (bool, optional): reset color cycle after finishing the plot. Defaults to True.

    Raises:
        ValueError: Invalid structure input

    Returns:
        matplotlib line: matplotlib's `scatter` output
    """

    import matplotlib.pyplot as plt
    from torchgdm.simulation import SimulationBase, Simulation
    from torchgdm.struct.struct3d import StructDiscretized3D
    from torchgdm.struct.struct3d import StructDiscretizedCubic3D
    from torchgdm.struct.struct3d import StructDiscretizedHexagonal3D
    from torchgdm.struct.struct3d import StructEffPola3D

    if reset_color_cycle:
        _reset_color_iterator()

    if (
        issubclass(type(struct), StructDiscretized3D)
        or issubclass(type(struct), StructDiscretizedCubic3D)
        or issubclass(type(struct), StructDiscretizedHexagonal3D)
        or type(struct) == torch.Tensor
    ):
        return _plot_contour_discretized(
            struct,
            projection=projection,
            color=color,
            alpha=alpha,
            alpha_value=alpha_value,
            set_ax_aspect=set_ax_aspect,
            **kwargs,
        )
    elif issubclass(type(struct), StructEffPola3D):
        if len(struct.full_geometries) == 0:
            warnings.warn("No mesh grid data available. Skipping.")
            return None
        ax, show = _get_axis_existing_or_new()
        for subgeo in struct.full_geometries:
            im = _plot_contour_discretized(
                subgeo,
                projection=projection,
                color=color,
                alpha=alpha,
                alpha_value=alpha_value,
                set_ax_aspect=set_ax_aspect,
                **kwargs,
            )
        return im
    elif issubclass(type(struct), Simulation) or issubclass(
        type(struct), SimulationBase
    ):
        # -- prep
        sim = struct
        ax, show = _get_axis_existing_or_new()

        if projection.lower() == "auto":
            projection = _automatic_projection(sim.get_all_positions())

        # -- call each structure's plot functions
        for i_s, _st in enumerate(sim.structures):
            im = _st.plot_contour(
                projection=projection,
                color=color,
                alpha=alpha,
                alpha_value=alpha_value,
                **kwargs,
            )

        # -- finalize: config global plot
        if show:
            plt.show()

        return im
    else:
        raise ValueError("Unknown structure input")


if __name__ == "__main__":
    print("test")
    import time
    import torchgdm as tg
    import matplotlib.pyplot as plt

    # - full structure: volume discretization
    step = 25.0  # nm
    r_disc = 120 / step  # units of step
    h_disc = 2
    material = tg.materials.MatConstant(eps=12.0)
    t0 = time.time()
    geometry = tg.struct3d.discretizer_hexagonalcompact(
        *tg.struct3d.disc(r_disc, h_disc), step=step, orientation=1
    )
    struct = tg.struct3d.StructDiscretizedHexagonal3D(geometry, material)
    # geometry = tg.struct3d.discretizer_cubic(
    #     *tg.struct3d.disc(r_disc, h_disc), step=step
    # )
    # struct = tg.struct3d.StructDiscretizedCubic3D(geometry, material)

    print(struct)
    print("Time meshing".format(time.time() - t0))

    fig, ax = plt.subplots()
    structure(struct)
    _plot_contour_discretized(struct)
    plt.show()
