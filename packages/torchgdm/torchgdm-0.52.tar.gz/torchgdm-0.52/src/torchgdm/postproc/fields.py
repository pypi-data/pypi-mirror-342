# -*- coding: utf-8 -*-
"""
near-fields and far-fields
"""
# %%
import warnings

import torch

from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX
from torchgdm.tools.misc import get_default_device
from torchgdm.tools.misc import get_closest_wavelength
from torchgdm.tools.batch import batched
from torchgdm.tools.batch import add_illuminations_info_to_dict


# --- internal helper
def _check_position_devices(r1: torch.tensor, r2: torch.tensor):
    if r1.device != r2.device:
        raise ValueError(
            "Position inputs are not on same device! Is `r_probe` on same device as the simulation?"
        )


def _pos_and_src_closer_than_step(
    sim,
    r_probe: torch.Tensor,
    source_distance_steps: float = 1.0,
):
    dipole_step_radius = sim.get_source_validity_radius()
    pos_p, pos_m = sim._get_polarizable_positions_p_m()
    idx_p, idx_m = sim._get_polarizable_positions_indices_p_m()

    dipole_stepsizes_p = torch.index_select(dipole_step_radius, 0, idx_p)
    dipole_stepsizes_m = torch.index_select(dipole_step_radius, 0, idx_m)

    # p-sources too close to r_probe
    all_dist_vec_p = r_probe.unsqueeze(1) - pos_p.unsqueeze(0)
    all_dist_p = torch.linalg.norm(all_dist_vec_p, dim=-1)
    mask_inner_p = all_dist_p <= (source_distance_steps * dipole_stepsizes_p)

    # m-sources too close to r_probe
    all_dist_vec_m = r_probe.unsqueeze(1) - pos_m.unsqueeze(0)
    all_dist_m = torch.linalg.norm(all_dist_vec_m, dim=-1)
    mask_inner_m = all_dist_m <= (source_distance_steps * dipole_stepsizes_m)

    # return masks for probe locations inside and outside
    return (mask_inner_p, mask_inner_m)


def _eval_Gpm(func_Gp, func_Gm, r_probe, r_p, r_m, wavelength):
    _check_position_devices(r_probe, r_p)

    # Green's tensors for propagation
    Gp = func_Gp(r_probe.unsqueeze(1), r_p.unsqueeze(0), wavelength=wavelength)
    Gm = func_Gm(r_probe.unsqueeze(1), r_m.unsqueeze(0), wavelength=wavelength)
    return Gp, Gm


# ******************************************************************
# main field calculation routines
# ******************************************************************
# --- private functions internally used by high-level interface
@batched(
    batch_kwarg="r_probe",
    arg_position=2,
    out_dim_batch=1,
    default_batch_size=1024,
    title="batched nearfield calculation",
)
def _nearfield(
    sim,
    wavelength: float,
    r_probe: torch.Tensor,
    illumination_index: int = None,  # None: batch all illumination fields
    source_distance_steps: float = 1.0,
    interpolation_step_range: float = 1.0,  # internal field interpolation
    **kwargs,
):
    wavelength = get_closest_wavelength(sim, wavelength)

    # test r_probe consistency
    if type(r_probe) == dict:
        _r = r_probe["r_probe"]
    r_probe = torch.as_tensor(r_probe, device=sim.device, dtype=DTYPE_FLOAT)
    r_probe = torch.atleast_2d(r_probe)

    assert len(r_probe.shape) == 2
    assert r_probe.shape[1] == 3

    # source positions and dipole moments
    p, m, pos_p, pos_m = sim.get_p_m_selfconsistent(wavelength, illumination_index)

    # Green's tensors for propagation
    G_EHp_6x3, G_EHm_6x3 = _eval_Gpm(
        sim.environment.get_G_EHp_6x3,
        sim.environment.get_G_EHm_6x3,
        r_probe,
        pos_p,
        pos_m,
        wavelength,
    )

    # scattered fields from all sources
    all_EHp = torch.matmul(
        G_EHp_6x3.unsqueeze(1), p.unsqueeze(0).unsqueeze(-1)
    ).swapaxes(1, 2)[..., 0]
    all_EHm = torch.matmul(
        G_EHm_6x3.unsqueeze(1), m.unsqueeze(0).unsqueeze(-1)
    ).swapaxes(1, 2)[..., 0]

    # identify and ignore probe positions too close to source points
    if source_distance_steps is not None:
        mask_inner_p, mask_inner_m = _pos_and_src_closer_than_step(
            sim,
            r_probe,
            source_distance_steps,
        )
        # set diverging tensors zero
        all_EHp[mask_inner_p] = 0
        all_EHm[mask_inner_m] = 0

    # superpose
    scat_EHp = torch.sum(all_EHp, axis=1).swapaxes(0, 1)
    scat_EHm = torch.sum(all_EHm, axis=1).swapaxes(0, 1)
    scat_EH = scat_EHp + scat_EHm

    # separate combined fields into E and H; creatae copies to allow aitograd
    e_sca, h_sca = torch.chunk(scat_EH, 2, dim=2)
    e_sca = e_sca.clone()
    h_sca = h_sca.clone()

    # calc. illumination and total fields
    inc_fields_at_r_probe = sim.get_fields_inc(
        wavelength=wavelength,
        r_probe=r_probe,
        illumination_index=illumination_index,
    )
    e_inc = inc_fields_at_r_probe.get_efield()
    h_inc = inc_fields_at_r_probe.get_hfield()

    e_tot = e_sca + e_inc
    h_tot = h_sca + h_inc

    # treat internal fields separately
    _e_tot_in, mask_r_e_in = _internal_fields_e(
        sim,
        wavelength=wavelength,
        r_probe=r_probe,
        illumination_index=illumination_index,
        interpolation_step_range=interpolation_step_range,
    )
    e_tot[:, mask_r_e_in] = _e_tot_in
    e_sca[:, mask_r_e_in] = e_tot[:, mask_r_e_in] - e_inc[:, mask_r_e_in]

    _h_tot_in, mask_r_h_in = _internal_fields_h(
        sim,
        wavelength=wavelength,
        r_probe=r_probe,
        illumination_index=illumination_index,
        interpolation_step_range=interpolation_step_range,
    )
    h_tot[:, mask_r_h_in] = _h_tot_in
    h_sca[:, mask_r_h_in] = h_tot[:, mask_r_h_in] - h_inc[:, mask_r_h_in]

    # wrap up in dict and add information on illumination fields
    res_dict = dict(
        e_sca=e_sca, e_tot=e_tot, e_inc=e_inc, h_sca=h_sca, h_tot=h_tot, h_inc=h_inc
    )

    return res_dict


def _internal_fields_e(
    sim,
    wavelength: float,
    r_probe: torch.Tensor,
    illumination_index: int = None,  # None: batch all illumination fields
    interpolation_step_range=1.0,
    min_step_radius_distance=1.0,
    epsilon=1e-2,
):
    wavelength = sim.get_closest_wavelength(wavelength)
    dipole_step_radius = sim.get_source_validity_radius()
    pos_p, pos_m = sim._get_polarizable_positions_p_m()
    idx_p, idx_m = sim._get_polarizable_positions_indices_p_m()
    step_radius_p = torch.index_select(dipole_step_radius, 0, idx_p)

    # all distances between probe and sources
    all_dist_vec = r_probe.unsqueeze(1) - pos_p.unsqueeze(0)
    all_dist = torch.linalg.norm(all_dist_vec, dim=-1)

    # internal positions
    mask_inner = all_dist <= step_radius_p / min_step_radius_distance + epsilon
    mask_pos_in = torch.logical_not(torch.all(torch.logical_not(mask_inner), dim=1))

    # get weighted positions of internal field cells close to singular r_probe
    mask_interpol = all_dist <= (interpolation_step_range * step_radius_p)
    all_weights = 1 / (all_dist + epsilon)
    all_weights[torch.logical_not(mask_interpol)] = 0
    all_weights = all_weights / all_weights.sum(keepdim=True, dim=-1)  # normalize
    all_weights[torch.logical_not(mask_interpol)] = 0
    all_weights = all_weights[mask_pos_in]

    # get internal fields
    e_in_dat, _, _, _ = sim.get_e_h_selfconsistent(wavelength)
    if illumination_index is not None:
        e_in_dat = e_in_dat[illumination_index].unsqueeze(0)

    # weighted average of internal fields close to singular r_probe
    e_in_weighted_sum = e_in_dat.unsqueeze(1) * all_weights.unsqueeze(0).unsqueeze(-1)
    e_in_interpolated = torch.sum(e_in_weighted_sum, axis=2)

    return e_in_interpolated, mask_pos_in


def _internal_fields_h(
    sim,
    wavelength: float,
    r_probe: torch.Tensor,
    illumination_index: int = None,  # None: batch all illumination fields
    interpolation_step_range=1.0,
    min_step_radius_distance=1.0,
    epsilon=1e-2,
):
    wavelength = get_closest_wavelength(sim, wavelength)

    dipole_step_radius = sim.get_source_validity_radius()
    pos_p, pos_m = sim._get_polarizable_positions_p_m()
    idx_p, idx_m = sim._get_polarizable_positions_indices_p_m()
    step_radius_m = torch.index_select(dipole_step_radius, 0, idx_m)

    # all distances between probe and sources
    all_dist_vec = r_probe.unsqueeze(1) - pos_m.unsqueeze(0)
    all_dist = torch.linalg.norm(all_dist_vec, dim=-1)

    # internal positions
    mask_inner = all_dist <= step_radius_m * min_step_radius_distance + epsilon
    mask_pos_in = torch.logical_not(torch.all(torch.logical_not(mask_inner), dim=1))

    # get weighted positions of internal field cells close to singular r_probe
    mask_interpol = all_dist <= (interpolation_step_range * step_radius_m)
    all_weights = 1 / (all_dist + epsilon)
    all_weights[torch.logical_not(mask_interpol)] = 0
    all_weights = all_weights / all_weights.sum(keepdim=True, dim=-1)  # normalize
    all_weights[torch.logical_not(mask_interpol)] = 0
    all_weights = all_weights[mask_pos_in]

    # get internal fields
    _, h_in_dat, _,_ = sim.get_e_h_selfconsistent(wavelength)
    if illumination_index is not None:
        h_in_dat = h_in_dat[illumination_index].unsqueeze(0)

    # weighted average of internal fields close to singular r_probe
    h_in_weighted_sum = h_in_dat.unsqueeze(1) * all_weights.unsqueeze(0).unsqueeze(-1)
    h_in_interpolated = torch.sum(h_in_weighted_sum, axis=2)

    return h_in_interpolated, mask_pos_in


# @batched(  # not necessary since `_nearfield` is already batched
#     batch_kwarg="r_probe", arg_position=2, out_dim_batch=1, default_batch_size=1024
# )
def _poynting(
    sim,
    wavelength: float,
    r_probe: torch.Tensor,
    illumination_index: int = None,  # None: batch all illumination fields
    source_distance_steps: float = None,
    whichfield="tot",
    **kwargs,
):
    nf_results = _nearfield(
        sim=sim,
        wavelength=wavelength,
        r_probe=r_probe,
        illumination_index=illumination_index,
        source_distance_steps=source_distance_steps,
        pgr_bar_title="batched Poynting calculation",
        **kwargs,
    )

    if whichfield.lower() == "tot":
        e, h = nf_results["e_tot"], nf_results["h_tot"]
    elif whichfield.lower() == "sca":
        e, h = nf_results["e_sca"], nf_results["h_sca"]
    elif whichfield.lower() in ["in", "inc", "0", "zero"]:
        e, h = nf_results["e_inc"], nf_results["h_inc"]

    S = torch.cross(torch.conj(e), h, dim=-1)

    # wrap up in dict and add information on illumination fields
    res_dict = dict(poynting=S)
    return res_dict


# @batched(  # not necessary since `_nearfield` is already batched
#     batch_kwarg="r_probe", arg_position=2, out_dim_batch=1, default_batch_size=1024
# )
def _chirality(
    sim,
    wavelength: float,
    r_probe: torch.Tensor,
    illumination_index: int = None,  # None: batch all illumination fields
    source_distance_steps: float = None,
    whichfield="tot",
    **kwargs,
):
    nf_results = _nearfield(
        sim=sim,
        wavelength=wavelength,
        r_probe=r_probe,
        illumination_index=illumination_index,
        source_distance_steps=source_distance_steps,
        pgr_bar_title="batched chirality calculation",
        **kwargs,
    )
    if whichfield.lower() == "tot":
        e, h = nf_results["e_tot"], nf_results["h_tot"]
    elif whichfield.lower() == "sca":
        e, h = nf_results["e_sca"], nf_results["h_sca"]
    elif whichfield.lower() in ["in", "inc", "0", "zero"]:
        e, h = nf_results["e_inc"], nf_results["h_inc"]

    # Meinzer et al, PRB 88, 041407, 2013: C ~ Im(conj(E) * B)
    C = -1 * torch.sum(torch.multiply(torch.conj(e), h), dim=-1).imag

    # wrap up in dict and add information on illumination fields
    res_dict = dict(chirality=C)
    return res_dict


@batched(
    batch_kwarg="r_probe",
    arg_position=2,
    out_dim_batch=1,
    default_batch_size=1024,
    title="batched farfield calculation",
)
def _farfield(
    sim,
    wavelength: float,
    r_probe: torch.Tensor,
    illumination_index: int = None,  # None: batch all illumination fields
    source_distance_steps: float = None,
    **kwargs,
):
    """calulate the farfield

    Note: in the far-field, the e/m waves are transverse. E, H and k are in a fixed, orthogonal relation.
    Therefore `farfield` calculates only the electric field.

    Args:
        sim (SimulationBase):               simulation
        wavelength (float):                 evaluation wavelength (nm)
        r_probe (torch.Tensor):             positions to evaluate (sufficiently far away)
        illumination_index (int, optional): Optional index of evaluation illumination field.
                                            If None, batch-eval all. Defaults to None.

    Returns:
        dict: scattered ("ff_e_sca"), total ("ff_e_tot") and illumination ("ff_e_inc") e-fields
    """
    wavelength = get_closest_wavelength(sim, wavelength)

    # test r_probe consistency
    r_probe = r_probe.to(sim.device)
    assert len(r_probe.shape) == 2
    assert r_probe.shape[1] == 3

    # source positions and dipole moments
    p, m, r_p, r_m = sim.get_p_m_selfconsistent(wavelength, illumination_index)

    # Green's tensors for propagation
    G_Ep_3x3, G_Em_3x3 = _eval_Gpm(
        sim.environment.get_G_Ep_farfield,
        sim.environment.get_G_Em_farfield,
        r_probe,
        r_p,
        r_m,
        wavelength,
    )

    # scattered fields from all sources
    all_Ep = torch.matmul(G_Ep_3x3.unsqueeze(1), p.unsqueeze(0).unsqueeze(-1)).swapaxes(
        1, 2
    )[..., 0]
    all_Em = torch.matmul(G_Em_3x3.unsqueeze(1), m.unsqueeze(0).unsqueeze(-1)).swapaxes(
        1, 2
    )[..., 0]

    # ignore source points too close to probe position
    if source_distance_steps is not None:
        all_Ep, all_Em = _pos_and_src_closer_than_step(
            sim, all_Ep, all_Em, r_probe, source_distance_steps
        )

    # superpose
    scat_Ep = torch.sum(all_Ep, axis=1).swapaxes(0, 1)
    scat_Em = torch.sum(all_Em, axis=1).swapaxes(0, 1)
    e_sca = scat_Ep + scat_Em

    # illumination fields, total fields
    inc_fields_at_r_probe = sim.get_fields_inc(
        wavelength=wavelength,
        r_probe=r_probe,
        illumination_index=illumination_index,
    )
    e_inc = inc_fields_at_r_probe.get_efield()
    e_tot = e_sca + e_inc

    # wrap up in dict and add information on illumination fields
    res_dict = dict(ff_e_sca=e_sca, ff_e_tot=e_tot, ff_e_inc=e_inc)
    return res_dict


# --- alternative e-only / h-only:
@batched(
    batch_kwarg="r_probe",
    arg_position=2,
    out_dim_batch=1,
    default_batch_size=1024,
    title="batched nearfield calculation (E only)",
)
def _nearfield_e(
    sim,
    wavelength: float,
    r_probe: torch.Tensor,
    illumination_index: int = None,  # None: batch all illumination fields
    source_distance_steps: float = None,
    **kwargs,
):
    """calculate E-field only.
    Note: this does not correctly process positions inside a structure

    further kwargs are ignored
    """

    wavelength = get_closest_wavelength(sim, wavelength)

    # test r_probe consistency
    r_probe = r_probe.to(sim.device)
    assert len(r_probe.shape) == 2
    assert r_probe.shape[1] == 3

    # source positions and dipole moments
    p, m, r_p, r_m = sim.get_p_m_selfconsistent(wavelength, illumination_index)

    # Green's tensors for propagation
    G_Ep_3x3, G_Em_3x3 = _eval_Gpm(
        sim.environment.get_G_Ep,
        sim.environment.get_G_Em,
        r_probe,
        r_p,
        r_m,
        wavelength,
    )

    # scattered fields from all sources
    all_Ep = torch.matmul(G_Ep_3x3.unsqueeze(1), p.unsqueeze(0).unsqueeze(-1)).swapaxes(
        1, 2
    )[..., 0]
    all_Em = torch.matmul(G_Em_3x3.unsqueeze(1), m.unsqueeze(0).unsqueeze(-1)).swapaxes(
        1, 2
    )[..., 0]

    # identify and ignore probe positions too close to source points
    if source_distance_steps is not None:
        mask_inner_p, mask_inner_m = _pos_and_src_closer_than_step(
            sim, r_probe, source_distance_steps
        )
        # set diverging tensors zero
        all_Ep[mask_inner_p] = 0
        all_Em[mask_inner_m] = 0

    # superpose
    scat_Ep = torch.sum(all_Ep, axis=1).swapaxes(0, 1)
    scat_Em = torch.sum(all_Em, axis=1).swapaxes(0, 1)
    e_sca = scat_Ep + scat_Em

    # illumination fields, total fields
    inc_fields_at_r_probe = sim.get_fields_inc(
        wavelength=wavelength,
        r_probe=r_probe,
        illumination_index=illumination_index,
    )
    e_inc = inc_fields_at_r_probe.get_efield()
    e_tot = e_sca + e_inc

    # wrap up in dict and add information on illumination fields
    res_dict = dict(e_sca=e_sca, e_tot=e_tot, e_inc=e_inc)
    return res_dict


@batched(
    batch_kwarg="r_probe",
    arg_position=2,
    out_dim_batch=1,
    default_batch_size=1024,
    title="batched nearfield calculation (H only)",
)
def _nearfield_h(
    sim,
    wavelength: float,
    r_probe: torch.Tensor,
    illumination_index: int = None,  # None: batch all illumination fields
    source_distance_steps: float = None,
    **kwargs,
):
    """calculate H-field only.
    Note: this does not correctly process positions inside a structure

    further kwargs are ignored
    """
    wavelength = get_closest_wavelength(sim, wavelength)

    # test r_probe consistency
    r_probe = r_probe.to(sim.device)
    assert len(r_probe.shape) == 2
    assert r_probe.shape[1] == 3

    # source positions and dipole moments
    p, m, r_p, r_m = sim.get_p_m_selfconsistent(wavelength, illumination_index)

    # Green's tensors for propagation
    G_Hp_3x3, G_Hm_3x3 = _eval_Gpm(
        sim.environment.get_G_Hp,
        sim.environment.get_G_Hm,
        r_probe,
        r_p,
        r_m,
        wavelength,
    )

    # scattered fields from all sources
    all_Hp = torch.matmul(G_Hp_3x3.unsqueeze(1), p.unsqueeze(0).unsqueeze(-1)).swapaxes(
        1, 2
    )[..., 0]
    all_Hm = torch.matmul(G_Hm_3x3.unsqueeze(1), m.unsqueeze(0).unsqueeze(-1)).swapaxes(
        1, 2
    )[..., 0]

    # identify and ignore probe positions too close to source points
    if source_distance_steps is not None:
        mask_inner_p, mask_inner_m = _pos_and_src_closer_than_step(
            sim, r_probe, source_distance_steps
        )
        # set diverging tensors zero
        all_Hp[mask_inner_p] = 0
        all_Hm[mask_inner_m] = 0

    # superpose
    scat_Hp = torch.sum(all_Hp, axis=1).swapaxes(0, 1)
    scat_Hm = torch.sum(all_Hm, axis=1).swapaxes(0, 1)
    h_sca = scat_Hp + scat_Hm

    # illumination fields, total fields
    inc_fields_at_r_probe = sim.get_fields_inc(
        wavelength=wavelength,
        r_probe=r_probe,
        illumination_index=illumination_index,
    )
    h_inc = inc_fields_at_r_probe.get_hfield()
    h_tot = h_sca + h_inc

    # wrap up in dict and add information on illumination fields
    res_dict = dict(h_sca=h_sca, h_tot=h_tot, h_inc=h_inc)
    return res_dict


# --- public functions of high-level API
@batched(
    batch_kwarg="r_probe",
    arg_position=2,
    out_dim_batch=1,
    default_batch_size=256,
    title="batched field gradient calculation",
)
def _field_grad(
    sim,
    wavelength: float,
    r_probe: torch.Tensor,
    illumination_index: int = None,  # None: batch all illumination fields
    source_distance_steps: float = None,
    delta=0.1,
    whichfield="e_tot",
    **kwargs,
):
    """nearfield gradient distribution inside or in proximity of a nanostructure"""
    # =============================================================================
    #     Exception handling
    # =============================================================================
    wavelength = get_closest_wavelength(sim, wavelength)

    # if r_probe is None:
    #     r_probe = sim.get_all_positions()

    if type(r_probe) == dict:
        r_probe = r_probe["r_probe"]

    # move probe positions to same device as simulation
    r_probe = torch.as_tensor(r_probe, device=sim.device, dtype=DTYPE_FLOAT)
    if len(r_probe.shape) == 1:
        r_probe = r_probe.unsqueeze(0)
    assert len(r_probe.shape) == 2
    assert r_probe.shape[1] == 3

    # =============================================================================
    #     preparation
    # =============================================================================
    whichfield = whichfield.lower()
    if whichfield not in ["e_tot", "e_sca", "e_inc", "h_tot", "h_sca", "h_inc"]:
        raise ValueError(
            "Wrong argument for `field`. Must be one of "
            + "['e_tot', 'e_sca', 'e_inc', 'h_tot', 'h_sca', 'h_inc']."
        )

    kw = dict(
        sim=sim,
        wavelength=wavelength,
        illumination_index=illumination_index,
    )

    if whichfield.lower() == "e_inc":

        def get_e0_wrap(**kwargs):
            if "sim" in kwargs:
                kwargs.pop("sim")
            inc_fields_at_r_probe = sim.get_fields_inc(**kwargs)
            return dict(e_inc=inc_fields_at_r_probe.get_efield())

        field_func = get_e0_wrap

    elif whichfield.lower() == "h_inc":

        def get_h0_wrap(**kwargs):
            if "sim" in kwargs:
                kwargs.pop("sim")
            inc_fields_at_r_probe = sim.get_fields_inc(**kwargs)
            return dict(h_inc=inc_fields_at_r_probe.get_hfield())

        field_func = get_h0_wrap

    else:
        field_func = _nearfield
        kw["source_distance_steps"] = source_distance_steps

    # =============================================================================
    #     calc field gradients
    # =============================================================================

    ## --- d/dx
    r_probe_px = torch.clone(r_probe)  # Xmap+delta
    r_probe_mx = torch.clone(r_probe)  # Xmap-delta
    r_probe_px.T[0] += delta
    r_probe_mx.T[0] -= delta
    F_px = field_func(r_probe=r_probe_px, **kw)[whichfield]
    F_mx = field_func(r_probe=r_probe_mx, **kw)[whichfield]

    dFdx = (F_px - F_mx) / (2 * delta)

    ## --- d/dy
    r_probe_py = torch.clone(r_probe)  # Ymap+delta
    r_probe_my = torch.clone(r_probe)  # Ymap-delta
    r_probe_py.T[1] += delta
    r_probe_my.T[1] -= delta
    F_py = field_func(r_probe=r_probe_py, **kw)[whichfield]
    F_my = field_func(r_probe=r_probe_my, **kw)[whichfield]

    dFdy = (F_py - F_my) / (2 * delta)

    ## --- d/dz
    r_probe_pz = torch.clone(r_probe)  # Zmap+delta
    r_probe_mz = torch.clone(r_probe)  # Zmap-delta
    r_probe_pz.T[2] += delta
    r_probe_mz.T[2] -= delta
    F_pz = field_func(r_probe=r_probe_pz, **kw)[whichfield]
    F_mz = field_func(r_probe=r_probe_mz, **kw)[whichfield]

    dFdz = (F_pz - F_mz) / (2 * delta)

    # wrap up in dict and add information on illumination fields
    res_dict = dict(dfdx=dFdx, dfdy=dFdy, dfdz=dFdz)
    return res_dict


# --- high-level interface
def nf(
    sim,
    wavelength: float,
    r_probe: dict = None,
    illumination_index: int = None,  # None: batch all illumination fields
    progress_bar=True,
    **kwargs,
):
    """nearfield (electric and magnetic) at positions `r_probe`

    Args:
        sim (:class:`torchgdm.Simulation`): simulation instance
        wavelength (float): evaluation wavelength (in nm)
        r_probe (dict, optional): probe locations describing dict (gen. from `tools.geometry`).  Defaults to None, in which case all positions of the simulation structures are used
        illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.
        progress_bar (bool, optional): Show progress bar. Defaults to True.

    Returns:
        dict: contains results for total, scattered and incident fields in instances of :class:`torchgdm.Field`
    """
    from torchgdm.field import Field

    if r_probe is None:
        r_probe = sim.get_all_positions()
        _r = r_probe
        warnings.warn(
            "No positions given. Falling back to internal fields. "
            + "For internal field intensities, you may use the "
            + "faster `integrated_nf_intensity_e_inside`."
        )
    elif type(r_probe) == dict:
        _r = r_probe["r_probe"]
    else:
        r_probe = torch.as_tensor(r_probe, device=sim.device, dtype=DTYPE_FLOAT)
        r_probe = torch.atleast_2d(r_probe)
        _r = r_probe

    nf_res = _nearfield(
        sim=sim,
        wavelength=wavelength,
        r_probe=_r,
        illumination_index=illumination_index,
        progress_bar=progress_bar,
        **kwargs,
    )
    res_dict = {}

    res_dict["sca"] = Field(r_probe, efield=nf_res["e_sca"], hfield=nf_res["h_sca"])
    res_dict["tot"] = Field(r_probe, efield=nf_res["e_tot"], hfield=nf_res["h_tot"])
    res_dict["inc"] = Field(r_probe, efield=nf_res["e_inc"], hfield=nf_res["h_inc"])
    res_dict["wavelength"] = wavelength

    # add information on illumination field config
    res_dict = add_illuminations_info_to_dict(
        sim, res_dict, illumination_index=illumination_index
    )

    return res_dict


def field_gradient(
    sim,
    wavelength: float,
    r_probe: torch.Tensor,
    illumination_index: int = None,  # None: batch all illumination fields
    source_distance_steps: float = None,
    delta=0.1,
    whichfield="e_tot",
    **kwargs,
):
    """nearfield gradient distribution inside or in proximity of a nanostructure

    Calculate field-gradients (positions defined by `r_probe`).
    pytorch AD is not efficient for gradients of functions R^n --> R^m, with $n \\sim m >> 1$.
    Therefore, here numerical derivatives are calculated via center differences.

    Based on the original implementation in pyGDM by C. Majorel.

    Warning: The current implementation is not memory efficient, since all fields are calculated, even though not required.

    Args:
        sim (:class:`torchgdm.Simulation`): simulation instance
        wavelength (float): in nm
        r_probe (torch.Tensor): tuple (x,y,z) or list of 3-lists/-tuples to evaluate field gradients.
        illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.
        delta (float, optional):  differential step for numerical center-derivative (in nanometers). Defaults to 0.1.
        whichfield (str, optional): fields to calculate the gradient for. One of ["e_sca","e_tot","e_inc", "h_sca","h_tot,"h_inc], . Defaults to "e_tot".

    Raises:
        ValueError: _description_

    Returns:
        3 lists of 3-tuples [dAx, dAy, dAz] (complex): dAj are the differential terms:
            - idx [0] = dE/dx = [dEx/dx, dEy/dx, dEz/dx]
            - idx [1] = dE/dy = [dEx/dy, dEy/dy, dEz/dy]
            - idx [2] = dE/dz = [dEx/dz, dEy/dz, dEz/dz]
    """
    if type(r_probe) == dict:
        _r_probe = r_probe["r_probe"]
    else:
        _r_probe = r_probe

    grad_f_dict = _field_grad(
        sim=sim,
        wavelength=wavelength,
        r_probe=_r_probe,
        illumination_index=illumination_index,
        source_distance_steps=source_distance_steps,
        delta=delta,
        whichfield=whichfield,
        **kwargs,
    )

    return grad_f_dict


def ff(
    sim,
    wavelength: float,
    r_probe: dict = None,
    illumination_index: int = None,  # None: batch all illumination fields
    progress_bar=True,
    **kwargs,
):
    """far-field (electric and magnetic) at positions `r_probe`

    Args:
        sim (:class:`torchgdm.Simulation`): simulation instance
        wavelength (float): evaluation wavelength (in nm)
        r_probe (dict, optional): probe locations describing dict (gen. from `tools.geometry`). Defaults to None, in which case full hemisphere coordinates are used
        illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.
        progress_bar (bool, optional): Show progress bar. Defaults to True.

    Returns:
        dict: contains results for total, scattered and incident fields in instances of :class:`torchgdm.Field`
    """

    from torchgdm.field import Field

    if r_probe is None:
        from torchgdm.tools.geometry import coordinate_map_2d_spherical

        r_probe = coordinate_map_2d_spherical()  # full hemisphere
        _r = r_probe["r_probe"]
    elif type(r_probe) == dict:
        _r = r_probe["r_probe"]
    else:
        r_probe = torch.as_tensor(r_probe, device=sim.device, dtype=DTYPE_FLOAT)
        r_probe = torch.atleast_2d(r_probe)
        _r = r_probe

    ff_res = _farfield(
        sim=sim,
        wavelength=wavelength,
        r_probe=_r,
        illumination_index=illumination_index,
        progress_bar=progress_bar,
        **kwargs,
    )
    res_dict = {}

    res_dict["sca"] = Field(r_probe, efield=ff_res["ff_e_sca"])
    res_dict["tot"] = Field(r_probe, efield=ff_res["ff_e_tot"])
    res_dict["inc"] = Field(r_probe, efield=ff_res["ff_e_inc"])
    res_dict["wavelength"] = wavelength

    # add information on illumination field config
    res_dict = add_illuminations_info_to_dict(
        sim, res_dict, illumination_index=illumination_index
    )

    return res_dict


def integrated_nf_intensity_e(
    sim,
    wavelength: float,
    r_probe: dict = None,
    illumination_index: int = None,  # None: batch all illumination fields
    **kwargs,
):
    """integrated electric near-field intensity at positions `r_probe`

    Args:
        sim (:class:`torchgdm.Simulation`): simulation instance
        wavelength (float): evaluation wavelength (in nm)
        r_probe (dict, optional): probe locations describing dict (gen. from `tools.geometry`). Defaults to None, in which case all positions of the simulation structures are used
        illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.

    Returns:
        dict: contains results for total, scattered and incident integrated E-field intensity
    """
    r_nf = nf(sim, wavelength, r_probe, illumination_index, **kwargs)

    res_dict = {}

    res_dict["wavelength"] = wavelength
    res_dict["sca"] = r_nf["sca"].get_integrated_efield_intensity()
    res_dict["tot"] = r_nf["tot"].get_integrated_efield_intensity()
    res_dict["inc"] = r_nf["inc"].get_integrated_efield_intensity()

    # add information on illumination field config
    res_dict = add_illuminations_info_to_dict(
        sim, res_dict, illumination_index=illumination_index
    )

    return res_dict


def integrated_nf_intensity_e_inside(
    sim,
    wavelength: float,
    illumination_index: int = None,  # None: batch all illumination fields
    **kwargs,
):
    """rapid function to calculate average internal total electric field intensity"""
    from torchgdm import to_np

    wl = float(to_np(wavelength))
    I_e = sim.fields_inside[wl].get_integrated_efield_intensity()
    I_e = I_e / len(sim.get_all_positions())

    res_dict = {}
    res_dict["wavelength"] = wavelength
    res_dict["tot"] = I_e

    # add information on illumination field config
    res_dict = add_illuminations_info_to_dict(
        sim, res_dict, illumination_index=illumination_index
    )

    return res_dict


def integrated_nf_intensity_h(
    sim,
    wavelength: float,
    r_probe: dict = None,
    illumination_index: int = None,  # None: batch all illumination fields
    **kwargs,
):
    """integrated magnetic near-field intensity at positions `r_probe`

    Args:
        sim (:class:`torchgdm.Simulation`): simulation instance
        wavelength (float): evaluation wavelength (in nm)
        r_probe (dict, optional): probe locations describing dict (gen. from `tools.geometry`). Defaults to None, in which case all positions of the simulation structures are used
        illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.

    Returns:
        dict: contains results for total, scattered and incident integrated H-field intensity
    """
    r_nf = nf(sim, wavelength, r_probe, illumination_index, **kwargs)

    res_dict = {}

    res_dict["wavelength"] = wavelength
    res_dict["sca"] = r_nf["sca"].get_integrated_hfield_intensity()
    res_dict["tot"] = r_nf["tot"].get_integrated_hfield_intensity()
    res_dict["inc"] = r_nf["inc"].get_integrated_hfield_intensity()

    # add information on illumination field config
    res_dict = add_illuminations_info_to_dict(
        sim, res_dict, illumination_index=illumination_index
    )

    return res_dict


def integrated_nf_intensity_h_inside(
    sim,
    wavelength: float,
    illumination_index: int = None,  # None: batch all illumination fields
    **kwargs,
):
    """rapid function to calculate average internal total magnetic field intensity"""
    from torchgdm import to_np

    wl = float(to_np(wavelength))
    I_h = sim.fields_inside[wl].get_integrated_hfield_intensity()
    I_h = I_h / len(sim.get_all_positions())

    res_dict = {}
    res_dict["wavelength"] = wavelength
    res_dict["tot"] = I_h

    # add information on illumination field config
    res_dict = add_illuminations_info_to_dict(
        sim, res_dict, illumination_index=illumination_index
    )

    return res_dict


def integrated_ff_intensity(
    sim,
    wavelength: float,
    r_probe: dict = None,
    illumination_index: int = None,  # None: batch all illumination fields
    **kwargs,
):
    """integrated far-field intensity (E-field) at positions `r_probe`

    Args:
        sim (:class:`torchgdm.Simulation`): simulation instance
        wavelength (float): evaluation wavelength (in nm)
        r_probe (dict, optional): probe locations describing dict (gen. from `tools.geometry`). Defaults to None, in which case full hemisphere coordinates are used
        illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.

    Returns:
        dict: contains results for total, scattered and incident integrated far-field E-field intensity
    """
    r_ff = ff(sim, wavelength, r_probe, illumination_index, **kwargs)

    res_dict = {}

    res_dict["wavelength"] = wavelength
    res_dict["sca"] = r_ff["sca"].get_integrated_efield_intensity()
    res_dict["tot"] = r_ff["tot"].get_integrated_efield_intensity()
    res_dict["inc"] = r_ff["inc"].get_integrated_efield_intensity()

    # add information on illumination field config
    res_dict = add_illuminations_info_to_dict(
        sim, res_dict, illumination_index=illumination_index
    )

    return res_dict

