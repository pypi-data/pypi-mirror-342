# -*- coding: utf-8 -*-
"""
vectorized pytorch implementations of free space Green's tensors
"""
# %%
import warnings

import numpy as np
import torch

from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX

from torchgdm.env.base_classes import EnvironmentBase
from torchgdm.tools.misc import _tensor_is_diagonal_and_identical, _test_positional_input
from torchgdm.tools.misc import get_default_device
from torchgdm.tools.special import H1n


# %%
# --- vectorized pytorch
def G0_2d_Ep(
    r_probe: torch.Tensor,
    r_source: torch.Tensor,
    wavelength: float,
    eps_env: float,
    k0_y: float,
    epsilon_dist: float = 1e-8,
) -> torch.Tensor:
    """2D free space electric field (at r_probe) Green's tensor for an electric line dipole (at r_source)

    Args:
        r_probe (torch.Tensor): probe position
        r_source (torch.Tensor): source position
        wavelength (float): in nm
        eps_env (float): environment permittivity
        k0_y (float): parallel wavevector component (must match the illumination)
        epsilon_dist (float, optional): small distance to avoid divergence at r_probe=r_source. Defaults to 1e-8.

    Returns:
        torch.Tensor: 2D electric-electric Green's Dyad
    """
    # note: hankel support only pure real / pure imag args
    eps_env = torch.as_tensor(eps_env, dtype=DTYPE_COMPLEX, device=r_probe.device).real

    r_probe, r_source = _test_positional_input(r_probe, r_source)

    # positional values
    delta_r = r_probe - r_source  # vector difference(s)
    d_x = delta_r[..., 0]
    d_z = delta_r[..., 2]
    y_obs = r_probe[..., 1]
    lR = torch.sqrt(d_x**2 + d_z**2 + epsilon_dist)

    # wavenumber
    k0 = 2 * np.pi / wavelength
    k02 = k0**2
    k0y2 = k0_y**2
    kr2 = eps_env * k02 - k0y2
    kr = torch.sqrt(kr2)  # wavenumber in 2D plane

    # evaluate Hankel functions of first kind
    h01 = H1n(0, kr * lR)
    h11 = H1n(1, kr * lR)
    h21 = H1n(2, kr * lR)

    # pre-calculate termes used multiple times
    cop = d_x / lR
    sip = d_z / lR
    co2p = 2.0 * cop**2 - 1.0
    si2p = 2.0 * cop * sip
    xx_t1 = (k02 - kr2 / (2.0 * eps_env)) * h01
    xx_t2 = kr2 * co2p * h21 / (2.0 * eps_env)

    # phase along infinite axis
    phase_y = torch.exp(1j * k0_y * y_obs)

    # populate the Green's tensor
    G0_2d = torch.zeros(
        (*delta_r.size()[:-1], 3, 3), dtype=DTYPE_COMPLEX, device=r_probe.device
    )
    G0_2d[..., 0, 0] = (xx_t1 + xx_t2) * phase_y
    G0_2d[..., 0, 1] = -1j * kr * k0_y * cop * h11 / eps_env * phase_y
    G0_2d[..., 0, 2] = (kr2 * si2p) * h21 / (2.0 * eps_env) * phase_y
    G0_2d[..., 1, 1] = (k02 - k0y2 / eps_env) * h01 * phase_y
    G0_2d[..., 1, 2] = -1j * kr * k0_y * sip * h11 / eps_env * phase_y
    G0_2d[..., 2, 2] = (xx_t1 - xx_t2) * phase_y

    G0_2d[..., 1, 0] = G0_2d[..., 0, 1]
    G0_2d[..., 2, 0] = G0_2d[..., 0, 2]
    G0_2d[..., 2, 1] = G0_2d[..., 1, 2]

    # here: cgs! SI: *1/(4*pi)
    return 1j * torch.pi * G0_2d


def G0_2d_Hp(
    r_probe: torch.Tensor,
    r_source: torch.Tensor,
    wavelength: float,
    eps_env: float,
    k0_y: float,
    epsilon_dist: float = 1e-8,  # to avoid divergence at r_probe=r_source
) -> torch.Tensor:
    """2D free space Green's tensor for magnetic field (at r_probe) from an electric line dipole (at r_source)

    Args:
        r_probe (torch.Tensor): probe position
        r_source (torch.Tensor): source position
        wavelength (float): in nm
        eps_env (float): environment permittivity
        k0_y (float): parallel wavevector component (must match the illumination)
        epsilon_dist (float, optional): small distance to avoid divergence at r_probe=r_source. Defaults to 1e-8.

    Returns:
        torch.Tensor: 2D magnetic-magnetic Green's Dyad
    """
    eps_env = torch.as_tensor(eps_env, dtype=DTYPE_COMPLEX, device=r_probe.device).real

    r_probe, r_source = _test_positional_input(r_probe, r_source)

    # positional values
    delta_r = r_probe - r_source  # vector difference(s)
    d_x = delta_r[..., 0]
    d_z = delta_r[..., 2]
    y_obs = r_probe[..., 1]
    lR = torch.sqrt(d_x**2 + d_z**2 + epsilon_dist)

    # wavenumber
    k0 = 2 * np.pi / wavelength
    k02 = k0**2
    k0y2 = k0_y**2
    kr2 = eps_env * k02 - k0y2
    kr = torch.sqrt(kr2)  # wavenumber in 2D plane

    # evaluate Hankel functions of first kind
    if k0_y != 0:
        h01 = H1n(0, kr * lR)
    else:
        h01 = 0
    h11 = H1n(1, kr * lR)

    # phase along infinite axis
    phase_y = torch.exp(1j * k0_y * y_obs)

    # populate the Green's tensor
    G0_2d = torch.zeros(
        (*delta_r.size()[:-1], 3, 3), dtype=DTYPE_COMPLEX, device=r_probe.device
    )
    G0_2d[..., 0, 0] = 0
    G0_2d[..., 0, 1] = k0 * torch.pi * h11 * (kr / lR) * d_z * phase_y
    G0_2d[..., 0, 2] = 1j * torch.pi * k0 * k0_y * h01 * phase_y

    G0_2d[..., 1, 0] = -1 * G0_2d[..., 0, 1]
    G0_2d[..., 1, 1] = 0
    G0_2d[..., 1, 2] = k0 * torch.pi * h11 * (kr / lR) * d_x * phase_y

    G0_2d[..., 2, 0] = -1 * G0_2d[..., 0, 2]
    G0_2d[..., 2, 1] = -1 * G0_2d[..., 1, 2]
    G0_2d[..., 2, 2] = 0

    # here: cgs! SI: *1/(4*pi)
    return G0_2d


def G0_2d_Em(
    r_probe, r_source, wavelength, eps_env, k0_y=0.0, epsilon_dist: float = 1e-8
):
    """2D free space electric field (at r_probe) Green's tensor for a magnetic line dipole (at r_source)

    G0_2d_Em = - G0_2d_Hp

    for doc, see :func:`G0_2d_Hp`
    """
    return -1 * G0_2d_Hp(
        r_probe,
        r_source,
        wavelength,
        eps_env=eps_env,
        k0_y=k0_y,
        epsilon_dist=epsilon_dist,
    )


def G0_2d_Hm(
    r_probe, r_source, wavelength, eps_env, k0_y=0.0, epsilon_dist: float = 1e-8
):
    """2D free space magnetic field (at r_probe) Green's tensor for a magnetic line dipole (at r_source)

    G0_2d_Hm = G0_2d_Ep

    for doc, see :func:`G0_2d_Ep`
    """
    return eps_env * G0_2d_Ep(
        r_probe,
        r_source,
        wavelength,
        eps_env=eps_env,
        k0_y=k0_y,
        epsilon_dist=epsilon_dist,
    )


# --- environment class
class EnvHomogeneous2D(EnvironmentBase):
    """class defining a homogeneous 2D environment

    - defines set of free-space Green's tensors
    - environemnt material needs to be isotropic (scalar epsilon) and lossless.
    - infinite axis is the y-axis
    """

    __name__ = "homogeneous environment 2D"

    def __init__(
        self,
        env_material=1.0,
        k0_y=0.0,
        inc_angle_y=None,
        device: torch.device = None,
    ):
        """class defining a homogeneous 2D environment. Infinite axis along y

        Args:
            env_material (float, optional): Environment material. Either float or class from :mod:`torchgdm.materials`. A float value is interpreted as permittivity.  Defaults to 1.0.
            k0_y (float, optional): parallel k-vector component. Must match the illumination field. Caution, using a `k0_y != 0` will be constant for all wavelengths! Defaults to 0.0 (normal incidence).
            inc_angle_y (float, optional): If used, `k0_y` will be ignored. Incident angle to calculate parallel k-vector component. Must match the illumination field.  Using the incident angle instead of `k0_y` will work for several wavelengths. Defaults to `None` (--> use `k0_y`).
            device (torch.device, optional): Defaults to "cpu" (can be changed by :func:`torchgdm.use_cuda`).
        """
        super().__init__(device=device)
        self.n_dim = 2

        if type(env_material) in (float, int):
            from torchgdm.materials import MatConstant

            self.env_material = MatConstant(env_material)
        else:
            self.env_material = env_material
        

        # set parallel k-vector comp.
        self.k0_y = torch.as_tensor(k0_y, dtype=DTYPE_FLOAT, device=device)
        self.inc_angle_y = inc_angle_y
        if inc_angle_y is not None:
            self.inc_angle_y = torch.as_tensor(
                inc_angle_y, dtype=DTYPE_FLOAT, device=self.device
            )
        
        self.set_device(self.device)

    def __repr__(self, verbose=False):
        """description about simulation environment defined by set of dyads"""
        out_str = " ------ homogeneous 2D environment, infinite axis along Y -------"
        out_str += "\n env. material: {}".format(self.env_material)
        return out_str

    def set_device(self, device):
        """move all tensors of the class to device"""
        super().set_device(device)

        if self.inc_angle_y is not None:
            self.inc_angle_y = self.inc_angle_y.to(device)

        self.k0_y = self.k0_y.to(device)

        self.env_material.set_device(device)

    def get_k0_y(self, wavelength):
        """return parallel k-vector component"""
        if self.inc_angle_y is not None:
            return torch.as_tensor(
                torch.sin(self.inc_angle_y) * 2 * torch.pi / wavelength,
                dtype=DTYPE_FLOAT,
                device=self.device,
            )
        else:
            return self.k0_y

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
        """2D free space electric field (at r_probe) Green's tensor for an electric line dipole (at r_source)

        Args:
            r_probe (torch.Tensor): probe position
            r_source (torch.Tensor): source position
            wavelength (float): in nm

        Returns:
            torch.Tensor: 2D electric-electric Green's Dyad
        """
        eps_env = self.get_environment_permittivity_scalar(
            wavelength,
            r_probe=torch.zeros((1, 3), dtype=DTYPE_FLOAT, device=self.device),
        )[0]
        k0_y = self.get_k0_y(wavelength)
        return G0_2d_Ep(r_probe, r_source, wavelength, k0_y=k0_y, eps_env=eps_env)

    def get_G_Hp(self, r_probe, r_source, wavelength):
        """2D free space magnetic field (at r_probe) Green's tensor for a magnetic line dipole (at r_source)

        Args:
            r_probe (torch.Tensor): probe position
            r_source (torch.Tensor): source position
            wavelength (float): in nm

        Returns:
            torch.Tensor: 2D magnetic-magnetic Green's Dyad
        """
        eps_env = self.get_environment_permittivity_scalar(
            wavelength,
            r_probe=torch.zeros((1, 3), dtype=DTYPE_FLOAT, device=self.device),
        )[0]
        k0_y = self.get_k0_y(wavelength)
        return G0_2d_Hp(r_probe, r_source, wavelength, k0_y=k0_y, eps_env=eps_env)

    def get_G_Em(
        self, r_probe: torch.Tensor, r_source: torch.Tensor, wavelength: float
    ):
        """2D free space electric field (at r_probe) Green's tensor for a magnetic line dipole (at r_source)

        G0_2d_Em = - G0_2d_Hp

        for doc, see :meth:`EnvHomogeneous2D.get_G_Hp`
        """
        eps_env = self.get_environment_permittivity_scalar(
            wavelength,
            r_probe=torch.zeros((1, 3), dtype=DTYPE_FLOAT, device=self.device),
        )[0]
        k0_y = self.get_k0_y(wavelength)
        return G0_2d_Em(r_probe, r_source, wavelength, k0_y=k0_y, eps_env=eps_env)

    def get_G_Hm(
        self, r_probe: torch.Tensor, r_source: torch.Tensor, wavelength: float
    ):
        """2D free space magnetic field (at r_probe) Green's tensor for a magnetic line dipole (at r_source)

        G0_2d_Hm = G0_2d_Ep

        for doc, see :meth:`EnvHomogeneous2D.get_G_Ep`
        """
        eps_env = self.get_environment_permittivity_scalar(
            wavelength,
            r_probe=torch.zeros((1, 3), dtype=DTYPE_FLOAT, device=self.device),
        )[0]
        k0_y = self.get_k0_y(wavelength)
        return G0_2d_Hm(r_probe, r_source, wavelength, k0_y=k0_y, eps_env=eps_env)

    def get_G_Ep_farfield(self, r_probe, r_source, wavelength):
        """2D far-field approximation  for electric-electric Green's tensor

        2D case: No approximation is used, return full 2D tensor

        Args:
            r_probe (torch.Tensor): probe position
            r_source (torch.Tensor): source position (electric line dipole)
            wavelength (float): in nm

        Returns:
            torch.Tensor: 2D farfield electric-electric Green's Dyad
        """
        return self.get_G_Ep(r_probe, r_source, wavelength)

    def get_G_Em_farfield(self, r_probe, r_source, wavelength):
        """2D far-field approximation for electric-magnetic Green's tensor

        2D case: No approximation is used, return full 2D tensor

        Args:
            r_probe (torch.Tensor): probe position
            r_source (torch.Tensor): source position (magnetic line dipole)
            wavelength (float): in nm

        Returns:
            torch.Tensor: 2D farfield electric-magnetic Green's Dyad
        """
        return self.get_G_Em(r_probe, r_source, wavelength)


## ---------------- test Green's tensors ----------------
if __name__ == "__main__":
    import time

    import scipy
    import numpy as np
    import matplotlib.pyplot as plt

    from pyGDM2 import tools
    from pyGDM2.propagators.propagators_2D import _s0_2D, _G0_2D, _G0_HE_2D

    # device = torch.device("cuda:0")
    device = torch.device("cpu")

    func_numba = _G0_2D
    func_torch = G0_2d_Ep

    # func_numba = _G0_HE_2D
    # func_torch = G0_2d_Hp

    # ---- quantitative test
    # setup
    eps_env = 1.0
    wl = 500.0
    k0_y = 0.5 * 2 * torch.pi / wl

    DX, NX = 50, 50
    Z0 = 0
    r_probe = tools.generate_NF_map_XZ(1, 10, NX, -2, 5, NX, Z0)
    r0 = np.zeros_like(r_probe, dtype=np.float32)  # fix emitter position
    r_probe_t = torch.as_tensor(r_probe, dtype=DTYPE_FLOAT).to(device)
    r0_t = torch.as_tensor(r0, dtype=DTYPE_FLOAT).to(device)

    # eval numba sequential
    G0_vec1 = np.zeros((NX * NX, 3, 3), dtype=np.complex64)
    print("evaluating {} greens tensors".format(len(r_probe)))
    t1a = time.time()
    for i, (_r0, _r) in enumerate(zip(r0, r_probe)):
        xx, yy, zz, xy, xz, yx, yz, zx, zy = func_numba(_r0, _r, wl, eps_env, ky0=k0_y)
        G0 = np.array(
            [
                [xx, xy, xz],
                [yx, yy, yz],
                [zx, zy, zz],
            ],
            dtype=np.complex64,
        )
        G0_vec1[i] = G0
    t1b = time.time()
    print("time sequential: {:.5f}s".format(t1b - t1a))

    # eval torch
    t2a = time.time()
    G0_vec2t = func_torch(r_probe_t, r0_t, wl, eps_env, k0_y=k0_y)
    t2b = time.time()

    # test evaluate using broadcasting
    # interact_NxN = func_torch(
    #     r_probe_t.unsqueeze(1), r_probe_t.unsqueeze(0), wl, eps_env, k0_y
    # )

    print("time torch (on device {}): {:.5f}s".format(device, t2b - t2a))
    print("speed-up torch: x{:.3f}".format((t1b - t1a) / (t2b - t2a)))

    G0_vec1 = G0_vec1.reshape(NX, NX, 3, 3)
    G0_vec2 = G0_vec2t.detach().cpu().numpy()
    G0_vec2 = G0_vec2.reshape(NX, NX, 3, 3)

    print(np.abs(G0_vec1).mean())
    print((np.abs(G0_vec1 - G0_vec2)).mean())

    i1, i2 = 2, 1
    plt.subplot(321)
    plt.title("numpy")
    plt.imshow(G0_vec1[..., i1, i2].real)
    plt.colorbar()
    plt.subplot(323)
    plt.imshow(G0_vec1[..., i1, i2].imag)
    plt.colorbar()
    plt.subplot(325)
    plt.imshow(np.abs(G0_vec1[..., i1, i2]))
    plt.colorbar()

    plt.subplot(322)
    plt.title("pytorch")
    plt.imshow(G0_vec2[..., i1, i2].real)
    plt.colorbar()
    plt.subplot(324)
    plt.imshow(G0_vec2[..., i1, i2].imag)
    plt.colorbar()
    plt.subplot(326)
    plt.imshow(np.abs(G0_vec2[..., i1, i2]))
    plt.colorbar()

    plt.show()
