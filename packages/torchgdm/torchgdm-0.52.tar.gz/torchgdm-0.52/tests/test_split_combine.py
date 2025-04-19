# encoding=utf-8
# %%
import unittest

import torch

import torchgdm as tg


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
        # - environment
        eps_env = 1.0
        mat_env = tg.materials.MatConstant(eps_env)
        self.env = tg.env.freespace_3d.EnvHomogeneous3D(env_material=mat_env)

        # - illumination field(s)
        self.wl = 733.0
        self.e_inc_list = [
            tg.env.freespace_3d.PlaneWave(e0p=0.8, e0s=1.0, inc_angle=torch.pi / 3),
        ]

        # - structure
        step = 25.0
        mat = tg.materials.MatDatabase("gaas")
        self.s1 = tg.struct3d.StructDiscretizedCubic3D(
            tg.struct3d.cuboid(l=2, w=1, h=1),
            step,
            mat,
        )
        step = 15.0
        mat = tg.materials.MatDatabase("Si")
        self.s2 = tg.struct3d.StructDiscretizedCubic3D(
            tg.struct3d.cuboid(l=1, w=2, h=1),
            step,
            mat,
        )

        self.sim_conf = dict(
            environment=self.env,
            illumination_fields=self.e_inc_list,
            wavelengths=torch.tensor([self.wl]),
        )

    def test_combine_sim_struct(self):
        for device in self.devices:
            s1 = self.s1 - [100, 200, 50]
            s2 = self.s2 + [100, -50, 150]
            sim1 = tg.simulation.Simulation(
                structures=[s1], device=device, **self.sim_conf
            )
            sim2 = tg.simulation.Simulation(
                structures=[s2], device=device, **self.sim_conf
            )
            # combine the two structures / simulations in different ways
            sim_comb_list = []
            sim_comb_list.append(
                tg.simulation.Simulation(
                    structures=[s1, s2], device=device, **self.sim_conf
                )
            )
            sim_comb_list.append(
                tg.simulation.Simulation(
                    structures=[s1.combine(s2)], device=device, **self.sim_conf
                )
            )
            sim_comb_list.append(
                tg.simulation.Simulation(
                    structures=[s1 + s2], device=device, **self.sim_conf
                )
            )
            sim_comb_list.append(sim1 + sim2)
            sim_comb_list.append(sim1.combine(sim2))

            # test if combined simulations are same
            for _s1 in sim_comb_list:
                for _s2 in sim_comb_list:
                    torch.testing.assert_close(
                        _s1.get_all_positions(), _s2.get_all_positions()
                    )
                    torch.testing.assert_close(
                        _s1.get_source_validity_radius(), _s2.get_source_validity_radius()
                    )
                    torch.testing.assert_close(
                        _s1._get_all_polarizabilitites_6x6(self.wl),
                        _s2._get_all_polarizabilitites_6x6(self.wl),
                    )

    def test_run_seperate_and_combined(self):
        for device in self.devices:

            self.s1.set_center_of_mass([-100, 0, 0])
            self.s2.set_center_of_mass([100, 50, 0])

            sim1 = tg.simulation.Simulation(
                structures=[self.s1, self.s2],
                device=device,
                **self.sim_conf,
            )
            sim1.run(calc_missing=True, verbose=False, progress_bar=False)

            sim2 = tg.simulation.Simulation(
                structures=[self.s1 + self.s2],
                device=device,
                **self.sim_conf,
            )
            sim2.run(calc_missing=True, verbose=False, progress_bar=False)

            torch.testing.assert_close(
                sim1.fields_inside[self.wl].efield,
                sim2.fields_inside[self.wl].efield,
            )

            torch.testing.assert_close(
                sim1.fields_inside[self.wl].hfield,
                sim2.fields_inside[self.wl].hfield,
            )

            if self.verbose:
                print("  - {}: list vs combined struct 3D sim test passed.".format(device))

    def test_calculate_E_H(self):
        for device in self.devices:

            self.s1.set_center_of_mass([-100, 0, 0])
            self.s2.set_center_of_mass([100, 50, 0])

            sim = tg.simulation.Simulation(
                structures=[self.s1, self.s2],
                device=device,
                **self.sim_conf,
            )

            sim.run(calc_missing=True, verbose=False, progress_bar=False)

            # test split/combine
            s_split0 = sim.split(0)
            s_split1 = sim.split(1)
            s_comb = s_split0.combine(s_split1)

            torch.testing.assert_close(
                sim.fields_inside[self.wl].efield,
                s_comb.fields_inside[self.wl].efield,
            )

            torch.testing.assert_close(
                sim.fields_inside[self.wl].hfield,
                s_comb.fields_inside[self.wl].hfield,
            )

            # test delete
            s0_delete = sim.delete_struct(1)
            s1_delete = sim.delete_struct(0)

            torch.testing.assert_close(
                s_split0.fields_inside[self.wl].efield,
                s0_delete.fields_inside[self.wl].efield,
            )

            torch.testing.assert_close(
                s_split1.fields_inside[self.wl].hfield,
                s1_delete.fields_inside[self.wl].hfield,
            )

            if self.verbose:
                print("  - {}: split combine 3D sim test passed.".format(device))


class TestSim2DSplitCombine(unittest.TestCase):

    def setUp(self):
        self.verbose = False
        if self.verbose:
            print("test splitting and combining simulations...")

        # --- determine if GPU is available
        self.devices = ["cpu"]
        if torch.cuda.is_available():
            self.devices.append("cuda:0")

        # --- setup a test case
        # - environment
        eps_env = 1.0
        mat_env = tg.materials.MatConstant(eps_env)
        self.env = tg.env.freespace_2d.EnvHomogeneous2D(env_material=mat_env)

        # - illumination field(s)
        self.wl = 670.0
        self.e_inc_list = [
            tg.env.freespace_2d.PlaneWave(
                e0p=0.9j, e0s=0.4, inc_angle=-torch.pi / 1.55
            ),
        ]

        # - structure
        step = 25.0
        mat = tg.materials.MatDatabase("gap")
        self.s1 = tg.struct2d.StructDiscretizedSquare2D(
            tg.struct2d.rectangle(l=3, h=2), step, mat
        )
        step = 20.0
        mat = tg.materials.MatDatabase("ge")
        self.s2 = tg.struct2d.StructDiscretizedSquare2D(
            tg.struct2d.rectangle(l=1, h=3), step, mat
        )

        self.sim_conf = dict(
            environment=self.env,
            illumination_fields=self.e_inc_list,
            wavelengths=torch.tensor([self.wl]),
        )

    def test_combine_sim_struct(self):
        for device in self.devices:
            s1 = self.s1 - [100, 0, 50]
            s2 = self.s2 + [100, 0, 150]
            sim1 = tg.simulation.Simulation(
                structures=[s1], device=device, **self.sim_conf
            )
            sim2 = tg.simulation.Simulation(
                structures=[s2], device=device, **self.sim_conf
            )
            # combine the two structures / simulations in different ways
            sim_comb_list = []
            sim_comb_list.append(
                tg.simulation.Simulation(
                    structures=[s1, s2], device=device, **self.sim_conf
                )
            )
            sim_comb_list.append(
                tg.simulation.Simulation(
                    structures=[s1.combine(s2)], device=device, **self.sim_conf
                )
            )
            sim_comb_list.append(
                tg.simulation.Simulation(
                    structures=[s1 + s2], device=device, **self.sim_conf
                )
            )
            sim_comb_list.append(sim1 + sim2)
            sim_comb_list.append(sim1.combine(sim2))

            # test if combined simulations are same
            for _s1 in sim_comb_list:
                for _s2 in sim_comb_list:
                    torch.testing.assert_close(
                        _s1.get_all_positions(), _s2.get_all_positions()
                    )
                    torch.testing.assert_close(
                        _s1.get_source_validity_radius(), _s2.get_source_validity_radius()
                    )
                    torch.testing.assert_close(
                        _s1._get_all_polarizabilitites_6x6(self.wl),
                        _s2._get_all_polarizabilitites_6x6(self.wl),
                    )

    def test_run_seperate_and_combined(self):
        for device in self.devices:

            self.s1.set_center_of_mass([-100, 0, 0])
            self.s2.set_center_of_mass([100, 0, 20])

            sim1 = tg.simulation.Simulation(
                structures=[self.s1, self.s2],
                device=device,
                **self.sim_conf,
            )
            sim1.run(calc_missing=True, verbose=False, progress_bar=False)

            sim2 = tg.simulation.Simulation(
                structures=[self.s1 + self.s2],
                device=device,
                **self.sim_conf,
            )
            sim2.run(calc_missing=True, verbose=False, progress_bar=False)

            torch.testing.assert_close(
                sim1.fields_inside[self.wl].efield,
                sim2.fields_inside[self.wl].efield,
            )

            torch.testing.assert_close(
                sim1.fields_inside[self.wl].hfield,
                sim2.fields_inside[self.wl].hfield,
            )

            if self.verbose:
                print("  - {}: list vs combined struct 2D sim test passed.".format(device))

    def test_calculate_E_H(self):
        for device in self.devices:

            self.s1.set_center_of_mass([-100, 0, 0])
            self.s2.set_center_of_mass([100, 0, 50])

            sim = tg.simulation.Simulation(
                structures=[self.s1, self.s2], device=device, **self.sim_conf
            )

            sim.run(calc_missing=True, verbose=False, progress_bar=False)

            # test split/combine
            s_split0 = sim.split(0)
            s_split1 = sim.split(1)
            s_comb = s_split0.combine(s_split1)

            torch.testing.assert_close(
                sim.fields_inside[self.wl].efield,
                s_comb.fields_inside[self.wl].efield,
            )

            torch.testing.assert_close(
                sim.fields_inside[self.wl].hfield,
                s_comb.fields_inside[self.wl].hfield,
            )

            # test delete
            s0_delete = sim.delete_struct(1)
            s1_delete = sim.delete_struct(0)

            torch.testing.assert_close(
                s_split0.fields_inside[self.wl].efield,
                s0_delete.fields_inside[self.wl].efield,
            )

            torch.testing.assert_close(
                s_split1.fields_inside[self.wl].hfield,
                s1_delete.fields_inside[self.wl].hfield,
            )

            if self.verbose:
                print("  - {}: split combine 2D sim test passed.".format(device))


# %%
if __name__ == "__main__":
    print("testing splitting / combining simulations...")
    torch.set_printoptions(precision=7)
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
