
# encoding=utf-8
# %%
import unittest

import torch

import torchgdm as tg


class TestAutoGrad(unittest.TestCase):

    def setUp(self):
        self.verbose = False
        if self.verbose:
            print("testing autograd with discretized simulation...")

        # --- determine if GPU is available
        self.devices = ["cpu"]
        if torch.cuda.is_available():
            self.devices.append("cuda:0")

        # --- setup a test case
        # - environment
        mat_env = tg.materials.MatConstant(1)
        self.env = tg.env.freespace_3d.EnvHomogeneous3D(env_material=mat_env)

        # - illumination field(s)
        self.wavelengths = torch.as_tensor([620.0])
        # self.e_inc_list = [
        #     tg.env.freespace_3d.GaussianParaxial(
        #         e0p=0.7, e0s=0.7, inc_angle=torch.pi / 3.0, NA=0.1
        #     ),
        # ]
        self.e_inc_list = [
            tg.env.freespace_3d.PlaneWave(e0p=0.7, e0s=0.7, inc_angle=torch.pi / 3.0),
        ]

        # - structure
        self.step = 20.0
        self.mat = tg.materials.MatDatabase("Ge")
        self.struct = tg.struct3d.StructDiscretizedCubic3D(
            tg.struct3d.cuboid(l=2, w=2, h=2), self.step, self.mat
        )

    def test_autograd_wavelength(self):
        for device in self.devices:
            wavelengths = self.wavelengths.clone().to(device=device)
            wavelengths.requires_grad = True

            # setup new material and structure (since wl-grad requires backprop through them)
            mat = tg.materials.MatDatabase("Ge")
            struct = tg.struct3d.StructDiscretizedCubic3D(
                tg.struct3d.cuboid(l=2, w=2, h=2), self.step, mat
            )

            # setup sim
            sim = tg.simulation.Simulation(
                structures=[struct],
                environment=self.env,
                illumination_fields=self.e_inc_list,
                wavelengths=wavelengths,
                device=device,
            )

            sim.run(verbose=False, progress_bar=False)
            cs_calc = tg.postproc.crosssect.total(sim, wavelength=wavelengths[0])
            scs_calc = cs_calc["scs"]

            scs_calc.backward()
            dscs_dwl = wavelengths.grad

            # print(scs_calc)
            # print(dscs_dwl)

            # compare to pre-calculated reference
            scs_truth = torch.as_tensor(
                [16.5680466],
                dtype=tg.constants.DTYPE_FLOAT,
                device=device,
            )
            dscs_dwl_truth = torch.as_tensor(
                [-0.1381907],
                dtype=tg.constants.DTYPE_FLOAT,
                device=device,
            )

            torch.testing.assert_close(scs_calc, scs_truth, rtol=1e-3, atol=1e-3)
            torch.testing.assert_close(dscs_dwl, dscs_dwl_truth, rtol=1e-3, atol=1e-3)

            if self.verbose:
                print("  - {}: autograd scs wrt wavelength test passed.".format(device))

    def test_autograd_position(self):
        for device in self.devices:

            pos = torch.as_tensor(
                [5050, 40, 100], dtype=tg.constants.DTYPE_FLOAT, device=device
            )
            pos.requires_grad = True
            self.struct.set_center_of_mass(pos)

            sim = tg.simulation.Simulation(
                structures=[self.struct],
                environment=self.env,
                illumination_fields=self.e_inc_list,
                wavelengths=self.wavelengths,
                device=device,
                copy_structures=False,
            )

            sim.run(verbose=False, progress_bar=False)
            cs_calc = tg.postproc.crosssect.total(sim, wavelength=self.wavelengths[0])
            scs_calc = cs_calc["scs"]

            scs_calc.backward()
            dscs_dpos = pos.grad

            # print(scs_calc)
            # print(dscs_dpos)

            # compare to pre-calculated reference
            scs_truth = torch.as_tensor(
                [16.5680466],
                dtype=tg.constants.DTYPE_FLOAT,
                device=device,
            )
            dscs_dpos_truth = torch.as_tensor(
                [8.9406967e-07, 5.9604645e-08, -2.9802322e-07],
                dtype=tg.constants.DTYPE_FLOAT,
                device=device,
            )

            torch.testing.assert_close(scs_calc, scs_truth, rtol=1e-3, atol=1e-3)
            torch.testing.assert_close(dscs_dpos, dscs_dpos_truth, rtol=1e-3, atol=1e-3)

            if self.verbose:
                print(
                    "  - {}: autograd scs wrt structure position test passed.".format(
                        device
                    )
                )


# %%
if __name__ == "__main__":
    print("testing autograd...")
    torch.set_printoptions(precision=7)
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
