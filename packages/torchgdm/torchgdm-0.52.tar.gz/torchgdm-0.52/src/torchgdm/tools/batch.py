# -*- coding: utf-8 -*-
"""batch processing tools:

- general batched evaluations (to limit memory usage)
- multi-wavelength evaluation of spectra
- tools for multi-illumination batched calculations

"""
# %%
import warnings
import gc
import typing

import torch

from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX
from torchgdm.tools.misc import get_default_device
from torchgdm.tools.misc import deprecated
from torchgdm.tools.misc import tqdm, _test_illumination_field_config_exists


def batched(
    batch_kwarg: str,
    arg_position: int = None,
    out_dim_batch: int = 0,
    default_batch_size: int = 256,
    title="batched evaluation",
):
    """decorator to wrap a function for mini-batch evaluation

    Notes:
        - useful to avoid memory problems in large calculations
        - batched input parameter must be specified as kwarg.
        - func must return a torch tensor, a tuple of such or a dict containing such

    Args:
        batch_kwarg (str): kwarg of batched function that receives multiple configurations, for which batches are created
        arg_position (int, optional): position of the argument that receives a list for which batches are created. Defaults to None.
        out_dim_batch (int, optional): concatenation dimension of the original function's output. Defaults to 0.
        default_batch_size (int, optional): Defaults to 256.
        title (str, optional): title to show for the optional progress bar. Defaults to "batched evaluation".
    """

    def wrap(func):
        def batched_func(
            *args,
            batch_size=default_batch_size,
            progress_bar=False,
            pgr_bar_title=None,
            **kwargs,
        ):
            if pgr_bar_title is None:
                pgr_bar_title = title
            # get batched argument, try kwarg first. If not given, try positional arg
            try:
                d = kwargs[batch_kwarg]
            except KeyError as e:
                if arg_position is None:
                    raise e
                else:
                    d = args[arg_position]
                    args = list(
                        args
                    )  # hacky way to remove the batched arg. as it will be passed as kwarg.
                    args.pop(arg_position)
            N = len(d)

            # --- loop over batches
            def loop_batches(batch_size):
                results = []
                if progress_bar:
                    iterator = tqdm(range(0, N, batch_size), title=pgr_bar_title)
                else:
                    iterator = range(0, N, batch_size)
                # if progress_bar in kwargs:
                #     kwargs.pop("progress_bar")

                for i in iterator:
                    kwargs[batch_kwarg] = d[i : i + batch_size]
                    result = func(*args, **kwargs)

                    results.append(result)
                return results

            try:
                results = loop_batches(batch_size=batch_size)
            except torch.cuda.OutOfMemoryError as e:
                if batch_size > 1:
                    warnings.warn(
                        "CUDA out of memory exception occurred. "
                        + "Current batch_size={}. ".format(batch_size)
                        + "Re-trying with batch_size=1. "
                        + "This may be inefficient, and you may want "
                        + "to try setting `batch_size` yourself."
                    )
                    results = loop_batches(batch_size=1)
                else:
                    print(
                        "Out of CUDA memory. Try to reduce `batch_size` (currently, batch_size={})!".format(
                            batch_size
                        )
                    )
                    raise e

            # --- concatenate output batches
            # case multiple outputs
            if type(results[0]) == tuple:
                return [
                    torch.cat([res[i_out] for res in results], dim=out_dim_batch)
                    for i_out in range(len(results[0]))
                ]

            # case dictionary output
            if type(results[0]) == dict:
                # print("WARNING: NOT YET TESTED!! DOES IT WORK??")
                dict_out = dict()
                for k in results[0]:
                    dict_out[k] = torch.cat(
                        [_d[k] for _d in results], dim=out_dim_batch
                    )
                return dict_out

            # case single torch tensor outputs
            else:
                return torch.cat(results, dim=out_dim_batch)

        return batched_func

    return wrap


# --- helper for wavelength batched evaluation
def calc_spectrum(
    sim,
    func,
    illumination_index=None,
    progress_bar=True,
    progress_bar_title="spectrum",
    **kwargs,
):
    """calculate spectrum for all wavelengths defined in simulation

    kwargs are passed to `func`

    Args:
        sim (`torchgdm.Simulation`): simulation (`sim.run()` needs to have been executed before)
        func (`typing.Callable`): function to call with simulation. Needs to accept following kwargs: `sim`, `wavelength` and `illumination_index`
        illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.
        progress_bar (bool): Whether to show a progress bar. Defaults to True

    Returns:
        dict: spectra results
         - contains spectra-lists with results returned by func
         - contains wavelengths
         - contains illumination field configs
    """
    wavelengths = sim.wavelengths

    # loop through wavelengths, add results to dict
    spectrum_results = {}
    for wl in tqdm(wavelengths, progress_bar, title=progress_bar_title):
        results = func(
            sim=sim,
            wavelength=wl,
            illumination_index=illumination_index,
            progress_bar=False,
            **kwargs,
        )
        for k in results:
            if k != "e0_config":
                if k not in spectrum_results:
                    spectrum_results[k] = []
                spectrum_results[k].append(results[k])

    # if `func` result is a single tensor, stack tensors of spectrum
    for k in spectrum_results:
        if type(results[k]) == torch.Tensor:
            spectrum_results[k] = torch.stack(spectrum_results[k])

    # add wavelengths and return dict containing all spectra
    if "wavelengths" not in spectrum_results:
        spectrum_results["wavelengths"] = wavelengths

    # add information on illumination field config
    spectrum_results = add_illuminations_info_to_dict(
        sim, spectrum_results, illumination_index=illumination_index
    )

    return spectrum_results


# --- helper for raster-scan type multiple illuminations batch evaluation
def calc_rasterscan(sim, func, wavelength, kw_r="r_focus", **kwargs):
    """calculate rasterscan, using all field configurations defined in the simulation

    kwargs are passed to `func`

    Args:
        sim (`torchgdm.Simulation`): simulation (`sim.run()` needs to have been executed before)
        func (`typing.Callable`): function to call with simulation. Needs to accept following kwargs: `sim`, `wavelength` and `illumination_index`
        wavelength (float): in nm
        kw_r (`str`): kwarg used for scan position of rasterscan

    Returns:
        dict: rasterscan results
         - contains wavelength
         - contains lists with rasterscan results at each pos returned by func
         - contains positions of illumination
    """
    # loop through illuminations
    pos = []
    for i, e_inc in enumerate(sim.illumination_fields):
        pos.append(getattr(e_inc, kw_r))
    pos = torch.stack(pos).to(device=sim.device, dtype=DTYPE_FLOAT)
    rs_results = dict(positions=pos)

    # evaluate and loop through results
    all_conf_res = func(sim=sim, wavelength=wavelength, **kwargs)

    for key in all_conf_res:
        if key != "e0_config":
            if key not in rs_results:
                rs_results[key] = []
            rs_results[key].append(all_conf_res[key])

    # if `func` result is a single tensor, stack tensors of spectrum
    for key in rs_results:
        if key not in ["positions", "wavelength"]:
            if type(all_conf_res[key]) == torch.Tensor:
                rs_results[key] = torch.stack(rs_results[key])

    # add working wavelength
    rs_results["wavelength"] = wavelength

    return rs_results


# --- helper for illumination field batch evaluation
def get_p_m_radiative_correction_prefactors(sim, wavelength: float, **kwargs):
    """get radiative absorption cross-section correction corrections at polarizable locations

    further kwargs are ignored

    Args:
        sim (`torchgdm.Simulation`): simulation (`sim.run()` needs to have been executed before)
        wavelength (float): in nm

    Returns:
        tuple: Two `torch.Tensor` with the radiative corrections for all polarizable electric and magnetic dipoles. of shape: (N_polarizable_p, 3) and (N_polarizable_m, 3)
    """
    idx_p, idx_m = sim._get_polarizable_positions_indices_p_m()

    rad_corr_factor_p = torch.cat(
        [
            _s.get_radiative_correction_prefactor_p(wavelength, sim.environment)
            for _s in sim.structures
        ]
    )

    rad_corr_factor_m = torch.cat(
        [
            _s.get_radiative_correction_prefactor_m(wavelength, sim.environment)
            for _s in sim.structures
        ]
    )

    # keep only for polarizable locations
    rad_corr_p = torch.index_select(rad_corr_factor_p, 0, idx_p)
    rad_corr_m = torch.index_select(rad_corr_factor_m, 0, idx_m)

    return rad_corr_p, rad_corr_m


# - illumination tools
def get_k0_vec(
    sim,
    wavelength: float,
    r_probe: torch.Tensor,
    illumination_index: int = None,
    **kwargs,
):
    """get illumination wave vector at `r`

    Note: For a non-plane wave field, the scaled time-averaged Poynting vector is used, which is identical to the wave vector only in isotropic media.

    further kwargs are ignored

    Args:
        sim (`torchgdm.Simulation`): simulation (`sim.run()` needs to have been executed before)
        wavelength (float): in nm
        r (torch.Tensor): position(s) at which to evaluate incident field's wave vector
        illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.

    Returns:
        torch.Tensor: wave vector(s) at `r`
    """
    k0_list = []
    for f_inc in sim.illumination_fields:
        try:
            propagation_vector = f_inc.k_vec_unit.real
            if len(propagation_vector.shape) == 1:
                propagation_vector = propagation_vector.unsqueeze(0)
        except AttributeError:
            warnings.warn(
                "Global wavevector not defined in illumination field class. "
                + "Using local time averaged Poynting vector. "
                + "Note that this is identical to the wave vector only in isotropic media."
            )
            e0 = f_inc.get_efield(
                r_probe, wavelength=wavelength, environment=sim.environment
            )
            h0 = f_inc.get_hfield(
                r_probe, wavelength=wavelength, environment=sim.environment
            )
            propagation_vector = torch.cross(torch.conj(e0), h0, dim=-1).real

        # normalize to wavenumber
        k0_unit = propagation_vector / torch.linalg.norm(propagation_vector)
        k0 = k0_unit * 2 * torch.pi / wavelength
        k0_list.append(k0)

    k0_list = torch.stack(k0_list, dim=0).to(dtype=DTYPE_FLOAT, device=sim.device)
    if illumination_index is not None:
        k0_list = k0_list[illumination_index].unsqueeze(0)
    return k0_list


def get_illuminations_info(sim, illumination_index: int = None, **kwargs):
    """get dict with configuration info of the illumination(s)

    further kwargs are ignored
    """
    e0_info = [e_inc.get_info() for e_inc in sim.illumination_fields]

    if illumination_index is not None:
        e0_info = [e0_info[illumination_index]]

    return e0_info


def add_illuminations_info_to_dict(
    sim, data_dict, illumination_index: int = None, **kwargs
):
    """add illumination information to `data_dict` as key 'e0_config'

    further kwargs are ignored
    """
    if "e0_config" not in data_dict:
        data_dict["e0_config"] = get_illuminations_info(
            sim=sim, illumination_index=illumination_index
        )
    else:
        warnings.warn("dict already contains `e0_config` key. Do nothing.")
    return data_dict
