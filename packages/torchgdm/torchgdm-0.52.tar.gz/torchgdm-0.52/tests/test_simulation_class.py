# encoding=utf-8
# %%
import unittest

import torch

import torchgdm as tg


class TestSimulationClass(unittest.TestCase):

    def setUp(self):
        self.verbose = False
        if self.verbose:
            print("testing simulation class API...")

        # --- determine if GPU is available
        self.devices = ["cpu"]
        if torch.cuda.is_available():
            self.devices.append("cuda:0")

        # --- setup a test case
        # - environment
        self.env = tg.env.freespace_3d.EnvHomogeneous3D(1)

        # - illumination field(s)
        self.wls = torch.linspace(550.0, 650, 2)
        self.wl = self.wls[0]
        self.e_inc = tg.env.freespace_3d.PlaneWave(e0p=1, e0s=1)

        # - structure
        step = 20.0  # nm
        self.struct = tg.struct3d.StructDiscretizedCubic3D(
            tg.struct3d.cuboid(1, 1, 2), step, tg.materials.MatConstant(8 + 0.2j)
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
            nf2 = tg.postproc.fields.nf(self.sim, self.wl, r_probe, progress_bar=False)
            for key in ["sca", "tot", "inc"]:
                torch.testing.assert_close(nf[key].efield, nf2[key].efield)
                torch.testing.assert_close(nf[key].hfield, nf2[key].hfield)

            r_probe = [[0, 0, 10000]]
            ff = self.sim.get_farfield(self.wl, r_probe, progress_bar=False)
            ff2 = tg.postproc.fields.ff(self.sim, self.wl, r_probe, progress_bar=False)
            for key in ["sca", "tot", "inc"]:
                torch.testing.assert_close(ff[key].efield, ff2[key].efield)

            # --- spectra
            # - crosssections
            cs = self.sim.get_spectra_crosssections(progress_bar=False)
            cs2 = tg.tools.batch.calc_spectrum(
                self.sim, tg.postproc.crosssect.total, progress_bar=False
            )
            for key in ["wavelengths", "scs", "ecs", "acs"]:
                torch.testing.assert_close(cs[key], cs2[key])

            ecs = self.sim.get_spectra_ecs(progress_bar=False)
            torch.testing.assert_close(ecs["ecs"], cs2["ecs"])

            # - field intensity
            # E-field
            r_probe = [0, 0, 100]
            I_nfe = self.sim.get_spectra_nf_intensity_e(r_probe, progress_bar=False)

            I_nfe2 = tg.tools.batch.calc_spectrum(
                self.sim,
                tg.postproc.fields.integrated_nf_intensity_e,
                r_probe=r_probe,
                progress_bar=False,
            )
            for key in ["wavelengths", "sca", "tot", "inc"]:
                torch.testing.assert_close(I_nfe[key], I_nfe2[key])

            # H-field
            I_nfh = self.sim.get_spectra_nf_intensity_h(r_probe, progress_bar=False)

            I_nfh2 = tg.tools.batch.calc_spectrum(
                self.sim,
                tg.postproc.fields.integrated_nf_intensity_h,
                r_probe=r_probe,
                progress_bar=False,
            )
            for key in ["wavelengths", "sca", "tot", "inc"]:
                torch.testing.assert_close(I_nfh[key], I_nfh2[key])

            # far-field
            r_probe = [0, 0, 10000]
            I_ff = self.sim.get_spectra_ff_intensity(r_probe, progress_bar=False)
            I_ff2 = tg.tools.batch.calc_spectrum(
                self.sim,
                tg.postproc.fields.integrated_ff_intensity,
                r_probe=r_probe,
                progress_bar=False,
            )
            for key in ["wavelengths", "sca", "tot", "inc"]:
                torch.testing.assert_close(I_ff[key], I_ff2[key])

            # multipole decomposition
            mp = self.sim.get_spectra_multipole(progress_bar=False)
            mp2 = tg.tools.batch.calc_spectrum(
                self.sim, tg.postproc.multipole.decomposition_exact, progress_bar=False
            )
            for key in [
                "ed_1",
                "ed_toroidal",
                "ed_tot",
                "md",
                "eq_1",
                "eq_toroidal",
                "eq_tot",
                "mq",
                "wavelengths",
            ]:
                torch.testing.assert_close(mp[key], mp2[key])

            mp_scs = self.sim.get_spectra_multipole_scs(progress_bar=False)
            mp_scs2 = tg.tools.batch.calc_spectrum(
                self.sim, tg.postproc.multipole.scs, progress_bar=False
            )
            for key in ["scs_ed", "scs_md", "scs_eq", "scs_mq", "wavelengths"]:
                torch.testing.assert_close(mp_scs[key], mp_scs2[key])

            mp_ecs = self.sim.get_spectra_multipole_ecs(progress_bar=False)
            mp_ecs2 = tg.tools.batch.calc_spectrum(
                self.sim, tg.postproc.multipole.ecs, progress_bar=False
            )
            for key in ["ecs_ed", "ecs_md", "ecs_eq", "ecs_mq", "wavelengths"]:
                torch.testing.assert_close(mp_ecs[key], mp_ecs2[key])

            if self.verbose:
                print("  - {}: simulation class API test passed.".format(device))


# %%
if __name__ == "__main__":
    print("testing simulation class API...")
    torch.set_printoptions(precision=7)
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
