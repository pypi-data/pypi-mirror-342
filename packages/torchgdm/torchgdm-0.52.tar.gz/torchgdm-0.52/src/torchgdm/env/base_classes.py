# -*- coding: utf-8 -*-
"""
base classes for defining torchgdm simulations
"""
# %%
import warnings

import torch

from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX
from torchgdm.tools.misc import get_default_device


# --- environment defining base class
class EnvironmentBase:
    """base class defining the environment via Green's tensors"""

    __name__ = "environment base class"

    def __init__(self, device: torch.device = None):
        if device is None:
            self.device = get_default_device()
        else:
            self.device = device

        self.n_dim = -1  # problem dimension needs to be set by child class

    def __repr__(self, verbose: bool = False):
        """description about simulation environment defined by set of dyads"""
        out_str = " ------ base environment class - doesn't define anything yet -------"
        return out_str

    def set_device(self, device):
        """move all tensors of the class to device"""
        self.device = device

    def copy(self):
        import copy

        return copy.deepcopy(self)

    def get_environment_permittivity_scalar(self, wavelength: float, r_probe: tuple):
        """return complex environment permittivity tensor - scalar(!)

        evaluate scalar epsilon for `wavelength` at position `r` (both in nm)
        """
        raise NotImplementedError(
            "Definition missing! This function needs to be overridden in child class!"
        )

    def get_G_6x6(
        self, r_probe: torch.Tensor, r_source: torch.Tensor, wavelength: float
    ):
        """electro-magnetic Green's tensor for an e/m pair-dipole"""
        raise NotImplementedError(
            "Definition missing! This function needs to be overridden in child class!"
        )

    def get_G_Ep(
        self, r_probe: torch.Tensor, r_source: torch.Tensor, wavelength: float
    ):
        """Electric field Green's tensor for an electric dipole"""
        raise NotImplementedError(
            "Definition missing! This function needs to be overridden in child class!"
        )

    def get_G_Hp(
        self, r_probe: torch.Tensor, r_source: torch.Tensor, wavelength: float
    ):
        """Magnetic field Green's tensor for an electric dipole"""
        raise NotImplementedError(
            "Definition missing! This function needs to be overridden in child class!"
        )

    def get_G_Em(
        self, r_probe: torch.Tensor, r_source: torch.Tensor, wavelength: float
    ):
        """Electric field Green's tensor for a magnetic dipole"""
        raise NotImplementedError(
            "Definition missing! This function needs to be overridden in child class!"
        )

    def get_G_Hm(
        self, r_probe: torch.Tensor, r_source: torch.Tensor, wavelength: float
    ):
        """Magnetic field Green's tensor for a magnetic dipole"""
        raise NotImplementedError(
            "Definition missing! This function needs to be overridden in child class!"
        )

    # --- wrapper for mixed e-m Green's tensors
    def get_G_6x6(self, r_probe, r_source, wavelength):
        """electro-magnetic Green's tensor for a pair of p/m dipoles

        r_probe: field evaluation position, r_source: emitter-pair position
        """
        G_6x6 = torch.cat(
            [
                torch.cat(
                    [
                        self.get_G_Ep(r_probe, r_source, wavelength),
                        self.get_G_Em(r_probe, r_source, wavelength),
                    ],
                    dim=-1,
                ),
                torch.cat(
                    [
                        self.get_G_Hp(r_probe, r_source, wavelength),
                        self.get_G_Hm(r_probe, r_source, wavelength),
                    ],
                    dim=-1,
                ),
            ],
            dim=-2,
        )
        return G_6x6

    def get_G_EHp_6x3(self, r_probe, r_source, wavelength):
        """electric field Green's tensor for a pair of p/m dipoles

        r_probe: field evaluation position, r_source: emitter-pair position
        """
        G_EHp_6x3 = torch.cat(
            [
                self.get_G_Ep(r_probe, r_source, wavelength),
                self.get_G_Hp(r_probe, r_source, wavelength),
            ],
            dim=-2,
        )

        return G_EHp_6x3

    def get_G_Epm_3x6(self, r_probe, r_source, wavelength):
        G_EHp_6x3 = torch.cat(
            [
                self.get_G_Ep(r_probe, r_source, wavelength),
                self.get_G_Hp(r_probe, r_source, wavelength),
            ],
            dim=-2,
        )

        return G_EHp_6x3

    def get_G_Epm_3x6(self, r_probe, r_source, wavelength):
        G_Epm_3x6 = torch.cat(
            [
                self.get_G_Ep(r_probe, r_source, wavelength),
                self.get_G_Em(r_probe, r_source, wavelength),
            ],
            dim=-1,
        )

        return G_Epm_3x6

    def get_G_EHm_6x3(self, r_probe, r_source, wavelength):
        """magnetic field Green's tensor for a pair of p/m dipoles

        r_probe: field evaluation position, r_source: emitter-pair position
        """
        G_EHm_6x3 = torch.cat(
            [
                self.get_G_Em(r_probe, r_source, wavelength),
                self.get_G_Hm(r_probe, r_source, wavelength),
            ],
            dim=-2,
        )

        return G_EHm_6x3

    def get_G_Hpm_3x6(self, r_probe, r_source, wavelength):
        G_Hpm_3x6 = torch.cat(
            [
                self.get_G_Hp(r_probe, r_source, wavelength),
                self.get_G_Hm(r_probe, r_source, wavelength),
            ],
            dim=-1,
        )

        return G_Hpm_3x6

    # --- far-field approximation
    def get_G_Ep_farfield(self, r_probe, r_source, wavelength):
        """Electric field asymptotic far-field Green's tensor for an electric dipole

        r_probe: field evaluation position, r_source: emitter position
        """
        warnings.warn(
            "No `G_Ep` ff approximation implemented. Using full Green's tensor."
        )
        return self.get_G_Ep(r_probe, r_source, wavelength)

    def get_G_Em_farfield(self, r_probe, r_source, wavelength):
        """Electric field asymptotic far-field Green's tensor for a magnetic dipole

        r_probe: field evaluation position, r_source: emitter position
        """
        warnings.warn(
            "No `G_Em` ff approximation implemented. Using full Green's tensor."
        )
        return self.get_G_Em(r_probe, r_source, wavelength)


# --- illumination field defining base class
class IlluminationfieldBase:
    """base class defining the illumination E/H field"""

    __name__ = "illumination base class"

    def __init__(
        self,
        device: torch.device = None,
    ):
        """_summary_

        Args:
            device (torch.device, optional): Defaults to 'cpu'.
        """
        if device is None:
            self.device = get_default_device()
        else:
            self.device = device

        self.n_dim = -1  # problem dimension needs to be set by child class

    def __repr__(self, verbose=False):
        """description of illumination field"""
        out_str = " ------ {} -------".format(self.__name__)
        return out_str

    def copy(self):
        import copy

        return copy.deepcopy(self)

    def get_info(self):
        return dict(name=self.__name__)

    def set_device(self, device):
        """move all tensors of the class to device"""
        self.device = device

    def get_efield(
        self, r_probe: torch.Tensor, wavelength: float, environment: EnvironmentBase
    ):
        """evaluate illumination electric field at position(s) `r_probe`"""
        raise NotImplementedError(
            "electric field evaluation needs to be implemented in child class."
        )

    def get_hfield(
        self, r_probe: torch.Tensor, wavelength: float, environment: EnvironmentBase
    ):
        """evaluate illumination magnetic field at position(s) `r_probe`"""
        raise NotImplementedError(
            "magnetic field evaluation needs to be implemented in child class."
        )

    def get_field(self, r_probe, wavelength: float, environment: EnvironmentBase):
        """return electro-magnetic fields at `r_probe` as `Field` object"""
        from torchgdm.field import Field

        if type(r_probe) == dict:
            _r = r_probe["r_probe"]
        else:
            _r = r_probe

        e0 = self.get_efield(r_probe=_r, wavelength=wavelength, environment=environment)
        h0 = self.get_hfield(r_probe=_r, wavelength=wavelength, environment=environment)

        return Field(
            positions=r_probe,
            efield=e0.unsqueeze(0),
            hfield=h0.unsqueeze(0),
            device=self.device,
        )


# - generic dipole source: Uses environment Green's tensors
class IlluminationDipole(IlluminationfieldBase):
    """generic electric/magnetic point-dipole light source"""

    __name__ = "dipole source"

    def __init__(
        self,
        r_source: torch.Tensor,
        dp_source: torch.Tensor,
        n_dim: int,
        device: torch.device = None,
    ):
        """electric/magnetic point dipole

        Args:
            r_source (complex torch.Tensor): 3D position of dipole as [x, y, z]
            dp_source (complex torch.Tensor): amplitude 6-vector of the source's electric and magnetic dipole moment as [p_x, p_y, p_z, m_x, m_y, m_z]
            n_dim (int): dimension (2 or 3) of problem the illumination is going to be used in (required by consistency checks).
            device (torch.device, optional): Defaults to "cpu".
        """
        super().__init__(device=device)
        self.n_dim = n_dim  # 2D or 3D?

        self.r_source = torch.as_tensor(r_source, dtype=DTYPE_FLOAT, device=device)
        self.dp_source = torch.as_tensor(dp_source, dtype=DTYPE_COMPLEX, device=device)
        assert len(self.r_source) == 3
        assert len(self.dp_source) == 6

    def set_device(self, device):
        super().set_device(device)
        self.r_source = self.r_source.to(device=device)
        self.dp_source = self.dp_source.to(device=device)

    def __repr__(self, verbose=False):
        out_str = " ------ {} -------".format(self.__name__)
        out_str += "\n - location (nm): {}".format(
            torch.round(self.r_source, decimals=1)
        )
        out_str += "\n - amplitude: {} ".format(self.dp_source)

        return out_str

    def get_info(self):
        """Get info about field config. as dictionary"""
        return dict(
            name=self.__name__,
            r_source=self.r_source,
            m_source=self.dp_source,
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

        G_Epm = environment.get_G_Epm_3x6(r_probe, self.r_source.unsqueeze(0), wavelength)
        Em = torch.matmul(G_Epm, self.dp_source.unsqueeze(-1))[..., 0]
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

        G_Hpm = environment.get_G_Hpm_3x6(r_probe, self.r_source.unsqueeze(0), wavelength)
        Hm = torch.matmul(G_Hpm, self.dp_source.unsqueeze(-1))[..., 0]
        return Hm
