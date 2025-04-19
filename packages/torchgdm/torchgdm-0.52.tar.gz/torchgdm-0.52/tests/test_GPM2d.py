# encoding: utf-8
"""
unittests for global polarizability matrix (GPM)

todo:
  - test accuracy (vs Mie?)
  - test combine of GPM structures

author: P. Wiecha, 04/2025
"""

# %%
import warnings
import unittest

import torch
import numpy as np

# deterministinc randomness (reproducible eff. model extraction)
torch.manual_seed(42)

import torchgdm as tg

SEED = 123


class TestSim3DSplitCombine(unittest.TestCase):

    def setUp(self):
        self.verbose = False
        if self.verbose:
            print("test splitting and combining simulations...")

        # --- determine if GPU is available
        self.devices = ["cpu"]
        if torch.cuda.is_available():
            self.devices.append("cuda:0")

        # --- setup a test case
        self.wls = torch.linspace(450.0, 750.0, 2)
        self.env = tg.env.EnvHomogeneous2D(env_material=1.0)
        self.inc = tg.env.freespace_2d.PlaneWave(
            e0p=0.71, e0s=0.71, inc_angle=torch.pi / 6
        )

        # - discretized structure
        self.struct = tg.struct2d.StructDiscretizedSquare2D(
            discretization_config=tg.struct2d.rectangle(l=25, h=10),
            step=10,
            materials=tg.materials.MatConstant(eps=16),
        )

    def test_gpm_vs_effpola_model(self):
        for device in self.devices:
            # small structure that with dipolar response
            struct = tg.struct2d.StructDiscretizedSquare2D(
                discretization_config=tg.struct2d.rectangle(l=5, h=4),
                step=10,
                materials=tg.materials.MatConstant(eps=16),
            )
            struct.set_device(device)

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")

                torch.manual_seed(SEED)
                np.random.seed(SEED)
                s_eff1 = struct.convert_to_effective_polarizability_pair(
                    self.wls,
                    environment=self.env,
                    verbose=False,
                    progress_bar=False,
                    test_accuracy=False,
                    residual_warning_threshold=1000,
                )

                n_gpm_dp = 1
                torch.manual_seed(SEED)
                np.random.seed(SEED)
                s_gpm1 = struct.convert_to_gpm(
                    self.wls,
                    n_gpm_dp,
                    environment=self.env,
                    verbose=False,
                    progress_bar=False,
                    test_accuracy=False,
                    residual_warning_threshold=1000,
                )

            sim_conf = dict(
                illumination_fields=self.inc, environment=self.env, wavelengths=self.wls
            )
            sim_gpm = tg.Simulation(structures=s_gpm1, **sim_conf)
            sim_gpm.run(verbose=False, progress_bar=False)

            sim_effdp = tg.Simulation(structures=s_eff1, **sim_conf)
            sim_effdp.run(verbose=False, progress_bar=False)

            wl = self.wls[0]
            r_probe = tg.tools.geometry.coordinate_map_2d_square(1000, 5, r3=100)

            nf_eff = sim_effdp.get_nearfield(wl, r_probe, progress_bar=False)["sca"]
            nf_gpm = sim_gpm.get_nearfield(wl, r_probe, progress_bar=False)["sca"]

            # single dipole GPM similar should give very result as eff-dipole extraction
            # print((nf_eff.efield).abs())
            # print((nf_gpm.efield).abs())
            # print((nf_eff.efield - nf_gpm.efield).abs().mean())
            assert (nf_eff.efield - nf_gpm.efield).abs().mean() < 0.001

    def test_gpm_translation(self):
        for device in self.devices:

            struct_a = self.struct.copy()
            struct_a.set_device(device)

            shift = [200, 0, 200]
            struct_b = self.struct.copy()
            struct_b.set_device(device)
            struct_b = struct_b + shift  # shift the discretized structure

            # manually define effective dipole positions
            r_gpm_0 = torch.as_tensor(
                [[float(x), 0, 0] for x in np.linspace(-100, 100, 5)], device=device
            )

            conf = dict(
                wavelengths=self.wls,
                verbose=False,
                environment=self.env,
                progress_bar=False,
                test_accuracy=False,
                residual_warning_threshold=1000,
                n_dipole_sources=0,  # optimize far-field illumination for testing
            )

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")

                r_gpm_a = r_gpm_0 + struct_a.r0
                torch.manual_seed(SEED)
                np.random.seed(SEED)
                s_gpm_a = struct_a.convert_to_gpm(r_gpm=r_gpm_a, **conf)
                s_gpm_a = s_gpm_a + shift  # shift the GPM structure

                r_gpm_b = r_gpm_0 + struct_b.r0
                torch.manual_seed(SEED)
                np.random.seed(SEED)
                # convert the shifted discretization
                s_gpm_b = struct_b.convert_to_gpm(r_gpm=r_gpm_b, **conf)

                # run simulations
                sim_conf = dict(
                    illumination_fields=self.inc,
                    environment=self.env,
                    wavelengths=self.wls,
                )
                sim_gpm_a = tg.Simulation(structures=s_gpm_a, **sim_conf)
                sim_gpm_b = tg.Simulation(structures=s_gpm_b, **sim_conf)
                sim_gpm_a.run(verbose=False, progress_bar=False)
                sim_gpm_b.run(verbose=False, progress_bar=False)

                # compare fields
                r_probe = tg.tools.geometry.coordinate_map_2d_square(500, 3, r3=800)
                for wl in self.wls:
                    nf1 = sim_gpm_a.get_nearfield(wl, r_probe, progress_bar=False)[
                        "sca"
                    ]
                    nf2 = sim_gpm_b.get_nearfield(wl, r_probe, progress_bar=False)[
                        "sca"
                    ]
                    # print(nf1.efield)
                    # print(nf2.efield)
                    # print((nf1.efield-nf2.efield).abs())
                    torch.testing.assert_close(
                        nf1.efield, nf2.efield, atol=1e-4, rtol=1e-5
                    )
                    torch.testing.assert_close(
                        nf1.hfield, nf2.hfield, atol=1e-4, rtol=1e-5
                    )

    def test_gpm_rotation(self):
        for device in self.devices:

            struct_a = self.struct.copy()
            struct_a.set_center_of_mass([0, 0, 0])
            struct_a.set_device(device)

            rotation_angle = torch.pi / 2
            struct_b = self.struct.copy()
            struct_b.set_center_of_mass([0, 0, 0])
            struct_b.set_device(device)
            struct_b = struct_b.rotate(
                rotation_angle, axis="y"
            )  # rotate the discretized struct

            # manually define effective dipole positions
            r_gpm = torch.as_tensor(
                [[float(x), 0, 0] for x in np.linspace(-100, 100, 10)], device=device
            )

            conf = dict(
                wavelengths=self.wls,
                verbose=False,
                environment=self.env,
                progress_bar=False,
                test_accuracy=False,
                residual_warning_threshold=1000,
                n_dipole_sources=0,  # optimize far-field illumination for testing
            )

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")

                r_gpm_a = r_gpm + struct_a.r0
                torch.manual_seed(SEED)
                np.random.seed(SEED)
                s_gpm_a = struct_a.convert_to_gpm(r_gpm=r_gpm_a, **conf)
                s_gpm_a = s_gpm_a.rotate(
                    rotation_angle, axis="y"
                )  # rotate the GPM struct

                # conv rotated discr. struct
                r_gpm_b = r_gpm + struct_b.r0
                rot_y = tg.tools.geometry.rotation_y(rotation_angle).to(device)
                r_gpm_b = torch.matmul(r_gpm_b, rot_y)
                torch.manual_seed(SEED)
                np.random.seed(SEED)
                s_gpm_b = struct_b.convert_to_gpm(r_gpm=r_gpm_b, **conf)

                # run simulations
                sim_conf = dict(
                    illumination_fields=self.inc,
                    environment=self.env,
                    wavelengths=self.wls,
                )
                sim_gpm_a = tg.Simulation(structures=s_gpm_a, **sim_conf)
                sim_gpm_b = tg.Simulation(structures=s_gpm_b, **sim_conf)
                sim_gpm_a.run(verbose=False, progress_bar=False)
                sim_gpm_b.run(verbose=False, progress_bar=False)

                # compare fields
                r_probe = tg.tools.geometry.coordinate_map_2d_square(
                    600, 3, r3=800, projection="xy"
                )
                for wl in self.wls:
                    nf1 = sim_gpm_a.get_nearfield(wl, r_probe, progress_bar=False)[
                        "sca"
                    ]
                    nf2 = sim_gpm_b.get_nearfield(wl, r_probe, progress_bar=False)[
                        "sca"
                    ]
                    # print(nf1.efield.abs())
                    # print(nf2.efield.abs())
                    # print((nf1.efield-nf2.efield).abs())
                    torch.testing.assert_close(
                        nf1.efield, nf2.efield, atol=0.005, rtol=0.5
                    )
                    torch.testing.assert_close(
                        nf1.hfield, nf2.hfield, atol=0.005, rtol=0.5
                    )

    def test_gpm_combine(self):
        for device in self.devices:

            struct_a = self.struct.copy()
            struct_a.set_device(device)

            struct_b = self.struct.copy()
            struct_b.set_device(device)

            # manually define effective dipole positions
            r_gpm_0 = torch.as_tensor(
                [[float(x), 0, 0] for x in np.linspace(-100, 100, 10)], device=device
            )

            conf = dict(
                wavelengths=self.wls,
                verbose=False,
                environment=self.env,
                progress_bar=False,
                test_accuracy=False,
                residual_warning_threshold=1000,
                n_dipole_sources=0,  # optimize far-field illumination for testing
            )

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")

                r_gpm_a = r_gpm_0 + struct_a.r0
                torch.manual_seed(SEED)
                np.random.seed(SEED)
                s_gpm_a = struct_a.convert_to_gpm(r_gpm=r_gpm_a, **conf)
                s_gpm_a = s_gpm_a + [200, 0, 200]

                r_gpm_b = r_gpm_0 + struct_b.r0
                torch.manual_seed(SEED)
                np.random.seed(SEED)
                s_gpm_b = struct_b.convert_to_gpm(r_gpm=r_gpm_b, **conf)

                # run simulations
                sim_conf = dict(
                    illumination_fields=self.inc,
                    environment=self.env,
                    wavelengths=self.wls,
                )
                sim_gpm_a = tg.Simulation(structures=[s_gpm_a, s_gpm_b], **sim_conf)
                sim_gpm_b = tg.Simulation(structures=s_gpm_a + s_gpm_b, **sim_conf)
                sim_gpm_a.run(verbose=False, progress_bar=False)
                sim_gpm_b.run(verbose=False, progress_bar=False)

                # compare fields
                r_probe = tg.tools.geometry.coordinate_map_2d_square(1000, 3, r3=500)
                for wl in self.wls:
                    nf1 = sim_gpm_a.get_nearfield(wl, r_probe, progress_bar=False)[
                        "sca"
                    ]
                    nf2 = sim_gpm_b.get_nearfield(wl, r_probe, progress_bar=False)[
                        "sca"
                    ]
                    # print(nf1.efield)
                    # print(nf2.efield)
                    # print((nf1.efield-nf2.efield).abs())
                    torch.testing.assert_close(
                        nf1.efield, nf2.efield, atol=1e-4, rtol=1e-5
                    )
                    torch.testing.assert_close(
                        nf1.hfield, nf2.hfield, atol=1e-4, rtol=1e-5
                    )


# %%
if __name__ == "__main__":
    print("testing 2D global polarizability matrix manipulations...")
    torch.set_printoptions(precision=7)
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
