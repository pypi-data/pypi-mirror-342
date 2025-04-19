# -*- coding: utf-8 -*-
"""2D surface discretizations

.. currentmodule:: torchgdm.struct.struct2d

Classes
-------

.. autosummary::
   :toctree: generated/

   StructDiscretized2D
   StructDiscretizedSquare2D
   StructGPM2D
   StructMieCylinderGPM2D
   StructTMatrixGPM2D


dipolar approximation
^^^^^^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: generated/
   
   StructEffPola2D
   StructMieCylinderEffPola2D
   

Functions
---------

.. autosummary::
   :toctree: generated/
   
   extract_gpm_from_struct
   extract_gpm_from_tmatrix
   extract_gpm_from_fields
   extract_eff_pola_2d
   get_gpm_positions_by_clustering


Geometries
----------

.. autosummary::
   :toctree: generated/

   square
   rectangle
   circle
   split_ring
   triangle_equilateral


Discretizer functions
---------------------

.. autosummary::
   :toctree: generated/

   discretizer_square

"""
from . import surface
from . import line
from . import gpm2d
from . import geometries

from .surface import StructDiscretized2D
from .surface import StructDiscretizedSquare2D
from .gpm2d import StructGPM2D
from .gpm2d import StructMieCylinderGPM2D
from .gpm2d import StructTMatrixGPM2D
from .line import StructEffPola2D
from .line import StructMieCylinderEffPola2D

from torchgdm.struct.eff_model_tools import extract_gpm_from_struct
from torchgdm.struct.eff_model_tools import extract_gpm_from_tmatrix
from torchgdm.struct.eff_model_tools import extract_gpm_from_fields
from torchgdm.struct.eff_model_tools import get_gpm_positions_by_clustering
from torchgdm.struct.eff_model_tools import extract_eff_pola_2d

from .geometries import discretizer_square

from .geometries import square
from .geometries import rectangle
from .geometries import circle
from .geometries import split_ring
from .geometries import triangle_equilateral
