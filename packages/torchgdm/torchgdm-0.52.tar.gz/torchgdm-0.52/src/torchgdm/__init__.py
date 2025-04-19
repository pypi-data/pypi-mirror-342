# encoding=utf-8
#
# Copyright (C) 2023-2025, P. R. Wiecha
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
TorchGDM - nano-optics + auto-diff

A full-field electrodynamical Green's Dyadic Method solver with 
support for effective E/M polarizabilities, written in pytorch. 




Core classes
============

Two classes provide high-level access to the core functionalities:

.. currentmodule:: torchgdm

.. autosummary::
   :recursive:
   :toctree: generated/

   Simulation
   Field
   

Simulation description
======================

The simulation takes a list of structures, the environment and a list 
of illumination fields as main inputs. 
The respective classes are found in following sub packages:

Structures
----------

The sub-packages :mod:`struct3d.volume` and :mod:`struct2d.surface` 
contain also discretizations for a selection of geometric primitives.

.. autosummary::
   :toctree: generated/

   struct2d
   struct3d


Materials
----------

.. autosummary::
   :toctree: generated/

   materials


Environments and illuminations
------------------------------

.. autosummary::
   :toctree: generated/

   env.freespace_2d
   env.freespace_3d

*Note:* Illumination fields are associated with each environment. 
They can be found in the respective base environment package
(:mod:`env.freespace_2d` and :mod:`env.freespace_3d`).


Postprocessing and Tools
========================

Most postprocessing and visualization tools are accessible also through 
the :class:`Simulation` and :class:`Field` classes. 
Alternatively the functional API can be used:

Post processing
---------------

.. autosummary::
   :toctree: generated/

   postproc
   postproc.crosssect
   postproc.fields
   postproc.multipole
   postproc.green


Visualization
-------------

.. autosummary::
   :toctree: generated/
   :recursive:

   visu.visu2d
   visu.visu3d


Tools
-----

For detailed documentation, see:

.. autosummary::
   :toctree: generated/

    tools


Many tools are used mainly internally. The most relevant tool modules are:

.. autosummary::
   :toctree: generated/
    
    tools.geometry
    tools.mie


CUDA GPU acceleration
=====================

TorchGDM exposes a few top level helper functions for CUDA usage:

.. autosummary::
   :toctree: generated/

    to_np
    use_cuda
    set_default_device
    get_default_device


"""

__name__ = "torchgdm"
__version__ = "0.52"
__date__ = "04/18/2025"  # MM/DD/YYY
__license__ = "GPL3"
__status__ = "beta"

__copyright__ = "Copyright 2023-2025, Peter R. Wiecha"
__author__ = "Peter R. Wiecha"
__maintainer__ = "Peter R. Wiecha"
__email__ = "pwiecha@laas.fr"
__credits__ = [
    "Christian Girard",
    "Arnaud Arbouet",
    "Clément Majorel",
    "Sofia Ponomareva",
    "Adelin Patoux",
    "Antoine Azéma",
    "Renaud Marty",
]

# --- populate namespace
from .constants import DEFAULT_DEVICE

device = DEFAULT_DEVICE

# make some functions and classes available at top level
from .simulation import Simulation
from .field import Field
from .tools.misc import to_np, tqdm
from .tools.misc import use_cuda, get_default_device, set_default_device

# make some submodules available at top level
from .visu import visu2d
from .visu import visu3d

# modules
from . import constants
from . import linearsystem
from . import simulation
from . import field

# sub packages
from . import env
from . import materials
from .struct import struct2d
from .struct import struct3d
from . import struct
from . import postproc
from . import tools
