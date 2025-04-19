# -*- coding: utf-8 -*-
"""3D exact multipole decomposition"""
# %%
import warnings
import copy

import torch

from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX
from torchgdm.tools.misc import get_default_device
from torchgdm.tools.geometry import get_step_from_geometry
from torchgdm.tools.misc import get_closest_wavelength
from torchgdm.tools.special import sph_j0, sph_j1, sph_j2, sph_j3


def decomposition_exact(
    sim,
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
    # =============================================================================
    #     Exception handling
    # =============================================================================
    wavelength = get_closest_wavelength(sim, wavelength)

    if float(wavelength) not in sim.fields_inside:
        raise ValueError(
            "Error: simulation at requested wavelength not yet "
            + "evaluated. Call `sim.run()`."
        )

    n_dim = sim.structures[0].n_dim
    if n_dim != 3:
        raise ValueError(
            f"Dimension Error: {n_dim}D simulation, but multipoles are only "
            + "implemented for 3D simulations."
        )

    # =============================================================================
    #     preparation
    # =============================================================================
    # electric polarization density of structure
    P, M, r_p, r_m = sim.get_p_m_selfconsistent(wavelength, illumination_index)
    if len(r_m.squeeze()) > 0:
        raise ValueError(
            "Multipole decomposition does not support structures "
            + "with magnetic polarizabilties so far."
        )

    # structure. By default, use "center of mass" for multimode expansion
    if r0 is None:
        r0 = torch.mean(r_p, axis=0)
    r = r_p - r0
    r = r.unsqueeze(0)

    # avoid divergence of Bessel terms
    step = get_step_from_geometry(r_p)
    r = torch.where(
        torch.linalg.norm(r, axis=-1).unsqueeze(-1) > epsilon * step, r, epsilon
    )
    norm_r = torch.linalg.norm(r, axis=-1).unsqueeze(-1)

    # wavenumber
    eps_env_at_p = sim.environment.get_environment_permittivity_scalar(
        wavelength, r_probe=r_p
    )
    n_env_at_p = (eps_env_at_p**0.5).real.unsqueeze(0).unsqueeze(-1)
    k0 = 2.0 * torch.pi / wavelength
    k0 = torch.ones_like(n_env_at_p) * k0
    k = k0 * n_env_at_p
    kr = k * norm_r

    # precalc. bessel functions and pre-factors
    if not long_wavelength_approx:
        j0kr = sph_j0(kr)
        j1kr = sph_j1(kr) / kr
        j2kr = sph_j2(kr) / (kr**2)
        j3kr = sph_j3(kr) / (kr**3)
        f_pt = 1 / 2
        f_ptA = 3
        f_ptB = -1
        f_qe = 3
        fqe2 = 2
        fqe2A = 5
        fqe2B = -1
        fqe2C = -1
        f_m = 3 / 2
        f_qm = 15
    else:
        j0kr = torch.ones_like(kr)
        j1kr = torch.ones_like(kr)
        j2kr = torch.ones_like(kr)
        j3kr = torch.ones_like(kr)
        f_pt = 1 / 10
        f_ptA = 1
        f_ptB = -2
        f_qe = 1
        fqe2 = 1 / 14
        fqe2A = 4
        fqe2B = -5
        fqe2C = 2
        f_m = 1 / 2
        f_qm = 1

    # =============================================================================
    #     multipole calculation
    # =============================================================================
    # ----------- dipole moments
    # electric dipole
    ed_1 = torch.sum(P * j0kr, axis=1)

    ## "toroidal" dipole
    rdotp = torch.einsum(
        "kij, kij->ki", r.to(dtype=DTYPE_COMPLEX, device=sim.device), P
    ).unsqueeze(-1)
    ed_toroid = f_pt * torch.sum(
        k**2 * (f_ptA * rdotp * r + f_ptB * norm_r**2 * P) * j2kr,
        axis=1,
    )

    ed_tot = ed_1 + ed_toroid

    # magnetic dipole
    r_cross_P = torch.cross(r.to(dtype=DTYPE_COMPLEX), P, dim=-1)
    md = -1j * f_m * torch.sum(k0 * r_cross_P * j1kr, axis=1)

    # ----------- quadrupole moments
    # electric quadrupole
    eq_1 = torch.zeros((P.shape[0], 3, 3), dtype=DTYPE_COMPLEX, device=sim.device)
    eq_toroid = torch.zeros((P.shape[0], 3, 3), dtype=DTYPE_COMPLEX, device=sim.device)
    for i_a in range(3):
        for i_b in range(3):

            # diagonal term
            if i_a == i_b:
                rP_delta = rdotp
            else:
                rP_delta = torch.zeros_like(rdotp)

            # electric quadrupole
            eq_1[:, i_a, i_b] = torch.sum(
                (
                    3 * (r[..., i_a] * P[..., i_b] + r[..., i_b] * P[..., i_a])
                    - 2 * (rP_delta[..., 0])
                )
                * j1kr[..., 0],
                axis=-1,
            )

            # "toroidal" quadrupole
            eq_toroid[:, i_a, i_b] = torch.sum(
                k[..., 0] ** 2
                * (
                    fqe2A * r[..., i_a] * r[..., i_b] * rdotp[..., 0]
                    + norm_r[..., 0] ** 2
                    * (
                        fqe2B * (r[..., i_a] * P[..., i_b] + r[..., i_b] * P[..., i_a])
                        + fqe2C * rP_delta[..., 0]
                    )
                )
                * j3kr[..., 0],
                axis=-1,
            )

    eq_1 = f_qe * eq_1
    eq_toroid = f_qe * fqe2 * eq_toroid
    eq_tot = eq_1 + eq_toroid

    # magnetic quadrupole
    mq = torch.zeros((P.shape[0], 3, 3), dtype=DTYPE_COMPLEX, device=sim.device)
    for i_a in range(3):
        for i_b in range(3):
            mq[:, i_a, i_b] = torch.sum(
                k0[..., 0]
                * (
                    r[..., i_a] * r_cross_P[..., i_b]
                    + r[..., i_b] * r_cross_P[..., i_a]
                )
                * j2kr[..., 0],
                axis=-1,
            )

    mq = -1j * f_qm * mq

    return {
        "ed_1": ed_1,
        "ed_toroidal": ed_toroid,
        "ed_tot": ed_tot,
        "md": md,
        "eq_tot": eq_tot,
        "eq_1": eq_1,
        "eq_toroidal": eq_toroid,
        "mq": mq,
    }


def scs(
    sim,
    wavelength: float,
    illumination_index: int = None,  # None: batch all illumination fields
    with_toroidal=True,
    r0=None,
    epsilon=0.1,
    normalization_E0=False,
    long_wavelength_approx=False,
    **kwargs,
):
    """multipole decomposition of scattering cross section

    Returns scattering cross sections for electric and magnetic dipole and quadrupole moments.
    For details about the exact multipole formalism and scs calculation, see:

        Alaee, R., Rockstuhl, C. & Fernandez-Corbaton, I.
        *An electromagnetic multipole expansion beyond the long-wavelength approximation.*
        Optics Communications 407, 17–21 (2018)

    Args:
        sim (:class:`torchgdm.Simulation`): simulation instance
        wavelength (float): in nm
        illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.
        with_toroidal (bool, optional): whether to add toroidal moments to electric dipole and quadrupole. Defaults to True.
        r0 (torch.Tensor, optional): [x,y,z] position of multipole decomposition development. Defaults to None, in which case the center of gravity is used.
        epsilon (float, optional): positions too close to r0 will moved away from r0 by epsilon (in units of step) to avoid numerical divergence of the Bessel terms. Defaults to 0.1.
        normalization_E0 (bool, optional): Normalize to illumination amplitude at `r0`. Can be useful to get approximate results for non-plane wave illumination. Defaults to False.
        long_wavelength_approx (bool, optional): if True, use long wavelength approximation. Defaults to False.
        kwargs: Further kwargs are ignored

    Returns:
        dict:
         - 'scs_ed': electric dipole scattering cross section (in nm^2)
         - 'scs_md': magnetic dipole scattering cross section (in nm^2)
         - 'scs_eq': electric quadrupole scattering cross section (in nm^2)
         - 'scs_mq': magnetic quadrupole scattering cross section (in nm^2)
    """
    # =============================================================================
    #     Exception handling
    # =============================================================================
    from torchgdm.tools.misc import _test_illumination_field_is_plane_wave

    wavelength = get_closest_wavelength(sim, wavelength)

    _test_illumination_field_is_plane_wave(
        sim,
        illumination_index,
        message="Scattering cross sections are only defined for plane wave illuminations! ",
    )
    # =============================================================================
    #     scattering section calculation
    # =============================================================================
    which_ed = "ed_tot" if with_toroidal else "ed_1"
    which_md = "md"
    which_eq = "eq_tot" if with_toroidal else "eq_1"
    which_mq = "mq"

    # get dipole moments
    mpd = decomposition_exact(
        sim,
        wavelength=wavelength,
        illumination_index=illumination_index,
        r0=r0,
        epsilon=epsilon,
        long_wavelength_approx=long_wavelength_approx,
    )

    # by default, use "center of mass" for multimode expansion
    if r0 is None:
        P, M, r_p, r_m = sim.get_p_m_selfconsistent(wavelength, illumination_index)
        r0 = torch.mean(r_p, axis=0)

    # wavenumber
    eps_env_at_p = sim.environment.get_environment_permittivity_scalar(
        wavelength, r_probe=r0.unsqueeze(0)
    )[0]
    n_env_at_p = eps_env_at_p**0.5
    k0 = 2.0 * torch.pi / wavelength
    k = (k0 * n_env_at_p).to(sim.device)  # scalar

    # optional normalization to incident field intensity
    if normalization_E0:
        inc_fields_at_r0 = sim.get_fields_inc(
            wavelength=wavelength,
            r_probe=r0.unsqueeze(0),
            illumination_index=illumination_index,
        )
        e_inc = inc_fields_at_r0.get_efield()
        e2in = torch.sum(torch.abs(e_inc) ** 2, axis=1)  # intensity of incident field
    else:
        e2in = 1.0

    ## factor 100: cm --> m (cgs units)
    sc_factor_dp = 100 / 12 * (k0**4 / e2in).real
    sc_factor_Q = 100 / 1440 * (k0**4 / e2in).real

    scs_ed = sc_factor_dp * torch.sum(torch.abs(mpd[which_ed]) ** 2, dim=1)
    scs_md = (
        sc_factor_dp * eps_env_at_p * torch.sum(torch.abs(mpd[which_md]) ** 2, dim=1)
    )
    scs_eq = sc_factor_Q * torch.sum(torch.abs(k * mpd[which_eq]) ** 2, dim=(1, 2))
    scs_mq = (
        sc_factor_Q
        * eps_env_at_p
        * torch.sum(torch.abs(k * mpd[which_mq]) ** 2, dim=(1, 2))
    )

    return dict(
        scs_ed=scs_ed.real, scs_md=scs_md.real, scs_eq=scs_eq.real, scs_mq=scs_mq.real
    )


def ecs(
    sim,
    wavelength: float,
    illumination_index: int = None,  # None: batch all illumination fields
    with_toroidal=True,
    r0=None,
    epsilon=0.1,
    eps_dd=0.1,
    normalization_E0=False,
    long_wavelength_approx=False,
    **kwargs,
):
    """multipole decomposition of extinction cross section

    Returns extinction cross sections for electric and magnetic dipole and
    quadrupole moments of the multipole decomposition.

    *Caution:*
        The multipole extinction calculation is not entirely undiputed
        It turns out that contributions can become negative, which is
        explained by Evlyukhin et al. ([JOSA B 30, 2589 (2013)] or
        [PRB 94, 205434 (2016)]) by interactions between non-orthogonal
        multipole modes in particles that strongly break the spherical
        symmetry of this modal basis.

    For details about the extinction section of multipole moments, see:
        Evlyukhin, A. B. et al. *Multipole analysis of light scattering by
        arbitrary-shaped nanoparticles on a plane surface.*,
        JOSA B 30, 2589 (2013)

    Args:
        sim (:class:`torchgdm.Simulation`): simulation instance
        wavelength (float): in nm
        illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.
        r0 (torch.Tensor, optional): [x,y,z] position of multipole decomposition development. Defaults to None, in which case the center of gravity is used.
        epsilon (float, optional): positions too close to r0 will moved away from r0 by epsilon (in units of step) to avoid numerical divergence of the Bessel terms. Defaults to 0.1.
        eps_dd (float, optional): numerical integration step for field gradients calc. (in nm). Required for e/m quadrupoles. Defaults to 0.1.
        normalization_E0 (bool, optional): Normalize to illumination amplitude at `r0`. Can be useful to get approximate results for non-plane wave illumination. Defaults to False.
        long_wavelength_approx (bool, optional): if True, use long wavelength approximation. Defaults to False.
        kwargs: Further kwargs are ignored

    Returns:
        dict:
         - 'ecs_ed': electric dipole extinction cross section (in nm^2)
         - 'ecs_md': magnetic dipole extinction cross section (in nm^2)
         - 'ecs_eq': electric quadrupole extinction cross section (in nm^2)
         - 'ecs_mq': magnetic quadrupole extinction cross section (in nm^2)
    """

    from torchgdm.postproc.fields import field_gradient
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
    #     extinction section calculation
    # =============================================================================
    which_ed = "ed_tot" if with_toroidal else "ed_1"
    which_md = "md"
    which_eq = "eq_tot" if with_toroidal else "eq_1"
    which_mq = "mq"

    # get dipole moments
    mpd = decomposition_exact(
        sim,
        wavelength=wavelength,
        illumination_index=illumination_index,
        r0=r0,
        epsilon=epsilon,
        long_wavelength_approx=long_wavelength_approx,
    )

    # by default, use "center of mass" for multimode expansion
    if r0 is None:
        P, M, r_p, r_m = sim.get_p_m_selfconsistent(wavelength, illumination_index)
        r0 = torch.mean(r_p, axis=0)

    # wavenumber
    eps_env_at_p = sim.environment.get_environment_permittivity_scalar(
        wavelength, r_probe=r0.unsqueeze(0)
    )[0]
    n_env_at_r0 = eps_env_at_p**0.5
    k0 = 2.0 * torch.pi / wavelength

    # illumination field and its gradients (index [:, 0, :] --> at single position `r0`)
    inc_fields_at_r0 = sim.get_fields_inc(
            wavelength=wavelength,
            r_probe=r0.unsqueeze(0),
            illumination_index=illumination_index,
        )
    e_inc = inc_fields_at_r0.get_efield()
    h_inc = inc_fields_at_r0.get_hfield()
    
    e_inc_cj = torch.conj(e_inc)[:, 0, :]
    h_inc_cj = torch.conj(h_inc)[:, 0, :]

    grad_e_inc_dict = field_gradient(
        sim, wavelength, r0.unsqueeze(0), whichfield="e_inc", delta=eps_dd
    )
    grad_e_inc = torch.concatenate(
        [grad_e_inc_dict["dfdx"], grad_e_inc_dict["dfdy"], grad_e_inc_dict["dfdz"]],
        dim=1,
    )
    grad_h_inc_dict = field_gradient(
        sim, wavelength, r0.unsqueeze(0), whichfield="h_inc", delta=eps_dd
    )
    grad_h_inc = torch.concatenate(
        [grad_h_inc_dict["dfdx"], grad_h_inc_dict["dfdy"], grad_h_inc_dict["dfdz"]],
        dim=1,
    )

    grad_e_inc_cj_T = torch.transpose(torch.conj(grad_e_inc), dim0=1, dim1=2)
    grad_h_inc_cj_T = torch.transpose(torch.conj(grad_h_inc), dim0=1, dim1=2)

    # optional normalization to incident field intensity
    if normalization_E0:
        e2in = torch.sum(torch.abs(e_inc) ** 2, axis=1)  # intensity of incident field
    else:
        e2in = 1.0

    # calculate the decomposition
    prefactor = (4.0 * torch.pi * k0 / n_env_at_r0 / e2in).real

    ecs_ed = prefactor * (torch.sum(e_inc_cj * mpd[which_ed], dim=1)).imag

    ecs_md = prefactor * (torch.sum(h_inc_cj * mpd[which_md], dim=1)).imag

    ecs_eq = (prefactor / 12.0) * (
        torch.sum(
            (torch.conj(grad_e_inc) + grad_e_inc_cj_T) * mpd[which_eq], dim=(1, 2)
        )
    ).imag

    ecs_mq = (prefactor / 6.0) * (
        torch.sum((grad_h_inc_cj_T * mpd[which_mq].transpose(-1, -2)), dim=(1, 2))
    ).imag

    # bundle results
    return dict(
        ecs_ed=ecs_ed.real, ecs_md=ecs_md.real, ecs_eq=ecs_eq.real, ecs_mq=ecs_mq.real
    )
