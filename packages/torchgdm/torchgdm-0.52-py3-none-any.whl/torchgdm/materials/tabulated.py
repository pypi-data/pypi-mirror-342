# -*- coding: utf-8 -*-
"""
dielectric functions of tabulated, isotropic materials

This is an API for the refractiveindex.info yaml dataformat ("full databas record").
It requires pyyaml. Install with:

.. code-block:: bash

     pip install pyyaml



.. autosummary::
   :toctree: generated/

    MatDatabase
"""
# %%
import warnings
import importlib.resources as pkg_resources
import pathlib

import torch

from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX
from torchgdm.tools.misc import get_default_device
from torchgdm import materials  # caution, dangerous wrt circular imports
from torchgdm.materials.base_classes import MaterialBase
from torchgdm.tools.misc import to_np
from torchgdm.tools.interp import interp1d

# --- get all available materials
DATA_FOLDER = "data/"
data_files = pkg_resources.files(materials).joinpath(DATA_FOLDER).iterdir()

REFINDEX_DATA = {}
for f in data_files:
    f_n = pathlib.Path(f).name
    mat_name = f_n.split("_")[0]
    REFINDEX_DATA[mat_name.lower()] = [f, mat_name]


def list_available_materials(verbose=False):
    """Return all keys for the database materials"""
    if verbose:
        for f in REFINDEX_DATA:
            print("{}: ".format(f, pathlib.Path(REFINDEX_DATA[f]).name))
    return [f for f in REFINDEX_DATA]


# --- internal helper
def _load_tabulated(dat_str):
    rows = dat_str["data"].split("\n")
    splitrows = [c.split() for c in rows]
    wl = []
    eps = []
    for s in splitrows:
        if len(s) > 0:
            wl.append(1000.0 * float(s[0]))  # microns --> nm
            _n = float(s[1])
            if len(s) > 2:
                _k = float(s[2])
            else:
                _k = 0.0
            eps.append((_n + 1j * _k) ** 2)
    return wl, eps


def _load_formula(dat_str):
    model_type = int((dat_str["type"].split())[1])
    coeff = [float(s) for s in dat_str["coefficients"].split()]
    for k in ["range", "wavelength_range"]:
        if k in dat_str:
            break
    # validity range (convert to nm)
    wl_range = [1e3 * float(dat_str[k].split()[0]), 1e3 * float(dat_str[k].split()[1])]

    return model_type, wl_range, coeff


# --- main interface classes
class MatDatabase(MaterialBase):
    """dispersion from a database entry

    Use permittivity data from included database (data from https://refractiveindex.info/),
    or by loading a yaml file downloaded from https://refractiveindex.info/. Currently
    supported ref.index formats are tabulated n(k) data or Sellmeier model.

    Tabulated materials natively available in torchgdm can be
    printed via :func:`torchgdm.materials.list_available_materials()`

    Requires `pyyaml` (pip3 install pyyaml)

    Parameters
    ----------
    name : str
        name of database entry

    yaml_file : str, default: None
        optional filename of yaml refractiveindex data to load. In case a
        filename is provided, `name` will only be used as __name__ attribute
        for the class instance.

    """

    def __init__(
        self,
        name="",
        yaml_file=None,
        device: torch.device = None,
        init_lookup_wavelengths=None,
    ):
        """dispersion from a database entry

        supports data following the yaml format of refractiveindex.info.
        Currently tabulated permittivity and Sellmeier models are supported.

        Args:
            name (str, optional): Name of database entry. Defaults to "".
            yaml_file (_type_, optional): path to optional yaml file with material data to load. If given, file is loaded and no data-base entry will be used, even if the name matches. Defaults to None.
            device (torch.device, optional): Defaults to "cpu" (can be changed by :func:`torchgdm.use_cuda`).
            init_lookup_wavelengths (torch.Tensor, optional): optional list of wavelengths to generate an initial lookup table. Defaults to None.

        Raises:
            ValueError: Unknown material or unknown dispersion model type
        """
        import yaml

        super().__init__(device=device)

        if (name == "") and (yaml_file is None):
            print("No material specified. Available materials in database: ")
            for k in REFINDEX_DATA:
                print("     - '{}'".format(k))
            del self
            return
        if (yaml_file is None) and (name.lower() not in REFINDEX_DATA):
            raise ValueError(
                "'{}': Unknown material. Available materials in database: {}".format(
                    name, REFINDEX_DATA.keys()
                )
            )

        # load database entry from yaml
        if yaml_file is None:
            yaml_file = REFINDEX_DATA[name.lower()][0]
            self.__name__ = REFINDEX_DATA[name.lower()][1]
        else:
            if name:
                self.__name__ = name
            else:
                self.__name__ = pathlib.Path(yaml_file).stem

        with open(yaml_file, "r", encoding="utf8") as f:
            self.dset = yaml.load(f, Loader=yaml.BaseLoader)

        if len(self.dset["DATA"]) > 1:
            warnings.warn(
                "Several model entries in data-set for '{}' ({}). Using first entry.".format(
                    name, yaml_file
                )
            )
        dat = self.dset["DATA"][0]
        self.type = dat["type"]
        self.wl_dat = torch.Tensor([])
        self.eps_dat = torch.Tensor([])
        self.lookup_eps = {}

        # load refractive index model.
        # currently supported: tabulated data and Sellmeier model.
        # - tabulated data
        if self.type.split()[0] == "tabulated":
            wl_dat, eps_dat = _load_tabulated(dat)
            self.wl_dat = torch.as_tensor(wl_dat, dtype=DTYPE_FLOAT, device=self.device)
            self.eps_dat = torch.as_tensor(
                eps_dat, dtype=DTYPE_COMPLEX, device=self.device
            )
            self.model_type = "data"
            self.coeff = []
            self.wl_range = [torch.min(self.wl_dat), torch.max(self.wl_dat)]

        # - Sellmeier
        elif self.type.split()[0] == "formula":
            self.model_type, self.wl_range, self.coeff = _load_formula(dat)
            if self.model_type == 1:
                self.model_type = "sellmeier"
        else:
            raise ValueError(
                "refractiveindex.info data type '{}' not implemented yet.".format(
                    self.type
                )
            )

        # optionally initialize wavelength lookup
        if init_lookup_wavelengths is not None:
            for wl in init_lookup_wavelengths:
                _eps = self._get_eps_single_wl(wl)

    def __repr__(self, verbose: bool = False):
        """description about material"""
        out_str = ' ----- Material "{}" ({}) -----'.format(
            self.__name__, self.model_type
        )
        if self.model_type == "data":
            out_str += "\n tabulated wavelength range: {:.1f}nm - {:.1f}nm".format(
                *self.wl_range
            )
        elif self.model_type == "sellmeier":
            out_str += "\n Sellmeier model validity range: {:.1f}nm - {:.1f}nm".format(
                *self.wl_range
            )
        return out_str

    def set_device(self, device):
        super().set_device(device)
        self.wl_dat = self.wl_dat.to(device)
        self.eps_dat = self.eps_dat.to(device)

        # transfer the lookup table
        for _w in self.lookup_eps:
            self.lookup_eps[_w] = self.lookup_eps[_w].to(device)

    def _eval(self, wavelength):
        """evaluate refractiveindex.info model"""

        # - tabulated, using bilinear interpolation
        if self.model_type == "data":
            # torch implementation of 1d interpolation:
            eps = interp1d(wavelength, self.wl_dat, self.eps_dat)

        # - Sellmeier
        elif self.model_type == "sellmeier":
            eps = 1 + self.coeff[0]

            def g(c1, c2, w):
                return c1 * (w**2) / (w**2 - c2**2)

            for i in range(1, len(self.coeff), 2):
                # wavelength factor 1/1000: nm --> microns
                wl_mu = wavelength / 1000.0
                eps += g(self.coeff[i], self.coeff[i + 1], wl_mu)

        else:
            raise ValueError(
                "Only formula '1' (Sellmeier) or 'data' models supported so far."
            )

        return eps

    def _get_eps_single_wl(self, wavelength):
        # memoize evaluations
        wl_key = float(wavelength)

        if wl_key in self.lookup_eps:
            eps = self.lookup_eps[wl_key]
        else:
            _eps = self._eval(wavelength)
            eps = torch.eye(
                3, dtype=DTYPE_COMPLEX, device=self.device
            ) * torch.as_tensor(_eps, dtype=DTYPE_COMPLEX, device=self.device)
            self.lookup_eps[wl_key] = eps

        return eps

    def get_epsilon(self, wavelength):
        """get permittivity at `wavelength`

        Args:
            wavelength (float): in nm

        Returns:
            torch.Tensor: (3,3) complex permittivity tensor at `wavelength`
        """
        wavelength = torch.as_tensor(wavelength, dtype=DTYPE_FLOAT, device=self.device)

        # multiple wavelengths
        if len(torch.as_tensor(wavelength).shape) == 1:
            eps = torch.stack([self._get_eps_single_wl(wl) for wl in wavelength], dim=0)
        else:
            eps = self._get_eps_single_wl(wavelength)

        return eps
