# encoding=utf-8
# %%
import unittest

import torch
from scipy.special import jv, yv, iv, kv, hankel1, hankel2

import torchgdm as tg
from torchgdm.tools import special
from torchgdm.constants import DTYPE_FLOAT
from torchgdm.constants import DTYPE_COMPLEX


class TestSpecialFunctions(unittest.TestCase):

    def setUp(self):
        self.verbose = False
        if self.verbose:
            print("testing plane wave illumination.")

        # --- determine if GPU is available
        self.devices = ["cpu"]
        if torch.cuda.is_available():
            self.devices.append("cuda:0")

        self.z_re = torch.linspace(0.01, 5, 100, dtype=torch.float32)
        self.z_im = 1j * torch.linspace(0.01, 5, 100, dtype=torch.complex64)

    def test_bessel(self):
        for device in self.devices:
            for n in torch.arange(-3, 4):
                z_re = self.z_re.to(device)
                z_im = self.z_im.to(device)

                # compare with scipy - real args
                j_scipy = torch.as_tensor(
                    jv(n, tg.to_np(self.z_re)), device=device, dtype=DTYPE_FLOAT
                )
                j_torch = special.Jn(n, z_re)
                y_scipy = torch.as_tensor(
                    yv(n, tg.to_np(self.z_re)), device=device, dtype=DTYPE_FLOAT
                )
                y_torch = special.Yn(n, z_re)

                torch.testing.assert_close(j_scipy, j_torch, rtol=1e-3, atol=1e-3)
                torch.testing.assert_close(y_scipy, y_torch, rtol=1e-3, atol=1e-3)

                # compare with scipy - complex args
                j_scipy_im = torch.as_tensor(
                    jv(n, tg.to_np(self.z_im)), device=device, dtype=DTYPE_COMPLEX
                )
                j_torch_im = special.Jn(n, z_im)
                y_scipy_im = torch.as_tensor(
                    yv(n, tg.to_np(self.z_im)), device=device, dtype=DTYPE_COMPLEX
                )
                y_torch_im = special.Yn(n, z_im)

                torch.testing.assert_close(j_scipy_im, j_torch_im, rtol=1e-3, atol=1e-3)
                torch.testing.assert_close(y_scipy_im, y_torch_im, rtol=1e-3, atol=1e-3)

            if self.verbose:
                print("  - {}: field evaluation test passed.".format(device))

    def test_modbessel(self):
        for device in self.devices:
            for n in torch.arange(-3, 4):
                z_re = self.z_re.to(device)

                # modified bessel - real arg
                i_scipy = torch.as_tensor(
                    iv(n, tg.to_np(self.z_re)), device=device, dtype=DTYPE_FLOAT
                )
                i_torch = special.In(n, z_re)
                k_scipy = torch.as_tensor(
                    kv(n, tg.to_np(self.z_re)), device=device, dtype=DTYPE_FLOAT
                )
                k_torch = special.Kn(n, z_re)

                torch.testing.assert_close(i_scipy, i_torch, rtol=1e-3, atol=1e-3)
                torch.testing.assert_close(k_scipy, k_torch, rtol=1e-3, atol=1e-3)

    def test_hankel(self):
        for device in self.devices:
            for n in torch.arange(-3, 4):
                z_re = self.z_re.to(device)
                z_im = self.z_im.to(device)

                # hankel - real arg
                h1_scipy = torch.as_tensor(
                    hankel1(n, tg.to_np(self.z_re)), device=device, dtype=DTYPE_COMPLEX
                )
                h1_torch = special.H1n(n, z_re)
                h2_scipy = torch.as_tensor(
                    hankel2(n, tg.to_np(self.z_re)), device=device, dtype=DTYPE_COMPLEX
                )
                h2_torch = special.H2n(n, z_re)

                torch.testing.assert_close(h1_scipy, h1_torch, rtol=1e-3, atol=1e-3)
                torch.testing.assert_close(h2_scipy, h2_torch, rtol=1e-3, atol=1e-3)

                # hankel - imag arg
                h1_scipy_im = torch.as_tensor(
                    hankel1(n, tg.to_np(self.z_im)), device=device, dtype=DTYPE_COMPLEX
                )
                h1_torch_im = special.H1n(n, z_im)
                h2_scipy_im = torch.as_tensor(
                    hankel2(n, tg.to_np(self.z_im)), device=device, dtype=DTYPE_COMPLEX
                )
                h2_torch_im = special.H2n(n, z_im)

                torch.testing.assert_close(
                    h1_scipy_im, h1_torch_im, rtol=1e-3, atol=1e-3
                )
                torch.testing.assert_close(
                    h2_scipy_im, h2_torch_im, rtol=1e-3, atol=1e-3
                )


# %%


if __name__ == "__main__":
    print("testing special functions.")
    torch.set_printoptions(precision=7)
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
