# -*- coding: utf-8 -*-
"""3D visualization tools based on pyvista

Requires `pyvista`. For interactive use in jupyter, requires additionally: `trame`, `trame-vtk`, `trame-vuetify`, `ipywidgets`. Install with:

.. code-block:: bash

     pip install 'jupyterlab>=3' ipywidgets 'pyvista[all,trame]'
 

*Note:* 3D visualizations of simulations or fields can be readily accessed through the :class:`torchgdm.Simulation` and :class:`torchgdm.Field` classes.


.. autosummary::
   :toctree: generated/
    
    structure
    vectorfield
    vectorfield_inside

"""
from . import geo3d
from . import vec3d

from .geo3d import structure
from .vec3d import vectorfield, vectorfield_inside
