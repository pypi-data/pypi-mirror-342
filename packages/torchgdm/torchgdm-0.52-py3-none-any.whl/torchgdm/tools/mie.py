# -*- coding: utf-8 -*-
"""Mie scattering tools using the `treams` toolkit

Mie theory tools (2d and 3d), using the treams t-matrix tool (`pip install treams`)

Beutel, D., Fernandez-Corbaton, I. & Rockstuhl, C.
**treams – a T-matrix-based scattering code for nanophotonics.**
Computer Physics Communications 297, 109076 (2024)
https://github.com/tfp-photonics/treams

"""
# %%
import warnings

import torch

from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX
from torchgdm.tools.misc import get_default_device
from torchgdm.tools.misc import tqdm, _test_illumination_field_config_exists
from torchgdm.tools.misc import to_np


def mie_ab_cylinder_2d(
    wavelengths: torch.Tensor,
    radii: list,
    materials: list,
    environment=None,
    m_max=3,
    device: torch.device = None,
    as_dict=False,
):
    """2D Mie coefficients for a multi-layer infinite cylinder

    Args:
        wavelengths (torch.Tensor): list of wavelengths (in nm).
        radii (list): radius or list of radii (multilayer).
        materials (list): material, or list of mateirals. Either float (interpreted as permittivity) or a material from :mod:`torchgdm.materials`.
        environment (float or environment, optional): TorchGDM environment. If `None`, use vacuum. If float, use the value as permittivity. Defaults to None.
        m_max (int, optional): maximum order. Defaults to 3.
        device (torch.device, optional): device for output tensors. If not give, use default device. Defaults to None.
        as_dict (bool, optional): If True, return more detailed results in dict. If False, only return a and b. Defaults to False.

    Raises:
        ValueError: if required package `treams` is not found

    Returns:
        tuple or dict: tuple containing (a, b) or dict with "a_n" and "b_n" keys containing coefficients, amongst other info.
    """
    # normal incidence 2D Mie
    from torchgdm.tools.misc import to_np
    from torchgdm.tools.misc import _check_environment
    from torchgdm.materials.base_classes import MaterialBase
    from torchgdm.materials import MatConstant
    import numpy as np

    # TODO: Replace with differentiable Mie code
    try:
        # ignore import warnings
        with warnings.catch_warnings():
            import treams
    except ModuleNotFoundError:
        print("Requires `treams`, install via `pip install treams`.")
        raise

    if device is None:
        device = get_default_device()
    else:
        device = device

    # environment
    env = _check_environment(environment, N_dim=2, device=device)

    # tensor conversion
    wavelengths = torch.as_tensor(wavelengths, dtype=DTYPE_FLOAT, device=device)
    wavelengths = torch.atleast_1d(wavelengths)
    k0 = 2 * torch.pi / wavelengths
    k0 = torch.as_tensor(k0, device=device)
    kz = 0.0

    # radii to array
    radii = np.atleast_1d(radii)
    r_enclosing = np.max(radii)  # outer radius

    # if single material, put in list
    if not hasattr(materials, "__iter__"):
        materials = [materials]

    # main Mie extraction and setup
    a_n = np.zeros((len(wavelengths), m_max), dtype=np.complex128)
    b_n = np.zeros_like(a_n)
    n_env = np.zeros(len(wavelengths), dtype=np.complex128)
    for i_wl, wl in enumerate(wavelengths):
        # embedding medium and wavevector therein
        eps_env = to_np(env.env_material.get_epsilon(wavelength=wl))[0, 0]
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

        for m in range(m_max):
            miecoef = treams.coeffs.mie_cyl(
                kz, m, to_np(k0[i_wl]), radii, *zip(*mat_treams)
            )
            a_n[i_wl, m] = -miecoef[0, 0] - miecoef[0, 1]
            b_n[i_wl, m] = -miecoef[0, 0] + miecoef[0, 1]

    a_n = torch.as_tensor(a_n, device=device, dtype=DTYPE_COMPLEX)
    b_n = torch.as_tensor(b_n, device=device, dtype=DTYPE_COMPLEX)
    n_env = torch.as_tensor(n_env, device=device, dtype=DTYPE_COMPLEX)

    if as_dict:
        return dict(
            a_n=a_n,
            b_n=b_n,
            environment=env,
            n_env=n_env,
            device=device,
            r_enclosing=r_enclosing,
            wavelengths=wavelengths,
        )
    else:
        return a_n, b_n


def mie_ab_sphere_3d(
    wavelengths: torch.Tensor,
    radii: list,
    materials: list,
    environment=None,
    l_max=2,
    device: torch.device = None,
    as_dict=False,
):
    """3D Mie coefficients for a multi-layer sphere

    Args:
        wavelengths (torch.Tensor): list of wavelengths (in nm).
        radii (list): radius or list of radii (multilayer).
        materials (list): material, or list of mateirals. Either float (interpreted as permittivity) or a material from :mod:`torchgdm.materials`.
        environment (float or environment, optional): TorchGDM environment. If `None`, use vacuum. If float, use the value as permittivity. Defaults to None.
        l_max (int, optional): maximum order. Defaults to 2.
        device (torch.device, optional): device for output tensors. If not give, use default device. Defaults to None.
        as_dict (bool, optional): If True, return more detailed results in dict. If False, only return a and b. Defaults to False.

    Raises:
        ValueError: if required package `treams` is not found

    Returns:
        tuple or dict: tuple containing (a, b) or dict with "a_n" and "b_n" keys containing coefficients, amongst other info.
    """
    from torchgdm.tools.misc import to_np
    from torchgdm.tools.misc import _check_environment
    from torchgdm.materials.base_classes import MaterialBase
    from torchgdm.materials import MatConstant
    import numpy as np

    # TODO: Replace with differentiable Mie code
    try:
        # ignore import warnings
        with warnings.catch_warnings():
            import treams
    except ModuleNotFoundError:
        print("Requires `treams`, install via `pip install treams`.")
        raise

    if device is None:
        device = get_default_device()
    else:
        device = device

    # environment
    env = _check_environment(environment, N_dim=3, device=device)

    # tensor conversion
    wavelengths = torch.as_tensor(wavelengths, dtype=DTYPE_FLOAT, device=device)
    wavelengths = torch.atleast_1d(wavelengths)
    k0 = 2 * torch.pi / wavelengths
    k0 = torch.as_tensor(k0, device=device)

    # radii to array
    radii = np.atleast_1d(radii)
    r_enclosing = np.max(radii)  # outer radius

    # if single material, put in list
    if not hasattr(materials, "__iter__"):
        materials = [materials]

    # main Mie extraction and setup
    a_n = np.zeros((len(wavelengths), l_max), dtype=np.complex128)
    b_n = np.zeros_like(a_n)
    n_env = np.zeros(len(wavelengths), dtype=np.complex128)
    for i_wl, wl in enumerate(wavelengths):
        # embedding medium and wavevector therein
        eps_env = to_np(env.env_material.get_epsilon(wavelength=wl))[0, 0]
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

        for l in range(1, l_max + 1):
            miecoef = treams.coeffs.mie(
                l, to_np(k0[i_wl]) * np.array(radii), *zip(*mat_treams)
            )
            a_n[i_wl, l - 1] = -miecoef[0, 0] - miecoef[0, 1]
            b_n[i_wl, l - 1] = -miecoef[0, 0] + miecoef[0, 1]

    a_n = torch.as_tensor(a_n, device=device, dtype=DTYPE_COMPLEX)
    b_n = torch.as_tensor(b_n, device=device, dtype=DTYPE_COMPLEX)
    n_env = torch.as_tensor(n_env, device=device, dtype=DTYPE_COMPLEX)

    if as_dict:
        return dict(
            a_n=a_n,
            b_n=b_n,
            environment=env,
            n_env=n_env,
            device=device,
            r_enclosing=r_enclosing,
            wavelengths=wavelengths,
        )
    else:
        return a_n, b_n


def mie_crosssections_cylinder_2d(
    wavelengths: torch.Tensor,
    radii: list,
    materials: list,
    environment=None,
    m_max=10,
    device: torch.device = None,
):
    """2D Mie cross widths in nm, of multi-layer infinite cylinder

    Args:
        wavelengths (torch.Tensor): list of wavelengths (in nm).
        radii (list): radius or list of radii (multilayer).
        materials (list): material, or list of mateirals. Either float (interpreted as permittivity) or a material from :mod:`torchgdm.materials`.
        environment (float or environment, optional): TorchGDM environment. If `None`, use vacuum. If float, use the value as permittivity. Defaults to None.
        m_max (int, optional): maximum order. Defaults to 3.
        device (torch.device, optional): device for output tensors. If not give, use default device. Defaults to None.
        as_dict (bool, optional): If True, return more detailed results in dict. If False, only return a and b. Defaults to False.

    Raises:
        ValueError: if required package `treams` is not found

    Returns:
        dict: dict containing all relevant cross widths (abs, ext, scat, geometric) and efficiencies (scaled by 1/sigma_geo). For TE (perp.), TM (parallel) polarizations.
    """
    # see Bohren Huffmann, chapter 8.4
    # no autodiff!
    mie_results = mie_ab_cylinder_2d(
        wavelengths=wavelengths,
        radii=radii,
        materials=materials,
        environment=environment,
        m_max=m_max,
        device=device,
        as_dict=True,
    )
    a = mie_results["a_n"]
    b = mie_results["b_n"]
    n_env = mie_results["n_env"]
    r_enclosing = mie_results["r_enclosing"]
    wavelengths = mie_results["wavelengths"]

    k = n_env * 2 * torch.pi / torch.as_tensor(wavelengths)
    size_param = (k * r_enclosing).real

    # scattering
    Qs_mie_par = torch.abs(a[:, 0]) ** 2
    Qs_mie_perp = torch.abs(b[:, 0]) ** 2
    Qs_mie_par += 2 * torch.sum(torch.abs(a[:, 1:]) ** 2, dim=1)
    Qs_mie_perp += 2 * torch.sum(torch.abs(b[:, 1:]) ** 2, dim=1)

    Qs_mie_par *= 2 / size_param
    Qs_mie_perp *= 2 / size_param
    Qs_mie_avg = (Qs_mie_par + Qs_mie_perp) / 2

    Cs_mie_par = Qs_mie_par * 2 * r_enclosing
    Cs_mie_perp = Qs_mie_perp * 2 * r_enclosing
    Cs_mie_avg = Qs_mie_avg * 2 * r_enclosing

    # extinction
    Qe_mie_par = (a[:, 0]).real
    Qe_mie_perp = (b[:, 0]).real
    Qe_mie_par += 2 * torch.sum((a[:, 1:]), dim=1).real
    Qe_mie_perp += 2 * torch.sum((b[:, 1:]), dim=1).real

    Qe_mie_par *= 2 / size_param
    Qe_mie_perp *= 2 / size_param
    Qe_mie_avg = (Qe_mie_par + Qe_mie_perp) / 2

    Ce_mie_par = Qe_mie_par * 2 * r_enclosing
    Ce_mie_perp = Qe_mie_perp * 2 * r_enclosing
    Ce_mie_avg = Qe_mie_avg * 2 * r_enclosing

    return dict(
        Qsca_perp=Qs_mie_perp,
        Qsca_par=Qs_mie_par,
        Qsca_avg=Qs_mie_avg,
        Csca_perp=Cs_mie_perp,
        Csca_par=Cs_mie_par,
        Csca_avg=Cs_mie_avg,
        Qext_perp=Qe_mie_perp,
        Qext_par=Qe_mie_par,
        Qext_avg=Qe_mie_avg,
        Cext_perp=Ce_mie_perp,
        Cext_par=Ce_mie_par,
        Cext_avg=Ce_mie_avg,
        Qabs_perp=Qe_mie_perp - Qs_mie_perp,
        Qabs_par=Qe_mie_par - Qs_mie_par,
        Qabs_avg=Qe_mie_avg - Qs_mie_avg,
        Cabs_perp=Ce_mie_perp - Cs_mie_perp,
        Cabs_par=Ce_mie_par - Cs_mie_par,
        Cabs_avg=Ce_mie_avg - Cs_mie_avg,
        Cgeo=torch.ones_like(Cs_mie_avg) * 2 * r_enclosing,
    )


def mie_crosssections_sphere_3d(
    wavelengths: torch.Tensor,
    radii: list,
    materials: list,
    environment=None,
    l_max=10,
    device: torch.device = None,
):
    """3D Mie cross sections in nm^2, of a multi-layer sphere

    Args:
        wavelengths (torch.Tensor): list of wavelengths (in nm).
        radii (list): radius or list of radii (multilayer).
        materials (list): material, or list of mateirals. Either float (interpreted as permittivity) or a material from :mod:`torchgdm.materials`.
        environment (float or environment, optional): TorchGDM environment. If `None`, use vacuum. If float, use the value as permittivity. Defaults to None.
        m_max (int, optional): maximum order. Defaults to 3.
        device (torch.device, optional): device for output tensors. If not give, use default device. Defaults to None.
        as_dict (bool, optional): If True, return more detailed results in dict. If False, only return a and b. Defaults to False.

    Raises:
        ValueError: if required package `treams` is not found

    Returns:
        dict: dict containing all relevant cross sections (abs, ext, scat, geometric) and efficiencies (scaled by 1/sigma_geo).
    """
    # see Bohren Huffmann, chapter 4.4
    # no autodiff!
    mie_results = mie_ab_sphere_3d(
        wavelengths=wavelengths,
        radii=radii,
        materials=materials,
        environment=environment,
        l_max=l_max,
        device=device,
        as_dict=True,
    )
    a = mie_results["a_n"]
    b = mie_results["b_n"]
    n_env = mie_results["n_env"]
    r_enclosing = mie_results["r_enclosing"]
    device = mie_results["device"]
    wavelengths = mie_results["wavelengths"]

    k = n_env * 2 * torch.pi / torch.as_tensor(wavelengths)
    size_param = (k * r_enclosing).real

    # scattering
    Qs_mie = torch.zeros(len(wavelengths), dtype=DTYPE_FLOAT, device=device)
    for l in range(l_max):
        Qs_mie += (2 * (l + 1) + 1) * (
            torch.abs(a[:, l]) ** 2 + torch.abs(b[:, l]) ** 2
        )

    Qs_mie *= 2 / size_param**2

    Cs_mie = Qs_mie * torch.pi * r_enclosing**2

    # extinction
    Qe_mie = torch.zeros(len(wavelengths), dtype=DTYPE_FLOAT, device=device)
    for l in range(l_max):
        Qe_mie += (2 * (l + 1) + 1) * (a[:, l] + b[:, l]).real

    Qe_mie *= 2 / size_param**2

    Ce_mie = Qe_mie * torch.pi * r_enclosing**2

    return dict(
        Qsca=Qs_mie,
        Csca=Cs_mie,
        Qext=Qe_mie,
        Cext=Ce_mie,
        Cgeo=torch.ones_like(Ce_mie) * torch.pi * r_enclosing**2,
    )
