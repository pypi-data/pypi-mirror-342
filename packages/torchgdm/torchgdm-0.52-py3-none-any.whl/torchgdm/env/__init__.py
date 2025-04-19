# encoding=utf-8
"""environments classes and illumination fields


An environment class implements:
  
    - Green's tensors, describing environments and their boundary conditions.  
    - illumination fields specific for the environment


.. currentmodule:: torchgdm.env


Environment classes
-------------------

.. autosummary::
   :toctree: generated/

   EnvHomogeneous2D
   EnvHomogeneous3D
   EnvironmentBase


Illumination classes
--------------------

A generic dipole illuminationas well as the illumination base class are defined here.

.. autosummary::
   :toctree: generated/
   
   IlluminationDipole
   IlluminationfieldBase


The illumination classes are defined in the subpackage of each environment.

.. autosummary::
   :toctree: generated/

   freespace_2d
   freespace_3d
  
"""
from .base_classes import IlluminationfieldBase, EnvironmentBase
from .base_classes import IlluminationDipole

from . import freespace_2d
from . import freespace_3d

from .freespace_2d import EnvHomogeneous2D
from .freespace_3d import EnvHomogeneous3D
