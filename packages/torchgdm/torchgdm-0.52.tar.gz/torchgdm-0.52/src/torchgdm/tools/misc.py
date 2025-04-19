# -*- coding: utf-8 -*-
"""
various helper for torchgdm
"""
# %%
from typing import Optional
import warnings
import gc

import torch

try:
    from psutil import virtual_memory
except ModuleNotFoundError:

    def virtual_memory():
        warnings.warn("Package `psutil` not found. Install for automatic memory purge.")

        class mem_class:
            percent = 0.0

        return mem_class()


from torchgdm.constants import ERROR_ON_WAVELENGTH_MISSMATCH


# --- setting global device
def set_default_device(device):
    """set specific device as global default"""
    import torchgdm as tg
    import torchgdm.constants as tgc

    if str(device).lower().startswith("cuda"):
        if not torch.cuda.is_available():
            warnings.warn("CUDA not available. Fall back to 'cpu'.")
            device = "cpu"

    if str(device).lower().startswith("cpu"):
        if not torch.cpu.is_available():
            raise ValueError("Unexpected error. CPU not available.")

    tgc.DEFAULT_DEVICE = device
    tg.device = device


def get_default_device():
    """return current default device"""
    import torchgdm.constants as tgc

    return tgc.DEFAULT_DEVICE


def use_cuda(use_cuda: bool = True, verbose=True):
    """set first CUDA device as default"""
    if use_cuda:
        set_default_device("cuda")
    else:
        set_default_device("cpu")

    if verbose:
        import torchgdm.constants as tgc

        print("torchGDM: Default device set to '{}'".format(tgc.DEFAULT_DEVICE))
        if tgc.DEFAULT_DEVICE.lower().startswith("cuda"):
            print(
                "          {}".format(
                    torch.cuda.get_device_properties(tgc.DEFAULT_DEVICE).name
                )
            )
            print(
                "          total VRAM: {:.1f} MiB".format(
                    torch.cuda.get_device_properties(tgc.DEFAULT_DEVICE).total_memory
                    / 1024**2
                )
            )


# --- progress bar via tqdm
def tqdm(iterable, progress_bar=True, title="", **kwargs):
    """wrapper to `tqdm` progress bar with optional `title`

    Args:
        iterable (iterable): iterable for loop over which to show a progress bar
        progress_bar (bool, optional): generic way to deactivate the progress bar. Defaults to True.
        title (str, optional): optional title of the progress bar. Defaults to "".
        **kwargs are passed to :func:`tqdm.tqdm`

    Returns:
        iterable: wrapped iterable that will show a progress bar when iterated over
    """
    if progress_bar:
        try:
            from tqdm import tqdm

            pbar = tqdm(iterable, **kwargs)
            pbar.set_description(title)
            return pbar
        except (ModuleNotFoundError, ImportError):
            # if tqdm not installed, replace by nothing
            warnings.warn(
                "Progress bar requires `tqdm`, seems to be not installed. You may try 'pip install tqdm'."
            )
            return iterable
    else:
        return iterable


# # !! TODO
# class Memoize:
#     """decorator for memoizing"""
#     def __init__(self, func, len_memory=10000):
#         self.func = func
#         self.memory = {}
#         self.len_memory = len_memory
#         self.i_call = 0

#     def __call__(self, *args, **kwargs):
#         self.i_call += 1
#         if len(self.memory) > self.len_memory:
#             self.memory.clear()

#         # !!! TODO: Hashing of input arguments
#         hash_args = ...
#         if not hash_args in self.memory:
#             # print(self.i_call, len(self.memory), "not pre-calculated.")
#             self.memory[hash_args] = self.func(*args, **kwargs)
#         # else:
#             # print(self.i_call, len(self.memory), "already pre-calculated!")
#         return self.memory[hash_args]

#     def __get__(self, obj, objtype):
#         '''Support instance methods.'''
#         return functools.partial(self.__call__, obj)


def deprecated(func):
    def batched_func(*args, **kwargs):
        warnings.warn(
            f"Deprecation warning: the '{func.__name__}' function"
            + " will be removed in a future release."
        )
        return func(*args, **kwargs)

    return batched_func


def get_closest_wavelength(sim, wavelength: float, raise_exception=None):
    """get closest available wavelength in the simulation

    Args:
        sim (:class:`torchgdm.Simulation`): simulation instance
        wavelength (float): target wavelength in nm
        raise_exception (bool, optional): If None (default), use global configuration in `torchgdm.constants.ERROR_ON_WAVELENGTH_MISSMATCH`. If True, raise an error if exact wavelength not available, if False just emit a warning. Defaults to None.

    Raises:
        ValueError: if wavelength is not available and `raise_exception=True`

    Returns:
        float: closest available match to `wavelength`
    """
    wavelength = float(wavelength)

    if wavelength not in sim.fields_inside:
        if ERROR_ON_WAVELENGTH_MISSMATCH:
            raise ValueError(
                "Requested wavelength ({}nm) not available.".format(wavelength)
            )
        else:
            wl = float(
                sim.wavelengths[torch.argmin(torch.abs(wavelength - sim.wavelengths))]
            )
            warnings.warn(
                "Requested wavelength ({}nm) not available. Use closest match: {}nm.".format(
                    wavelength, wl
                )
            )
    else:
        wl = wavelength

    return wl


def sum_of_list_elements(lst):
    """sum of list, element wise"""
    if len(lst) == 1:
        return lst[0]

    l_sum = lst[0]
    for _l in lst[1:]:
        l_sum += _l

    return l_sum


def concatenation_of_list_elements(lst):
    """sequential concatenation of all list elements"""
    if len(lst) == 1:
        return lst[0]

    l_sum = lst[0]
    for _l in lst[1:]:
        l_sum = l_sum.cat(_l)

    return l_sum


def ptp(input: torch.Tensor, dim: Optional[int] = None, keepdim=False) -> torch.Tensor:
    """Range of values (maximum - minimum) along an axis.

    simple torch implementation of :func:`numpy.ptp`

    Args:
        input (torch.Tensor): Input values.
        dim (Optional[int], optional): Axis along which to find the peaks. Defaults to None.
        keepdim (bool, optional): If this is set to True, the axes which are reduced are left in the result as dimensions with size one. Defaults to False.

    Returns:
        torch.Tensor: The range of a given input tensor - scalar if one-dimensional or an array holding the result along the given axis
    """
    if dim is None:
        return input.max() - input.min()
    return input.max(dim, keepdim).values - input.min(dim, keepdim).values


def to_np(input: torch.Tensor, warn_detach_fail=False):
    """detach tensor and convert to numpy array
    
    Args:
        input (torch.Tensor): tensor to convert to numpy
        warn_detach_fail (bool, optional): If True, warn on failed conversion (for example if input is already a numpy array). Defaults to False.

    Returns:
        numpy.ndarray: `input` converted to numpy array. If conversion fails, return original `input`
    """
    try:
        return input.detach().cpu().numpy()
    except AttributeError:
        if warn_detach_fail:
            warnings.warn("Torch.Tensor detach failed. Returning original input instead.")
        return input


# %% - private test functions and helper


# environment
def _check_environment(environment, N_dim=None, device=None):
    from torchgdm.env import EnvHomogeneous2D
    from torchgdm.env import EnvHomogeneous3D

    if device is None:
        device = get_default_device()

    if environment is None:
        if N_dim == 2:
            env = EnvHomogeneous2D(device=device)
            warnings.warn(
                "No environment specified. Falling back to a 2D vacuum environment."
            )
        elif N_dim == 3:
            env = EnvHomogeneous3D(device=device)
            warnings.warn(
                "No environment specified. Falling back to a 3D vacuum environment."
            )
        else:
            raise ValueError(f"No valid environment and dimension specified.")

    elif type(environment) in [complex, float, int]:
        if type(environment) == complex:
            assert environment.imag == 0, "only absorptionless environments supported."
            environment = environment.real
        if N_dim == 2:
            env = EnvHomogeneous2D(env_material=environment, device=device)
        elif N_dim == 3:
            env = EnvHomogeneous3D(env_material=environment, device=device)
        elif N_dim is None:
            raise ValueError(f"dimension must be given if environement is not given as class instance.")
        else:
            raise ValueError(f"{N_dim}-dim simulations not supported.")
    else:
        env = environment
        if device is not None:
            env.set_device(device)

    # test dimension, if indicated
    if N_dim is not None:
        if env.n_dim != N_dim:
            raise ValueError(
                f"expected {N_dim}D environement (got {env.n_dim}D). "
                + "Please use a compatible environment."
            )

    return env


def _purge_mem(obj=None, dev=None, pruge_threshold=0.8):
    """purge RAM and GPU VRAM

    RAM will be purged only if occupied RAM > `pruge_threshold`

    Args:
        obj (any torch instance, optional): optional torch object to get device from. Defaults to None.
        dev (str or torch.device, optional): specify torch device for pruge. Defaults to None.
        pruge_threshold (float, optional): threshold above which to run garbage collector. Defaults to 0.8.
    """
    if obj is not None:
        try:
            dev = obj.device.type
        except AttributeError:
            dev = ""

        del obj

    # purge cuda cache if applicable
    if dev is not None:
        if type(dev) == torch.device:
            dev = dev.type
        if dev.startswith("cuda"):
            torch.cuda.empty_cache()

    # garbage collect if memory almost full
    if virtual_memory().percent > 0.8 * 100:
        gc.collect()


def _test_positional_input(r1: torch.tensor, r2: torch.tensor):
    """test shapes of positional inputs for correct broadcasting"""
    if r1.device != r2.device:
        r2 = r2.to(r1.device)

    if len(r1.shape) == 1:
        if r1.shape[0] != 3:
            raise ValueError(
                "single point needs to be cartesian coordinate with 3 values."
            )
        # single point: expand dim
        r1 = r1[None, :]
        r2 = r2[None, :]
    elif len(r1.shape) == 2:
        if r1.shape[1] != 3:
            raise ValueError("points need to be cartesian coordinates with 3 values.")

    return r1, r2


def _tensor_is_diagonal_and_identical(tensor: torch.Tensor):
    """Check if a tensor is diagonal and all elements are identical"""
    device = tensor.device
    # Check if all off-diagonal elements are zero
    off_diagonal_mask = ~torch.eye(tensor.size(0), dtype=torch.bool, device=device)
    if tensor.masked_select(off_diagonal_mask).nonzero().size(0) > 0:
        return False

    # Check if all diagonal elements are equal
    diag = tensor.diagonal()
    if not torch.all(diag == diag[0]):
        return False

    return True


def _test_illumination_field_config_exists(
    sim,
    wavelength: float,
    illumination_index: int = None,
    raise_exception=True,
):
    """test if an illumination configuration exists and has been simulated yet

    Args:
        sim (:class:`torchgdm.Simulation`): simulation instance
        wavelength (float): in nm
        illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.
        raise_exception (bool, optional): whether to raise an error if illumination not present or not evaluated. Defaults to True.

    Returns:
        bool: True if illumination exists and was calculated, else False
    """
    if float(wavelength) in sim.fields_inside:
        if illumination_index is not None:
            if (
                len(sim.fields_inside[float(wavelength)].efield) <= illumination_index
            ) or (illumination_index < 0):
                field_exists = False
            else:
                field_exists = True
        else:
            field_exists = True
    else:
        field_exists = False

    if len(sim.fields_inside) == 0:
        field_exists = False

    if field_exists:
        return True
    else:
        if raise_exception:
            raise ValueError(
                "Field configuration does not exist (wavelength: "
                + "{}nm, illumination index {}).".format(wavelength, illumination_index)
            )
        else:
            return False


def _test_illumination_field_is_plane_wave(
    sim, illumination_index=None, raise_exception=False, message=""
):
    """test if the illumination is a plane wave

    This is used internally to verify correct usage of cross-section calculation

    Args:
        sim (:class:`torchgdm.Simulation`): simulation instance
        illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.
        raise_exception (bool, optional): If True, raise an error, if False just a warning. Defaults to False.
        message (str, optional): optional pre-posted message to warning / error. Defaults to "".

    Raises:
        Exception: if illumination is not a plane wave and `raise_exception=True`
    """
    pw_class_name = "free space plane wave"
    e_inc_names = [e_inc.__name__ for e_inc in sim.illumination_fields]
    if illumination_index is not None:
        e_inc_names = [e_inc_names[illumination_index]]

    for i, _n in enumerate(e_inc_names):
        if not _n.startswith(pw_class_name):
            if illumination_index is not None:
                i_f = illumination_index
            else:
                i_f = i

            if raise_exception:
                raise Exception(message + f"Field config #{i_f} is not a plane wave!")
            else:
                warnings.warn(message + f"Field config #{i_f} is not a plane wave!")
