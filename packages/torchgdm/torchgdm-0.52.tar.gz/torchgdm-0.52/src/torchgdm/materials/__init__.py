# -*- coding: utf-8 -*-
"""material optical properties

.. currentmodule:: torchgdm.materials

Classes
-------

.. autosummary::
   :toctree: generated/
   :recursive:

    MatConstant
    MatDatabase
    MatTiO2
    MaterialBase


Functions
---------

.. autosummary::
   :toctree: generated/

    list_available_materials

"""
from .base_classes import MaterialBase

from .hardcoded import MatConstant
from .hardcoded import MatTiO2

from .tabulated import list_available_materials
from .tabulated import MatDatabase
