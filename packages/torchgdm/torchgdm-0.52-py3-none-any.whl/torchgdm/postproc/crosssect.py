# -*- coding: utf-8 -*-
"""
scattering / extinction / absorption cross sections
"""
# %%
import warnings

import torch

from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX
from torchgdm.tools.misc import get_default_device
from torchgdm.tools.misc import get_closest_wavelength
from torchgdm.tools.batch import get_p_m_radiative_correction_prefactors


def ecs(
    sim,
    wavelength: float,
    illumination_index: int = None,  # None: batch all illumination fields
    normalize_to_local_e0: bool = False,
    **kwargs,
):
    """total extinction cross section

    further kwargs are ignored

    Args:
        sim (:class:`torchgdm.Simulation`): simulation instance
        wavelength (float): in nm
        illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.
        normalize_to_local_e0 (bool, optional): Whether to normalize to local illumination amplitude. Can be useful to get an approximate cross-section for non-plane wave illuminations. Defaults to False.

    Returns:
        dict: dictionaty containing the extinction cross section
    """

    from torchgdm.tools.misc import _test_illumination_field_is_plane_wave

    # =============================================================================
    #     Exception handling
    # =============================================================================

    wavelength = get_closest_wavelength(sim, wavelength)

    _test_illumination_field_is_plane_wave(
        sim,
        illumination_index,
        message="Extinction cross sections are only defined for plane wave illuminations! ",
    )

    # =============================================================================
    #     main calculation
    # =============================================================================

    # source positions and dipole moments
    p, m, r_p, r_m = sim.get_p_m_selfconsistent(wavelength, illumination_index)

    k0 = 2.0 * torch.pi / wavelength

    # environment ref. index at each source
    eps_env_at_p = sim.environment.get_environment_permittivity_scalar(
        wavelength, r_probe=r_p
    )
    eps_env_at_m = sim.environment.get_environment_permittivity_scalar(
        wavelength, r_probe=r_m
    )
    n_env_at_p = (eps_env_at_p**0.5).real
    n_env_at_m = (eps_env_at_m**0.5).real

    # optionally normalize each contribution to the local field amplitude
    conf = dict(wavelength=wavelength, illumination_index=illumination_index)
    inc_fields_at_p = sim.get_fields_inc(**conf, r_probe=r_p)
    inc_fields_at_m = sim.get_fields_inc(**conf, r_probe=r_m)
    e0_at_p = inc_fields_at_p.get_efield(warn=False)
    h0_at_m = inc_fields_at_m.get_hfield(warn=False)
    if normalize_to_local_e0:
        # illumination fields
        e0_at_m = inc_fields_at_m.get_efield(warn=False)
        # intensities
        I0_at_p = torch.sum(torch.abs(e0_at_p) ** 2, dim=-1)
        I0_at_m = torch.sum(torch.abs(e0_at_m) ** 2, dim=-1)
    else:
        I0_at_p = torch.ones(p.shape[:-1], device=p.device)
        I0_at_m = torch.ones(m.shape[:-1], device=m.device)

    ext_factor_p = (4 * torch.pi * k0 / (n_env_at_p * I0_at_p)).real.unsqueeze(-1)
    ext_factor_m = (4 * torch.pi * k0 / (n_env_at_m * I0_at_m)).real.unsqueeze(-1)

    cs_ext_p = (ext_factor_p * torch.multiply(torch.conj(e0_at_p), p)).imag.sum((1, 2))
    cs_ext_m = (ext_factor_m * torch.multiply(torch.conj(h0_at_m), m)).imag.sum((1, 2))
    cs_ext = cs_ext_p + cs_ext_m
    
    return dict(ecs=cs_ext.real)


def acs(
    sim,
    wavelength: float,
    illumination_index: int = None,  # None: batch all illumination fields
    normalize_to_local_e0: bool = False,
    radiative_correction: bool = True,
    **kwargs,
):
    """total absorption cross section

    further kwargs are ignored

    Args:
        sim (:class:`torchgdm.Simulation`): simulation instance
        wavelength (float): in nm
        illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.

    Returns:
        dict: dictionaty containing the absorption cross section
    """
    # c.f. [Chaumet & Rahmani. JQSRT 110, 22–29 (2009), doi: 10.1016/j.jqsrt.2008.09.004]
    from torchgdm.tools.misc import _test_illumination_field_is_plane_wave

    # =============================================================================
    #     Exception handling
    # =============================================================================

    wavelength = get_closest_wavelength(sim, wavelength)

    _test_illumination_field_is_plane_wave(
        sim,
        illumination_index,
        message="Absorption cross sections are only defined for plane wave illuminations! ",
    )

    # =============================================================================
    #     main calculation
    # =============================================================================

    # source positions and dipole moments
    p, m, r_p, r_m = sim.get_p_m_selfconsistent(wavelength, illumination_index)
    e_at_p, h_at_m, r_p, r_m = sim.get_e_h_selfconsistent(wavelength, illumination_index)

    k0 = 2.0 * torch.pi / wavelength

    # environment ref. index at each source
    eps_env_at_p = sim.environment.get_environment_permittivity_scalar(
        wavelength, r_probe=r_p
    )
    eps_env_at_m = sim.environment.get_environment_permittivity_scalar(
        wavelength, r_probe=r_m
    )
    n_env_at_p = (eps_env_at_p**0.5).real
    n_env_at_m = (eps_env_at_m**0.5).real

    # optionally normalize each contribution to the local field amplitude
    if normalize_to_local_e0:
        # illumination fields
        conf = dict(wavelength=wavelength, illumination_index=illumination_index)
        inc_fields_at_p = sim.get_fields_inc(**conf, r_probe=r_p)
        inc_fields_at_m = sim.get_fields_inc(**conf, r_probe=r_m)
        e0_at_p = inc_fields_at_p.get_efield(warn=False)
        e0_at_m = inc_fields_at_m.get_efield(warn=False)
        # intensities
        I0_at_p = torch.sum(torch.abs(e0_at_p) ** 2, dim=-1)
        I0_at_m = torch.sum(torch.abs(e0_at_m) ** 2, dim=-1)
    else:
        I0_at_p = torch.ones(p.shape[:-1], device=p.device)
        I0_at_m = torch.ones(m.shape[:-1], device=m.device)

    # --- absorption
    abs_factor_p = (4 * torch.pi * k0 / (n_env_at_p * I0_at_p)).real.unsqueeze(-1)
    abs_factor_m = (4 * torch.pi * k0 / (n_env_at_m * I0_at_m)).real.unsqueeze(-1)

    cs_abs_p = (abs_factor_p * torch.multiply(p, torch.conj(e_at_p))).imag.sum((1, 2))
    cs_abs_m = (abs_factor_m * torch.multiply(m, torch.conj(h_at_m))).imag.sum((1, 2))

    # radiative correction:
    f_rad_p, f_rad_m = get_p_m_radiative_correction_prefactors(sim, wavelength)

    rad_corr_p = (
        abs_factor_p * (torch.multiply(p * f_rad_p.unsqueeze(0), torch.conj(p)))
    ).sum((1, 2))

    rad_corr_m = (
        abs_factor_m * (torch.multiply(m * f_rad_m.unsqueeze(0), torch.conj(m)))
    ).sum((1, 2))

    cs_abs_p = cs_abs_p - rad_corr_p
    cs_abs_m = cs_abs_m - rad_corr_m

    cs_abs = (cs_abs_p + cs_abs_m).real

    return dict(acs=cs_abs.real)


def scs(
    sim,
    wavelength: float,
    illumination_index: int = None,  # None: batch all illumination fields
    normalize_to_local_e0: bool = False,
    radiative_correction: bool = True,
    **kwargs,
):
    """total scattering cross section

    This function also returns extinction and absorption cross-sections, which are calculated as byproducts

    further kwargs are ignored

    Args:
        sim (:class:`torchgdm.Simulation`): simulation instance
        wavelength (float): in nm
        illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.
        normalize_to_local_e0 (bool, optional): Whether to normalize to local illumination amplitude. Can be useful to get an approximate cross-section for non-plane wave illuminations. Defaults to False.
        radiative_correction (bool, optional): Whether to add radiative correction term. Defaults to True.

    Returns:
        dict: dictionaty containing the scattering, absorption and extinction cross sections
    """
    from torchgdm.tools.misc import _test_illumination_field_is_plane_wave

    # =============================================================================
    #     Exception handling
    # =============================================================================

    wavelength = get_closest_wavelength(sim, wavelength)

    _test_illumination_field_is_plane_wave(
        sim,
        illumination_index,
        message="Scattering cross sections are only defined for plane wave illuminations! ",
    )

    # =============================================================================
    #     main calculation
    # =============================================================================

    # --- general pre-calculation
    # source positions and dipole moments
    p, m, r_p, r_m = sim.get_p_m_selfconsistent(wavelength, illumination_index)
    e_at_p, h_at_m, r_p, r_m = sim.get_e_h_selfconsistent(wavelength, illumination_index)

    k0 = 2.0 * torch.pi / wavelength

    # environment ref. index at each source
    eps_env_at_p = sim.environment.get_environment_permittivity_scalar(
        wavelength, r_probe=r_p
    )
    eps_env_at_m = sim.environment.get_environment_permittivity_scalar(
        wavelength, r_probe=r_m
    )
    n_env_at_p = (eps_env_at_p**0.5).real
    n_env_at_m = (eps_env_at_m**0.5).real

    # illumination field
    conf = dict(wavelength=wavelength, illumination_index=illumination_index)
    inc_fields_at_p = sim.get_fields_inc(**conf, r_probe=r_p)
    inc_fields_at_m = sim.get_fields_inc(**conf, r_probe=r_m)
    e0_at_p = inc_fields_at_p.get_efield(warn=False)
    e0_at_m = inc_fields_at_m.get_efield(warn=False)
    h0_at_m = inc_fields_at_m.get_hfield(warn=False)

    # optionally normalize each contribution to the local field amplitude
    if normalize_to_local_e0:
        # intensities
        I0_at_p = torch.sum(torch.abs(e0_at_p) ** 2, dim=-1)
        I0_at_m = torch.sum(torch.abs(e0_at_m) ** 2, dim=-1)
    else:
        I0_at_p = torch.ones(p.shape[:-1], device=p.device)
        I0_at_m = torch.ones(m.shape[:-1], device=m.device)

    # --- absorption
    abs_factor_p = (4 * torch.pi * k0 / (n_env_at_p * I0_at_p)).real.unsqueeze(-1)
    abs_factor_m = (4 * torch.pi * k0 / (n_env_at_m * I0_at_m)).real.unsqueeze(-1)

    cs_abs_p = (abs_factor_p * torch.multiply(p, torch.conj(e_at_p))).imag.sum((1, 2))
    cs_abs_m = (abs_factor_m * torch.multiply(m, torch.conj(h_at_m))).imag.sum((1, 2))

    # radiative correction:
    f_rad_p, f_rad_m = get_p_m_radiative_correction_prefactors(sim, wavelength)

    rad_corr_p = (
        abs_factor_p * (torch.multiply(p * f_rad_p.unsqueeze(0), torch.conj(p)))
    ).sum((1, 2))

    rad_corr_m = (
        abs_factor_m * (torch.multiply(m * f_rad_m.unsqueeze(0), torch.conj(m)))
    ).sum((1, 2))

    cs_abs_p = cs_abs_p - rad_corr_p
    cs_abs_m = cs_abs_m - rad_corr_m

    cs_abs = (cs_abs_p + cs_abs_m).real

    # --- extinction
    ext_factor_p = (4 * torch.pi * k0 / (n_env_at_p * I0_at_p)).real.unsqueeze(-1)
    ext_factor_m = (4 * torch.pi * k0 / (n_env_at_m * I0_at_m)).real.unsqueeze(-1)

    cs_ext_p = (ext_factor_p * torch.multiply(torch.conj(e0_at_p), p)).imag.sum((1, 2))
    cs_ext_m = (ext_factor_m * torch.multiply(torch.conj(h0_at_m), m)).imag.sum((1, 2))
    cs_ext = (cs_ext_p + cs_ext_m).real

    # --- scattering
    cs_scat = cs_ext - cs_abs

    return dict(scs=cs_scat, ecs=cs_ext, acs=cs_abs)


def total(
    sim,
    wavelength: float,
    illumination_index: int = None,  # None: batch all illumination fields
    normalize_to_local_e0: bool = False,
    radiative_correction: bool = True,
    **kwargs,
):
    """alias for :func:`scs`.

    compute total cross sections: extinction, absorption and scattering

    Args:
        sim (:class:`torchgdm.Simulation`): simulation instance
        wavelength (float): in nm
        illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.
        normalize_to_local_e0 (bool, optional): Whether to normalize to local illumination amplitude. Can be useful to get an approximate cross-section for non-plane wave illuminations. Defaults to False.
        radiative_correction (bool, optional): Whether to add radiative correction term. Defaults to True.

    Returns:
        dict: dictionaty containing the scattering, absorption and extinction cross sections
    """

    return scs(
        sim=sim,
        wavelength=wavelength,
        illumination_index=illumination_index,
        normalize_to_local_e0=normalize_to_local_e0,
        radiative_correction=radiative_correction,
        **kwargs,
    )


# --- testing
if __name__ == "__main__":
    pass
