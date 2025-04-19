# -*- coding: utf-8 -*-
"""internla helper and tools related to effective structure models"""
import warnings

import torch

from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX, STRUCTURE_IDS
from torchgdm.tools.geometry import get_enclosing_sphere_radius
from torchgdm.tools.geometry import get_surface_meshpoints
from torchgdm.tools.geometry import sample_random_spherical
from torchgdm.tools.geometry import sample_random_circular


#########################################################
# - public functions
#########################################################
# - find positions for multiple internal dipoles
def get_gpm_positions_by_clustering(
    struct, n_gpm_dp, skeletonize=True, status_plotting=False
):
    """get GPM dipole positions by sectioning the geometry via spectral clustering

    Geometry sectioning is done using scikit-learn's `SpectralClustering`.
    Optionally, as a pre-processing step, a simple skeletonization via thinning is performed.
    See: Lamprianidis et al. JQSRT 296, 108455 (2023)

    requires `sklearn` for clustering (install via `pip install scikit-learn`).

    caution: doesn't support auto-diff.

    Args:
        struct (`struct` instance): torchgdm structure instance
        n_gpm_dp (int): Number of GPM dipole positions to create
        skeletonize (bool, optional): If True, perform a skeletonization prior clustering. Defaults to True.
        status_plotting (bool, optional): If True, plot the structure and GPM positions. Defaults to False.

    Returns:
        torch.Tensor: List of 3D coordinates
    """
    import numpy as np
    from torchgdm import to_np
    from torchgdm.tools.geometry import get_step_from_geometry

    try:
        # ignore import warnings
        with warnings.catch_warnings():
            import sklearn.cluster as skc
    except ModuleNotFoundError:
        print("Requires `sklearn`, install via `pip install scikit-learn`.")
        raise

    _struct = struct.copy()
    _struct.set_center_of_mass([0, 0, 0])

    n_dim = _struct.n_dim

    if skeletonize:
        from torchgdm.tools.geometry import get_surface_meshpoints

        skeletonize_error = False
        r_loc = to_np(_struct.get_all_positions())

        if n_dim == 2:
            NN_bulk, max_bound = 4, 1.1
        elif n_dim == 3:
            NN_bulk, max_bound = 6, 1.1

        g_s = _struct.get_all_positions()
        step = get_step_from_geometry(g_s)
        while 1:  # iteratively remove surface-shells
            p_s, n_s = get_surface_meshpoints(g_s, NN_bulk=NN_bulk, max_bound=max_bound)
            # _sim_sf, _sim_inner = tools.split_simulation(_s, p_s)
            if len(p_s) == len(g_s):
                break

            idx_remain = []
            for i, pos in enumerate(g_s):
                try:
                    # test if 'pos' exists in geometry
                    if torch.linalg.norm(p_s - pos, dim=1).min() > step / 4:
                        idx_remain.append(i)
                except RuntimeError:
                    # if error occurs, do not skeletonize
                    warnings.warn("Skeletonize failed. Using unsupported mesh?")
                    r_loc = to_np(_struct.get_all_positions())
                    skeletonize_error = True
                    break
            if skeletonize_error:
                break
            g_s = g_s[idx_remain]
            r_loc = to_np(g_s)
    else:
        r_loc = to_np(_struct.get_all_positions())
    r_skeleton = r_loc.copy()

    if len(r_skeleton) < n_gpm_dp:
        if len(_struct.get_all_positions()) > n_gpm_dp:
            warnings.warn(
                "skeletonize result has less positions than requested dipole locations"
                + f" ({len(r_skeleton)} vs. {n_gpm_dp})."
                + "Falling back to full structure. You may want to optimize this manually."
            )
            r_loc = to_np(_struct.get_all_positions())
        else:
            raise ValueError("More requested dipoles than original positions!")

    # - cluster the regions
    clustering = skc.SpectralClustering(n_clusters=n_gpm_dp).fit(r_loc)
    labels = clustering.labels_

    r_effdp = []
    for l in np.unique(labels):
        ## ignore label '-1' which is noise in certain clustring algorithms
        if l >= 0:
            r_effdp.append(np.average(r_loc[labels == l], axis=0))
    r_effdp = np.array(r_effdp)

    if status_plotting:
        import matplotlib.pyplot as plt

        if n_dim == 2:
            plt.figure(figsize=(4, 3))
            _struct.plot_contour(projection="xz")
            plt.scatter(r_skeleton[:, 0], r_skeleton[:, 2], s=3, marker="x")
            plt.scatter(r_effdp[:, 0], r_effdp[:, 2])

            plt.show()
        if n_dim == 3:
            plt.figure(figsize=(10, 3))
            plt.subplot(131)
            _struct.plot_contour(projection="xy")
            plt.scatter(r_skeleton[:, 0], r_skeleton[:, 1], s=3, marker="x")
            plt.scatter(r_effdp[:, 0], r_effdp[:, 1])

            plt.subplot(132)
            _struct.plot_contour(projection="xz")
            plt.scatter(r_skeleton[:, 0], r_skeleton[:, 2], s=3, marker="x")
            plt.scatter(r_effdp[:, 0], r_effdp[:, 2])

            plt.subplot(133)
            _struct.plot_contour(projection="yz")
            plt.scatter(r_skeleton[:, 1], r_skeleton[:, 2], s=3, marker="x")
            plt.scatter(r_effdp[:, 1], r_effdp[:, 2])

            plt.show()

    return torch.as_tensor(r_effdp, dtype=DTYPE_FLOAT, device=struct.device)


# GPM extraction
# --------------
def extract_gpm_from_fields(
    wavelength,
    efields_sca,
    hfields_sca,
    efields_inc,
    hfields_inc,
    r_probe,
    r_gpm,
    environment,
    inv_method="pinv",
    return_all_results=False,
    verbose=True,
    device=None,
    **kwargs,
):
    """Extract global polarizability matrix (GPM) from scattered fields (2D or 3D)

    Extract the GPM from the simulated scattered fields by a nanostructure in a given `environement` at `wavelength`.
    The electric and magnetic fields can be obtained by any simulation method.

    This is done in 2 steps:

        1) The effective dipole moment for each GPM dipole at `r_gpm` is obtained
           via matching of their emission and the scattered fields at `r_probe`.
        2) The GPM is matched such that it creates the dipoles moments found in (1)
           with the given incident fields.


    Additional kwargs are ignored.

    Args:
        efields_scat (torch.Tensor): scattered E-fields at probe locations. Shape (n_inc, n_probe, 3)
        hfields_scat (torch.Tensor): scattered H-fields at probe locations. Shape (n_inc, n_probe, 3)
        efields_inc (torch.Tensor): incident E-fields at GPM source locations. Shape (n_inc, n_gpm, 3)
        hfields_inc (torch.Tensor): incident H-fields at GPM source locations. Shape (n_inc, n_gpm, 3)
        r_probe (torch.Tensor): probe positions where the simulated and the GPM scattered fields are matched. shape (n_probe, 3)
        r_gpm (torch.Tensor): Locations where to place effective dipole pairs. shape (n_gpm, 3).
        environment (environment class): environement class.
        inv_method (str, optional): one of "lstsq" (least squares) or "pinv" (pseudoinverse). Method used to solve GPM problem. Defaults to "pinv".
        return_all_results (bool, optional): If True, return a dict containing intermediate results like dipole moments and fields. If False, only return a tensor containing the GPM. Defaults to False.
        verbose (bool, optional): whether to sprint progess info. Defaults to True.
        device (str, optional). Defaults to None, in which case the structure's device is used.

    Returns:
        tensor or dict: Depends on `return_all_results`.
          - if Tensor: GPM of shape (6*n_gpm, 6*n_gpm).
          - if dict: contains GPM as "GPM", dipole moments as "pm", scattered and incidente E/H fields as "f_eval" and "f0_eval".
    """
    import time
    from torchgdm.linearsystem import _reduce_dimensions
    from torchgdm.tools.misc import _check_environment
    from torchgdm.constants import DTYPE_COMPLEX, DTYPE_FLOAT

    if verbose:
        t_start = time.time()
        print("GPM optimization... ", end="")

    # --- perpare
    # - device
    if device is None:
        from torchgdm.tools.misc import get_default_device

        device = get_default_device()

    # - dipole pair locations
    r_gpm = torch.atleast_2d(r_gpm)
    r_probe = torch.atleast_2d(r_probe)
    assert r_gpm.shape[1] == 3
    assert r_probe.shape[1] == 3

    # - probe positions
    r_probe = torch.as_tensor(r_probe, dtype=DTYPE_FLOAT, device=device)
    r_probe = torch.atleast_2d(r_probe)

    # - set device
    env = _check_environment(environment, device=device)
    efields_inc = efields_inc.to(device)
    efields_sca = efields_sca.to(device)
    hfields_inc = hfields_inc.to(device)
    hfields_sca = hfields_sca.to(device)
    r_probe = r_probe.to(device)
    r_gpm = r_gpm.to(device)
    wavelength = torch.as_tensor(wavelength, dtype=DTYPE_FLOAT, device=device)

    # - test shapes
    n_illuminations = len(efields_inc)
    n_gpm = len(r_gpm)
    n_probe = len(r_probe)
    assert efields_inc.shape == hfields_inc.shape
    assert efields_sca.shape == hfields_sca.shape
    assert len(efields_inc) == n_illuminations
    assert len(efields_sca) == n_illuminations
    assert efields_inc.shape[1] == n_gpm
    assert efields_sca.shape[1] == n_probe

    # --- solve the optimization problem
    # - combine E and H fields; reshape
    f_eval = torch.cat([efields_sca, hfields_sca], dim=-1)
    f_eval = f_eval.reshape(n_illuminations, -1)  # (n_illumination, n_probe*6)
    f0_eval = torch.cat([efields_inc, hfields_inc], dim=-1)
    f0_eval = f0_eval.reshape(n_illuminations, -1)  # (n_illumination, n_gpm_dp*6)

    # - calculate Green's tensors between all r_gpm and r_probe
    if verbose:
        print("get G... ", end="")
    G_6x6 = env.get_G_6x6(
        r_probe=r_probe.unsqueeze(1), r_source=r_gpm.unsqueeze(0), wavelength=wavelength
    )  # shape (n_probe, n_gpm, 6, 6)
    G_all = _reduce_dimensions(G_6x6)  # shape (n_probe*6, n_gpm*6)
    # - inv. problem #1: probe fields + Green's tensors --> dipole moments
    if verbose:
        print("solve p/m... ", end="")
    Gi = torch.linalg.pinv(G_all)
    pm_eff = torch.matmul(Gi.unsqueeze(0), f_eval.unsqueeze(-1))[..., 0]

    # - inv. problem #2: dipole moments + illumination --> effective pola
    if verbose:
        print("solve GPM... ", end="")
    if inv_method == "lstsq":
        # leastsquares may be more robust than pinv
        GPM_result = torch.linalg.lstsq(f0_eval, pm_eff)
        GPM_best = GPM_result.solution.T
    else:
        pinv_f0 = torch.linalg.pinv(f0_eval)
        GPM_best = torch.matmul(pinv_f0, pm_eff).T

    if verbose:
        print("Done in {:.2f}s.".format(time.time() - t_start))

    if return_all_results:
        return dict(GPM=GPM_best, pm=pm_eff, f_eval=f_eval, f0_eval=f0_eval)
    else:
        return GPM_best


def extract_gpm_from_struct(
    struct,
    wavelengths,
    r_gpm,
    skeletonize=True,
    r_probe=None,
    illumination_list=None,
    environment=None,
    probe_type="particle",
    n_probe=1500,
    probe_spacing=3.0,
    n_planewave_sources=5,
    dipole_source_type="particle",
    n_dipole_sources=60,
    dipole_sources_spacing=5.0,
    verbose=True,
    progress_bar=True,
    device=None,
    residual_warning_threshold=0.1,
    batch_size=256,
):
    """Extract global polarizability matrix (GPM) of a discretized structure (2D or 3D)

    Extract the GPM for `struct` in a given `environement` at `wavelengths`.
    This is done in 3 steps:

        1) Illuminate with various sources, calculated scattered fields at
           various probe positions
        2) The effective dipole moment for each GPM dipole is obtained
           via matching of their emission and the probe fields of (1).
        3) A second inverse problem of adjusting the GPM to create the dipoles
           moments found in (2) is solved via pseudoinverse.

    By default, use a mix of plane waves and local dipole sources
    (different incidence directions, polarizations, locations, orientations).

    Args:
        struct (class:`StructDiscretized3D`): the discretized structure to extract the model for.
        wavelengths (torch.Tensor): list of wavelengths to extract the model at. in nm.
        r_gpm (int or torch.Tensor): Either int: number of positions or a torch.Tensor of shape (N, 3), giving the locations where to place effective dipole pairs.
        skeletonize (bool, optional): Has effect only if `r_gpm` is of type int. If True, perform a skeletonization prior clustering. Defaults to True.
        r_probe (torch.Tensor): probe positions where the simulated and the GPM scattered fields are matched. Overrides all other probe-related configurations. If not given, use automatic probe positions, which may not be optimal. Defaults to None (automatic).
        illumination_list (list of illuminations): List of torchgdm illumination fields to use for extraction. If not given, use automatic illumination fields, which may not be optimal. Defaults to None (automatic).
        environment (environment class): Defaults to None (vacuum, dimension used from `struct`).
        probe_type (str, optional): Where to probe, one of ["particle", "sphere", "circle"]. "particle": probe at fixed distance to particle surface. "sphere": probe on enclosing sphere surface (analoguously with "circle"). Defaults to "particle".
        n_probe (int, optional): maximum number of probe positions on enclosing sphere. Defaults to 1500.
        probe_spacing (float, optional): additional distance to particle or to enclosing sphere/circle, in units of discretization step. Defaults to 3.0.
        n_planewave_sources (int, optional): number of plane wave angles to use as illumination. Defaults to 7.
        dipole_source_type (str, optional): Where to put sources, one of ["particle", "sphere", "circle"]. "particle": probe at fixed distance to particle surface. "sphere": probe on enclosing sphere surface (analoguously with "circle"). Defaults to "particle".
        n_dipole_sources (int, optional): If given, use `n` dipole sources as illumination instead of plane waves. Defaults to None.
        dipole_sources_spacing (float, optional): if using dipole light sources, additional distance to enclosing sphere surface, in units of discretization step. Defaults to 5.0.
        verbose (bool, optional): whether to sprint progess info. Defaults to True.
        progress_bar (bool, optional): whether to show a progress bar. Defaults to True.
        device (str, optional). Defaults to None, in which case the structure's device is used.
        residual_warning_threshold (float, optional). Maximum residual L2 norm before triggering a warning. Defaults to 0.1.

    Returns:
        dict: contains all informations about the GPM model
    """
    import time
    from torchgdm.simulation import Simulation
    from torchgdm.linearsystem import _reduce_dimensions
    from torchgdm.postproc.fields import nf
    from torchgdm.tools.geometry import get_enclosing_sphere_radius
    from torchgdm.struct.eff_model_tools import _get_eff_model_probe_positions
    from torchgdm.struct.eff_model_tools import _get_eff_model_illuminations
    from torchgdm.struct.eff_model_tools import _test_residual_GPM
    from torchgdm.tools.misc import tqdm
    from torchgdm.tools.misc import _check_environment
    from torchgdm.constants import DTYPE_COMPLEX, DTYPE_FLOAT

    _struct = struct.copy()
    _struct.set_center_of_mass([0, 0, 0])
    n_dim = _struct.n_dim

    if device is None:
        device = _struct.device
    else:
        _struct.set_device(device)

    # convert single wavelength to list
    wavelengths = torch.as_tensor(wavelengths, dtype=DTYPE_FLOAT, device=device)
    wavelengths = torch.atleast_1d(wavelengths)

    # environment
    env = _check_environment(environment, N_dim=n_dim, device=device)

    if verbose:
        print(
            "--- extracting GPM model from struct ({}D, {} wavelengths) ---".format(
                n_dim, len(wavelengths)
            )
        )
        t_start = time.time()

    # GPM dipole locations
    if type(r_gpm) == int:
        from torchgdm.struct.eff_model_tools import get_gpm_positions_by_clustering

        r_gpm = get_gpm_positions_by_clustering(_struct, r_gpm, skeletonize=skeletonize)
    else:
        r_gpm = torch.as_tensor(r_gpm, dtype=DTYPE_FLOAT, device=device)
        r_gpm = torch.atleast_2d(r_gpm)
        r_gpm = r_gpm - struct.r0  # shift by original center of mass
    n_gpm_dp = len(r_gpm)

    # --- setup probe positions
    if r_probe is None:
        # - automatic probe positions
        r_probe = _get_eff_model_probe_positions(
            _struct, n_probe, probe_spacing=probe_spacing, probe_type=probe_type
        )
        if probe_type.lower() == "particle":
            r_probe, sf_vec = r_probe
    else:
        # - user defined probe positions
        r_probe = torch.as_tensor(r_probe, dtype=DTYPE_FLOAT, device=device)
        r_probe = torch.atleast_2d(r_probe)

    # --- setup illuminations
    if illumination_list is None:
        # - automatic illuminations
        einc_list = _get_eff_model_illuminations(
            struct=_struct,
            n_planewave_sources=n_planewave_sources,
            n_dipole_sources=n_dipole_sources,
            dipole_sources_spacing=dipole_sources_spacing,
            dipole_source_type=dipole_source_type,
            device=device,
        )
    else:
        # - user specifice illuminations
        einc_list = illumination_list

    # - setup simulation with replaced illuminations
    _sim = Simulation(
        structures=[_struct],
        environment=env,
        illumination_fields=einc_list,
        wavelengths=wavelengths,
        device=device,
    )

    if verbose:
        _pos_p, _pos_m = _sim._get_polarizable_positions_p_m()
        n_dp = len(_pos_p) + len(_pos_m)
        print("  - {} full structure dipoles".format(n_dp))
        print("  - {} GPM dipole pairs to replace structure".format(n_gpm_dp))
        print("  - {} illumination sources".format(len(einc_list)))
        print("  - {} probe positions".format(len(r_probe)))

        t0 = time.time()
        print("Run full simulation... ", end="")
    _sim.run(verbose=False, progress_bar=progress_bar)

    if verbose and not progress_bar:
        print("Done in {:.2f}s.".format(time.time() - t0))

    # - solve the optimization problem
    GPM_N6xN6 = torch.zeros(
        (len(wavelengths), n_gpm_dp * 6, n_gpm_dp * 6),
        dtype=DTYPE_COMPLEX,
        device=device,
    )
    if verbose:
        print("Running GPM optimization... ", end="")

    residuals = []
    for i_wl in tqdm(range(len(wavelengths)), progress_bar, title=""):
        wl = wavelengths[i_wl]

        # scattered fields from full sim.
        nf_probe = nf(
            _sim, wl, r_probe=r_probe, progress_bar=False, batch_size=batch_size
        )

        # illuminations at r_gpm
        e0 = [e_inc.get_field(r_gpm, wl, env).efield[0] for e_inc in einc_list]
        h0 = [e_inc.get_field(r_gpm, wl, env).hfield[0] for e_inc in einc_list]

        # solve optimization
        GPM_dict = extract_gpm_from_fields(
            wavelength=wl,
            efields_sca=nf_probe["sca"].efield,
            hfields_sca=nf_probe["sca"].hfield,
            efields_inc=torch.stack(e0, dim=0),
            hfields_inc=torch.stack(h0, dim=0),
            r_probe=r_probe,
            r_gpm=r_gpm,
            environment=env,
            verbose=False,
            return_all_results=True,
            device=device,
        )
        # optimum alphas to obtain dipole moments for each illumination
        GPM_N6xN6[i_wl] = GPM_dict["GPM"]

        _res = _test_residual_GPM(
            _struct,
            wl,
            env,
            GPM_dict["GPM"],
            GPM_dict["f0_eval"],
            GPM_dict["pm"],
            residual_warning_threshold=residual_warning_threshold,
        )
        residuals.append(_res)

    enclosing_radius = get_enclosing_sphere_radius(_struct.get_all_positions())
    dict_gpm = dict(
        r_gpm=r_gpm,
        GPM_N6xN6=GPM_N6xN6,
        wavelengths=wavelengths,
        # additional metadata
        full_geometry=_struct.get_all_positions(),
        n_gpm_dp=n_gpm_dp,
        residuals_per_dipole=residuals,
        r0=_struct.get_center_of_mass(),
        enclosing_radius=enclosing_radius,
        k0_spectrum=2 * torch.pi / wavelengths,
        extraction_r_probe=r_probe,
        extraction_illuminations=einc_list,
        environment=env,
    )
    if probe_type.lower() == "particle":
        dict_gpm["surface_vec_normal"] = sf_vec

    if verbose:
        print("Extraction done in {:.2f}s.".format(time.time() - t_start))
        print("---------------------------------------------")

    return dict_gpm


def extract_gpm_from_tmatrix(
    tmatrix,
    r_enclosing,
    r_gpm,
    wavelengths=None,
    r_probe=None,
    environment=None,
    n_probe=None,
    probe_spacing_nm=30.0,
    n_src_pw_angles=None,
    n_src_local=None,
    source_spacing_nm=50.0,
    verbose=True,
    progress_bar=True,
    device=None,
    n_proc=None,
    **kwargs,
):
    """Extract global polarizability matrix (GPM) of a T-matrix (treams)

    Caution: Assuming the T-matrix with `r_enclosing` to be centered around (0,0,0)

    Extract the GPM for `struct` in a given `environement` at `wavelengths`.
    This is done in 3 steps:

        1) Illuminate the t-matrix with various sources (plane and spherical waves),
           calculated scattered fields at various probe positions just outside
           the circubscribing sphere
        2) The effective dipole moment for each GPM dipole is obtained
           via matching of their emission and the probe fields of (1).
        3) A second inverse problem of adjusting the GPM to create the dipoles
           moments found in (2) is solved via pseudoinverse.

    If an integer is given for `r_gpm`, GPM positions inside the T-matrix
    circumscribing sphere are generated via random quasi Monte Carlo sampling.

    Additional kwargs are passed to the T-Matrix conversion.


    requires `tream` (T-Matrix) and `joblib` (multiprocessing).

    Args:
        tmatrix (treams TMatrix or list): treams T-matrix or list of T-matrices.
        r_enclosing (float): radius of T-matrix enclosing sphere in nm (assume center at origin).
        r_gpm (int or torch.Tensor): Either int: number of positions or a torch.Tensor of shape (N, 3), giving the locations where to place effective dipole pairs.
        wavelengths (float or torch.Tensor, optional): wavelengths of each T-matrix. Defaults to None, in which case use T-Matrix wavenumbers.
        r_probe (torch.Tensor): probe positions where the simulated and the GPM scattered fields are matched. Overrides all other probe-related configurations. If not given, use automatic probe positions. Defaults to None (automatic).
        environment (torchgdm env, optional): Torchgdm environment if not give, will use first T-matrix's environment permittivity. Defaults to None.
        n_probe (int, optional): Number of probe locations. Generate points of equal angular spacing on a sphere around the origin. Defaults to None, then: 3D=300, 2D=100.
        probe_spacing_nm (float, optional): Distance of probe locations to enclosing sphere (in nm). Defaults to 30.0.
        n_src_pw_angles (int, optional): Number of plave wave incident angles for illumination during extraction. Defaults to None, then: 3D=4, 2D=4.
        n_src_local (int, optional): Number of local illumination sources (spherical or cylindrical waves) for extraction. Defaults to None, then: 3D=30, 2D=20.
        source_spacing_nm (float, optional): Distance of spherical wave sources to enclosing sphere (in nm). Defaults to 50.0.
        progress_bar (bool, optional): Progress bar for several tmatrices. Defaults to True.
        verbose (bool, optional): whether to print progess info. Defaults to True.
        device (str, optional). Device to transfer output to. Internally, everything is done only on CPU. Defaults to None, in which case the torchgdm default device is used.
        n_proc (int, optional): Number of parallel `joblib` processes. Defaults to None (Nr of physical cpu cores).

    Returns:
        dict: contains all informations about the GPM model
    """
    import time

    try:
        from joblib import Parallel, delayed
        from joblib import cpu_count
        import joblib
        import contextlib

        if n_proc is None:
            n_proc = cpu_count(only_physical_cores=True)
    except ModuleNotFoundError:
        print("Requires `joblib`, install via `pip install joblib`.")
        raise

    # allow tqdm progressbar to monitor joblib multiprocessing
    # from : https://stackoverflow.com/questions/24983493/tracking-progress-of-joblib-parallel-execution/58936697#58936697
    @contextlib.contextmanager
    def tqdm_joblib(tqdm_object):
        """Context manager to patch joblib to report into tqdm progress bar given as argument"""

        def tqdm_print_progress(self):
            if self.n_completed_tasks > tqdm_object.n:
                n_completed = self.n_completed_tasks - tqdm_object.n
                tqdm_object.update(n=n_completed)

        original_print_progress = joblib.parallel.Parallel.print_progress
        joblib.parallel.Parallel.print_progress = tqdm_print_progress

        try:
            yield tqdm_object
        finally:
            joblib.parallel.Parallel.print_progress = original_print_progress
            tqdm_object.close()

    try:
        # ignore import warnings
        with warnings.catch_warnings():
            import treams
    except ModuleNotFoundError:
        print("Requires `treams`, install via `pip install treams`.")
        raise

    import numpy as np
    from torchgdm.tools.misc import to_np
    from torchgdm.tools.misc import tqdm
    from torchgdm.tools.misc import get_default_device
    from torchgdm.tools.misc import _check_environment
    from torchgdm.tools.geometry import coordinate_map_1d_circular
    from torchgdm.tools.geometry import coordinate_map_2d_spherical
    from torchgdm.tools.tmatrix import convert_tmatrix2D_to_GPM
    from torchgdm.tools.tmatrix import convert_tmatrix3D_to_GPM

    if device is None:
        device = get_default_device()
    else:
        device = device

    _device_int = "cpu"  # treams: internally use only CPU

    # single t-matrix: wrap in a list
    if hasattr(tmatrix, "__iter__"):
        tm_list = tmatrix
    else:
        tm_list = [tmatrix]
    if len(tmatrix) == 1:
        progress_bar = False

    for _tm in tm_list:
        assert type(_tm) == type(tm_list[0]), "all T-Matrices must be of same type."

    # get dim from treams t-matrix. If not given, set autoconfig
    if type(tm_list[0]) == treams.TMatrix:
        n_dim = 3
        tm_to_gpm_func = convert_tmatrix3D_to_GPM
        if n_probe is None:
            n_probe = 300
        if n_src_pw_angles is None:
            n_src_pw_angles = 4
        if n_src_local is None:
            n_src_local = 30
    elif type(tm_list[0]) == treams.TMatrixC:
        n_dim = 2
        tm_to_gpm_func = convert_tmatrix2D_to_GPM
        if n_probe is None:
            n_probe = 100
        if n_src_pw_angles is None:
            n_src_pw_angles = 4
        if n_src_local is None:
            n_src_local = 20
    else:
        raise ValueError(
            f"Only 2D and 3D treams T-Matrices supported. got {type(tm_list[0])}"
        )

    # get wavelength from T-Matrix; to tensor
    if wavelengths is None:
        wavelengths = [2 * np.pi / _tm.k0 for _tm in tm_list]
    wavelengths = torch.as_tensor(wavelengths, dtype=DTYPE_FLOAT, device=device)
    wavelengths = torch.atleast_1d(wavelengths)

    # environment
    if environment is None:  # use first T-Matrix
        environment = complex(tm_list[0].material.epsilon)
    env = _check_environment(environment, N_dim=n_dim, device=_device_int)

    # consistency checks
    assert len(tm_list) == len(wavelengths), "require one tmatrix for each wavelength"
    assert len(torch.unique(wavelengths)) == len(
        wavelengths
    ), "usage restricted to strictly spectral data (no identical wavelengths allowed)"
    for _tm, _wl in zip(tm_list, wavelengths):
        eps_env_scalar = env.get_environment_permittivity_scalar(_wl, [[0, 0, 0]])
        assert _tm.material.epsilon == to_np(
            eps_env_scalar
        ), "same environment required"
        assert np.allclose(
            _tm.k0, 2 * np.pi / float(_wl)
        ), "tmatrix wavenumbers must match wavelengths"

    if verbose:
        print("--- extracting GPM model from t-matrix ({}D) ---".format(n_dim))
        t_start = time.time()

    # --- setup GPM dipole locations
    if type(r_gpm) == int:
        from scipy.stats import qmc

        sampler = qmc.Halton(d=n_dim, scramble=False)
        r_gpm = sampler.random(n=r_gpm)
        r_gpm /= np.max(np.linalg.norm(r_gpm, axis=1)) + 0.0001
        r_gpm -= np.mean(r_gpm, axis=0)
        r_gpm *= 0.65 * (r_enclosing * 2)  # not too close to sphere surface
        if n_dim == 2:
            r_gpm = np.insert(r_gpm, 1, values=0, axis=1)  # 2d torchgdm y-axis = 0
        r_gpm = torch.as_tensor(r_gpm, dtype=DTYPE_FLOAT, device=_device_int)

    else:
        r_gpm = torch.as_tensor(r_gpm, dtype=DTYPE_FLOAT, device=device)
        r_gpm = torch.atleast_2d(r_gpm)
    n_gpm = len(r_gpm)

    # --- setup probe positions
    if r_probe is None:
        # - automatic probe positions
        if n_dim == 3:
            n_teta = int((n_probe / 2) ** 0.5)
            n_phi = n_probe // n_teta
            r_probe = coordinate_map_2d_spherical(
                r=r_enclosing + probe_spacing_nm,
                n_teta=n_teta,
                n_phi=n_phi,
                device=_device_int,
            )["r_probe"]
        elif n_dim == 2:
            n_phi = n_probe
            r_probe = coordinate_map_1d_circular(
                r=r_enclosing + probe_spacing_nm,
                n_phi=n_phi,
                device=_device_int,
            )["r_probe"]
            # caution, 2D: Y axis is infinite (treams: Z infinite)

    else:
        # - user defined probe positions
        r_probe = torch.as_tensor(r_probe, dtype=DTYPE_FLOAT, device=device)
        r_probe = torch.atleast_2d(r_probe)

    if n_dim == 2:
        assert torch.all(r_probe[:, 1] == 0), "2D: all r_probe y must be 0!"
        assert torch.all(r_gpm[:, 1] == 0), "2D: all r_gpm y must be 0!"

    if verbose:
        _Npw = 6 * n_src_pw_angles if n_dim == 3 else 2 * n_src_pw_angles
        print("  - {} T-matrices (and wavelengths)".format(len(wavelengths)))
        print("  - {} GPM dipole pairs to approximate each T-matrix".format(n_gpm))
        print("  - {} illumination sources".format(_Npw + n_src_local))
        print("  - {} probe positions".format(len(r_probe)))

    # --- extract the GPM for each t-matrix - parallelized with `joblib`
    def wrapper_to_gpm(tm, n_proc=1):
        GPM_dict = tm_to_gpm_func(
            tmatrix=tm,
            r_gpm=r_gpm,
            r_probe=r_probe,
            n_src_pw_angles=n_src_pw_angles,
            n_src_local=n_src_local,
            radius_src_local=r_enclosing + source_spacing_nm,
            n_proc=n_proc,
            **kwargs,
        )
        return GPM_dict["GPM"]

    # progress bar
    prog_bar = tqdm(
        tm_list,
        title="treams GPM extraction",
        progress_bar=progress_bar,
        total=len(tm_list),
    )
    if type(prog_bar) == list:  # no progress bar: parallelize inc.fields
        results = [wrapper_to_gpm(tm, n_proc=n_proc) for tm in tm_list]
    else:
        if len(tm_list) < n_proc:
            # parallelize illuminations
            results = [wrapper_to_gpm(tm, n_proc=n_proc) for tm in prog_bar]
        else:
            # parallelize T-Matrices (faster for many tmatrices)
            with tqdm_joblib(prog_bar) as prg_bar:
                results = Parallel(n_jobs=n_proc)(
                    delayed(wrapper_to_gpm)(tm) for tm in tm_list
                )

    GPM_N6xN6 = torch.stack(results, dim=0).to(dtype=DTYPE_COMPLEX, device=_device_int)

    # --- wrap up GPM and metainfo into dict
    # dummy sphere structure as representative mesh
    _step_dummy_sphere = r_enclosing / 7  # dummy for extraciton only
    if n_dim == 2:
        from torchgdm.struct.struct2d import circle
        from torchgdm.struct.struct2d import discretizer_square

        _geo_dummy = discretizer_square(
            *circle(r=r_enclosing / _step_dummy_sphere),
            step=_step_dummy_sphere,
            z_offset=0,
        )
    elif n_dim == 3:
        from torchgdm.struct.struct3d import sphere
        from torchgdm.struct.struct3d import discretizer_cubic

        _geo_dummy = discretizer_cubic(
            *sphere(r=r_enclosing / _step_dummy_sphere),
            step=_step_dummy_sphere,
            z_offset=0,
        )

    # set device to torchgdm working device
    GPM_N6xN6 = GPM_N6xN6.to(dtype=DTYPE_COMPLEX, device=device)
    wavelengths = torch.as_tensor(wavelengths, dtype=DTYPE_FLOAT, device=device)
    r_probe = torch.as_tensor(r_probe, dtype=DTYPE_FLOAT, device=device)
    r_gpm = torch.as_tensor(r_gpm, dtype=DTYPE_FLOAT, device=device)
    _geo_dummy = torch.as_tensor(_geo_dummy, dtype=DTYPE_FLOAT, device=device)

    env.set_device(device)

    dict_gpm = dict(
        r_gpm=r_gpm,
        GPM_N6xN6=GPM_N6xN6,
        wavelengths=wavelengths,
        # additional metadata
        full_geometry=_geo_dummy,
        n_gpm_dp=n_gpm,
        r0=torch.as_tensor([0, 0, 0], dtype=DTYPE_FLOAT, device=device),
        enclosing_radius=r_enclosing,
        k0_spectrum=2 * torch.pi / wavelengths,
        environment=env,
        extraction_r_probe=r_probe,
        t_matrices=tm_list,
    )

    if verbose:
        print("Extraction done in {:.2f}s.".format(time.time() - t_start))
        print("---------------------------------------------")

    return dict_gpm


# effective dipole polarizability extraction
# ------------------------------------------
def extract_eff_pola_via_exact_mp_3d(
    struct,
    wavelengths,
    environment=None,
    n_dipoles=None,
    distance_dipoles=5000,
    verbose=True,
    only_pE_mH=True,
    progress_bar=True,
    device=None,
    batch_size=16,
    residual_warning_threshold=0.25,
    long_wavelength_approx=False,
    **kwargs,
):
    """Extract 3D effective dipole-pair polarizability model from volume discretization

    Via exact multipole decomposition, wxtract the polarizability for the
    structure `struct` in a given `environement` at the specified `wavelengths`

    solve inverse problem of adjusting polarizability for different illuminations
    via pseudoinverse

    By default, use 14 plane waves (different incidence directions and polarizations).
    alternative: illumination with `n_dipoles` point-dipole sources if `n_dipoles` is an integer > 0.


    Args:
        struct (class:`StructDiscretized3D`): the discretized structure to extract the model for.
        wavelengths (torch.Tensor): list of wavelengths to extract the model at. in nm.
        environment (environment class): 3D environement class. Defaults to None (vacuum).
        n_dipoles (int, optional): If given, use `n` dipole sources as illumination instead of plane waves. Defaults to None.
        distance_dipoles (int, optional): if using dipoles, specify their distance to the center of gravity. Defaults to 5000.
        verbose (bool, optional): whether to sprint progess info. Defaults to True.
        only_pE_mH (bool, optional): whether to extract only a p/m model (True) or a full (6x6) polarizability (False). Defaults to True.
        progress_bar (bool, optional): whether to show a progress bar. Defaults to True.
        device (str, optional). Defaults to None, in which case the structure's device is used.
        residual_warning_threshold (float, optional). Maximum residual L2 norm before triggering a warning. Defaults to 0.25.
        long_wavelength_approx (bool, optional): If True, use long wavelength approximation for dupole extraction. Defaults to False.

    Returns:
        dict: contains all informations about the effective dipole polarizability model
    """
    from torchgdm.env.freespace_3d.inc_fields import ElectricDipole, PlaneWave
    from torchgdm.simulation import Simulation
    from torchgdm.postproc.multipole import decomposition_exact
    from torchgdm.tools.geometry import get_enclosing_sphere_radius
    from torchgdm.struct.eff_model_tools import _test_residual_effective_polarizability
    from torchgdm.tools.misc import tqdm
    from torchgdm.tools.misc import _check_environment

    _struct = struct.copy()

    if device is None:
        device = _struct.device
    else:
        struct.set_device(device)

    # convert single wavelength to list
    wavelengths = torch.as_tensor(wavelengths, dtype=DTYPE_FLOAT, device=device)
    wavelengths = torch.atleast_1d(wavelengths)

    # environment
    env = _check_environment(environment, N_dim=3, device=device)

    if verbose:
        import time

        print(
            "--- extracting eff. dipole pair model (3D, {} wavelengths) ---".format(
                len(wavelengths)
            )
        )
        t_start = time.time()

    # use first order multipole moments (propto local field)
    enclosing_radius = get_enclosing_sphere_radius(_struct.get_all_positions())
    r_sphere = enclosing_radius + distance_dipoles
    r0 = struct.get_center_of_mass()

    # setup perpendicular plane waves illuminations
    if n_dipoles is None:
        pw_conf_list = [
            [0.0, 1.0, 0, "xz"],  # E-x, H-y, k-z
            [1.0, 0.0, 0, "xz"],  # E-y, H-x, k-z
            #
            [1.0, 0.0, torch.pi / 2.0, "xz"],  # E-x, H-z, k-y
            [0.0, 1.0, torch.pi / 2.0, "xz"],  # E-z, H-x, k-y
            #
            [1.0, 0.0, torch.pi / 2.0, "yz"],  # E-y, H-z, k-x
            [0.0, 1.0, torch.pi / 2.0, "yz"],  # E-z, H-y, k-x
            #
            [1.0, 0.0, -torch.pi / 2.0, "xz"],  # E-x, H-z, -k-y
            [0.0, 1.0, -torch.pi / 2.0, "xz"],  # E-z, H-x, -k-y
            #
            [1.0, 0.0, -torch.pi / 2.0, "yz"],  # E-y, H-z, -k-x
            [0.0, 1.0, -torch.pi / 2.0, "yz"],  # E-z, H-y, -k-x
            #
            [1.0, 0.0, torch.pi / 4.0, "xz"],  # oblique
            [0.0, 1.0, torch.pi / 4.0, "yz"],  # oblique
            #
            [0.0, 1.0, -torch.pi / 4.0, "xz"],  # oblique, opposite
            [1.0, 0.0, -torch.pi / 4.0, "yz"],  # oblique, opposite
        ]
        e_inc_list = [
            PlaneWave(e0s=a, e0p=b, inc_angle=c, inc_plane=d, device=device)
            for [a, b, c, d] in pw_conf_list
        ]
    # optional: multiple dipole illuminations
    else:
        if n_dipoles <= 0 or type(n_dipoles) != int:
            raise ValueError(
                "dipole illumination mode: `n_dipoles` needs to be a positive integer."
            )

        # setup dipoles of random position and random orientation
        rnd_pos = sample_random_spherical(n_dipoles) * r_sphere
        e_inc_list = [
            ElectricDipole(
                r_source=r_dp,
                p_source=torch.rand(3, device=device) * r_sphere,
                device=device,
            )
            for r_dp in rnd_pos
        ]

    # replace illumination
    _sim = Simulation(
        structures=[_struct],
        environment=env,
        illumination_fields=e_inc_list,
        wavelengths=wavelengths,
        device=device,
    )

    if verbose:
        t0 = time.time()
        _pos_p, _pos_m = _sim._get_polarizable_positions_p_m()
        n_dp = len(_pos_p) + len(_pos_m)
        n_wl = len(wavelengths)
        print("Running simulation ({} dipoles, {} wls)... ".format(n_dp, n_wl), end="")
    _sim.run(verbose=False, progress_bar=progress_bar, batch_size=batch_size)

    if verbose and not progress_bar:
        print("Done in {:.2f}s.".format(time.time() - t0))

    # solve the optimization problem
    alpha_6x6 = torch.zeros(
        (len(wavelengths), 6, 6), dtype=DTYPE_COMPLEX, device=device
    )
    if verbose:
        t0 = time.time()
        print("Running p/m optimization... ", end="")

    for i_wl in tqdm(range(len(wavelengths)), progress_bar, title=""):
        wl = wavelengths[i_wl]

        # multipole expansion for all illuminations
        mp_dict = decomposition_exact(
            _sim,
            wl,
            long_wavelength_approx=long_wavelength_approx,
        )
        p_eval = mp_dict["ed_1"]
        m_eval = mp_dict["md"]

        # residual quadrupoles
        _EQ_res = torch.linalg.norm(mp_dict["eq_tot"], dim=(1, 2)).mean()
        _MQ_res = torch.linalg.norm(mp_dict["mq"], dim=(1, 2)).mean()

        # illuminating fields at expansion location
        e0_eval = torch.zeros((len(e_inc_list), 3), dtype=DTYPE_COMPLEX, device=device)
        h0_eval = torch.zeros((len(e_inc_list), 3), dtype=DTYPE_COMPLEX, device=device)
        for i_field, e_inc in enumerate(e_inc_list):
            inc_f = e_inc.get_field(r0.unsqueeze(0), wl, env)
            e0_eval[i_field] = inc_f.get_efield()
            h0_eval[i_field] = inc_f.get_hfield()

        # --- full 6x6 polarizability
        if not only_pE_mH:
            # pseudo-inverse of all illuminations
            f0_eval = torch.cat([e0_eval, h0_eval], dim=1)
            pinv_f0 = torch.linalg.pinv(f0_eval)

            # optimum alphas to obtain dipole moments for each illumination
            pm_eval = torch.cat([p_eval, m_eval], dim=1)
            alpha_6x6_inv = torch.matmul(pinv_f0, pm_eval)
            alpha_6x6[i_wl] = alpha_6x6_inv

            # test residuals
            _test_residual_effective_polarizability(
                _struct,
                wl,
                env,
                alpha_6x6_inv,
                f0_eval,
                pm_eval,
                text_which_dp="6x6 dipole",
                residual_warning_threshold=residual_warning_threshold,
                residual_EQ=_EQ_res,
                residual_MQ=_MQ_res,
            )

        # --- only pE and mH
        if only_pE_mH:
            # pseudo-inverse of all illuminations
            pinv_e0 = torch.linalg.pinv(e0_eval)
            pinv_h0 = torch.linalg.pinv(h0_eval)

            # optimum alphas to obtain dipole moments for each illumination
            alpha_pinv = torch.matmul(pinv_e0, p_eval)
            alpha_minv = torch.matmul(pinv_h0, m_eval)

            alpha_6x6[i_wl, :3, :3] = alpha_pinv
            alpha_6x6[i_wl, 3:, 3:] = alpha_minv

            # test residuals
            _test_residual_effective_polarizability(
                _struct,
                wl,
                env,
                alpha_pinv,
                e0_eval,
                p_eval,
                text_which_dp="electric dipole",
                residual_warning_threshold=residual_warning_threshold,
                residual_EQ=_EQ_res,
                residual_MQ=_MQ_res,
            )
            _test_residual_effective_polarizability(
                _struct,
                wl,
                env,
                alpha_minv,
                h0_eval,
                m_eval,
                text_which_dp="magnetic dipole",
                residual_warning_threshold=residual_warning_threshold,
                residual_EQ=_EQ_res,
                residual_MQ=_MQ_res,
            )

    if verbose:
        print("Done in {:.2f}s.".format(time.time() - t_start))
        print("---------------------------------------------")

    dict_pola_pseudo = dict(
        r0=r0,
        r0_MD=r0,
        r0_ED=r0,
        full_geometry=_struct.get_all_positions(),
        alpha_6x6=alpha_6x6,
        wavelengths=wavelengths,
        enclosing_radius=enclosing_radius,
        k0_spectrum=2 * torch.pi / wavelengths,
        environment=env,
    )
    return dict_pola_pseudo


# wrapper to GPM extraction with a single dipole pair
def extract_eff_pola_2d(
    struct,
    wavelengths,
    environment=None,
    n_probe=150,
    distance_probe=3.0,
    n_dipoles=None,
    distance_dipoles=5000,
    verbose=True,
    only_pE_mH=True,
    progress_bar=True,
    device=None,
    residual_warning_threshold=0.25,
    batch_size=256,
):
    if only_pE_mH:
        warnings.warn(
            "`only_pE_mH` has been removed from 2D model extraction. "
            + "This option will have no effect."
        )

    step_max = struct.get_source_validity_radius().max()
    r0 = struct.get_center_of_mass()

    if n_dipoles is None:
        n_dipoles = 0

    # extract single dipole-pair GPM
    gpm_dict = extract_gpm_from_struct(
        struct,
        wavelengths,
        r_gpm=r0,
        r_probe=None,
        environment=environment,
        probe_type="circle",
        n_probe=n_probe,
        probe_spacing=distance_probe,
        n_planewave_sources=7,
        dipole_source_type="circle",
        n_dipole_sources=n_dipoles,
        dipole_sources_spacing=distance_dipoles / step_max,
        verbose=verbose,
        progress_bar=progress_bar,
        device=device,
        residual_warning_threshold=residual_warning_threshold,
        batch_size=batch_size,
    )

    # wrap results
    dict_pola_pseudo = dict(
        r0=r0,
        r0_MD=r0,
        r0_ED=r0,
        full_geometry=struct.get_all_positions(),
        alpha_6x6=gpm_dict["GPM_N6xN6"],
        wavelengths=wavelengths,
        enclosing_radius=gpm_dict["enclosing_radius"],
        k0_spectrum=2 * torch.pi / wavelengths,
        environment=gpm_dict["environment"],
    )
    return dict_pola_pseudo


#########################################################
# - private functions
#########################################################
# --- effective model extraction helper
def _get_eff_model_probe_positions(
    struct, n_probe, probe_spacing=3.0, probe_type: str = "sphere"
):
    n_dim = struct.n_dim

    device = struct.device
    step_max = torch.max(struct.step)
    spacing_nm = probe_spacing * step_max

    enclosing_radius = get_enclosing_sphere_radius(struct.get_all_positions())
    probe_radius = enclosing_radius + spacing_nm

    if probe_type.lower() == "particle":
        # - around particle surface
        from torchgdm.tools.geometry import get_positions_outside_struct

        r_probe, sf_vec = get_positions_outside_struct(struct, probe_spacing)

        # more pos. available than requested: keep random selection
        if len(r_probe) > n_probe:
            perm = torch.randperm(r_probe.size(0))
            idx = perm[:n_probe]
            r_probe = r_probe[idx]
            sf_vec = sf_vec[idx]
        return r_probe, sf_vec

    elif probe_type.lower() == "sphere":
        # - on circumscribing sphere
        if n_dim == 2:
            raise ValueError("Sphere positions for sources only possible for 3D.")
        r_probe = sample_random_spherical(n_probe, device=device) * probe_radius
        return r_probe

    elif probe_type.lower() == "circle":
        # - on circumscribing circle
        r_probe = sample_random_circular(n_probe, device=device) * probe_radius
        return r_probe


def _get_eff_model_illuminations(
    struct,
    n_planewave_sources,
    n_dipole_sources,
    dipole_source_type="particle",
    dipole_sources_spacing=3.0,  # units if step
    device=None,
):
    n_dim = struct.n_dim

    einc_list = []
    if n_planewave_sources > 0:
        # plane waves (multiple incident angles, s / p polarization)
        if n_dim == 2:
            from torchgdm.env.freespace_2d.inc_fields import PlaneWave

            inc_planes = ["xz"]
        elif n_dim == 3:
            from torchgdm.env.freespace_3d.inc_fields import PlaneWave

            inc_planes = ["xz", "yz"]
        else:
            raise ValueError("Only 2D and 3D structures supported so far.")

        pw_conf_list = []
        for angle in torch.linspace(
            0, 2 * (1 - 1 / n_planewave_sources) * torch.pi, n_planewave_sources
        ):
            for plane in inc_planes:
                pw_conf_list.append([1.0, 0.0, angle, plane])
                pw_conf_list.append([0.0, 1.0, angle, plane])

        einc_list += [
            PlaneWave(e0s=a, e0p=b, inc_angle=c, inc_plane=d, device=device)
            for [a, b, c, d] in pw_conf_list
        ]
    if n_dipole_sources > 0:
        # dipole light sources (random positions, multiple orientations, ED and MD)
        step_max = torch.max(struct.step)
        spacing_nm = dipole_sources_spacing * step_max

        enclosing_radius = get_enclosing_sphere_radius(struct.get_all_positions())
        illumination_radius = enclosing_radius + spacing_nm
        # multiple dipole illuminations
        # dipole locations: a few of the probe locations (randomly chosen)
        from torchgdm.env import IlluminationDipole

        if dipole_source_type.lower() == "particle":
            # - sources around particle surface
            from torchgdm.tools.geometry import get_positions_outside_struct

            r_sources, sf_vec = get_positions_outside_struct(
                struct, dipole_sources_spacing
            )
            # more pos. available than requested: keep random selection
            if len(r_sources) > n_dipole_sources:
                perm = torch.randperm(r_sources.size(0))
                idx = perm[:n_dipole_sources]
                r_sources = r_sources[idx]
        elif dipole_source_type.lower() == "sphere":
            # - sources on circumscribing sphere
            if n_dim == 2:
                raise ValueError("Sphere positions for sources only possible for 3D.")
            r_sources = (
                sample_random_spherical(n_dipole_sources, device=device)
                * illumination_radius
            )
        elif dipole_source_type.lower() == "circle":
            # - sources on circumscribing circle
            r_sources = (
                sample_random_circular(n_dipole_sources, device=device)
                * illumination_radius
            )
        else:
            raise ValueError(
                "Unknown type of source illumination. "
                + "Must be one of ['particle', 'sphere', 'circle']"
            )

        if n_dim == 2:
            Adp = 3e2 * (illumination_radius) ** (1 / 2.0)
        elif n_dim == 3:
            Adp = 1e5 * (illumination_radius) ** (1 / 2.0)
        else:
            raise ValueError("Only 2D and 3D structures supported so far.")

        vec_orients = Adp * torch.diagflat(
            torch.ones(6, dtype=DTYPE_COMPLEX, device=device)
        )
        for r_dp in r_sources:
            vec_dp = vec_orients[torch.randint(6, (1,))[0]]
            einc_list += [
                IlluminationDipole(
                    r_source=r_dp, dp_source=vec_dp, n_dim=n_dim, device=device
                )
            ]

    if len(einc_list) == 0:
        raise ValueError("At least one type of illuminations must be specified.")

    return einc_list


# --- Accuracy tests
def _test_residual_effective_polarizability(
    _struct,
    wavelength,
    environment,
    alpha_eff,
    f0,
    dp_moments,
    text_which_dp="",
    residual_warning_threshold=0.25,
    residual_EQ=None,
    residual_MQ=None,
):
    # --- test - calculate mean residuals for accuracy estimation
    epsilon_dpm = torch.abs(
        _struct.get_polarizability_6x6(wavelength=wavelength, environment=environment)
    ).max()  # add a single mesh-cell polarizability as epsilon to relative error test

    res_p = torch.abs(dp_moments - torch.matmul(alpha_eff, f0.T).T)
    norm_p = torch.linalg.norm(dp_moments, dim=-1).unsqueeze(1) + epsilon_dpm

    if torch.max(res_p / norm_p) > residual_warning_threshold:
        print(
            "Warning: wl={}nm - eff. {} pola. peak residual is exceeing the threshold! ({:.4f} > {:.2f})".format(
                wavelength,
                text_which_dp,
                torch.max(res_p / norm_p),
                residual_warning_threshold,
            )
        )
    if residual_EQ is not None:
        if (residual_EQ / 1.25e9) > residual_warning_threshold:
            print(
                "Warning: wl={}nm - residual electric quadrupole is exceeing the threshold! ({:.4f} > {:.2f} [1E9])".format(
                    wavelength, residual_EQ / 1e9, residual_warning_threshold * 1.25
                )
            )
    if residual_MQ is not None:
        if (residual_MQ / 1.25e9) > residual_warning_threshold:
            print(
                "Warning: wl={}nm - residual magnetic quadrupole is exceeing the threshold! ({:.4f} > {:.2f} [1E9])".format(
                    wavelength, residual_MQ / 1e9, residual_warning_threshold * 1.25
                )
            )


def _test_residual_GPM(
    _struct,
    wavelength,
    environment,
    gpm,
    f0,
    dp_moments,
    residual_warning_threshold=0.25,
):

    # --- test - calculate mean residuals for accuracy estimation
    epsilon_dpm = torch.abs(
        _struct.get_polarizability_6x6(wavelength=wavelength, environment=environment)
    ).max()  # add a single mesh-cell polarizability as epsilon to relative error test

    # MSE residual per dipole pair
    N_dp_pairs = len(gpm) / 6
    res = torch.abs(dp_moments - torch.matmul(gpm, f0.T).T) / N_dp_pairs
    norm = torch.linalg.norm(dp_moments, dim=-1).unsqueeze(1) + epsilon_dpm
    test_results = res / norm

    if torch.max(test_results) > residual_warning_threshold:
        print(
            "Warning: wl={}nm - ".format(wavelength)
            + "GPM peak residual is exceeing the threshold "
            + "({:.3g} > {:.2g})!".format(
                torch.max(res / norm), residual_warning_threshold
            )
            + " The model may still be good enough depending on the use-case."
            + " If not, consider using a larger number of effective dipoles "
            + " or a larger number of illuminations / probes."
        )

    return test_results


def _test_effective_model_accuracy(
    struct_alpha,
    struct_full,
    which=["scs", "ecs", "nf_tot"],
    environment=None,
    rtol=0.10,
    verbose=True,
    progress_bar=False,
    device=None,
):
    """test effective polarizability model in a scattering simulation

    Print some information about model accuracy

    Args:
        struct_alpha (torchgdm.struct3d.StructEffPola3D): effective polarizability structure
        struct_full (StructDiscretized3D): associated full discretization structure as reference
        which_test (list of str, optional): Which observables to test. Can contain any of ["scs", "ecs", "nf_tot"]. Defaults to ["scs", "ecs", "nf_tot"].
        environment (3D env. class, optional): Simulation environment. If None, use environment from effective dipole model structure. Defaults to None.
        rtol (float, optional): relative error threshold for raising warnings. Defaults to 0.10.
        verbose (bool, optional): Print detailed info. Defaults to True.
        progress_bar (bool, optional): Show progress bars. Defaults to False.
        device (str, optional): If None, use structure's device. Defaults to None.

    """
    from torchgdm.tools.batch import calc_spectrum
    from torchgdm.postproc import crosssect
    from torchgdm.simulation import Simulation
    from torchgdm.tools.misc import to_np

    if environment is None:
        if struct_alpha.environment is None:
            raise ValueError(
                "Structure does not contain environement definition, "
                + "and no environemnt has been specified. Please provide the environment."
            )
        environment = struct_alpha.environment

    if device is None:
        device = struct_alpha.device

    wavelengths = struct_alpha.wavelengths_data

    n_dim = struct_full.n_dim
    if n_dim == 3:
        # test configs: plane wave, s/p-polarization, 0/90 deg incidence
        from torchgdm.env.freespace_3d.inc_fields import PlaneWave
    elif n_dim == 2:
        from torchgdm.env.freespace_2d.inc_fields import PlaneWave
    else:
        raise ValueError(
            "Currently only 2d and 3d structures are supported in this test. "
            + f"Given structure has N_dim={n_dim}"
        )

    e_inc_list = [
        PlaneWave(e0p=1.0, e0s=0.0, inc_angle=0),
        PlaneWave(e0p=0.0, e0s=1.0, inc_angle=0),
        PlaneWave(e0p=1.0, e0s=0.0, inc_angle=torch.pi / 2),
        PlaneWave(e0p=0.0, e0s=1.0, inc_angle=torch.pi / 2),
    ]
    if n_dim == 3:
        e_inc_list += [
            PlaneWave(e0p=1.0, e0s=0.0, inc_plane="yz", inc_angle=torch.pi / 2),
            PlaneWave(e0p=0.0, e0s=1.0, inc_plane="yz", inc_angle=torch.pi / 2),
        ]

    # setup a discretized and a effective dipole pair simulation
    sim_alpha = Simulation(
        structures=[struct_alpha],
        environment=environment,
        illumination_fields=e_inc_list,
        wavelengths=wavelengths,
        device=device,
    )
    sim_discr = Simulation(
        structures=[struct_full],
        environment=environment,
        illumination_fields=e_inc_list,
        wavelengths=wavelengths,
        device=device,
    )

    # run simulations and calc. cross section spectra
    if verbose:
        print("-" * 55)
        print("Testing effective model vs. discretized simulation.")

    sim_alpha.run(verbose=False, progress_bar=progress_bar)
    sim_discr.run(verbose=False, progress_bar=progress_bar)

    test_results = dict()

    # calculate cross section errors
    cs_alpha = calc_spectrum(sim_alpha, crosssect.total, progress_bar=progress_bar)
    cs_discr = calc_spectrum(sim_discr, crosssect.total, progress_bar=progress_bar)

    which_cs = []
    if "scs" in which:
        which_cs.append("scs")
    if "ecs" in which:
        which_cs.append("ecs")

    for k in which_cs:
        try:
            rel_diff = (cs_discr[k] - cs_alpha[k]) / ((cs_discr[k] + cs_alpha[k]))
            test_results[k] = rel_diff

            mean_rel_error = torch.mean(torch.abs(rel_diff))
            peak_rel_error = torch.max(torch.abs(rel_diff))
            if verbose:
                print("cross sections - '{}':".format(k))
                print("    - mean rel. error: {:.3f}".format(to_np(mean_rel_error)))
                print("    - peak rel. error: {:.3f}".format(to_np(peak_rel_error)))
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

        except TypeError:
            pass

    # calculate nearfield errors several steps above structure
    from torchgdm.tools.geometry import coordinate_map_1d

    max_step = sim_discr.get_source_validity_radius().max()
    n_step_dist_nf = 5.0
    z_max = sim_discr.get_all_positions()[:, 2].max() + n_step_dist_nf * max_step
    r_probe = coordinate_map_1d(
        [-500, 500], r2=0, r3=z_max, direction="x", device=sim_discr.device
    )
    nf_discr = sim_discr.get_spectra_nf_intensity_e(
        r_probe=r_probe, progress_bar=progress_bar
    )
    nf_alpha = sim_alpha.get_spectra_nf_intensity_e(
        r_probe=r_probe, progress_bar=progress_bar
    )

    which_nf = []
    if "nf_tot" in which:
        which_nf.append("tot")
    if "nf_sca" in which:
        which_nf.append("sca")
    for k in which_nf:
        try:
            e_discr = nf_discr[k].flatten()
            e_alpha = nf_alpha[k].flatten()
            rel_diff = (e_discr - e_alpha) / ((e_discr + e_alpha))
            test_results[k] = rel_diff

            mean_rel_error = torch.mean(torch.abs(rel_diff))
            peak_rel_error = torch.max(torch.abs(rel_diff))
            if verbose:
                print("nearfield - '{}':".format(k))
                print("    - mean rel. error: {:.3f}".format(to_np(mean_rel_error)))
                print("    - peak rel. error: {:.3f}".format(to_np(peak_rel_error)))
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

        except TypeError:
            pass
    if verbose:
        print("-" * 60)

    return test_results
