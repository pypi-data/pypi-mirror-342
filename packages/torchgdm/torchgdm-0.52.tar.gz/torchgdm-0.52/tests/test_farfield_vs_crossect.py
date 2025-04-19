# encoding=utf-8
# %%
import unittest

import torch

import torchgdm as tg


class TestFarfieldVsCrosssect(unittest.TestCase):

    def setUp(self):
        self.verbose = False
        if self.verbose:
            print("testing far-field scattering vs scattering cross-section...")

        # --- determine if GPU is available
        self.devices = ["cpu"]
        if torch.cuda.is_available():
            self.devices.append("cuda:0")

        # --- setup a test case
        # - environment
        eps_env = 1.0
        mat_env = tg.materials.MatConstant(eps_env)
        env = tg.env.freespace_3d.EnvHomogeneous3D(env_material=mat_env)

        # - illumination field(s)
        self.wavelengths = torch.tensor([532.0])
        e_inc_list = [
            tg.env.freespace_3d.PlaneWave(
                e0p=0.0, e0s=1.0, inc_angle=torch.pi / 3
            ),  # s-polarization, incidence from some angle
        ]

        # - structure
        step = 10.0
        mat_struct = tg.materials.MatConstant(eps=10.0 + 0.5j)
        struct1 = tg.struct3d.StructDiscretizedCubic3D(
            tg.struct3d.cuboid(l=5, w=10, h=3),
            step,
            mat_struct,
            radiative_correction=False,
        )

        self.sim = tg.simulation.Simulation(
            structures=[struct1],
            environment=env,
            illumination_fields=e_inc_list,
            wavelengths=self.wavelengths,
        )

    def test_farfield_vs_nearfield(self):
        for device in self.devices:
            self.sim.set_device(device)
            self.sim.run(verbose=False, progress_bar=False)

            sf_spherical = tg.tools.geometry.coordinate_map_2d_spherical(
                n_phi=18, n_teta=9
            )

            # far-field integration
            ff_res = tg.postproc.fields.ff(
                self.sim, self.wavelengths[0], sf_spherical, progress_bar=False
            )
            r_ff = ff_res["sca"]
            I_sc_ff_int = r_ff.get_integrated_efield_intensity(progress_bar=False)

            # near-field integration in far-zone (slower)
            nf_res = tg.postproc.fields.nf(
                self.sim, self.wavelengths[0], sf_spherical, progress_bar=False
            )
            r_nf = nf_res["sca"]
            I_sc_nf_int = r_nf.get_integrated_efield_intensity(progress_bar=False)

            # print(I_sc_ff_int, I_sc_nf_int)

            torch.testing.assert_close(I_sc_nf_int, I_sc_ff_int, rtol=1e-5, atol=0.1)

            if self.verbose:
                print("  - {}: far-field vs near-field test passed.".format(device))

    def test_farfield_vs_crosssections(self):
        for device in self.devices:
            self.sim.set_device(device)
            self.sim.run(verbose=False, progress_bar=False)

            # cross-section
            res_cs = tg.postproc.crosssect.total(
                self.sim, wavelength=self.wavelengths[0], progress_bar=False
            )
            scs = res_cs["scs"]

            # far-field integration
            sf_spherical = tg.tools.geometry.coordinate_map_2d_spherical(
                n_phi=360, n_teta=180
            )
            ff_res = tg.postproc.fields.ff(self.sim, self.wavelengths[0], sf_spherical, progress_bar=False)
            r_ff = ff_res["sca"]
            I_sc_int = r_ff.get_integrated_efield_intensity(progress_bar=False)

            # print(scs, I_sc_int)
            torch.testing.assert_close(scs, I_sc_int, rtol=2e-3, atol=15)

            if self.verbose:
                print(
                    "  - {}: far-field integration vs SCS test passed.".format(device)
                )


# %%

# %%
if __name__ == "__main__":
    print("testing fields postprocessing...")
    torch.set_printoptions(precision=7)
    unittest.main(argv=["first-arg-is-ignored"], exit=False)

    # t = TestFieldCalculations()
    # t.test_farfield_vs_crosssections()
