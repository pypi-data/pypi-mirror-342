# -*- coding: utf-8 -*-
"""
provider for dielectric functions of selected materials.

.. autosummary::
   :toctree: generated/

    MatDatabase
    MatTiO2

"""
# %%
import torch

from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX
from torchgdm.tools.misc import get_default_device
from torchgdm.materials.base_classes import MaterialBase


class MatConstant(MaterialBase):
    """constant material index

    Material without dispersion
    """

    def __init__(self, eps=2.0 + 0.0j, device: torch.device = None):
        """constant permittivity material

        Args:
            eps (complex, optional): complex permittivity value. Defaults to (2.0 + 0.0j).
            device (torch.device, optional): Defaults to "cpu" (can be changed by :func:`torchgdm.use_cuda`).
        """
        super().__init__(device=device)

        self.eps_scalar = torch.as_tensor(eps, dtype=DTYPE_COMPLEX, device=self.device)

        _eps_re = torch.round(self.eps_scalar.real, decimals=2)
        _eps_im = torch.round(self.eps_scalar.imag, decimals=3)
        if _eps_im == 0:
            self.__name__ = "eps={:.2f}".format(_eps_re)
        else:
            self.__name__ = "eps={:.2f}+i{:.3f}".format(_eps_re, _eps_im)

    def __repr__(self, verbose: bool = False):
        """description about material"""
        out_str = "constant, isotropic material. permittivity = {}".format(
            self.eps_scalar
        )
        return out_str

    def set_device(self, device):
        super().set_device(device)
        self.eps_scalar = self.eps_scalar.to(device)

    def get_epsilon(self, wavelength):
        """dispersionless, constant permittivity function

        Args:
            wavelength (float): in nm

        Returns:
            torch.Tensor: (3,3) complex permittivity tensor at `wavelength`
        """
        eps = torch.eye(3, dtype=DTYPE_COMPLEX, device=self.device)
        wavelength = torch.as_tensor(wavelength, device=self.device)

        # multiple wavelengths
        if len(wavelength.shape) == 1:
            eps = torch.repeat_interleave(
                torch.eye(3, dtype=DTYPE_COMPLEX, device=self.device).unsqueeze(0),
                wavelength.shape[0],
                dim=0,
            )

        return eps * self.eps_scalar


class MatTiO2(MaterialBase):
    """TiO2 permittivity

    model for visible and NIR range (~500nm - ~1500nm)
    from https://refractiveindex.info/?shelf=main&book=TiO2&page=Devore-o

    Thanks to Dr. Frank Mersch (Kronos International) for help
    """

    __name__ = "TiO2 (Devore)"

    def __init__(self, orientation="avg", device: torch.device = None):
        """TiO2 permittivity

        supports single axis, averaged or tensorial permittivity models.

        Args:
            orientation (str, optional): one of 'avg' (average of n_o and n_e: n = (2*n_o + n_e) / 3), 'n_o' (ordinary axis permittivity),          - 'n_e' (extra-ordinary axis permittivity), or 'tensor'. x,y: ordinary axes; z: extraordinary axis. Defaults to "avg".
            device (torch.device, optional): Defaults to "cpu" (can be changed by :func:`torchgdm.use_cuda`).
        """
        super().__init__(device=device)

        self.orientation = orientation.lower()

    def __repr__(self, verbose: bool = False):
        """description about material"""
        out_str = "TiO2 birefringent permittivity. ordinary: x,y; extraordinary: z."
        return out_str

    def set_device(self, device):
        super().set_device(device)

    def _n_o(self, wavelength):
        n = torch.sqrt(
            torch.as_tensor(
                5.913 + 0.2441 / ((wavelength / 1e3) ** 2 - 0.0803),
                dtype=DTYPE_FLOAT,
                device=self.device,
            )
        )
        return n

    def _n_e(self, wavelength):
        n = torch.sqrt(
            torch.as_tensor(
                7.197 + 0.3322 / ((wavelength / 1e3) ** 2 - 0.0843),
                dtype=DTYPE_FLOAT,
                device=self.device,
            )
        )
        return n

    def _get_eps_single_wl(self, wavelength):
        if self.orientation in ["n_o", "no"]:
            # purely real in available spectral range
            eps = (self._n_o(wavelength) ** 2 + 0j) * torch.eye(
                3, dtype=DTYPE_COMPLEX, device=self.device
            )
        elif self.orientation in ["n_e", "ne"]:
            eps = (self._n_e(wavelength) ** 2 + 0j) * torch.eye(
                3, dtype=DTYPE_COMPLEX, device=self.device
            )
        elif self.orientation in ["n_e", "ne"]:
            eps = (self._n_e(wavelength) ** 2 + 0j) * torch.eye(
                3, dtype=DTYPE_COMPLEX, device=self.device
            )
        elif self.orientation == "avg":
            n_o = self._n_o(wavelength)
            n_e = self._n_e(wavelength)
            n_avg = (2 * n_o + n_e) / 3.0
            eps = (n_avg**2 + 0j) * torch.eye(
                3, dtype=DTYPE_COMPLEX, device=self.device
            )
        else:
            n_o = self._n_o(wavelength)
            n_e = self._n_e(wavelength)
            eps = torch.eye(3, dtype=DTYPE_COMPLEX, device=self.device)
            eps[0, 0] = n_o**2
            eps[1, 1] = n_o**2
            eps[2, 2] = n_e**2

        return eps

    def get_epsilon(self, wavelength):
        """get permittivity at `wavelength`

        Args:
            wavelength (float): in nm

        Returns:
            torch.Tensor: (3,3) complex permittivity tensor at `wavelength`
        """

        # multiple wavelengths
        if len(torch.as_tensor(wavelength).shape) == 1:
            eps = torch.stack([self._get_eps_single_wl(wl) for wl in wavelength], dim=0)
        else:
            eps = self._get_eps_single_wl(wavelength)

        return eps
