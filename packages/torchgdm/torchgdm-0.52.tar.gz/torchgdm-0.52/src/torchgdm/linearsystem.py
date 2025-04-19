# -*- coding: utf-8 -*-
"""
handling of linear equation systems (coupling)
"""
# %%
from collections.abc import Callable
import time
import warnings

import torch

from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX
from torchgdm.tools.misc import _purge_mem, get_default_device
from torchgdm.tools.batch import batched


def _reduce_dimensions(Q: torch.Tensor):
    """expand dimensions of Q from (A1, A2, N, N) to (A1*N, A2*N)

    Args:
        Q (torch.Tensor): 4D tensor of shape (A1, A2, N, N), containing an array of (N, N) tensors

    Returns:
        torch.Tensor: tensor of shape (A1*N, A2*N) with conserved global structure of Q
    """
    Q_red = Q.permute(0, 2, 1, 3)
    dim_Q1 = Q_red.shape[0] * Q_red.shape[1]
    dim_Q2 = Q_red.shape[2] * Q_red.shape[3]

    # note: this is not memory efficient as it copies the full matrix...
    Q_red = Q_red.contiguous().view(dim_Q1, dim_Q2)
    return Q_red


def _expand_dimensions(Q: torch.Tensor, N: int = 6):
    """expand dimensions of Q from (A1*N, A2*N) to (A1, A2, N, N)

    Args:
        Q (torch.Tensor): 4D tensor of shape (A1, A2, N, N), containing an array of (N, N) tensors
        N (int): size of rank 2 sub-tensors. Defaults to 6

    Returns:
        torch.Tensor: tensor of shape (A1, A2, N, N) with conserved global structure of Q
    """
    dim_Q1 = Q.shape[0] // N
    dim_Q2 = Q.shape[1] // N

    # note: this is not memory efficient as it copies the full matrix...
    Q_exp = Q.contiguous().view(dim_Q1, N, dim_Q2, N)
    Q_exp = Q_exp.permute(0, 2, 1, 3)

    return Q_exp


@batched("f0")
def _batched_lu_solve(LU, pivots, f0=None):
    if f0 is None:
        raise ValueError("'f0' must be given.")
    return torch.linalg.lu_solve(LU, pivots, f0)


# --- linear system base class
class LinearSystemBase:
    """torchgdm base class for linearsystem, describing and solving the coupling"""

    __name__ = "linearsystem base class"

    def __init__(self, device: torch.device = None):
        if device is None:
            self.device = get_default_device()
        else:
            self.device = device

    def set_device(self, device):
        """move all tensors of the class to device"""
        self.device = device

    def solve(self):
        """solve coupling for illumination(s)"""
        raise NotImplementedError("`solve` not implemented with this linear system.")

    def get_generalized_propagator(self):
        """get the generalized propagator"""
        raise NotImplementedError(
            "Generalized propoagator not available with this linear system."
        )


class LinearSystemFullInverse(LinearSystemBase):
    """Solve coupling by full inversion

    This linear system solver class is a reference implementation using full 6x6 coupling at
    every position, even if not all polarizability tensor components are required.
    In cases containing full volume discretization structures, this is not memory and compute efficient .
    """

    def __init__(self, device: torch.device = None):
        """Solve coupling by full inversion

        Args:
            device (torch.device, optional): Defaults to "cpu" (can be changed by :func:`torchgdm.use_cuda`).
        """
        super().__init__(device=device)

    def set_device(self, device):
        """move all tensors of the class to device"""
        super().set_device(device)

    # --- functions to setup interaction systems
    def _get_full_interaction_matrix_G_tensors(
        self, positions: torch.Tensor, G_func: Callable, wavelength: float
    ) -> torch.Tensor:
        # evaluate Green's tensors for each couple of points
        # iteract_G_NxN is of shape (N,N,6,6)
        interact_G_NxN = G_func(
            positions.unsqueeze(1),
            positions.unsqueeze(0),
            wavelength=wavelength,
        )
        return interact_G_NxN

    def _get_full_Gdotalpha(
        self,
        sim,
        G_func: Callable,
        wavelength: float,
    ) -> torch.Tensor:
        """calc. interaction matrix $(G.alpha)$, selfterms on diagonal"""

        all_alpha = []
        for s in sim.structures:
            all_alpha += list(
                s.get_polarizability_6x6(wavelength, sim.environment).unbind()
            )
        block_pola = torch.block_diag(*all_alpha)

        all_selfterms = []
        for s in sim.structures:
            all_selfterms += list(
                s.get_selfterm_6x6(wavelength, sim.environment).unbind()
            )
        block_selfterms = torch.block_diag(*all_selfterms)

        # GPM: non-local coupling already solved. Set G to zero
        # Note:  In non-homogeneous env, GPM dipoles may couple
        # through environemnt. Then, need to subtract only G0 here
        ones_gpm = torch.block_diag(
            *[torch.ones_like(s.real).to(torch.int) for s in all_alpha]
        )

        interact_NxNx6x6 = self._get_full_interaction_matrix_G_tensors(
            sim.get_all_positions(), G_func, wavelength
        )
        interact_NxN = _reduce_dimensions(interact_NxNx6x6)
        interact_NxN = interact_NxN.masked_fill(ones_gpm == 1, 0)
        interact_NxN += block_selfterms

        G_dot_interact = torch.matmul(interact_NxN, block_pola)

        return G_dot_interact

    def get_interact(self, sim_gpm, wavelength: float) -> torch.Tensor:
        """get the full interaction block (E, H) of the linear system for a list of structures

        containes all direct and cross-contributions (E-E, H-H, E-H, H-E)
        """
        # calc. interactions (G dot GPM)
        interact = self._get_full_Gdotalpha(
            sim=sim_gpm,
            G_func=sim_gpm.environment.get_G_6x6,
            wavelength=wavelength,
        )

        # invertible matrix block is (1 - G.alpha), which adds the illumination field
        interact = torch.eye(len(interact), device=self.device) - interact

        return interact

    def solve(
        self,
        sim,
        wavelength: float,
        batch_size=32,
        verbose: int = 1,
    ) -> torch.Tensor:
        """solve system of coupled structures for all illuminations

        Args:
            sim (SimulationBase): simulation container
            wavelength (float): wavelength (nm)
            batch_size (int, optional): Nr of incident fields evaluated in parallel. Defaults to 32.
            verbose (int, optional): wether to print status info. Defaults to 1.

        Returns:
            torch.Tensor: list of internal fields, one for each illumination. Shape: (N_e0, nr of pos, 3)
        """
        if verbose >= 2:
            t_start = time.time()
            print("linsys", end="")

        # - setup interaction system
        interact = self.get_interact(sim, wavelength)
        if verbose >= 2:
            t_interact = time.time()
            print(" {:.2f}s. solve".format(t_interact - t_start), end="")

        # - inversion
        # LU, pivots, info = torch.linalg.lu_factor_ex(interact)  # experimental version, faster on GPU
        LU, pivots = torch.linalg.lu_factor(interact)
        if verbose >= 2:
            t_lu = time.time()
            print(
                " {:.2f}s. {}xE0".format(
                    t_lu - t_interact, len(sim.illumination_fields)
                ),
                end="",
            )

        # - evaluate zero order fields
        f0 = sim._get_all_e0_h0(wavelength)
        f0 = f0.view(len(f0), -1, 1)

        # - solve for RHS vectors
        f_inside = _batched_lu_solve(LU, pivots, f0=f0, batch_size=batch_size)
        eh_inside = f_inside.view(len(f_inside), -1, 6)  # conv 6N to N 6-tuples (E,H)
        e_inside, h_inside = torch.chunk(eh_inside, 2, dim=2)  # separate E and H fields

        if verbose >= 2:
            t_solve = time.time()
            print(" {:.2f}s.".format(t_solve - t_lu), end="")

        return e_inside, h_inside

    def get_generalized_propagator(self, sim, wavelength: float) -> torch.Tensor:
        interact = self.get_interact(sim, wavelength)
        K = torch.linalg.inv(interact)
        return K


class LinearSystemFullMemEff(LinearSystemFullInverse):
    """Solve coupling by full inversion

    This linear system solver couples only actually polarizable terms.
    """

    def __init__(self, device: torch.device = None):
        """Solve coupling by full inversion

        This linear system solver couples only actually polarizable terms.

        Args:
            device (torch.device, optional): Defaults to "cpu" (can be changed by :func:`torchgdm.use_cuda`).
        """
        super().__init__(device=device)

    def set_device(self, device):
        """move all tensors of the class to device"""
        super().set_device(device)

    # --- select proper coupling for structure pair
    def get_struct_pair_coupling_config(
        self,
        struct1,
        struct2,
        sim,
        verbose=False,
    ):
        """get evaluation functions for required coupling between two structures

        Concerns Greens tensor, polarizability and self-term evaluation

        Args:
            struct1 (structBase): target of scattered light
            struct2 (structBase): origin of light scattering
            sim (SimulationBase): simulation descriptor

        Returns:
            callable: Green's tensor calculation function
            callable: polarizability calculation function
            callable: self-term evaluator, only returned for equal coupling of st1 and st2. default: None
        """

        _s1T = struct1.interaction_type  # observer structure (target)
        _s2T = struct2.interaction_type  # emitter structure (origin)
        selfterm_func = (
            None  # default: two different structures --> no self-terms required
        )

        # --- electric-only observer and source
        # e <- e
        if _s1T == "E" and _s2T == "E":
            G_func = sim.environment.get_G_Ep
            alpha_func = struct2.get_polarizability_pE
            selfterm_func = struct2.get_selfterm_pE

        # --- mixed observer, electric-only source
        # e,m <- e
        elif _s1T == "EH" and _s2T == "E":
            G_func = sim.environment.get_G_6x6
            alpha_func = struct2.get_polarizability_pmE_6x3

        # --- electric-only observer, mixed source
        # e <- e,m
        elif _s1T == "E" and _s2T == "EH":
            G_func = sim.environment.get_G_Epm_3x6
            alpha_func = struct2.get_polarizability_6x6

        # --- full coupling case
        # e,m <- e,m
        else:
            G_func = sim.environment.get_G_6x6
            alpha_func = struct2.get_polarizability_6x6
            selfterm_func = struct2.get_selfterm_6x6

        return G_func, alpha_func, selfterm_func

    # --- functions to setup interaction systems
    def _get_block_Gdotalpha(
        self,
        struct1: torch.Tensor,
        struct2: torch.Tensor,
        sim,
        wavelength: float,
    ) -> torch.Tensor:
        """calc. invertible interaction matrix $(G.alpha)$. selfterms on diagonal

        consider light scattering from source (struct2) to target (struct1)
        """
        # process selfterms and polarizabilities
        G_func, alpha_func, selfterm_func = self.get_struct_pair_coupling_config(
            struct1, struct2, sim
        )

        # all polarizabilities
        all_pola = list(alpha_func(wavelength, sim.environment).unbind())
        block_pola = torch.block_diag(*all_pola)
        ones_gpm = torch.block_diag(
            *[torch.ones_like(s.real).to(torch.int) for s in all_pola]
        )

        # Green's tensors form s2 to s1. shape (N1,N2,6,6)
        interact_N1xN2x6x6 = G_func(
            struct1.get_all_positions().unsqueeze(1),  # light targets
            struct2.get_all_positions().unsqueeze(0),  # light sources
            wavelength=wavelength,
        )
        interact_N1xN2 = _reduce_dimensions(interact_N1xN2x6x6)

        # self-terms
        if struct1 == struct2:
            all_selfterms = list(selfterm_func(wavelength, sim.environment).unbind())
            block_selfterms = torch.block_diag(*all_selfterms)

            # fill GPMs (nonlocal polas, coupling already solved)
            interact_N1xN2 = interact_N1xN2.masked_fill(ones_gpm == 1, 0)
            interact_N1xN2 += block_selfterms

        G_dot_interact = torch.matmul(interact_N1xN2, block_pola)

        return G_dot_interact

    def get_interact(self, sim, wavelength: float, verbose=False) -> torch.Tensor:
        """get the full interaction block (E, H) of the linear system for a list of structures

        containes all direct and cross-contributions (E-E, H-H, E-H, H-E)

        Note: This implementation is not efficient for large numbers of structures.
        TODO: combine all structures of same interaction type before doing the simulation
        """
        from torchgdm.tools.misc import tqdm

        prgbar = True if verbose >= 3 else False

        # combine consecutive structures of same coupling type to reduce
        # memory transfer cost during iteration of all structures
        struct_list_reduced = [sim.structures[0]]
        if len(sim.structures) > 1:
            for _s in tqdm(
                sim.structures[1:], progress_bar=prgbar, title="optimizing structures"
            ):
                if _s.interaction_type == struct_list_reduced[-1].interaction_type:
                    try:
                        struct_list_reduced[-1] = struct_list_reduced[-1].combine(_s)
                    except:
                        # if combine fails, add as separate structure
                        struct_list_reduced.append(_s)
                else:
                    # if different coupling type, add as separate structure
                    struct_list_reduced.append(_s)

        if len(struct_list_reduced) > 10:
            warnings.warn(
                "Structure list could not be fully optimized. "
                + "For optimal performance, add structures with same "
                + "mesh or same coupling type in consecutive groups."
            )

        # calc. G dot alpha
        interact_rows = []
        for struct2 in tqdm(
            struct_list_reduced, progress_bar=prgbar, title="interaction matrix"
        ):
            interact_cols = []
            for struct1 in struct_list_reduced:
                # interaction block for struct2 (emitter) --> struct1 (observer)
                interact_expand = self._get_block_Gdotalpha(
                    struct1=struct1,
                    struct2=struct2,
                    sim=sim,
                    wavelength=wavelength,
                )
                interact_cols.append(interact_expand)
            interact_rows.append(torch.cat(interact_cols, dim=0))
        interact_full = torch.cat(interact_rows, dim=1)

        # free (GPU-)RAM
        _purge_mem(interact_rows)

        # invertible matrix block is (1 - G.alpha): add the illumination field to output
        interact_full = (
            torch.eye(len(interact_full), device=self.device) - interact_full
        )

        return interact_full

    # --- field mask operations
    def _zero_fill_nonpolarizable_fields(
        self, sim, field_at_polarizable: torch.Tensor
    ) -> torch.Tensor:
        """create full field tensor with polarizable fields inserted.

        Args:
            sim (`torchgdm.Simulation`): simulation instance
            field_at_polarizable (torch.Tensor): field values to be inserted at polarizable positions

        Returns:
            torch.Tensor: full field tensor at all meshpoints with masked regions inserted
        """
        # init full internal e/h field tensor (N_inc, N_pos, 6)
        fields_full = torch.zeros(
            (len(sim.illumination_fields), len(sim.get_all_positions()), 6),
            dtype=DTYPE_COMPLEX,
            device=self.device,
        )

        # get polarizable positions mask for field tensor
        mask_fields = sim._get_polarizable_mask_full_fields()

        # insert field elements at polarizable positions into masked full field tensor
        fields_full.flatten()[mask_fields.flatten()] = field_at_polarizable.flatten()

        return fields_full

    def solve(
        self,
        sim,
        wavelength: float,
        batch_size=32,
        verbose: int = 1,
    ) -> torch.Tensor:
        """solve system of coupled structures for all illuminations

        Args:
            sim (`torchgdm.Simulation`): simulation instance
            wavelength (float): wavelength (nm)
            batch_size (int, optional): Nr of incident fields evaluated in parallel. Defaults to 32.
            verbose (int, optional): verbose level of status reporting. One of [0,1,2]. The higher, the more info are printed. Defaults to 1.

        Returns:
            torch.Tensor: list of internal fields, one for each illumination. Shape: (N_e0, nr of pos, 3)
        """
        if verbose >= 2:
            t_start = time.time()
            print("linsys", end="")

        # - setup interaction system
        interact = self.get_interact(sim, wavelength, verbose=verbose)
        if verbose >= 2:
            t_interact = time.time()
            print(" {:.2f}s. solve".format(t_interact - t_start), end="")

        # - inversion
        # LU, pivots, info = torch.linalg.lu_factor_ex(interact)  # experimental version, faster on GPU
        LU, pivots = torch.linalg.lu_factor(interact)
        if verbose >= 2:
            t_lu = time.time()
            print(
                " {:.2f}s. {}xE0".format(
                    t_lu - t_interact, len(sim.illumination_fields)
                ),
                end="",
            )

        # - evaluate zero order fields (illumination)
        f0 = sim._get_polarizablefields_e0_h0(wavelength)
        f0 = f0.view(len(f0), -1, 1)  # add dim for lu_solve

        # - solve for RHS vectors
        f_masked = _batched_lu_solve(LU, pivots, f0=f0, batch_size=batch_size)
        eh_inside = self._zero_fill_nonpolarizable_fields(sim, f_masked[..., 0])
        e_inside, h_inside = torch.chunk(eh_inside, 2, dim=2)  # separate E and H fields

        if verbose >= 2:
            t_solve = time.time()
            print(" {:.2f}s.".format(t_solve - t_lu), end="")

        return e_inside, h_inside

    def get_generalized_propagator(self, sim, wavelength: float) -> torch.Tensor:
        """solve system of coupled structures without illumination

        Args:
            sim (`torchgdm.Simulation`): simulation instance
            wavelength (float): wavelength (nm)

        Returns:
            torch.Tensor: full generalized propagator tensor for all polarizable elements
        """
        interact = self.get_interact(sim, wavelength)
        K = torch.linalg.inv(interact)
        return K


## --- legacy
# - Deprecated!
class _LinearSystemFullInverse(LinearSystemBase):
    """Solve coupling by full inversion

    This linear system solver class is a non-optimized reference implementation for testing.
    It uses (6x6) polarizabilities for all dipoles, which is non memory efficient in most cases.
    """

    def __init__(self, device: torch.device = None):
        """Solve coupling by full inversion

        Memory-inefficient test implementation. Uses 6x6 polarizabilities for every positio.

        Args:
            device (torch.device, optional): Defaults to "cpu" (can be changed by :func:`torchgdm.use_cuda`).
        """
        super().__init__(device=device)
        warnings.warn(
            "This class is deprecated and will be removed in the future. "
            + "Use `LinearSystemFullInverse` instead.",
            DeprecationWarning,
        )

    def set_device(self, device):
        """move all tensors of the class to device"""
        super().set_device(device)

    # --- functions to setup interaction systems
    def _get_full_interaction_matrix_G_tensors(
        self, positions: torch.Tensor, G_func: Callable, wavelength: float
    ) -> torch.Tensor:
        # evaluate Green's tensors for each couple of points
        # iteract_G_NxN is of shape (N,N,3,3)
        interact_G_NxN = G_func(
            positions.unsqueeze(1),
            positions.unsqueeze(0),
            wavelength=wavelength,
        )
        return interact_G_NxN

    def _get_full_Gdotalpha(
        self,
        positions: torch.Tensor,
        polarizabilities: torch.Tensor,
        self_terms: torch.Tensor,
        G_func: Callable,
        wavelength: float,
    ) -> torch.Tensor:
        """calc. invertible interaction matrix $(G.alpha)$, selfterms on diagonal"""
        N = len(positions)

        interact_NxN = self._get_full_interaction_matrix_G_tensors(
            positions, G_func, wavelength
        )

        # put self-term matrices on diagonal (at R1[i]==R2[i])
        eye_indices = torch.arange(N, device=self.device)
        interact_NxN[eye_indices, eye_indices, :, :] = self_terms.unsqueeze(0)

        # multiply by polarizabilities
        interact_NxN = torch.matmul(interact_NxN, polarizabilities.unsqueeze(0))

        # reshape (N,N,6,6) to (6N, 6N) matrix (or (3N,3N) if electric-only)
        interact_6Nx6N = _reduce_dimensions(interact_NxN)

        return interact_6Nx6N

    def get_interact(self, sim, wavelength: float) -> torch.Tensor:
        """get the full interaction block (E, H) of the linear system for a list of structures

        containes all direct and cross-contributions (E-E, H-H, E-H, H-E)
        """
        # calc. interactions (G.alpha)
        all_positions = sim.get_all_positions()

        interact = self._get_full_Gdotalpha(
            positions=all_positions,
            polarizabilities=sim._get_all_polarizabilitites_6x6(wavelength),
            self_terms=sim._get_all_selfterms_6x6(wavelength),
            G_func=sim.environment.get_G_6x6,
            wavelength=wavelength,
        )

        # invertible matrix block is (1 - G.alpha), which adds the illumination field
        interact = torch.eye(len(interact), device=self.device) - interact

        return interact

    def solve(
        self,
        sim,
        wavelength: float,
        batch_size=32,
        verbose: int = 1,
    ) -> torch.Tensor:
        """solve system of coupled structures for all illuminations

        Args:
            sim (SimulationBase): simulation container
            wavelength (float): wavelength (nm)
            batch_size (int, optional): Nr of incident fields evaluated in parallel. Defaults to 32.
            verbose (int, optional): wether to print status info. Defaults to 1.

        Returns:
            torch.Tensor: list of internal fields, one for each illumination. Shape: (N_e0, nr of pos, 3)
        """
        if verbose >= 2:
            t_start = time.time()
            print("linsys", end="")

        # - setup interaction system
        interact = self.get_interact(sim, wavelength)
        if verbose >= 2:
            t_interact = time.time()
            print(" {:.2f}s. solve".format(t_interact - t_start), end="")

        # - inversion
        # LU, pivots, info = torch.linalg.lu_factor_ex(interact)  # experimental version, faster on GPU
        LU, pivots = torch.linalg.lu_factor(interact)
        if verbose >= 2:
            t_lu = time.time()
            print(
                " {:.2f}s. {}xE0".format(
                    t_lu - t_interact, len(sim.illumination_fields)
                ),
                end="",
            )

        # - evaluate zero order fields
        f0 = sim._get_all_e0_h0(wavelength)
        f0 = f0.view(len(f0), -1, 1)

        # - solve for RHS vectors
        f_inside = _batched_lu_solve(LU, pivots, f0=f0, batch_size=batch_size)
        eh_inside = f_inside.view(len(f_inside), -1, 6)  # conv 6N to N 6-tuples (E,H)
        e_inside, h_inside = torch.chunk(eh_inside, 2, dim=2)  # separate E and H fields

        if verbose >= 2:
            t_solve = time.time()
            print(" {:.2f}s.".format(t_solve - t_lu), end="")

        return e_inside, h_inside

    def get_generalized_propagator(self, sim, wavelength: float) -> torch.Tensor:
        interact = self.get_interact(sim, wavelength)
        K = torch.linalg.inv(interact)
        return K


# deprecated!
class _LinearSystemFullMemEffnoGPM(LinearSystemFullInverse):
    """Solve coupling by full inversion

    This linear system solver couples only actually polarizable terms.
    """

    def __init__(self, device: torch.device = None):
        """Solve coupling by full inversion

        This linear system solver couples only actually polarizable terms.

        Args:
            device (torch.device, optional): Defaults to "cpu" (can be changed by :func:`torchgdm.use_cuda`).
        """
        super().__init__(device=device)
        warnings.warn(
            "This class is deprecated and will be removed in the future. "
            + "Use `LinearSystemFullMemEff` instead.",
            DeprecationWarning,
        )

    def set_device(self, device):
        """move all tensors of the class to device"""
        super().set_device(device)

    # --- select proper coupling for structure pair
    def get_struct_pair_coupling_config(
        self,
        struct1,
        struct2,
        sim,
        verbose=False,
    ):
        """get evaluation functions for required coupling between two structures

        Concerns Greens tensor, polarizability and self-term evaluation

        Args:
            struct1 (structBase): target of scattered light
            struct2 (structBase): origin of light scattering
            sim (SimulationBase): simulation descriptor

        Returns:
            callable: Green's tensor calculation function
            callable: polarizability calculation function
            callable: self-term evaluator, only returned for equal coupling of st1 and st2. default: None
        """

        _s1T = struct1.interaction_type  # observer structure (target)
        _s2T = struct2.interaction_type  # emitter structure (origin)
        selfterm_func = (
            None  # default: two different structures --> no self-terms required
        )

        # --- electric-only observer and source
        # e <- e
        if _s1T == "E" and _s2T == "E":
            G_func = sim.environment.get_G_Ep
            alpha_func = struct2.get_polarizability_pE
            selfterm_func = struct2.get_selfterm_pE

        # --- mixed observer, electric-only source
        # e,m <- e
        elif _s1T == "EH" and _s2T == "E":
            G_func = sim.environment.get_G_6x6
            alpha_func = struct2.get_polarizability_pmE_6x3

        # --- electric-only observer, mixed source
        # e <- e,m
        elif _s1T == "E" and _s2T == "EH":
            G_func = sim.environment.get_G_Epm_3x6
            alpha_func = struct2.get_polarizability_6x6

        # --- full coupling case
        # e,m <- e,m
        else:
            G_func = sim.environment.get_G_6x6
            alpha_func = struct2.get_polarizability_6x6
            selfterm_func = struct2.get_selfterm_6x6

        return G_func, alpha_func, selfterm_func

    # --- functions to setup interaction systems
    def _get_block_Gdotalpha(
        self,
        struct1: torch.Tensor,
        struct2: torch.Tensor,
        sim,
        wavelength: float,
    ) -> torch.Tensor:
        """calc. invertible interaction matrix $(G.alpha)$. selfterms on diagonal"""

        # process selfterms and polarizabilities
        G_func, alpha_func, selfterm_func = self.get_struct_pair_coupling_config(
            struct1, struct2, sim
        )

        # eval. Greens tensors between struct2 (emitter) and struct1 (observer)
        gdotalpha = G_func(
            struct1.get_all_positions().unsqueeze(1),  # light targets
            struct2.get_all_positions().unsqueeze(0),  # light sources
            wavelength=wavelength,
        )

        # if struct1 == struct2: put self-terms on diagonal (at R1[i]==R2[i])
        if struct1 == struct2:
            self_terms = selfterm_func(wavelength, sim.environment)

            N = len(struct1.get_all_positions())
            eye_idx = torch.arange(N, device=self.device)
            gdotalpha[eye_idx, eye_idx, :, :] = self_terms.unsqueeze(0)

        # multiply by polarizabilities
        polarizabilities = alpha_func(wavelength, sim.environment)
        gdotalpha = torch.matmul(gdotalpha, polarizabilities.unsqueeze(0))

        # reshape (N1,N2,6,6) to (6xN1, 6xN2) matrix (or (3,3), (6,3), (3,6) if not full coupling)
        gdotalpha_expanded = _reduce_dimensions(gdotalpha)

        return gdotalpha_expanded

    def get_interact(self, sim, wavelength: float, verbose=False) -> torch.Tensor:
        """get the full interaction block (E, H) of the linear system for a list of structures

        containes all direct and cross-contributions (E-E, H-H, E-H, H-E)

        Note: This implementation is not efficient for large numbers of structures.
        TODO: combine all structures of same interaction type before doing the simulation
        """
        from torchgdm.tools.misc import tqdm

        prgbar = True if verbose >= 3 else False

        # combine consecutive structures of same coupling type to reduce
        # memory transfer cost during iteration of all structures
        struct_list_reduced = [sim.structures[0]]
        if len(sim.structures) > 1:
            for _s in tqdm(
                sim.structures[1:], progress_bar=prgbar, title="optimizing structures"
            ):
                if _s.interaction_type == struct_list_reduced[-1].interaction_type:
                    try:
                        struct_list_reduced[-1] = struct_list_reduced[-1].combine(_s)
                    except:
                        # if combine fails, add as separate structure
                        struct_list_reduced.append(_s)
                else:
                    # if different coupling type, add as separate structure
                    struct_list_reduced.append(_s)

        if len(struct_list_reduced) > 10:
            warnings.warn(
                "Structure list could not be fully optimized. "
                + "For optimal performance, add structures with same "
                + "mesh or same coupling type in consecutive groups."
            )

        # calc. G dot alpha
        interact_rows = []
        for struct2 in tqdm(
            struct_list_reduced, progress_bar=prgbar, title="interaction matrix"
        ):
            interact_cols = []
            for struct1 in struct_list_reduced:
                # interaction block for struct2 (emitter) --> struct1 (observer)
                interact_expand = self._get_block_Gdotalpha(
                    struct1=struct1,
                    struct2=struct2,
                    sim=sim,
                    wavelength=wavelength,
                )
                interact_cols.append(interact_expand)
            interact_rows.append(torch.cat(interact_cols, dim=0))
        interact_full = torch.cat(interact_rows, dim=1)

        # free (GPU-)RAM
        _purge_mem(interact_rows)

        # invertible matrix block is (1 - G.alpha): add the illumination field to output
        interact_full = (
            torch.eye(len(interact_full), device=self.device) - interact_full
        )

        return interact_full

    # --- field mask operations
    def _zero_fill_nonpolarizable_fields(
        self, sim, field_at_polarizable: torch.Tensor
    ) -> torch.Tensor:
        """create full field tensor with polarizable fields inserted.

        Args:
            sim (`torchgdm.Simulation`): simulation instance
            field_at_polarizable (torch.Tensor): field values to be inserted at polarizable positions

        Returns:
            torch.Tensor: full field tensor at all meshpoints with masked regions inserted
        """
        # init full internal e/h field tensor (N_inc, N_pos, 6)
        fields_full = torch.zeros(
            (len(sim.illumination_fields), len(sim.get_all_positions()), 6),
            dtype=DTYPE_COMPLEX,
            device=self.device,
        )

        # get polarizable positions mask for field tensor
        mask_fields = sim._get_polarizable_mask_full_fields()

        # insert field elements at polarizable positions into masked full field tensor
        fields_full.flatten()[mask_fields.flatten()] = field_at_polarizable.flatten()

        return fields_full

    def solve(
        self,
        sim,
        wavelength: float,
        batch_size=32,
        verbose: int = 1,
    ) -> torch.Tensor:
        """solve system of coupled structures for all illuminations

        Args:
            sim (`torchgdm.Simulation`): simulation instance
            wavelength (float): wavelength (nm)
            batch_size (int, optional): Nr of incident fields evaluated in parallel. Defaults to 32.
            verbose (int, optional): verbose level of status reporting. One of [0,1,2]. The higher, the more info are printed. Defaults to 1.

        Returns:
            torch.Tensor: list of internal fields, one for each illumination. Shape: (N_e0, nr of pos, 3)
        """
        if verbose >= 2:
            t_start = time.time()
            print("linsys", end="")

        # - setup interaction system
        interact = self.get_interact(sim, wavelength, verbose=verbose)
        if verbose >= 2:
            t_interact = time.time()
            print(" {:.2f}s. solve".format(t_interact - t_start), end="")

        # - inversion
        # LU, pivots, info = torch.linalg.lu_factor_ex(interact)  # experimental version, faster on GPU
        LU, pivots = torch.linalg.lu_factor(interact)
        if verbose >= 2:
            t_lu = time.time()
            print(
                " {:.2f}s. {}xE0".format(
                    t_lu - t_interact, len(sim.illumination_fields)
                ),
                end="",
            )

        # - evaluate zero order fields (illumination)
        f0 = sim._get_polarizablefields_e0_h0(wavelength)
        f0 = f0.view(len(f0), -1, 1)  # add dim for lu_solve

        # - solve for RHS vectors
        f_masked = _batched_lu_solve(LU, pivots, f0=f0, batch_size=batch_size)
        eh_inside = self._zero_fill_nonpolarizable_fields(sim, f_masked[..., 0])
        e_inside, h_inside = torch.chunk(eh_inside, 2, dim=2)  # separate E and H fields

        if verbose >= 2:
            t_solve = time.time()
            print(" {:.2f}s.".format(t_solve - t_lu), end="")

        return e_inside, h_inside

    def get_generalized_propagator(self, sim, wavelength: float) -> torch.Tensor:
        """solve system of coupled structures without illumination

        Args:
            sim (`torchgdm.Simulation`): simulation instance
            wavelength (float): wavelength (nm)

        Returns:
            torch.Tensor: full generalized propagator tensor for all polarizable elements
        """
        interact = self.get_interact(sim, wavelength)
        K = torch.linalg.inv(interact)
        return K
