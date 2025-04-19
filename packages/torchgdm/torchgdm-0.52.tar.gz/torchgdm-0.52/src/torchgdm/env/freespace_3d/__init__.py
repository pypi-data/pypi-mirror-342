# encoding=utf-8
"""3D homogeneous environment and illuminations

Classes
-------

along with the main environment definition, compatible illuminations are defined:

.. currentmodule:: torchgdm.env.freespace_3d

Environment classes
^^^^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: generated/

   EnvHomogeneous3D

Illumination classes
^^^^^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: generated/
   
   NullField
   PlaneWave
   GaussianParaxial
   ElectricDipole
   MagneticDipole

"""
from . import inc_fields

from .dyads import EnvHomogeneous3D

from .inc_fields import NullField
from .inc_fields import PlaneWave
from .inc_fields import GaussianParaxial
from .inc_fields import ElectricDipole
from .inc_fields import MagneticDipole