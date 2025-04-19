# -*- coding: utf-8 -*-
"""
vectorized pytorch implementations of free space Green's tensors
"""
# %%
import warnings

import numpy as np
import torch

from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX
from torchgdm.tools.misc import get_default_device
from torchgdm.env.base_classes import EnvironmentBase
from torchgdm.tools.misc import _tensor_is_diagonal_and_identical, _test_positional_input


# %%
# --- vectorized pytorch
def G0_Ep(
    r_probe: torch.Tensor,
    r_source: torch.Tensor,
    wavelength: float,
    eps_env: float,
    epsilon_dist: float = 1e-8,  # to avoid divergence at r_probe=r_source
):
    """3D free space electric field (at r_probe) Green's tensor for an electric dipole (at r_source)

    Args:
        r_probe (torch.Tensor): probe position
        r_source (torch.Tensor): source position
        wavelength (float): in nm
        eps_env (float): environment permittivity
        epsilon_dist (float, optional): small distance to avoid divergence at r_probe=r_source. Defaults to 1e-8.

    Returns:
        torch.Tensor: 3D electric-electric Green's Dyad
    """
    r_probe, r_source = _test_positional_input(r_probe, r_source)

    # positional values
    R = r_probe - r_source  # vector difference(s)
    RR = torch.einsum("...i,...j", R, R)  # broadcasted outer product of each vector R
    lR2 = torch.sum(R * R, dim=-1)
    R2diag = torch.eye(3).unsqueeze(0).to(r_probe.device) * lR2.unsqueeze(-1).unsqueeze(
        -1
    )
    lR = torch.sqrt(lR2 + epsilon_dist)

    # wavenumber
    k0 = 2 * torch.pi / wavelength  # vacuum wave number
    k = k0 * torch.sqrt(eps_env)  # k in env. medium
    k_sqrt_eps_lR = k * lR

    # Compute the combined T_EE tensor
    T_combined = (
        -(k**2) * torch.div(RR - R2diag, lR.pow(3).unsqueeze(-1).unsqueeze(-1))  # T1
        - (1j * k)
        * torch.div((3 * RR - R2diag), lR.pow(4).unsqueeze(-1).unsqueeze(-1))  # T2
        + torch.div((3 * RR - R2diag), lR.pow(5).unsqueeze(-1).unsqueeze(-1))  # T3
    )

    # Calculate the phase term and multiply element-wise with T_combined
    sG0 = torch.exp(1j * k_sqrt_eps_lR) / eps_env
    G0 = T_combined * sG0.unsqueeze(-1).unsqueeze(-1)
    return G0


def G0_Hp(
    r_probe: torch.Tensor,
    r_source: torch.Tensor,
    wavelength: float,
    eps_env: float,
    epsilon_dist: float = 1e-8,  # to avoid divergence at r_probe=r_source
) -> torch.Tensor:
    """3D free space magnetic field (at r_probe) Green's tensor for an electric dipole (at r_source)

    Args:
        r_probe (torch.Tensor): probe position
        r_source (torch.Tensor): source position
        wavelength (float): in nm
        eps_env (float): environment permittivity
        epsilon_dist (float, optional): small distance to avoid divergence at r_probe=r_source. Defaults to 1e-8.

    Returns:
        torch.Tensor: 3D electric-electric Green's Dyad
    """
    r_probe, r_source = _test_positional_input(r_probe, r_source)

    # positional values
    R = r_probe - r_source  # vector difference(s)
    Dx = R[..., 0]
    Dy = R[..., 1]
    Dz = R[..., 2]
    lR2 = torch.sum(R**2, dim=-1) + epsilon_dist
    lR = torch.sqrt(lR2)

    # wavenumber
    n_env = torch.sqrt(eps_env)
    k0 = 2 * torch.pi / wavelength
    k02n = k0 * k0 * n_env
    k = n_env * k0
    k_sqrt_eps_lR = k * lR

    # compute the combined T_HE tensor
    T_combined = torch.zeros(
        (*R.size()[:-1], 3, 3), dtype=DTYPE_COMPLEX, device=r_probe.device
    )
    T_combined[..., 0, 1] = 1j * k0 * (Dz / (lR**3)) + k02n * (Dz / lR2)
    T_combined[..., 0, 2] = 1j * k0 * (-Dy / (lR**3)) + k02n * (-Dy / lR2)
    T_combined[..., 1, 2] = 1j * k0 * (Dx / (lR**3)) + k02n * (Dx / lR2)
    T_combined[..., 1, 0] = -T_combined[..., 0, 1]
    T_combined[..., 2, 0] = -T_combined[..., 0, 2]
    T_combined[..., 2, 1] = -T_combined[..., 1, 2]

    # Phase term
    sG0 = -1 * torch.exp(1j * k_sqrt_eps_lR)
    T_combined = T_combined * sG0.unsqueeze(-1).unsqueeze(-1)

    return T_combined


def G0_Em(r_probe, r_source, wavelength, eps_env, epsilon_dist: float = 1e-8):
    """3D free space electric field (at r_probe) Green's tensor for a magnetic dipole (at r_source)

    G0_Em = - G0_Hp

    for doc, see :func:`G0_Hp`
    """
    return -1 * G0_Hp(r_probe, r_source, wavelength, eps_env, epsilon_dist=epsilon_dist)


def G0_Hm(r_probe, r_source, wavelength, eps_env, epsilon_dist: float = 1e-8):
    """3D free space magnetic field (at r_probe) Green's tensor for a magnetic dipole (at r_source)

    G0_Hm = G0_Ep

    for doc, see :func:`G0_Ep`
    """
    return eps_env * G0_Ep(
        r_probe, r_source, wavelength, eps_env, epsilon_dist=epsilon_dist
    )


def G0_Ep_ff(
    r_probe: torch.Tensor,
    r_source: torch.Tensor,
    wavelength: float,
    eps_env: float,
    epsilon_dist: float = 1e-8,  # to avoid divergence at r_probe=r_source
):
    """3D far-field approximation for electric-electric Green's tensor

    Args:
        r_probe (torch.Tensor): probe position
        r_source (torch.Tensor): source position
        wavelength (float): in nm
        eps_env (float): environment permittivity
        epsilon_dist (float, optional): small distance to avoid divergence at r_probe=r_source. Defaults to 1e-8.

    Returns:
        torch.Tensor: 3D electric-electric far-field Green's Dyad
    """
    r_probe, r_source = _test_positional_input(r_probe, r_source)

    # positional values
    R = r_probe - r_source  # vector difference(s)
    RR = torch.einsum("...i,...j", R, R)  # broadcasted outer product of each vector R
    lR2 = torch.sum(R * R, dim=-1)
    R2diag = torch.eye(3).unsqueeze(0).to(r_probe.device) * lR2.unsqueeze(-1).unsqueeze(
        -1
    )
    lR = torch.sqrt(lR2 + epsilon_dist)

    # wavenumber
    k0 = 2 * torch.pi / wavelength  # vacuum wave number
    k = k0 * torch.sqrt(eps_env + epsilon_dist)  # k in env. medium
    k_sqrt_eps_lR = k * lR

    # Compute the combined T_EE tensor
    T_combined = -(k**2) * torch.div(
        RR - R2diag, lR.pow(3).unsqueeze(-1).unsqueeze(-1)
    )  # T1

    # Calculate the phase term and multiply element-wise with T_combined
    sG0 = torch.exp(1j * k_sqrt_eps_lR) / eps_env
    G0 = T_combined * sG0.unsqueeze(-1).unsqueeze(-1)
    return G0


def G0_Em_ff(
    r_probe: torch.Tensor,
    r_source: torch.Tensor,
    wavelength: float,
    eps_env: float,
    epsilon_dist: float = 1e-8,  # to avoid divergence at r_probe=r_source
) -> torch.Tensor:
    """3D far-field approximation for electric-magnetic Green's tensor

    Args:
        r_probe (torch.Tensor): probe position
        r_source (torch.Tensor): source position
        wavelength (float): in nm
        eps_env (float): environment permittivity
        epsilon_dist (float, optional): small distance to avoid divergence at r_probe=r_source. Defaults to 1e-8.

    Returns:
        torch.Tensor: 3D electric-electric far-field Green's Dyad
    """
    r_probe, r_source = _test_positional_input(r_probe, r_source)

    # positional values
    R = r_probe - r_source  # vector difference(s)
    Dx = R[..., 0]
    Dy = R[..., 1]
    Dz = R[..., 2]
    lR2 = torch.sum(R**2, dim=-1) + epsilon_dist
    lR = torch.sqrt(lR2)

    # wavenumber
    k0 = 2 * torch.pi / wavelength
    n_env = torch.sqrt(eps_env)
    k = n_env * k0
    k02n = k0 * k0 * n_env
    k_sqrt_eps_lR = k * lR

    # compute the combined T_HE tensor
    T_combined = torch.zeros(
        (*R.size()[:-1], 3, 3), dtype=DTYPE_COMPLEX, device=r_probe.device
    )
    T_combined[..., 0, 1] = 1j * k02n * (Dz / lR2)
    T_combined[..., 0, 2] = 1j * k02n * (-Dy / lR2)
    T_combined[..., 1, 2] = 1j * k02n * (Dx / lR2)
    T_combined[..., 1, 0] = -T_combined[..., 0, 1]
    T_combined[..., 2, 0] = -T_combined[..., 0, 2]
    T_combined[..., 2, 1] = -T_combined[..., 1, 2]

    # Phase term
    sG0 = -1 * torch.exp(1j * k_sqrt_eps_lR)
    T_combined = T_combined * sG0.unsqueeze(-1).unsqueeze(-1)

    # Em = -1*Hp:
    return -1 * T_combined


# --- environment class
class EnvHomogeneous3D(EnvironmentBase):
    """class defining a homogeneous environment

    - defines set of free-space Green's tensors
    - environemnt material needs to be isotropic (scalar epsilon) and lossless.
    """

    __name__ = "homogeneous environment 3D"

    def __init__(self, env_material=1.0, device: torch.device = None):
        """class defining a homogeneous 3D environment

        Args:
            env_material (float, optional): Environment material. Either float or class from :mod:`torchgdm.materials`. A float value is interpreted as permittivity.  Defaults to 1.0.
            device (torch.device, optional): Defaults to "cpu".
        """
        super().__init__(device=device)
        self.n_dim = 3

        if type(env_material) in (float, int):
            from torchgdm.materials import MatConstant

            self.env_material = MatConstant(env_material)
        else:
            self.env_material = env_material
        
        self.set_device(self.device)

    def __repr__(self, verbose=False):
        """description about simulation environment defined by set of dyads"""
        out_str = " ------ homogeneous 3D environment -------"
        out_str += "\n env. material: {}".format(self.env_material)
        # out_str += "\n --------------------------------------"
        return out_str

    def set_device(self, device):
        """move all tensors of the class to device"""
        super().set_device(device)
        self.env_material.set_device(device)

    def get_environment_permittivity_scalar(
        self, wavelength: float, r_probe: torch.Tensor
    ):
        """return scalar complex environment permittivity for `wavelength` at pos. `r_probe` (units in nm)

        assume isotropic env. material: returns [0,0]-component of eps. tensor

        homogeneous medium: all positions `r_probe` will be same material

        Args:
            wavelength (float): in nm
            r_probe (torch.Tensor): position(s) at which the permittivity is to be returned

        Raises:
            ValueError: In case env. material is not isotropic

        Returns:
            torch.Tensor: scalar permittivity at all positions `r_probe`
        """

        eps_env_tensor = self.env_material.get_epsilon(wavelength)

        if not _tensor_is_diagonal_and_identical(eps_env_tensor):
            raise ValueError(
                "Environment material is not isotropic, but tensorial epsilon was received. "
                + "Only isotropic environment media are supported."
            )
        self.eps_env_scalar = eps_env_tensor[0, 0]

        if self.eps_env_scalar.imag != 0:
            warnings.warn(
                "Environment permittivity evaluated to non-zero imaginary part. "
                + "This is not physically meaningful in the infinite environment medium."
            )

        eps_env_tensor = (
            torch.ones(len(r_probe), dtype=DTYPE_COMPLEX, device=self.device)
            * self.eps_env_scalar
        )

        return eps_env_tensor

    # --- individual sources Green's tensors
    def get_G_Ep(self, r_probe, r_source, wavelength):
        """3D free space electric field (at r_probe) Green's tensor for an electric dipole (at r_source)

        Args:
            r_probe (torch.Tensor): probe position
            r_source (torch.Tensor): source position
            wavelength (float): in nm

        Returns:
            torch.Tensor: electric-electric Green's Dyad
        """
        eps_env = self.get_environment_permittivity_scalar(
            wavelength,
            r_probe=torch.zeros((1, 3), dtype=DTYPE_FLOAT, device=self.device),
        )[0]
        if r_probe.device != eps_env.device or r_source.device != eps_env.device:
            r_probe.to(self.device)
            r_source.to(self.device)
        return G0_Ep(r_probe, r_source, wavelength, eps_env=eps_env)

    def get_G_Hp(self, r_probe, r_source, wavelength):
        """3D free space magnetic field (at r_probe) Green's tensor for a magnetic dipole (at r_source)

        Args:
            r_probe (torch.Tensor): probe position
            v (torch.Tensor): source position
            wavelength (float): in nm

        Returns:
            torch.Tensor: magnetic-magnetic Green's Dyad
        """
        eps_env = self.get_environment_permittivity_scalar(
            wavelength,
            r_probe=torch.zeros((1, 3), dtype=DTYPE_FLOAT, device=self.device),
        )[0]
        return G0_Hp(r_probe, r_source, wavelength, eps_env=eps_env)

    def get_G_Em(
        self, r_probe: torch.Tensor, r_source: torch.Tensor, wavelength: float
    ):
        """3D free space electric field (at r_probe) Green's tensor for a magnetic dipole (at r_source)

        G0_Em = - G0_Hp

        for doc, see :meth:`EnvHomogeneous3D.get_G_Hp`
        """
        eps_env = self.get_environment_permittivity_scalar(
            wavelength,
            r_probe=torch.zeros((1, 3), dtype=DTYPE_FLOAT, device=self.device),
        )[0]
        return G0_Em(r_probe, r_source, wavelength, eps_env=eps_env)

    def get_G_Hm(
        self, r_probe: torch.Tensor, r_source: torch.Tensor, wavelength: float
    ):
        """3D free space magnetic field (at r_probe) Green's tensor for a magnetic dipole (at r_source)

        G0_Hm = G0_Ep

        for doc, see :meth:`EnvHomogeneous3D.get_G_Ep`
        """
        eps_env = self.get_environment_permittivity_scalar(
            wavelength,
            r_probe=torch.zeros((1, 3), dtype=DTYPE_FLOAT, device=self.device),
        )[0]
        return G0_Hm(r_probe, r_source, wavelength, eps_env=eps_env)

    # --- far-field approximation
    def get_G_Ep_farfield(self, r_probe, r_source, wavelength):
        """Electric field asymptotic far-field Green's tensor for an electric dipole

        r_probe: field evaluation position, r_source: emitter position
        """
        eps_env = self.get_environment_permittivity_scalar(
            wavelength,
            r_probe=torch.zeros((1, 3), dtype=DTYPE_FLOAT, device=self.device),
        )[0]
        return G0_Ep_ff(r_probe, r_source, wavelength, eps_env=eps_env)

    def get_G_Em_farfield(self, r_probe, r_source, wavelength):
        """Electric field asymptotic far-field Green's tensor for a magnetic dipole

        r_probe: field evaluation position, r_source: emitter position
        """
        eps_env = self.get_environment_permittivity_scalar(
            wavelength,
            r_probe=torch.zeros((1, 3), dtype=DTYPE_FLOAT, device=self.device),
        )[0]
        return G0_Em_ff(r_probe, r_source, wavelength, eps_env=eps_env)


## ---------------- test Green's tensors ----------------
if __name__ == "__main__":
    import time

    import scipy
    import numpy as np
    import matplotlib.pyplot as plt

    from torchgdm.env.freespace_3d._dyads_numpy import (
        G0_Ep_vec,
        G0_Hp_vec,
        G0_Em_vec,
        G0_Hm_vec,
    )
    from pyGDM2 import tools
    from pyGDM2.propagators import _G0 as G0_Ep_seq
    from pyGDM2.propagators import _G0_HE as G0_Hp_seq

    device = torch.device("cuda:0")
    # torch.cuda.empty_cache()
    # device = torch.device('cpu')

    func_seq = G0_Ep_seq
    func_np = G0_Ep_vec
    func_torch = G0_Ep

    func_seq = G0_Hp_seq
    func_np = G0_Hp_vec
    func_torch = G0_Hp

    # func_np = G0_Em_vec
    # func_torch = G0_Em
    # func_np = G0_Hm_vec
    # func_torch = G0_Hm

    # ---- technical test
    N_dim1 = 10
    R1 = torch.randn(N_dim1, 3).to(device)
    R2 = torch.randn(N_dim1, 3).to(device)
    wavelength = 500.0  # nm
    eps = 2.25  # permittivity
    result = func_torch(R1, R2, wavelength, eps)
    print(result.shape)

    # ---- quantitative test
    # setup
    eps_env = 1.5
    wl = 500.0

    DX, NX = 10, 20
    Z0 = 10
    r_probe = tools.generate_NF_map_XY(-DX, DX, NX, -DX, DX, NX, Z0)
    r0 = np.zeros_like(r_probe, dtype=np.float32)  # fix emitter position
    r_probe_t = torch.as_tensor(r_probe, dtype=DTYPE_FLOAT).to(device)
    r0_t = torch.as_tensor(r0, dtype=DTYPE_FLOAT).to(device)

    # eval numpy
    print("evaluating {} greens tensors".format(len(r_probe)))
    t1a = time.time()
    G0_vec1 = func_np(r0, r_probe, wl, eps_env)
    t1b = time.time()
    print("time numpy: {:.5f}s".format(t1b - t1a))

    # eval sequential
    # print('evaluating {} greens tensors'.format(len(r_probe)))
    # t1a = time.time()
    # for i in range(len(r0)):
    #     xx, yy, zz, xy, xz, yx, yz, zx, zy = func_seq(r0[i], r_probe[i], wl, eps_env)
    #     G0 = np.array([
    #         [xx, xy, xz],
    #         [yx, yy, yz],
    #         [zx, zy, zz],
    #         ]).astype(np.complex64)
    #     G0_vec1[i] = G0
    # t1b = time.time()
    # print('time sequential: {:.5f}s'.format(t1b-t1a))

    # eval torch
    t2a = time.time()
    G0_vec2t = func_torch(r0_t, r_probe_t, wl, eps_env)
    t2b = time.time()

    # evaluate using broadcasting
    # interact_NxN = func_torch(r_probe_t.unsqueeze(1), r_probe_t.unsqueeze(0), wl, eps_env)

    print("time torch (on device {}): {:.5f}s".format(device, t2b - t2a))
    print("speed-up torch: x{:.3f}".format((t1b - t1a) / (t2b - t2a)))

    G0_vec2 = G0_vec2t.cpu().numpy()
    G0_vec1 = G0_vec1.reshape(NX, NX, 3, 3)
    G0_vec2 = G0_vec2.reshape(NX, NX, 3, 3)

    print(np.abs(G0_vec1).mean())
    print((np.abs(G0_vec1) - np.abs(G0_vec2)).mean())

    i1, i2 = 2, 0
    plt.subplot(221)
    plt.title("numpy")
    plt.imshow(G0_vec1[..., i1, i2].real)
    plt.colorbar()
    plt.subplot(222)
    plt.title("pytorch")
    plt.imshow(G0_vec2[..., i1, i2].real)
    plt.colorbar()
    plt.subplot(223)
    plt.imshow(G0_vec1[..., i1, i2].imag)
    plt.colorbar()
    plt.subplot(224)
    plt.imshow(G0_vec2[..., i1, i2].imag)
    plt.colorbar()

    plt.show()

    # ---- test inversion speed
    print("test inversion: {}x{} dipoles".format(NX, NX))

    t3a = time.time()
    G0_vec1 = G0_vec1.reshape(3 * NX, 3 * NX)
    inv = scipy.linalg.lu(G0_vec1)
    t3b = time.time()
    print("time scipy-LU (on CPU): {:.5f}s".format(t3b - t3a))

    t4a = time.time()
    G0_vec2t = G0_vec2t.reshape(3 * NX, 3 * NX)
    inv = torch.linalg.lu(G0_vec2t)
    t4b = time.time()
    print("time torch-LU (on device {}): {:.5f}s".format(device, t4b - t4a))

    # %%
    # t0 = time.time()
    # i1 = torch.linalg.inv(G0_vec2t)
    # t1 = time.time()
    # i2 = torch.linalg.inv_ex(G0_vec2t)
    # t2 = time.time()
    # print(t1-t0)
    # print(t2-t1)
