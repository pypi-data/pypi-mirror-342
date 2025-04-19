# -*- coding: utf-8 -*-
"""point polarizability classes"""
import warnings
import copy

import torch

from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX
from torchgdm.struct.struct3d.gpm3d import StructGPM3D
from torchgdm.struct.struct2d.surface import StructDiscretized2D
from torchgdm.tools.misc import ptp
from torchgdm.tools.misc import get_default_device


# --- base class volume discretized structure container - 3D
class StructGPM2D(StructGPM3D):
    """class for 2D line polarizability structure (infinite y axis)"""

    __name__ = "effective line polarizability (2D) structure class"

    def __init__(
        self,
        positions: torch.Tensor,
        gpm_dicts: list,
        radiative_correction: bool = True,
        device: torch.device = None,
        environment=None,
        shift_z_to_r0: bool = True,
        progress_bar=True,
    ):
        """2D line polarizability class

        The main information is provided in the `alpha_dicts`, which is a list of dicts with the full effective polarizability definitions. Each dict defines one structure and must contain following:
            - 'wavelengths': wavelengths at which the polarizabilities are calculated
            - at least one of: ['alpha_pE', 'alpha_mH', 'alpha_mE', 'alpha_pH']:
                polarizability tensors of shape [len(wavelengths), 3, 3]
            optional keys:
            - 'full_geometry': the original volume discretization of the represented geometry
            - 'r0': the origin of the effective polarizabilities with respect to optional 'full_geometry'
            - 'enclosing_radius': enclosing radius of original structure

        Args:
            positions (torch.Tensor): polarizability positions (3D, but all y values must be zero)
            alpha_dicts (list): list of polarizability model dictionaries
            radiative_correction (bool, optional): Whether to add raditative correction for cross section calculations. Defaults to True.
            device (torch.device, optional): Defaults to "cpu".
            environment (`environment` instance, optional): 2D environment class. By default use environment defined in eff.pola. dictionary. Defaults to None.
            shift_z_to_r0 (bool, optional): If True, if a position z-value is zero, each polarizability model's z position will be shifted to the height of the effective dipole development center. Defaults to True.

        Raises:
            ValueError: positions for 2D simulations must be at y=0
        """
        if device is None:
            self.device = get_default_device()
        else:
            self.device = device

        # expand positions, put single scatterer in list
        _positions = torch.as_tensor(positions, dtype=DTYPE_FLOAT, device=self.device)
        if len(_positions.shape) == 1:
            assert len(_positions) == 3
            _positions = _positions.unsqueeze(0)

        if torch.count_nonzero(_positions[..., 1]) > 0:
            warnings.warn("2D structure. Remove all positions with y!=0.")
            _positions = _positions[_positions[..., 1] != 0]
            if len(_positions) == 0:
                raise ValueError("No mesh positions at y=0. Please check geometry.")

        super().__init__(
            positions=positions,
            gpm_dicts=gpm_dicts,
            environment=environment,
            shift_z_to_r0=shift_z_to_r0,
            device=device,
            progress_bar=progress_bar,
        )

        self.n_dim = 2

        self.radiative_correction = radiative_correction

    def __repr__(self, verbose=False):
        """description about structure"""
        out_str = ""
        out_str += "------ 2D effective line GPM object -------"
        out_str += "\n" + " nr. of dipole-pairs:    {}".format(
            len(self.get_all_positions())
        )
        out_str += "\n" + " nominal enclosing circle diameters (nm): {}".format(
            [round(float(f), 1) for f in torch.unique(self.step)]
        )
        if len(self.full_geometries) > 0:
            pos = torch.cat(self.full_geometries)
            out_str += "\n" + " original 2D geometry: "
            out_str += "\n" + "  - replacing nr. of meshpoints: {}".format(len(pos))
            bnds = ptp(pos, dim=0)
            out_str += "\n" + "  - size & position:"
            out_str += "\n" + "        X-extension    :    {:.1f} (nm)".format(bnds[0])
            out_str += "\n" + "        Z-extension    :    {:.1f} (nm)".format(bnds[2])
            out_str += "\n" + "  - center of mass :    ({:.1f}, {:.1f}, {:.1f})".format(
                *[float(f) for f in self.get_center_of_mass()]
            )

        return out_str

    # - radiative correction for cross section calc. - 2D case
    # inherit from discretized 2D class
    get_radiative_correction_prefactor_p = (
        StructDiscretized2D.get_radiative_correction_prefactor_p
    )
    get_radiative_correction_prefactor_m = (
        StructDiscretized2D.get_radiative_correction_prefactor_m
    )

    # --- plotting
    def plot(
        self,
        scale=1.0,
        color="auto",
        linestyle_circle=(0, (2, 2)),
        color_circle="auto",
        color_circle_fill=None,
        alpha=1,
        show_grid=True,
        color_grid="auto",
        alpha_grid=0.25,
        legend=True,
        set_ax_aspect=True,
        reset_color_cycle=True,
        gpm_plot_source_probes=False,
        **kwargs,
    ):
        """plot the structure of the effective line-polarizability (2D)

        Args:
            scale (float, optional): scaling factor of the grid cells, if shown. Defaults to 1.0.
            color (str, optional): plot color. Defaults to "auto".
            linestyle_circle (tuple, optional): optional line style for enclosing circle. Defaults to (0, (2, 2)).
            color_circle (str, optional): optional alternative color for enclosing circle. Defaults to "auto".
            color_circle_fill (_type_, optional): optional alternative fill color for enclosing circle. Defaults to None.
            alpha (int, optional): optional transparency. Defaults to 1.
            show_grid (bool, optional): whether to show mesh grid (if available in structure). Defaults to True.
            color_grid (str, optional): optional alternative color for the mesh grid. Defaults to "auto".
            alpha_grid (float, optional): optional alternative transparency for the mesh grid. Defaults to 0.25.
            legend (bool, optional): show legend. Defaults to True.
            set_ax_aspect (bool, optional): automatically set aspect ratio to equal. Defaults to True.
            reset_color_cycle (bool, optional): reset color cycle after finishing the plot. Defaults to True.
            gpm_plot_source_probes (bool, optional): Plot the GPM extraction source and probe locations. Defaults to False.

        Returns:
            matplotlib axes
        """
        kwargs["projection"] = "xz"
        im = super().plot(
            scale=scale,
            color=color,
            linestyle_circle=linestyle_circle,
            color_circle=color_circle,
            color_circle_fill=color_circle_fill,
            alpha=alpha,
            show_grid=show_grid,
            color_grid=color_grid,
            alpha_grid=alpha_grid,
            legend=legend,
            set_ax_aspect=set_ax_aspect,
            reset_color_cycle=reset_color_cycle,
            gpm_plot_source_probes=gpm_plot_source_probes,
            **kwargs,
        )

        return im

    def plot_contour(
        self,
        color="auto",
        set_ax_aspect=True,
        alpha=1.0,
        alpha_value=None,
        reset_color_cycle=True,
        **kwargs,
    ):
        """plot the contour of the underlying 2D-mesh (2D)

        Args:
            color (str, optional): optional matplotlib compatible color. Defaults to "auto".
            set_ax_aspect (bool, optional): If True, will set aspect of plot to equal. Defaults to True.
            alpha (float, optional): matplotlib transparency value. Defaults to 1.0.
            alpha_value (float, optional): alphashape value. If `None`, try to automatically optimize for best enclosing of structure. Defaults to None.
            reset_color_cycle (bool, optional): reset color cycle after finishing the plot. Defaults to True.

        Returns:
            matplotlib line: matplotlib's `scatter` output
        """
        kwargs["projection"] = "xz"
        im = super().plot_contour(
            color=color,
            set_ax_aspect=set_ax_aspect,
            alpha=alpha,
            alpha_value=alpha_value,
            reset_color_cycle=reset_color_cycle,
            **kwargs,
        )

        return im

    def plot3d(self, **kwargs):
        """plot the point polarizability structure (3D)"""
        im = super().plot3d(**kwargs)

        return im

    # --- geometry operations
    def rotate(
        self,
        alpha: float,
        center: torch.Tensor = torch.as_tensor([0.0, 0.0, 0.0]),
        axis: str = "y",
    ):
        """rotate the structure

        Args:
            alpha (float): rotation angle (in rad)
            center (torch.Tensor, optional): center of rotation axis. Defaults to torch.as_tensor([0.0, 0.0, 0.0]).
            axis (str, optional): rotation axis. Defaults to "y".

        Raises:
            ValueError: only "y" axis supported in 2D

        Returns:
            :class:`StructDiscretized2D`: copy of structure with rotated geometry
        """
        if axis.lower() != "y":
            raise ValueError(
                "Only rotation axis 'y' supported in 2D (infinite axis).".format(axis)
            )

        _struct_rotated = super().rotate(alpha=alpha, center=center, axis=axis)

        return _struct_rotated


# --- Mie sphere - GPM3d
class StructMieCylinderGPM2D(StructGPM2D):
    """class for Mie-theory based 2D GPM

    Defines a global polarizability matrix structure representing an infinite core-shell cylinder.
    TorchGDM infinite axis is along Y.
    Caution, GPM is an empirical model, its accuracy depends on a successful extraction procedure.

    Requires external package `treams`
    !!! class constructor does not support automatic differentiation !!!

    """

    __name__ = "Mie-theory cylinder GPM (2D) structure class"

    def __init__(
        self,
        r_gpm: torch.Tensor,
        wavelengths: torch.Tensor,
        radii: list,
        materials: list,
        mmax=5,
        environment=None,
        r0: torch.Tensor = None,
        device: torch.device = None,
        verbose=True,
        progress_bar=True,
        **kwargs,
    ):
        """2D GPM class for a core-shell cylinder (Mie)

        Use Mie theory to get an effective GPM model for a core-shell cylinder.
        Requires the `treams` package for Mie coefficient calculation.
        https://github.com/tfp-photonics/treams

        `pip install treams`

        Args:
            r_gpm (int or torch.Tensor): Either int: number of positions or a torch.Tensor of shape (N, 3), giving the locations where to place effective dipole pairs.
            wavelengths (torch.Tensor): list of wavelengths to evaluate (nm)
            radii (list): list of the sphere's core and (multiple) shell radii (in nm).
            materials (list): materials of core and shell(s). A float or int is interpreted as permittivity value.
            mmax (int, optional): maximum order of Mie expansion. Defaults to 5.
            environment (environment instance, optional): Homogeneous 2D environment to evaluate Mie theory in. Defaults to None, which uses vacuum.
            r0 (torch.Tensor, optional): GPM structure position (x,y,z). If not given, is set to (0, 0, 0). Defaults to None
            device (torch.device, optional): Defaults to "cpu".
            verbose (bool, optional): whether to print progess info. Defaults to True.
            progress_bar (bool, optional): Progress bar for several tmatrices. Defaults to True.
            **kwargs: are passed to :func:`torchgdm.struct.eff_model_tools.extract_gpm_from_tmatrix`

        Raises:
            ValueError: incorrect parameters
        """
        import numpy as np
        from torchgdm.tools.misc import to_np
        from torchgdm.tools.misc import _check_environment
        from torchgdm.tools.misc import get_default_device
        from torchgdm.struct.eff_model_tools import extract_gpm_from_tmatrix
        from torchgdm.materials import MatConstant

        try:
            # ignore import warnings
            with warnings.catch_warnings():
                import treams
        except ModuleNotFoundError:
            print("Requires `treams`, install via `pip install treams`.")
            raise

        if device is None:
            self.device = get_default_device()
        else:
            self.device = device

        # environment
        env = _check_environment(environment, N_dim=2, device=device)

        # tensor conversion
        wavelengths = torch.as_tensor(
            wavelengths, dtype=DTYPE_FLOAT, device=self.device
        )
        wavelengths = torch.atleast_1d(wavelengths)
        k0 = 2 * torch.pi / wavelengths
        k0 = torch.as_tensor(k0, device=device)

        # radii to array
        radii = np.atleast_1d(radii)
        r_enclosing = np.max(radii)  # outer radius

        # if single material, put in list
        if not hasattr(materials, "__iter__"):
            materials = [materials]

        n_env = np.zeros(len(wavelengths), dtype=np.complex128)
        tmatrixC_list = []
        for i_wl, wl in enumerate(wavelengths):

            # embedding medium and wavevector therein
            eps_env = to_np(env.env_material.get_epsilon(wavelength=wl).real)[0, 0]
            n_env[i_wl] = eps_env**0.5

            # core and shell materials
            mat_treams = []
            for mat in materials:
                if type(mat) in [float, int, complex]:
                    mat = MatConstant(mat)
                eps_mat = to_np(mat.get_epsilon(wavelength=wl))[0, 0]
                mat_treams.append(treams.Material(eps_mat))

            # add environment material last
            mat_treams.append(treams.Material(float(eps_env)))

            tmatrixC_list.append(
                treams.TMatrixC.cylinder(
                    kzs=0.0,
                    mmax=mmax,
                    k0=float(to_np(k0[i_wl])),
                    radii=radii,
                    materials=mat_treams,
                )
            )

        dict_gpm = extract_gpm_from_tmatrix(
            tmatrixC_list,
            r_enclosing=r_enclosing,
            wavelengths=wavelengths,
            r_gpm=r_gpm,
            environment=env,
            device=self.device,
            verbose=verbose,
            progress_bar=progress_bar,
            **kwargs,
        )

        # set center of mass
        if r0 is None:
            r0 = torch.as_tensor([0.0, 0.0, 0.0], dtype=DTYPE_FLOAT, device=self.device)
        else:
            r0 = torch.as_tensor(r0, dtype=DTYPE_FLOAT, device=self.device)
            r0 = r0.squeeze()
            assert len(r0) == 3

        super().__init__(positions=r0, gpm_dicts=[dict_gpm], device=self.device)


class StructTMatrixGPM2D(StructGPM2D):
    """class for cylindrical T-Matrix based 2D GPM

    Defines a global polarizability matrix structure approximating cylindrical (2D) T-Matrices.
    TorchGDM infinite axis is along Y.
    Caution, GPM is an empirical model, its accuracy depends on a successful extraction procedure.

    Requires external package `treams`
    !!! class constructor does not support automatic differentiation !!!

    """

    __name__ = "T-Matrix based GPM (2D) structure class"

    def __init__(
        self,
        tmatrices,
        r_gpm: torch.Tensor,
        r_enclosing: float,
        r0: torch.Tensor = None,
        device: torch.device = None,
        verbose=True,
        progress_bar=True,
        test_accuracy=False,
        **kwargs,
    ):
        """2D GPM class to approximate an arbitrary cylindrical T-Matrix (2D)

        Use `treams` to extract an effective GPM model for a 2D T-Matrix (or a list of).
        If a list is given, it needs to contain spectrally resolved T-Matrices (each at a different wavelength).
        Torchgdm assumes that the T-Matrices describe the same object.

        Requires the `treams` package for T-matrix scattered field calculations.
        https://github.com/tfp-photonics/treams

        `pip install treams`


        Args:
            tmatrices (list): list of treams T-matrices. Each T-Matrix must describe the same object at different wavelengths.
            r_enclosing (float): radius of T-matrix enclosing sphere in nm (assume center at origin).
            r_gpm (int or torch.Tensor): Either int: number of positions or a torch.Tensor of shape (N, 3), giving the locations where to place effective dipole pairs.
            r0 (torch.Tensor, optional): position to move the structure to (x,y,z). If not given, use the origin (0, 0, 0). Defaults to None
            device (torch.device, optional): Defaults to "cpu".
            verbose (bool, optional): whether to print progess info. Defaults to True.
            progress_bar (bool, optional): Progress bar for several tmatrices. Defaults to True.
            test_accuracy (bool, optional): Whether to test accuracy against a T-Matrix scattering simulation. Defaults to False.
            **kwargs: are passed to :func:`torchgdm.struct.eff_model_tools.extract_gpm_from_tmatrix`

        Raises:
            ValueError: incorrect parameters
        """
        from torchgdm.tools.misc import get_default_device
        from torchgdm.struct.eff_model_tools import extract_gpm_from_tmatrix
        from torchgdm.tools.tmatrix import _test_effective_model_accuracy_2d

        try:
            # ignore import warnings
            with warnings.catch_warnings():
                import treams
        except ModuleNotFoundError:
            print("Requires `treams`, install via `pip install treams`.")
            raise

        if device is None:
            self.device = get_default_device()
        else:
            self.device = device

        dict_gpm = extract_gpm_from_tmatrix(
            tmatrices,
            r_enclosing=r_enclosing,
            r_gpm=r_gpm,
            device=self.device,
            verbose=verbose,
            progress_bar=progress_bar,
            **kwargs,
        )

        # set center of mass
        if r0 is None:
            r0 = torch.as_tensor([0.0, 0.0, 0.0], dtype=DTYPE_FLOAT, device=self.device)
        else:
            r0 = torch.as_tensor(r0, dtype=DTYPE_FLOAT, device=self.device)
            r0 = r0.squeeze()
            assert len(r0) == 3

        super().__init__(positions=r0, gpm_dicts=[dict_gpm], device=self.device)

        if test_accuracy:
            _test_results = _test_effective_model_accuracy_2d(
                self, dict_gpm["t_matrices"]
            )
