# SPDX-FileCopyrightText: 2024 Tjark Sievers
# SPDX-FileCopyrightText: 2025 Tjark Sievers
#
# SPDX-License-Identifier: MIT

"""
Geometry
========

.. currentmodule:: quant_met.geometry

Functions
---------

.. autosummary::
   :toctree: generated/

    generate_bz_path

Classes
-------

.. autosummary::
   :toctree: generated/

   BaseLattice
   GrapheneLattice
   SquareLattice
"""  # noqa: D205, D400

from .base_lattice import BaseLattice
from .bz_path import generate_bz_path
from .graphene import GrapheneLattice
from .square import SquareLattice

__all__ = ["BaseLattice", "GrapheneLattice", "SquareLattice", "generate_bz_path"]
