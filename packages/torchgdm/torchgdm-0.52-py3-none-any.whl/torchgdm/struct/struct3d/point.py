# -*- coding: utf-8 -*-
"""point polarizability classes"""
import warnings
import copy

import torch

from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX
from torchgdm.tools.misc import get_default_device
from torchgdm.struct.base_classes import StructBase
from torchgdm.tools import interp
from torchgdm.tools.geometry import rotation_x, rotation_y, rotation_z
from torchgdm.tools.geometry import test_structure_distances
from torchgdm.tools.geometry import get_enclosing_sphere_radius
from torchgdm.tools.geometry import sample_random_spherical
from torchgdm.tools.misc import ptp


# --- base class volume discretized structure container - 3D
class StructEffPola3D(StructBase):
    """3D point polarizability structure

    Defines a basic effective polarizability based structure
    """

    __name__ = "effective point polarizability (3D) structure class"

    def __init__(
        self,
        positions: torch.Tensor,
        alpha_dicts: list,
        radiative_correction: bool = True,
        device: torch.device = None,
        environment=None,
        shift_z_to_r0: bool = True,
    ):
        """3D point polarizability class

        The main information is provided in the `alpha_dicts`, which is a list of dicts with the full effective polarizability definitions. Each dict defines one structure and must contain following:
            - 'wavelengths': wavelengths at which the polarizabilities are calculated
            - 'alpha_6x6':
                6x6 polarizability tensors of shape [len(wavelengths),6,6]. Coupling terms:
                    - pE: [:, :3, :3]
                    - mH: [:, 3:, 3:]
                    - mE: [:, 3:, :3]
                    - pH: [:, :3, 3:]
            optional keys:
            - 'full_geometry': the original volume discretization of the represented geometry
            - 'r0': the origin of the effective polarizabilities with respect to optional 'full_geometry'
            - 'enclosing_radius': enclosing radius of the original structure

        Args:
            positions (torch.Tensor): polarizability positions
            alpha_dicts (list): list of polarizability model dictionaries
            radiative_correction (bool, optional): Whether to add raditative correction for cross section calculations. Defaults to True.
            device (torch.device, optional): Defaults to "cpu".
            environment (environment instance, optional): 3D environment class. By default use environment defined in eff.pola. dictionary. Defaults to None.
            shift_z_to_r0 (bool, optional): If True, if a position z-value is zero, each polarizability model's z position will be shifted to the height of the effective dipole development center. Defaults to True.

        Raises:
            ValueError: _description_
        """
        super().__init__(device=device)
        self.n_dim = 3

        # expand positions, put single scatterer in list
        self.positions = torch.as_tensor(
            positions, dtype=DTYPE_FLOAT, device=self.device
        )
        if len(self.positions.shape) == 1:
            self.positions = self.positions.unsqueeze(0)
        assert self.positions.shape[1] == 3

        self.radiative_correction = radiative_correction

        # single alpha_dict: put in list
        if type(alpha_dicts) == dict:
            alpha_dicts = [alpha_dicts] * len(self.positions)
        assert type(alpha_dicts[0]) == dict

        # environment at which alpha has been extracted (if given):
        if environment is None:
            self.environment = alpha_dicts[0]["environment"]
        else:
            warnings.warn(
                "Using different environment than specified in eff.pola-dict."
            )
            self.environment = environment

        for _adict in alpha_dicts:
            assert "wavelengths" in _adict
            if "alpha_6x6" not in _adict:
                raise ValueError(
                    "Polarizability-description dicts must contain polarizaility tensors "
                    + "under the dict key: 'alpha_6x6'."
                )

        # use first pola-tensor wavelength range
        wavelengths = alpha_dicts[0]["wavelengths"]
        self.wavelengths_data = torch.as_tensor(
            wavelengths, dtype=DTYPE_FLOAT, device=self.device
        )

        for _adict in alpha_dicts:
            _wls = torch.as_tensor(
                _adict["wavelengths"], dtype=DTYPE_FLOAT, device=self.device
            )
            if not torch.all(torch.isin(self.wavelengths_data, _wls)):
                warnings.warn(
                    "Pre-calculated wavelengths for the structures are not identical. "
                    + "Try to use linear interpolation to fill missing values. "
                    + "This may be inaccurate."
                )
            if (torch.min(_wls) > torch.min(self.wavelengths_data)) or (
                torch.max(_wls) < torch.max(self.wavelengths_data)
            ):
                raise ValueError(
                    "Interpolation not possible. Pre-calculated wavelengths of the structures "
                    + "must be within the same range to allow interpolation."
                )

        # optionally shift z such that 'bottom' is at z=0. Do only if z=0
        if shift_z_to_r0:
            for i, p in enumerate(self.positions):
                if p[2] == 0:
                    p[2] = torch.as_tensor(
                        alpha_dicts[i]["r0"][2], dtype=p.dtype, device=p.device
                    )

        # populate polarizability tensors database for each position at
        # pre-calculated wavelengths. if necessary, interpolate between data points
        alpha_data = []
        enclosing_radius = []
        full_geometries = []
        for i, _adict in enumerate(alpha_dicts):
            alpha_data.append(
                self._interpolate_single_alpha(
                    wls=self.wavelengths_data,
                    a_data=_adict["alpha_6x6"],
                    wl_data=_adict["wavelengths"],
                )
            )

            # optional values
            if "full_geometry" in _adict:
                full_geometries.append(
                    torch.as_tensor(
                        _adict["full_geometry"] - _adict["r0"],
                        dtype=DTYPE_FLOAT,
                        device=self.device,
                    )
                    + self.positions[i]
                )

            if "enclosing_radius" in _adict:
                enclosing_radius.append(_adict["enclosing_radius"] * 2)
            else:
                if "full_geometry" in _adict:
                    _r_eff = get_enclosing_sphere_radius(full_geometries[-1])
                    enclosing_radius.append(_r_eff)
                else:
                    enclosing_radius.append(0)

        self.full_geometries = full_geometries

        # define zeros for later reuse
        self.zeros_spectral = torch.zeros(
            (len(self.positions), len(self.wavelengths_data), 6, 6),
            dtype=DTYPE_COMPLEX,
            device=self.device,
        )

        # effective polarizabilities of each meshpoint at each wavelength: shape (Npos, Nwl, 6, 6)
        if len(alpha_data) != 0:
            self.alpha_data = torch.stack(alpha_data)
        else:
            self.alpha_data = self.zeros_spectral

        # case of a single point-polarizability: expand dimensions
        if len(self.alpha_data.shape) == 3:
            self.alpha_data = self.alpha_data.unsqueeze(0)

        # selfterms are zero.
        self.selfterms_data = self.zeros_spectral

        # populate lookup tables
        self.create_lookup()

        # other parameters ("step" corresponds to the effective diameter)
        self.step = torch.as_tensor(
            enclosing_radius, dtype=DTYPE_FLOAT, device=self.device
        )

        # center of gravity of ensemble of all points
        self.r0 = self.get_center_of_mass()

        # verify dimensions
        if self.alpha_data.shape != self.zeros_spectral.shape:
            raise ValueError(
                "Wrong shape of a polarizability tensor list. "
                + "Needs to be (N_dipoles, N_wavelengths, 6, 6)."
            )

        # effective EE / HH polarizabilities
        self.interaction_type = "EH"

    def __repr__(self, verbose=False):
        """description about structure"""
        out_str = ""
        out_str += "------ 3D effective ED / MD polarizability nano-object -------"
        out_str += "\n" + " nr. of dipole-pairs:    {}".format(
            len(self.get_all_positions())
        )
        out_str += "\n" + " nominal enclosing sphere diameters (nm): {}".format(
            [round(float(f), 1) for f in torch.unique(self.step)]
        )
        if len(self.full_geometries) > 0:
            pos = torch.cat(self.full_geometries)
            out_str += "\n" + " original geometry: "
            out_str += "\n" + "  - replacing nr. of meshpoints: {}".format(len(pos))
            bnds = ptp(pos, dim=0)
            out_str += "\n" + "  - size & position:"
            out_str += "\n" + "        X-extension    :    {:.1f} (nm)".format(bnds[0])
            out_str += "\n" + "        Y-extension    :    {:.1f} (nm)".format(bnds[1])
            out_str += "\n" + "        Z-extension    :    {:.1f} (nm)".format(bnds[2])
            out_str += "\n" + "  - center of mass :    ({:.1f}, {:.1f}, {:.1f})".format(
                *[float(f) for f in self.get_center_of_mass()]
            )

        return out_str

    def create_lookup(self):
        """Create a lookup table for the polarizability tensors"""
        # populate lookup tables with pre-calculated data
        self.lookup = {}
        for i_wl, wl in enumerate(self.wavelengths_data):
            self.lookup[float(wl)] = self.alpha_data[:, i_wl, :, :]

    def set_device(self, device):
        """move all tensors of the class to device"""
        super().set_device(device)
        if self.environment is not None:
            self.environment.set_device(device)

        self.positions = self.positions.to(device)
        if len(self.full_geometries) > 0:
            self.full_geometries = [_g.to(device) for _g in self.full_geometries]

        self.zeros_spectral = self.zeros_spectral.to(device)
        self.step = self.step.to(device)
        self.r0 = self.r0.to(device)
        self.wavelengths_data = self.wavelengths_data.to(device)

        self.alpha_data = self.alpha_data.to(device)
        self.selfterms_data = self.selfterms_data.to(device)

        # transfer the lookup tables
        for wl in self.lookup:
            self.lookup[wl] = self.lookup[wl].to(device)

    # --- dipole moments and their positions (self-consistent within a simulation)
    def get_e_selfconsistent(self, wavelength, **kwargs):
        if float(wavelength) not in self.fields_inside:
            raise ValueError(
                f"Inside field not available at wl={wavelength}nm. "
                + "Run the simulation."
            )
        return self.fields_inside[float(wavelength)].get_efield()

    def get_h_selfconsistent(self, wavelength, **kwargs):
        if float(wavelength) not in self.fields_inside:
            raise ValueError(
                f"Inside field not available at wl={wavelength}nm. "
                + "Run the simulation."
            )
        return self.fields_inside[float(wavelength)].get_hfield()

    def get_e_h_selfconsistent(self, wavelength, **kwargs) -> torch.Tensor:
        e = self.get_e_selfconsistent(wavelength)
        h = self.get_h_selfconsistent(wavelength)
        return torch.cat([e, h], dim=-1)

    def get_r_pm(self):
        """positions of electric and magnetic polarizable dipoles"""
        r_p = self.get_all_positions()
        r_m = self.get_all_positions()
        return r_p, r_m

    def get_pm(self, wavelength):
        """self-consistent electric and magnetic dipole moments"""
        alpha_6x6 = self.get_polarizability_6x6(wavelength, self.environment)
        e_h_in = self.get_e_h_selfconsistent(wavelength)

        p_m = torch.matmul(alpha_6x6, e_h_in.unsqueeze(-1))[..., 0]
        p = p_m[..., :3]
        m = p_m[..., 3:]

        return p, m

    # - polarizability handling
    def _interpolate_single_alpha(self, wls, a_data, wl_data):
        # convert to tensor
        wls = torch.as_tensor(wls, dtype=DTYPE_FLOAT, device=self.device)
        wl_dat = torch.as_tensor(wl_data, dtype=DTYPE_FLOAT, device=self.device)
        a_dat = torch.as_tensor(a_data, dtype=DTYPE_COMPLEX, device=self.device)

        # wavelength-interpolation of each tensor component
        a_ip = torch.zeros((len(wls), 6, 6), dtype=DTYPE_COMPLEX, device=self.device)
        for i in range(6):
            for j in range(6):
                _func_ip = interp.RegularGridInterpolator([wl_dat], a_dat[:, i, j])
                _ip = _func_ip([wls])
                a_ip[:, i, j] = _ip

        return a_ip

    def interpolate_alpha(self, wls, a_data_many, wl_data, lookup=None):
        """interpolate the polarizabilities between available wavelengths"""
        a_ip = torch.zeros(
            (len(a_data_many), len(wls), 6, 6), dtype=DTYPE_COMPLEX, device=self.device
        )

        # iterate all polarizabilities (different structures)
        for i_a, a_data in enumerate(a_data_many):
            _a = self._interpolate_single_alpha(wls, a_data, wl_data)
            a_ip[i_a] = _a

        # optionally add wavelengths to lookup
        if lookup is not None:
            for i_wl, wl in enumerate(wls):
                wl = float(wl)
                if wl not in lookup:
                    lookup[wl] = a_ip[:, i_wl, :, :]

        return a_ip

    # --- self-terms
    # self-terms are zero
    # TODO: Make them user-definable (use same approach as for alpha_XX)

    # --- polarizabilities
    def _call_interpolation(self, wavelength):
        warnings.warn(
            "Interpolating polarizabilities at wavelength {:.3f}.".format(
                float(wavelength)
            )
        )
        self.interpolate_alpha(
            [wavelength],
            self.alpha_data,
            self.wavelengths_data,
            lookup=self.lookup,
        )

    def get_polarizability_pE(self, wavelength: float, environment) -> torch.Tensor:
        """return pE polarizability tensors (3x3) at each position

        Args:
            wavelength (float): in nm
            environment (environment class): 3D environement class

        Returns:
            torch.Tensor: pE polarizability tensor
        """
        if float(wavelength) not in self.lookup:
            self._call_interpolation(wavelength)

        return self.lookup[float(wavelength)][:, :3, :3]

    def get_polarizability_mE(self, wavelength: float, environment) -> torch.Tensor:
        """return mE polarizability tensors (3x3) at each position

        Args:
            wavelength (float): in nm
            environment (environment class): 3D environement class

        Returns:
            torch.Tensor: mE polarizability tensor
        """
        if float(wavelength) not in self.lookup:
            self._call_interpolation(wavelength)

        return self.lookup[float(wavelength)][:, 3:, :3]

    def get_polarizability_pH(self, wavelength: float, environment) -> torch.Tensor:
        """return pH polarizability tensors (3x3) at each position

        Args:
            wavelength (float): in nm
            environment (environment class): 3D environement class

        Returns:
            torch.Tensor: pH polarizability tensor
        """
        if float(wavelength) not in self.lookup:
            self._call_interpolation(wavelength)

        return self.lookup[float(wavelength)][:, :3, 3:]

    def get_polarizability_mH(self, wavelength: float, environment) -> torch.Tensor:
        """return mH polarizability tensors (3x3) at each position

        Args:
            wavelength (float): in nm
            environment (environment class): 3D environement class

        Returns:
            torch.Tensor: mH polarizability tensor
        """
        if float(wavelength) not in self.lookup:
            self._call_interpolation(wavelength)

        return self.lookup[float(wavelength)][:, 3:, 3:]

    # --- plotting
    def plot(
        self,
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
        legend=True,
        set_ax_aspect=True,
        reset_color_cycle=True,
        **kwargs,
    ):
        """plot the point polarizability structure (2D)

        Args:
            projection (str, optional): Cartesian projection. Default: "XY" or plane in which all dipoles lie. Defaults to "auto".
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

        Returns:
            matplotlib axes
        """
        from torchgdm.visu import visu2d

        im = visu2d.geo2d._plot_structure_eff_pola(
            self,
            projection=projection,
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
        """plot the contour of the underlying mesh (2D)

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
        """plot the point polarizability structure (3D)"""
        from torchgdm.visu import visu3d

        return visu3d.geo3d._plot_structure_eff_3dpola(self, **kwargs)

    # --- geometry operations
    def translate(self, vector):
        """return a copy moved by `vector`"""
        vector = torch.as_tensor(vector, dtype=DTYPE_FLOAT, device=self.device)
        vector = torch.atleast_2d(vector)
        _shifted = self.copy()

        _shifted.positions += vector
        _shifted.r0 = _shifted.get_center_of_mass()

        if len(_shifted.full_geometries) > 0:
            for _g in _shifted.full_geometries:
                _g += vector

        return _shifted

    def set_center_of_mass(self, r0_new: torch.Tensor):
        """move center of mass to new position `r0_new` (in-place)"""
        r0_new = torch.as_tensor(r0_new, device=self.device)

        if len(r0_new.shape) != 1:
            if len(r0_new) not in [2, 3]:
                raise ValueError("`r0_new` needs to be (X,Y) or (X,Y,Z) tuple.")
        r0_old = self.get_center_of_mass()

        # treat case r0_new is 2D (X,Y)
        if len(r0_new) == 2:
            r0_new = torch.as_tensor(
                [r0_new[0], r0_new[1], r0_old[2]], device=self.device
            )

        # move to origin, then to new location
        self.positions -= r0_old - r0_new

        if len(self.full_geometries) > 0:
            for _g in self.full_geometries:
                # move to origin, the to new pos.
                _g -= r0_old - r0_new

        self.r0 = self.get_center_of_mass()

    def rotate(self, alpha, center=torch.as_tensor([0.0, 0.0, 0.0]), axis="z"):
        """rotate the structure

        Args:
            alpha (float): rotation angle (in rad)
            center (torch.Tensor, optional): center of rotation axis. Defaults to torch.as_tensor([0.0, 0.0, 0.0]).
            axis (str, optional): rotation axis, one of ['x', 'y', 'z']. Defaults to 'z'.

        Raises:
            ValueError: unknown rotation axis

        Returns:
            :class:`StructEffPola3D`: copy of structure with rotated geometry
        """
        _s_rot = self.copy()
        center = center.to(dtype=DTYPE_FLOAT, device=self.device)

        if axis.lower() == "x":
            rot = rotation_x(alpha, device=self.device)
        elif axis.lower() == "y":
            rot = rotation_y(alpha, device=self.device)
        elif axis.lower() == "z":
            rot = rotation_z(alpha, device=self.device)
        else:
            raise ValueError("Unknown rotation axis ''.".format(axis))

        # rotate positions
        _s_rot.positions = torch.matmul(_s_rot.positions - (center + self.r0), rot) + (
            center + self.r0
        )

        # rotate full discretizations (if available)
        for i_g, _geo in enumerate(_s_rot.full_geometries):
            if len(_geo) > 1:
                _s_rot.full_geometries[i_g] = torch.matmul(
                    _geo - (center + self.r0), rot
                ) + (center + self.r0)

        # rotate polarizability sub-tensors
        rot = rot.to(DTYPE_COMPLEX).unsqueeze(0).unsqueeze(0)
        rotT = rot.transpose(-2, -1)
        for m in [0, 3]:
            for n in [0, 3]:
                _s_rot.alpha_data[..., m : m + 3, n : n + 3] = torch.matmul(
                    torch.matmul(
                        rotT,
                        _s_rot.alpha_data[..., m : m + 3, n : n + 3],
                    ),
                    rot,
                )

        # update lookup tables
        _s_rot.create_lookup()

        return _s_rot

    def combine(
        self, other, inplace=False, refresh_lookup=True, on_distance_violation="warn"
    ):
        """combine with a second structure

        Structures must be of same coupling type (electric / magnetic)

        Args:
            other (_type_): _description_
            inplace (bool, optional): Don't copy original structure, just add other structure. Can be necessary e.g. when gradients are required. Defaults to False.
            refresh_lookup (bool, optional): refresh the polarizability lookup table. Defaults to True.
            on_distance_violation (str, optional): can be "error", "warn", None (do nothing). Defaults to "error".

        Returns:
            :class:`StructBase`: new structure
        """
        if inplace:
            new_struct = self
        else:
            new_struct = self.copy()

        assert torch.all(new_struct.wavelengths_data == other.wavelengths_data)
        assert type(self) == type(other)

        N_dist1, N_dist2 = test_structure_distances(self, other)
        if on_distance_violation == "error" and (N_dist1 + N_dist2 > 0):
            raise ValueError(
                "Several meshpoints in structures are too close (struct1: {}, structu2: {})!".format(
                    N_dist1, N_dist2
                )
            )
        elif on_distance_violation == "warn" and (N_dist1 + N_dist2 > 0):
            warnings.warn(
                "Several meshpoints in structures are too close (struct1: {}, structu2: {})!".format(
                    N_dist1, N_dist2
                )
            )

        new_struct.positions = torch.concatenate(
            [self.get_all_positions(), other.positions], dim=0
        )

        new_struct.zeros_spectral = torch.concatenate(
            [new_struct.zeros_spectral, other.zeros_spectral], dim=0
        )

        new_struct.step = torch.concatenate([new_struct.step, other.step], dim=0)
        new_struct.r0 = new_struct.get_center_of_mass()

        new_struct.alpha_data = torch.concatenate(
            [new_struct.alpha_data, other.alpha_data], dim=0
        )

        new_struct.selfterms_data = torch.concatenate(
            [new_struct.selfterms_data, other.selfterms_data], dim=0
        )

        # finally, add full geometries
        new_struct.full_geometries = new_struct.full_geometries + other.full_geometries

        # create lookup
        if refresh_lookup:
            new_struct.create_lookup()

        return new_struct


# --- Mie sphere - dipolar model
class StructMieSphereEffPola3D(StructEffPola3D):
    """class for Mie-theory based 3D point polarizability

    Requires external package `treams`
    !!! class constructor does not support automatic differentiation !!!

    Defines a point polarizability representing a sphere using
    first order (dipolar) Mie coefficients
    """

    __name__ = "Mie-theory sphere dipolar polarizability (3D) structure class"

    def __init__(
        self,
        wavelengths: torch.Tensor,
        radii: list,
        materials: list,
        environment=None,
        r0: torch.Tensor = None,
        device: torch.device = None,
        quadrupol_tol=0.15,
    ):
        """3D point polarizability class for a core-shell sphere (Mie)

        Use Mie theory in dipole approximation (first order) to get an
        effective polarizability model for a core-shell sphere.
        Requires the `treams` package for Mie coefficient calculation.
        https://github.com/tfp-photonics/treams

        Args:
            wavelengths (torch.Tensor): list of wavelengths to evaluate (nm)
            radii (list): list of the sphere's core and (multiple) shell radii (in nm).
            materials (list): materials of core and shell(s). A float or int is interpreted as permittivity value.
            environment (environment instance, optional): Homogeneous 3D environment to evaluate Mie theory in. Defaults to None, which uses vacuum.
            r0 (torch.Tensor, optional): polarizability position (x,y,z). If not given, is set to (0, 0, 0). Defaults to None
            device (torch.device, optional): Defaults to "cpu".
            quadrupol_tol (float, optional): ratio of tolerable residual quadrupole terms relative to the dipole order before warning. Defaults to 0.15.

        Raises:
            ValueError: incorrect parameters
        """
        # prep and imports
        from torchgdm.tools.misc import to_np
        from torchgdm.materials.base_classes import MaterialBase
        from torchgdm.materials import MatConstant
        import numpy as np

        # TODO: Replace with differentiable Mie code
        from torchgdm.tools.mie import mie_ab_sphere_3d

        if device is None:
            self.device = get_default_device()
        else:
            self.device = device

        # tensor conversion
        wavelengths = torch.as_tensor(
            wavelengths, dtype=DTYPE_FLOAT, device=self.device
        )
        wavelengths = torch.atleast_1d(wavelengths)
        k0 = 2 * torch.pi / wavelengths

        # mie coefficients
        mie_results = mie_ab_sphere_3d(
            wavelengths=wavelengths,
            radii=radii,
            materials=materials,
            environment=environment,
            device=self.device,
            as_dict=True,
        )
        a_n = mie_results["a_n"]
        b_n = mie_results["b_n"]
        env = mie_results["environment"]
        n_env = mie_results["n_env"]
        r_enclosing = mie_results["r_enclosing"]

        # check if dipole approximation is good
        a_quadrupol_res = a_n[:, 1].abs()
        wls_violation_a = to_np(wavelengths[a_quadrupol_res.to("cpu") > quadrupol_tol])
        if len(wls_violation_a) > 0:
            warnings.warn(
                "Mie series: {} wavelengths with ".format(len(wls_violation_a))
                + "significant residual electric quadrupole contribution: "
                + "{} nm".format([round(r, 1) for r in wls_violation_a])
            )

        b_quadrupol_res = b_n[:, 1].abs()
        wls_violation_b = to_np(wavelengths[b_quadrupol_res.to("cpu") > quadrupol_tol])
        if len(wls_violation_b) > 0:
            warnings.warn(
                "Mie series: {} wavelengths with ".format(len(wls_violation_b))
                + "significant residual magnetic quadrupole contribution: "
                + "{} nm".format([round(r, 1) for r in wls_violation_b])
            )

        # convert to polarizabilities (units of volume)
        # see: García-Etxarri, A. et al. Optics Express 19, 4815 (2011)
        a_pE = 1j * 3 / 2 * a_n[:, 0] / k0**3 / n_env**1
        a_mH = 1j * 3 / 2 * b_n[:, 0] / k0**3 / n_env**3

        # populate 6x6 polarizabilities for all wavelengths
        alpha_6x6 = torch.zeros(
            (len(wavelengths), 6, 6), dtype=DTYPE_COMPLEX, device=self.device
        )
        alpha_6x6[:, torch.arange(3), torch.arange(3)] += a_pE.unsqueeze(1)
        alpha_6x6[:, torch.arange(3, 6), torch.arange(3, 6)] += a_mH.unsqueeze(1)

        # set center of mass
        if r0 is None:
            r0 = torch.as_tensor([0.0, 0.0, 0.0], dtype=DTYPE_FLOAT, device=self.device)
        else:
            r0 = torch.as_tensor(r0, dtype=DTYPE_FLOAT, device=self.device)
            r0 = r0.squeeze()
            assert len(r0) == 3

        # wrap up in a dictionary compatible with the point dipole structure class
        alpha_dict = dict(
            r0=r0,
            r0_MD=r0,
            r0_ED=r0,
            alpha_6x6=alpha_6x6,
            wavelengths=wavelengths,
            enclosing_radius=r_enclosing,
            k0_spectrum=k0,
            environment=env,
        )

        # - point polarizability structure with Mie dipolar response
        super().__init__(
            positions=r0,
            alpha_dicts=[alpha_dict],
            device=self.device,
        )
