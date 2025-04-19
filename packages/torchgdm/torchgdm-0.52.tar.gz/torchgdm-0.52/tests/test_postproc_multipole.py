# encoding=utf-8
# %%
import unittest

import torch

import torchgdm as tg


class TestSimCrossSections(unittest.TestCase):

    def setUp(self):
        self.verbose = False
        if self.verbose:
            print("testing multipole decomposition...")

        # --- determine if GPU is available
        self.devices = ["cpu"]
        if torch.cuda.is_available():
            self.devices.append("cuda:0")

        # --- setup a test case
        # - environment
        eps_env = 1.0
        mat_env = tg.materials.MatConstant(eps_env)
        self.env = tg.env.freespace_3d.EnvHomogeneous3D(env_material=mat_env)

        # - illumination field(s)
        self.wl = torch.as_tensor(720.0)
        self.wavelengths = torch.as_tensor([self.wl])
        self.e_inc_list = [
            tg.env.freespace_3d.PlaneWave(e0p=1.0, e0s=0.0, inc_angle=0),
        ]

        # - structure
        step = 33.0  # nm
        mat_struct = tg.materials.MatConstant(eps=12.0)
        self.struct1 = tg.struct3d.StructDiscretizedCubic3D(
            tg.struct3d.cuboid(3, 3, 2),
            step,
            mat_struct,
            radiative_correction=False,
        )

        self.sim = tg.simulation.Simulation(
            structures=[self.struct1],
            environment=self.env,
            illumination_fields=self.e_inc_list,
            wavelengths=self.wavelengths,
        )

    def test_effective_polarizability(self):
        for device in self.devices:
            self.sim.set_device(device)
            # random seed for reproducible extraction (based on rnd dipole sources)
            torch.manual_seed(1)

            # extract effective ed/md polarizabilities
            a_tgdm = tg.struct3d.extract_eff_pola_via_exact_mp_3d(
                self.struct1,
                self.wavelengths,
                environment=self.env, 
                verbose=False,
                progress_bar=False,
            )

            # create equivalent effective pola simulation
            struct_eff = tg.struct3d.StructEffPola3D(
                a_tgdm["r0"].unsqueeze(0), a_tgdm
            )
            sim_aeff = tg.Simulation(
                structures=[struct_eff],
                environment=self.env,
                illumination_fields=self.e_inc_list,
                wavelengths=self.wavelengths,
                device=device,
            )

            # run both simulations
            self.sim.run(verbose=False, progress_bar=False)
            sim_aeff.run(verbose=False, progress_bar=False)

            # --- compare scat/extinct of full and effective pola. simulations
            cs_full = tg.postproc.crosssect.total(self.sim, self.wl)
            cs_aeff = tg.postproc.crosssect.total(sim_aeff, self.wl)
            # print(cs_f2ull["scs"], cs_aeff["scs"])
            # print(cs_full["ecs"], cs_aeff["ecs"])

            torch.testing.assert_close(
                cs_full["scs"], cs_aeff["scs"], atol=1e4, rtol=2e-2
            )
            torch.testing.assert_close(
                cs_full["ecs"], cs_aeff["ecs"], atol=1e4, rtol=2e-2
            )

            if self.verbose:
                print(
                    "  - {}: effective polarizability extraction test passed.".format(
                        device
                    )
                )

            # --- compare total scat/extinct with mutlipole sum
            mp_full_s = tg.postproc.multipole.scs(self.sim, self.wl)
            scs_ed = mp_full_s["scs_ed"]
            scs_md = mp_full_s["scs_md"]
            scs_eq = mp_full_s["scs_eq"]
            scs_mq = mp_full_s["scs_mq"]
            scs_mp_sum = scs_ed + scs_md + scs_eq + scs_mq

            mp_full_e = tg.postproc.multipole.ecs(self.sim, self.wl)
            ecs_ed = mp_full_e["ecs_ed"]
            ecs_md = mp_full_e["ecs_md"]
            ecs_eq = mp_full_e["ecs_eq"]
            ecs_mq = mp_full_e["ecs_mq"]
            ecs_mp_sum = ecs_ed + ecs_md + ecs_eq + ecs_mq
            # print(cs_full["scs"], scs_mp_sum)
            # print(cs_full["ecs"], ecs_mp_sum)

            torch.testing.assert_close(
                cs_full["scs"], scs_mp_sum, atol=5e3, rtol=1e-2
            )
            torch.testing.assert_close(
                cs_full["ecs"], ecs_mp_sum, atol=5e3, rtol=1e-2
            )

            if self.verbose:
                print("  - {}: multipole sum test passed.".format(device))


# %%
if __name__ == "__main__":
    print("testing exact multipole decomposition...")
    torch.set_printoptions(precision=7)
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
