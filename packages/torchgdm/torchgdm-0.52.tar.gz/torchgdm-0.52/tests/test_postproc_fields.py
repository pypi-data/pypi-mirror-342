# encoding=utf-8
# %%
import unittest

import torch

import torchgdm as tg


class TestFieldCalculations2D(unittest.TestCase):

    def setUp(self):
        self.verbose = False
        if self.verbose:
            print("testing fields postprocessing with discretized 2D-simulation...")

        # --- determine if GPU is available
        self.devices = ["cpu"]
        if torch.cuda.is_available():
            self.devices.append("cuda:0")

        # --- setup a test case
        # - environment
        eps_env = 1.0
        mat_env = tg.materials.MatConstant(eps_env)
        env = tg.env.freespace_2d.EnvHomogeneous2D(env_material=mat_env)

        # - illumination field(s)
        self.wavelengths = torch.tensor([500.0])
        e_inc_list = [
            tg.env.freespace_2d.PlaneWave(
                e0p=0.5, e0s=0.7, inc_angle=torch.pi
            ),  # linear-polarization, incidence from top
        ]

        # - structure
        step = 15.0
        mat_struct = tg.materials.MatConstant(eps=7.0)
        struct2d = tg.struct2d.StructDiscretizedSquare2D(
            tg.struct2d.rectangle(l=5, h=3), step, mat_struct
        )

        self.sim = tg.simulation.Simulation(
            structures=[struct2d],
            environment=env,
            illumination_fields=e_inc_list,
            wavelengths=self.wavelengths,
        )

    def test_internal_fields(self):
        for device in self.devices:
            self.sim.set_device(device)
            self.sim.run(verbose=False, progress_bar=False, calc_missing=True)

            # calculate internal fields
            self.r_probe = self.sim.get_all_positions()
            nf_res = tg.postproc.fields.nf(
                self.sim,
                self.wavelengths[0],
                self.r_probe,
                interpolation_step_range=0.1,
                source_distance_steps=0.1,
                progress_bar=False,
            )
            nf_postproc = nf_res["tot"]
            nf_inside = self.sim.fields_inside[float(self.wavelengths[0])]

            torch.testing.assert_close(
                nf_postproc.efield, nf_inside.efield, rtol=1e-3, atol=1e-3
            )
            torch.testing.assert_close(
                nf_postproc.hfield, nf_inside.hfield, rtol=1e-3, atol=1e-3
            )

            if self.verbose:
                print(
                    "  - {}: 2D-sim internal field consistency test passed.".format(
                        device
                    )
                )

    def test_nearfield(self):
        for device in self.devices:
            self.sim.set_device(device)
            self.sim.run(verbose=False, progress_bar=False)

            # calculate nearfield
            self.r_probe = torch.as_tensor(
                [[300.0, 00.0, 105.0], [12.0, 0.0, -50.0]], device=device
            )
            nf_res = tg.postproc.fields._nearfield(
                self.sim,
                self.wavelengths[0],
                self.r_probe,
            )
            nf = torch.stack([nf_res["e_sca"], nf_res["e_tot"], nf_res["h_tot"]])
            # print(nf)

            # compare to pre-calculated reference
            nf_truth = torch.as_tensor(
                [
                    [
                        [
                            [
                                -0.0123919 - 0.0022812j,
                                0.1676146 - 0.1816293j,
                                -0.0049116 + 0.0124582j,
                            ],
                            [
                                -0.1053862 + 0.0654174j,
                                -0.3760716 + 0.3414206j,
                                -0.0329867 + 0.0019590j,
                            ],
                        ]
                    ],
                    [
                        [
                            [
                                0.1119532 - 0.4865728j,
                                0.3416977 - 0.8596374j,
                                -0.0049116 + 0.0124581j,
                            ],
                            [
                                0.2991223 + 0.3593100j,
                                0.1902403 + 0.7528703j,
                                -0.0329866 + 0.0019590j,
                            ],
                        ]
                    ],
                    [
                        [
                            [
                                0.1220035 - 0.6340325j,
                                -0.1247076 + 0.4713390j,
                                0.1848267 - 0.1560034j,
                            ],
                            [
                                0.0178721 + 0.5906836j,
                                -0.3645644 - 0.4154846j,
                                -0.0858047 + 0.0229988j,
                            ],
                        ]
                    ],
                ],
                dtype=tg.constants.DTYPE_COMPLEX,
                device=device,
            )

            torch.testing.assert_close(nf, nf_truth, rtol=1e-3, atol=1e-3)

            if self.verbose:
                print("  - {}: 3D-sim nearfield test passed.".format(device))

    def test_field_gradients(self):
        for device in self.devices:
            self.sim.set_device(device)
            self.sim.run(verbose=False, progress_bar=False)

            # calculate field gradients
            self.r_probe = torch.as_tensor(
                [[0.0, 0.0, 105.0], [12.0, 0.0, 200.0]],
                dtype=tg.constants.DTYPE_FLOAT,
                device=device,
            )
            delta = 0.1
            field = "e_tot"
            fgrads = tg.postproc.fields.field_gradient(
                self.sim,
                self.wavelengths[0],
                self.r_probe,
                delta=delta,
                whichfield=field,
            )
            grad = torch.stack([fgrads["dfdx"], fgrads["dfdy"], fgrads["dfdz"]])
            # print(grad)

            # compare to pre-calculated reference
            grad_truth = torch.as_tensor(
                [
                    [
                        [
                            [
                                -3.7252903e-08 + 0.0000000e00j,
                                1.4901161e-07 - 1.4901161e-07j,
                                2.1063897e-03 - 1.5938655e-04j,
                            ],
                            [
                                7.2568655e-05 - 1.2069941e-05j,
                                2.1457672e-04 - 1.8179417e-04j,
                                3.8543949e-04 + 2.3508561e-04j,
                            ],
                        ]
                    ],
                    [
                        [
                            [
                                0.0000000e00 + 0.0000000e00j,
                                0.0000000e00 + 0.0000000e00j,
                                0.0000000e00 + 0.0000000e00j,
                            ],
                            [
                                0.0000000e00 + 0.0000000e00j,
                                0.0000000e00 + 0.0000000e00j,
                                0.0000000e00 + 0.0000000e00j,
                            ],
                        ]
                    ],
                    [
                        [
                            [
                                -5.2526221e-03 - 2.2722781e-03j,
                                -9.8736584e-03 - 8.6054206e-03j,
                                2.9604230e-09 - 1.3007728e-09j,
                            ],
                            [
                                -3.3956766e-03 + 4.4409931e-03j,
                                -1.9621849e-03 + 4.3258071e-03j,
                                -7.2531402e-05 + 1.2074597e-05j,
                            ],
                        ]
                    ],
                ],
                dtype=tg.constants.DTYPE_COMPLEX,
                device=device,
            )

            torch.testing.assert_close(grad, grad_truth, rtol=1e-3, atol=1e-3)

            if self.verbose:
                print("  - {}: 3D-sim field gradients test passed.".format(device))


class TestFieldCalculations3D(unittest.TestCase):

    def setUp(self):
        self.verbose = False
        if self.verbose:
            print("testing fields postprocessing with discretized 3D-simulation...")

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
        self.wavelengths = torch.tensor([500.0])
        e_inc_list = [
            tg.env.freespace_3d.PlaneWave(
                e0p=1.0, e0s=0.0, inc_angle=torch.pi
            ),  # X-polarization, incidence from top
        ]

        # - structure
        step = 15.0
        mat_struct = tg.materials.MatConstant(eps=9.0)
        struct1 = tg.struct3d.StructDiscretizedCubic3D(
            tg.struct3d.geometries.cuboid(l=3, w=4, h=2),
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

    def test_internal_fields(self):
        for device in self.devices:
            self.sim.set_device(device)
            self.sim.run(verbose=False, progress_bar=False, calc_missing=True)

            # calculate internal fields
            self.r_probe = self.sim.get_all_positions()
            nf_res = tg.postproc.fields.nf(
                self.sim,
                self.wavelengths[0],
                self.r_probe,
                interpolation_step_range=0.1,
                source_distance_steps=0.1,
                progress_bar=False,
            )
            nf_postproc = nf_res["tot"]
            nf_inside = self.sim.fields_inside[float(self.wavelengths[0])]

            torch.testing.assert_close(
                nf_postproc.efield, nf_inside.efield, rtol=1e-3, atol=1e-3
            )
            torch.testing.assert_close(
                nf_postproc.hfield, nf_inside.hfield, rtol=1e-3, atol=1e-3
            )

            if self.verbose:
                print(
                    "  - {}: 3D-sim internal field consistency test passed.".format(
                        device
                    )
                )

    def test_nearfield(self):
        for device in self.devices:
            self.sim.set_device(device)
            self.sim.run(verbose=False, progress_bar=False)

            # calculate nearfield
            self.r_probe = torch.as_tensor(
                [[300.0, 40.0, 105.0], [12.0, 50.0, -50.0]], device=device
            )
            nf_res = tg.postproc.fields._nearfield(
                self.sim,
                self.wavelengths[0],
                self.r_probe,
            )
            nf = torch.stack([nf_res["e_sca"], nf_res["e_tot"], nf_res["h_tot"]])
            # print(nf)

            # compare to pre-calculated reference
            nf_truth = torch.as_tensor(
                [
                    [
                        [
                            [
                                -3.4736176e-03 + 1.8434002e-03j,
                                1.4439697e-04 + 8.7944919e-04j,
                                3.6897586e-04 + 2.4145723e-03j,
                            ],
                            [
                                -2.1888228e-02 + 2.1395750e-02j,
                                8.2111722e-03 - 9.2640589e-04j,
                                -1.5400744e-02 + 1.9592703e-03j,
                            ],
                        ]
                    ],
                    [
                        [
                            [
                                2.4521643e-01 - 9.6673971e-01j,
                                1.4439697e-04 + 8.7944919e-04j,
                                3.6899760e-04 + 2.4144875e-03j,
                            ],
                            [
                                7.8712869e-01 + 6.0918105e-01j,
                                8.2111722e-03 - 9.2640589e-04j,
                                -1.5400673e-02 + 1.9593218e-03j,
                            ],
                        ]
                    ],
                    [
                        [
                            [
                                -5.3811527e-07 - 5.9395365e-06j,
                                -2.5016230e-01 + 9.6671307e-01j,
                                5.3901912e-04 + 6.8496628e-04j,
                            ],
                            [
                                -4.0306677e-05 + 1.0966815e-04j,
                                -8.0708373e-01 - 6.2726992e-01j,
                                2.1683499e-03 - 2.3433529e-02j,
                            ],
                        ]
                    ],
                ],
                dtype=tg.constants.DTYPE_COMPLEX,
                device=device,
            )

            torch.testing.assert_close(nf, nf_truth, rtol=1e-3, atol=1e-3)

            if self.verbose:
                print("  - {}: 3D-sim nearfield test passed.".format(device))

    def test_field_gradients(self):
        for device in self.devices:
            self.sim.set_device(device)
            self.sim.run(verbose=False, progress_bar=False)

            # calculate field gradients
            self.r_probe = torch.as_tensor(
                [[0.0, 0.0, 105.0], [12.0, 50.0, 200.0]],
                dtype=tg.constants.DTYPE_FLOAT,
                device=device,
            )
            delta = 0.1
            field = "e_tot"
            fgrads = tg.postproc.fields.field_gradient(
                self.sim,
                self.wavelengths[0],
                self.r_probe,
                delta=delta,
                whichfield=field,
            )
            grad = torch.stack([fgrads["dfdx"], fgrads["dfdy"], fgrads["dfdz"]])
            # print(grad)

            # compare to pre-calculated reference
            grad_truth = torch.as_tensor(
                [
                    [
                        [
                            [
                                0.0000000e00 + 0.0000000e00j,
                                -5.7825473e-05 + 9.4272946e-06j,
                                8.1359642e-04 - 1.3028191e-04j,
                            ],
                            [
                                1.1026859e-05 - 4.7683716e-06j,
                                1.9397121e-05 + 5.9410741e-06j,
                                8.6341170e-05 + 2.6219059e-05j,
                            ],
                        ]
                    ],
                    [
                        [
                            [
                                -2.2500753e-05 + 1.3709068e-05j,
                                2.9103830e-10 + 2.0918378e-10j,
                                2.9103830e-10 - 2.9103830e-10j,
                            ],
                            [
                                -5.9604645e-07 - 2.9206276e-05j,
                                4.5253546e-06 + 1.7492493e-06j,
                                -4.7066715e-06 + 3.4109689e-07j,
                            ],
                        ]
                    ],
                    [
                        [
                            [
                                -1.1811852e-02 - 3.3086538e-03j,
                                4.3655746e-10 - 5.4569682e-11j,
                                -1.3551205e-09 - 1.0508572e-09j,
                            ],
                            [
                                -7.3888898e-03 + 1.0038614e-02j,
                                -4.7260255e-06 + 3.6117854e-07j,
                                -1.5694532e-05 + 3.2107346e-06j,
                            ],
                        ]
                    ],
                ],
                dtype=tg.constants.DTYPE_COMPLEX,
                device=device,
            )

            torch.testing.assert_close(grad, grad_truth, rtol=1e-3, atol=1e-3)

            if self.verbose:
                print("  - {}: 3D-sim field gradients test passed.".format(device))


# %%

# %%

# %%
if __name__ == "__main__":
    print("testing fields postprocessing...")
    torch.set_printoptions(precision=7)
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
