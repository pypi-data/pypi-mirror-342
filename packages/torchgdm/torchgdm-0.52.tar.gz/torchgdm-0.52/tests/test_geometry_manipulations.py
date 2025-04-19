# encoding=utf-8
# %%
import unittest

import torch

import torchgdm as tg


class TestStructureRotation2D(unittest.TestCase):

    def setUp(self):
        self.verbose = False
        if self.verbose:
            print("testing structure rotations - 2D...")

        # --- determine if GPU is available
        self.devices = ["cpu"]
        if torch.cuda.is_available():
            self.devices.append("cuda:0")

        self.angles = torch.as_tensor([0, 90, 237.5])

        # --- setup a test case
        # - environment
        mat_env = tg.materials.MatConstant(eps=1.0)
        self.env = tg.env.freespace_2d.EnvHomogeneous2D(env_material=mat_env)

        # - illumination field(s)
        self.wl = torch.as_tensor(620.0)
        self.wavelengths = torch.as_tensor([self.wl])
        self.e_inc_list = [
            tg.env.freespace_2d.PlaneWave(e0p=1, e0s=1, inc_angle=angle)
            for angle in self.angles
        ]

        # - structure
        step = 20.0  # nm
        mat_struct = tg.materials.MatConstant(8 + 0.2j)
        self.struct = tg.struct2d.StructDiscretizedSquare2D(
            tg.struct2d.rectangle(5, 2),
            step,
            mat_struct,
            radiative_correction=False,
        )

    def test_rotate_discretized(self):
        for device in self.devices:
            self.struct.set_device(device)

            sim_full = tg.simulation.Simulation(
                structures=[self.struct],
                environment=self.env,
                illumination_fields=[self.e_inc_list[0]],
                wavelengths=self.wavelengths,
                device=device,
            )
            sim_full.run(verbose=False, progress_bar=False)
            cs_full_0 = tg.postproc.crosssect.total(sim_full, self.wl)

            # rotate structure and illumination polarization angle and compare
            for i_alpha, alpha in enumerate(self.angles[1:]):
                _sim_f = tg.simulation.Simulation(
                    structures=[self.struct.rotate(alpha)],
                    environment=self.env,
                    illumination_fields=[self.e_inc_list[i_alpha + 1]],
                    wavelengths=self.wavelengths,
                    device=device,
                )

                # run rotated simulation
                _sim_f.run(verbose=False, progress_bar=False)

                # compare scat / extinct of full and effective pola. simulations
                _cs_f = tg.postproc.crosssect.total(_sim_f, self.wl)

                torch.testing.assert_close(
                    cs_full_0["scs"], _cs_f["scs"], atol=1e-3, rtol=1e-5
                )
                torch.testing.assert_close(
                    cs_full_0["ecs"], _cs_f["ecs"], atol=1e-3, rtol=1e-5
                )

            if self.verbose:
                print(
                    "  - {}: discretized 2D structure rotation test passed.".format(
                        device
                    )
                )


class TestStructureTranslation2D(unittest.TestCase):

    def setUp(self):
        self.verbose = False
        if self.verbose:
            print("testing strucure copy / combining - 2D...")

        # --- determine if GPU is available
        self.devices = ["cpu"]
        if torch.cuda.is_available():
            self.devices.append("cuda:0")

        self.angles = torch.as_tensor([0, 23.7])

        # --- setup a test case
        # - environment
        mat_env = tg.materials.MatConstant(eps=1.0)
        self.env = tg.env.freespace_2d.EnvHomogeneous2D(env_material=mat_env)

        # - illumination field(s)
        self.wl = torch.as_tensor(700.0)
        self.wavelengths = torch.as_tensor([self.wl])
        self.e_inc_list = [
            tg.env.freespace_2d.PlaneWave(e0p=torch.cos(angle), e0s=torch.sin(angle))
            for angle in self.angles
        ]

        # - structure
        step = 25.0  # nm
        mat_struct = tg.materials.MatConstant(6.5 + 0.1j)
        self.struct = tg.struct2d.StructDiscretizedSquare2D(
            tg.struct2d.rectangle(5, 3),
            step,
            mat_struct,
            radiative_correction=False,
        )

        # - combined simulation config
        self.sim_conf = dict(
            environment=self.env,
            illumination_fields=self.e_inc_list,
            wavelengths=self.wavelengths,
        )

    def test_translate_copy(self):
        pos1 = [250, 0, 150]
        pos2 = [0, 0, 50]
        for device in self.devices:
            self.struct.set_device(device)

            sim_1 = tg.simulation.Simulation(
                structures=[self.struct + pos1, self.struct + pos2],
                device=device,
                **self.sim_conf,
            )
            sim_1.run(verbose=False, progress_bar=False)
            cs_full_1 = tg.postproc.crosssect.total(sim_1, self.wl)

            sim_2 = tg.simulation.Simulation(
                structures=[self.struct.copy([pos1, pos2])],
                device=device,
                **self.sim_conf,
            )
            sim_2.run(verbose=False, progress_bar=False)
            cs_full_2 = tg.postproc.crosssect.total(sim_2, self.wl)

            torch.testing.assert_close(
                cs_full_1["scs"], cs_full_2["scs"], atol=1e1, rtol=1e-5
            )
            torch.testing.assert_close(
                cs_full_1["ecs"], cs_full_2["ecs"], atol=1e1, rtol=1e-5
            )

        if self.verbose:
            print(
                "  - {}: discretized 2D structure copy / translate test passed.".format(
                    device
                )
            )

    def test_combine(self):
        pos1 = [250, 0, 150]
        pos2 = [0, 0, 50]
        for device in self.devices:
            self.struct.set_device(device)

            sim_1 = tg.simulation.Simulation(
                structures=[self.struct + pos1],
                device=device,
                **self.sim_conf,
            )
            sim_2 = tg.simulation.Simulation(
                structures=[self.struct + pos2],
                device=device,
                **self.sim_conf,
            )

            # - combined sim / combine struct
            sim_combo1 = tg.simulation.Simulation(
                structures=[self.struct + pos1, self.struct + pos2],
                device=device,
                **self.sim_conf,
            )
            sim_combo2 = sim_1.combine(sim_2)

            # - run and compare results
            sim_combo1.run(verbose=False, progress_bar=False)
            sim_combo2.run(verbose=False, progress_bar=False)

            cs_full_1 = tg.postproc.crosssect.total(sim_combo1, self.wl)
            cs_full_2 = tg.postproc.crosssect.total(sim_combo2, self.wl)

            torch.testing.assert_close(
                cs_full_1["scs"], cs_full_2["scs"], atol=1e1, rtol=1e-5
            )
            torch.testing.assert_close(
                cs_full_1["ecs"], cs_full_2["ecs"], atol=1e1, rtol=1e-5
            )

        if self.verbose:
            print(
                "  - {}: discretized 2D simulation combine test passed.".format(device)
            )


class TestStructureRotation3D(unittest.TestCase):

    def setUp(self):
        self.verbose = False
        if self.verbose:
            print("testing structure rotations...")

        # --- determine if GPU is available
        self.devices = ["cpu"]
        if torch.cuda.is_available():
            self.devices.append("cuda:0")

        self.angles = torch.as_tensor([0, 90, 237.5])

        # --- setup a test case
        # - environment
        mat_env = tg.materials.MatConstant(eps=1.0)
        self.env = tg.env.freespace_3d.EnvHomogeneous3D(env_material=mat_env)

        # - illumination field(s)
        self.wl = torch.as_tensor(700.0)
        self.wavelengths = torch.as_tensor([self.wl])
        self.e_inc_list = [
            tg.env.freespace_3d.PlaneWave(e0p=torch.cos(angle), e0s=torch.sin(angle))
            for angle in self.angles
        ]

        # - structure
        step = 15.0  # nm
        mat_struct = tg.materials.MatDatabase("Au")
        self.struct = tg.struct3d.StructDiscretizedCubic3D(
            tg.struct3d.cuboid(5, 2, 2),
            step,
            mat_struct,
            radiative_correction=False,
        )

    def test_rotate_discretized(self):
        for device in self.devices:
            self.struct.set_device(device)

            sim_full = tg.simulation.Simulation(
                structures=[self.struct],
                environment=self.env,
                illumination_fields=[self.e_inc_list[0]],
                wavelengths=self.wavelengths,
                device=device,
            )
            sim_full.run(verbose=False, progress_bar=False)
            cs_full_0 = tg.postproc.crosssect.total(sim_full, self.wl)

            # rotate structure and illumination polarization angle and compare
            for i_alpha, alpha in enumerate(self.angles[1:]):
                _sf = self.struct.rotate(alpha)
                _sim_f = tg.simulation.Simulation(
                    structures=[_sf],
                    environment=self.env,
                    illumination_fields=[self.e_inc_list[i_alpha + 1]],
                    wavelengths=self.wavelengths,
                    device=device,
                )

                # run rotated simulation
                _sim_f.run(verbose=False, progress_bar=False)

                # compare scat / extinct of full and effective pola. simulations
                _cs_f = tg.postproc.crosssect.total(_sim_f, self.wl)

                torch.testing.assert_close(
                    cs_full_0["scs"], _cs_f["scs"], atol=1e1, rtol=1e-5
                )
                torch.testing.assert_close(
                    cs_full_0["ecs"], _cs_f["ecs"], atol=1e1, rtol=1e-5
                )

            if self.verbose:
                print(
                    "  - {}: discretized structure rotation test passed.".format(device)
                )

    def test_rotate_polarizability(self):
        for device in self.devices:
            self.struct.set_device(device)

            struct_alpha = self.struct.convert_to_effective_polarizability_pair(
                self.wavelengths,
                environment=self.env,
                verbose=False,
                progress_bar=False,
            )
            sim_aeff = tg.simulation.Simulation(
                structures=[self.struct],
                environment=self.env,
                illumination_fields=[self.e_inc_list[0]],
                wavelengths=self.wavelengths,
                device=device,
            )
            sim_aeff.run(verbose=False, progress_bar=False)
            cs_aeff_0 = tg.postproc.crosssect.total(sim_aeff, self.wl)

            # rotate structure and illumination polarization angle and compare
            for i_alpha, alpha in enumerate(self.angles[1:]):
                _sa = struct_alpha.rotate(alpha)
                _sim_a = tg.simulation.Simulation(
                    structures=[_sa],
                    environment=self.env,
                    illumination_fields=[self.e_inc_list[i_alpha + 1]],
                    wavelengths=self.wavelengths,
                    device=device,
                )

                # run rotated simulation
                _sim_a.run(verbose=False, progress_bar=False)

                # compare scat / extinct of full and effective pola. simulations
                _cs_a = tg.postproc.crosssect.total(_sim_a, self.wl)

                torch.testing.assert_close(
                    cs_aeff_0["scs"], _cs_a["scs"], atol=1e3, rtol=1e-2
                )
                torch.testing.assert_close(
                    cs_aeff_0["ecs"], _cs_a["ecs"], atol=1e3, rtol=1e-2
                )

            if self.verbose:
                print(
                    "  - {}: effective polarizability structure rotation test passed.".format(
                        device
                    )
                )


class TestStructureTranslation3D(unittest.TestCase):

    def setUp(self):
        self.verbose = False
        if self.verbose:
            print("testing strucure copy / combining...")

        # --- determine if GPU is available
        self.devices = ["cpu"]
        if torch.cuda.is_available():
            self.devices.append("cuda:0")

        self.angles = torch.as_tensor([0, 23.7])

        # --- setup a test case
        # - environment
        mat_env = tg.materials.MatConstant(eps=1.0)
        self.env = tg.env.freespace_3d.EnvHomogeneous3D(env_material=mat_env)

        # - illumination field(s)
        self.wl = torch.as_tensor(700.0)
        self.wavelengths = torch.as_tensor([self.wl])
        self.e_inc_list = [
            tg.env.freespace_3d.PlaneWave(e0p=torch.cos(angle), e0s=torch.sin(angle))
            for angle in self.angles
        ]

        # - structure
        step = 25.0  # nm
        mat_struct = tg.materials.MatDatabase("Al")
        self.struct = tg.struct3d.StructDiscretizedCubic3D(
            tg.struct3d.cuboid(3, 2, 2),
            step,
            mat_struct,
            radiative_correction=False,
        )

        self.struct_pola = self.struct.convert_to_effective_polarizability_pair(
            self.wavelengths, environment=self.env, verbose=False, progress_bar=False
        )

        # - combined simulation config
        self.sim_conf = dict(
            environment=self.env,
            illumination_fields=self.e_inc_list,
            wavelengths=self.wavelengths,
        )

    def test_translate_copy(self):
        pos1 = [250, 50, 150]
        pos2 = [0, -50, 50]
        for device in self.devices:
            for struct in [self.struct, self.struct_pola]:
                struct.set_device(device)

                sim_1 = tg.simulation.Simulation(
                    structures=[struct + pos1, struct + pos2],
                    device=device,
                    **self.sim_conf,
                )
                sim_1.run(verbose=False, progress_bar=False)
                cs_full_1 = tg.postproc.crosssect.total(sim_1, self.wl)

                sim_2 = tg.simulation.Simulation(
                    structures=[struct.copy([pos1, pos2])],
                    device=device,
                    **self.sim_conf,
                )
                sim_2.run(verbose=False, progress_bar=False)
                cs_full_2 = tg.postproc.crosssect.total(sim_2, self.wl)

                torch.testing.assert_close(
                    cs_full_1["scs"], cs_full_2["scs"], atol=1e1, rtol=1e-5
                )
                torch.testing.assert_close(
                    cs_full_1["ecs"], cs_full_2["ecs"], atol=1e1, rtol=1e-5
                )

            if self.verbose:
                print("  - {}: structure copy / translate test passed.".format(device))

    def test_combine(self):
        pos1 = [250, 20, 150]
        pos2 = [0, -83, 50]
        for device in self.devices:
            for struct in [self.struct, self.struct_pola]:
                struct.set_device(device)

                sim_1 = tg.simulation.Simulation(
                    structures=[struct + pos1],
                    device=device,
                    **self.sim_conf,
                )
                sim_2 = tg.simulation.Simulation(
                    structures=[struct + pos2],
                    device=device,
                    **self.sim_conf,
                )

                # - combined sim / combine struct
                sim_combo1 = tg.simulation.Simulation(
                    structures=[struct + pos1, struct + pos2],
                    device=device,
                    **self.sim_conf,
                )
                sim_combo2 = sim_1.combine(sim_2)

                # - run and compare results
                sim_combo1.run(verbose=False, progress_bar=False)
                sim_combo2.run(verbose=False, progress_bar=False)

                cs_full_1 = tg.postproc.crosssect.total(sim_combo1, self.wl)
                cs_full_2 = tg.postproc.crosssect.total(sim_combo2, self.wl)

                torch.testing.assert_close(
                    cs_full_1["scs"], cs_full_2["scs"], atol=1e1, rtol=1e-5
                )
                torch.testing.assert_close(
                    cs_full_1["ecs"], cs_full_2["ecs"], atol=1e1, rtol=1e-5
                )

        if self.verbose:
            print(
                "  - {}: discretized 3D simulation combine test passed.".format(device)
            )


# %%
if __name__ == "__main__":
    print("testing structure rotation...")
    torch.set_printoptions(precision=7)
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
