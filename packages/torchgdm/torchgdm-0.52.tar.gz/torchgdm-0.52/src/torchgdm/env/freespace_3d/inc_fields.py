# -*- coding: utf-8 -*-
"""
illumination fields for torchgdm
"""
import warnings

import torch

from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX
from torchgdm.tools.misc import get_default_device
from torchgdm.env.base_classes import IlluminationfieldBase
from torchgdm.tools.geometry import rotation_x, rotation_y, rotation_z


# ==============================================================================
# field generator classes
# ==============================================================================
class NullField(IlluminationfieldBase):
    """Zero-Field

    all additional kwargs are ignored

    """

    __name__ = "null field"

    def __init__(self, device: torch.device = None):
        super().__init__(device=device)
        self.n_dim = 3

    def set_device(self, device):
        super().set_device(device)

    def get_efield(self, r_probe: torch.Tensor, wavelength: float, environment):
        """evaluate illumination field at position(s) `r_probe`"""
        if len(r_probe.shape) == 1:
            r_probe = r_probe.unsqueeze(0)
        assert r_probe.shape[1] == 3

        return torch.zeros((len(r_probe), 3), dtype=DTYPE_COMPLEX, device=self.device)

    def get_hfield(self, r_probe: torch.Tensor, wavelength: float, environment):
        """evaluate illumination field at position(s) `r_probe`"""
        if len(r_probe.shape) == 1:
            r_probe = r_probe.unsqueeze(0)
        assert r_probe.shape[1] == 3

        return torch.zeros((len(r_probe), 3), dtype=DTYPE_COMPLEX, device=self.device)


class _PlaneWaveNormalInc(IlluminationfieldBase):
    """Simple plane wave in homogeneous environment, normal incidence (along z)

    The polarization state can be defined in different ways. The s- and p-polarization
    complex amplitudes can be defined with a relative phase using. Alternatively a
    relative phase (in rad) can be given for the s-polarization component.

    Parameters
    ----------
    e0x : complex, default: 1.0
        E_x constant amplitude factor (complex for possible phase wrt E_y)

    e0y : complex, default: 0.0
        E_y constant amplitude factor (complex for possible phase wrt E_x)

    k_z_sign : int, default: -1
        sign of z-wavenumber (incidence direction).
        +1: towards increasing z, -1: towards smaller z (default)

    """

    __name__ = "normal incidence plane wave"

    def __init__(
        self,
        e0x: complex = 1.0,
        e0y: complex = 0.0,
        k_z_sign: float = -1.0,
        absolute_phase: float = 0.0,
        device: torch.device = None,
    ):
        super().__init__(device=device)
        self.n_dim = 3

        self.e0x = e0x
        self.e0y = e0y
        self.k_z_sign = k_z_sign
        self.absolute_phase = absolute_phase
        if self.k_z_sign not in [-1, 1]:
            raise ValueError("planewave: kSign must be either +1 or -1!")

        warnings.warn(
            "`_IlluminationPlaneWave_simple` is deprecated. Will be removed soon."
        )

    def set_device(self, device):
        super().set_device(device)

    def __repr__(self, verbose=False):
        out_str = " ------ {} -------".format(self.__name__)
        out_str += "\n - pol: {} ex + {} ey ".format(self.e0x, self.e0y)
        out_str += "\n - sign(k_z): {}".format(self.k_z_sign)

        return out_str

    def get_info(self):
        return dict(
            name="plane wave",
            e0x=self.e0x,
            e0y=self.e0y,
            k_z_sign=self.k_z_sign,
            abs_phase=self.absolute_phase,
        )

    def _eval_field(
        self,
        r_probe: torch.Tensor,
        wavelength: float,
        environment,
    ):
        eps_env = environment.get_environment_permittivity_scalar(
            wavelength, r_probe=r_probe
        )
        n_env = eps_env**0.5

        k_z = self.k_z_sign * n_env * (2 * torch.pi / wavelength)  # incidence along z

        field_x = torch.ones(len(r_probe), dtype=DTYPE_COMPLEX, device=self.device)
        field_y = torch.ones(len(r_probe), dtype=DTYPE_COMPLEX, device=self.device)
        field_z = torch.zeros(len(r_probe), dtype=DTYPE_COMPLEX, device=self.device)

        phase_factor = torch.exp(1j * (k_z * r_probe[:, 2] + self.absolute_phase))
        field_x *= self.e0x * phase_factor
        field_y *= self.e0y * phase_factor

        return field_x, field_y, field_z

    def get_efield(self, r_probe: torch.Tensor, wavelength: float, environment):
        """evaluate illumination electric field at position(s) `r_probe`"""
        r_probe = torch.as_tensor(r_probe, dtype=DTYPE_FLOAT, device=self.device)
        if len(r_probe.shape) == 1:
            r_probe = r_probe.unsqueeze(0)

        assert r_probe.shape[1] == 3

        ex, ey, ez = self._eval_field(
            r_probe=r_probe,
            wavelength=wavelength,
            environment=environment,
        )

        return torch.stack((ex, ey, ez), dim=1)

    def get_hfield(self, r_probe: torch.Tensor, wavelength: float, environment):
        """evaluate illumination magnetic field at position(s) `r_probe`"""
        r_probe = torch.as_tensor(r_probe, dtype=DTYPE_FLOAT, device=self.device)
        if len(r_probe.shape) == 1:
            r_probe = r_probe.unsqueeze(0)

        hy, hx, hz = self._eval_field(
            r_probe=r_probe,
            wavelength=wavelength,
            environment=environment,
        )
        eps_env = environment.get_environment_permittivity_scalar(
            wavelength, r_probe=r_probe
        )
        n_env = eps_env**0.5
        return torch.stack((hx, -1 * hy, hz), dim=1) * n_env.unsqueeze(1)


class PlaneWave(IlluminationfieldBase):
    """3D plane wave in homogeneous environment"""

    __name__ = "free space plane wave 3D"

    def __init__(
        self,
        e0s=0.0,
        e0p=1.0,
        inc_angle=0.0,
        phase_e0s=0.0,
        phase_global=0,
        inc_plane="xz",
        device: torch.device = None,
    ):
        """plane wave in homogeneous 3D environment

        The polarization state can be defined in different ways. The s- and p-polarization
        complex amplitudes can be defined with a relative phase using. Alternatively a
        relative phase (in rad) can be given for the s-polarization component.

        Args:
            e0s (complex, optional): s-polarization amplitude factor. Defaults to 0.0.
            e0p (complex, optional): s-polarization amplitude factor. Defaults to 1.0.
            inc_angle (float, optional): incident angle in rad. 0:k=-ez, pi/2:k=ex, pi:k=+ez. Defaults to 0.0.
            inc_plane (str, optional): Either "xz" or "yz". Defaults to "xz".
            phase_e0s (float, optional): additional phase of s-amplitude vector (in rad). Defaults to 0.0.
            phase_global (int, optional): additional global phase (in rad). Defaults to 0.
            device (torch.device, optional): Defaults to "cpu".
        """
        super().__init__(device=device)
        self.n_dim = 3

        self.e0s = torch.as_tensor(e0s, dtype=DTYPE_COMPLEX, device=device)
        self.e0p = torch.as_tensor(e0p, dtype=DTYPE_COMPLEX, device=device)
        # in rad (xz inc_plane: 0=-ez, pi/2=ex, pi=ez)
        self.inc_angle = torch.as_tensor(inc_angle, dtype=DTYPE_FLOAT, device=device)
        self.phase_e0s = torch.as_tensor(phase_e0s, dtype=DTYPE_FLOAT, device=device)
        self.phase_global = torch.as_tensor(
            phase_global, dtype=DTYPE_FLOAT, device=device
        )

        self.inc_plane = inc_plane.lower()  # 'xz' or 'yz'
        if self.inc_plane == "xz":
            self.k_vec_unit = torch.as_tensor(
                [-torch.sin(self.inc_angle), 0.0, torch.cos(self.inc_angle)],
                dtype=DTYPE_COMPLEX,
                device=self.device,
            )
            self.e0s_vec_unit = torch.as_tensor(
                [0.0, 1.0, 0.0],
                dtype=DTYPE_COMPLEX,
                device=self.device,
            )
            self.e0p_vec_unit = torch.as_tensor(
                [-torch.cos(self.inc_angle), 0.0, -torch.sin(self.inc_angle)],
                dtype=DTYPE_COMPLEX,
                device=self.device,
            )
        elif self.inc_plane == "yz":
            self.k_vec_unit = torch.as_tensor(
                [0.0, -torch.sin(self.inc_angle), torch.cos(self.inc_angle)],
                dtype=DTYPE_COMPLEX,
                device=self.device,
            )
            self.e0s_vec_unit = torch.as_tensor(
                [-1.0, 0.0, 0.0],
                dtype=DTYPE_COMPLEX,
                device=self.device,
            )
            self.e0p_vec_unit = torch.as_tensor(
                [0.0, -torch.cos(self.inc_angle), -torch.sin(self.inc_angle)],
                dtype=DTYPE_COMPLEX,
                device=self.device,
            )
        else:
            raise ValueError(
                "planewave currently supports only 'xz' and 'yz' incident planes."
            )

    def set_device(self, device):
        super().set_device(device)
        self.e0s = torch.as_tensor(self.e0s, device=device)
        self.e0p = torch.as_tensor(self.e0p, device=device)
        self.inc_angle = torch.as_tensor(self.inc_angle, device=device)
        self.phase_e0s = torch.as_tensor(self.phase_e0s, device=device)
        self.phase_global = torch.as_tensor(self.phase_global, device=device)
        self.k_vec_unit = torch.as_tensor(self.k_vec_unit, device=device)
        self.e0s_vec_unit = torch.as_tensor(self.e0s_vec_unit, device=device)
        self.e0p_vec_unit = torch.as_tensor(self.e0p_vec_unit, device=device)

    def __repr__(self, verbose=False):
        out_str = " ------ {} -------".format(self.__name__)
        out_str += "\n - pol: {} e_p + {} e_s ".format(self.e0p, self.e0s)
        out_str += "\n - additional e_s phase (rad): {}".format(self.phase_e0s)
        out_str += "\n - incident angle (rad): {}".format(self.inc_angle)
        out_str += "\n - plane of incidence  : {}".format(self.inc_plane)

        return out_str

    def get_info(self):
        """Get info about field config. as dictionary"""
        return dict(
            name="plane wave",
            e0s=self.e0s,
            e0p=self.e0p,
            inc_angle=self.inc_angle,
            phase_e0s=self.phase_e0s,
            phase_global=self.phase_global,
        )

    def _eval_field(
        self,
        r_probe: torch.Tensor,
        wavelength: float,
        environment,
    ):
        # calculate wave vector and phase factor
        eps_env = environment.get_environment_permittivity_scalar(
            wavelength, r_probe=r_probe
        )
        n_env = eps_env**0.5

        k0 = 2 * torch.pi / torch.as_tensor(wavelength, device=self.device)
        k_vec = self.k_vec_unit.unsqueeze(0) * k0 * n_env.unsqueeze(1)
        kr = (k_vec * r_probe).sum(axis=1)  # k dot r for each vector pair
        phase_vec = torch.exp(1j * (kr + self.phase_global))

        # 2D simulations: test if y-component of k-vector matches environment
        if hasattr(environment, "get_k0_y"):
            k0_y_field = torch.as_tensor(
                torch.abs(self.k_vec_unit[1]) * k0, dtype=DTYPE_COMPLEX
            )
            k0_y_env = torch.as_tensor(
                environment.get_k0_y(wavelength), dtype=DTYPE_COMPLEX
            )
            if not torch.allclose(k0_y_field, k0_y_env, atol=1e-6, rtol=1e-6):
                raise ValueError(
                    "k-vector component along y must match `k0_y` of the 2D environment class. "
                    + "But k0_y field: {} != k0_y environment: {}".format(
                        k0_y_field, k0_y_env
                    )
                    + "Check and correct the incident angle configuration."
                )

        # calculate s and p field amplitudes
        es = (
            self.e0s_vec_unit.unsqueeze(0)
            * phase_vec.unsqueeze(1)
            * torch.exp(
                1j * self.phase_e0s
            )  # optional phase of s-polarization component
        )
        ep = self.e0p_vec_unit.unsqueeze(0) * phase_vec.unsqueeze(1)

        return es, ep

    def get_efield(self, r_probe: torch.Tensor, wavelength: float, environment):
        """evaluate the illumination's electric field

        Args:
            r_probe (torch.Tensor): evaluation position(s)
            wavelength (float): in nm
            environment (:class:`torchgdm.env.base_classes.EnvironmentBase`): Evaluation environment

        Returns:
            torch.Tensor: E-field(s) at evaluation position(s)
        """
        r_probe = torch.as_tensor(r_probe, dtype=DTYPE_FLOAT, device=self.device)
        if len(r_probe.shape) == 1:
            r_probe = r_probe.unsqueeze(0)

        es, ep = self._eval_field(
            r_probe=r_probe,
            wavelength=wavelength,
            environment=environment,
        )

        return self.e0s * es + self.e0p * ep

    def get_hfield(self, r_probe: torch.Tensor, wavelength: float, environment):
        """evaluate the illumination's magnetic field

        Args:
            r_probe (torch.Tensor): evaluation position(s)
            wavelength (float): in nm
            environment (:class:`torchgdm.env.base_classes.EnvironmentBase`): Evaluation environment

        Returns:
            torch.Tensor: H-field(s) at evaluation position(s)
        """
        r_probe = torch.as_tensor(r_probe, dtype=DTYPE_FLOAT, device=self.device)
        if len(r_probe.shape) == 1:
            r_probe = r_probe.unsqueeze(0)

        es, ep = self._eval_field(
            r_probe=r_probe,
            wavelength=wavelength,
            environment=environment,
        )
        eps_env = environment.get_environment_permittivity_scalar(
            wavelength, r_probe=r_probe
        )
        n_env = eps_env**0.5
        return (-self.e0p * es + self.e0s * ep) * n_env.unsqueeze(1)


class GaussianParaxial(IlluminationfieldBase):
    """Paraxial Gaussian beam with tight focus correction

    homogeneous environment, 'xz' incident plane.

    The polarization state is defined by Ex and Ey complex amplitude
    as well as a relative phase between x and y (optional).

    Parameters
    ----------
    e0x : complex, default: 1.0
        E_x constant amplitude factor (complex for possible phase wrt E_y)

    e0y : complex, default: 0.0
        E_y constant amplitude factor (complex for possible phase wrt E_x)

    k_z_sign : int, default: -1
        sign of z-wavenumber (incidence direction).
        +1: towards increasing z, -1: towards smaller z (default)

    Notes
    -----
     - paraxial correction, see:
       Novotny & Hecht. "Principles of nano-optics". Cambridge University Press (2006)

    """

    __name__ = "paraxial focused Gaussian beam"

    def __init__(
        self,
        e0s=0.0,
        e0p=1.0,
        r_focus=torch.as_tensor([0.0, 0.0, 0.0]),
        NA=None,
        waist=None,
        inc_angle=0.0,
        phase_e0s=0.0,
        phase_global=0,
        correction_div_e=True,
        device: torch.device = None,
    ):
        """focused paraxial Gaussian in homogeneous 3D environment, in "xz" incident plane

        tight focus paraxial correction, see:
        Novotny & Hecht. "Principles of nano-optics". Cambridge University Press (2006)

        The polarization state can be defined in different ways. The s- and p-polarization
        complex amplitudes can be defined directly, or a relative phase for the s-component
        can be given.

        Args:
            e0s (complex, optional): s-polarization amplitude factor. Defaults to 0.0.
            e0p (complex, optional): s-polarization amplitude factor. Defaults to 1.0.
            r_focus (float torch.Tensor, optional): focal position (in nm). Defaults to torch.as_tensor([0.0, 0.0, 0.0]).
            NA (float, optional): numerical aperture used for focal spotsize calculation. If None, use explicit `waist`. Defaults to None.
            waist (float, optional): explicit, constant Gausian waist (in nm). Defaults to None.
            inc_angle (float, optional): incident angle in rad. 0:k=-ez, pi:k=+ez. Defaults to 0.0.
            inc_plane (str, optional): either "xz" or "yz". Defaults to "xz".
            phase_e0s (float, optional): additional phase of s-amplitude vector (in rad). Defaults to 0.0.
            phase_global (int, optional): additional global phase (in rad). Defaults to 0.
            correction_div_e (bool, optional): whether to use paraxial tight focus correction term. Defaults to True.
            device (torch.device, optional): Defaults to "cpu".
        """
        super().__init__(device=device)
        self.n_dim = 3

        self.e0s = torch.as_tensor(e0s, dtype=DTYPE_COMPLEX, device=device)
        # sign -1 for p-polarization for orthonormal system handedness convention
        self.e0p = torch.as_tensor(e0p, dtype=DTYPE_COMPLEX, device=device)
        self.r_focus = torch.as_tensor(r_focus, dtype=DTYPE_FLOAT, device=device)
        self.inc_angle = torch.as_tensor(inc_angle, dtype=DTYPE_FLOAT, device=device)
        self.phase_e0s = torch.as_tensor(phase_e0s, dtype=DTYPE_FLOAT, device=device)
        self.phase_global = torch.as_tensor(
            phase_global, dtype=DTYPE_FLOAT, device=device
        )

        self.epsilon = 1e-5  # avoid div by zero at pi/2
        self.rot_y = rotation_y(self.inc_angle + self.epsilon, device=self.device)

        self.waist = waist
        self.NA = NA
        if self.waist is None and self.NA is None:
            raise ValueError("Gaussian Beam Error: Either waist or NA must be given.")
        if self.waist is not None and self.NA is not None:
            warnings.warn("Both, waist and NA given. Ignoring `NA`.")
            self.NA = None
        if self.NA is not None:
            self.NA = torch.as_tensor(self.NA, device=device)
        if self.waist is not None:
            self.waist = torch.as_tensor(self.waist, device=device)

        self.correction_div_e = correction_div_e

    def set_device(self, device):
        super().set_device(device)
        self.e0s = torch.as_tensor(self.e0s, device=device)
        self.e0p = torch.as_tensor(self.e0p, device=device)
        self.r_focus = torch.as_tensor(self.r_focus, device=device)
        self.inc_angle = torch.as_tensor(self.inc_angle, device=device)
        self.phase_e0s = torch.as_tensor(self.phase_e0s, device=device)
        self.phase_global = torch.as_tensor(self.phase_global, device=device)
        self.rot_y = torch.as_tensor(self.rot_y, device=device)
        if self.NA is not None:
            self.NA = torch.as_tensor(self.NA, device=device)
        if self.waist is not None:
            self.waist = torch.as_tensor(self.waist, device=device)

    def __repr__(self, verbose=False):
        out_str = " ------ {} -------".format(self.__name__)
        out_str += "\n - pol: {} e_p + {} e_s ".format(self.e0p, self.e0s)
        out_str += "\n - additional e_s phase (rad): {}".format(self.phase_e0s)
        out_str += "\n - focal position (nm): {}".format(
            torch.round(self.r_focus, decimals=1)
        )
        if self.waist is None:
            out_str += "\n - numerical aperture: {}".format(
                torch.round(self.NA, decimals=4)
            )
        else:
            out_str += "\n - waist (Gaussian width): {}nm".format(
                torch.round(self.waist, decimals=1)
            )
        out_str += "\n - incident angle (rad): {}".format(self.inc_angle)
        out_str += "\n - plane of inclination  : xz"

        return out_str

    def get_info(self):
        """Get info about field config. as dictionary"""
        return dict(
            name="Gaussian",
            e0s=self.e0s,
            e0p=self.e0p,
            inc_angle=self.inc_angle,
            r_focus=self.r_focus,
            phase_e0s=self.phase_e0s,
            phase_global=self.phase_global,
        )

    def get_x(self):
        """return x position of focus"""
        return self.r_focus.squeeze()[0]

    def get_y(self):
        """return y position of focus"""
        return self.r_focus.squeeze()[1]

    def get_z(self):
        """return z position of focus"""
        return self.r_focus.squeeze()[2]

    # waist
    def _w(self, z, a_foc, w0):
        # eps: avoid div/0 at focus
        return w0 * torch.sqrt(1 + (z / (a_foc + self.epsilon)) ** 2)

    # curvature
    def _R(self, z, a_foc):
        # eps: avoid div/0 at focus
        return z * (1 + (a_foc / (z + self.epsilon)) ** 2) + self.epsilon

    # gouy-phase
    def _gouy(self, z, a_foc):
        return torch.arctan2(z, a_foc)

    def _eval_field(
        self,
        r_probe: torch.Tensor,
        wavelength: float,
        environment,
    ):
        # --- coordinate transform.
        # shift focus, rotate around Y-axis
        r_t = torch.clone(r_probe)
        r_t -= self.r_focus.unsqueeze(0)
        r_t = torch.matmul(r_t.unsqueeze(1), self.rot_y.unsqueeze(0))
        r_t = r_t[:, 0]
        if len(r_t.shape) == 1:
            r_t = r_t.unsqueeze(0)

        # relative coordinates
        x = r_t[:, 0]
        y = r_t[:, 1]
        z = r_t[:, 2]
        z += self.epsilon * (z == 0.0).type(torch.float32)
        r2_foc = x**2 + y**2

        # wavenumber
        eps_env = environment.get_environment_permittivity_scalar(
            wavelength, r_probe=r_t
        )
        n_env = eps_env**0.5
        k_z = (
            n_env
            * 2
            * torch.pi
            / torch.as_tensor(wavelength, dtype=DTYPE_FLOAT, device=self.device)
        )

        # gaussian beam waist
        if self.waist is None:
            w0 = torch.as_tensor(
                2 * wavelength / (self.NA * torch.pi),
                dtype=DTYPE_FLOAT,
                device=self.device,
            )
        else:
            w0 = torch.as_tensor(self.waist, dtype=DTYPE_FLOAT, device=self.device)
        a_foc = torch.pi * w0**2 / wavelength
        waist = self._w(z, a_foc, w0)

        # normalized complex amplitude
        e_gaussian = ((w0 / waist) * torch.exp(-r2_foc / waist**2)) * torch.exp(
            1j
            * (
                k_z * z
                + k_z * (r2_foc / (2 * self._R(z, a_foc)))
                - self._gouy(z, a_foc)
            )
        )

        # optional phase on ey (after rotation this will be the s-polarization)
        ex = e_gaussian * torch.exp(1j * self.phase_global)
        ey = e_gaussian * torch.exp(1j * (self.phase_global + self.phase_e0s))

        # optionally: correct for divE=0
        if self.correction_div_e:
            ez = (-1j * 2 / (k_z * self._w(z, a_foc, w0) ** 2)) * (
                x * (ex * self.e0p) + y * (ey * self.e0s)
            )
        else:
            ez = torch.zeros_like(e_gaussian)

        # --- coordinate transform, xz scattering plane: fields rotate around y axis
        ef = torch.stack([ex, ey, ez], axis=1)
        ef = torch.matmul(
            ef.unsqueeze(1), self.rot_y.t().unsqueeze(0).to(dtype=DTYPE_COMPLEX)
        )
        ef = ef[:, 0]
        if len(ef.shape) == 1:
            ef = ef.unsqueeze(0)

        return ef[:, 0], ef[:, 1], ef[:, 2]

    def get_efield(self, r_probe: torch.Tensor, wavelength: float, environment):
        """evaluate the illumination's electric field

        Args:
            r_probe (torch.Tensor): evaluation position(s)
            wavelength (float): in nm
            environment (:class:`torchgdm.env.base_classes.EnvironmentBase`): Evaluation environment

        Returns:
            torch.Tensor: E-field(s) at evaluation position(s)
        """
        r_probe = torch.as_tensor(r_probe, dtype=DTYPE_FLOAT, device=self.device)
        if len(r_probe.shape) == 1:
            r_probe = r_probe.unsqueeze(0)

        ep, es, ek = self._eval_field(
            r_probe=r_probe,
            wavelength=wavelength,
            environment=environment,
        )

        return torch.stack([-self.e0p * ep, self.e0s * es, self.e0p * ek], axis=1)

    def get_hfield(self, r_probe: torch.Tensor, wavelength: float, environment):
        """evaluate the illumination's magnetic field

        Args:
            r_probe (torch.Tensor): evaluation position(s)
            wavelength (float): in nm
            environment (:class:`torchgdm.env.base_classes.EnvironmentBase`): Evaluation environment

        Returns:
            torch.Tensor: H-field(s) at evaluation position(s)
        """
        r_probe = torch.as_tensor(r_probe, dtype=DTYPE_FLOAT, device=self.device)
        if len(r_probe.shape) == 1:
            r_probe = r_probe.unsqueeze(0)

        ep, es, ek = self._eval_field(
            r_probe=r_probe,
            wavelength=wavelength,
            environment=environment,
        )
        eps_env = environment.get_environment_permittivity_scalar(
            wavelength, r_probe=r_probe
        )
        n_env = eps_env**0.5

        return torch.stack(
            [-self.e0s * ep, -self.e0p * es, self.e0s * ek], axis=1
        ) * n_env.unsqueeze(1)


class ElectricDipole(IlluminationfieldBase):
    """electric point-dipole light source in homogeneous 3D environment"""

    __name__ = "electric dipole source"

    def __init__(
        self,
        r_source: torch.Tensor,
        p_source: torch.Tensor,
        device: torch.device = None,
    ):
        """electric point dipole in homogeneous environment

        Args:
            r_source (complex torch.Tensor): 3D position of dipole as [x, y, z]
            p_source (complex torch.Tensor): amplitude vector (3D) of the source's electric dipole moment as [p_x, p_y, p_z]
            device (torch.device, optional): Defaults to "cpu".
        """
        super().__init__(device=device)
        self.n_dim = 3

        self.r_source = torch.as_tensor(r_source, dtype=DTYPE_FLOAT, device=device)
        self.p_source = torch.as_tensor(p_source, dtype=DTYPE_COMPLEX, device=device)

        assert len(self.r_source) == 3
        assert len(self.r_source.shape) == 1
        assert len(self.p_source) == 3
        assert len(self.p_source.shape) == 1

    def set_device(self, device):
        super().set_device(device)
        self.r_source = self.r_source.to(device=device)
        self.p_source = self.p_source.to(device=device)

    def __repr__(self, verbose=False):
        out_str = " ------ {} -------".format(self.__name__)
        out_str += "\n - location (nm): {}".format(
            torch.round(self.r_source, decimals=1)
        )
        out_str += "\n - amplitude: {} ".format(self.p_source)

        return out_str

    def get_info(self):
        """Get info about field config. as dictionary"""
        return dict(
            name=self.__name__,
            r_source=self.r_source,
            p_source=self.p_source,
        )

    def get_x(self):
        """return x position of dipole"""
        return self.r_source.squeeze()[0]

    def get_y(self):
        """return y position of dipole"""
        return self.r_source.squeeze()[1]

    def get_z(self):
        """return z position of dipole"""
        return self.r_source.squeeze()[2]

    def get_efield(self, r_probe: torch.Tensor, wavelength: float, environment):
        """evaluate the illumination's electric field

        Args:
            r_probe (torch.Tensor): evaluation position(s)
            wavelength (float): in nm
            environment (:class:`torchgdm.env.base_classes.EnvironmentBase`): Evaluation environment

        Returns:
            torch.Tensor: E-field(s) at evaluation position(s)
        """
        r_probe = torch.as_tensor(r_probe, dtype=DTYPE_FLOAT, device=self.device)
        if len(r_probe.shape) == 1:
            r_probe = r_probe.unsqueeze(0)

        G_Ep = environment.get_G_Ep(r_probe, self.r_source.unsqueeze(0), wavelength)
        Ep = torch.matmul(G_Ep, self.p_source.unsqueeze(-1))[..., 0]
        return Ep

    def get_hfield(self, r_probe: torch.Tensor, wavelength: float, environment):
        """evaluate the illumination's magnetic field

        Args:
            r_probe (torch.Tensor): evaluation position(s)
            wavelength (float): in nm
            environment (:class:`torchgdm.env.base_classes.EnvironmentBase`): Evaluation environment

        Returns:
            torch.Tensor: H-field(s) at evaluation position(s)
        """
        r_probe = torch.as_tensor(r_probe, dtype=DTYPE_FLOAT, device=self.device)
        if len(r_probe.shape) == 1:
            r_probe = r_probe.unsqueeze(0)

        G_Hp = environment.get_G_Hp(r_probe, self.r_source.unsqueeze(0), wavelength)
        Hp = torch.matmul(G_Hp, self.p_source.unsqueeze(-1))[..., 0]
        return Hp


class MagneticDipole(IlluminationfieldBase):
    """magnetic point-dipole light source in homogeneous 3D environment"""

    __name__ = "magnetic dipole source"

    def __init__(
        self,
        r_source: torch.Tensor,
        m_source: torch.Tensor,
        device: torch.device = None,
    ):
        """magnetic point dipole in homogeneous environment

        Args:
            r_source (complex torch.Tensor): 3D position of dipole as [x, y, z]
            m_source (complex torch.Tensor): amplitude vector (3D) of the source's magnetic dipole moment as [p_x, p_y, p_z]
            device (torch.device, optional): Defaults to "cpu".
        """
        super().__init__(device=device)
        self.n_dim = 3

        self.r_source = torch.as_tensor(r_source, dtype=DTYPE_FLOAT, device=device)
        self.m_source = torch.as_tensor(m_source, dtype=DTYPE_COMPLEX, device=device)

    def set_device(self, device):
        super().set_device(device)
        self.r_source = self.r_source.to(device=device)
        self.m_source = self.m_source.to(device=device)

    def __repr__(self, verbose=False):
        out_str = " ------ {} -------".format(self.__name__)
        out_str += "\n - location (nm): {}".format(
            torch.round(self.r_source, decimals=1)
        )
        out_str += "\n - amplitude: {} ".format(self.m_source)

        return out_str

    def get_info(self):
        """Get info about field config. as dictionary"""
        return dict(
            name=self.__name__,
            r_source=self.r_source,
            m_source=self.m_source,
        )

    def get_x(self):
        """return x position of dipole"""
        return self.r_source.squeeze()[0]

    def get_y(self):
        """return y position of dipole"""
        return self.r_source.squeeze()[1]

    def get_z(self):
        """return z position of dipole"""
        return self.r_source.squeeze()[2]

    def get_efield(self, r_probe: torch.Tensor, wavelength: float, environment):
        """evaluate the illumination's electric field

        Args:
            r_probe (torch.Tensor): evaluation position(s)
            wavelength (float): in nm
            environment (:class:`torchgdm.env.base_classes.EnvironmentBase`): Evaluation environment

        Returns:
            torch.Tensor: E-field(s) at evaluation position(s)
        """
        r_probe = torch.as_tensor(r_probe, dtype=DTYPE_FLOAT, device=self.device)
        if len(r_probe.shape) == 1:
            r_probe = r_probe.unsqueeze(0)

        G_Em = environment.get_G_Em(r_probe, self.r_source.unsqueeze(0), wavelength)
        Em = torch.matmul(G_Em, self.m_source.unsqueeze(-1))[..., 0]
        return Em

    def get_hfield(self, r_probe: torch.Tensor, wavelength: float, environment):
        """evaluate the illumination's magnetic field

        Args:
            r_probe (torch.Tensor): evaluation position(s)
            wavelength (float): in nm
            environment (:class:`torchgdm.env.base_classes.EnvironmentBase`): Evaluation environment

        Returns:
            torch.Tensor: H-field(s) at evaluation position(s)
        """
        r_probe = torch.as_tensor(r_probe, dtype=DTYPE_FLOAT, device=self.device)
        if len(r_probe.shape) == 1:
            r_probe = r_probe.unsqueeze(0)

        G_Hm = environment.get_G_Hm(r_probe, self.r_source.unsqueeze(0), wavelength)
        Hm = torch.matmul(G_Hm, self.m_source.unsqueeze(-1))[..., 0]
        return Hm


# %%
if __name__ == "__main__":
    from torchgdm import env
    from torchgdm import tools
    import torchgdm as tg

    torch.set_printoptions(precision=3)
    # -- test plane wave
    wavelength = 700.0
    eps_env = 1.0
    env = env.dyads.EnvHomogeneous3D(env_material=eps_env)
    r_probe = torch.as_tensor(
        [[100, 0, 20], [0, 0, 100], [-100, 0, 200], [-500, 40, -200]], dtype=DTYPE_FLOAT
    )
    r_probe_xz = tools.geometry.coordinate_map_2d_square(2000, 51, 5, projection="xz")
    r_probe_yz = tools.geometry.coordinate_map_2d_square(2000, 51, 5, projection="yz")

    inangledeg = 60 * torch.pi / 180
    e_p = 0.5
    e_s = 0.2

    efield_xz = PlaneWave(e0p=e_p, e0s=e_s, inc_angle=inangledeg, inc_plane="xz")
    field_xz = efield_xz.get_field(r_probe_xz, wavelength=wavelength, environment=env)
    efield_yz = PlaneWave(e0p=e_p, e0s=e_s, inc_angle=inangledeg, inc_plane="yz")
    field_yz = efield_yz.get_field(r_probe_yz, wavelength=wavelength, environment=env)

    import matplotlib.pyplot as plt

    plt.figure(figsize=(8, 4))
    plt.subplot(221, aspect="equal")
    tg.visu.visu2d.vec2d.vectorfield(field_xz, whichfield="e")

    plt.subplot(223, aspect="equal")
    tg.visu.visu2d.vec2d.vectorfield(field_xz, whichfield="h")

    plt.subplot(222, aspect="equal")
    tg.visu.visu2d.vec2d.vectorfield(field_yz, whichfield="e")

    plt.subplot(224, aspect="equal")
    tg.visu.visu2d.vec2d.vectorfield(field_yz, whichfield="h")

    plt.show()
