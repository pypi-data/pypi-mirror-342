# encoding=utf-8
# %%
import unittest

import torch

import torchgdm as tg


class TestFreeSpacePlanWave(unittest.TestCase):

    def setUp(self):
        self.verbose = False
        if self.verbose:
            print("testing plane wave illumination.")

        # --- determine if GPU is available
        self.devices = ["cpu"]
        if torch.cuda.is_available():
            self.devices.append("cuda:0")

        # --- setup a test case
        eps_env = 1.3
        inangledeg = 180.0
        e_p = 1
        e_s = 1
        self.r_probe = torch.as_tensor(
            [[100, 0, 20], [0, 0, 100], [-100, 0, 200], [-500, 40, -200]],
            dtype=tg.constants.DTYPE_FLOAT,
        )

        # --- setup a reference simulation
        self.env = tg.env.freespace_3d.EnvHomogeneous3D(env_material=eps_env)

        self.efield = tg.env.freespace_3d.PlaneWave(
            e0p=e_p, e0s=e_s, inc_angle=inangledeg * torch.pi / 180
        )

    def test_E_H_factor(self):
        """test if in homogeneous medium |H|=n_env*|E|"""
        for device in self.devices:
            r_probe = (torch.rand((10, 3), device=device) - 0.5) * 1000
            wavelength = torch.tensor(500.0, device=device)
            for eps_env in [1.0, 2.25, 9.0]:
                efield = tg.env.freespace_3d.PlaneWave(device=device)
                env = tg.env.freespace_3d.EnvHomogeneous3D(
                    env_material=eps_env, device=device
                )
                E0tg = efield.get_efield(
                    r_probe, wavelength=wavelength, environment=env
                )
                H0tg = efield.get_hfield(
                    r_probe, wavelength=wavelength, environment=env
                )

                torch.testing.assert_close(
                    torch.sum((H0tg.abs()[:, 1]) / (E0tg.abs()[:, 0]) - eps_env**0.5),
                    torch.as_tensor(0.0, device=device),
                )

    def test_phase(self):
        config_pairs = [
            # test-case 1
            [
                dict(
                    e0s=1.0,
                    e0p=0.0,
                    inc_angle=0.0,
                    phase_e0s=torch.pi / 2,
                    inc_plane="xz",
                ),
                dict(
                    e0s=1.0,
                    e0p=0.0,
                    inc_angle=0.0,
                    phase_global=torch.pi / 2,
                    inc_plane="xz",
                ),
            ],
            # test-case 2
            [
                dict(e0s=1.0, e0p=1.0, inc_angle=torch.pi / 2, inc_plane="xz"),
                dict(
                    e0s=1.0,
                    e0p=1.0,
                    inc_angle=torch.pi / 2,
                    phase_global=torch.pi * 2,
                    inc_plane="xz",
                ),
            ],
            # test-case 3
            [
                dict(inc_plane="yz"),
                dict(phase_global=torch.pi * 2, inc_plane="yz"),
            ],
        ]
        for device in self.devices:
            wavelength = torch.as_tensor(500.0, device=device)
            for conf1, conf2 in config_pairs:
                env = tg.env.freespace_3d.EnvHomogeneous3D(device=device)
                ef1 = tg.env.freespace_3d.PlaneWave(**conf1, device=device)
                ef2 = tg.env.freespace_3d.PlaneWave(**conf2, device=device)

                r_probe = torch.as_tensor(
                    [[120, -50, -100]], dtype=tg.constants.DTYPE_FLOAT, device=device
                )

                e01 = ef1.get_efield(r_probe, wavelength=wavelength, environment=env)
                h01 = ef1.get_hfield(r_probe, wavelength=wavelength, environment=env)
                e02 = ef1.get_efield(r_probe, wavelength=wavelength, environment=env)
                h02 = ef1.get_hfield(r_probe, wavelength=wavelength, environment=env)

                torch.testing.assert_close(e01, e02)
                torch.testing.assert_close(h01, h02)

    def test_vector_directions(self):
        for device in self.devices:
            configs = [
                dict(e0s=0.0, e0p=1.0, inc_angle=0.0, inc_plane="xz"),
                dict(e0s=0.0, e0p=1.0, inc_angle=torch.pi / 2, inc_plane="xz"),
                dict(e0s=0.0, e0p=1.0, inc_angle=torch.pi / 2, inc_plane="yz"),
                dict(e0s=1.0, e0p=0.0, inc_angle=0.0, inc_plane="xz"),
                dict(e0s=1.0, e0p=0.0, inc_angle=torch.pi / 2, inc_plane="xz"),
                dict(e0s=1.0, e0p=0.0, inc_angle=torch.pi / 2, inc_plane="yz"),
                dict(
                    e0s=1.0,
                    e0p=0.0,
                    inc_angle=0.0,
                    phase_e0s=torch.pi / 4,
                    inc_plane="xz",
                ),
                dict(
                    e0s=1.0,
                    e0p=0.0,
                    inc_angle=torch.pi / 2,
                    phase_e0s=torch.pi / 4,
                    inc_plane="xz",
                ),
                dict(
                    e0s=1.0,
                    e0p=0.0,
                    inc_angle=torch.pi / 2,
                    phase_e0s=torch.pi / 4,
                    inc_plane="yz",
                ),
            ]
            wavelength = torch.as_tensor(500.0, device=device)
            for conf in configs:
                env = tg.env.freespace_3d.EnvHomogeneous3D(device=device)
                ef = tg.env.freespace_3d.PlaneWave(**conf, device=device)

                r_probe = torch.as_tensor(
                    [[0, 0, 0]], dtype=tg.constants.DTYPE_FLOAT, device=device
                )

                e0 = ef.get_efield(r_probe, wavelength=wavelength, environment=env)
                h0 = ef.get_hfield(r_probe, wavelength=wavelength, environment=env)
                k_unit = ef.k_vec_unit

                # check orthogonality
                torch.testing.assert_close(
                    torch.einsum("in,in->i", e0, h0).sum(),
                    torch.as_tensor(0 + 0j, device=device),
                )
                torch.testing.assert_close(
                    torch.einsum("in,in->i", e0, k_unit.unsqueeze(0)).sum(),
                    torch.as_tensor(0 + 0j, device=device),
                )

                # check handedness of vectors
                e_cross_h_dot_k = torch.einsum(
                    "in,in->i", torch.cross(e0, h0, dim=1), k_unit.unsqueeze(0)
                )
                if e_cross_h_dot_k[0].real != 0:
                    torch.testing.assert_close(
                        torch.sign(e_cross_h_dot_k[0].real),
                        torch.as_tensor(1.0, device=device),
                    )
                if e_cross_h_dot_k[0].imag != 0:
                    torch.testing.assert_close(
                        torch.sign(e_cross_h_dot_k[0].imag),
                        torch.as_tensor(1.0, device=device),
                    )

    def test_calculate_E_H(self):
        wavelength = 500.0
        for device in self.devices:
            self.r_probe = self.r_probe.to(device=device)
            self.efield.set_device(device)
            self.env.set_device(device)

            e0 = self.efield.get_efield(
                self.r_probe, wavelength=wavelength, environment=self.env
            )
            h0 = self.efield.get_hfield(
                self.r_probe, wavelength=wavelength, environment=self.env
            )
            # print(e0)
            # print(h0)

            e0_truth = torch.as_tensor(
                [
                    [
                        9.5922262e-01 - 2.8265165e-01j,
                        9.5922262e-01 - 2.8265165e-01j,
                        -1.1747089e-16 + 3.4614844e-17j,
                    ],
                    [
                        1.3757181e-01 - 9.9049180e-01j,
                        1.3757181e-01 - 9.9049180e-01j,
                        -1.6847687e-17 + 1.2130026e-16j,
                    ],
                    [
                        -9.6214800e-01 - 2.7252749e-01j,
                        -9.6214800e-01 - 2.7252749e-01j,
                        1.1782915e-16 + 3.3374992e-17j,
                    ],
                    [
                        -9.6214800e-01 + 2.7252749e-01j,
                        -9.6214800e-01 + 2.7252749e-01j,
                        1.1782915e-16 - 3.3374992e-17j,
                    ],
                ],
                dtype=tg.constants.DTYPE_COMPLEX,
                device=device,
            )

            h0_truth = torch.as_tensor(
                [
                    [
                        1.0936821e00 - 3.2227247e-01j,
                        -1.0936821e00 + 3.2227247e-01j,
                        -1.3393742e-16 + 3.9466995e-17j,
                    ],
                    [
                        1.5685599e-01 - 1.1293344e00j,
                        -1.5685599e-01 + 1.1293344e00j,
                        -1.9209319e-17 + 1.3830358e-16j,
                    ],
                    [
                        -1.0970175e00 - 3.1072915e-01j,
                        1.0970175e00 + 3.1072915e-01j,
                        1.3434590e-16 + 3.8053346e-17j,
                    ],
                    [
                        -1.0970175e00 + 3.1072915e-01j,
                        1.0970175e00 - 3.1072915e-01j,
                        1.3434590e-16 - 3.8053346e-17j,
                    ],
                ],
                dtype=tg.constants.DTYPE_COMPLEX,
                device=device,
            )

            # compare random e-field
            torch.testing.assert_close(e0, e0_truth)
            torch.testing.assert_close(h0, h0_truth)
            if self.verbose:
                print("  - {}: field evaluation test passed.".format(device))

    def test_integration_crosssections(self):

        for device in self.devices:
            torch.set_printoptions(precision=3, linewidth=200)

            # - anisotropic structure
            step = 40.0
            mat_struct = tg.materials.MatConstant(eps=20 + 0.5j)
            mat_struct = tg.materials.MatDatabase("Ge")
            struct = tg.struct3d.StructDiscretizedCubic3D(
                tg.struct3d.cuboid(l=4, w=4, h=4), step, mat_struct
            )

            # - environment / illuminations setup
            env = tg.env.freespace_3d.EnvHomogeneous3D(env_material=1)
            wavelengths = torch.as_tensor([550])

            # illumination configs for same electric response
            e_inc_same_e_1 = [  # Ex, Hy, kz   -   Ex, Hz, ky
                tg.env.freespace_3d.PlaneWave(
                    e0p=0, e0s=1, inc_angle=0, inc_plane="yz"
                ),
                tg.env.freespace_3d.PlaneWave(
                    e0p=0, e0s=1, inc_angle=torch.pi / 2, inc_plane="yz"
                ),
            ]
            e_inc_same_e_2 = [
                tg.env.freespace_3d.PlaneWave(
                    e0p=0, e0s=1, inc_angle=0, inc_plane="xz"
                ),
                tg.env.freespace_3d.PlaneWave(
                    e0p=0, e0s=1, inc_angle=torch.pi / 2, inc_plane="xz"
                ),
            ]
            e_inc_same_e_3 = [
                tg.env.freespace_3d.PlaneWave(
                    e0p=1, e0s=0, inc_angle=torch.pi / 2, inc_plane="xz"
                ),
                tg.env.freespace_3d.PlaneWave(
                    e0p=1, e0s=0, inc_angle=torch.pi / 2, inc_plane="yz"
                ),
            ]

            # illumination configs for same magnetic response
            e_inc_same_h_1 = [  # Ey, Hx, kz   -   Ez, Hx, ky
                tg.env.freespace_3d.PlaneWave(
                    e0p=1, e0s=0, inc_angle=0, inc_plane="yz"
                ),
                tg.env.freespace_3d.PlaneWave(
                    e0p=1, e0s=0, inc_angle=torch.pi / 2, inc_plane="yz"
                ),
            ]
            e_inc_same_h_2 = [
                tg.env.freespace_3d.PlaneWave(
                    e0p=1, e0s=0, inc_angle=0, inc_plane="xz"
                ),
                tg.env.freespace_3d.PlaneWave(
                    e0p=1, e0s=0, inc_angle=torch.pi / 2, inc_plane="xz"
                ),
            ]
            e_inc_same_h_3 = [
                tg.env.freespace_3d.PlaneWave(
                    e0p=0, e0s=1, inc_angle=torch.pi / 2, inc_plane="xz"
                ),
                tg.env.freespace_3d.PlaneWave(
                    e0p=0, e0s=1, inc_angle=torch.pi / 2, inc_plane="yz"
                ),
            ]

            # symmetric structure: test all illumination pairs
            e_inc_list = [
                e_inc_same_e_1,
                e_inc_same_e_2,
                e_inc_same_e_3,
                e_inc_same_h_1,
                e_inc_same_h_2,
                e_inc_same_h_3,
            ]

            # test all pairs
            for i, e_inc in enumerate(e_inc_list):
                sim = tg.simulation.Simulation(
                    structures=[struct],
                    environment=env,
                    illumination_fields=e_inc,
                    wavelengths=wavelengths,
                    device=device,
                )
                sim.run(verbose=False, progress_bar=False)

                # - scs
                scs_mp = sim.get_spectra_multipole_scs(progress_bar=False)
                torch.testing.assert_close(
                    scs_mp["scs_ed"][:, 0], scs_mp["scs_ed"][:, 1], atol=0.5, rtol=1e-3
                )
                torch.testing.assert_close(
                    scs_mp["scs_eq"][:, 0], scs_mp["scs_eq"][:, 1], atol=0.5, rtol=1e-3
                )
                torch.testing.assert_close(
                    scs_mp["scs_md"][:, 0], scs_mp["scs_md"][:, 1], atol=0.5, rtol=1e-3
                )
                torch.testing.assert_close(
                    scs_mp["scs_mq"][:, 0], scs_mp["scs_mq"][:, 1], atol=0.5, rtol=1e-3
                )

                # - ecs
                ecs_mp = sim.get_spectra_multipole_ecs(progress_bar=False)
                torch.testing.assert_close(
                    ecs_mp["ecs_ed"][:, 0], ecs_mp["ecs_ed"][:, 1], atol=0.5, rtol=1e-3
                )
                torch.testing.assert_close(
                    ecs_mp["ecs_eq"][:, 0], ecs_mp["ecs_eq"][:, 1], atol=0.5, rtol=1e-3
                )
                torch.testing.assert_close(
                    ecs_mp["ecs_md"][:, 0], ecs_mp["ecs_md"][:, 1], atol=0.5, rtol=1e-3
                )
                torch.testing.assert_close(
                    ecs_mp["ecs_mq"][:, 0], ecs_mp["ecs_mq"][:, 1], atol=0.5, rtol=1e-3
                )

                # print("------")
                # print(i, "scs:")
                # print("ED - ", scs_mp["scs_ed"][:, 0], scs_mp["scs_ed"][:, 1])
                # print("EQ - ", scs_mp["scs_eq"][:, 0], scs_mp["scs_eq"][:, 1])
                # print("MD - ", scs_mp["scs_md"][:, 0], scs_mp["scs_md"][:, 1])
                # print("MQ - ", scs_mp["scs_mq"][:, 0], scs_mp["scs_mq"][:, 1])
                # print(i, "ecs:")
                # print("ED - ", ecs_mp["ecs_ed"][:, 0], ecs_mp["ecs_ed"][:, 1])
                # print("EQ - ", ecs_mp["ecs_eq"][:, 0], ecs_mp["ecs_eq"][:, 1])
                # print("MD - ", ecs_mp["ecs_md"][:, 0], ecs_mp["ecs_md"][:, 1])
                # print("MQ - ", ecs_mp["ecs_mq"][:, 0], ecs_mp["ecs_mq"][:, 1])


class TestFreeSpaceGaussian(unittest.TestCase):

    def setUp(self):
        self.verbose = False
        if self.verbose:
            print("testing gaussian beam illumination.")

        # --- determine if GPU is available
        self.devices = ["cpu"]
        if torch.cuda.is_available():
            self.devices.append("cuda:0")

        # --- setup a test case
        eps_env = 1.45**2
        inangledeg = 40.0 * torch.pi / 180.0
        e_p = 1
        e_s = 0.5
        waist = 250.0
        self.r_focus = torch.as_tensor([0, 0, 10])
        self.r_probe = torch.as_tensor(
            [[100, 0, 20], [0, 0, 100], [-100, 0, 200], [-500, 40, -200]],
            dtype=tg.constants.DTYPE_FLOAT,
        )

        # --- setup a reference simulation
        self.env = tg.env.freespace_3d.EnvHomogeneous3D(env_material=eps_env)

        self.efield = tg.env.freespace_3d.GaussianParaxial(
            e0p=e_p,
            e0s=e_s,
            r_focus=self.r_focus,
            waist=waist,
            inc_angle=inangledeg,
            correction_div_e=True,
        )

    def test_compare_with_planewave(self):
        wavelength = 650.0
        for device in self.devices:
            self.r_probe = self.r_probe.to(device=device)
            self.env.set_device(device)
            polas = [[1, 0], [0, 1], [1, 1]]
            inc_angles_deg = [0, 30, 90, 150, 180]
            for e_p_s in polas:
                for inc_angle_deg in inc_angles_deg:

                    planewave = tg.env.freespace_3d.PlaneWave(
                        e0p=e_p_s[0],
                        e0s=e_p_s[1],
                        inc_angle=inc_angle_deg * torch.pi / 180,
                        device=device,
                    )

                    gaussian = tg.env.freespace_3d.GaussianParaxial(
                        e0p=e_p_s[0],
                        e0s=e_p_s[1],
                        r_focus=[0, 0, 0],
                        waist=10000000,
                        inc_angle=inc_angle_deg * torch.pi / 180,
                        correction_div_e=True,
                        device=device,
                    )

                    # eval electric fields
                    e0_p = planewave.get_efield(
                        [0, 0, 0], wavelength=wavelength, environment=self.env
                    )
                    e0_g = gaussian.get_efield(
                        [0, 0, 0], wavelength=wavelength, environment=self.env
                    )
                    torch.testing.assert_close(e0_p, e0_g, rtol=1e-2, atol=0.01)

                    # eval magnetic fields
                    h0_p = planewave.get_hfield(
                        [0, 0, 0], wavelength=wavelength, environment=self.env
                    )
                    h0_g = gaussian.get_hfield(
                        [0, 0, 0], wavelength=wavelength, environment=self.env
                    )
                    torch.testing.assert_close(h0_p, h0_g, rtol=1e-2, atol=0.01)

    def test_calculate_E_H(self):
        wavelength = 650.0
        for device in self.devices:
            self.r_probe = self.r_probe.to(device=device)
            self.efield.set_device(device)
            self.env.set_device(device)

            e0 = self.efield.get_efield(
                self.r_probe, wavelength=wavelength, environment=self.env
            )
            h0 = self.efield.get_hfield(
                self.r_probe, wavelength=wavelength, environment=self.env
            )
            # print(e0)
            # print(h0)

            e0_truth = torch.as_tensor(
                [
                    [
                        -0.5448776 - 4.3501070e-01j,
                        0.3144340 + 3.2393885e-01j,
                        -0.3289866 - 4.8949170e-01j,
                    ],
                    [
                        -0.4636163 - 5.4261190e-01j,
                        0.3361847 + 3.1875351e-01j,
                        -0.4935032 - 3.4512645e-01j,
                    ],
                    [
                        -0.0536437 - 4.3212891e-01j,
                        0.1200230 + 2.3944278e-01j,
                        -0.3095120 - 2.3002407e-01j,
                    ],
                    [
                        -0.3082355 + 4.6097115e-04j,
                        0.1981485 - 2.4692476e-02j,
                        -0.2491881 + 7.6279074e-02j,
                    ],
                ],
                dtype=tg.constants.DTYPE_COMPLEX,
                device=device,
            )

            h0_truth = torch.as_tensor(
                [
                    [
                        -0.3950363 - 3.1538275e-01j,
                        -0.9118586 - 9.3942261e-01j,
                        -0.2385153 - 3.5488147e-01j,
                    ],
                    [
                        -0.3361218 - 3.9339361e-01j,
                        -0.9749354 - 9.2438513e-01j,
                        -0.3577898 - 2.5021666e-01j,
                    ],
                    [
                        -0.0388917 - 3.1329343e-01j,
                        -0.3480666 - 6.9438404e-01j,
                        -0.2243962 - 1.6676745e-01j,
                    ],
                    [
                        -0.2234707 + 3.3420406e-04j,
                        -0.5746307 + 7.1608178e-02j,
                        -0.1806614 + 5.5302326e-02j,
                    ],
                ],
                dtype=tg.constants.DTYPE_COMPLEX,
                device=device,
            )

            # compare random e-field
            torch.testing.assert_close(e0, e0_truth)
            torch.testing.assert_close(h0, h0_truth)
            if self.verbose:
                print("  - {}: field evaluation test passed.".format(device))


class TestFreeSpaceElectricDipole(unittest.TestCase):

    def setUp(self):
        self.verbose = False
        if self.verbose:
            print("testing electric dipole illumination.")

        # --- determine if GPU is available
        self.devices = ["cpu"]
        if torch.cuda.is_available():
            self.devices.append("cuda:0")

        # --- setup a test case
        eps_env = 1.3
        p_source = torch.as_tensor([1.0, -1.0, 0.5], dtype=tg.constants.DTYPE_FLOAT)
        r_source = torch.as_tensor([10.0, 5.0, 15.0], dtype=tg.constants.DTYPE_FLOAT)
        self.r_probe = torch.as_tensor(
            [[10, 0, 20], [0, 0, -10], [-10, 10, 5], [-500, 40, -200]],
            dtype=tg.constants.DTYPE_FLOAT,
        )

        # --- setup a reference simulation
        self.env = tg.env.freespace_3d.EnvHomogeneous3D(env_material=eps_env)

        self.efield = tg.env.freespace_3d.ElectricDipole(
            r_source=r_source, p_source=p_source
        )

    def test_calculate_E_H(self):
        wavelength = 500.0
        for device in self.devices:
            self.r_probe = self.r_probe.to(device=device)
            self.efield.set_device(device)
            self.env.set_device(device)

            e0 = self.efield.get_efield(
                self.r_probe, wavelength=wavelength, environment=self.env
            )
            h0 = self.efield.get_hfield(
                self.r_probe, wavelength=wavelength, environment=self.env
            )
            # print(e0)
            # print(h0)

            e0_truth = torch.as_tensor(
                [
                    [
                        -2.1646330e-03 + 1.5052938e-06j,
                        -2.7391179e-03 - 1.5064361e-06j,
                        3.8214340e-03 + 7.5378472e-07j,
                    ],
                    [
                        -7.9824858e-06 + 1.4676721e-06j,
                        4.8353097e-05 - 1.4596324e-06j,
                        4.9836235e-05 + 7.4455437e-07j,
                    ],
                    [
                        1.6251166e-04 + 1.4944962e-06j,
                        4.9544378e-06 - 1.4806619e-06j,
                        8.1255821e-05 + 7.4724721e-07j,
                    ],
                    [
                        8.1364007e-08 - 5.7865215e-09j,
                        5.1592448e-08 - 2.5644798e-07j,
                        2.9485673e-08 + 1.9189642e-08j,
                    ],
                ],
                dtype=tg.constants.DTYPE_COMPLEX,
                device=device,
            )

            h0_truth = torch.as_tensor(
                [
                    [
                        -3.0768206e-08 + 8.9312525e-05j,
                        -6.1536412e-08 + 1.7862505e-04j,
                        -6.1536412e-08 + 1.7862505e-04j,
                    ],
                    [
                        3.3363011e-07 - 1.8070623e-05j,
                        2.4264011e-07 - 1.3142271e-05j,
                        -1.8198000e-07 + 9.8567043e-06j,
                    ],
                    [
                        9.1412744e-08 - 8.2457755e-06j,
                        0.0000000e00 + 0.0000000e00j,
                        -1.8282549e-07 + 1.6491551e-05j,
                    ],
                    [
                        2.5095151e-08 - 1.1380054e-07j,
                        -5.0825637e-09 + 2.3048244e-08j,
                        -6.0355426e-08 + 2.7369757e-07j,
                    ],
                ],
                dtype=tg.constants.DTYPE_COMPLEX,
                device=device,
            )

            # compare random e-field
            torch.testing.assert_close(e0, e0_truth)
            torch.testing.assert_close(h0, h0_truth)
            if self.verbose:
                print("  - {}: field evaluation test passed.".format(device))


class TestFreeSpaceMagneticDipole(unittest.TestCase):

    def setUp(self):
        self.verbose = False
        if self.verbose:
            print("testing magnetic dipole illumination.")

        # --- determine if GPU is available
        self.devices = ["cpu"]
        if torch.cuda.is_available():
            self.devices.append("cuda:0")

        # --- setup a test case
        eps_env = 1.3
        m_source = torch.as_tensor([1.0, -1.0, 0.5], dtype=tg.constants.DTYPE_FLOAT)
        r_source = torch.as_tensor([10.0, 5.0, 15.0], dtype=tg.constants.DTYPE_FLOAT)
        self.r_probe = torch.as_tensor(
            [[10, 0, 20], [0, 0, -10], [-10, 10, 5], [-500, 40, -200]],
            dtype=tg.constants.DTYPE_FLOAT,
        )

        # --- setup a reference simulation
        self.env = tg.env.freespace_3d.EnvHomogeneous3D(env_material=eps_env)

        self.efield = tg.env.freespace_3d.MagneticDipole(
            r_source=r_source, m_source=m_source
        )

    def test_calculate_E_H(self):
        wavelength = 500.0
        for device in self.devices:
            self.r_probe = self.r_probe.to(device=device)
            self.efield.set_device(device)
            self.env.set_device(device)

            e0 = self.efield.get_efield(
                self.r_probe, wavelength=wavelength, environment=self.env
            )
            h0 = self.efield.get_hfield(
                self.r_probe, wavelength=wavelength, environment=self.env
            )
            # print(e0)
            # print(h0)

            e0_truth = torch.as_tensor(
                [
                    [
                        3.0768206e-08 - 8.9312525e-05j,
                        6.1536412e-08 - 1.7862505e-04j,
                        6.1536412e-08 - 1.7862505e-04j,
                    ],
                    [
                        -3.3363062e-07 + 1.8070623e-05j,
                        -2.4264045e-07 + 1.3142271e-05j,
                        1.8198034e-07 - 9.8567043e-06j,
                    ],
                    [
                        -9.1413085e-08 + 8.2457755e-06j,
                        0.0000000e00 + 0.0000000e00j,
                        1.8282617e-07 - 1.6491551e-05j,
                    ],
                    [
                        -2.5095151e-08 + 1.1380054e-07j,
                        5.0825637e-09 - 2.3048230e-08j,
                        6.0355426e-08 - 2.7369754e-07j,
                    ],
                ],
                dtype=tg.constants.DTYPE_COMPLEX,
                device=device,
            )

            h0_truth = torch.as_tensor(
                [
                    [
                        -2.8140228e-03 + 1.9568818e-06j,
                        -3.5608532e-03 - 1.9583667e-06j,
                        4.9678641e-03 + 9.7992017e-07j,
                    ],
                    [
                        -1.0377235e-05 + 1.9079737e-06j,
                        6.2859021e-05 - 1.8975221e-06j,
                        6.4787106e-05 + 9.6792064e-07j,
                    ],
                    [
                        2.1126511e-04 + 1.9428496e-06j,
                        6.4407595e-06 - 1.9248594e-06j,
                        1.0563256e-04 + 9.7142367e-07j,
                    ],
                    [
                        1.0577320e-07 - 7.5224733e-09j,
                        6.7070182e-08 - 3.3338233e-07j,
                        3.8331365e-08 + 2.4946530e-08j,
                    ],
                ],
                dtype=tg.constants.DTYPE_COMPLEX,
                device=device,
            )

            # compare random e-field
            torch.testing.assert_close(e0, e0_truth)
            torch.testing.assert_close(h0, h0_truth)
            if self.verbose:
                print("  - {}: field evaluation test passed.".format(device))


class TestGenericDipoleSource(unittest.TestCase):

    def setUp(self):
        self.verbose = False
        if self.verbose:
            print("testing generic dipole illumination source.")

        # --- determine if GPU is available
        self.devices = ["cpu"]
        if torch.cuda.is_available():
            self.devices.append("cuda:0")

        # --- setup test cases
        self.r_probe = torch.as_tensor([[500, 0, 200]])
        r_source = torch.as_tensor([10.0, 0.0, 15.0])
        p = 1e6
        self.conf_dicts = [
            dict(eps_env=1.0, p=[p, 0, 0, 0, 0, 0]),
            dict(eps_env=1.0, p=[0, p, 0, 0, 0, 0]),
            dict(eps_env=1.0, p=[0, 0, p, 0, 0, 0]),
            dict(eps_env=1.0, p=[0, 0, 0, p, 0, 0]),
            dict(eps_env=1.0, p=[0, 0, 0, 0, p, 0]),
            dict(eps_env=1.0, p=[0, 0, 0, 0, 0, p]),
            dict(eps_env=1.0, p=[p, p, p, 0, 0, 0]),
            dict(eps_env=1.0, p=[0, 0, 0, p, p, p]),
            # with non-vacuum medium
            dict(eps_env=1.5, p=[p, 0, 0, 0, 0, 0]),
            dict(eps_env=1.5, p=[0, p, 0, 0, 0, 0]),
            dict(eps_env=1.5, p=[0, 0, p, 0, 0, 0]),
            dict(eps_env=1.5, p=[0, 0, 0, p, 0, 0]),
            dict(eps_env=1.5, p=[0, 0, 0, 0, p, 0]),
            dict(eps_env=1.5, p=[0, 0, 0, 0, 0, p]),
            dict(eps_env=1.5, p=[p, p, p, 0, 0, 0]),
            dict(eps_env=1.5, p=[0, 0, 0, p, p, p]),
        ]
        self.env_list = []
        self.illum1_list = []
        self.illum2_list = []
        for conf in self.conf_dicts:
            # 3D environment test-case
            self.env_list.append(tg.env.EnvHomogeneous3D(env_material=conf["eps_env"]))
            if sum(conf["p"][:3]) == 0:
                efield_1 = tg.env.freespace_3d.MagneticDipole(
                    r_source=r_source, m_source=conf["p"][3:]
                )
            else:
                efield_1 = tg.env.freespace_3d.ElectricDipole(
                    r_source=r_source, p_source=conf["p"][:3]
                )
            efield_2 = tg.env.IlluminationDipole(
                r_source=r_source, dp_source=conf["p"], n_dim=3
            )
            self.illum1_list.append(efield_1)
            self.illum2_list.append(efield_2)

            # 2D environment test-case
            self.env_list.append(tg.env.EnvHomogeneous2D(env_material=conf["eps_env"]))
            if sum(conf["p"][:3]) == 0:
                efield_1 = tg.env.freespace_2d.MagneticLineDipole(
                    r_source=r_source, m_source=conf["p"][3:]
                )
            else:
                efield_1 = tg.env.freespace_2d.ElectricLineDipole(
                    r_source=r_source, p_source=conf["p"][:3]
                )
            efield_2 = tg.env.IlluminationDipole(
                r_source=r_source, dp_source=conf["p"], n_dim=2
            )
            self.illum1_list.append(efield_1)
            self.illum2_list.append(efield_2)

    def test_compare_dipole_sources(self):
        wavelength = 500.0
        for device in self.devices:
            for i, conf in enumerate(self.conf_dicts):
                self.r_probe = self.r_probe.to(device=device)
                env = self.env_list[i]
                source_1 = self.illum1_list[i]
                source_2 = self.illum2_list[i]

                env.set_device(device)
                source_1.set_device(device)
                source_2.set_device(device)

                e0_1 = source_1.get_efield(
                    self.r_probe, wavelength=wavelength, environment=env
                )
                h0_1 = source_1.get_hfield(
                    self.r_probe, wavelength=wavelength, environment=env
                )
                e0_2 = source_2.get_efield(
                    self.r_probe, wavelength=wavelength, environment=env
                )
                h0_2 = source_2.get_hfield(
                    self.r_probe, wavelength=wavelength, environment=env
                )

            # compare fields
            torch.testing.assert_close(e0_1, e0_2)
            torch.testing.assert_close(h0_1, h0_2)
            if self.verbose:
                print("  - {}: dipole source comparison passed.".format(device))


# %%


if __name__ == "__main__":
    print("testing illumination fields.")
    torch.set_printoptions(precision=7)
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
