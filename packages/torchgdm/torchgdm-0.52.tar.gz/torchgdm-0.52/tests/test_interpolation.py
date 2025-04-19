# encoding=utf-8
# %%
import unittest

import torch

import torchgdm as tg


class TestInterpolation(unittest.TestCase):

    def setUp(self):
        self.verbose = False
        if self.verbose:
            print("testing plane wave illumination.")

        # --- determine if GPU is available
        self.devices = ["cpu"]
        if torch.cuda.is_available():
            self.devices.append("cuda:0")

    def test_interp1d(self):
        from torchgdm.tools.interp import interp1d

        try:
            import numpy as np
        except ImportError:
            import warnings

            warnings.warn("Numpy not installed. Skipping interpolation test.")
            return

        for device in self.devices:
            x_e = torch.linspace(-1.2, 1.2, 500, device=device)
            x_t = torch.linspace(-1, 1, 40, device=device)

            y_t = torch.sin(x_t)
            y_t = torch.rand(len(x_t), dtype=torch.complex64, device=device)

            y_e = interp1d(x_e, x_t, y_t)
            y_e_np = torch.as_tensor(
                np.interp(
                    x_e.detach().cpu().numpy(),
                    x_t.detach().cpu().numpy(),
                    y_t.detach().cpu().numpy(),
                )
            )

            # test if numpy and torch interpolations return equal results
            np.testing.assert_almost_equal(y_e_np.imag, y_e.imag.detach().cpu().numpy(), decimal=6)
            np.testing.assert_almost_equal(y_e_np.real, y_e.real.detach().cpu().numpy(), decimal=6)

            if self.verbose:
                print("  - {}: interpolation test passed.".format(device))


# %%


if __name__ == "__main__":
    print("testing interpolation functions.")
    torch.set_printoptions(precision=7)
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
