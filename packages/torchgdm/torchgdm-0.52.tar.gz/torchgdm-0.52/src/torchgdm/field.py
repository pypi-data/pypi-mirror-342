# -*- coding: utf-8 -*-
"""
core field container class
"""
# %%
import warnings

import torch

from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX
from torchgdm.tools.misc import tqdm


# Container for fields
class Field:
    """container for electro-magnetic field data

    contains:
     - evaluation points
     - if applicable: line elements or surface elements

    routines:
     - field intensity
     - intensity integration
     - chirality
     - Poynting
     - plotting

    """

    def __init__(
        self,
        positions: torch.Tensor,
        efield: torch.Tensor,
        hfield: torch.Tensor = None,
        ds: torch.Tensor = None,
        device=None,
    ):
        """container for electro-magnetic field data

        Args:
            positions (torch.Tensor): positions at which field data exists. Either a tensor of shape (N,3), or a dict containing "r_probe" and "ds" keys.
            efield (torch.Tensor): complex electric field at positions. Shape must match the positions.
            hfield (torch.Tensor, optional): complex magnetic field at positions. Shape must match the positions. If not given, set to zero (e.g. for far-fields). Defaults to None.
            ds (torch.Tensor, optional): optional surface (or line) elements corresponding to each position. If given, used in field integration. Defaults to None.
            device (str, optional): If None, use device of `efield` tensor. Defaults to None.

        Raises:
            ValueError: insufficient inputs provided
        """
        # exception handling
        if efield is None and hfield is None:
            raise ValueError("At least one of efield or hfield needs to be given.")

        # set device
        if device is None:
            self.device = efield.device
        else:
            self.device = device

        # main data
        self.efield = efield
        self.hfield = hfield
        if type(positions) == dict:
            self.ds = positions["ds"] if (ds is None and "ds" in positions) else ds
            self.positions = positions["r_probe"]
        else:
            self.ds = ds
            self.positions = positions

        # set not given data to zero / unit
        if self.ds is None:  # surface elements (for integration)
            self.ds = torch.ones(
                len(self.positions), device=self.device, dtype=DTYPE_FLOAT
            )
        if self.efield is None:
            self.efield = torch.zeros_like(self.hfield)
        if self.hfield is None:
            self.hfield = torch.zeros_like(self.efield)

        # move tensors to same device as fields
        self.set_device(self.device)

        assert self.efield.shape[1:] == self.positions.shape
        assert self.hfield.shape[1:] == self.positions.shape
        assert len(self.ds) == len(self.positions)

    def __add__(self, other):
        if issubclass(type(other), Field):
            # if all positions are identical, superpose the fields
            if len(self.positions) == len(other.positions):
                if torch.all(self.positions == other.positions):
                    new_field = self.copy()
                    new_field.set_device(other.device)
                    new_field.efield = new_field.efield + other.efield
                    new_field.hfield = new_field.hfield + other.hfield

                    return new_field
            # if no points are shared, combine all positions
            if (
                len(
                    (
                        (self.positions[:, None, :] == other.positions[None, ...]).all(
                            dim=2
                        )
                    ).nonzero()
                )
                == 0
            ):
                all_pos = torch.cat([self.positions, other.positions], dim=0)
                all_e = torch.cat([self.efield, other.efield], dim=1)
                all_h = torch.cat([self.hfield, other.hfield], dim=1)
                all_ds = torch.cat([self.ds, other.ds], dim=0)
                new_field = Field(
                    positions=all_pos,
                    efield=all_e,
                    hfield=all_h,
                    ds=all_ds,
                    device=other.device,
                )
                return new_field

            raise ValueError(
                "Addition only possible if either "
                + "all positions or none of the positions are equal."
            )
        else:
            raise ValueError("Addition only possible with `Field` instances.")

    def __sub__(self, other):
        if issubclass(type(other), Field):
            assert torch.all(self.positions == other.positions)

            new_field = self.copy()
            new_field.set_device(other.device)
            new_field.efield = new_field.efield - other.efield
            new_field.hfield = new_field.hfield - other.hfield

            return new_field
        else:
            raise ValueError("Subtraction only possible with `Field` instances.")

    def __repr__(self, verbose: bool = False):
        """description about field object"""
        from torchgdm.tools.misc import ptp

        bnds = ptp(self.positions, dim=0)
        out_str = "------ E/M field container -------"
        out_str += "\n" + " nr of fields: {}".format(len(self.efield)) + "\n"
        out_str += " grid ({} positions):".format(len(self.positions)) + "\n"
        out_str += "   Nx = {:}, ".format(len(torch.unique(self.positions[:, 0])))
        out_str += "Ny = {:}, ".format(len(torch.unique(self.positions[:, 1])))
        out_str += "Nz = {:}, ".format(len(torch.unique(self.positions[:, 2])))

        out_str += "\n" + " extension (nm) : " + "\n"
        out_str += "   X  = {:.1f}, ".format(bnds[0])
        out_str += "Y  = {:.1f}, ".format(bnds[1])
        out_str += "Z  = {:.1f}, ".format(bnds[2])

        return out_str

    def cat(self, other):
        """concatenate with other field

        will add another complex field "layer" of same size
        (Nfields1, Nx, Ny), (Nfields2, Nx, Ny) --> (Nfields1 + Nfields2, Nx, Ny)
        """
        if issubclass(type(other), Field) and torch.all(
            self.positions == other.positions
        ):
            new_field = self.copy()
            new_field.set_device(other.device)
            new_field.efield = torch.cat([new_field.efield, other.efield], dim=0)
            new_field.hfield = torch.cat([new_field.hfield, other.hfield], dim=0)

            return new_field

        else:
            raise ValueError("Concatenation only possible all positions are equal.")

    def copy(self):
        import copy

        return copy.deepcopy(self)

    def set_device(self, device):
        self.positions = self.positions.to(device=device)
        self.efield = self.efield.to(device=device)
        self.ds = self.ds.to(device=device)
        if self.hfield is not None:
            self.hfield = self.hfield.to(device=device)

    def set_efield(self, efield: torch.Tensor):
        """replace the electric field by `efield`"""
        assert efield.shape[1:] == self.positions.shape
        self.efield = torch.as_tensor(efield, device=self.device)

    def set_hfield(self, hfield: torch.Tensor):
        """replace the magnetic field by `hfield`"""
        assert hfield.shape[1:] == self.positions.shape
        self.hfield = torch.as_tensor(hfield, device=self.device)

    def set_ds(self, ds: torch.Tensor):
        """replace the surface elements by `ds`"""
        assert len(ds) == len(self.positions)
        self.ds = torch.as_tensor(ds, device=self.device)

    # --- postprocessing methods
    def get_positions(self, **kwargs):
        """return all positions"""

        return self.positions

    def get_efield(self, warn=True, **kwargs):
        """return the electric field at all positions"""
        if warn and torch.sum(torch.abs(self.efield)) == 0:
            warnings.warn("No e-fields available.")

        return self.efield

    def get_hfield(self, warn=True, **kwargs):
        """return the magnetic field at all positions"""
        if warn and torch.sum(torch.abs(self.hfield)) == 0:
            warnings.warn("No h-fields available.")

        return self.hfield

    def get_efield_intensity(self, warn=True, **kwargs):
        """return the electric field intensity at all positions"""
        if warn and torch.sum(torch.abs(self.efield)) == 0:
            warnings.warn("No e-fields available.")

        I_e = torch.sum(torch.abs(self.efield) ** 2, dim=-1)
        return I_e

    def get_hfield_intensity(self, warn=True, **kwargs):
        """return the magnetic field intensity at all positions"""
        if warn and torch.sum(torch.abs(self.hfield)) == 0:
            warnings.warn("No h-fields available.")

        I_h = torch.sum(torch.abs(self.hfield) ** 2, dim=-1)
        return I_h

    def get_poynting(self, **kwargs):
        """get the complex Poynting vector at all positions

        S = conj(E) x H
        (conj(): complex conjugate)
        """
        if torch.sum(torch.abs(self.efield)) == 0:
            warnings.warn("No e-fields available.")
        if torch.sum(torch.abs(self.hfield)) == 0:
            warnings.warn("No h-fields available.")

        S = torch.cross(torch.conj(self.efield), self.hfield, dim=-1)
        return S

    def get_energy_flux(self, **kwargs):
        """time average Poynting vector at all positions

        <S>=Re(S)
        """
        return self.get_poynting().real

    def get_chirality(self, **kwargs):
        """return the near-field chirality at all positions

        calculated as in Meinzer et al, PRB 88, 041407, 2013:
        C ~ Im(conj(E) * B)
        """
        if torch.sum(torch.abs(self.efield)) == 0:
            warnings.warn("No e-fields available.")
        if torch.sum(torch.abs(self.hfield)) == 0:
            warnings.warn("No h-fields available.")

        C = (
            -1
            * torch.sum(
                torch.multiply(torch.conj(self.efield), self.hfield), dim=-1
            ).imag
        )
        return C

    # --- integration methods
    def get_integrated_efield_intensity(self, **kwargs):
        """get the integrated electric field intensity

        return sum(abs(E)^2 x dS) as a single float value
        """
        if torch.mean(torch.abs(self.efield)) == 1:
            warnings.warn("Surface elements are set to 1.")
        return torch.sum(self.get_efield_intensity() * self.ds, dim=-1)

    def get_integrated_hfield_intensity(self, **kwargs):
        """get the integrated magnetic field intensity

        return sum(abs(H)^2 x dS) as a single float value
        """
        if torch.mean(torch.abs(self.efield)) == 1:
            warnings.warn("Surface elements are set to 1.")
        return torch.sum(self.get_hfield_intensity() * self.ds, dim=-1)

    # --- plotting methods
    # - plotting for e-field
    def plot_efield_amplitude(
        self, illumination_index=0, field_component="x", complex_part="re", **kwargs
    ):
        """plot E-field amplitude using :func:`~torchgdm.visu.visu2d.field_amplitude`"""
        from torchgdm.visu.visu2d import field_amplitude as visu_field_amplitude_2d

        return visu_field_amplitude_2d(
            self,
            illumination_index=illumination_index,
            whichfield="e",
            field_component=field_component,
            complex_part=complex_part,
            **kwargs,
        )

    def plot_efield_vectors(self, illumination_index=0, **kwargs):
        """plot E-field vectors using :func:`~torchgdm.visu.visu2d.vectorfield`"""
        from torchgdm.visu.visu2d import vectorfield as visu_vectorfield_2d

        return visu_vectorfield_2d(
            self, illumination_index=illumination_index, whichfield="e", **kwargs
        )

    def plot_efield_intensity(self, illumination_index=0, **kwargs):
        """plot E-field intensity map using :func:`~torchgdm.visu.visu2d.field_intensity`"""
        from torchgdm.visu.visu2d import field_intensity as visu_field_intensity_2d

        return visu_field_intensity_2d(
            self, illumination_index=illumination_index, whichfield="e", **kwargs
        )

    def plot_efield_vectors3d(self, illumination_index=0, **kwargs):
        """plot E-field 3D vectors using :func:`~torchgdm.visu.visu3d.vectorfield`"""
        from torchgdm.visu.visu3d import vectorfield as visu_vectorfield_3d

        return visu_vectorfield_3d(
            self, illumination_index=illumination_index, whichfield="e", **kwargs
        )

    # - plotting for h-field
    def plot_hfield_amplitude(
        self, illumination_index=0, field_component="x", complex_part="re", **kwargs
    ):
        """plot H-field amplitude using :func:`~torchgdm.visu.visu2d.field_amplitude`"""
        from torchgdm.visu.visu2d import field_amplitude as visu_field_amplitude_2d

        return visu_field_amplitude_2d(
            self,
            illumination_index=illumination_index,
            whichfield="h",
            field_component=field_component,
            complex_part=complex_part,
            **kwargs,
        )

    def plot_hfield_vectors(self, illumination_index=0, **kwargs):
        """plot H-field vectors using :func:`~torchgdm.visu.visu2d.vectorfield`"""
        from torchgdm.visu.visu2d import vectorfield as visu_vectorfield_2d

        return visu_vectorfield_2d(
            self, illumination_index=illumination_index, whichfield="h", **kwargs
        )

    def plot_hfield_intensity(self, illumination_index=0, **kwargs):
        """plot H-field intensity map using :func:`~torchgdm.visu.visu2d.field_intensity`"""
        from torchgdm.visu.visu2d import field_intensity as visu_field_intensity_2d

        return visu_field_intensity_2d(
            self, illumination_index=illumination_index, whichfield="h", **kwargs
        )

    def plot_hfield_vectors3d(self, illumination_index=0, **kwargs):
        """plot H-field 3D vectors using :func:`~torchgdm.visu.visu3d.vectorfield`"""
        from torchgdm.visu.visu3d import vectorfield as visu_vectorfield_3d

        return visu_vectorfield_3d(
            self, illumination_index=illumination_index, whichfield="h", **kwargs
        )

    # - plot chirality
    def plot_chirality(self, illumination_index=0, **kwargs):
        """plot nearfield chirality :func:`~torchgdm.visu.visu2d.`"""
        from torchgdm.visu.visu2d.scalar2d import _scalarfield

        return _scalarfield(
            self.get_chirality()[illumination_index], self.positions, **kwargs
        )

    # - plotting for time averaged Poynting
    def plot_energy_flux_vectors(self, illumination_index=0, **kwargs):
        """plot energy flux vector field using :func:`torchgdm.visu.visu2d.vec2d._vectorfield`"""
        from torchgdm.visu.visu2d.vec2d import _vectorfield

        f = self.get_energy_flux()[illumination_index]

        return _vectorfield(f, self.positions, **kwargs)

    def plot_energy_flux_streamlines(self, illumination_index=0, **kwargs):
        """plot energy flux streamlines using :func:`~torchgdm.visu.visu2d.vec2d.streamlines_energy_flux`"""
        from torchgdm.visu.visu2d.vec2d import streamlines_energy_flux

        return streamlines_energy_flux(
            self, illumination_index=illumination_index, **kwargs
        )
