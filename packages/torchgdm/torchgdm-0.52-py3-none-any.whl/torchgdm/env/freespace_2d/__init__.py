# encoding=utf-8
"""2D homogeneous environment and illuminations

Classes
-------

along with the main environment definition, compatible illuminations are defined:

.. currentmodule:: torchgdm.env.freespace_2d

Environment classes
^^^^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: generated/

   EnvHomogeneous2D
   

Illumination classes
^^^^^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: generated/
   
   NullField
   PlaneWave
   ElectricLineDipole
   MagneticLineDipole

"""
from . import inc_fields

from .dyads import EnvHomogeneous2D

from .inc_fields import NullField
from .inc_fields import PlaneWave
from .inc_fields import ElectricLineDipole
from .inc_fields import MagneticLineDipole