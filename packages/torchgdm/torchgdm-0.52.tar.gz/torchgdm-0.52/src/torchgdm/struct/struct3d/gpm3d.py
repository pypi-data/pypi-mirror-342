"""
global polarizability matrix (GPM) module

see:
Bertrand, M., Devilez, A., Hugonin, J.-P., Lalanne, P. & Vynck, K.
*Global polarizability matrix method for efficient modeling of light scattering by dense ensembles of non-spherical particles in stratified media.*
JOSA A 37, 70-83 (2020)
DOI: 10.1364/JOSAA.37.000070

author: P. Wiecha, 03/2025
"""

import warnings

import torch
from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX
from torchgdm.struct.base_classes import StructBase
from torchgdm.tools.geometry import get_enclosing_sphere_radius
from torchgdm.tools.geometry import test_structure_distances
from torchgdm.tools.geometry import rotation_x, rotation_y, rotation_z
from torchgdm.tools import interp
from torchgdm.tools.misc import ptp


class StructGPM3D(StructBase):
    """3D global polarizability matrix structure

    Defines a GPM-based structure

    for details about GPM, see:

    Bertrand, M., Devilez, A., Hugonin, J.-P., Lalanne, P. & Vynck, K.
    *Global polarizability matrix method for efficient modeling of light scattering by dense ensembles of non-spherical particles in stratified media.*
    JOSA A 37, 70-83 (2020), DOI: 10.1364/JOSAA.37.000070
    """

    __name__ = "global polarizability matrix 3D structure class"

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
        """3D global polarizability matrix (GPM) class

        The main information is provided in the `gpm_dicts` argument, which is a list of dicts with the full global polarizability matrix definitions. Each dict defines one structure and must contain following:
            - 'wavelengths': wavelengths at which the polarizabilities are calculated
            - 'GPM_N6xN6':
                6N x 6N global polarizability tensors, each of shape [len(wavelengths),6N,6N]. Each 6x6 sub-matrix describes electric and magnetic dipole moments induced by and electric and magentic field.
                N is the number of dipole pairs for the GPM. Caution! All GPMs in one structure must have the same number of dipoles.
            optional keys:
            - 'full_geometry': the original volume discretization of the represented geometry
            - 'r0': the origin of the effective polarizabilities with respect to optional 'full_geometry'
            - 'enclosing_radius': enclosing radius of the original structure

        Args:
            positions (torch.Tensor): positions of the individual GPMs (same size as `gpm_dicts`)
            gpm_dicts (list): list of polarizability model dictionaries (same size as `positions`)
            radiative_correction (bool, optional): Whether to add raditative correction for cross section calculations. Defaults to True.
            device (torch.device, optional): Defaults to "cpu".
            environment (environment instance, optional): 3D environment class. Defaults to None.
            shift_z_to_r0 (bool, optional): If True, if a position z-value is zero, each polarizability model's z position will be shifted to the height of the effective dipole development center. Defaults to True.
            progress_bar (bool optional): whether to show progress bars on internal compute. Defaults to True.

        Raises:
            ValueError: _description_
        """
        super().__init__(device=device)

        self.n_dim = 3
        self.interaction_type = "EH"
        self.gpm_dict = gpm_dicts

        # expand positions, put single scatterer in list
        move_positions = torch.as_tensor(
            positions, dtype=DTYPE_FLOAT, device=self.device
        )
        move_positions = torch.atleast_2d(move_positions)
        assert move_positions.shape[1] == 3

        self.radiative_correction = radiative_correction

        # single alpha_dict: put in list
        if type(gpm_dicts) == dict:
            gpm_dicts = [gpm_dicts] * len(move_positions)
        for _gd in gpm_dicts:
            assert type(_gd) == dict

        # environment at which alpha has been extracted (if given):
        if environment is None:
            self.environment = gpm_dicts[0]["environment"]
        else:
            warnings.warn("Using different environment than specified in GPM-dict.")
            self.environment = environment
        self.progress_bar = progress_bar

        for _adict in gpm_dicts:
            assert "wavelengths" in _adict
            if "GPM_N6xN6" not in _adict:
                raise ValueError(
                    "Global polarizability matrix description dicts must contain GPM tensors "
                    + "under the dict key: 'GPM_N6xN6'."
                )
            if "r_gpm" not in _adict:
                raise ValueError(
                    "Global polarizability matrix description dicts must contain GPM position tensors "
                    + "under the dict key: 'r_gpm'."
                )

        # use first pola-tensor wavelength range
        wavelengths = gpm_dicts[0]["wavelengths"]
        n_dp_gpm = len(gpm_dicts[0]["r_gpm"])
        self.wavelengths_data = torch.as_tensor(
            wavelengths, dtype=DTYPE_FLOAT, device=self.device
        )

        for _adict in gpm_dicts:
            _wls = torch.as_tensor(
                _adict["wavelengths"], dtype=DTYPE_FLOAT, device=self.device
            )
            if len(_adict["r_gpm"]) != n_dp_gpm:
                raise ValueError(
                    "All GPMs must have the same number of dipoles, if several GPMs are combined in one structure."
                )
            if not torch.all(torch.isin(self.wavelengths_data, _wls)):
                warnings.warn(
                    "Pre-calculated wavelengths of the structures are not identical. "
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
            for i, p in enumerate(move_positions):
                if p[2] == 0:
                    p[2] = torch.as_tensor(
                        gpm_dicts[i]["r0"][2], dtype=p.dtype, device=p.device
                    )

        # populate polarizability tensors database for each position at
        # pre-calculated wavelengths. if necessary, interpolate between data points
        gpm_pos = []
        gpm_data = []
        reduced_step = []
        full_geometries = []
        for i, _adict in enumerate(gpm_dicts):
            gpm_pos.append(
                _adict["r_gpm"] - _adict["r0"] + move_positions[i].unsqueeze(0)
            )
            if torch.all(_adict["wavelengths"] == self.wavelengths_data):
                _gpm = _adict["GPM_N6xN6"]
            else:
                # if requested other wavelengths than given, interpolate
                _gpm = self._interpolate_single_alpha(
                    wls=self.wavelengths_data,
                    gpm_data=_adict["GPM_N6xN6"],
                    wl_data=_adict["wavelengths"],
                )
            gpm_data.append(_gpm)

            # optional values
            if "full_geometry" in _adict:
                full_geometries.append(
                    torch.as_tensor(
                        _adict["full_geometry"] - _adict["r0"],
                        dtype=DTYPE_FLOAT,
                        device=self.device,
                    )
                    + move_positions[i]
                )

            if "enclosing_radius" in _adict:
                _rstep = _adict["enclosing_radius"] * 2
            else:
                if "full_geometry" in _adict:
                    _r_eff = get_enclosing_sphere_radius(full_geometries[-1])
                    _rstep = _r_eff
                else:
                    _rstep = 0
            reduced_step += [_rstep / n_dp_gpm**0.66] * n_dp_gpm

        self.full_geometries = full_geometries

        # effective polarizabilities of each meshpoint at each wavelength: shape (Npos, Nwl, 6, 6)
        if len(gpm_data) != 0:
            self.gpm_data = torch.stack(gpm_data)
            self.gpm_pos = torch.stack(gpm_pos)
        else:
            raise ValueError("Unexpected error: Not GPM data.")

        # selfterms are zero. This acts as a placeholder and is not being used
        self.selfterms_data = torch.zeros_like(self.gpm_data)

        # populate lookup tables
        self.create_lookup()

        # other parameters ("step" corresponds to the effective diameter divided by nr of GPM dipole pairs)
        self.step = torch.as_tensor(reduced_step, dtype=DTYPE_FLOAT, device=self.device)

        # center of gravity of ensemble of all points
        self.r0 = self.get_center_of_mass()

        # set device
        self.set_device(self.device)

    def __repr__(self, verbose=False):
        """description about structure"""
        out_str = ""
        out_str += "------ 3D Global Polarizability Matrix nano-object -------"
        out_str += "\n" + " nr. of GPM structures:  {}".format(self.gpm_pos.shape[0])
        out_str += "\n" + " nr. of dipoles per GPM: {} (each {} ED and MD)".format(
            self.gpm_pos.shape[1] * 2, self.gpm_pos.shape[1]
        )
        out_str += "\n" + " total nr. of dipoles:   {} (each {} ED and MD)".format(
            self.gpm_pos.shape[0] * self.gpm_pos.shape[1] * 2,
            self.gpm_pos.shape[0] * self.gpm_pos.shape[1],
        )
        if len(self.full_geometries) > 0:
            pos = torch.cat(self.full_geometries)
            out_str += "\n" + " original geometry: "
            out_str += "\n" + "  - replacing nr. of meshpoints: {}".format(len(pos))
            bnds = ptp(pos, dim=0)
            out_str += "\n" + "  - size & position:"
            out_str += "\n" + "        X-extension    : {:.1f} (nm)".format(bnds[0])
            out_str += "\n" + "        Y-extension    : {:.1f} (nm)".format(bnds[1])
            out_str += "\n" + "        Z-extension    : {:.1f} (nm)".format(bnds[2])
            out_str += "\n" + "  - center of mass : ({:.1f}, {:.1f}, {:.1f})".format(
                *[float(f) for f in self.get_center_of_mass()]
            )

        return out_str

    def get_all_positions(self) -> torch.Tensor:
        return torch.reshape(self.gpm_pos, (-1, 3))

    def get_r_pm(self):
        """positions of electric and magnetic polarizable dipoles"""
        r_p = self.get_all_positions()
        r_m = self.get_all_positions()
        return r_p, r_m

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

    def get_pm(self, wavelength):
        """self-consistent electric and magnetic dipole moments"""
        gpm = self.get_gpm(wavelength, self.environment)
        f_in = self.get_e_h_selfconsistent(wavelength)
        f_per_gpm = f_in.chunk(chunks=len(self.gpm_pos), dim=1)
        p = []
        m = []
        for i, _f in enumerate(f_per_gpm):
            _f = _f.reshape(len(_f), -1)
            _pm = torch.matmul(gpm[i], _f.unsqueeze(-1))[..., 0]
            _pm = _pm.reshape(len(_pm), -1, 6)
            p.append(_pm[..., :3])
            m.append(_pm[..., 3:])

        p = torch.cat(p, dim=1)
        m = torch.cat(m, dim=1)

        return p, m

    def get_center_of_mass(self) -> torch.Tensor:
        # use full geometries if available
        if len(self.full_geometries) == len(self.gpm_pos):
            r0 = [_pos.mean(dim=0) for _pos in self.full_geometries]
            r0 = torch.stack(r0, axis=0).mean(dim=0)
        else:
            r0 = self.gpm_pos.mean(dim=(0, 1))
        return r0

    def create_lookup(self):
        """Create a lookup table for the polarizability tensors"""
        # populate lookup tables with pre-calculated data
        self.lookup = {}
        for i_wl, wl in enumerate(self.wavelengths_data):
            self.lookup[round(float(wl), 3)] = self.gpm_data[:, i_wl, :, :]

    def set_device(self, device):
        """move all tensors of the class to device"""
        super().set_device(device)
        if self.environment is not None:
            self.environment.set_device(device)

        if len(self.full_geometries) > 0:
            self.full_geometries = [_g.to(device) for _g in self.full_geometries]

        self.step = self.step.to(device)
        self.r0 = self.r0.to(device)
        self.wavelengths_data = self.wavelengths_data.to(device)

        self.gpm_data = self.gpm_data.to(device)
        self.gpm_pos = self.gpm_pos.to(device)
        self.selfterms_data = self.selfterms_data.to(device)

        # transfer the lookup tables
        for wl in self.lookup:
            self.lookup[wl] = self.lookup[wl].to(device)

    def _interpolate_single_alpha(self, wls, gpm_data, wl_data):

        # convert to tensor
        wls = torch.as_tensor(wls, dtype=DTYPE_FLOAT, device=self.device)
        wl_dat = torch.as_tensor(wl_data, dtype=DTYPE_FLOAT, device=self.device)
        gpm_dat = torch.as_tensor(gpm_data, dtype=DTYPE_COMPLEX, device=self.device)

        gpm_size = gpm_dat.shape[1]
        assert gpm_dat.shape[1] == gpm_dat.shape[2]

        # wavelength-interpolation of each tensor component
        a_ip = torch.zeros(
            (len(wls), gpm_size, gpm_size), dtype=DTYPE_COMPLEX, device=self.device
        )

        for i in range(gpm_size):
            for j in range(gpm_size):
                _func_ip = interp.RegularGridInterpolator([wl_dat], gpm_dat[:, i, j])
                _ip = _func_ip([wls])
                a_ip[:, i, j] = _ip

        return a_ip

    def interpolate_alpha(self, wls, a_data_many, wl_data, lookup=None):
        """interpolate the polarizabilities between available wavelengths"""
        from torchgdm.tools.misc import tqdm

        gpm_ip = torch.zeros(
            (
                self.gpm_data.shape[0],
                len(wls),
                self.gpm_data.shape[2],
                self.gpm_data.shape[3],
            ),
            dtype=DTYPE_COMPLEX,
            device=self.device,
        )

        # iterate all polarizabilities (different structures)
        for i_a, a_data in tqdm(
            enumerate(a_data_many),
            title="creating GPM lookup...",
            progress_bar=self.progress_bar,
        ):
            _gpm = self._interpolate_single_alpha(wls, a_data, wl_data)
            gpm_ip[i_a] = _gpm

        # optionally add to lookup
        if lookup is not None:
            for i_wl, wl in enumerate(wls):
                wl = round(float(wl), 3)
                if wl not in lookup:
                    lookup[wl] = gpm_ip[:, i_wl, :, :]

        return gpm_ip

    # --- self-terms
    # self-terms are zero

    # --- polarizabilities
    def _call_interpolation(self, wavelength):
        warnings.warn(
            "Interpolating polarizabilities at wavelength {:.3f}.".format(
                float(wavelength)
            )
        )
        self.interpolate_alpha(
            [wavelength],
            self.gpm_data,
            self.wavelengths_data,
            lookup=self.lookup,
        )

    def get_gpm(self, wavelength: float, environment) -> torch.Tensor:
        """return list of GPM tensors (N_struct, 6N, 6N) of each GPM structure

        Args:
            wavelength (float): in nm

        Returns:
            list of torch.Tensor
        """
        if round(float(wavelength), 3) not in self.lookup:
            self._call_interpolation(wavelength)

        return self.lookup[round(float(wavelength), 3)]

    def get_polarizability_6x6(self, wavelength: float, environment) -> torch.Tensor:
        """return diagonal N6xN6 GPM

        warning: this does not return 6x6 tensors but
        GPMs of shape (N_structure, 6N, 6N)
        """
        return self.get_gpm(wavelength, environment)

    def get_selfterm_6x6(self, wavelength: float, environment) -> torch.Tensor:
        """return diagonal N6xN6 self-terms (zero)

        warning: this does not return 6x6 tensors but
        zeros of shape (N_structure, 6N, 6N)
        """
        return torch.zeros_like(self.gpm_data[:, 0])

    def get_polarizability_pE(self, wavelength: float, environment) -> torch.Tensor:
        raise Exception("GPM does not provide single, local polarizabilities")

    def get_polarizability_mE(self, wavelength: float, environment) -> torch.Tensor:
        raise Exception("GPM does not provide single, local polarizabilities")

    def get_polarizability_pH(self, wavelength: float, environment) -> torch.Tensor:
        raise Exception("GPM does not provide single, local polarizabilities")

    def get_polarizability_mH(self, wavelength: float, environment) -> torch.Tensor:
        raise Exception("GPM does not provide single, local polarizabilities")

    # --- geometry operations
    def translate(self, vector):
        """return a copy moved by `vector`"""

        vector = torch.as_tensor(vector, dtype=DTYPE_FLOAT, device=self.device)
        vector = torch.atleast_2d(vector)
        _shifted = self.copy()

        # shift effective dipole positions of each GPM
        _shifted.gpm_pos = self.gpm_pos + vector.unsqueeze(0)

        if len(_shifted.full_geometries) > 0:
            for _g in _shifted.full_geometries:
                _g += vector

        # shift center of mass positions
        _shifted.r0 = _shifted.get_center_of_mass()

        return _shifted

    def set_center_of_mass(self, r0_new: torch.Tensor):
        """move center of mass to new position `r0_new` (in-place)"""
        r0_new = torch.as_tensor(r0_new, device=self.device)
        r0_old = self.get_center_of_mass()

        if len(r0_new.shape) != 1:
            if len(r0_new) not in [2, 3]:
                raise ValueError("`r0_new` needs to be (X,Y) or (X,Y,Z) tuple.")

        # treat case r0_new is 2D (X,Y)
        if len(r0_new) == 2:
            r0_new = torch.as_tensor(
                [r0_new[0], r0_new[1], r0_old[2]], device=self.device
            )

        # move each dipole to origin, then to new location
        self.gpm_pos -= (r0_old - r0_new).unsqueeze(0).unsqueeze(1)

        if len(self.full_geometries) > 0:
            # move to origin, the to new pos.
            self.full_geometries = [
                _g - (r0_old - r0_new) for _g in self.full_geometries
            ]

        self.r0 = self.get_center_of_mass()

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
        gpm_plot_source_probes=False,
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
            gpm_plot_source_probes (bool, optional): Plot the GPM extraction source and probe locations. Requires `projection` specifically given. Defaults to False.

        Returns:
            matplotlib axes
        """
        from torchgdm.visu import visu2d

        if gpm_plot_source_probes and type(self.gpm_dict) == dict:
            import matplotlib.pyplot as plt
            from torchgdm.tools.misc import to_np

            # - probes
            r_prb = torch.stack([_r for _r in self.gpm_dict["extraction_r_probe"]])
            r_prb = to_np(r_prb + self.r0)
            if projection == "xy":
                ix, iy = 0, 1
            if projection == "xz":
                ix, iy = 0, 2
            if projection == "yz":
                ix, iy = 1, 2
            if projection in ["xy", "xz", "yz"]:
                plt.scatter(
                    r_prb[:, ix],
                    r_prb[:, iy],
                    color="g",
                    marker="o",
                    s=2,
                    label="GPM probes",
                )

            # - sources
            r_src = torch.stack(
                [
                    inc.r_source
                    for inc in self.gpm_dict["extraction_illuminations"]
                    if hasattr(inc, "r_source")
                ]
            )
            r_src = to_np(r_src + self.r0)
            if projection == "xy":
                ix, iy = 0, 1
            if projection == "xz":
                ix, iy = 0, 2
            if projection == "yz":
                ix, iy = 1, 2
            if projection in ["xy", "xz", "yz"]:
                plt.scatter(
                    r_src[:, ix],
                    r_src[:, iy],
                    color="r",
                    marker="x",
                    s=15,
                    label="GPM sources",
                )

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
        from torchgdm.visu.visu2d._tools import _get_axis_existing_or_new
        from torchgdm.visu.visu2d.geo2d import _plot_contour_discretized
        from torchgdm.visu.visu2d.geo2d import _reset_color_iterator

        if reset_color_cycle:
            _reset_color_iterator()

        if len(self.full_geometries) == 0:
            warnings.warn("No mesh grid data available. Skipping.")
            return None
        ax, show = _get_axis_existing_or_new()
        for subgeo in self.full_geometries:
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

    def plot3d(self, **kwargs):
        """plot the point polarizability structure (3D)"""
        from torchgdm.visu import visu3d

        return visu3d.geo3d._plot_structure_eff_3dpola(self, **kwargs)

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

        # rotate GPM positions around `center`
        for i in range(len(_s_rot.gpm_pos)):
            _s_rot.gpm_pos[i] = torch.matmul(
                _s_rot.gpm_pos[i] - (center + self.r0), rot
            ) + (center + self.r0)

        # rotate full discretizations (if available)
        for i_g, _geo in enumerate(_s_rot.full_geometries):
            if len(_geo) > 1:
                _s_rot.full_geometries[i_g] = torch.matmul(
                    _geo - (center + self.r0), rot
                ) + (center + self.r0)
        # rotate GPM extraction probes and sources (if available)
        if type(_s_rot.gpm_dict) == dict:
            _s_rot.gpm_dict["extraction_r_probe"] = torch.matmul(
                _s_rot.gpm_dict["extraction_r_probe"], rot
            )
            for inc in _s_rot.gpm_dict["extraction_illuminations"]:
                if hasattr(inc, "r_source"):
                    inc.r_source = torch.matmul(inc.r_source, rot)

        # rotate all local and non-local polarizability tensors
        rot = rot.to(DTYPE_COMPLEX).unsqueeze(0).unsqueeze(0)
        rotT = rot.transpose(-2, -1)
        N_dp = 2 * self.gpm_pos.shape[1]  # rotate electric / magnetic dps separately
        for i_m in range(N_dp):
            m = 3 * i_m
            for i_n in range(N_dp):
                n = 3 * i_n
                _s_rot.gpm_data[..., m : m + 3, n : n + 3] = torch.matmul(
                    torch.matmul(
                        rotT,
                        _s_rot.gpm_data[..., m : m + 3, n : n + 3],
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

        new_struct.gpm_pos = torch.concatenate([self.gpm_pos, other.gpm_pos], dim=0)
        new_struct.step = torch.concatenate([new_struct.step, other.step], dim=0)

        new_struct.gpm_data = torch.concatenate(
            [new_struct.gpm_data, other.gpm_data], dim=0
        )
        new_struct.selfterms_data = torch.concatenate(
            [new_struct.selfterms_data, other.selfterms_data], dim=0
        )

        # finally, add full geometries lists together
        new_struct.full_geometries = new_struct.full_geometries + other.full_geometries

        new_struct.r0 = new_struct.get_center_of_mass()
        # create lookup
        if refresh_lookup:
            new_struct.create_lookup()

        return new_struct


# --- Mie sphere - GPM3d
class StructMieSphereGPM3D(StructGPM3D):
    """class for Mie-theory based 3D GPM

    Defines a global polarizability matrix structure representing a core-shell sphere.
    Caution, GPM is an empirical model, its accuracy depends on a successful extraction procedure.

    Requires external package `treams`
    !!! class constructor does not support automatic differentiation !!!

    """

    __name__ = "Mie-theory sphere GPM (3D) structure class"

    def __init__(
        self,
        r_gpm: torch.Tensor,
        wavelengths: torch.Tensor,
        radii: list,
        materials: list,
        lmax=5,
        environment=None,
        r0: torch.Tensor = None,
        device: torch.device = None,
        verbose=True,
        progress_bar=True,
        **kwargs,
    ):
        """3D GPM class for a core-shell sphere (Mie)

        Use Mie theory to get an effective GPM model for a core-shell sphere.
        Requires the `treams` package for Mie coefficient calculation.
        https://github.com/tfp-photonics/treams

        `pip install treams`

        Args:
            r_gpm (int or torch.Tensor): Either int: number of positions or a torch.Tensor of shape (N, 3), giving the locations where to place effective dipole pairs.
            wavelengths (torch.Tensor): list of wavelengths to evaluate (nm)
            radii (list): list of the sphere's core and (multiple) shell radii (in nm).
            materials (list): materials of core and shell(s). A float or int is interpreted as permittivity value.
            lmax (int, optional): maximum order of Mie expansion. Defaults to 5.
            environment (environment instance, optional): Homogeneous 3D environment to evaluate Mie theory in. Defaults to None, which uses vacuum.
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
        env = _check_environment(environment, N_dim=3, device=device)

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
        tmatrix_list = []
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
            mat_treams.append(treams.Material(eps_env))

            tmatrix_list.append(
                treams.TMatrix.sphere(lmax, to_np(k0[i_wl]), radii, mat_treams)
            )

        dict_gpm = extract_gpm_from_tmatrix(
            tmatrix_list,
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


class StructTMatrixGPM3D(StructGPM3D):
    """class for T-Matrix based 3D GPM

    Defines a global polarizability matrix structure approximating T-Matrices.
    Caution, GPM is an empirical model, its accuracy depends on a successful extraction procedure.

    Requires external package `treams`
    !!! class constructor does not support automatic differentiation !!!

    """

    __name__ = "T-Matrix based GPM (3D) structure class"

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
        """3D GPM class to approximate an arbitrary T-Matrix

        Use `treams` to extract an effective GPM model for a T-Matrix (or a list of).
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
        from torchgdm.tools.tmatrix import _test_effective_model_accuracy_3d

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
            _test_results = _test_effective_model_accuracy_3d(
                self, dict_gpm["t_matrices"]
            )
