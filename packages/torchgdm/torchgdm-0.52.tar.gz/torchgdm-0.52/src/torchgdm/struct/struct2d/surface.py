# -*- coding: utf-8 -*-
"""2D surface discretization structure classes"""
import warnings

import torch

from torchgdm.constants import (
    DTYPE_FLOAT,
    DTYPE_COMPLEX,
    COLORS_DEFAULT,
)
from torchgdm.tools.misc import get_default_device
from torchgdm.struct.base_classes import StructBase
from torchgdm.tools.geometry import get_step_from_geometry
from torchgdm.tools.geometry import rotation_y
from torchgdm.tools.misc import ptp


class StructDiscretized2D(StructBase):
    """base class 2D surface discretized structure (infinite y axis)

    Using a list of positions in the XZ-plane and materials,
    this class defines the basic 2D surface discretization, the
    polarizabilities and self-terms
    """

    __name__ = "2D discretized structure"

    def __init__(
        self,
        positions: torch.Tensor,
        materials,
        step=None,
        on_distance_violation: str = "warn",
        radiative_correction: bool = False,
        device: torch.device = None,
        **kwargs,
    ):
        """2D discretized structure

        Args:
            positions (torch.Tensor): meshpoint positions (3D, but all y values must be zero)
            materials (material class, or list of them): material of structure. If list, define the material of each meshpoint.
            step (float, optional): nominal stepsize. If not provided, infer automatically from geometry. Defaults to None.
            on_distance_violation (str, optional): behavior on distance violation. can be "error", "warn", None (silent), or "ignore" (do nothing, keep invalid meshpoints). Defaults to "error".
            radiative_correction (bool, optional): Whether to add raditative correction for cross section calculations. Defaults to False.
            device (torch.device, optional): Defaults to "cpu" (can be changed by :func:`torchgdm.use_cuda`).

        Raises:
            ValueError: No mesh points at y=0, Invalid material config
        """
        super().__init__(device=device, **kwargs)
        self.mesh = "2D"
        self.n_dim = 2

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

        if torch.count_nonzero(self.positions[..., 1]) > 0:
            warnings.warn("require 2D structure. Remove all positions with y!=0.")
            self.positions = self.positions[self.positions[..., 1] != 0]
            if len(self.positions) == 0:
                raise ValueError("No mesh positions at y=0. Please check geometry.")

        self.r0 = self.get_center_of_mass()  # center of gravity

        if step is None:
            step_scalar = get_step_from_geometry(self.positions)
        else:
            step_scalar = step

        # step for every meshcell, for consistency with other struct classes
        self.step = step_scalar * torch.ones(
            len(self.positions), dtype=DTYPE_FLOAT, device=self.device
        )

        self.radiative_correction = radiative_correction
        self.mesh_normalization_factor = torch.as_tensor(
            1, dtype=DTYPE_FLOAT, device=self.device
        )  # square mesh

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
        self.interaction_type = "E"  # possible types "E" or "EH"

    def __repr__(self, verbose=False):
        """description about structure"""
        out_str = ""
        out_str += "------ discretized 2D nano-object -------"
        out_str += "\n" + " mesh type:              {}".format(self.mesh)
        out_str += "\n" + " nr. of meshpoints:      {}".format(len(self.positions))
        out_str += "\n" + " nominal stepsizes (nm): {}".format(
            [float(f) for f in torch.unique(self.step)]
        )
        out_str += "\n" + " material:               {}".format(
            [m.__name__ for m in set(self.materials)]
        )
        bnds = ptp(self.positions, dim=0)
        out_str += "\n" + " size & position (Y-axis is infinite):"
        out_str += "\n" + "     X-extension          :   {:.1f} (nm)".format(bnds[0])
        out_str += "\n" + "     Z-extension          :   {:.1f} (nm)".format(bnds[2])
        out_str += "\n" + "     center of mass (x,z) : ({:.1f}, {:.1f})".format(
            self.r0[0], self.r0[2]
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
            environment (environment class): 2D environement class

        Returns:
            torch.Tensor: pE self term tensor
        """
        eps_env = environment.get_environment_permittivity_scalar(
            wavelength, r_probe=self.positions
        )
        # cast env permittivity to real, because hankel only support real args
        eps_env = torch.as_tensor(eps_env, dtype=DTYPE_COMPLEX, device=self.device).real

        k0 = 2 * torch.pi / wavelength
        k02 = k0**2

        if self.mesh_normalization_factor == 0:
            norm_xz = 0
            norm_y = 0
        else:
            from torchgdm.tools.special import H1n

            S = self.step**2
            k0_y = environment.get_k0_y(wavelength)

            kr2 = torch.as_tensor(
                eps_env * k02 - k0_y**2, dtype=DTYPE_FLOAT, device=self.device
            )
            kr = torch.sqrt(kr2)

            h11 = H1n(1, kr * self.step / torch.pi**0.5)
            norm01 = self.step / torch.pi**0.5 * h11 / kr + 2j / (torch.pi * kr**2)

            norm_xz_nonrad = -1 * self.mesh_normalization_factor / (2.0 * S * eps_env)
            norm_xz_rad = 1j * torch.pi * (2 * k02 - kr2 / eps_env) * norm01 / (4 * S)

            norm_y_nonrad = 0
            norm_y_rad = 1j * torch.pi * (k02 - k0_y**2 / eps_env) * norm01 / (2 * S)

            norm_xz = 4.0 * torch.pi * (norm_xz_nonrad + norm_xz_rad)
            norm_y = 4.0 * torch.pi * (norm_y_nonrad + norm_y_rad)

        self_terms_pE = torch.zeros(
            (len(self.positions), 3, 3), dtype=DTYPE_COMPLEX, device=self.device
        )
        self_terms_pE[:, 0, 0] = norm_xz
        self_terms_pE[:, 1, 1] = norm_y
        self_terms_pE[:, 2, 2] = norm_xz

        return self_terms_pE

    # --- polarizabilities
    def get_polarizability_pE(self, wavelength: float, environment) -> torch.Tensor:
        """return list of EE polarizability tensors (3x3) at each meshpoint

        Args:
            wavelength (float): in nm
            environment (environment class): 2D environement class

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

        S_cell_norm = self.step**2 / float(self.mesh_normalization_factor)

        # --- polarizability
        alpha_pE = (
            (eps_geo - eps_env_tensor)
            * S_cell_norm.unsqueeze(1).unsqueeze(1)
            / (4.0 * torch.pi)
        )

        return alpha_pE

    # - radiative correction for cross section calc. - 2D case
    def get_radiative_correction_prefactor_p(self, wavelength: float, environment):
        """return electric dipole radiative correction prefactor vectors (3) at each meshpoint"""
        if self.radiative_correction:
            k0 = 2 * torch.pi / wavelength

            pf_vec = torch.as_tensor(
                [1.0, 2.0, 1.0], device=self.device, dtype=DTYPE_COMPLEX
            )
            pf_vec = pf_vec * torch.pi / 2 * k0**2

            return torch.ones(
                (len(self.get_all_positions()), 3),
                device=self.device,
                dtype=DTYPE_COMPLEX,
            ) * pf_vec.unsqueeze(0)
        else:
            return torch.zeros(
                (len(self.get_all_positions()), 3),
                device=self.device,
                dtype=DTYPE_COMPLEX,
            )

    def get_radiative_correction_prefactor_m(self, wavelength: float, environment):
        """return magnetic dipole radiative correction prefactor vectors (3) at each meshpoint"""
        if self.radiative_correction:
            k0 = 2 * torch.pi / wavelength
            n_env = (
                environment.get_environment_permittivity_scalar(
                    wavelength, self.get_all_positions()
                )
                ** 0.5
            )
            pf_vec = torch.as_tensor(
                [1.0, 2.0, 1.0], device=self.device, dtype=DTYPE_COMPLEX
            )
            pf_vec = pf_vec * torch.pi / 2 * k0**2

            return (
                torch.ones(
                    (len(self.get_all_positions()), 3),
                    device=self.device,
                    dtype=DTYPE_COMPLEX,
                )
                * pf_vec.unsqueeze(0)
                * n_env.unsqueeze(1) ** 2
            )
        else:
            return torch.zeros(
                (len(self.get_all_positions()), 3),
                device=self.device,
                dtype=DTYPE_COMPLEX,
            )

    # --- plotting
    def plot(self, **kwargs):
        """plot the structure in XZ plane (2D)"""
        from torchgdm.visu import visu2d

        kwargs["projection"] = "xz"
        im = visu2d.geo2d._plot_structure_discretized(self, **kwargs)
        return im

    def plot_contour(self, **kwargs):
        """plot the structure contour in XZ plane (2D)"""
        from torchgdm.visu import visu2d

        kwargs["projection"] = "xz"
        im = visu2d.geo2d._plot_contour_discretized(self, **kwargs)
        return im

    def plot3d(self, **kwargs):
        """plot the structure in 3D"""
        from torchgdm.visu import visu3d

        return visu3d.geo3d._plot_structure_discretized(self, **kwargs)

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
        _struct_rotated = self.copy()
        center = center.to(dtype=DTYPE_FLOAT, device=self.device)

        if axis.lower() == "y":
            rot = rotation_y(alpha, device=self.device)
        else:
            raise ValueError(
                "Only rotation axis 'y' supported in 2D (infinite axis).".format(axis)
            )

        if len(_struct_rotated.positions) > 1:
            _struct_rotated.positions = torch.matmul(
                _struct_rotated.positions - (center + self.r0), rot
            ) + (center + self.r0)
        else:
            warnings.warn("Single meshpoint found, ignore rotation.")

        return _struct_rotated

    # --- effective model extraction wrapper
    def convert_to_effective_polarizability_pair(
        self, wavelengths, environment=None, test_accuracy=False, **kwargs
    ):
        from torchgdm.struct.struct2d import StructEffPola2D

        # from torchgdm.struct.struct2d.line import extract_eff_pola_2d
        from torchgdm.struct.eff_model_tools import extract_eff_pola_2d
        from torchgdm.struct.eff_model_tools import _test_effective_model_accuracy

        warnings.warn(
            "2D effective polarizabilities only implemented for illumination incidence in XZ plane!"
        )
        wavelengths = torch.as_tensor(
            wavelengths, dtype=DTYPE_FLOAT, device=self.device
        )
        wavelengths = torch.atleast_1d(wavelengths)

        alpha = extract_eff_pola_2d(
            struct=self, wavelengths=wavelengths, environment=environment, **kwargs
        )
        struct_aeff = StructEffPola2D(
            positions=torch.stack([self.r0]),
            alpha_dicts=[alpha],
            device=self.device,
        )

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
        probe_spacing=5.0,
        n_planewave_sources=5,
        dipole_source_type="particle",
        n_dipole_sources=60,
        dipole_sources_spacing=6.0,
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
            skeletonize (bool, optional): Has effect only if `r_gpm` is of type int. If True, perform a skeletonization prior clustering. Defaults to False.
            r_probe (torch.Tensor): probe positions where the simulated and the GPM scattered fields are matched. Overrides all other probe-related configurations. If not given, use automatic probe positions, which may not be optimal. Defaults to None (automatic).
            illumination_list (list of illuminations): List of torchgdm illumination fields to use for extraction. If not given, use automatic illumination fields, which may not be optimal. Defaults to None (automatic).
            environment (environment class): 3D environement class. Defaults to None (vacuum).
            probe_type (str, optional): Where to probe, one of ["particle", "circle"]. "particle": probe at fixed distance to particle surface. "circle": probe on enclosing circle surface. Defaults to "particle".
            n_probe (int, optional): maximum number of probe positions on enclosing circle. Defaults to 1500.
            probe_spacing (float, optional): additional distance to particle or to enclsing circle surface, in units of discretization step. Defaults to 5.0.
            n_planewave_sources (int, optional): number of plane wave angles to use as illumination. Defaults to 7.
            dipole_source_type (str, optional): Where to put sources, one of ["particle", "circle"]. "particle": probe at fixed distance to particle surface. "circle": sources on enclosing circle. Defaults to "particle".
            n_dipole_sources (int, optional): If given, use `n` dipole sources as illumination instead of plane waves. Defaults to None.
            dipole_sources_spacing (float, optional): if using dipole light sources, additional distance to enclosing circle surface, in units of discretization step. Defaults to  6.0.
            verbose (bool, optional): whether to sprint progess info. Defaults to True.
            progress_bar (bool, optional): whether to show a progress bar. Defaults to True.
            device (str, optional). Defaults to None, in which case the structure's device is used.
            residual_warning_threshold (float, optional). Maximum residual L2 norm before triggering a warning. Defaults to 0.1.

            Returns:
                :class:`torchgdm.struct.struct3d.gpm.StructGPM3D`: Effective dipole-pair model
        """
        from torchgdm.struct.struct2d.gpm2d import StructGPM2D
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

        struct_gpm = StructGPM2D(
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


class StructDiscretizedSquare2D(StructDiscretized2D):
    """class for square surface discretized, infinitely long 2D structure

    Defines the square surface discretization, polarizabilities and self-terms
    """

    __name__ = "2D square lattice discretized structure class"

    def __init__(
        self,
        discretization_config,
        step,
        materials,
        device: torch.device = None,
        **kwargs,
    ):
        """2D structure, discretized on a square lattice

        Infinite axis along Y

        Args:
            discretization_config (tuple): tuple of discretization condition function, and discretizer walk limits (as provided by the geometries generators)
            step (float, optional): nominal stepsize. If not provided, infer automatically from geometry. Defaults to None.
            materials (material class, or list of them): material of structure. If list, define the material of each meshpoint.
            device (torch.device, optional): Defaults to "cpu" (can be changed by :func:`torchgdm.use_cuda`).

        Raises:
            ValueError: No mesh points at y=0, Invalid material config
        """
        from torchgdm.struct.struct2d import discretizer_square

        positions = discretizer_square(*discretization_config, step=step)

        super().__init__(
            positions,
            materials,
            step=step,
            device=device,
            on_distance_violation="ignore",  # trust the discretizer --> speedup
            **kwargs,
        )

        self.mesh = "square (2D)"
        self.mesh_normalization_factor = torch.tensor(
            1.0, dtype=DTYPE_FLOAT, device=self.device
        )
