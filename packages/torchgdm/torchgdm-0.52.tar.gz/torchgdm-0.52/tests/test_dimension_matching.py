# encoding=utf-8
# %%
import unittest
import warnings

import torch

import torchgdm as tg


class TestDimensionMatching(unittest.TestCase):

    def setUp(self):
        self.verbose = False
        if self.verbose:
            print("testing 3D discretized simulation, plane wave illumination...")

        # --- determine if GPU is available
        self.devices = ["cpu"]
        if torch.cuda.is_available():
            self.devices.append("cuda:0")

    def test_check_dimensions_verifications(self):
        for device in self.devices:
            # ignore warnings temporarily:
            warnings.simplefilter("ignore")
            
            wavelengths = torch.linspace(600.0, 700.0, 2)
            # - some dummy material
            material = tg.materials.MatConstant(3.0)

            # - fields
            e02d = tg.env.freespace_2d.PlaneWave()
            e03d = tg.env.freespace_3d.PlaneWave()

            # - environments
            env2d = tg.env.EnvHomogeneous2D(1.0)
            env3d = tg.env.EnvHomogeneous3D(1.0)

            # - structures
            # 2D
            s2d_mesh = tg.struct2d.StructDiscretizedSquare2D(
                discretization_config=tg.struct2d.square(2),
                step=10,
                materials=material,
            )
            try:
                s2d_line = s2d_mesh.convert_to_effective_polarizability_pair(
                    environment=env3d,
                    wavelengths=wavelengths,
                    verbose=False,
                    progress_bar=False,
                )
                raise Exception("ERROR! EXTRACT 2D with 3D ENV SHOULD RAISE AN ERROR!!")
            except ValueError:
                pass
            s2d_line = s2d_mesh.convert_to_effective_polarizability_pair(
                environment=env2d,
                wavelengths=wavelengths,
                verbose=False,
                progress_bar=False,
            )

            # 3D
            s3d_mesh = tg.struct3d.StructDiscretizedCubic3D(
                discretization_config=tg.struct3d.cube(2),
                step=10,
                materials=tg.materials.MatConstant(2.25),
            )
            try:
                s3d_point = s3d_mesh.convert_to_effective_polarizability_pair(
                    environment=env2d,
                    wavelengths=wavelengths,
                    verbose=False,
                    progress_bar=False,
                )
                raise Exception("ERROR! EXTRACT 3D with 2D ENV SHOULD RAISE AN ERROR!!")
            except ValueError:
                pass
            s3d_point = s3d_mesh.convert_to_effective_polarizability_pair(
                environment=env3d,
                wavelengths=wavelengths,
                verbose=False,
                progress_bar=False,
            )
            
            test_cases = [
                [s2d_mesh, e02d, env2d, True],
                [s2d_line, e02d, env2d, True],
                [s2d_mesh, [e02d, e02d], env2d, True],
                [s3d_mesh, e03d, env3d, True],
                [s3d_point, e03d, env3d, True],
                [[s3d_mesh, s3d_point], [e03d, e03d], env3d, True],
                [s2d_line, e02d, env3d, False],
                [s3d_mesh, [e03d, e02d], env3d, False],
                [s3d_point, e03d, env2d, False],
                [[s2d_line, s2d_mesh], [e03d, e02d], env2d, False],
            ]

            # 3D Mie
            try:
                # ignore import warnings
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    import treams
                mie_test = True
            except ModuleNotFoundError:
                print(
                    "Skipping test. Mie tests require package `treams`. "
                    + "Please install via `pip install treams`."
                )
                mie_test = False
            if mie_test:
                try:
                    s3d_mie = tg.struct3d.StructMieSphereEffPola3D(
                        wavelengths, environment=env2d, materials=material, radii=100.0
                    )
                    raise Exception(
                        "ERROR! EXTRACT MIE (3D) with 2D ENV SHOULD RAISE AN ERROR!!"
                    )
                except ValueError:
                    pass
                s3d_mie = tg.struct3d.StructMieSphereEffPola3D(
                    wavelengths, environment=env3d, materials=material, radii=100.0
                )
            if mie_test:
                test_cases += [
                [s3d_mie, e03d, env3d, True],
                [s3d_mie, e02d, env3d, False],
                ]


            for i, _t in enumerate(test_cases):
                try:
                    sim = tg.Simulation(
                        structures=_t[0],
                        illumination_fields=_t[1],
                        environment=_t[2],
                        wavelengths=wavelengths,
                        device=device,
                    )
                    if not _t[3]:
                        raise Exception(
                            "Simulation dimensionality check passed but "
                            + f"should have failed on case {i}."
                        )
                except ValueError:
                    if _t[3] == False:
                        pass  # everything ok: An exception is expected in this config
                    else:
                        raise Exception(
                            "Simulation dimensionality check failed but "
                            + f"should have passed on case {i}."
                        )
            if self.verbose:
                print("  - {}: dimension check test passed.".format(device))


# %%
if __name__ == "__main__":
    print("testing simulation dimensionality check...")
    torch.set_printoptions(precision=7)
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
