# -*- coding: utf-8 -*-
"""3D volume discretizations

.. currentmodule:: torchgdm.struct.struct3d

Classes
-------

.. autosummary::
   :toctree: generated/
   
   StructDiscretized3D
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


Functions
---------

.. autosummary::
   :toctree: generated/
   
   extract_gpm_from_struct
   extract_gpm_from_tmatrix
   extract_gpm_from_fields
   extract_eff_pola_via_exact_mp_3d
   get_gpm_positions_by_clustering


Geometries
----------

.. autosummary::
   :toctree: generated/
   
   cube
   cuboid
   sphere
   spheroid
   disc
   ellipse
   split_ring
   lshape
   prism_trigonal
   from_image


Discretizer functions
---------------------

.. autosummary::
   :toctree: generated/
   
   discretizer_cubic
   discretizer_hexagonalcompact


"""
from . import volume
from . import point
from . import gpm3d
from . import geometries

from .volume import StructDiscretizedCubic3D
from .volume import StructDiscretizedHexagonal3D
from .volume import StructDiscretized3D
from .point import StructEffPola3D
from .point import StructMieSphereEffPola3D
from .gpm3d import StructGPM3D
from .gpm3d import StructMieSphereGPM3D
from .gpm3d import StructTMatrixGPM3D

from torchgdm.struct.eff_model_tools import extract_gpm_from_struct
from torchgdm.struct.eff_model_tools import extract_gpm_from_tmatrix
from torchgdm.struct.eff_model_tools import extract_gpm_from_fields
from torchgdm.struct.eff_model_tools import get_gpm_positions_by_clustering
from torchgdm.struct.eff_model_tools import extract_eff_pola_via_exact_mp_3d

from .geometries import discretizer_cubic
from .geometries import discretizer_hexagonalcompact

from .geometries import cube
from .geometries import cuboid
from .geometries import sphere
from .geometries import spheroid
from .geometries import disc
from .geometries import ellipse
from .geometries import split_ring
from .geometries import lshape
from .geometries import prism_trigonal

from .geometries import from_image
