# -*- coding: utf-8 -*-
"""
core simulation class
"""
# %%
import warnings
import time

import torch

from torchgdm.field import Field
from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX
from torchgdm.tools.misc import tqdm, _purge_mem, get_default_device
from torchgdm.tools.misc import sum_of_list_elements
from torchgdm.tools.misc import concatenation_of_list_elements
from torchgdm.tools.misc import _check_environment
from torchgdm.tools.misc import deprecated

# from torchgdm.tools.batch import get_e0, get_h0
from torchgdm.tools.geometry import test_structure_distances


# --- simulation base class
class SimulationBase:
    """torchgdm simulation container

    This class contains all elements describing a simulation:
     - the environment
     - the structure(s)
     - the illumination field(s)
     - the evaluation wavelength(s)

    It also acts as an interface to running and postprocessing
    of the simulation as well as for several visualization tools.
     - run the simulation
     - evaluate observables
     - evaluate spectra
     - evaluate a rasterscan

    It also contains methods for manipulations of the simulation and structures
     - add / remove a structure
     - split off a new simulation with a sub-structure
     - combine with structures and their fields from another simulation
     - copy (including optional shift of all structures)

    Furthermore it several contains private methods necessary for simulation setup and running
    """

    __name__ = "simulation base class"

    def __init__(
        self,
        structures: list,
        environment,
        illumination_fields: list,
        wavelengths: torch.Tensor,
        test_structure_collisions: bool = True,
        copy_structures=True,
        on_distance_violation: str = "error",
        device: torch.device = None,
    ):
        """base simulation constructor

        Args:
            structures (_type_): list of structures
            environment (_type_): environment class
            illumination_fields (_type_): list of illuminations
            wavelengths (torch.Tensor): evaluation wavelengths (in nm)
            test_structure_collisions (bool, optional): Check for overlapping / colliding structures. Can be slow in case of many structures. Defaults to True.
            copy_structures (bool, optional): Create copies of each structure for safety (using the same structure in different simulations can create strange behaviors). Defaults to True.
            on_distance_violation (str, optional): behavior on distance violation. can be "error", "warn" or None (do nothing). Defaults to "error".
            device (torch.device, optional): Defaults to "cpu" (can be changed by :func:`torchgdm.use_cuda`).
        """
        if device is None:
            self.device = get_default_device()
        else:
            self.device = device

        # structures, wavelengths, illuminations: if single element given, wrap into list
        if copy_structures:
            if hasattr(structures, "__iter__"):
                self.structures = [
                    _s.copy() for _s in structures if _s is not None
                ]  # ignore "None" entries
            else:
                self.structures = [structures.copy()]
        else:
            if hasattr(structures, "__iter__"):
                self.structures = [
                    _s for _s in structures if _s is not None
                ]  # ignore "None" entries
            else:
                self.structures = [structures]

        if hasattr(illumination_fields, "__iter__"):
            self.illumination_fields = illumination_fields
        else:
            self.illumination_fields = [illumination_fields]

        # convert single wavelength to list
        self.wavelengths = torch.as_tensor(
            wavelengths, dtype=DTYPE_FLOAT, device=self.device
        )
        self.wavelengths = torch.atleast_1d(self.wavelengths)

        # environment
        env = _check_environment(
            environment, N_dim=self.structures[0].n_dim, device=device
        )
        self.environment = env

        # test collisions:
        if test_structure_collisions:
            for _s1 in self.structures:
                for _s2 in self.structures:
                    if _s1 != _s2:
                        N_dist1, N_dist2 = test_structure_distances(
                            _s1, _s2, on_distance_violation=on_distance_violation
                        )

        # reset all fields
        self.reset_fields()

        # test if all components are same dimension as environment
        self._test_dimensions_matching()

    def _test_dimensions_matching(self):
        self.n_dim = dim = self.environment.n_dim
        if dim == -1:
            raise ValueError(
                "The environemnt has undefined dimension (-1), please modify your environment class."
            )

        # test structures
        for _s in self.structures:
            if _s.n_dim == -1:
                raise ValueError(
                    "A structure has undefined dimension (-1), please modify your structure class. "
                    + f"The current environment is {dim}D."
                )
            if _s.n_dim != dim:
                raise ValueError(
                    "Structures with inconsistent dimensions found. "
                    + f"Environment is {dim}D, all structures must be {dim}D as well."
                )

        # test illumination fields
        for _f in self.illumination_fields:
            if _f.n_dim == -1:
                raise ValueError(
                    "An illumination field has undefined dimension (-1), please modify your field class. "
                    + f"The current environment is {dim}D."
                )
            if _f.n_dim != dim:
                raise ValueError(
                    "Illumination fields with inconsistent dimensions found. "
                    + f"Environment is {dim}D, all fields must be {dim}D as well."
                )

    def set_device(self, device):
        """move all tensors of the class to device"""
        self.device = device

        # iterate lists of torchgdm objects
        for i in range(len(self.structures)):
            self.structures[i].set_device(device=device)
        for i in range(len(self.illumination_fields)):
            self.illumination_fields[i].set_device(device=device)

        # stored fields
        for k in self.fields_inside:
            self.fields_inside[k].set_device(device=device)
        for k in self.fields_inc:
            self.fields_inc[k].set_device(device=device)

        # further objects
        self.environment.set_device(device=device)
        self.wavelengths = self.wavelengths.to(device=device)

    def reset_fields(self):
        self.fields_inside = dict()
        self.fields_inc = dict()
        for _s in self.structures:
            _s.reset_fields()

    # --- simulation manipulation
    def add_struct(self, struct, on_distance_violation="error"):
        """add a structure to the simulation

        reset possibly pre-calculated fields.
        **Caution:** Not compatible with autograd!

        Args:
            struct (StructBase): structure to add

        Returns:
            simulation including added structure
        """
        import copy

        _new_sim = copy.deepcopy(self)

        _new_sim.structures.append(struct)

        N_dist1, N_dist2 = test_structure_distances(
            self, struct, on_distance_violation=on_distance_violation
        )

        warnings.warn(
            "Resetting pre-calculated fields. This should be changed, e.g. add zero fields."
        )
        _new_sim.reset_fields()
        return _new_sim

    def delete_struct(self, index: int):
        """delete a structure from the simulation

        **Caution:** Not compatible with autograd!

        Args:
            index (int): index of structure to delete from sim

        Returns:
            simulation without deleted structure
        """
        _simlist = [self.split(i) for i in range(len(self.structures))]
        if index == 0:
            _s = _simlist.pop(0)

        _new_sim = _simlist.pop(0)
        for i, _s in enumerate(_simlist):
            if index != 0 and i == index:
                pass  # delete (don't add) this structure
            else:
                _new_sim.combine(_s)

        return _new_sim

    def split(self, structure_index: int):
        """split a structure into new simulation

        return a new simulation with identical config,
        containing only the splitted structure.
        If fields were calculated, they are kept for the splitted structure

        **Caution:** Not compatible with autograd!

        Args:
            index (int): index of structure to split from sim

        Returns:
            simulation containing splitted structure
        """
        import copy

        _new_sim = copy.deepcopy(self)

        # if calculated, extract fields inside splitted structure
        if len(_new_sim.fields_inside) > 0:
            _new_sim.fields_inside = _new_sim._get_insidefields_for_single_structure(
                structure_index=structure_index
            )

        # retain selected structure
        _new_sim.structures = [_new_sim.structures[structure_index]]

        return _new_sim

    def combine(self, other_sim, on_distance_violation="error"):
        """combine with other simulation

        Combining pre-calculated fields. Wavelengths and field configs must match!

        **Caution:** Not compatible with autograd!

        Args:
            other_sim (:class:`Simulation`): simulation to combine with
            on_distance_violation (str, optional): behavior on distance violation. can be "error", "warn" or None (do nothing). Defaults to "error".

        Returns:
            :class:`Simulation`: combined simulation
        """
        import copy

        _new_sim = copy.deepcopy(self)

        assert len(_new_sim.fields_inside) == len(other_sim.fields_inside)
        assert _new_sim.wavelengths == other_sim.wavelengths
        assert len(_new_sim.illumination_fields) == len(other_sim.illumination_fields)
        assert _new_sim.environment.__name__ == other_sim.environment.__name__
        assert _new_sim.device == other_sim.device

        _, _ = test_structure_distances(
            self, other_sim, on_distance_violation=on_distance_violation
        )

        # if existing: combine inside fields
        if len(_new_sim.fields_inside) > 0:
            fields_inside_combined = dict()
            for wl in self.wavelengths:
                wl = float(wl)

                e_in_1 = _new_sim.fields_inside[wl].efield
                h_in_1 = _new_sim.fields_inside[wl].hfield
                e_in_2 = other_sim.fields_inside[wl].efield
                h_in_2 = other_sim.fields_inside[wl].hfield
                e_in = torch.cat([e_in_1, e_in_2], dim=1)
                h_in = torch.cat([h_in_1, h_in_2], dim=1)

                pos1 = _new_sim.get_all_positions()
                pos2 = other_sim.get_all_positions()
                pos = torch.cat([pos1, pos2], dim=0)

                _f = Field(pos, e_in, h_in)
                fields_inside_combined[float(wl)] = _f

            _new_sim.fields_inside = fields_inside_combined

        # combine structures
        _new_sim.structures += other_sim.structures  # add 2 lists

        return _new_sim

    def copy(self, positions=None):
        """(batch) copy simulation

        optionally, a simulations with multiple copies of its structures can be created, where each copy of structures is shifted to a new position.

        Args:
            positions (list, optional): list of new positions to create copies of the structures at. If None, create a single, identical copy. Defaults to None.

        Returns:
            :class:`Simulation`: new simulation
        """
        if positions is None:
            import copy

            return copy.deepcopy(self)
        else:
            # generate multiple copies, moved to `positions`
            positions = torch.as_tensor(
                positions, device=self.device, dtype=DTYPE_FLOAT
            )

            # single position: expand dim
            if len(positions.shape) == 1:
                positions = positions.unsqueeze(0)

            assert len(positions.shape) == 2
            assert positions.shape[1] == 3

            new_sim_list = []
            for _r in positions:
                _sim = self.copy()
                for i in range(len(_sim.structures)):
                    _sim.structures[i] = _sim.structures[i] + _r
                new_sim_list.append(_sim)

            new_sim = new_sim_list.pop(0)
            for _s in new_sim_list:
                new_sim = new_sim.combine(_s)

            return new_sim

    def __add__(self, other):
        if issubclass(type(other), type(self)):
            # add another simulation: try combining both.
            return self.combine(other)
        else:
            raise ValueError(
                "Unknown add type, only addition of other sim is supported."
            )

    # --- functions combining properties from all structures
    def get_all_positions(self) -> torch.Tensor:
        """return a list of all positions with dipoles"""
        return torch.cat(
            [struct.get_all_positions() for struct in self.structures], dim=0
        )

    def get_source_validity_radius(self) -> torch.Tensor:
        """return a list of all effective step-radii / enclosing sphere radius"""
        all_pos_step = [_s.get_source_validity_radius() for _s in self.structures]
        return torch.cat(all_pos_step)

    def get_closest_wavelength(self, wavelength):
        """return closest wavelength match available in the simulation"""
        from torchgdm.tools.misc import get_closest_wavelength

        return get_closest_wavelength(self, wavelength)

    # --- internal API: helper for polarizable / non-polarizable dipole handling
    def _get_polarizable_positions_indices_p_m(self, structure_index=-1) -> tuple:
        """get lists with indices of polarizable positions, separate for p and m

        Args:
            structure_index (int, optional): Optionally select a specific sub-structure. if -1, return for all structures. Defaults to -1.

        Returns:
            tuple: (torch.Tensor, torch.Tensor). position indices at which polarizable p and m dipoles are located
        """
        # optional: consider only a specific structure
        if structure_index == -1:
            structures = self.structures
        else:
            structures = [self.structures[structure_index]]

        idx_p = [torch.tensor([], dtype=torch.int32, device=self.device)]
        idx_m = [torch.tensor([], dtype=torch.int32, device=self.device)]
        i_offset = 0
        for struct in structures:
            N_pos = len(struct.get_all_positions())

            _sT = struct.interaction_type
            if "E" in _sT:
                idx_p.append(
                    torch.arange(i_offset, i_offset + N_pos, device=self.device)
                )
            if "H" in _sT:
                idx_m.append(
                    torch.arange(i_offset, i_offset + N_pos, device=self.device)
                )

            i_offset += N_pos

        return torch.cat(idx_p, dim=0), torch.cat(idx_m, dim=0)

    def _get_nonpolarizable_positions_indices_p_m(self, structure_index=-1) -> tuple:
        """get lists with indices of non-polarizable positions (where *no* polarizabilites are located), separate for p and m

        Args:
            structure_index (int, optional): Optionally select a specific sub-structure. if -1, return for all structures. Defaults to -1.

        Returns:
            tuple: (torch.Tensor, torch.Tensor). non-polarizable position indices at which *no* p or *no* m dipoles are located
        """
        # optional: consider only a specific structure
        if structure_index == -1:
            structures = self.structures
        else:
            structures = [self.structures[structure_index]]

        idx_p = [torch.tensor([], dtype=torch.int32, device=self.device)]
        idx_m = [torch.tensor([], dtype=torch.int32, device=self.device)]
        i_offset = 0
        for struct in structures:
            N_pos = len(struct.get_all_positions())

            _sT = struct.interaction_type
            if "E" not in _sT:
                idx_p.append(
                    torch.arange(i_offset, i_offset + N_pos, device=self.device)
                )
            if "H" not in _sT:
                idx_m.append(
                    torch.arange(i_offset, i_offset + N_pos, device=self.device)
                )

            i_offset += N_pos

        return torch.cat(idx_p, dim=0), torch.cat(idx_m, dim=0)

    def _get_polarizable_positions_p_m(self) -> tuple:
        """get lists with polarizable positions, separate for p and m

        Args:
            structure_index (int, optional): Optionally select a specific sub-structure. if -1, return for all structures. Defaults to -1.

        Returns:
            tuple: (torch.Tensor, torch.Tensor). positions at which polarizable p and m dipoles are located
        """
        pos_pm = [_s.get_r_pm() for _s in self.structures]
        pos_p = torch.cat([_s[0] for _s in pos_pm], dim=0)
        pos_m = torch.cat([_s[1] for _s in pos_pm], dim=0)

        return pos_p, pos_m

    def _get_nonpolarizable_positions_p_m(self) -> tuple:
        """get lists with non-polarizable positions (where *no* polarizabilites are located), separate for p and m

        Args:
            structure_index (int, optional): Optionally select a specific sub-structure. if -1, return for all structures. Defaults to -1.

        Returns:
            tuple: (torch.Tensor, torch.Tensor). non-polarizable positions at which *no* p or *no* m dipoles are located
        """
        idx_p, idx_m = self._get_nonpolarizable_positions_indices_p_m()
        dp_pos = self.get_all_positions()
        pos_miss_p = torch.index_select(dp_pos, 0, idx_p)
        pos_miss_m = torch.index_select(dp_pos, 0, idx_m)

        return pos_miss_p, pos_miss_m

    def _get_polarizable_mask_full_fields(self) -> torch.Tensor:
        # loop through structures and create field-mask for polarizable positions
        mask_fields = []
        for struct in self.structures:
            Npos = len(struct.get_all_positions())

            _sT = struct.interaction_type
            _mask_e0h0 = torch.zeros(
                (len(self.illumination_fields), Npos, 6),
                dtype=torch.bool,
                device=self.device,
            )
            if "E" in _sT:
                _mask_e0h0[..., :3] = 1
            if "H" in _sT:
                _mask_e0h0[..., 3:] = 1
            mask_fields.append(_mask_e0h0)
        mask_fields = torch.cat(mask_fields, dim=1)

        return mask_fields

    # --- polarizabilities of all structure dipoles
    # THESE FUNCTIONS WILL BE DEPRECATED (when GPMs are fully implemented)
    @deprecated
    def _get_all_polarizabilitites_6x6(self, wavelength: float) -> torch.Tensor:
        pola_list = torch.cat(
            [
                struct.get_polarizability_6x6(wavelength, self.environment)
                for struct in self.structures
            ],
            dim=0,
        )
        return pola_list

    @deprecated
    def _get_all_polarizabilitites_pEH_3x6(self, wavelength: float) -> torch.Tensor:
        pola_list = torch.cat(
            [
                struct.get_polarizability_pEH_3x6(wavelength, self.environment)
                for struct in self.structures
            ],
            dim=0,
        )
        return pola_list

    @deprecated
    def _get_all_polarizabilitites_mEH_3x6(self, wavelength: float) -> torch.Tensor:
        pola_list = torch.cat(
            [
                struct.get_polarizability_mEH_3x6(wavelength, self.environment)
                for struct in self.structures
            ],
            dim=0,
        )
        return pola_list

    @deprecated
    def _get_all_selfterms_6x6(self, wavelength: float) -> torch.Tensor:
        st_list = []
        for struct in self.structures:
            st_list.append(struct.get_selfterm_6x6(wavelength, self.environment))
        return torch.cat(st_list, dim=0)

    # --- illumination fields at all dipoles
    def _get_all_e0(self, wavelength: float) -> torch.Tensor:
        if float(wavelength) not in self.fields_inc:
            _f0 = self.get_fields_inc(wavelength)
        return self.fields_inc[float(wavelength)].get_efield()

    def _get_all_h0(self, wavelength: float) -> torch.Tensor:
        if float(wavelength) not in self.fields_inc:
            _f0 = self.get_fields_inc(wavelength)
        return self.fields_inc[float(wavelength)].get_hfield()

    def _get_all_e0_h0(self, wavelength: float) -> torch.Tensor:
        e0 = self._get_all_e0(wavelength)
        h0 = self._get_all_h0(wavelength)
        return torch.cat([e0, h0], dim=-1)

    # --- fields per structure
    def _get_insidefields_for_single_structure(self, structure_index):
        """return :class:`torchgdm.field.Field` instance of field in single structure"""
        fields_inside_struct = dict()
        for wl in self.wavelengths:
            _f = self.structures[structure_index].get_fields_inside(wl)
            fields_inside_struct[float(wl)] = _f
        return fields_inside_struct

    # --- fields and dipole moments at polarizable sources only
    def _get_polarizablefields_e0_h0(self, wavelength: float) -> torch.Tensor:
        # get full illumination E0, H0 fields (defined in parent class)
        e0_h0_all = self._get_all_e0_h0(wavelength=wavelength)

        mask_fields = self._get_polarizable_mask_full_fields()
        return e0_h0_all[mask_fields].reshape(len(self.illumination_fields), -1)

    # - public API
    def get_fields_inc(
        self,
        wavelength,
        r_probe: torch.Tensor = None,
        illumination_index: int = None,
        **kwargs,
    ):
        """get illumination fields at all structure positions or at `r_probe`

        further kwargs are ignored

        Args:
            wavelength (float): in nm
            r_probe (torch.Tensor): position(s) at which to evaluate incident field. If not given, evaluate at all dipole positions. Defaults to None.
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.

        Returns:
            `torchgdm.field.Field`: incident field as `Field` instance
        """
        if r_probe is None:
            # return illumination fields at all mesh locations
            if float(wavelength) not in self.fields_inc:
                f0 = [
                    s.get_fields_inc(
                        wavelength, self.environment, self.illumination_fields
                    )
                    for s in self.structures
                ]
                self.fields_inc[float(wavelength)] = sum_of_list_elements(f0)

            if illumination_index is not None:
                return f0[illumination_index]  # specific field only
            else:
                return self.fields_inc[float(wavelength)]
        else:
            # return illumination fields at r_probe
            kwargs_einc = dict(
                r_probe=r_probe, wavelength=wavelength, environment=self.environment
            )
            if illumination_index is not None:
                # eval specific field only
                f_inc = self.illumination_fields[illumination_index].get_field(
                    **kwargs_einc
                )
            else:
                f0_list = [
                    f_inc.get_field(**kwargs_einc) for f_inc in self.illumination_fields
                ]
                f_inc = concatenation_of_list_elements(f0_list)

            return f_inc

    def get_p_m_selfconsistent(
        self, wavelength: float, illumination_index: int = None, **kwargs
    ):
        """get self-consistent internal dipole moments at polarizable locations and their locations

        further kwargs are ignored

        Args:
            sim (`torchgdm.Simulation`): simulation (`sim.run()` needs to have been executed before)
            wavelength (float): in nm
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.

        Returns:
            tuple: tuple containing 4x `torch.Tensor` with the dipole moments and their 3D positions (p, m, r_p and r_m)
        """
        pass
        p = []
        m = []
        r_p = []
        r_m = []
        for _s in self.structures:
            _rp, _rm = _s.get_r_pm()
            _p, _m = _s.get_pm(wavelength)
            p.append(_p)
            m.append(_m)
            r_p.append(_rp)
            r_m.append(_rm)

        if len(p) > 0:
            p = torch.cat(p, dim=1)
        if len(m) > 0:
            m = torch.cat(m, dim=1)
        if len(r_p) > 0:
            r_p = torch.cat(r_p)
        if len(r_m) > 0:
            r_m = torch.cat(r_m)

        if illumination_index is not None:
            p = p[illumination_index].unsqueeze(0)
            m = m[illumination_index].unsqueeze(0)
        return p, m, r_p, r_m

    def get_e_h_selfconsistent(
        self, wavelength: float, illumination_index: int = None, **kwargs
    ):
        """get self-consistent internal dipole moments at polarizable locations and their locations

        further kwargs are ignored

        Args:
            sim (`torchgdm.Simulation`): simulation (`sim.run()` needs to have been executed before)
            wavelength (float): in nm
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.

        Returns:
            tuple: tuple containing 4x `torch.Tensor` with the dipole moments and their 3D positions (p, m, r_p and r_m)
        """
        pass
        e = []
        h = []
        r_e = []
        r_h = []
        for _s in self.structures:
            _re, _rh = _s.get_r_pm()
            _e = _s.get_e_selfconsistent(wavelength)
            _h = _s.get_h_selfconsistent(wavelength)
            e.append(_e)
            h.append(_h)
            r_e.append(_re)
            r_h.append(_rh)

        if len(e) > 0:
            e = torch.cat(e, dim=1)
        if len(h) > 0:
            h = torch.cat(h, dim=1)
        if len(r_e) > 0:
            r_e = torch.cat(r_e)
        if len(r_h) > 0:
            r_h = torch.cat(r_h)

        if illumination_index is not None:
            e = e[illumination_index].unsqueeze(0)
            h = h[illumination_index].unsqueeze(0)
        return e, h, r_e, r_h


# --- simulation container class
class Simulation(SimulationBase):
    """torchgdm simulation container"""

    __name__ = "torchgdm simulation container"

    def __init__(
        self,
        structures: list,
        environment,
        illumination_fields: list,
        wavelengths: list,
        linearsystem="default",
        test_structure_collisions: bool = True,
        copy_structures: bool = True,
        on_distance_violation: str = "error",
        device: torch.device = None,
    ):
        """simulation constructor

        Args:
            structures (list): list of structures
            environment (environmentBase): environment class
            illumination_fields (list): list of illuminations
            wavelengths (list): list of wavelengths to evaluate (nm)
            linearsystem (linearSystemBase): solver for the coupling system. Defaults to `LinearSystemFullMemEff`
            test_structure_collisions (bool, optional): Check for overlapping / colliding structures. Can be slow in case of many structures. Defaults to True.
            on_distance_violation (str, optional): behavior on distance violation. can be "error", "warn" or None (do nothing). Defaults to "error".
            device (torch.device, optional): Defaults to 'cpu'.
        """
        super().__init__(
            structures=structures,
            environment=environment,
            illumination_fields=illumination_fields,
            wavelengths=wavelengths,
            device=device,
            test_structure_collisions=test_structure_collisions,
            copy_structures=copy_structures,
            on_distance_violation=on_distance_violation,
        )
        if type(linearsystem) == str:
            if linearsystem.lower() == "default":
                from torchgdm.linearsystem import LinearSystemFullMemEff

                self.linearsystem = LinearSystemFullMemEff(device=device)
            else:
                raise ValueError("Unknown linearsystem.")
        else:
            self.linearsystem = linearsystem

        # set the global device for the simulation
        self.set_device(self.device)

    def __repr__(self):
        out_str = ""
        out_str += "simulation on device '{}'...\n".format(self.device)

        out_str += " - {}\n".format(self.environment.__name__)

        out_str += " - {} structures\n".format(len(self.structures))

        _pos = self.get_all_positions()
        out_str += " - {} positions\n".format(len(_pos))

        _pos_p, _pos_m = self._get_polarizable_positions_p_m()
        out_str += " - {} coupled dipoles\n".format(len(_pos_p) + len(_pos_m))
        out_str += "   (of which {} p, {} m)\n".format(len(_pos_p), len(_pos_m))

        out_str += " - {} wavelengths\n".format(len(self.wavelengths))

        out_str += " - {} illumination fields per wavelength".format(
            len(self.illumination_fields)
        )
        return out_str

    def set_device(self, device):
        super().set_device(device)
        self.linearsystem.set_device(device)

    def run(
        self,
        batch_size: int = 32,
        calc_missing: bool = False,
        verbose: int = 1,
        progress_bar=True,
    ):
        """run the simulation: evaluate all illuminations at all wavelengths

        results are the selfconsistent, full electric and magnetic fields
        at each meshpoint of all structures.

        this will populate `self.fields_inside` a dict with the wavelengths (in nm) as keys.
        Each element is a :class:`torchgdm.Field` instance, containing the `efield` and `hfield`.

        Args:
            batch_size (int, optional):    Nr of incident fields evaluated in parallel. Defaults to 32.
            calc_missing (bool, optional): calculate non-relevant internal fields, typically
                                           H-Field in discretized structures). Defaults to False.
            verbose (int, optional):       print status info. Defaults to 1.
        """
        t_start = time.time()
        if verbose:
            print("-" * 60)
            print(self)
            print("\nrun spectral simulation:")

        self.reset_fields()

        # loop over wavelengths
        for wl in tqdm(self.wavelengths, progress_bar, title=""):
            t_start_wl = time.time()
            if verbose and not progress_bar:
                print("wl={:.1f}nm: ".format(wl), end="")
            e_in, h_in = self.linearsystem.solve(
                sim=self,
                wavelength=wl,
                batch_size=batch_size,
                verbose=verbose,
            )

            # set full field to simulation
            _f = Field(self.get_all_positions(), e_in, h_in)
            self.fields_inside[float(wl)] = _f
            self._set_inside_fields_in_structures(wl)

            # pure electric / pure magnetic reponse: calc. missing fields via propagation
            if calc_missing:
                t_fillmiss0 = time.time()
                if verbose and not progress_bar:
                    print(" propa", end="")
                self._calculate_fields_at_nonpolarizable(wavelength=wl)
                t_fillmiss1 = time.time()
                if verbose and not progress_bar:
                    print(" {:.2f}s.".format(t_fillmiss1 - t_fillmiss0), end="")

            # cleanup
            _purge_mem(dev=e_in.device)

            if verbose and not progress_bar:
                t_end = time.time()
                print(" tot {:.2f}s.".format(t_end - t_start_wl))

        if verbose:
            t_end = time.time()
            if not progress_bar:
                print()
            print("spectrum done in {:.2f}s".format(t_end - t_start))
            print("-" * 60 + "\n")

    # --- internal fields helper
    def _set_inside_fields_in_structures(self, wavelength):
        """calculate internal fields for non-polarizable locations

        calculates the magnetic field at locations of purely electric-electric polarizabilties and
        the electric field at locations of purely magnetic-magnetic polarizabilties

        Args:
            wavelength (float): in nm
        """
        # get full inside fields
        e_in = self.fields_inside[float(wavelength)].efield
        h_in = self.fields_inside[float(wavelength)].hfield

        # set inside fields per structure
        n_dp = [len(_s.get_all_positions()) for _s in self.structures]
        e_chuncks = e_in.split(n_dp, dim=1)
        h_chuncks = h_in.split(n_dp, dim=1)
        for i_s, _s in enumerate(self.structures):
            _f_s = Field(_s.get_all_positions(), e_chuncks[i_s], h_chuncks[i_s])
            _s.set_fields_inside(wavelength, _f_s, self.environment)

    def _calculate_fields_at_nonpolarizable(self, wavelength: float):
        """calculate internal fields for non-polarizable locations

        calculates the magnetic field at locations of purely electric-electric polarizabilties and
        the electric field at locations of purely magnetic-magnetic polarizabilties

        Args:
            wavelength (float): in nm
        """
        # - calculate missing fields at a wavelength via re-propagation
        from torchgdm.postproc.fields import _nearfield_e, _nearfield_h

        wl_key = float(wavelength)
        field_shape = self.fields_inside[wl_key].efield.shape

        mask = self._get_polarizable_mask_full_fields()
        mask_e, mask_h = torch.chunk(mask, 2, dim=2)

        (
            pos_e_miss,
            pos_h_miss,
        ) = self._get_nonpolarizable_positions_p_m()

        if len(pos_e_miss) > 0:
            nf_e = _nearfield_e(
                sim=self,
                wavelength=wavelength,
                r_probe=pos_e_miss,
                source_distance_steps=0.1,  # exclude 'self-source' (divergence of G)
            )
            _e = nf_e["e_tot"]
            e_in = self.fields_inside[wl_key].efield.flatten()
            e_in[~mask_e.flatten()] = _e.flatten()
            e_in = e_in.reshape(field_shape)
            self.fields_inside[wl_key].set_efield(e_in)

        if len(pos_h_miss) > 0:
            nf_h = _nearfield_h(
                sim=self,
                wavelength=wavelength,
                r_probe=pos_h_miss,
                source_distance_steps=0.1,  # exclude 'self-source' (divergence of G)
            )
            _h = nf_h["h_tot"]
            h_in = self.fields_inside[wl_key].hfield.flatten()
            h_in[~mask_h.flatten()] = _h.flatten()
            h_in = h_in.reshape(field_shape)
            self.fields_inside[wl_key].set_hfield(h_in)

        # update fields inside structures
        self._set_inside_fields_in_structures(wavelength)

    # --- wrapper for post processing functions
    def get_geometric_crosssection(self, projection="xy"):
        """get ensemble geometric cross section of all structures in nm^2

        Args:
            projection (str, optional): cartesian projection of cross section. Defaults to "xy"

        Returns:
            float: geometric cross section in nm^2
        """
        import torchgdm as tg

        pos = self.get_all_positions()
        steps = torch.cat(
            [s.step / s.mesh_normalization_factor for s in self.structures]
        )
        return tg.tools.geometry._get_geo_cs_positions_steps(pos, steps, projection)

    def get_crosssections(self, wavelength, **kwargs):
        """total scattering, absorption and extinction cross section at a specific wavelength

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.crosssect.scs`.

        Args:
            sim (:class:`torchgdm.Simulation`): simulation instance
            wavelength (float): evaluation wavelength (in nm)
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.
            normalize_to_local_e0 (bool, optional): Whether to normalize to local illumination amplitude. Can be useful to get an approximate cross-section for non-plane wave illuminations. Defaults to False.
            radiative_correction (bool, optional): Whether to add radiative correction term. Defaults to True.

        Returns:
            dict: dictionaty containing the scattering, absorption and extinction cross section
        """
        from torchgdm.postproc.crosssect import scs

        return scs(wavelength=wavelength, **kwargs)

    # - fields
    def get_nearfield(
        self, wavelength, r_probe=None, illumination_index=None, **kwargs
    ):
        """calculate the nearfield (electric and magnetic) at positions `r_probe`

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.fields.nf`.

        Outside of the source zone fields are calculated via repropagation.
        Inside of structures, via interpolation from the fields at the neighbor meshpoint locations.

        Args:
            sim (:class:`torchgdm.Simulation`): simulation instance
            wavelength (float): evaluation wavelength (in nm)
            r_probe (dict, optional): probe locations describing dict (gen. from `tools.geometry`).  Defaults to None, in which case all positions of the simulation structures are used
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.

        Returns:
            dict: results for total, scattered and incident fields (keys: "tot", "sca", "inc") in instances of :class:`torchgdm.Field`
        """
        import torchgdm as tg

        if r_probe is None:
            r_probe = self.get_all_positions()

        nf = tg.postproc.fields.nf(
            self,
            wavelength=wavelength,
            r_probe=r_probe,
            illumination_index=illumination_index,
            **kwargs,
        )

        return nf

    def get_nf(self, **kwargs):
        """alias for :meth:`Simulation.get_nearfield`"""
        return self.get_nearfield(**kwargs)

    def get_multipole_decomposition(
        self,
        wavelength: float,
        illumination_index: int = None,  # None: batch all illumination fields
        r0=None,
        epsilon=0.1,
        long_wavelength_approx=False,
        **kwargs,
    ):
        """exact multipole decomposition of the internal electric field

        Multipole decomposition of the electromagnetic field inside a nanostructure for
        electric and magnetic dipole and quadrupole moments.

        For details about the method, see:

            Alaee, R., Rockstuhl, C. & Fernandez-Corbaton, I. *An electromagnetic
            multipole expansion beyond the long-wavelength approximation.*
            Optics Communications 407, 17-21 (2018)

        Args:
            sim (:class:`torchgdm.Simulation`): simulation instance
            wavelength (float): in nm
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.
            r0 (torch.Tensor, optional): [x,y,z] position of multipole decomposition development. Defaults to None, in which case the center of gravity is used.
            epsilon (float, optional): positions too close to r0 will moved away from r0 by epsilon (in units of step) to avoid numerical divergence of the Bessel terms. Defaults to 0.1.
            long_wavelength_approx (bool, optional): if True, use long wavelength approximation. Defaults to False.
            kwargs: Further kwargs are ignored

        Raises:
            ValueError: Simulation has not been run yet, or magnetic polarizabilities are present, or simulation is not 3D.

        Returns:
            dict: the multipole moments. dipoles are rank-1 (3-vectors), quadrupoles are rank 2 (3x3 tensors):
                - 'ed_tot': electric dipole (full)
                - 'md': magnetic dipole
                - 'eq_tot': electric quadrupole (full)
                - 'mq': magnetic quadrupole
                - 'ed_1': electric dipole (first order)
                - 'ed_toroidal': toroidal dipole
                - 'eq1': electric quadrupole (first order)
                - 'eq_toroidal': toroidal quadrupole

        """
        import torchgdm as tg

        nf = tg.postproc.multipole.decomposition_exact(
            self,
            wavelength=wavelength,
            illumination_index=illumination_index,
            r0=r0,
            epsilon=epsilon,
            long_wavelength_approx=long_wavelength_approx,
            **kwargs,
        )

        return nf

    def get_field_gradients(
        self,
        wavelength: float,
        r_probe: torch.Tensor = None,
        illumination_index: int = None,  # None: batch all illumination fields
        source_distance_steps: float = None,
        delta=0.1,
        whichfield="e_tot",
        **kwargs,
    ):
        """nearfield gradients inside or in proximity of a nanostructure

        Calculate field-gradients (positions defined by `r_probe`).
        pytorch AD is not efficient for gradients of functions R^n --> R^m, with $n \\sim m >> 1$.
        Therefore, here numerical derivatives are calculated via center differences.

        Based on the original implementation in pyGDM by C. Majorel.

        Warning: The current implementation is not memory efficient, since all fields are calculated, even though not required.

        Args:
            sim (:class:`torchgdm.Simulation`): simulation instance
            wavelength (float): in nm
            r_probe (torch.Tensor, optional): tuple (x,y,z) or list of 3-lists/-tuples to evaluate field gradients. Use all structure positions by default. Defaults to None.
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.
            delta (float, optional):  differential step for numerical center-derivative (in nanometers). Defaults to 0.1.
            whichfield (str, optional): fields to calculate the gradient for. One of ["e_sca","e_tot","e_inc", "h_sca","h_tot,"h_inc], . Defaults to "e_tot".

        Raises:
            ValueError: _description_

        Returns:
            3 lists of 3-tuples [dAx, dAy, dAz] (complex): dAj are the differential terms:
                - idx [0] = dE/dx = [dEx/dx, dEy/dx, dEz/dx]
                - idx [1] = dE/dy = [dEx/dy, dEy/dy, dEz/dy]
                - idx [2] = dE/dz = [dEx/dz, dEy/dz, dEz/dz]
        """
        import torchgdm as tg

        if r_probe is None:
            r_probe = self.get_all_positions()
        # field_gradient(sim, wavelength, r_probe, delta=delta, whichfield=field)
        fieldgrad = tg.postproc.fields.field_gradient(
            self,
            wavelength=wavelength,
            r_probe=r_probe,
            illumination_index=illumination_index,
            source_distance_steps=source_distance_steps,
            delta=delta,
            whichfield=whichfield,
            **kwargs,
        )

        return fieldgrad

    def get_nearfield_intensity_efield(
        self, wavelength, r_probe=None, illumination_index=None, **kwargs
    ):
        """calculate the electric field intensity in the nearfield at positions `r_probe`

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.fields.nf`.

        Args:
            sim (:class:`torchgdm.Simulation`): simulation instance
            wavelength (float): evaluation wavelength (in nm)
            r_probe (dict, optional): probe locations describing dict (gen. from `tools.geometry`).  Defaults to None, in which case all positions of the simulation structures are used
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.

        Returns:
            dict: results for total, scattered and incident electric field intensity (keys: "tot", "sca", "inc")
        """
        nf = self.get_nearfield(
            wavelength=wavelength,
            r_probe=r_probe,
            illumination_index=illumination_index,
            **kwargs,
        )

        # add positions
        nf["r_probe"] = nf["tot"].get_positions()

        for which in ["tot", "sca", "inc"]:
            nf[which] = nf[which].get_efield_intensity()

        return nf

    def get_nearfield_intensity_hfield(
        self, wavelength, r_probe=None, illumination_index=None, **kwargs
    ):
        """calculate the magnetic field intensity in the nearfield at positions `r_probe`

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.fields.nf`.

        Args:
            sim (:class:`torchgdm.Simulation`): simulation instance
            wavelength (float): evaluation wavelength (in nm)
            r_probe (dict, optional): probe locations describing dict (gen. from `tools.geometry`).  Defaults to None, in which case all positions of the simulation structures are used
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.

        Returns:
            dict: results for total, scattered and incident magnetic field intensity (keys: "tot", "sca", "inc")
        """
        nf = self.get_nearfield(
            wavelength=wavelength,
            r_probe=r_probe,
            illumination_index=illumination_index,
            **kwargs,
        )

        # add positions
        nf["r_probe"] = nf["tot"].get_positions()

        for which in ["tot", "sca", "inc"]:
            nf[which] = nf[which].get_hfield_intensity()

        return nf

    def get_chirality(
        self, wavelength, r_probe=None, illumination_index=None, **kwargs
    ):
        """calculate the nearfield chirality at positions `r_probe`

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.fields.nf`.

        Args:
            sim (:class:`torchgdm.Simulation`): simulation instance
            wavelength (float): evaluation wavelength (in nm)
            r_probe (dict, optional): probe locations describing dict (gen. from `tools.geometry`).  Defaults to None, in which case all positions of the simulation structures are used
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.

        Returns:
            dict: results for total, scattered and incident magnetic field intensity (keys: "tot", "sca", "inc")
        """
        nf_C = self.get_nearfield(
            wavelength=wavelength,
            r_probe=r_probe,
            illumination_index=illumination_index,
            **kwargs,
        )

        # add positions
        nf_C["r_probe"] = nf_C["tot"].get_positions()

        # overwrite Field instances by the chirality
        for which in ["tot", "sca", "inc"]:
            nf_C[which] = nf_C[which].get_chirality()

        return nf_C

    def get_poynting(self, wavelength, r_probe=None, illumination_index=None, **kwargs):
        """calculate the Poynting vector at positions `r_probe`

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.fields.nf`.

        Args:
            sim (:class:`torchgdm.Simulation`): simulation instance
            wavelength (float): evaluation wavelength (in nm)
            r_probe (dict, optional): probe locations describing dict (gen. from `tools.geometry`).  Defaults to None, in which case all positions of the simulation structures are used
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.

        Returns:
            dict: results for total, scattered and incident field's Poynting vector (keys: "tot", "sca", "inc")
        """
        nf_S = self.get_nearfield(
            wavelength=wavelength,
            r_probe=r_probe,
            illumination_index=illumination_index,
            **kwargs,
        )

        # add positions
        nf_S["r_probe"] = nf_S["tot"].get_positions()

        # overwrite Field instances by the Poynting vectors
        for which in ["tot", "sca", "inc"]:
            nf_S[which] = nf_S[which].get_poynting()

        return nf_S

    def get_energy_flux(
        self, wavelength, r_probe=None, illumination_index=None, **kwargs
    ):
        """calculate the energy flux (time averaged Poynting vector) at positions `r_probe`

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.fields.nf`.

        Args:
            sim (:class:`torchgdm.Simulation`): simulation instance
            wavelength (float): evaluation wavelength (in nm)
            r_probe (dict, optional): probe locations describing dict (gen. from `tools.geometry`).  Defaults to None, in which case all positions of the simulation structures are used
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.

        Returns:
            dict: results for total, scattered and incident field's time averaged Poynting vector (keys: "tot", "sca", "inc")
        """
        nf_S = self.get_nearfield(
            wavelength=wavelength,
            r_probe=r_probe,
            illumination_index=illumination_index,
            **kwargs,
        )

        # add positions
        nf_S["r_probe"] = nf_S["tot"].get_positions()

        # overwrite Field instances by the time averaged Poynting vectors
        for which in ["tot", "sca", "inc"]:
            nf_S[which] = nf_S[which].get_energy_flux()

        return nf_S

    def get_green(
        self,
        r_probe: torch.Tensor,
        r_source: torch.Tensor,
        wavelength: float,
        use_sim_copy=True,
        progress_bar=True,
        verbose=0,
        **kwargs,
    ):
        """calculate the Green's tensor in presence of the structure(s)

        kwargs (such as `batch_size`) are passed to :func:`tg.postproc.green.G`.

        Args:
            sim (`torchgdm.Simulation`): simulation
            r_probe (torch.Tensor): probe position(s)
            r_source (torch.Tensor): source location(s)
            wavelength (float): in nm
            use_sim_copy (bool, optional): Use copy of simulation or use simulation in-place. May not work in some autograd scenario. Defaults to True.
            progress_bar (bool, optional): Show progress bar. Defaults to True.
            verbose (bool, optional): Print status of underlying simulation call. Defaults to False.

        Returns:
            dict: Green's tensors for all source/probe position combinations:
                - "G_6x6": full 6x6 tensor
                - "G_Ep": electric-electric 3x3 tensor
                - "G_Em": electric-magnetic 3x3 tensor
                - "G_Hp": magnetic-electric 3x3 tensor
                - "G_Hm": magnetic-magnetic 3x3 tensor
        """
        import torchgdm as tg

        if r_probe is None:
            r_probe = self.get_all_positions()

        G = tg.postproc.green.G(
            self,
            r_probe=r_probe,
            r_source=r_source,
            wavelength=wavelength,
            use_sim_copy=use_sim_copy,
            progress_bar=progress_bar,
            verbose=verbose,
            **kwargs,
        )

        return G

    def get_ldos(
        self,
        r_probe: torch.Tensor,
        wavelength: float,
        progress_bar=True,
        verbose=False,
        **kwargs,
    ):
        """calculate the LDOS close to the structure(s)

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.fields.nf`.

        Args:
            sim (`torchgdm.Simulation`): simulation
            r_probe (torch.Tensor): probe position(s)
            wavelength (float): in nm
            progress_bar (bool, optional): Show progress bar. Defaults to True.
            verbose (bool, optional): Print status info. Defaults to False.


        Returns:
            dict: Green's tensors, partial and averaged LDOS all probe positions:
                - "G_ii": full 6x6 tensor
                - "ldos_partial": partial electric (first 3) and magnetic (last 3) LDOS. (Diagonal elements of Green's tensor)
                - "ldos_e": full electric LDOS
                - "ldos_m": full magnetic LDOS
        """
        import torchgdm as tg

        if r_probe is None:
            r_probe = self.get_all_positions()

        ldos = tg.postproc.green.ldos(
            self,
            r_probe=r_probe,
            wavelength=wavelength,
            progress_bar=progress_bar,
            verbose=verbose,
            **kwargs,
        )

        return ldos

    def get_farfield(self, wavelength, r_probe, illumination_index=None, **kwargs):
        """calculate the far-field (electric and magnetic) at positions `r_probe`

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.fields.nf`.

        Args:
            sim (:class:`torchgdm.Simulation`): simulation instance
            wavelength (float): evaluation wavelength (in nm)
            r_probe (dict, optional): probe locations describing dict (gen. from `tools.geometry`). Defaults to None, in which case full hemisphere coordinates are used
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.

        Returns:
            dict: results for total, scattered and incident fields in instances of :class:`torchgdm.Field`
        """
        import torchgdm as tg

        ff = tg.postproc.fields.ff(
            self,
            wavelength=wavelength,
            r_probe=r_probe,
            illumination_index=illumination_index,
            **kwargs,
        )

        return ff

    def get_ff(self, **kwargs):
        """alias for :meth:`Simulation.get_farfield`"""
        return self.get_farfield(**kwargs)

    # - rasterscan
    def get_rasterscan(self, func, wavelength, kw_r="r_focus", **kwargs):
        """Get rasterscan from a "scan-position" parameters `kw_r` and evaluation function `func`

        `kw_r` must be an attribute of the available illuminations, defining
        some position (3-tuple), this is used as the raster-scan position for each evaluation.

        kwargs are passed to `func`.

        Args:
            func (callable): postprocessing function, from :mod:`tg.postproc`
            wavelength (float): evaluation wavelength (in nm)
            kw_r (str): kwarg used for scan position of rasterscan

        Returns:
            dict: spectrum results
        """
        from torchgdm.tools.batch import calc_rasterscan

        rs_res = calc_rasterscan(self, func, wavelength=wavelength, kw_r=kw_r)
        return rs_res

    # - spectra
    def get_spectra(self, func, **kwargs):
        """Get spectra using all available wavelengths for evaluation function `func`

        kwargs are passed to `func`

        Args:
            func (callable): postprocessing function, from :mod:`tg.postproc`

        Returns:
            dict: spectrum results
        """
        from torchgdm.tools.batch import calc_spectrum

        nf_spec = calc_spectrum(self, func, **kwargs)
        return nf_spec

    def get_spectra_scs(self, **kwargs):
        """total scattering, absorption and extinction cross section spectra

        This function also returns extinction and absorption cross-sections, which are calculated as byproducts.

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.crosssect.scs`.

        Args:
            sim (:class:`torchgdm.Simulation`): simulation instance
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.
            normalize_to_local_e0 (bool, optional): Whether to normalize to local illumination amplitude. Can be useful to get an approximate cross-section for non-plane wave illuminations. Defaults to False.
            radiative_correction (bool, optional): Whether to add radiative correction term. Defaults to True.

        Returns:
            dict: dictionaty containing the scattering, absorption and extinction cross section spectra
        """
        import torchgdm as tg

        scs_spec = tg.tools.batch.calc_spectrum(
            self, tg.postproc.crosssect.scs, **kwargs
        )
        return scs_spec

    def get_spectra_crosssections(self, **kwargs):
        """total scattering, absorption and extinction cross section spectra

        *Note:* this is an alias for :func:`Simulation.get_spectra_scs`.

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.crosssect.scs`.

        Args:
            sim (:class:`torchgdm.Simulation`): simulation instance
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.
            normalize_to_local_e0 (bool, optional): Whether to normalize to local illumination amplitude. Can be useful to get an approximate cross-section for non-plane wave illuminations. Defaults to False.
            radiative_correction (bool, optional): Whether to add radiative correction term. Defaults to True.

        Returns:
            dict: dictionaty containing the scattering, absorption and extinction cross section spectra
        """
        return self.get_spectra_scs(**kwargs)

    def get_spectra_ecs(self, **kwargs):
        """total exctinction cross section spectra

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.crosssect.ecs`.

        Args:
            sim (:class:`torchgdm.Simulation`): simulation instance
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.
            normalize_to_local_e0 (bool, optional): Whether to normalize to local illumination amplitude. Can be useful to get an approximate cross-section for non-plane wave illuminations. Defaults to False.

        Returns:
            dict: dictionaty containing the extinction cross section spectra
        """
        import torchgdm as tg

        ecs_spec = tg.tools.batch.calc_spectrum(
            self, tg.postproc.crosssect.ecs, **kwargs
        )
        return ecs_spec

    def get_spectra_acs(self, **kwargs):
        """total absorption cross section spectra

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.crosssect.acs`.

        Args:
            sim (:class:`torchgdm.Simulation`): simulation instance
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.
            normalize_to_local_e0 (bool, optional): Whether to normalize to local illumination amplitude. Can be useful to get an approximate cross-section for non-plane wave illuminations. Defaults to False.

        Returns:
            dict: dictionaty containing the absorption cross section spectra
        """
        import torchgdm as tg

        ecs_spec = tg.tools.batch.calc_spectrum(
            self, tg.postproc.crosssect.ecs, **kwargs
        )
        return ecs_spec

    def get_spectra_nf(self, r_probe=None, **kwargs):
        """Get spectra of complex nearfields at all available wavelengths at positions `r_probe`

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.fields.nf`.

        Args:
            r_probe (dict, optional): probe locations describing dict (gen. from `tools.geometry`). Defaults to None, in which case all positions of the simulation structures are used
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.

        Returns:
            dict: contains results for total, scattered and incident fields in instances of :class:`torchgdm.Field`
        """
        import torchgdm as tg

        if r_probe is None:
            r_probe = self.get_all_positions()

        nf_spec = tg.tools.batch.calc_spectrum(
            self, tg.postproc.fields.nf, r_probe=r_probe, **kwargs
        )
        return nf_spec

    def get_spectra_nf_intensity_e(self, r_probe=None, **kwargs):
        """Get spectrum of electric nearfield intensities, integrated over probe points

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.fields.nf`.

        Args:
            r_probe (dict, optional): probe locations describing dict (gen. from `tools.geometry`). Defaults to None, in which case all positions of the simulation structures are used
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.

        Returns:
            dict: contains results for total (key "tot"), scattered (key "sca") and incident (key "inc") electric field intensity
        """
        nf_spec = self.get_spectra_nf(r_probe=r_probe, **kwargs)

        for which in ["tot", "sca", "inc"]:
            nf_spec[which] = torch.stack(
                [f.get_integrated_efield_intensity() for f in nf_spec[which]]
            )

        return nf_spec

    def get_spectra_nf_intensity_h(self, r_probe=None, **kwargs):
        """Get spectrum of magnetic nearfield intensities, integrated over probe points

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.fields.nf`.

        Args:
            r_probe (dict, optional): probe locations describing dict (gen. from `tools.geometry`). Defaults to None, in which case all positions of the simulation structures are used
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.

        Returns:
            dict: contains results for total (key "tot"), scattered (key "sca") and incident (key "inc") magnetic field intensity
        """
        nf_spec = self.get_spectra_nf(r_probe=r_probe, **kwargs)

        for which in ["tot", "sca", "inc"]:
            nf_spec[which] = torch.stack(
                [f.get_integrated_hfield_intensity() for f in nf_spec[which]]
            )

        return nf_spec

    def get_spectra_nf_intensity_e_inside(self):
        """Get spectrum of averaged electric nearfield intensities inside structure"""
        import torchgdm as tg

        nf_int_e = tg.tools.batch.calc_spectrum(
            self, tg.postproc.fields.integrated_nf_intensity_e_inside
        )

        return nf_int_e

    def get_spectra_nf_intensity_h_inside(self):
        """Get spectrum of averaged magnetic nearfield intensities inside structure"""
        import torchgdm as tg

        nf_int_h = tg.tools.batch.calc_spectrum(
            self, tg.postproc.fields.integrated_nf_intensity_h_inside
        )

        return nf_int_h

    def get_spectra_ff(self, r_probe=None, **kwargs):
        """Get spectra of complex far-fields at all available wavelengths at positions `r_probe`

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.fields.ff`.

        Args:
            sim (:class:`torchgdm.Simulation`): simulation instance
            r_probe (dict, optional): probe locations describing dict (gen. from `tools.geometry`). Defaults to None, in which case all positions of the simulation structures are used
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.

        Returns:
            dict: contains results for total, scattered and incident fields in instances of :class:`torchgdm.Field`
        """
        import torchgdm as tg

        ff_spec = tg.tools.batch.calc_spectrum(
            self, tg.postproc.fields.ff, r_probe=r_probe, **kwargs
        )
        return ff_spec

    def get_spectra_ff_intensity(self, r_probe=None, **kwargs):
        """Get spectrum of integrated far-field intensities

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.fields.ff`.

        Args:
            sim (:class:`torchgdm.Simulation`): simulation instance
            r_probe (dict or list, optional): probe locations (gen. from `tools.geometry`). Defaults to None, in which case intergration goes over full hemisphere
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.

        Returns:
            dict: contains results for total (key "tot"), scattered (key "sca") and incident (key "inc") far-field intensity
        """
        ff_spec = self.get_spectra_ff(r_probe, **kwargs)

        for which in ["tot", "sca", "inc"]:
            ff_spec[which] = torch.stack(
                [f.get_integrated_efield_intensity() for f in ff_spec[which]]
            )

        return ff_spec

    def get_spectra_multipole(self, **kwargs):
        """Get spectrum of exact multipole decomposition

        This returns the spectra for the full multipole moments of dipole and quadrupole order.
        For more detailed documentation, see :func:`torchgdm.postproc.multipole.decomposition_exact`.
        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.multipole.decomposition_exact`.

        Args:
            sim (:class:`torchgdm.Simulation`): simulation instance
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.
            r0 (torch.Tensor, optional): [x,y,z] position of multipole decomposition development. Defaults to None, in which case the center of gravity is used.
            epsilon (float, optional): positions too close to r0 will moved away from r0 by epsilon (in units of step) to avoid numerical divergence of the Bessel terms. Defaults to 0.1.
            long_wavelength_approx (bool, optional): if True, use long wavelength approximation. Defaults to False.

        Returns:
            dict: each element contains the spectrum for one multipole moment. dipoles are rank-1 (3-vectors), quadrupoles are rank 2 (3x3 tensors):
                - 'ed_tot': electric dipole (full)
                - 'md': magnetic dipole
                - 'eq_tot': electric quadrupole (full)
                - 'mq': magnetic quadrupole
                - 'ed_1': electric dipole (first order)
                - 'ed_toroidal': toroidal dipole
                - 'eq1': electric quadrupole (first order)
                - 'eq_toroidal': toroidal quadrupole
        """
        import torchgdm as tg

        mpd_spec = tg.tools.batch.calc_spectrum(
            self, tg.postproc.multipole.decomposition_exact, **kwargs
        )
        return mpd_spec

    def get_spectra_multipole_scs(self, **kwargs):
        """spectra of multipole decomposition of extinction cross section

        Returns the exact multipole decomposition of the extinction cross section spectra: electric and magnetic dipole and quadrupole moments.
        For more detailed documentation, see :func:`torchgdm.postproc.multipole.ecs`.
        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.multipole.ecs`.

        For details about the extinction section of multipole moments, see:
            Evlyukhin, A. B. et al. *Multipole analysis of light scattering by
            arbitrary-shaped nanoparticles on a plane surface.*,
            JOSA B 30, 2589 (2013)

        Args:
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.
            r0 (torch.Tensor, optional): [x,y,z] position of multipole decomposition development. Defaults to None, in which case the center of gravity is used.
            epsilon (float, optional): positions too close to r0 will moved away from r0 by epsilon (in units of step) to avoid numerical divergence of the Bessel terms. Defaults to 0.1.
            eps_dd (float, optional): numerical integration step for field gradients calc. (in nm). Required for e/m quadrupoles. Defaults to 0.1.
            normalization_E0 (bool, optional): Normalize to illumination amplitude at `r0`. Can be useful to get approximate results for non-plane wave illumination. Defaults to False.
            long_wavelength_approx (bool, optional): if True, use long wavelength approximation. Defaults to False.

        Returns:
            dict:
            - 'ecs_ed': electric dipole extinction cross section spectra (in nm^2)
            - 'ecs_md': magnetic dipole extinction cross section spectra (in nm^2)
            - 'ecs_eq': electric quadrupole extinction cross section spectra (in nm^2)
            - 'ecs_mq': magnetic quadrupole extinction cross section spectra (in nm^2)
        """
        import torchgdm as tg

        scs_mpd_spec = tg.tools.batch.calc_spectrum(
            self, tg.postproc.multipole.scs, **kwargs
        )
        return scs_mpd_spec

    def get_spectra_multipole_ecs(self, **kwargs):
        """spectrum of multipole decomposition of scattering cross section

        Returns the exact multipole decomposition of the scattering cross section spectra: electric and magnetic dipole and quadrupole moments.
        For more detailed documentation, see :func:`torchgdm.postproc.multipole.scs`.
        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.multipole.scs`.

        For details about the exact multipole formalism and scs calculation, see:
            Alaee, R., Rockstuhl, C. & Fernandez-Corbaton, I. *An electromagnetic
            multipole expansion beyond the long-wavelength approximation.*
            Optics Communications 407, 17–21 (2018)

        Args:
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.
            with_toroidal (bool, optional): whether to add toroidal moments to electric dipole and quadrupole. Defaults to True.
            r0 (torch.Tensor, optional): [x,y,z] position of multipole decomposition development. Defaults to None, in which case the center of gravity is used.
            epsilon (float, optional): positions too close to r0 will moved away from r0 by epsilon (in units of step) to avoid numerical divergence of the Bessel terms. Defaults to 0.1.
            normalization_E0 (bool, optional): Normalize to illumination amplitude at `r0`. Can be useful to get approximate results for non-plane wave illumination. Defaults to False.
            long_wavelength_approx (bool, optional): if True, use long wavelength approximation. Defaults to False.

        Returns:
            dict:
            - 'scs_ed': electric dipole scattering cross section spectra (in nm^2)
            - 'scs_md': magnetic dipole scattering cross section spectra (in nm^2)
            - 'scs_eq': electric quadrupole scattering cross section spectra (in nm^2)
            - 'scs_mq': magnetic quadrupole scattering cross section spectra (in nm^2)
        """
        import torchgdm as tg

        scs_mpd_spec = tg.tools.batch.calc_spectrum(
            self, tg.postproc.multipole.ecs, **kwargs
        )
        return scs_mpd_spec

    def get_spectra_chirality(self, r_probe=None, whichfield="tot", **kwargs):
        """Get spectra of nearfield chirality at positions `r_probe`

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.fields.chirality`.

        Args:
            r_probe (dict, optional): probe locations describing dict (gen. from `tools.geometry`). Defaults to None, in which case all positions of the simulation structures are used
            whichfield (str, optional): which field to use. One of ["inc", "sca", "tot"]. Defaults to "tot".
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.

        Returns:
            dict: contains results for chirality as key "chirality"
        """
        import torchgdm as tg

        if r_probe is None:
            r_probe = self.get_all_positions()

        nf_chirality = tg.tools.batch.calc_spectrum(
            self,
            tg.postproc.fields._chirality,
            r_probe=r_probe,
            whichfield=whichfield,
            **kwargs,
        )
        return nf_chirality

    def get_spectra_LDOS(self, r_probe=None, **kwargs):
        """Get spectra of the LDOS at positions `r_probe`

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.green.ldos`.

        Args:
            r_probe (dict, optional): probe locations describing dict (gen. from `tools.geometry`). Defaults to None, in which case all positions of the simulation structures are used

        Returns:
            dict: spectra results for Green's tensors, partial and averaged LDOS all probe positions:
                - "G_ii": full 6x6 tensor
                - "ldos_partial": partial electric (first 3) and magnetic (last 3) LDOS. (Diagonal elements of Green's tensor)
                - "ldos_e": full electric LDOS
                - "ldos_m": full magnetic LDOS
        """
        import torchgdm as tg

        if r_probe is None:
            r_probe = self.get_all_positions()

        spec_ldos = tg.tools.batch.calc_spectrum(
            self, tg.postproc.green.ldos, r_probe=r_probe, **kwargs
        )
        return spec_ldos

    def get_spectra_green(self, r_probe, r_source, **kwargs):
        """Get spectra of the Green's tensor at positions `r_probe`

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.green.G`.

        Args:
            r_probe (torch.Tensor): probe position(s)
            r_source (torch.Tensor): source location(s)

        Returns:
            dict: spectra of the Green's tensors for all source/probe position combinations:
                - "G_6x6": full 6x6 tensor
                - "G_Ep": electric-electric 3x3 tensor
                - "G_Em": electric-magnetic 3x3 tensor
                - "G_Hp": magnetic-electric 3x3 tensor
                - "G_Hm": magnetic-magnetic 3x3 tensor
        """
        import torchgdm as tg

        if r_probe is None:
            r_probe = self.get_all_positions()

        spec_G = tg.tools.batch.calc_spectrum(
            self, tg.postproc.green.G, r_probe=r_probe, r_source=r_source, **kwargs
        )
        return spec_G

    # --- convenience plotting wrapper
    def plot_structure(self, **kwargs):
        """2D plot of the structure

        for doc, see :func:`torchgdm.visu.visu2d.structure`
        """
        from torchgdm.visu import visu2d

        visu2d.structure(self, **kwargs)

    def plot_contour(self, **kwargs):
        """2D plot of the structure contour

        for doc, see :func:`torchgdm.visu.visu2d.contour`
        """
        from torchgdm.visu import visu2d

        visu2d.contour(self, **kwargs)

    def plot_structure_3d(self, **kwargs):
        """3D plot of the structure

        for doc, see :func:`torchgdm.visu.visu3d.structure`
        """
        from torchgdm.visu import visu3d

        visu3d.structure(self, **kwargs)

    def plot_efield_vectors_inside(self, wavelength, illumination_index=0, **kwargs):
        """quiver plot of 2d projection of the internal E-field

        for doc, see :func:`torchgdm.visu.visu2d.vectorfield_inside`
        """
        from torchgdm.visu import visu2d

        visu2d.vectorfield_inside(
            self,
            wavelength=wavelength,
            illumination_index=illumination_index,
            whichfield="e",
            **kwargs,
        )

    def plot_hfield_vectors_inside(self, wavelength, illumination_index=0, **kwargs):
        """quiver plot of 2d projection of the internal H-field

        for doc, see :func:`torchgdm.visu.visu2d.vectorfield_inside`
        """
        from torchgdm.visu import visu2d

        visu2d.vectorfield_inside(
            self,
            wavelength=wavelength,
            illumination_index=illumination_index,
            whichfield="h",
            **kwargs,
        )

    def plot_efield_vectors_inside_3d(
        self, wavelength, illumination_index=0, scale=1, **kwargs
    ):
        """3D quiver plot of the internal E-field

        for doc, see :func:`torchgdm.visu.visu3d.vectorfield_inside`
        """
        from torchgdm.visu import visu3d

        visu3d.vectorfield_inside(
            self,
            wavelength=wavelength,
            illumination_index=illumination_index,
            whichfield="e",
            scale=25 * scale,
            **kwargs,
        )

    def plot_hfield_vectors_inside_3d(
        self, wavelength, illumination_index=0, scale=1, **kwargs
    ):
        """3D quiver plot of the internal H-field

        for doc, see :func:`torchgdm.visu.visu3d.vectorfield_inside`
        """
        from torchgdm.visu import visu3d

        visu3d.vectorfield_inside(
            self,
            wavelength=wavelength,
            illumination_index=illumination_index,
            whichfield="h",
            scale=25 * scale,
            **kwargs,
        )
