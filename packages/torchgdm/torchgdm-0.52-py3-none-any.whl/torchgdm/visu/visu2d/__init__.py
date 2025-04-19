# -*- coding: utf-8 -*-
"""2D visualization tools based on matplotlib

Requires `matplotlib`. Install with:

.. code-block:: bash

     pip install matplotlib


Contains following plotting tools:

    
.. autosummary::
   :toctree: generated/
    
    structure
    contour
    scalarfield
    field_intensity
    field_amplitude
    vectorfield
    vectorfield_inside
    streamlines_energy_flux

"""
from . import geo2d, vec2d, scalar2d

from .geo2d import _reset_color_iterator

from .geo2d import structure, contour
from .scalar2d import _scalarfield as scalarfield
from .scalar2d import field_intensity, field_amplitude
from .vec2d import vectorfield, vectorfield_inside, streamlines_energy_flux
