# -*- coding: utf-8 -*-
"""package for torchgdm structures

Contains Classes for 3D and 2D discretized structures and point (3D) and line (2D) effective polarizability structures:

.. currentmodule:: torchgdm.struct

3D
--

.. autosummary::
   :toctree: generated/
   
   StructDiscretizedCubic3D
   StructDiscretizedHexagonal3D
   StructGPM3D
   StructMieSphereGPM3D
   StructTMatrixGPM3D


dipolar approximation
^^^^^^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: generated/
   
   StructEffPola3D
   StructMieSphereEffPola3D


3D discretization
-----------------

.. autosummary::
   :toctree: generated/
   
   struct3d


2D
--

.. autosummary::
   :toctree: generated/
   
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


2D discretization
-----------------

.. autosummary::
   :toctree: generated/
   
   struct2d

base class
----------

.. autosummary::
   :toctree: generated/
   
   StructBase

"""
# - packages / modules
from . import struct2d
from . import struct3d
from . import eff_model_tools


# - 3D
from .struct3d.volume import StructDiscretized3D
from .struct3d.volume import StructDiscretizedCubic3D
from .struct3d.volume import StructDiscretizedHexagonal3D

from .struct3d.point import StructMieSphereEffPola3D  # Mie core-shell sphere
from .struct3d.point import StructEffPola3D

from .struct3d.gpm3d import StructGPM3D
from .struct3d.gpm3d import StructMieSphereGPM3D
from .struct3d.gpm3d import StructTMatrixGPM3D

# - 2D
from .struct2d.surface import StructDiscretized2D
from .struct2d.surface import StructDiscretizedSquare2D

from .struct2d.line import StructMieCylinderEffPola2D  # Mie core-shell cylinder
from .struct2d.line import StructEffPola2D

from .struct2d.gpm2d import StructGPM2D
from .struct2d.gpm2d import StructMieCylinderGPM2D
from .struct2d.gpm2d import StructTMatrixGPM2D

# - base class
from .base_classes import StructBase
