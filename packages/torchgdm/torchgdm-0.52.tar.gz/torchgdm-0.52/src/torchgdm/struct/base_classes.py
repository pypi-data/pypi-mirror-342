# -*- coding: utf-8 -*-
"""base class for structures

.. autosummary::
   :toctree: generated/

   StructBase

"""
import warnings

import torch

from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX, STRUCTURE_IDS
from torchgdm.tools.misc import get_default_device
from torchgdm.tools.misc import concatenation_of_list_elements
from torchgdm.tools.geometry import test_structure_distances


# --- base class structure container
class StructBase:
    """base class for structure container

    Defines the polarizabilities and self-terms
    """

    __name__ = "structure base class"

    def __init__(self, device: torch.device = None):
        """Initialization"""
        if device is None:
            self.device = get_default_device()
        else:
            self.device = device

        self.n_dim = -1  # problem dimension needs to be set by child class

        self.positions = torch.as_tensor(
            [], dtype=DTYPE_FLOAT, device=self.device
        )  # shape: (N, 3)
        self.step = torch.as_tensor(
            [], dtype=DTYPE_FLOAT, device=self.device
        )  # shape: (N, 3)

        self.mesh_normalization_factor = 1.0

        # create placeholders for internal fields
        self.reset_fields()
        self.environment = None

        # a structure may have a pure electric "E" 
        # or mixed electric/magnetic "EH" response
        # this is used to reduce computation requirements for "E" scatterers
        self.interaction_type = "EH"

        # unique identifier
        self.id = next(STRUCTURE_IDS)

    def reset_fields(self):
        self.fields_inside = dict()
        self.fields_inc = dict()

    def __add__(self, other):
        if issubclass(type(other), StructBase):
            # add a structure: try combining both.
            return self.combine(other)
        elif len(other) == 3:
            # add a 3-tuple: Try shift
            return self.translate(other)
        else:
            raise ValueError("Unknown addition.")

    def __sub__(self, other):
        if issubclass(type(other), StructBase):
            # subtract a structure:  TODO (not clear yet what to do)
            raise NotImplementedError(
                "Removing a structure from another is not implemented yet."
            )
        elif len(other) == 3:
            # subtract a 3-tuple: Try shift
            return self.translate(
                -1 * torch.as_tensor(other, dtype=DTYPE_FLOAT, device=self.device)
            )
        else:
            raise ValueError("Unknown addition.")

    def __repr__(self, verbose: bool = False):
        """description about structure"""
        out_str = " ------ base structure class - doesn't define anything yet -------"
        return out_str

    def set_device(self, device):
        """move all tensors of the class to device"""
        self.device = device
        self.positions = self.positions.to(device=device)

        # stored fields
        for k in self.fields_inside:
            self.fields_inside[k].set_device(device=device)
        for k in self.fields_inc:
            self.fields_inc[k].set_device(device=device)

    # --- plot placeholder
    def plot(self):
        raise NotImplementedError("Plot not implement yet.")

    def plot_contour(self, **kwargs):
        """if not implemented: fall back to full structure plot"""
        return self.plot(**kwargs)

    def plot3d(self):
        raise NotImplementedError("3D Plot not implement yet.")

    # --- common interface for positions / step
    def get_all_positions(self) -> torch.Tensor:
        return self.positions

    def get_source_validity_radius(self) -> torch.Tensor:
        """get the radius of the validity zone of each effective source"""

        # effective pola structure: step=diameter. return step / 2
        if hasattr(self, "full_geometries"):
            _r = self.step / 2
        # discretized structure: step=cell side length. return sqrt(2) * step / 2
        else:
            _r = 2**0.5 * self.step / 2
        return _r

    # --- illumination fields at dipole positions
    def get_fields_inc(self, wavelength, environment, f_inc_list=None):
        if float(wavelength) not in self.fields_inc:
            if f_inc_list is None:
                raise ValueError(
                    f"illumination not yet evaluated at wavelength {wavelength}nm."
                    + "But no illumination fields are given. "
                    + "Please provide illuminations as `f_inc_list`."
                )
            r_probe = self.get_all_positions()
            f0 = [
                f_inc.get_field(r_probe, wavelength=wavelength, environment=environment)
                for f_inc in f_inc_list
            ]
            f0 = concatenation_of_list_elements(f0)
            self.fields_inc[float(wavelength)] = f0
        return self.fields_inc[float(wavelength)]

    def get_e0(self, wavelength, environment, f_inc_list=None):
        if float(wavelength) not in self.fields_inc:
            self.get_fields_inc(wavelength, environment, f_inc_list)

        return self.fields_inc[float(wavelength)].get_efield()

    def get_h0(self, wavelength, environment, f_inc_list=None):
        if float(wavelength) not in self.fields_inc:
            self.get_fields_inc(wavelength, environment, f_inc_list)

        return self.fields_inc[float(wavelength)].get_hfield()

    def get_e0_h0(self, wavelength, environment, f_inc_list=None) -> torch.Tensor:
        e0 = self.get_e0(wavelength, environment, f_inc_list)
        h0 = self.get_h0(wavelength, environment, f_inc_list)
        return torch.cat([e0, h0], dim=-1)

    # --- fields inside (self-consistent within a simulation) at dipole positions
    def set_fields_inside(self, wavelength, field, environment):
        self.environment = environment
        self.fields_inside[float(wavelength)] = field

    def get_fields_inside(self, wavelength, **kwargs):
        if float(wavelength) not in self.fields_inside:
            raise ValueError(
                f"Inside field not available at wl={wavelength}nm. "
                + "Run the simulation."
            )
        return self.fields_inside[float(wavelength)]

    def get_e_selfconsistent(self, wavelength, **kwargs):
        if float(wavelength) not in self.fields_inside:
            raise ValueError(
                f"Inside field not available at wl={wavelength}nm. "
                + "Run the simulation."
            )
        return self.fields_inside[float(wavelength)].get_efield()

    def get_h_selfconsistent(self, wavelength, **kwargs):
        # assume no magnetic moments (electric coupling only)
        # modify this for magnetic response
        e_in = self.get_e_selfconsistent(wavelength)
        h = torch.empty(size=(len(e_in), 0, 3), dtype=DTYPE_COMPLEX, device=self.device)
        return h

    def get_e_h_selfconsistent(self, wavelength, **kwargs) -> torch.Tensor:
        # modify this for magnetic response
        raise ValueError(
            f"Structure has no magnetic response, only selfconsistent e-fields available."
        )

    # --- dipole moments and their positions (self-consistent within a simulation)
    def get_r_pm(self):
        """positions of electric and magnetic polarizable dipoles"""
        r_p = self.get_all_positions()
        # assume electric-only coupling. modify this for magnetic response
        r_m = torch.empty(size=(0, 3), dtype=DTYPE_FLOAT, device=self.device)
        return r_p, r_m

    def get_pm(self, wavelength):
        """electric-electric interaction: p is due to E-field only, m is zero"""
        # electric coupling
        alpha_pE = self.get_polarizability_pE(wavelength, self.environment)
        e_in = self.get_e_selfconsistent(wavelength)
        p = torch.matmul(alpha_pE, e_in.unsqueeze(-1))[..., 0]

        # assume electric-only coupling. modify this for magnetic response
        m = torch.empty(size=(len(e_in), 0, 3), dtype=DTYPE_COMPLEX, device=self.device)

        return p, m

    # --- self-terms
    def get_selfterm_6x6(self, wavelength: float, environment) -> torch.Tensor:
        """return list of magneto-electric self-term tensors (6x6) at each meshpoint

        Args:
            wavelength (float): in nm
            environment (environment class): 3D environement class

        Returns:
            torch.Tensor: 6x6 selfterm tensor
        """
        selfterm_6x6 = torch.cat(
            [
                torch.cat(
                    [
                        self.get_selfterm_pE(wavelength, environment),
                        self.get_selfterm_pH(wavelength, environment),
                    ],
                    dim=-1,
                ),
                torch.cat(
                    [
                        self.get_selfterm_mE(wavelength, environment),
                        self.get_selfterm_mH(wavelength, environment),
                    ],
                    dim=-1,
                ),
            ],
            dim=-2,
        )
        return selfterm_6x6

    def get_selfterm_pE(self, wavelength: float, environment):
        """return list of 'EE' self-term tensors (3x3) at each meshpoint"""
        return torch.zeros(
            (len(self.get_all_positions()), 3, 3),
            device=self.device,
            dtype=DTYPE_COMPLEX,
        )

    def get_selfterm_mE(self, wavelength: float, environment):
        """return list of 'HE' self-term tensors (3x3) at each meshpoint"""
        return torch.zeros(
            (len(self.get_all_positions()), 3, 3),
            device=self.device,
            dtype=DTYPE_COMPLEX,
        )

    def get_selfterm_pH(self, wavelength: float, environment):
        """return list of 'EH' self-term tensors (3x3) at each meshpoint"""
        return torch.zeros(
            (len(self.get_all_positions()), 3, 3),
            device=self.device,
            dtype=DTYPE_COMPLEX,
        )

    def get_selfterm_mH(self, wavelength: float, environment):
        """return list of 'HH' self-term tensors (3x3) at each meshpoint"""
        return torch.zeros(
            (len(self.get_all_positions()), 3, 3),
            device=self.device,
            dtype=DTYPE_COMPLEX,
        )

    # --- polarizabilities
    def get_polarizability_6x6(self, wavelength: float, environment) -> torch.Tensor:
        """return list of magneto-electric polarizability tensors (6x6) at each meshpoint

        Args:
            wavelength (float): in nm
            environment (environment class): 3D environement class

        Returns:
            torch.Tensor: 6x6 polarizability tensor
        """
        alpha_6x6 = torch.cat(
            [
                torch.cat(
                    [
                        self.get_polarizability_pE(wavelength, environment),
                        self.get_polarizability_pH(wavelength, environment),
                    ],
                    dim=-1,
                ),
                torch.cat(
                    [
                        self.get_polarizability_mE(wavelength, environment),
                        self.get_polarizability_mH(wavelength, environment),
                    ],
                    dim=-1,
                ),
            ],
            dim=-2,
        )
        return alpha_6x6

    def get_polarizability_pmE_6x3(
        self, wavelength: float, environment
    ) -> torch.Tensor:
        alpha_pmE_6x3 = torch.cat(
            [
                self.get_polarizability_pE(wavelength, environment),
                self.get_polarizability_mE(wavelength, environment),
            ],
            dim=-2,
        )
        return alpha_pmE_6x3

    def get_polarizability_pEH_3x6(
        self, wavelength: float, environment
    ) -> torch.Tensor:
        """return list of magneto-electric self-term tensors (6x6) at each meshpoint"""
        alpha_pEH_3x6 = torch.cat(
            [
                self.get_polarizability_pE(wavelength, environment),
                self.get_polarizability_pH(wavelength, environment),
            ],
            dim=-1,
        )
        return alpha_pEH_3x6

    def get_polarizability_pmH_6x3(
        self, wavelength: float, environment
    ) -> torch.Tensor:
        alpha_pmH_6x3 = torch.cat(
            [
                self.get_polarizability_pH(wavelength, environment),
                self.get_polarizability_mH(wavelength, environment),
            ],
            dim=-2,
        )
        return alpha_pmH_6x3

    def get_polarizability_mEH_3x6(
        self, wavelength: float, environment
    ) -> torch.Tensor:
        """return list of magneto-electric self-term tensors (6x6) at each meshpoint"""
        alpha_pmH_3x6 = torch.cat(
            [
                self.get_polarizability_mE(wavelength, environment),
                self.get_polarizability_mH(wavelength, environment),
            ],
            dim=-1,
        )
        return alpha_pmH_3x6

    def get_polarizability_pE(self, wavelength: float, environment):
        """return list of EE polarizability tensors (3x3) at each meshpoint"""
        return torch.zeros(
            (len(self.get_all_positions()), 3, 3),
            device=self.device,
            dtype=DTYPE_COMPLEX,
        )

    def get_polarizability_mE(self, wavelength: float, environment):
        """return list of HE polarizability tensors (3x3) at each meshpoint"""
        return torch.zeros(
            (len(self.get_all_positions()), 3, 3),
            device=self.device,
            dtype=DTYPE_COMPLEX,
        )

    def get_polarizability_pH(self, wavelength: float, environment):
        """return list of EH polarizability tensors (3x3) at each meshpoint"""
        return torch.zeros(
            (len(self.get_all_positions()), 3, 3),
            device=self.device,
            dtype=DTYPE_COMPLEX,
        )

    def get_polarizability_mH(self, wavelength: float, environment):
        """return list of HH polarizability tensors (3x3) at each meshpoint"""
        return torch.zeros(
            (len(self.get_all_positions()), 3, 3),
            device=self.device,
            dtype=DTYPE_COMPLEX,
        )

    # - radiative correction for cross section calc. - 3D case
    def get_radiative_correction_prefactor_p(self, wavelength: float, environment):
        """return electric dipole radiative correction prefactor vectors (3) at each meshpoint"""
        if self.radiative_correction:
            if self.n_dim != 3:
                raise ValueError(
                    f"{self.n_dim}D simulation, but trying to evluate 3D radiative correction. "
                    + "Please deactivate radiative correction or implement adequate "
                    "`get_radiative_correction_prefactor_p` / `..._m`"
                )
            k0 = 2 * torch.pi / wavelength
            n_env = (
                environment.get_environment_permittivity_scalar(
                    wavelength, self.get_all_positions()
                )
                ** 0.5
            )
            rad_corr_3d = (2 / 3) * k0**3 * n_env
            return torch.ones(
                (len(self.get_all_positions()), 3),
                device=self.device,
                dtype=DTYPE_COMPLEX,
            ) * rad_corr_3d.unsqueeze(-1)
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
            rad_corr_3d = (2 / 3) * k0**3 * n_env**3
            return torch.ones(
                (len(self.get_all_positions()), 3),
                device=self.device,
                dtype=DTYPE_COMPLEX,
            ) * rad_corr_3d.unsqueeze(-1)
        else:
            return torch.zeros(
                (len(self.get_all_positions()), 3),
                device=self.device,
                dtype=DTYPE_COMPLEX,
            )

    # --- geometry operations
    def copy(self, positions=None, rotation_angles=None):
        """(batch) copy structre to new position(s)

        optionally, the copied structures can also be batch-rotated along the `z` axis.

        Args:
            positions (list, optional): list of new positions to create copies at. If None, create a single, identical copy. Defaults to None.
            rotation_angles (list, optional): list of rotation angles for the copies. If None, keep orientations. Defaults to None.

        Returns:
            :class:`StructBase`: new structure
        """
        if type(positions) == dict:
            positions = positions["r_probe"]

        if positions is None:
            import copy

            try:
                return copy.deepcopy(self)
            except RuntimeError:
                warnings.warn(
                    "RuntimeError in structure copy detected. "
                    + "Returning original structure instead. "
                    + "Caution!! This may result in unexpected behavior! "
                    + "You should try to fix this problem or avoid creating structure copies. "
                    + "Maybe some structure parameters require gradients, then copy is not possible. "
                    + "You may try passing `copy_structures=False` to the simulation."
                )
                return self

        else:
            # generate multiple copies, moved to `positions`
            positions = torch.as_tensor(
                positions, device=self.device, dtype=DTYPE_FLOAT
            )
            positions = torch.atleast_2d(positions)
            assert len(positions.shape) == 2
            assert positions.shape[1] == 3

            if rotation_angles is None:
                rotation_angles = torch.zeros(
                    len(positions), device=self.device, dtype=DTYPE_FLOAT
                )
            else:
                rotation_angles = torch.as_tensor(
                    rotation_angles, device=self.device, dtype=DTYPE_FLOAT
                )
                rotation_angles =torch.atleast_1d(rotation_angles)
                assert len(rotation_angles) == len(positions)
                assert len(rotation_angles.shape) == 1

            new_struct_list = []
            for _r, _a in zip(positions, rotation_angles):
                _struct = self.copy()
                _struct.set_center_of_mass(_r)
                if _a != 0:
                    _struct = _struct.rotate(_a)
                new_struct_list.append(_struct)

            new_struct = new_struct_list.pop(0)
            for _s in new_struct_list:
                new_struct = new_struct.combine(_s, inplace=True)

            new_struct.r0 = new_struct.get_center_of_mass()
            return new_struct

    def get_geometric_crosssection(self, projection="xy"):
        """get geometric cross section the structure in nm^2

        Args:
            projection (str, optional): cartesian projection of cross section. Defaults to "xy"

        Returns:
            float: geometric cross section in nm^2
        """
        from torchgdm.tools.geometry import get_geometric_crosssection

        return get_geometric_crosssection(self, projection)

    def get_center_of_mass(self):
        """return the center of mass"""
        return torch.mean(self.get_all_positions(), axis=0)

    def set_center_of_mass(self, r0_new: torch.Tensor):
        """move center of mass to new position `r0_new` (in-place)"""
        r0_new = torch.as_tensor(r0_new, device=self.device)

        if len(r0_new.shape) != 1:
            if len(r0_new) not in [2, 3]:
                raise ValueError("`r0_new` needs to be (X,Y) or (X,Y,Z) tuple.")
        r0_old = self.get_center_of_mass()

        if len(r0_new) == 2:
            warnings.warn("Got 2-vector, assume xy coordinates.")
            r0_new = torch.as_tensor(
                [r0_new[0], r0_new[1], r0_old[2]], device=self.device
            )

        # move
        self.positions -= r0_old  # move to origin
        self.positions += r0_new  # move to new location
        self.r0 = self.get_center_of_mass()

    def translate(self, vector):
        """return copy, moved by `vector`"""
        vector = torch.as_tensor(vector, dtype=DTYPE_FLOAT, device=self.device)
        vector = torch.atleast_2d(vector)

        _shifted = self.copy()

        _shifted.positions += vector
        _shifted.r0 = _shifted.get_center_of_mass()
        return _shifted

    def rotate(self, alpha, center=torch.as_tensor([0.0, 0.0, 0.0]), axis="z"):
        raise NotImplementedError(
            "`rotate` is not yet implemented in the current class."
        )

    def combine(self, other, inplace=False, on_distance_violation="error"):
        """combine with a second structure (requires definition at same wavelengths!)

        Structures must be of same coupling type (electric / magnetic)

        Args:
            other (_type_): _description_
            inplace (bool, optional): Don't copy original structure, just add other structure. Can be necessary e.g. when gradients are required. Defaults to False.
            on_distance_violation (str, optional): can be "error", "warn", None (do nothing). Defaults to "error".

        Returns:
            :class:`StructBase`: new structure
        """
        if inplace:
            new_struct = self
        else:
            new_struct = self.copy()

        assert self.mesh_normalization_factor == other.mesh_normalization_factor
        assert self.radiative_correction == other.radiative_correction
        assert self.interaction_type == other.interaction_type
        assert type(self) == type(other)

        N_dist1, N_dist2 = test_structure_distances(
            self, other, on_distance_violation=on_distance_violation
        )

        new_struct.positions = torch.concatenate(
            [self.get_all_positions(), other.positions], dim=0
        )
        new_struct.step = torch.concatenate([new_struct.step, other.step], dim=0)
        new_struct.zeros = torch.concatenate([new_struct.zeros, other.zeros], dim=0)
        new_struct.materials = new_struct.materials + other.materials

        new_struct.r0 = new_struct.get_center_of_mass()  # center of gravity
        return new_struct
