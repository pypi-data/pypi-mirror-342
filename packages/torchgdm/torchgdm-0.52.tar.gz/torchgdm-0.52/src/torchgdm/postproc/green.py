# -*- coding: utf-8 -*-
"""Green's function and LDOS"""
# %%
import warnings

import torch

import torchgdm as tg
from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX
from torchgdm.tools.misc import get_default_device
from torchgdm.linearsystem import _expand_dimensions
from torchgdm.linearsystem import _reduce_dimensions
from torchgdm.tools.misc import _test_positional_input
from torchgdm.tools.batch import batched


def G(
    sim,
    r_probe: torch.Tensor,
    r_source: torch.Tensor,
    wavelength: float,
    use_sim_copy=True,
    progress_bar=True,
    verbose=False,
    **kwargs,
):
    """calculate the Green's tensor of the complex environment defined by `sim`

    Args:
        sim (`torchgdm.Simulation`): simulation
        r_probe (torch.Tensor): probe position(s)
        r_source (torch.Tensor): source location(s)
        wavelength (float): in nm
        use_sim_copy (bool, optional): Use copy of simulation or use simulation in-place. May not work in some autograd scenario. Defaults to True.
        progress_bar (bool, optional): Show progress bar. Defaults to True.
        verbose (bool, optional): Print status of underlying simulation call. Defaults to False.

    Returns:
        dict: contains Green's tensors for all source/probe position combinations:
            - "G_6x6": full 6x6 tensor
            - "G_Ep": electric-electric 3x3 tensor
            - "G_Em": electric-magnetic 3x3 tensor
            - "G_Hp": magnetic-electric 3x3 tensor
            - "G_Hm": magnetic-magnetic 3x3 tensor
    """
    if type(r_probe) == dict:
        r_probe = r_probe["r_probe"]
    if type(r_source) == dict:
        r_source = r_source["r_probe"]

    if r_probe is None:
        r_probe = r_source

    r_probe = torch.as_tensor(r_probe, dtype=DTYPE_FLOAT, device=sim.device)
    r_source = torch.as_tensor(r_source, dtype=DTYPE_FLOAT, device=sim.device)
    r_probe, r_source = _test_positional_input(r_probe, r_source)

    if len(r_source.shape) == 1:
        r_source = r_source.unsqueeze(0)
    if len(r_probe.shape) == 1:
        r_probe = r_probe.unsqueeze(0)

    if use_sim_copy:
        _sim = sim.copy()
    else:
        _sim = sim
        warnings.warn("Using simulation in-place modifies the illuminations!")

    # --- configure p, m dipole illuminations with all perpendicular orientations
    e_inc_list = []
    for r_dp in r_source:
        dp_orients = torch.zeros((6, 6))
        dp_orients[torch.arange(6), torch.arange(6)] = 1
        for dp in dp_orients:
            e_inc_list.append(
                tg.env.IlluminationDipole(
                    r_source=r_dp,
                    dp_source=dp,
                    n_dim=_sim.environment.n_dim,
                    device=sim.device,
                )
            )
    _sim.illumination_fields = e_inc_list

    # run the simulation
    _sim.run(calc_missing=False, verbose=verbose, progress_bar=progress_bar)

    nf_results = tg.postproc.fields.nf(
        _sim,
        wavelength,
        r_probe=r_probe,
        progress_bar=progress_bar,
        pgr_bar_title="batched Green's tensor evaluation",
        **kwargs,
    )
    e_sca = nf_results["tot"]

    G_E = e_sca.efield
    G_H = e_sca.hfield

    # reshape. second last column e-field components, last column dipole orientations
    G_E = G_E.reshape(-1, 6, *G_E.shape[1:])
    G_E = torch.moveaxis(G_E, 1, -1)
    G_H = G_H.reshape(-1, 6, *G_H.shape[1:])
    G_H = torch.moveaxis(G_H, 1, -1)

    G_Ep = G_E[..., :3]
    G_Em = G_E[..., 3:]
    G_Hp = G_H[..., :3]
    G_Hm = G_H[..., 3:]

    G_6x6 = torch.cat([G_E, G_H], dim=-2)

    return dict(G_6x6=G_6x6, G_Ep=G_Ep, G_Em=G_Em, G_Hp=G_Hp, G_Hm=G_Hm)


def ldos(
    sim,
    r_probe: torch.Tensor,
    wavelength: float,
    progress_bar=True,
    verbose=0,
    **kwargs,
):
    """calculate the relative LDOS of the complex environment defined by `sim`

    this is yields the same results as Green's tensor evaluation, but
    is optimized for evaluation of (r_source, r_source) tuples

    Args:
        sim (`torchgdm.Simulation`): simulation
        r_probe (torch.Tensor): probe position(s)
        wavelength (float): in nm
        progress_bar (bool, optional): Show progress bar. Defaults to True.
        verbose (bool, optional): Print status info. Defaults to False.

    Returns:
        dict: contains Green's tensors, partial and averaged LDOS all probe positions:
            - "G_ii": full 6x6 tensor
            - "ldos_partial": partial electric (first 3) and magnetic (last 3) LDOS. (Diagonal elements of Green's tensor)
            - "ldos_e": full electric LDOS
            - "ldos_m": full magnetic LDOS
    """
    @batched(
        batch_kwarg="r_src",
        arg_position=2,
        out_dim_batch=0,
        default_batch_size=128,
        title="batched LDOS calculation",
    )
    def _eval_Gii(sim, wavelength, r_src, r_geo, K, alpha, **kwargs):
        # kwargs are ignored
        
        # dyads: source -> structure
        Q = sim.environment.get_G_6x6(
            r_geo.unsqueeze(0), r_src.unsqueeze(1), wavelength
        )

        # dyads: structure -> probe
        S = sim.environment.get_G_6x6(
            r_src.unsqueeze(0), r_geo.unsqueeze(1), wavelength
        )
        
        # alpha dot K
        K_NxN = _reduce_dimensions(K)
        alpha_K_NxN = torch.matmul(alpha, K_NxN)
        aK = _expand_dimensions(alpha_K_NxN, N=6)

        # calculate double integral of tensor products:
        aKS = torch.einsum("jkab, kmbc -> jmac", [aK, S])
        tg.tools.misc._purge_mem(aK)
        QaKS = torch.einsum("njab, jnbc -> nca", [Q, aKS])
        tg.tools.misc._purge_mem(aKS)

        return QaKS
    
    if verbose:
        print("-" * 60)
        print(sim)
        print("\nrun LDOS simulation.")

    # - prep
    if type(r_probe) == dict:
        r_src = r_probe["r_probe"]
    else:
        r_src = r_probe

    r_src = torch.as_tensor(r_src, dtype=DTYPE_FLOAT, device=sim.device)

    if len(r_src.shape) == 1:
        r_src = r_src.unsqueeze(0)

    r_geo = sim.get_all_positions()

    # - evaluate and integrate Q.alpha.K.S
    # --- dyads
    # TODO: memory efficiency
    #   - use polarizable positions only
    #   - Q and S as reduced coupling matrices
    
    # polarizabilities (mesh-dipoles, eff. dp-pairs and GPMs)
    if verbose:
        print("get alphas...", end="")
 
    all_alpha = []
    for s in sim.structures:
        all_alpha += list(
            s.get_polarizability_6x6(wavelength, sim.environment).unbind()
        )
    alpha = torch.block_diag(*all_alpha)
    
    # Note: for discretized structures this is not memory / computational efficient!
    if verbose:
        print(" Done.\nsolve linear system...", end="")
    full_linsys = tg.linearsystem.LinearSystemFullInverse(device=sim.device)
    K_red = full_linsys.get_generalized_propagator(sim, wavelength=wavelength)
    K = _expand_dimensions(K_red, N=6)
    tg.tools.misc._purge_mem(K_red)
    if verbose:
        print(" Done.")

    G_ii = _eval_Gii(
        sim,
        wavelength,
        r_src=r_src,
        r_geo=r_geo,
        K=K,
        alpha=alpha,
        progress_bar=progress_bar,
        **kwargs,
    )

    k0 = 2 * torch.pi / wavelength
    prefactor = (3.0 / 2.0) * (1.0 / k0**3)
    G_ii_diag = torch.diagonal(G_ii, offset=0, dim1=1, dim2=2)

    ldos_partial = 1.0 + prefactor * G_ii_diag.imag
    ldos_e = 1.0 + prefactor * torch.sum(G_ii_diag[:, :3].imag, dim=-1)
    ldos_m = 1.0 + prefactor * torch.sum(G_ii_diag[:, 3:].imag, dim=-1)

    return dict(G_ii=G_ii, ldos_partial=ldos_partial, ldos_e=ldos_e, ldos_m=ldos_m)



# - convenience wrapper
def G_6x6(
    sim,
    r_probe: torch.Tensor,
    r_source: torch.Tensor,
    wavelength: float,
    use_sim_copy=True,
    progress_bar=False,
    **kwargs,
):
    """alias for :func:`G`, see there for more documentation.

    calculate the Ep Green's tensor for `sim`

    Returns:
        torch.Tensor: full electric-magnetic Green's tensor for all source/probe position combinations
    """
    G_results = G(
        sim=sim,
        r_probe=r_probe,
        r_source=r_source,
        wavelength=wavelength,
        use_sim_copy=use_sim_copy,
        progress_bar=progress_bar,
        **kwargs,
    )
    return G_results["G_6x6"]


def G_Ep(
    sim,
    r_probe: torch.Tensor,
    r_source: torch.Tensor,
    wavelength: float,
    use_sim_copy=True,
    progress_bar=False,
    **kwargs,
):
    """calculate the Ep Green's tensor for `sim`

    wrapper to :func:`G`, see there for more documentation.

    Returns:
        torch.Tensor: electric-electric Green's tensor for all source/probe position combinations
    """
    G_results = G(
        sim=sim,
        r_probe=r_probe,
        r_source=r_source,
        wavelength=wavelength,
        use_sim_copy=use_sim_copy,
        progress_bar=progress_bar,
        **kwargs,
    )
    return G_results["G_Ep"]


def G_Em(
    sim,
    r_probe: torch.Tensor,
    r_source: torch.Tensor,
    wavelength: float,
    use_sim_copy=True,
    progress_bar=False,
    **kwargs,
):
    """calculate the Em Green's tensor for `sim`

    wrapper to :func:`G`, see there for more documentation.

    Returns:
        torch.Tensor: electric-magnetic Green's tensor for all source/probe position combinations
    """
    G_results = G(
        sim=sim,
        r_probe=r_probe,
        r_source=r_source,
        wavelength=wavelength,
        use_sim_copy=use_sim_copy,
        progress_bar=progress_bar,
        **kwargs,
    )
    return G_results["G_Em"]


def G_Hp(
    sim,
    r_probe: torch.Tensor,
    r_source: torch.Tensor,
    wavelength: float,
    use_sim_copy=True,
    progress_bar=False,
    **kwargs,
):
    """calculate the Hp Green's tensor for `sim`

    wrapper to :func:`G`, see there for more documentation.

    Returns:
        torch.Tensor: magnetic-electric Green's tensor for all source/probe position combinations
    """
    G_results = G(
        sim=sim,
        r_probe=r_probe,
        r_source=r_source,
        wavelength=wavelength,
        use_sim_copy=use_sim_copy,
        progress_bar=progress_bar,
        **kwargs,
    )
    return G_results["G_Hp"]


def G_Hm(
    sim,
    r_probe: torch.Tensor,
    r_source: torch.Tensor,
    wavelength: float,
    use_sim_copy=True,
    progress_bar=False,
    **kwargs,
):
    """calculate the Hm Green's tensor for `sim`

    wrapper to :func:`G`, see there for more documentation.

    Returns:
        torch.Tensor: magnetic-magnetic Green's tensor for all source/probe position combinations
    """
    G_results = G(
        sim=sim,
        r_probe=r_probe,
        r_source=r_source,
        wavelength=wavelength,
        use_sim_copy=use_sim_copy,
        progress_bar=progress_bar,
        **kwargs,
    )
    return G_results["G_Hm"]



def _G_direct(
    sim,
    r_probe: torch.Tensor,
    r_source: torch.Tensor,
    wavelength: float = None,
    verbose=False,
    progress_bar=True,
    **kwargs,
):
    """calculate the Green's tensor via direct evaluation

    should give the same results as :func:`G`, but significantly less memory efficient
    and incorrect inside a discretized nanostructure.

    Args:
        sim (`torchgdm.Simulation`): simulation
        r_probe (torch.Tensor): probe position(s)
        r_source (torch.Tensor): source location(s)
        wavelength (float): in nm
    """
    @batched(
        batch_kwarg="r_src",
        arg_position=2,
        out_dim_batch=0,
        default_batch_size=1024,
        title="batched Green's tensor calculation",
    )
    def _eval_Gii(sim, wavelength, r_src, r_geo, r_prb, K, alpha):
        # dyads: source -> structure
        Q = sim.environment.get_G_6x6(
            r_geo.unsqueeze(0), r_src.unsqueeze(1), wavelength
        )

        # dyads: structure -> probe
        S = sim.environment.get_G_6x6(
            r_prb.unsqueeze(0), r_geo.unsqueeze(1), wavelength
        )
        
        # dyads: source -> probe
        D = sim.environment.get_G_6x6(
            r_prb.unsqueeze(0), r_src.unsqueeze(1), wavelength
        )

        # alpha dot K
        K_NxN = _reduce_dimensions(K)
        alpha_K_NxN = torch.matmul(alpha, K_NxN)
        aK = _expand_dimensions(alpha_K_NxN, N=6)

        # calculate double integral of tensor products:
        # sum_j sum_k (Q_nj * ((alpha_j * K_jk) * S_kn))
        aKS = torch.einsum("jkab, kmbc -> jmac", [aK, S])
        tg.tools.misc._purge_mem(aK)
        QaKS = torch.einsum("mjab, jnbc -> mnca", [Q, aKS])
        tg.tools.misc._purge_mem(aKS)

        return QaKS + D

    # - prep
    if wavelength is None:
        raise ValueError("Wavelength not given. Needs to be defined.")

    if type(r_probe) == dict:
        r_prb = r_probe["r_probe"]
    else:
        r_prb = r_probe

    r_prb = torch.as_tensor(r_prb, dtype=DTYPE_FLOAT, device=sim.device)
    r_src = torch.as_tensor(r_source, dtype=DTYPE_FLOAT, device=sim.device)

    if len(r_prb.shape) == 1:
        r_prb = r_prb.unsqueeze(0)
    if len(r_src.shape) == 1:
        r_src = r_src.unsqueeze(0)

    r_geo = sim.get_all_positions()

    # - evaluate and integrate Q.alpha.K.S
    # --- dyads
    # TODO: memory efficiency
    #   - use polarizable positions only
    #   - Q and S as reduced coupling matrices

    # polarizabilities (mesh-dipoles, eff. dp-pairs and GPMs)
    all_alpha = []
    for s in sim.structures:
        all_alpha += list(
            s.get_polarizability_6x6(wavelength, sim.environment).unbind()
        )
    alpha = torch.block_diag(*all_alpha)

    # Note: this is not memory / computational efficient!
    full_linsys = tg.linearsystem.LinearSystemFullInverse(device=sim.device)
    K_red = full_linsys.get_generalized_propagator(sim, wavelength=wavelength)
    K = _expand_dimensions(K_red, N=6)
    tg.tools.misc._purge_mem(K_red)

    G = _eval_Gii(
        sim,
        wavelength,
        r_src=r_src,
        r_geo=r_geo,
        r_prb=r_prb,
        K=K,
        alpha=alpha,
        progress_bar=progress_bar,
        **kwargs,
    )
    
    return G


# %% testing
if __name__ == "__main__":
    # %% TODO:
    # tests for Green's tensor vs vacuum in absence of structure
    # test for Green's tensor reciprocity
    # test for Green's tensor vs LDOS (for same result)

    import matplotlib.pyplot as plt

    device = "cpu"
    device = "cuda"

    # --- setup test case simulation
    # - illumination field(s)
    wavelengths = torch.tensor([550.0])

    # - environment
    eps_env = 1.0
    mat_env = tg.materials.MatConstant(eps_env)
    env = tg.env.freespace_3d.EnvHomogeneous3D(env_material=mat_env)

    # - dummy illumination field
    e_inc_dummy = tg.env.freespace_3d.NullField()

    # - first structure: volume discretization
    l = 20
    w = 10
    h = 5
    step = 20.0
    l = w = h = 7
    step = 22.0
    mat_struct = tg.materials.MatConstant(eps=14.0)

    struct_mesh = tg.struct3d.StructDiscretizedCubic3D(
        tg.struct3d.cuboid(l, w, h), step, mat_struct
    )
    struct_mesh.set_center_of_mass([0, 0, 0])
    # struct_mesh += [100000, 100000, -400]
    struct_mesh.plot()

    # - full simulation
    sim = tg.simulation.Simulation(
        structures=[struct_mesh],
        environment=env,
        illumination_fields=[e_inc_dummy],
        wavelengths=wavelengths,
        device=device,
    )

    print("nr of dipoles: {}".format(len(sim.get_all_positions())))

    wavelength = wavelengths[0]
    r_source = [0, 0, 200]
    r_source = [[-220, 0, 0], [50, 0, 200]]
    r_probe = [[0, 0, 200], [100, 200, 300]]
    r_probe = [[100, 20, 200]]

    r_probe = tg.tools.geometry.coordinate_map_2d_square(500, 100, r3=100)
    # r_source = r_probe

    # r_probe = None

    G_results = G(
        sim,
        wavelength=wavelength,
        r_probe=r_probe,
        r_source=r_source,
        progress_bar=True,
    )

    G_6x6 = G_results["G_6x6"]
    G_Ep = G_results["G_Ep"]
    G_Hm = G_results["G_Hm"]

    tg.visu.visu2d.scalar2d._scalarfield(
        field_scalars=G_Ep[0, :, 0, 0].real, positions=r_probe["r_probe"]
    )  # %%
    # %% LDOS test
    # G_selfEp = G_Ep[torch.arange(G_Ep.shape[0]), torch.arange(G_Ep.shape[1]), ...]
    # G_selfHm = G_Hm[torch.arange(G_Hm.shape[0]), torch.arange(G_Hm.shape[1]), ...]

    # plt.subplot(121)
    # im = tg.visu.visu2d.scalar2d._scalarfield(
    #     field_scalars=G_selfEp[:, 1, 1].imag, positions=r_probe["r_probe"], cmap="jet"
    # )
    # plt.colorbar(im)
    # plt.subplot(122)
    # im = tg.visu.visu2d.scalar2d._scalarfield(
    #     field_scalars=G_selfHm[:, 1, 1].imag, positions=r_probe["r_probe"], cmap="jet"
    # )
    # plt.colorbar(im)
    # plt.show()

    # # %%
    # # G = G.reshape(len(r_probe), len(r_source), 3,3)
    # # G = torch.moveaxis(G, 2, 3)
    # # print(G)
    # torch.set_printoptions(precision=3, linewidth=150)

    # print(G_Ep.shape)
    # G_self = G_Ep[torch.arange(G_Ep.shape[0]), torch.arange(G_Ep.shape[1]), ...]
    # print(G_self.shape)

    # r_source = torch.as_tensor(r_source)
    # r_probe = torch.as_tensor(r_probe)
    # G_vac = env.get_G_Ep(r_probe, r_source, wavelength)
    # G_vac_6x6 = env.get_G_6x6(r_probe, r_source, wavelength)
    # print(G_vac_6x6.shape)

    # # test if vacuum solution is indentical
    # print(G_6x6[0, 0])
    # print(G_vac_6x6[0])
    # torch.testing.assert_close(G_6x6[0, 0], G_vac_6x6[0], rtol=1e-9, atol=1e-9)
