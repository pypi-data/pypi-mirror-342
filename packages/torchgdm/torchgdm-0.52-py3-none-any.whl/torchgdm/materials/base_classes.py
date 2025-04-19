# -*- coding: utf-8 -*-
"""
provider for dielectric functions of selected materials.
"""
# %%
import torch

from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX
from torchgdm.tools.misc import get_default_device


# --- material defining base class
class MaterialBase:
    """base class for material permittivity"""

    __name__ = "material dielectric constant base class"

    def __init__(self, device: torch.device = None):
        if device is None:
            self.device = get_default_device()
        else:
            self.device = device

    def __repr__(self, verbose: bool = False):
        """description about material"""
        out_str = " ------ base material class - doesn't define anything yet -------"
        return out_str

    def set_device(self, device):
        """move all tensors of the class to device"""
        self.device = device

    def get_epsilon(self, wavelength: float):
        """return (3, 3) permittivity tensor at `wavelength`"""
        raise NotImplementedError("Needs to be implemented in child class.")

    def plot_epsilon(
        self, wavelengths=torch.linspace(400, 1400, 100), tensor_comp=[0, 0]
    ):
        """plot the permittivity dispersion

        Args:
            wavelengths (torch.Tensor, optional): wavelengths to evaluate. Defaults to torch.linspace(400, 1400, 100).
            tensor_comp (list, optional): permittivity tensor component indices. Defaults to [0, 0].
        """
        import matplotlib.pyplot as plt
        from torchgdm import to_np
        from torchgdm.visu.visu2d._tools import _get_axis_existing_or_new

        eps = self.get_epsilon(wavelengths)

        # plot
        ax, show = _get_axis_existing_or_new()

        plt.title("epsilon - '{}'".format(self.__name__))
        plt.plot(
            to_np(wavelengths),
            to_np(eps[:, tensor_comp[0], tensor_comp[1]].real),
            label=r"Re($\epsilon$)",
        )
        plt.plot(
            to_np(wavelengths),
            to_np(eps[:, tensor_comp[0], tensor_comp[1]].imag),
            label=r"Im($\epsilon$)",
        )
        plt.legend()
        plt.xlabel("wavelength (nm)")
        plt.ylabel("permittivity")

        if show:
            plt.show()

    def plot_refractive_index(
        self, wavelengths=torch.linspace(400, 1400, 100), tensor_comp=[0, 0]
    ):
        """plot the refractive index dispersion

        Args:
            wavelengths (torch.Tensor, optional): wavelengths to evaluate. Defaults to torch.linspace(400, 1400, 100).
            tensor_comp (list, optional): refractive index tensor component indices. Defaults to [0, 0].
        """
        import matplotlib.pyplot as plt
        from torchgdm import to_np
        from torchgdm.visu.visu2d._tools import _get_axis_existing_or_new

        n_mat = self.get_epsilon(wavelengths) ** 0.5

        # plot
        ax, show = _get_axis_existing_or_new()

        plt.title("ref. index - '{}'".format(self.__name__))
        plt.plot(
            to_np(wavelengths),
            to_np(n_mat[:, tensor_comp[0], tensor_comp[1]].real),
            label="n",
        )
        plt.plot(
            to_np(wavelengths),
            to_np(n_mat[:, tensor_comp[0], tensor_comp[1]].imag),
            label="k",
        )
        plt.legend()
        plt.xlabel("wavelength (nm)")
        plt.ylabel("refractive index")

        if show:
            plt.show()
