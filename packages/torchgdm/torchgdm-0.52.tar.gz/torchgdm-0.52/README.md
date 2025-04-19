![torchgdm logo](https://homepages.laas.fr/pwiecha/_image_for_ext/torchgdm_logo.png)

# TorchGDM
> nano-optics full-field solver, written in PyTorch.

TorchGDM is a PyTorch implementation of the [Green's dyadic method (GDM)](https://doi.org/10.1088/0034-4885/68/8/R05), a electro-dynamics full-field volume integral technique. It's main features are mixed simulations **combining volume discretized and effective e/m dipole-pair polarizabilities**, as well as the general support of torch's **automatic differentiation**. 

TorchGDM is available on the [gitlab repository](https://gitlab.com/wiechapeter/torchgdm) and via [PyPi and pip](https://pypi.org/project/torchgdm/).  Please visit also the [TorchGDM documentation website](https://homepages.laas.fr/pwiecha/torchgdm_doc/).

TorchGDM is originally based on various theoretical works by [Christian Girard](https://scholar.google.de/citations?user=P3HnK28AAAAJ) at CEMES (see e.g. [Ch. Girard 2005 Rep. Prog. Phys. 68 1883](https://doi.org/10.1088/0034-4885/68/8/R05)), with contributions from G. Colas des Francs, A. Arbouet, R. Marty, C. Majorel, A. Patoux, Y. Brûlé and P. R. Wiecha.

If you use TorchGDM for your projects, please cite it.


## Getting started

Simulate and plot the scattering cross section spectrum between 550nm and 950nm of a GaN nano-cube (240nm side length), placed in vacuum, illuminated by an x-polarized plane wave:

```python
import torch
import matplotlib.pyplot as plt
import torchgdm as tg

# --- simulation setup
# - vacuum environment
mat_env = tg.materials.MatConstant(eps=1.0)
env = tg.env.EnvHomogeneous3D(env_material=mat_env)

# - illumination field(s) and wavelength
wavelengths = torch.linspace(550.0, 950.0, 25)
plane_wave = tg.env.freespace_3d.PlaneWave(e0p=1.0, e0s=0.0)

# - discretized structure
structure = tg.struct3d.StructDiscretizedCubic3D(
    discretization_config=tg.struct3d.cube(l=8),
    step=30.0,    # in nm
    materials=tg.materials.MatDatabase("GaN"),
)

# - define and run simulation.
sim = tg.Simulation(
    structures=[structure],
    illumination_fields=[plane_wave],
    environment=env,
    wavelengths=wavelengths,
)
sim.plot_structure()  # visualize structure
sim.run()             # run the main simulation

# - post-processing: cross sections
cs_results = sim.get_spectra_crosssections()

# plot
plt.figure(figsize=(5, 4))
plt.plot(tg.to_np(wavelengths), tg.to_np(cs_results["scs"]))
plt.xlabel("wavelength (nm)")
plt.ylabel("scs (nm^2)")
plt.show()
```


### GPU support

TorchGDM was tested on [CUDA](https://developer.nvidia.com/cuda-zone) GPUs and [google TPUs](https://cloud.google.com/tpu). All you need is a [GPU enabled version of pytorch](https://pytorch.org/get-started/locally/). Running on GPU can be enabled by using:

```python
  import torchgdm as tg
  tg.use_cuda(True)
```

Alternatively, GPU usage can be controlled by setting the device manually:

```python
  sim = tg.Simulation(...)
  sim.set_device("cuda")
```


## Features

List of features

General:

* pure python
* run on CPU and GPU, parallelized and vectorized
* full support of torch's automatic differentiation

Simulations:

* 2D and 3D discretized nano-structures
* 2D and 3D effective polarizabilities (electric and magnetic dipoles)
* mix of discretized / effective dipole-pair structures
* far-field (plane wave, focused Gaussian) and local illumination (point/line emitters)

Post-processing:

* cross sections (extinction, scattering, absorption)
* near-fields and far-fields
* optical chirality
* Poynting vector
* field gradients
* exact multipole decomposition
* Green's tensors in complex environments
* LDOS / decay rate
* efficient rasterscan simulations
* extract ED/MD dipole pair effective polarizability models
* plotting tools for convenient 2D / 3D visualizations
* ...

Extensible:

* Object-oriented extensibility
* materials
* structures
* illuminations
* environments (via adequate Green's tensors)


## Installing / Requirements

TorchGDM is pure python, so install via pip is possible on all major operating systems:

```shell
pip install -U torchgdm
```

TorchGDM was tested under linux and windows with python versions 3.9 to 3.12. 
It requires following python packages

- **pytorch** (v2.0+)
- **numpy**

Following not strictly required packages will be automatically installed:

- **scipy** (for several tools)
- **tqdm** (progress bars)
- **pyyaml** (support for refractiveindex.info permittivity data)
- **matplotlib** (2d plotting)
- **alphashape** (2d contour plotting)
- **psutil** (for automatic memory purge)

Further optional dependencies

- **treams** (for Mie theory tools)
- **pyvista** (3d visualizations)
- **ipywidgets**, **jupyterlab** and **trame** (for jupyter inline 3D visualizations)
- **scikit-learn** (automatic GPM extraction)
- **pymiecs** (for some Mie theory unit tests)

(install all optional dependencies via pip: `pip install -U torchgdm[all]`)


## Contributing

If you'd like to contribute, please fork the repository and use a feature
branch. Pull requests are warmly welcome.


## Links

- torchgdm documentation: [https://homepages.laas.fr/pwiecha/torchgdm_doc/](https://homepages.laas.fr/pwiecha/torchgdm_doc/)
- link to PyPi: [https://pypi.org/project/torchgdm/](https://pypi.org/project/torchgdm/)
- gitlab repository: [https://gitlab.com/wiechapeter/torchgdm](https://gitlab.com/wiechapeter/torchgdm)
- issue tracker: [https://gitlab.com/wiechapeter/torchgdm/-/issues](https://gitlab.com/wiechapeter/torchgdm/-/issues)
  - in case of sensitive bugs you can also contact me directly at
    pwiecha|AT|laas|DOT|fr.
- related projects:
  - pyGDM2: [https://homepages.laas.fr/pwiecha/pygdm_doc/](https://homepages.laas.fr/pwiecha/pygdm_doc/)


## Licensing

The code in this project is licensed under the [GNU GPLv3](http://www.gnu.org/licenses/).
