# -*- coding: utf-8 -*-
"""
illumination fields for torchgdm
"""
import warnings

import torch

from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX
from torchgdm.tools.misc import get_default_device
from torchgdm.env.base_classes import IlluminationfieldBase

# make 2D compatible fields available
from torchgdm.env.freespace_3d.inc_fields import NullField as _nullfield3D
from torchgdm.env.freespace_3d.inc_fields import PlaneWave as _planewave3D


class NullField(_nullfield3D):
    """Zero-Field

    all additional kwargs are ignored

    """

    __name__ = "null field - 2D"

    def __init__(self, device: torch.device = None):
        super().__init__(device=device)
        self.n_dim = 2


class PlaneWave(_planewave3D):
    """2D plane wave in homogeneous environment"""

    __name__ = "free space plane wave 2D"

    def __init__(
        self,
        e0s=0.0,
        e0p=1.0,
        inc_angle=0.0,
        inc_plane="xz",
        phase_e0s=0.0,
        phase_global=0,
        device: torch.device = None,
    ):
        """plane wave in homogeneous 2D environment

        The polarization state can be defined in different ways. The s- and p-polarization
        complex amplitudes can be defined with a relative phase using. Alternatively a
        relative phase (in rad) can be given for the s-polarization component.

        Args:
            e0s (complex, optional): s-polarization amplitude factor. Defaults to 0.0.
            e0p (complex, optional): s-polarization amplitude factor. Defaults to 1.0.
            inc_angle (float, optional): incident angle in rad. 0:k=-ez, pi:k=+ez. Defaults to 0.0.
            inc_plane (str, optional): Either "xz" or "yz". Defaults to "xz".
            phase_e0s (float, optional): additional phase of s-amplitude vector (in rad). Defaults to 0.0.
            phase_global (int, optional): additional global phase (in rad). Defaults to 0.
            device (torch.device, optional): Defaults to "cpu".
        """
        super().__init__(
            e0s=e0s,
            e0p=e0p,
            inc_angle=inc_angle,
            phase_e0s=phase_e0s,
            phase_global=phase_global,
            inc_plane=inc_plane,
            device=device,
        )
        self.n_dim = 2


class ElectricLineDipole(IlluminationfieldBase):
    """2D electric line-dipole in homogeneous environment"""

    __name__ = "electric line dipole"

    def __init__(
        self,
        r_source: torch.Tensor,
        p_source: torch.Tensor,
        device: torch.device = None,
    ):
        """2D electric line-dipole in homogeneous environment

        Args:
            r_source (complex torch.Tensor): 2D position of line dipole as [x, z] or [x, 0, z] (y: infinite axis)
            p_source (complex torch.Tensor): amplitude vector (3D) of the source's electric dipole moment as [p_x, p_y, p_z]
            device (torch.device, optional): Defaults to "cpu".
        """
        super().__init__(device=device)
        self.n_dim = 2

        self.r_source = torch.as_tensor(r_source, dtype=DTYPE_FLOAT, device=device)
        self.p_source = torch.as_tensor(p_source, dtype=DTYPE_COMPLEX, device=device)

        assert len(self.r_source.shape) == 1
        if len(self.r_source) == 2:
            self.r_source = torch.tensor([self.r_source[0], 0, self.r_source[1]])
        assert len(r_source) == 3 and len(p_source) == 3
        assert self.r_source[1] == 0, "2D: requires y=0"

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
        return dict(
            name=self.__name__,
            r_source=self.r_source,
            p_source=self.p_source,
        )

    def get_x(self):
        """return x position of line dipole"""
        return self.r_source.squeeze()[0]

    def get_y(self):
        """return y position of line dipole"""
        # this is 0 by definition
        return self.r_source.squeeze()[1]

    def get_z(self):
        """return z position of line dipole"""
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


class MagneticLineDipole(IlluminationfieldBase):
    """2D magnetic line-dipole in homogeneous environment"""

    __name__ = "magnetic line dipole"

    def __init__(
        self,
        r_source: torch.Tensor,
        m_source: torch.Tensor,
        device: torch.device = None,
    ):
        """2D magnetic line-dipole in homogeneous environment

        Args:
            r_source (complex torch.Tensor): 2D position of line dipole as [x, z] or [x, 0, z] (y: infinite axis)
            m_source (complex torch.Tensor): amplitude vector (3D) of the source's magnetic dipole moment as [p_x, p_y, p_z]
            device (torch.device, optional): Defaults to "cpu".
        """
        super().__init__(device=device)
        self.n_dim = 2

        self.r_source = torch.as_tensor(r_source, dtype=DTYPE_FLOAT, device=device)
        self.m_source = torch.as_tensor(m_source, dtype=DTYPE_COMPLEX, device=device)

        assert len(self.r_source.shape) == 1
        if len(self.r_source) == 2:
            self.r_source = torch.tensor([self.r_source[0], 0, self.r_source[1]])
        assert len(r_source) == 3 and len(m_source) == 3
        assert self.r_source[1] == 0, "2D: requires y=0"

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
        return dict(
            name=self.__name__,
            r_source=self.r_source,
            p_source=self.m_source,
        )

    def get_x(self):
        """return x position of line dipole"""
        return self.r_source.squeeze()[0]

    def get_y(self):
        """return y position of line dipole"""
        # this is 0 by definition
        return self.r_source.squeeze()[1]

    def get_z(self):
        """return z position of line dipole"""
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
        Ep = torch.matmul(G_Em, self.m_source.unsqueeze(-1))[..., 0]
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

        G_Hm = environment.get_G_Hm(r_probe, self.r_source.unsqueeze(0), wavelength)
        Hp = torch.matmul(G_Hm, self.m_source.unsqueeze(-1))[..., 0]
        return Hp
