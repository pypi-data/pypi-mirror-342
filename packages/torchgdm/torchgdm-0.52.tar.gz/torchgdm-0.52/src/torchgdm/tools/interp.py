# -*- coding: utf-8 -*-
"""
torch-based linear interpolation
"""
# %%
from itertools import product

import torch

from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX
from torchgdm.tools.misc import get_default_device


class RegularGridInterpolator:
    """
    `RegularGridInterpolator` from S. Barrett:
    https://github.com/sbarratt/torch_interpolations
    published under Apache V2 license

    Copyright (C) 2020, S. Barrett

    Licensed to the Apache Software Foundation (ASF) under one
    or more contributor license agreements.  See the NOTICE file
    distributed with this work for additional information
    regarding copyright ownership.  The ASF licenses this file
    to you under the Apache License, Version 2.0 (the
    "License"); you may not use this file except in compliance
    with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing,
    software distributed under the License is distributed on an
    "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
    KIND, either express or implied.  See the License for the
    specific language governing permissions and limitations
    under the License.
    """

    def __init__(self, points, values):
        self.points = points
        self.values = values

        assert isinstance(self.points, tuple) or isinstance(self.points, list)
        assert isinstance(self.values, torch.Tensor)

        self.ms = list(self.values.shape)
        self.n = len(self.points)

        assert len(self.ms) == self.n

        for i, p in enumerate(self.points):
            assert isinstance(p, torch.Tensor)
            assert p.shape[0] == self.values.shape[i]

    def __call__(self, points_to_interp):
        assert self.points is not None
        assert self.values is not None

        assert len(points_to_interp) == len(self.points)
        K = points_to_interp[0].shape[0]
        for x in points_to_interp:
            assert x.shape[0] == K

        idxs = []
        dists = []
        overalls = []
        for p, x in zip(self.points, points_to_interp):
            idx_right = torch.bucketize(x, p)
            idx_right[idx_right >= p.shape[0]] = p.shape[0] - 1
            idx_left = (idx_right - 1).clamp(0, p.shape[0] - 1)
            dist_left = x - p[idx_left]
            dist_right = p[idx_right] - x
            dist_left[dist_left < 0] = 0.0
            dist_right[dist_right < 0] = 0.0
            both_zero = (dist_left == 0) & (dist_right == 0)
            dist_left[both_zero] = dist_right[both_zero] = 1.0

            idxs.append((idx_left, idx_right))
            dists.append((dist_left, dist_right))
            overalls.append(dist_left + dist_right)

        numerator = 0.0
        for indexer in product([0, 1], repeat=self.n):
            as_s = [idx[onoff] for onoff, idx in zip(indexer, idxs)]
            bs_s = [dist[1 - onoff] for onoff, dist in zip(indexer, dists)]
            numerator += self.values[as_s] * torch.prod(torch.stack(bs_s), dim=0)
        denominator = torch.prod(torch.stack(overalls), dim=0)
        return numerator / denominator


def interp1d(x_eval: torch.Tensor, x_dat: torch.Tensor, y_dat: torch.Tensor):
    """1D bilinear interpolation

    simple torch implementation of :func:`numpy.interp`

    Args:
        x_eval (torch.Tensor): The x-coordinates at which to evaluate the interpolated values.
        x_dat (torch.Tensor): The x-coordinates of the data points
        y_dat (torch.Tensor): The y-coordinates of the data points, same length as `x_dat`.

    Returns:
        torch.Tensor: The interpolated values, same shape as `x_eval`
    """
    assert len(x_dat) == len(y_dat)
    assert not torch.is_complex(x_dat)

    # sort x input data
    i_sort = torch.argsort(x_dat)
    _x = x_dat[i_sort]
    _y = y_dat[i_sort]

    # find left/right neighbor x datapoints
    idx_r = torch.bucketize(x_eval, _x)
    idx_l = idx_r - 1
    idx_r = idx_r.clamp(0, _x.shape[0] - 1)
    idx_l = idx_l.clamp(0, _x.shape[0] - 1)

    # distances to left / right (=weights)
    dist_l = x_eval - _x[idx_l]
    dist_r = _x[idx_r] - x_eval
    dist_l[dist_l < 0] = 0.0
    dist_r[dist_r < 0] = 0.0
    dist_l[torch.logical_and(dist_l == 0, dist_r == 0)] = 1.0
    sum_d_l_r = dist_l + dist_r
    y_l = _y[idx_l]
    y_r = _y[idx_r]

    # bilinear interpolated values
    y_eval = (y_l * dist_r + y_r * dist_l) / sum_d_l_r

    return y_eval
