# encoding=utf-8
# %%
import unittest

import torch

import torchgdm as tg


class TestGreensFreeSpace2D(unittest.TestCase):

    def setUp(self):
        self.verbose = False

        # --- determine if GPU is available
        self.devices = ["cpu"]
        if torch.cuda.is_available():
            self.devices.append("cuda")

        # --- setup a test case
        eps_env = 1.0
        self.mat_env = tg.materials.MatConstant(eps_env)

    def test_G2D_ky0(self):
        for device in self.devices:
            # positions and wavelength in nm
            env = tg.env.freespace_2d.EnvHomogeneous2D(
                env_material=self.mat_env, device=device
            )

            wl = torch.as_tensor(730.0)
            r_probe = torch.as_tensor(
                [50, 0, 70], dtype=tg.constants.DTYPE_FLOAT, device=device
            )
            r_source = torch.as_tensor(
                [73, 0, 99], dtype=tg.constants.DTYPE_FLOAT, device=device
            )

            G_ref = torch.as_tensor(
                [
                    [
                        [
                            -2.5220914e-04 + 1.1310077e-04j,
                            0.0000000e00 + 0.0000000e00j,
                            1.4593793e-03 + 1.4253797e-06j,
                            -0.0000000e00 + 0.0000000e00j,
                            2.8679229e-05 - 3.9634385e-04j,
                            0.0000000e00 - 0.0000000e00j,
                        ],
                        [
                            0.0000000e00 + 0.0000000e00j,
                            1.7823000e-04 + 2.2686829e-04j,
                            0.0000000e00 + 0.0000000e00j,
                            -2.8679229e-05 + 3.9634385e-04j,
                            -0.0000000e00 + 0.0000000e00j,
                            2.2745597e-05 - 3.1434168e-04j,
                        ],
                        [
                            1.4593793e-03 + 1.4253797e-06j,
                            0.0000000e00 + 0.0000000e00j,
                            4.3043910e-04 + 1.1376752e-04j,
                            0.0000000e00 + 0.0000000e00j,
                            -2.2745597e-05 + 3.1434168e-04j,
                            -0.0000000e00 + 0.0000000e00j,
                        ],
                        [
                            0.0000000e00 + 0.0000000e00j,
                            -2.8679229e-05 + 3.9634385e-04j,
                            -0.0000000e00 + 0.0000000e00j,
                            -2.5220914e-04 + 1.1310077e-04j,
                            0.0000000e00 + 0.0000000e00j,
                            1.4593793e-03 + 1.4253797e-06j,
                        ],
                        [
                            2.8679229e-05 - 3.9634385e-04j,
                            0.0000000e00 + 0.0000000e00j,
                            -2.2745597e-05 + 3.1434168e-04j,
                            0.0000000e00 + 0.0000000e00j,
                            1.7823000e-04 + 2.2686829e-04j,
                            0.0000000e00 + 0.0000000e00j,
                        ],
                        [
                            0.0000000e00 - 0.0000000e00j,
                            2.2745597e-05 - 3.1434168e-04j,
                            0.0000000e00 + 0.0000000e00j,
                            1.4593793e-03 + 1.4253797e-06j,
                            0.0000000e00 + 0.0000000e00j,
                            4.3043910e-04 + 1.1376752e-04j,
                        ],
                    ]
                ],
                device=device,
                dtype=tg.constants.DTYPE_COMPLEX,
            )
            G_test = env.get_G_6x6(r_probe, r_source, wl)
            # torch.set_printoptions(precision=7)
            # print(G_test)

            torch.testing.assert_close(G_test, G_ref)
            if self.verbose:
                print(
                    "  - {}: G-2D vacuum normal incidence test passed.".format(device)
                )

    def test_G2D_ky(self):
        for device in self.devices:
            # positions and wavelength in nm
            self.mat_env.set_device(device)
            env = tg.env.freespace_2d.EnvHomogeneous2D(
                env_material=self.mat_env, inc_angle_y=-torch.pi / 4, device=device
            )

            wl = torch.as_tensor(530.0, device=device)
            r_probe = torch.as_tensor(
                [20, 0, 33], dtype=tg.constants.DTYPE_FLOAT, device=device
            )
            r_source = torch.as_tensor(
                [-65, 0, -5], dtype=tg.constants.DTYPE_FLOAT, device=device
            )

            G_ref = torch.as_tensor(
                [
                    [
                        [
                            2.1607113e-04 + 2.8792763e-04j,
                            -7.2812261e-05 + 2.0167719e-04j,
                            2.0219064e-04 + 5.9515496e-06j,
                            -0.0000000e00 + 0.0000000e00j,
                            -4.6034576e-05 + 1.2750768e-04j,
                            3.3123157e-05 + 2.6643940e-04j,
                        ],
                        [
                            -7.2812261e-05 + 2.0167719e-04j,
                            2.3421604e-05 + 1.8840107e-04j,
                            -3.2551361e-05 + 9.0161549e-05j,
                            4.6034576e-05 - 1.2750768e-04j,
                            -0.0000000e00 + 0.0000000e00j,
                            -1.0297208e-04 + 2.8521454e-04j,
                        ],
                        [
                            2.0219064e-04 + 5.9515496e-06j,
                            -3.2551361e-05 + 9.0161549e-05j,
                            -1.4580631e-04 + 2.7727569e-04j,
                            -3.3123157e-05 - 2.6643940e-04j,
                            1.0297208e-04 - 2.8521454e-04j,
                            -0.0000000e00 + 0.0000000e00j,
                        ],
                        [
                            0.0000000e00 + 0.0000000e00j,
                            4.6034576e-05 - 1.2750768e-04j,
                            -3.3123157e-05 - 2.6643940e-04j,
                            2.1607113e-04 + 2.8792763e-04j,
                            -7.2812261e-05 + 2.0167719e-04j,
                            2.0219064e-04 + 5.9515496e-06j,
                        ],
                        [
                            -4.6034576e-05 + 1.2750768e-04j,
                            0.0000000e00 + 0.0000000e00j,
                            1.0297208e-04 - 2.8521454e-04j,
                            -7.2812261e-05 + 2.0167719e-04j,
                            2.3421604e-05 + 1.8840107e-04j,
                            -3.2551361e-05 + 9.0161549e-05j,
                        ],
                        [
                            3.3123157e-05 + 2.6643940e-04j,
                            -1.0297208e-04 + 2.8521454e-04j,
                            0.0000000e00 + 0.0000000e00j,
                            2.0219064e-04 + 5.9515496e-06j,
                            -3.2551361e-05 + 9.0161549e-05j,
                            -1.4580631e-04 + 2.7727569e-04j,
                        ],
                    ]
                ],
                device=device,
                dtype=tg.constants.DTYPE_COMPLEX,
            )
            G_test = env.get_G_6x6(r_probe, r_source, wl)
            # torch.set_printoptions(precision=7)
            # print(G_test)

            torch.testing.assert_close(G_test, G_ref)
            if self.verbose:
                print(
                    "  - {}: G-2D vacuum normal incidence test passed.".format(device)
                )

    def test_subtensors(self):
        for device in self.devices:
            for angle_ky in [0, torch.pi / 4, torch.pi / 2.1]:
                env = tg.env.freespace_2d.EnvHomogeneous2D(
                    env_material=self.mat_env, inc_angle_y=angle_ky, device=device
                )
                # positions and wavelength in nm
                wl = torch.as_tensor(
                    730.0, dtype=tg.constants.DTYPE_FLOAT, device=device
                )
                r_probe = torch.as_tensor(
                    [250, 0, 5], dtype=tg.constants.DTYPE_FLOAT, device=device
                )
                r_source = torch.as_tensor(
                    [244, 0, -2], dtype=tg.constants.DTYPE_FLOAT, device=device
                )
                env.set_device(device)

                G = env.get_G_6x6(r_probe, r_source, wl)
                GEp = env.get_G_Ep(r_probe, r_source, wl)
                GEm = env.get_G_Em(r_probe, r_source, wl)
                GHp = env.get_G_Hp(r_probe, r_source, wl)
                GHm = env.get_G_Hm(r_probe, r_source, wl)
                GEHp = env.get_G_EHp_6x3(r_probe, r_source, wl)
                GEHm = env.get_G_EHm_6x3(r_probe, r_source, wl)
                GEpm = env.get_G_Epm_3x6(r_probe, r_source, wl)
                GHpm = env.get_G_Hpm_3x6(r_probe, r_source, wl)

                # test correlated 3x3 tensors
                torch.testing.assert_close(GEp[0], GHm[0], rtol=1e-9, atol=1e-9)
                torch.testing.assert_close(GEm[0], -1 * GHp[0], rtol=1e-9, atol=1e-9)

                # test 3x3 tensors in 6x6 tensor
                torch.testing.assert_close(GEp[0], G[0, :3, :3], rtol=1e-9, atol=1e-9)
                torch.testing.assert_close(GHm[0], G[0, 3:, 3:], rtol=1e-9, atol=1e-9)
                torch.testing.assert_close(GHp[0], G[0, 3:, :3], rtol=1e-9, atol=1e-9)
                torch.testing.assert_close(GEm[0], G[0, :3, 3:], rtol=1e-9, atol=1e-9)

                # test 6x3 and 3x6 tensors
                torch.testing.assert_close(GEHp[0], G[0, :, :3], rtol=1e-9, atol=1e-9)
                torch.testing.assert_close(GEHm[0], G[0, :, 3:], rtol=1e-9, atol=1e-9)
                torch.testing.assert_close(GEpm[0], G[0, :3, :], rtol=1e-9, atol=1e-9)
                torch.testing.assert_close(GHpm[0], G[0, 3:, :], rtol=1e-9, atol=1e-9)

                if self.verbose:
                    print(
                        "  - {}: 2D subtensor consistency test passed.".format(device)
                    )


class TestGreensFreeSpace3D(unittest.TestCase):

    def setUp(self):
        self.verbose = False

        # --- determine if GPU is available
        self.devices = ["cpu"]
        if torch.cuda.is_available():
            self.devices.append("cuda:0")

        # --- setup a test case
        eps_env = 1.0
        mat_env = tg.materials.MatConstant(eps_env)
        self.env = tg.env.freespace_3d.EnvHomogeneous3D(env_material=mat_env)

    def test_G(self):
        for device in self.devices:
            self.env.set_device(device)
            
            # positions and wavelength in nm
            wl = torch.as_tensor(730.0, device=device)
            r_probe = torch.as_tensor(
                [50, 60, 70], dtype=tg.constants.DTYPE_FLOAT, device=device
            )
            r_source = torch.as_tensor(
                [73, -45, 99], dtype=tg.constants.DTYPE_FLOAT, device=device
            )

            G_ref = torch.as_tensor(
                [
                    [
                        [
                            -4.9245153e-07 + 3.5233521e-07j,
                            -5.0107946e-07 - 7.1189419e-09j,
                            1.3839337e-07 + 1.9661783e-09j,
                            0.0000000e00 + 0.0000000e00j,
                            4.8337917e-08 - 2.4580962e-07j,
                            1.7501657e-07 - 8.9000031e-07j,
                        ],
                        [
                            -5.0107946e-07 - 7.1189419e-09j,
                            1.6853248e-06 + 3.8327528e-07j,
                            -6.3179590e-07 - 8.9760874e-09j,
                            -4.8337917e-08 + 2.4580962e-07j,
                            0.0000000e00 + 0.0000000e00j,
                            3.8336964e-08 - 1.9495246e-07j,
                        ],
                        [
                            1.3839337e-07 + 1.9661783e-09j,
                            -6.3179590e-07 - 8.9760874e-09j,
                            -4.2771575e-07 + 3.5325488e-07j,
                            -1.7501657e-07 + 8.9000031e-07j,
                            -3.8336964e-08 + 1.9495246e-07j,
                            0.0000000e00 + 0.0000000e00j,
                        ],
                        [
                            0.0000000e00 - 0.0000000e00j,
                            -4.8337917e-08 + 2.4580962e-07j,
                            -1.7501657e-07 + 8.9000031e-07j,
                            -4.9245153e-07 + 3.5233521e-07j,
                            -5.0107946e-07 - 7.1189419e-09j,
                            1.3839337e-07 + 1.9661783e-09j,
                        ],
                        [
                            4.8337917e-08 - 2.4580962e-07j,
                            0.0000000e00 - 0.0000000e00j,
                            -3.8336964e-08 + 1.9495246e-07j,
                            -5.0107946e-07 - 7.1189419e-09j,
                            1.6853248e-06 + 3.8327528e-07j,
                            -6.3179590e-07 - 8.9760874e-09j,
                        ],
                        [
                            1.7501657e-07 - 8.9000031e-07j,
                            3.8336964e-08 - 1.9495246e-07j,
                            0.0000000e00 - 0.0000000e00j,
                            1.3839337e-07 + 1.9661783e-09j,
                            -6.3179590e-07 - 8.9760874e-09j,
                            -4.2771575e-07 + 3.5325488e-07j,
                        ],
                    ]
                ],
                device=device,
                dtype=tg.constants.DTYPE_COMPLEX,
            )
            G_test = self.env.get_G_6x6(r_probe, r_source, wl)
            # torch.set_printoptions(precision=7); print(G_test)

            torch.testing.assert_close(G_test, G_ref)
            if self.verbose:
                print("  - {}: 3D vacuum test passed.".format(device))

    def test_subtensors(self):
        for device in self.devices:
            # positions and wavelength in nm
            wl = torch.as_tensor(730.0, dtype=tg.constants.DTYPE_FLOAT, device=device)
            r_probe = torch.as_tensor(
                [250, 10, 5], dtype=tg.constants.DTYPE_FLOAT, device=device
            )
            r_source = torch.as_tensor(
                [244, -5, -2], dtype=tg.constants.DTYPE_FLOAT, device=device
            )
            self.env.set_device(device)

            G = self.env.get_G_6x6(r_probe, r_source, wl)
            GEp = self.env.get_G_Ep(r_probe, r_source, wl)
            GEm = self.env.get_G_Em(r_probe, r_source, wl)
            GHp = self.env.get_G_Hp(r_probe, r_source, wl)
            GHm = self.env.get_G_Hm(r_probe, r_source, wl)
            GEHp = self.env.get_G_EHp_6x3(r_probe, r_source, wl)
            GEHm = self.env.get_G_EHm_6x3(r_probe, r_source, wl)
            GEpm = self.env.get_G_Epm_3x6(r_probe, r_source, wl)
            GHpm = self.env.get_G_Hpm_3x6(r_probe, r_source, wl)

            # test correlated 3x3 tensors
            torch.testing.assert_close(GEp[0], GHm[0], rtol=1e-9, atol=1e-9)
            torch.testing.assert_close(GEm[0], -1 * GHp[0], rtol=1e-9, atol=1e-9)

            # test 3x3 tensors in 6x6 tensor
            torch.testing.assert_close(GEp[0], G[0, :3, :3], rtol=1e-9, atol=1e-9)
            torch.testing.assert_close(GHm[0], G[0, 3:, 3:], rtol=1e-9, atol=1e-9)
            torch.testing.assert_close(GHp[0], G[0, 3:, :3], rtol=1e-9, atol=1e-9)
            torch.testing.assert_close(GEm[0], G[0, :3, 3:], rtol=1e-9, atol=1e-9)

            # test 6x3 and 3x6 tensors
            torch.testing.assert_close(GEHp[0], G[0, :, :3], rtol=1e-9, atol=1e-9)
            torch.testing.assert_close(GEHm[0], G[0, :, 3:], rtol=1e-9, atol=1e-9)
            torch.testing.assert_close(GEpm[0], G[0, :3, :], rtol=1e-9, atol=1e-9)
            torch.testing.assert_close(GHpm[0], G[0, 3:, :], rtol=1e-9, atol=1e-9)

            if self.verbose:
                print("  - {}: 3D subtensor consistency test passed.".format(device))


# %%
if __name__ == "__main__":
    print("testing free space (2d & 3d) Green's tensors...")
    torch.set_printoptions(precision=7)
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
