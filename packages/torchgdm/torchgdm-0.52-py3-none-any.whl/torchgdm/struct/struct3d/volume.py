# -*- coding: utf-8 -*-
"""3D volume discretization structure classes"""
import warnings
import copy

import torch

from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX, COLORS_DEFAULT
from torchgdm.tools.misc import get_default_device
from torchgdm.struct.base_classes import StructBase
from torchgdm.tools.geometry import get_step_from_geometry
from torchgdm.tools.geometry import rotation_x, rotation_y, rotation_z


# --- base class volume discretized structure container - 3D
class StructDiscretized3D(StructBase):
    """base class volume discretized structure

    Using a list of positions and materials (for permittivites),
    this class defines the basic volume discretization, the
    polarizabilities and self-terms
    """

    __name__ = "3D volume discretized structure class"

    def __init__(
        self,
        positions: torch.Tensor,
        materials,
        step=None,
        mesh_normalization_factor: float = 1,
        on_distance_violation: str = "warn",
        radiative_correction: bool = False,
        device: torch.device = None,
        **kwargs,
    ):
        """3D discretized structure

        Args:
            positions (torch.Tensor): meshpoint positions (3D, but all y values must be zero)
            materials (material class, or list of them): material of structure. If list, define the material of each meshpoint.
            step (float, optional): nominal stepsize. If not provided, infer automatically from geometry. Defaults to None.
            mesh_normalization_factor (float, optional): mesh normalization. Needs to be adapted for non-cubic meshes. Defaults to 1 (cubic).
            on_distance_violation (str, optional): behavior on distance violation. can be "error", "warn", None (silent), or "ignore" (do nothing, keep invalid meshpoints). Defaults to "error".
            radiative_correction (bool, optional): Whether to add raditative correction for cross section calculations. Defaults to False.
            device (torch.device, optional): Defaults to "cpu" (can be changed by :func:`torchgdm.use_cuda`).

        Raises:
            ValueError: Invalid material config
        """
        super().__init__(device=device, **kwargs)
        self.mesh = "3D"
        self.n_dim = 3

        # test for collisions:
        geo = torch.as_tensor(positions, dtype=DTYPE_FLOAT, device=self.device)

        if on_distance_violation.lower() == "ignore":
            geo_clean = geo
        if step is not None:
            norm = torch.norm(geo.unsqueeze(0) - geo.unsqueeze(1), dim=-1)
            norm[norm.triu() == 0] += 100 * step
            geo_clean = geo[norm.min(dim=0).values >= step * 0.999]
        else:
            warnings.warn("step not provided, cannot check mesh consistency.")
            geo_clean = geo

        if on_distance_violation.lower() == "error" and (len(geo) > len(geo_clean)):
            raise ValueError(
                "{} meshpoints in structure are too close!".format(
                    len(geo) - len(geo_clean)
                )
            )
        elif on_distance_violation.lower() == "warn" and (len(geo) > len(geo_clean)):
            warnings.warn(
                "{} meshpoints in structure are too close! Removing concerned meshpoints and continue.".format(
                    len(geo) - len(geo_clean)
                )
            )
        self.positions = torch.as_tensor(
            geo_clean, dtype=DTYPE_FLOAT, device=self.device
        )

        self.r0 = self.get_center_of_mass()  # center of gravity

        if step is None:
            step_scalar = get_step_from_geometry(self.positions)
        else:
            step_scalar = step
        # step for every meshcell, for consistency with other struct classes
        self.step = step_scalar * torch.ones(
            len(self.positions), dtype=DTYPE_FLOAT, device=self.device
        )

        self.mesh_normalization_factor = torch.as_tensor(
            mesh_normalization_factor, dtype=DTYPE_FLOAT, device=self.device
        )
        if mesh_normalization_factor == 1:
            self.mesh = "cubic"
        else:
            self.mesh = "hexagonal"

        self.radiative_correction = radiative_correction

        # material of each meshpoint
        if hasattr(materials, "__iter__"):
            if len(materials) != len(self.positions):
                raise ValueError(
                    "Either a global material needs to be given or "
                    + "each meshpoint needs a defined material. "
                    + "But meshpoint list and materials list are of different lengths."
                )
            self.materials = materials
        else:
            self.materials = [materials for i in self.positions]

        self.zeros = torch.zeros(
            (len(self.positions), 3, 3), dtype=DTYPE_COMPLEX, device=self.device
        )

        # discretized, made from natural material: only electric response
        self.interaction_type = "E"

    def __repr__(self, verbose=False):
        """description about structure"""
        from torchgdm.tools.misc import ptp

        out_str = ""
        out_str += "------ discretized 3D nano-object -------"
        out_str += "\n" + " mesh type:              {}".format(self.mesh)
        out_str += "\n" + " nr. of meshpoints:      {}".format(len(self.positions))
        out_str += "\n" + " nominal stepsizes (nm): {}".format(
            [float(f) for f in torch.unique(self.step)]
        )
        out_str += "\n" + " materials:              {}".format(
            [m.__name__ for m in set(self.materials)]
        )
        bnds = ptp(self.positions, dim=0)
        out_str += "\n" + " size & position:"
        out_str += "\n" + "     X-extension    :    {:.1f} (nm)".format(bnds[0])
        out_str += "\n" + "     Y-extension    :    {:.1f} (nm)".format(bnds[1])
        out_str += "\n" + "     Z-extension    :    {:.1f} (nm)".format(bnds[2])
        out_str += "\n" + "     center of mass :    ({:.1f}, {:.1f}, {:.1f})".format(
            *self.r0
        )

        return out_str

    def set_device(self, device):
        """move all tensors of the class to device"""
        super().set_device(device)

        self.zeros = self.zeros.to(device)
        self.step = self.step.to(device)
        self.r0 = self.r0.to(device)

        self.mesh_normalization_factor = self.mesh_normalization_factor.to(device)

        for mat in self.materials:
            mat.set_device(device)

    # --- self-terms
    def get_selfterm_pE(self, wavelength: float, environment) -> torch.Tensor:
        """return list of 'EE' self-term tensors (3x3) at each meshpoint

        Args:
            wavelength (float): in nm
            environment (environment class): 3D environement class

        Returns:
            torch.Tensor: pE self term tensor
        """
        eps_env = environment.get_environment_permittivity_scalar(
            wavelength, r_probe=self.positions
        )

        norm_nonrad = (
            (-4 * torch.pi)
            * self.mesh_normalization_factor
            / (3 * self.step**3 * eps_env)
        )

        if self.radiative_correction:
            k0 = 2 * torch.pi / wavelength
            norm_rad = (
                self.mesh_normalization_factor
                * (1j * k0**3 * (2 / 3))
                * torch.ones(
                    len(self.positions), dtype=DTYPE_COMPLEX, device=self.device
                )
            )
            cnorm = norm_nonrad + norm_rad
        else:
            cnorm = norm_nonrad

        self_terms_pE = torch.zeros(
            (len(self.positions), 3, 3), dtype=DTYPE_COMPLEX, device=self.device
        )
        self_terms_pE[:, 0, 0] = cnorm
        self_terms_pE[:, 1, 1] = cnorm
        self_terms_pE[:, 2, 2] = cnorm

        return self_terms_pE

    def get_selfterm_mE(self, wavelength: float, environment) -> torch.Tensor:
        return self.zeros

    def get_selfterm_pH(self, wavelength: float, environment) -> torch.Tensor:
        return self.zeros

    def get_selfterm_mH(self, wavelength: float, environment) -> torch.Tensor:
        return self.zeros

    # --- polarizabilities
    def get_polarizability_pE(self, wavelength: float, environment) -> torch.Tensor:
        """return list of EE polarizability tensors (3x3) at each meshpoint

        Args:
            wavelength (float): in nm
            environment (environment class): 3D environement class

        Returns:
            torch.Tensor: pE polarizability tensor
        """
        eps_env = environment.get_environment_permittivity_scalar(
            wavelength, r_probe=self.positions
        )
        eps_env_tensor = torch.zeros(
            (len(self.positions), 3, 3), dtype=DTYPE_COMPLEX, device=self.device
        )
        eps_env_tensor[:, 0, 0] = eps_env
        eps_env_tensor[:, 1, 1] = eps_env
        eps_env_tensor[:, 2, 2] = eps_env

        eps_geo = torch.zeros(
            (len(self.positions), 3, 3), dtype=DTYPE_COMPLEX, device=self.device
        )
        for i, mat in enumerate(self.materials):
            eps_geo[i] = mat.get_epsilon(wavelength)

        vcell_norm = self.step**3 / self.mesh_normalization_factor

        ## --- isotropic polarizability
        alpha_pE = (
            (eps_geo - eps_env_tensor)
            * vcell_norm.unsqueeze(1).unsqueeze(1)
            / (4.0 * torch.pi)
        )

        # with radiative reaction term:
        if self.radiative_correction:
            k0 = 2 * torch.pi / wavelength
            alpha_pE = alpha_pE / (1 - (1j * k0**3 * (2 / 3)) * alpha_pE)

        return alpha_pE

    def get_polarizability_mE(self, wavelength: float, environment) -> torch.Tensor:
        return self.zeros

    def get_polarizability_pH(self, wavelength: float, environment) -> torch.Tensor:
        return self.zeros

    def get_polarizability_mH(self, wavelength: float, environment) -> torch.Tensor:
        return self.zeros

    # --- plotting
    def plot(
        self,
        projection="auto",
        scale=1.0,
        color="auto",
        show_grid=True,
        legend=True,
        set_ax_aspect=True,
        alpha=1.0,
        reset_color_cycle=True,
        **kwargs,
    ):
        """plot the structure (2D)

        Args:
            projection (str, optional): Cartesian projection. Default: "XY" or plane in which all dipoles lie. Defaults to "auto".
            scale (float, optional): scaling factor of the grid cells, if shown. Defaults to 1.0.
            color (str, optional): plot color. Defaults to "auto".
            show_grid (bool, optional): whether to show mesh grid (if available in structure). Defaults to True.
            legend (bool, optional): show legend. Defaults to True.
            set_ax_aspect (bool, optional): automatically set aspect ratio to equal. Defaults to True.
            alpha (int, optional): optional transparency. Defaults to 1.
            reset_color_cycle (bool, optional): reset color cycle after finishing the plot. Defaults to True.

        Returns:
            matplotlib axes
        """
        from torchgdm.visu import visu2d

        im = visu2d.geo2d._plot_structure_discretized(
            self,
            projection=projection,
            scale=scale,
            color=color,
            show_grid=show_grid,
            legend=legend,
            set_ax_aspect=set_ax_aspect,
            alpha=alpha,
            reset_color_cycle=reset_color_cycle,
            **kwargs,
        )
        return im

    def plot_contour(
        self,
        projection="auto",
        color="auto",
        set_ax_aspect=True,
        alpha=1.0,
        alpha_value=None,
        reset_color_cycle=True,
        **kwargs,
    ):
        """plot the contour around the structure (2D)

        Args:
            projection (str, optional): which cartesian plane to project onto. Defaults to "auto".
            color (str, optional): optional matplotlib compatible color. Defaults to "auto".
            set_ax_aspect (bool, optional): If True, will set aspect of plot to equal. Defaults to True.
            alpha (float, optional): matplotlib transparency value. Defaults to 1.0.
            alpha_value (float, optional): alphashape value. If `None`, try to automatically optimize for best enclosing of structure. Defaults to None.
            reset_color_cycle (bool, optional): reset color cycle after finishing the plot. Defaults to True.

        Returns:
            matplotlib line: matplotlib's `scatter` output
        """
        from torchgdm.visu import visu2d

        im = visu2d.geo2d.contour(
            self,
            projection=projection,
            color=color,
            set_ax_aspect=set_ax_aspect,
            alpha=alpha,
            alpha_value=alpha_value,
            reset_color_cycle=reset_color_cycle,
            **kwargs,
        )
        return im

    def plot3d(self, **kwargs):
        """plot the structure (3D)"""
        from torchgdm.visu import visu3d

        return visu3d.geo3d._plot_structure_discretized(self, **kwargs)

    # --- geometry operations
    def rotate(self, alpha, center=torch.as_tensor([0.0, 0.0, 0.0]), axis="z"):
        """rotate the structure

        Args:
            alpha (float): rotation angle (in rad)
            center (torch.Tensor, optional): center of rotation axis. Defaults to torch.as_tensor([0.0, 0.0, 0.0]).
            axis (str, optional): rotation axis, one of ['x', 'y', 'z']. Defaults to 'z'.

        Raises:
            ValueError: unknown rotation axis

        Returns:
            :class:`StructDiscretized3D`: copy of structure with rotated geometry
        """
        _struct_rotated = self.copy()
        center = center.to(dtype=DTYPE_FLOAT, device=self.device)

        if axis.lower() == "x":
            rot = rotation_x(alpha, device=self.device)
        elif axis.lower() == "y":
            rot = rotation_y(alpha, device=self.device)
        elif axis.lower() == "z":
            rot = rotation_z(alpha, device=self.device)
        else:
            raise ValueError("Unknown rotation axis ''.".format(axis))

        if len(_struct_rotated.positions) > 1:
            _struct_rotated.positions = torch.matmul(
                _struct_rotated.positions - (center + self.r0), rot
            ) + (center + self.r0)
        else:
            warnings.warn("Single meshpoint found, ignore rotation.")

        _struct_rotated.r0 = _struct_rotated.get_center_of_mass()
        return _struct_rotated

    # --- effective model extraction wrapper
    def convert_to_effective_polarizability_pair(
        self,
        wavelengths: torch.Tensor,
        environment=None,
        test_accuracy: bool = False,
        only_pE_mH: bool = True,
        residual_warning_threshold=0.25,
        batch_size=16,
        **kwargs,
    ):
        """convert the structure to an effective point polarizability structure model

        The model consists of a pair of electric and magnetic dipole.

        kwargs are passed to :func:`extract_effective_polarizability`

        Args:
            wavelengths (torch.Tensor): list of wavelengths to extract the model at. in nm
            environment (environment class): 3D environement class. Defaults to None (vacuum).
            test_accuracy (bool, optional): Whether to test accuracy in a scattering simulation. Defaults to False.
            only_pE_mH (bool, optional): whether to extract only a p/m model (True) or a full (6x6) polarizability (False). Defaults to True.
            residual_warning_threshold (float, optional). Maximum residual L2 norm before triggering a warning. Defaults to 0.25.

        Returns:
            :class:`torchgdm.struct.StructEffPola3D`: Effective dipole-pair model
        """
        from torchgdm.struct import StructEffPola3D
        from torchgdm.struct.eff_model_tools import extract_eff_pola_via_exact_mp_3d
        from torchgdm.struct.eff_model_tools import _test_effective_model_accuracy

        wavelengths = torch.as_tensor(
            wavelengths, dtype=DTYPE_FLOAT, device=self.device
        )
        wavelengths = torch.atleast_1d(wavelengths)

        alpha = extract_eff_pola_via_exact_mp_3d(
            struct=self,
            wavelengths=wavelengths,
            environment=environment,
            only_pE_mH=only_pE_mH,
            batch_size=batch_size,
            residual_warning_threshold=residual_warning_threshold,
            **kwargs,
        )

        struct_aeff = StructEffPola3D(
            positions=torch.stack([self.r0]),
            alpha_dicts=[alpha],
            device=self.device,
        )

        # perform a test in an actual scattering simulation
        if test_accuracy:
            _test_results = _test_effective_model_accuracy(struct_aeff, self)

        return struct_aeff

    def convert_to_gpm(
        self,
        wavelengths,
        r_gpm,
        skeletonize=False,
        r_probe=None,
        illumination_list=None,
        environment=None,
        probe_type="particle",
        n_probe=1500,
        probe_spacing=3.0,
        n_planewave_sources=5,
        dipole_source_type="particle",
        n_dipole_sources=60,
        dipole_sources_spacing=5.0,
        verbose=True,
        progress_bar=True,
        device=None,
        residual_warning_threshold=0.1,
        test_accuracy=False,
        **kwargs,
    ):
        """convert the structure to a global polarizability matrix (GPM)

        Extract the GPM in a given `environement` at `wavelengths`.
        This is done in 3 steps:

            1) Illuminate with various sources, calculated scattered fields at
            various probe positions
            2) The effective dipole moment for each GPM dipole is obtained
            via matching of their emission and the probe fields of (1).
            3) A second inverse problem of adjusting the GPM to create the dipoles
            moments found in (2) is solved via pseudoinverse.

        By default, use a mix of plane waves and local dipole sources (different incidence directions, polarizations, locations, orientations).

        Args:
            struct (class:`StructDiscretized3D`): the discretized structure to extract the model for.
            wavelengths (torch.Tensor): list of wavelengths to extract the model at. in nm.
            r_gpm (int or torch.Tensor): Either int: number of positions or a torch.Tensor of shape (N, 3), giving the locations where to place effective dipole pairs.
            skeletonize (bool, optional): Has effect only if `r_gpm` is of type int. If True, perform a skeletonization prior clustering. Defaults to True.
            r_probe (torch.Tensor): probe positions where the simulated and the GPM scattered fields are matched. Overrides all other probe-related configurations. If not given, use automatic probe positions, which may not be optimal. Defaults to None (automatic).
            illumination_list (list of illuminations): List of torchgdm illumination fields to use for extraction. If not given, use automatic illumination fields, which may not be optimal. Defaults to None (automatic).
            environment (environment class): 3D environement class. Defaults to None (vacuum).
            probe_type (str, optional): Where to probe, one of ["particle", "sphere"]. "particle": probe at fixed distance to particle surface. "sphere": probe on enclosing sphere surface. Defaults to "particle".
            n_probe (int, optional): maximum number of probe positions on enclosing sphere. Defaults to 1500.
            probe_spacing (float, optional): additional distance to particle or to enclsing sphere surface, in units of discretization step. Defaults to 3.0.
            n_planewave_sources (int, optional): number of plane wave angles to use as illumination. Defaults to 7.
            dipole_source_type (str, optional): Where to put sources, one of ["particle", "sphere"]. "particle": probe at fixed distance to particle surface. "sphere": probe on enclosing sphere surface. Defaults to "particle".
            n_dipole_sources (int, optional): If given, use `n` dipole sources as illumination instead of plane waves. Defaults to None.
            dipole_sources_spacing (float, optional): if using dipole light sources, additional distance to enclosing sphere surface, in units of discretization step. Defaults to 5.0.
            verbose (bool, optional): whether to sprint progess info. Defaults to True.
            progress_bar (bool, optional): whether to show a progress bar. Defaults to True.
            device (str, optional). Defaults to None, in which case the structure's device is used.
            residual_warning_threshold (float, optional). Maximum residual L2 norm before triggering a warning. Defaults to 0.1.
            test_accuracy (bool, optional): Whether to test accuracy in a scattering simulation. Defaults to False.

        Returns:
            :class:`torchgdm.struct.struct3d.gpm.StructGPM3D`: Effective dipole-pair model
        """
        from torchgdm.struct.struct3d.gpm3d import StructGPM3D
        from torchgdm.struct.eff_model_tools import extract_gpm_from_struct
        from torchgdm.struct.eff_model_tools import _test_effective_model_accuracy

        wavelengths = torch.as_tensor(
            wavelengths, dtype=DTYPE_FLOAT, device=self.device
        )
        wavelengths = torch.atleast_1d(wavelengths)

        gpm_dict = extract_gpm_from_struct(
            struct=self,
            wavelengths=wavelengths,
            r_gpm=r_gpm,
            skeletonize=skeletonize,
            r_probe=r_probe,
            illumination_list=illumination_list,
            environment=environment,
            probe_type=probe_type,
            n_probe=n_probe,
            probe_spacing=probe_spacing,
            n_planewave_sources=n_planewave_sources,
            dipole_source_type=dipole_source_type,
            n_dipole_sources=n_dipole_sources,
            dipole_sources_spacing=dipole_sources_spacing,
            verbose=verbose,
            progress_bar=progress_bar,
            device=device,
            residual_warning_threshold=residual_warning_threshold,
            **kwargs,
        )

        struct_gpm = StructGPM3D(
            positions=self.r0,
            gpm_dicts=gpm_dict,
            device=self.device,
            progress_bar=progress_bar,
        )

        # perform a test in an actual scattering simulation
        if test_accuracy:
            _test_results = _test_effective_model_accuracy(
                struct_gpm, self, which=["ecs", "nf_sca"]
            )

        return struct_gpm


class StructDiscretizedCubic3D(StructDiscretized3D):
    """class for cubic volume discretized structure

    Defines the cubic volume discretization, polarizabilities and self-terms
    """

    __name__ = "3D cubic discretized structure class"

    def __init__(
        self,
        discretization_config,
        step,
        materials,
        device: torch.device = None,
        **kwargs,
    ):
        """3D structure, discretized on a cubic lattice

        Args:
            discretization_config (tuple): tuple of discretization condition function, and discretizer walk limits (as provided by the geometries generators)
            step (float, optional): nominal stepsize. If not provided, infer automatically from geometry. Defaults to None.
            materials (material class, or list of them): material of structure. If list, define the material of each meshpoint.
            device (torch.device, optional): Defaults to "cpu" (can be changed by :func:`torchgdm.use_cuda`).

        Raises:
            ValueError: Invalid material config
        """
        from torchgdm.struct.struct3d import discretizer_cubic

        positions = discretizer_cubic(*discretization_config, step=step)

        super().__init__(
            positions,
            materials,
            step=step,
            device=device,
            on_distance_violation="ignore",  # trust the discretizer --> speedup
            **kwargs,
        )

        self.mesh = "cubic"
        self.mesh_normalization_factor = torch.tensor(
            1.0, dtype=DTYPE_FLOAT, device=self.device
        )


class StructDiscretizedHexagonal3D(StructDiscretized3D):
    """class for hexagonal compact volume discretized structure

    Defines the hexagonal compact volume discretization, polarizabilities and self-terms
    """

    __name__ = "3D hexagonal compact discretized structure class"

    def __init__(
        self,
        discretization_config,
        step,
        materials,
        device: torch.device = None,
        **kwargs,
    ):
        """3D structure, discretized on a hexagonal compact lattice

        Args:
            discretization_config (tuple): tuple of discretization condition function, and discretizer walk limits (as provided by the geometries generators)
            step (float, optional): nominal stepsize. If not provided, infer automatically from geometry. Defaults to None.
            materials (material class, or list of them): material of structure. If list, define the material of each meshpoint.
            device (torch.device, optional): Defaults to "cpu" (can be changed by :func:`torchgdm.use_cuda`).

        Raises:
            ValueError: Invalid material config
        """
        from torchgdm.struct.struct3d import discretizer_hexagonalcompact

        positions = discretizer_hexagonalcompact(*discretization_config, step=step)

        super().__init__(
            positions,
            materials,
            step=step,
            device=device,
            on_distance_violation="ignore",  # trust the discretizer --> speedup
            **kwargs,
        )

        self.mesh = "hexagonal"
        self.mesh_normalization_factor = torch.sqrt(
            torch.as_tensor(2.0, dtype=DTYPE_FLOAT, device=self.device)
        )
