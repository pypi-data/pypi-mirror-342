# -*- coding: utf-8 -*-
"""T-matrix tools using the `treams` toolkit

Tools to convert T-matrices to GPM structures

Requires treams (`pip install treams`).

Beutel, D., Fernandez-Corbaton, I. & Rockstuhl, C.
**treams – a T-matrix-based scattering code for nanophotonics.**
Computer Physics Communications 297, 109076 (2024)
https://github.com/tfp-photonics/treams

"""
import warnings

import numpy as np
import torch

from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX
from torchgdm.tools.misc import to_np


def spherical_wave_source_treams(
    k0, l, m, pol, mat_env=1.0, r_spherical_wave_source=[0, 0, 0], l_max=2
):
    """E and H field of a spherical wave source

    Args:
        k0 (float): wavnumber (2*pi / lambda0, in nm^-1)
        l (int): degree
        m (int): order
        pol (int): treams polarization
        mat_env (float, material): treams material or float. Float is interpreted as environment's permittivity.
        r_spherical_wave_source (list, optional): Cartesian location of source in nm. Defaults to [0, 0, 0].
        l_max (int, optional): maximum degree of expansion. Defaults to 2.

    Returns:
        spherical wave source

    Raises:
        ValueError: if required package `treams` is not found

    """
    try:
        # ignore import warnings
        with warnings.catch_warnings():
            import treams
    except ModuleNotFoundError:
        print("Requires `treams`, install via `pip install treams`.")
        raise

    spw = treams.spherical_wave(
        l=l, m=m, pol=pol, k0=k0, material=mat_env, modetype="regular", poltype="parity"
    )

    local_swb = treams.SphericalWaveBasis.default(
        l_max, positions=l_max * [r_spherical_wave_source]
    )

    ex_sph = spw.expand.apply_left(local_swb)

    return ex_sph


def cylindrical_wave_source_treams(
    k0,
    m,
    pol,
    k_par=0,
    mat_env=1.0,
    r_cyl_wave_source=[0, 0, 0],
    m_max=2,
):
    """E and H field of a cylindrical wave source in the XY(!!) plane

    Caution: infinite axis is along Z (=treams default; torchgdm default is Y axis)

    Args:
        k0 (float): wavnumber (2*pi / lambda0, in nm^-1)
        m (int): order
        pol (int): treams polarization. 0: TE (E in xy plane). 1: TM (E along z).
        k_par (float): wavevector component along the infinite axis (torchgdm: y-axis).
        mat_env (float, material): treams material or float. Float is interpreted as environment's permittivity.
        r_cyl_wave_source (list, optional): Cartesian location of source in nm. Defaults to [0, 0, 0].
        m_max (int, optional): maximum degree of expansion. Defaults to 2.

    Returns:
        cylindrical wave source

    Raises:
        ValueError: if required package `treams` is not found

    """
    try:
        # ignore import warnings
        with warnings.catch_warnings():
            import treams
    except ModuleNotFoundError:
        print("Requires `treams`, install via `pip install treams`.")
        raise

    cw = treams.cylindrical_wave(
        m=m,
        pol=pol,
        k0=k0,
        kz=k_par,
        material=mat_env,
        modetype="regular",
        poltype="parity",
    )

    local_cwb = treams.CylindricalWaveBasis.default(
        kzs=k_par, mmax=m_max, positions=r_cyl_wave_source
    )

    ex_sph = cw.expand.apply_left(local_cwb)

    return ex_sph


def setup_spherical_waves_treams(r_source, k0, l_max, m_max, mat_env=1.0):
    try:
        # ignore import warnings
        with warnings.catch_warnings():
            import treams
    except ModuleNotFoundError:
        print("Requires `treams`, install via `pip install treams`.")
        raise

    r_source = np.atleast_2d(r_source)

    inc_fields = []
    for i, r_s in enumerate(r_source):

        # generate random configurations for each source
        _l = np.random.randint(1, l_max + 1)
        _pol = np.random.randint(0, 2)  # 0 or 1
        m_lim = min([_l, m_max])
        _m = np.random.randint(-m_lim, m_lim + 1)

        sw_source = spherical_wave_source_treams(
            k0=k0,
            l=_l,
            m=_m,
            pol=_pol,
            mat_env=mat_env,
            r_spherical_wave_source=r_s,
            l_max=_l,
        )
        inc_fields.append(sw_source)

    return inc_fields


def setup_cylindrical_waves_treams(r_source, k0, m_max, mat_env=1.0):
    try:
        # ignore import warnings
        with warnings.catch_warnings():
            import treams
    except ModuleNotFoundError:
        print("Requires `treams`, install via `pip install treams`.")
        raise

    r_source = np.atleast_2d(r_source)

    inc_fields = []
    for i, r_s in enumerate(r_source):

        # generate random configurations for each source
        _m = np.random.randint(-m_max, m_max + 1)
        _pol = np.random.randint(0, 2)  # 0 or 1
        _mmax = max([1, abs(_m)])
        cw_source = cylindrical_wave_source_treams(
            k0=k0, m=_m, pol=_pol, mat_env=mat_env, r_cyl_wave_source=r_s, m_max=_mmax
        )
        inc_fields.append(cw_source)

    return inc_fields


def setup_plane_waves_treams(
    n_angles, k0, mat_env, e0_amplitude=1.0, inc_planes=["xz", "xy"]
):
    try:
        # ignore import warnings
        with warnings.catch_warnings():
            import treams
    except ModuleNotFoundError:
        print("Requires `treams`, install via `pip install treams`.")
        raise

    _e0 = e0_amplitude
    inc_fields = []
    for angle in np.linspace(0, 2 * np.pi, n_angles, endpoint=False):

        # - XZ plane
        if "xz" in inc_planes:
            k0_vec = [np.sin(angle), 0, np.cos(angle)]
            # s-pol
            e0_vec = [0, _e0, 0]
            inc_fields.append(
                treams.plane_wave(
                    k0_vec, pol=e0_vec, k0=k0, material=mat_env, poltype="parity"
                )
            )
            # p-pol
            e0_vec = [np.cos(angle) * _e0, 0, np.sin(angle) * _e0]
            inc_fields.append(
                treams.plane_wave(
                    k0_vec, pol=e0_vec, k0=k0, material=mat_env, poltype="parity"
                )
            )

        # - YZ plane
        if "yz" in inc_planes:
            k0_vec = [0, np.sin(angle), np.cos(angle)]
            # s-pol
            e0_vec = [_e0, 0, 0]
            inc_fields.append(
                treams.plane_wave(
                    k0_vec, pol=e0_vec, k0=k0, material=mat_env, poltype="parity"
                )
            )
            # p-pol
            e0_vec = [0, np.cos(angle) * _e0, np.sin(angle) * _e0]
            inc_fields.append(
                treams.plane_wave(
                    k0_vec, pol=e0_vec, k0=k0, material=mat_env, poltype="parity"
                )
            )

        # - XY plane
        if "xy" in inc_planes:
            k0_vec = [np.sin(angle), np.cos(angle), 0]
            # s-pol
            e0_vec = [0, 0, _e0]
            inc_fields.append(
                treams.plane_wave(
                    k0_vec, pol=e0_vec, k0=k0, material=mat_env, poltype="parity"
                )
            )
            # p-pol
            e0_vec = [np.cos(angle) * _e0, np.sin(angle) * _e0, 0]
            inc_fields.append(
                treams.plane_wave(
                    k0_vec, pol=e0_vec, k0=k0, material=mat_env, poltype="parity"
                )
            )

    return inc_fields


# - parallelized treams evaluation (illumination and scattering)
def _eval_treams(inc, tmatrix, r_probe, r_gpm):
    try:
        # ignore import warnings
        with warnings.catch_warnings():
            import treams
    except ModuleNotFoundError:
        print("Requires `treams`, install via `pip install treams`.")
        raise

    if type(tmatrix) == treams.TMatrixC:
        assert torch.all(r_probe[..., 2] == 0), "2D treams: all z pos must be 0!"
        assert torch.all(r_gpm[..., 2] == 0), "2D treams: all z pos must be 0!"

    # - parity polarization
    if tmatrix.poltype != "parity":
        tm = tmatrix.changepoltype("parity")
    else:
        tm = tmatrix
    sca = tm @ inc.expand(tm.basis)

    # - calc incident and scattered fields
    _e_sca = sca.efield(to_np(r_probe))._array
    _h_sca = sca.hfield(to_np(r_probe))._array
    _e_inc = inc.efield(to_np(r_gpm))._array
    _h_inc = inc.hfield(to_np(r_gpm))._array

    return _e_sca, _h_sca, _e_inc, _h_inc


def convert_tmatrix3D_to_GPM(
    tmatrix,
    r_gpm,
    r_probe,
    n_src_pw_angles,
    n_src_local,
    radius_src_local,
    l_max_sw_inc=2,
    m_max_sw_inc=2,
    normalize_inc_fields=True,
    n_proc=None,
    **kwargs,
):
    try:
        from joblib import Parallel, delayed
        from joblib import cpu_count

        if n_proc is None:
            n_proc = cpu_count(only_physical_cores=True)
    except ModuleNotFoundError:
        print("Requires `joblib`, install via `pip install joblib`.")
        raise

    try:
        # ignore import warnings
        with warnings.catch_warnings():
            import treams
    except ModuleNotFoundError:
        print("Requires `treams`, install via `pip install treams`.")
        raise

    from torchgdm.env import EnvHomogeneous3D
    from torchgdm.struct.eff_model_tools import extract_gpm_from_fields
    from torchgdm.tools.geometry import sample_random_spherical
    from torchgdm.tools.misc import to_np

    _device_int = "cpu"  # torchgdm part on CPU
    assert type(tmatrix) == treams.TMatrix, "Requires treams 3D T-Matrix"
    assert tmatrix.material.epsilon.imag == 0, "absorbing environments not supported"

    _env_3d = EnvHomogeneous3D(env_material=float(tmatrix.material.epsilon.real))

    # --- setup illumination sources
    # - plane waves
    inc_fields_pw = setup_plane_waves_treams(
        n_src_pw_angles,
        k0=tmatrix.k0,
        mat_env=tmatrix.material,
        inc_planes=["xz", "yz", "xy"],
    )

    # - spherical waves
    if n_src_local > 0:
        r_sw_src = sample_random_spherical(n_src_local) * radius_src_local
        inc_fields_dp = setup_spherical_waves_treams(
            r_source=to_np(r_sw_src),
            k0=tmatrix.k0,
            l_max=l_max_sw_inc,
            m_max=m_max_sw_inc,
            mat_env=tmatrix.material,
        )
    else:
        inc_fields_dp = []
    inc_fields = inc_fields_pw + inc_fields_dp

    # - scattering and illuminations
    # illum_results = [_eval_treams(inc, tmatrix, r_probe, r_gpm) for inc in inc_fields]
    illum_results = Parallel(n_jobs=n_proc)(
        delayed(_eval_treams)(inc, tmatrix, r_probe, r_gpm) for inc in inc_fields
    )

    # - fill full arrays
    e_inc_treams = np.zeros((len(inc_fields), len(r_gpm), 3), dtype=np.complex128)
    h_inc_treams = np.zeros((len(inc_fields), len(r_gpm), 3), dtype=np.complex128)
    e_sca_treams = np.zeros((len(inc_fields), len(r_probe), 3), dtype=np.complex128)
    h_sca_treams = np.zeros((len(inc_fields), len(r_probe), 3), dtype=np.complex128)
    for i_inc, fields in enumerate(illum_results):
        if normalize_inc_fields:
            norm = max([np.abs(_f).max() for _f in fields])
        else:
            norm = 1.0

        e_sca_treams[i_inc] = fields[0] / norm
        h_sca_treams[i_inc] = fields[1] / norm
        e_inc_treams[i_inc] = fields[2] / norm
        h_inc_treams[i_inc] = fields[3] / norm

    # - optimize GPM
    GPM_dict = extract_gpm_from_fields(
        wavelength=2 * np.pi / tmatrix.k0,
        efields_sca=torch.as_tensor(e_sca_treams, device=_device_int).to(
            dtype=DTYPE_COMPLEX
        ),
        hfields_sca=torch.as_tensor(h_sca_treams, device=_device_int).to(
            dtype=DTYPE_COMPLEX
        ),
        efields_inc=torch.as_tensor(e_inc_treams, device=_device_int).to(
            dtype=DTYPE_COMPLEX
        ),
        hfields_inc=torch.as_tensor(h_inc_treams, device=_device_int).to(
            dtype=DTYPE_COMPLEX
        ),
        r_probe=r_probe,
        r_gpm=r_gpm,
        environment=_env_3d,
        device=_device_int,
        verbose=False,
        return_all_results=True,
        **kwargs,
    )

    return GPM_dict


def convert_tmatrix2D_to_GPM(
    tmatrix,
    r_gpm,
    r_probe,
    n_src_pw_angles,
    n_src_local,
    radius_src_local,
    m_max_sw_inc=1,
    normalize_inc_fields=True,
    n_proc=None,
    **kwargs,
):
    try:
        from joblib import Parallel, delayed
        from joblib import cpu_count

        if n_proc is None:
            n_proc = cpu_count(only_physical_cores=True)
    except ModuleNotFoundError:
        print("Requires `joblib`, install via `pip install joblib`.")
        raise

    try:
        # ignore import warnings
        with warnings.catch_warnings():
            import treams
    except ModuleNotFoundError:
        print("Requires `treams`, install via `pip install treams`.")
        raise

    from torchgdm.env import EnvHomogeneous2D
    from torchgdm.struct.eff_model_tools import extract_gpm_from_fields
    from torchgdm.tools.geometry import sample_random_circular
    from torchgdm.tools.misc import to_np

    _device_int = "cpu"  # torchgdm part on CPU
    assert type(tmatrix) == treams.TMatrixC, "Requires treams 2D T-Matrix (`TMatrixC`)"
    assert tmatrix.material.epsilon.imag == 0, "absorbing environments not supported"

    _env_2d = EnvHomogeneous2D(env_material=float(tmatrix.material.epsilon.real))

    # --- setup illumination sources
    # - plane waves perp. to infinite axis
    inc_fields_pw = setup_plane_waves_treams(
        n_src_pw_angles, k0=tmatrix.k0, mat_env=tmatrix.material, inc_planes=["xy"]
    )

    # - cylindrical waves
    if n_src_local > 0:
        r_sw_src = (
            sample_random_circular(n_src_local, projection="xy") * radius_src_local
        )
        from torchgdm.tools.geometry import coordinate_map_1d_circular

        r_sw_src = coordinate_map_1d_circular(
            r=radius_src_local,
            n_phi=n_src_local,
            device=_device_int,
        )["r_probe"]
        r_sw_src = r_sw_src[..., [0, 2, 1]]  # XY plane
        inc_fields_dp = setup_cylindrical_waves_treams(
            r_source=to_np(r_sw_src),
            k0=tmatrix.k0,
            m_max=m_max_sw_inc,
            mat_env=tmatrix.material,
        )
    else:
        inc_fields_dp = []
    inc_fields = inc_fields_pw + inc_fields_dp

    # - scattering and illuminations
    r_probe_z_infinite = r_probe.clone()
    r_probe_z_infinite = r_probe_z_infinite[:, [0, 2, 1]]
    r_gpm_z_infinite = r_gpm.clone()
    r_gpm_z_infinite = r_gpm_z_infinite[:, [0, 2, 1]]
    # illum_results = [_eval_treams(inc, tmatrix, r_probe_z_infinite, r_gpm_z_infinite) for inc in inc_fields]
    illum_results = Parallel(n_jobs=n_proc)(
        delayed(_eval_treams)(inc, tmatrix, r_probe_z_infinite, r_gpm_z_infinite)
        for inc in inc_fields
    )

    # - fill full arrays
    e_inc_treams = np.zeros((len(inc_fields), len(r_gpm), 3), dtype=np.complex128)
    h_inc_treams = np.zeros((len(inc_fields), len(r_gpm), 3), dtype=np.complex128)
    e_sca_treams = np.zeros((len(inc_fields), len(r_probe), 3), dtype=np.complex128)
    h_sca_treams = np.zeros((len(inc_fields), len(r_probe), 3), dtype=np.complex128)

    idx_treams = [0, 2, 1]  # treams is infinite along z
    for i_inc, fields in enumerate(illum_results):
        if normalize_inc_fields:
            norm = max([np.abs(_f).max() for _f in fields])
        else:
            norm = 1.0

        e_sca_treams[i_inc] = fields[0][..., idx_treams] / norm
        h_sca_treams[i_inc] = fields[1][..., idx_treams] / norm
        e_inc_treams[i_inc] = fields[2][..., idx_treams] / norm
        h_inc_treams[i_inc] = fields[3][..., idx_treams] / norm

    # - adapt sign of y-comp. (2D torchgdm infinite axis) component
    # treams infinite axis opposite handedness convention
    field_directions = [1, -1, 1]
    for i_f, sign in enumerate(field_directions):
        e_sca_treams[..., i_f] = e_sca_treams[..., i_f] * sign
        h_sca_treams[..., i_f] = h_sca_treams[..., i_f] * sign
        e_inc_treams[..., i_f] = e_inc_treams[..., i_f] * sign
        h_inc_treams[..., i_f] = h_inc_treams[..., i_f] * sign

    # - optimize GPM
    GPM_dict = extract_gpm_from_fields(
        wavelength=2 * np.pi / tmatrix.k0,
        efields_sca=torch.as_tensor(e_sca_treams, device=_device_int).to(
            dtype=DTYPE_COMPLEX
        ),
        hfields_sca=torch.as_tensor(h_sca_treams, device=_device_int).to(
            dtype=DTYPE_COMPLEX
        ),
        efields_inc=torch.as_tensor(e_inc_treams, device=_device_int).to(
            dtype=DTYPE_COMPLEX
        ),
        hfields_inc=torch.as_tensor(h_inc_treams, device=_device_int).to(
            dtype=DTYPE_COMPLEX
        ),
        r_probe=r_probe,
        r_gpm=r_gpm,
        environment=_env_2d,
        device=_device_int,
        verbose=False,
        return_all_results=True,
        **kwargs,
    )

    return GPM_dict


def _test_effective_model_accuracy_3d(
    struct_alpha,
    tm_list,
    which=["ecs", "nf_tot"],
    environment=None,
    r_enclosing=None,
    rtol=0.10,
    verbose=True,
    progress_bar=False,
    device=None,
):
    """test effective torchgdm model against a T-Matrix simulation (3D)

    Print some information about model accuracy

    Args:
        struct_alpha (torchgdm.struct3d.StructEffPola3D): effective polarizability structure
        tm_list (list of treams TMatrix): list of reference T-Matrix for each wavelength
        which_test (list of str, optional): Which observables to test. Can contain any of ["ecs", "nf_sca", "nf_tot"]. Defaults to ["ecs", "nf_tot"].
        environment (3D env. class, optional): Simulation environment. If None, use environment from first T-Matrix. Defaults to None.
        r_enclosing (float, optional): T-Matrix enclosing sphere radius, used for nearfield check. If not given, guess some value from the GPM. Defaults to None.
        rtol (float, optional): relative error threshold for raising warnings. Defaults to 0.10.
        verbose (bool, optional): Print detailed info. Defaults to True.
        progress_bar (bool, optional): Show progress bars. Defaults to False.
        device (str, optional): If None, use structure's device. Defaults to None.

    """
    try:
        # ignore import warnings
        with warnings.catch_warnings():
            import treams
    except ModuleNotFoundError:
        print("Requires `treams`, install via `pip install treams`.")
        raise

    from torchgdm.tools.batch import calc_spectrum
    from torchgdm.postproc import crosssect
    from torchgdm.simulation import Simulation
    from torchgdm.tools.geometry import coordinate_map_1d
    from torchgdm.tools.misc import to_np
    from torchgdm.tools.misc import _check_environment

    if device is None:
        device = struct_alpha.device

    # environment
    n_dim = struct_alpha.n_dim
    if n_dim == 3:
        from torchgdm.env.freespace_3d.inc_fields import PlaneWave
    else:
        raise ValueError(
            f"This test is for 3D structures. Given structure has N_dim={n_dim}"
        )

    if environment is None:  # use first T-Matrix
        environment = complex(tm_list[0].material.epsilon)
    env = _check_environment(environment, N_dim=n_dim, device=device)

    wavelengths = struct_alpha.wavelengths_data

    # guess some circumscribing radius if not given
    if r_enclosing is None:
        r_enclosing = (
            struct_alpha.get_all_positions().max() * 2 + struct_alpha.step.max() * 2
        )

    # nearfield calc. positions
    max_step = struct_alpha.step.max()
    z_max = r_enclosing + max_step * 2.0
    r_probe = coordinate_map_1d(
        [-500, 500], 10, r2=50, r3=z_max, direction="x", device=device
    )["r_probe"]

    # - treams
    cs_tm = {}
    cs_tm["scs"] = []
    cs_tm["ecs"] = []
    nf_tm = {}
    nf_tm["inc"] = []
    nf_tm["sca"] = []
    nf_tm["tot"] = []
    for i_wl, wl in enumerate(wavelengths):
        k0 = float(2 * np.pi / wl)
        eps_env = to_np(env.env_material.get_epsilon(wavelength=wl).real)[0, 0]
        tm = tm_list[i_wl]
        if tm.poltype != "parity":
            tm = tm.changepoltype("parity")

        kw_inc = dict(k0=k0, material=eps_env, poltype="parity")
        inc_list = [
            treams.plane_wave(kvec=[0, 0, 1], pol=[-1, 0, 0], **kw_inc),
            treams.plane_wave(kvec=[0, 0, 1], pol=[0, 1, 0], **kw_inc),
            treams.plane_wave(kvec=[-1, 0, 0], pol=[0, 0, -1], **kw_inc),
            treams.plane_wave(kvec=[-1, 0, 0], pol=[0, 1, 0], **kw_inc),
            treams.plane_wave(kvec=[0, -1, 0], pol=[0, 0, -1], **kw_inc),
            treams.plane_wave(kvec=[0, -1, 0], pol=[-1, 0, 0], **kw_inc),
        ]

        cs_tm["scs"].append([tm.xs(inc)[0] for inc in inc_list])
        cs_tm["ecs"].append([tm.xs(inc)[1] for inc in inc_list])

        for inc in inc_list:
            sca = tm @ inc.expand(tm.basis)
            _ef_tm = sca.efield(r_probe)
            _ef_inc = inc.efield(r_probe)
            nf_tm["inc"].append(_ef_inc)
            nf_tm["sca"].append(_ef_tm)
            nf_tm["tot"].append(_ef_inc + _ef_tm)

    cs_tm["scs"] = np.array(cs_tm["scs"])
    cs_tm["ecs"] = np.array(cs_tm["ecs"])

    nf_tm["inc"] = np.array(nf_tm["inc"])
    nf_tm["sca"] = np.array(nf_tm["sca"])
    nf_tm["tot"] = np.array(nf_tm["tot"])

    e_inc_list = [
        PlaneWave(e0p=1.0, e0s=0.0, inc_angle=0),  # k||z
        PlaneWave(e0p=0.0, e0s=1.0, inc_angle=0),  # k||z
        PlaneWave(e0p=1.0, e0s=0.0, inc_angle=torch.pi / 2),  # k||x
        PlaneWave(e0p=0.0, e0s=1.0, inc_angle=torch.pi / 2),  # k||x
        PlaneWave(e0p=1.0, e0s=0.0, inc_plane="yz", inc_angle=torch.pi / 2),  # k||y
        PlaneWave(e0p=0.0, e0s=1.0, inc_plane="yz", inc_angle=torch.pi / 2),  # k||y
    ]

    # setup a discretized and a effective dipole pair simulation
    sim_alpha = Simulation(
        structures=[struct_alpha],
        environment=env,
        illumination_fields=e_inc_list,
        wavelengths=wavelengths,
        device=device,
    )

    # run simulations and calc. cross section spectra
    if verbose:
        print("-" * 60)
        print("Testing effective model vs. T-Matrix (treams, 3D).")

    sim_alpha.run(verbose=False, progress_bar=progress_bar)

    test_results = dict()

    # calculate cross section errors
    cs_alpha = sim_alpha.get_spectra_crosssections(progress_bar=progress_bar)

    which_cs = []
    if "scs" in which:
        which_cs.append("scs")
    if "ecs" in which:
        which_cs.append("ecs")

    for k in which_cs:
        try:
            rel_diff = (cs_tm[k] - to_np(cs_alpha[k])) / (
                (cs_tm[k] + to_np(cs_alpha[k]))
            )
            test_results[k] = rel_diff

            mean_rel_error = np.mean(np.abs(rel_diff))
            peak_rel_error = np.max(np.abs(rel_diff))
            if verbose:
                print("cross sections - '{}':".format(k))
                print("    - mean rel. error: {:.3g}".format(mean_rel_error))
                print("    - peak rel. error: {:.3g}".format(peak_rel_error))
            if mean_rel_error > rtol:
                warnings.warn(
                    "'{}': Effective model mean relative error larger than tolerance ({:.3f} > {:.3f})".format(
                        k, mean_rel_error, rtol
                    )
                )

            elif peak_rel_error > rtol:
                warnings.warn(
                    "'{}': Effective model peak relative error larger than tolerance ({:.3f} > {:.3f})".format(
                        k, peak_rel_error, rtol
                    )
                )

            # print(cs_tm[k], rel_diff)
        except TypeError:
            pass

    # calculate nearfield errors several steps above structure
    nf_alpha = sim_alpha.get_spectra_nf(r_probe=r_probe, progress_bar=progress_bar)

    which_nf = []
    if "nf_tot" in which:
        which_nf.append("tot")
    if "nf_sca" in which:
        which_nf.append("sca")
    for k in which_nf:
        try:
            e_alpha = np.array([to_np(_nf.efield) for _nf in nf_alpha[k]])
            e_alpha = e_alpha.flatten()
            e_discr = to_np(nf_tm[k])
            e_discr = e_discr.flatten()
            rel_diff = (e_discr - e_alpha) / ((e_discr.max() + e_alpha.max()))
            test_results[k] = rel_diff

            mean_rel_error = np.mean(np.abs(rel_diff))
            peak_rel_error = np.max(np.abs(rel_diff))
            if verbose:
                print("nearfield - '{}' (at z={}nm):".format(k, int(to_np(z_max))))
                print("    - mean rel. error: {:.3g}".format(to_np(mean_rel_error)))
                print("    - peak rel. error: {:.3g}".format(to_np(peak_rel_error)))
            if mean_rel_error > rtol:
                warnings.warn(
                    "'{}': Effective model mean relative error larger than tolerance ({:.3f} > {:.3f})".format(
                        k, mean_rel_error, rtol
                    )
                )

            elif peak_rel_error > rtol:
                warnings.warn(
                    "'{}': Effective model peak relative error larger than tolerance ({:.3f} > {:.3f})".format(
                        k, peak_rel_error, rtol
                    )
                )
            # print('avg err per field config', np.mean(rel_diff, axis=(2)))

        except TypeError:
            pass
    if verbose:
        print("-" * 60)

    return test_results


def _test_effective_model_accuracy_2d(
    struct_alpha,
    tm_list,
    which=["ecs", "nf_tot"],
    environment=None,
    r_enclosing=None,
    rtol=0.10,
    verbose=True,
    progress_bar=False,
    device=None,
):
    """test effective torchgdm model against a T-Matrix simulation (2D)

    Print some information about model accuracy

    Args:
        struct_alpha (torchgdm.struct3d.StructEffPola3D): effective polarizability structure
        tm_list (list of treams TMatrix): list of reference T-Matrix for each wavelength
        which_test (list of str, optional): Which observables to test. Can contain any of ["ecs", "nf_sca", "nf_tot"]. Defaults to ["ecs", "nf_tot"].
        environment (2D env. class, optional): Simulation environment. If None, use environment from first T-Matrix. Defaults to None.
        r_enclosing (float, optional): T-Matrix enclosing sphere radius, used for nearfield check. If not given, guess some value from the GPM. Defaults to None.
        rtol (float, optional): relative error threshold for raising warnings. Defaults to 0.10.
        verbose (bool, optional): Print detailed info. Defaults to True.
        progress_bar (bool, optional): Show progress bars. Defaults to False.
        device (str, optional): If None, use structure's device. Defaults to None.

    """
    try:
        # ignore import warnings
        with warnings.catch_warnings():
            import treams
    except ModuleNotFoundError:
        print("Requires `treams`, install via `pip install treams`.")
        raise

    from torchgdm.tools.batch import calc_spectrum
    from torchgdm.simulation import Simulation
    from torchgdm.tools.misc import to_np
    from torchgdm.tools.misc import _check_environment
    from torchgdm.tools.geometry import coordinate_map_1d

    if device is None:
        device = struct_alpha.device

    # environment
    n_dim = struct_alpha.n_dim
    if environment is None:  # use first T-Matrix
        environment = complex(tm_list[0].material.epsilon)
    env = _check_environment(environment, N_dim=n_dim, device=device)

    wavelengths = struct_alpha.wavelengths_data

    # guess some circumscribing radius if not given
    if r_enclosing is None:
        r_enclosing = (
            struct_alpha.get_all_positions().max() * 2 + struct_alpha.step.max() * 2
        )

    # nearfield calc. positions
    max_step = struct_alpha.step.max()
    z_max = r_enclosing + max_step * 2.0
    r_probe = coordinate_map_1d(
        [-500, 500], 40, r2=0, r3=z_max, direction="x", device=device
    )["r_probe"]

    # probe pos. in treams coordinate convention (Y <--> Z)
    r_prb_tr = to_np(r_probe).copy()
    r_prb_tr = r_prb_tr[:, [0, 2, 1]]

    if n_dim == 2:
        from torchgdm.env.freespace_2d.inc_fields import PlaneWave
    else:
        raise ValueError(
            f"This test is for 3D structures. Given structure has N_dim={n_dim}"
        )

    # - treams
    cs_tm = {}
    cs_tm["scs"] = []
    cs_tm["ecs"] = []
    nf_tm = {}
    nf_tm["inc"] = []
    nf_tm["sca"] = []
    nf_tm["tot"] = []
    for i_wl, wl in enumerate(wavelengths):
        k0 = float(2 * np.pi / wl)
        eps_env = to_np(env.env_material.get_epsilon(wavelength=wl).real)[0, 0]
        tm = tm_list[i_wl]
        if tm.poltype != "parity":
            tm = tm.changepoltype("parity")

        # 2D treams: y <--> z; treams z-comp: sign
        kw_inc = dict(k0=k0, material=eps_env, poltype="parity")
        # inc_list = [treams.plane_wave(
        #     kvec=[0, 1, 0], pol=[1,0,0], k0=tm.k0, material=tm.material, poltype="parity"
        # )]
        inc_list = [
            treams.plane_wave(kvec=[0, 1, 0], pol=[-1, 0, 0], **kw_inc),
            treams.plane_wave(kvec=[0, 1, 0], pol=[0, 0, -1], **kw_inc),
            treams.plane_wave(kvec=[-1, 0, 0], pol=[0, -1, 0], **kw_inc),
            treams.plane_wave(kvec=[-1, 0, 0], pol=[0, 0, -1], **kw_inc),
        ]
        _scs_ecs = [tm.xw(inc) for inc in inc_list]
        cs_tm["scs"].append(_scs_ecs)
        cs_tm["ecs"].append(_scs_ecs)

        for inc in inc_list:
            sca = tm @ inc.expand(tm.basis)
            _ef_tm = sca.efield(r_prb_tr)
            _ef_inc = inc.efield(r_prb_tr)
            nf_tm["inc"].append(_ef_inc)
            nf_tm["sca"].append(_ef_tm)
            nf_tm["tot"].append(_ef_inc + _ef_tm)

    cs_tm["scs"] = np.array(cs_tm["scs"])[..., 0]  # keep only scs
    cs_tm["ecs"] = np.array(cs_tm["ecs"])[..., 1]  # keep only ecs
    # adapt 2D treams to torchgdm conventions
    nf_tm["inc"] = np.array(nf_tm["inc"])[..., [0, 2, 1]]
    nf_tm["sca"] = np.array(nf_tm["sca"])[..., [0, 2, 1]]
    nf_tm["tot"] = np.array(nf_tm["tot"])[..., [0, 2, 1]]
    nf_tm["inc"][..., 1] = -1 * nf_tm["inc"][..., 1]
    nf_tm["sca"][..., 1] = -1 * nf_tm["sca"][..., 1]
    nf_tm["tot"][..., 1] = -1 * nf_tm["tot"][..., 1]

    e_inc_list = [
        PlaneWave(e0p=1.0, e0s=0.0, inc_angle=0),  # k||z
        PlaneWave(e0p=0.0, e0s=1.0, inc_angle=0),  # k||z
        PlaneWave(e0p=1.0, e0s=0.0, inc_angle=torch.pi / 2),  # k||x
        PlaneWave(e0p=0.0, e0s=1.0, inc_angle=torch.pi / 2),  # k||x
    ]

    # setup a discretized and a effective dipole pair simulation
    sim_alpha = Simulation(
        structures=[struct_alpha],
        environment=env,
        illumination_fields=e_inc_list,
        wavelengths=wavelengths,
        device=device,
    )

    # run simulations and calc. cross section spectra
    if verbose:
        print("-" * 60)
        print("Testing effective model vs. T-Matrix (treams, 2D).")

    sim_alpha.run(verbose=False, progress_bar=progress_bar)

    test_results = dict()

    # calculate cross section errors
    cs_alpha = sim_alpha.get_spectra_crosssections(progress_bar=progress_bar)

    which_cs = []
    if "scs" in which:
        which_cs.append("scs")
    if "ecs" in which:
        which_cs.append("ecs")
    for k in which_cs:
        try:
            rel_diff = (cs_tm[k] - to_np(cs_alpha[k])) / (
                (cs_tm[k] + to_np(cs_alpha[k]))
            )
            test_results[k] = rel_diff

            mean_rel_error = np.mean(np.abs(rel_diff))
            peak_rel_error = np.max(np.abs(rel_diff))
            if verbose:
                print("cross sections - '{}':".format(k))
                print("    - mean rel. error: {:.3g}".format(mean_rel_error))
                print("    - peak rel. error: {:.3g}".format(peak_rel_error))
            if mean_rel_error > rtol:
                warnings.warn(
                    "'{}': Effective model mean relative error larger than tolerance ({:.3f} > {:.3f})".format(
                        k, mean_rel_error, rtol
                    )
                )

            elif peak_rel_error > rtol:
                warnings.warn(
                    "'{}': Effective model peak relative error larger than tolerance ({:.3f} > {:.3f})".format(
                        k, peak_rel_error, rtol
                    )
                )
            # print(rel_diff)
            # print(cs_tm[k])
            # print(to_np(cs_alpha[k]))
        except TypeError:
            pass

    # calculate nearfield errors several steps above structure
    nf_alpha = sim_alpha.get_spectra_nf(r_probe=r_probe, progress_bar=progress_bar)

    which_nf = []
    if "nf_tot" in which:
        which_nf.append("tot")
    if "nf_sca" in which:
        which_nf.append("sca")
    for k in which_nf:
        try:
            e_alpha = np.array([to_np(_nf.efield) for _nf in nf_alpha[k]])
            e_alpha = e_alpha.flatten()
            e_discr = to_np(nf_tm[k])
            e_discr = e_discr.flatten()
            rel_diff = (e_discr - e_alpha) / ((e_discr.max() + e_alpha.max()))
            test_results[k] = rel_diff

            mean_rel_error = np.mean(np.abs(rel_diff))
            peak_rel_error = np.max(np.abs(rel_diff))
            if verbose:
                print("nearfield - '{}' (at z={}nm):".format(k, int(to_np(z_max))))
                print("    - mean rel. error: {:.3g}".format(to_np(mean_rel_error)))
                print("    - peak rel. error: {:.3g}".format(to_np(peak_rel_error)))
            if mean_rel_error > rtol:
                warnings.warn(
                    "'{}': Effective model mean relative error larger than tolerance ({:.3f} > {:.3f})".format(
                        k, mean_rel_error, rtol
                    )
                )

            elif peak_rel_error > rtol:
                warnings.warn(
                    "'{}': Effective model peak relative error larger than tolerance ({:.3f} > {:.3f})".format(
                        k, peak_rel_error, rtol
                    )
                )
            # print('avg err per field config', np.mean(rel_diff, axis=(2)))

        except TypeError:
            pass
    if verbose:
        print("-" * 60)

    return test_results
