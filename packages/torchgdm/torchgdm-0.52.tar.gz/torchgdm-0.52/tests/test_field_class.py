# encoding=utf-8
# %%
import unittest

import torch

import torchgdm as tg


class TestFieldClass(unittest.TestCase):

    def setUp(self):
        self.verbose = False
        if self.verbose:
            print("testing field class API...")

        # --- determine if GPU is available
        self.devices = ["cpu"]
        if torch.cuda.is_available():
            self.devices.append("cuda:0")

        # --- setup a test case
        # - environment
        self.env = tg.env.freespace_3d.EnvHomogeneous3D(1)

        # - illumination field(s)
        self.wl = 500.0
        self.wls = [self.wl]
        self.e_inc = tg.env.freespace_3d.PlaneWave(e0p=1, e0s=1)

        # - structure
        step = 20.0  # nm
        self.struct = tg.struct3d.StructDiscretizedCubic3D(
            tg.struct3d.cuboid(1, 1, 2), step, tg.materials.MatConstant(6 + 0.2j)
        )

        # - sim
        self.sim = tg.simulation.Simulation(
            structures=[self.struct],
            environment=self.env,
            illumination_fields=[self.e_inc],
            wavelengths=self.wls,
        )

    def test_class_api(self):
        for device in self.devices:
            self.sim.set_device(device)
            self.sim.run(verbose=False, progress_bar=False)

            # --- single wavelength evaluations
            r_probe = [[0, 0, 0], [150, 200, 0]]
            nf = self.sim.get_nearfield(self.wl, r_probe, progress_bar=False)
            field = nf["tot"]

            # - complex fields
            assert torch.all(field.efield == field.get_efield())
            assert torch.all(field.hfield == field.get_hfield())

            # - intensity
            intensity_e = torch.sum(torch.abs(field.efield) ** 2, dim=-1)
            intensity_h = torch.sum(torch.abs(field.hfield) ** 2, dim=-1)
            int_I_E = torch.sum(intensity_e * field.ds, dim=-1)
            int_I_H = torch.sum(intensity_h * field.ds, dim=-1)

            assert torch.all(intensity_e == field.get_efield_intensity())
            assert torch.all(intensity_h == field.get_hfield_intensity())
            assert torch.all(int_I_E == field.get_integrated_efield_intensity())
            assert torch.all(int_I_H == field.get_integrated_hfield_intensity())

            # - poynting
            poynting = torch.cross(torch.conj(field.efield), field.hfield, dim=-1)
            assert torch.all(poynting == field.get_poynting())

            # - chirality
            EHconj = torch.multiply(torch.conj(field.efield), field.hfield)
            chirality = -1 * torch.sum(EHconj.imag, dim=-1)
            assert torch.all(chirality == field.get_chirality())

    def test_add_fields(self):
        for device in self.devices:
            self.sim.set_device(device)
            self.sim.run(verbose=False, progress_bar=False)

            # --- single wavelength evaluations
            r_probe = [[0, 0, 0], [150, 200, 0]]
            nf = self.sim.get_nearfield(self.wl, r_probe, progress_bar=False)

            # - field addition - same positions (= superpose fields)
            f_tot2 = nf["sca"] + nf["inc"]
            torch.testing.assert_close(nf["tot"].efield, f_tot2.efield)
            torch.testing.assert_close(nf["tot"].hfield, f_tot2.hfield)

            # - field concatenation - several parallel field containers
            f2 = nf["sca"].cat(nf["inc"]).cat(nf["sca"])
            assert torch.all(nf["sca"].efield == f2.efield[0])
            assert torch.all(nf["inc"].efield == f2.efield[1])
            assert torch.all(nf["sca"].efield == f2.efield[2])
            assert torch.all(nf["sca"].hfield == f2.hfield[0])
            assert torch.all(nf["inc"].hfield == f2.hfield[1])
            assert torch.all(nf["sca"].hfield == f2.hfield[2])

            # - field addition - different positions (= extend)
            r_probe1 = [[0, 0, 0]]
            r_probe2 = [[150, 200, 0]]
            nf1 = self.sim.get_nearfield(self.wl, r_probe1, progress_bar=False)
            nf2 = self.sim.get_nearfield(self.wl, r_probe2, progress_bar=False)
            f_tot3 = nf1["tot"] + nf2["tot"]
            assert torch.all(nf["tot"].efield == f_tot3.efield)
            assert torch.all(nf["tot"].hfield == f_tot3.hfield)
            assert torch.all(nf["tot"].positions == f_tot3.positions)


# %%
if __name__ == "__main__":
    print("testing field class API...")
    torch.set_printoptions(precision=7)
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
