# SPDX-FileCopyrightText: 2024 Tjark Sievers
# SPDX-FileCopyrightText: 2025 Tjark Sievers
#
# SPDX-License-Identifier: MIT

"""
Parameter Classes
=================

Main class holding all the parameters for the calculation.

Classes holding the configuration for the Hamiltonians.

.. autosummary::
    :toctree: generated/parameters/hamiltonians

    hamiltonians

.. autosummary::
   :toctree: generated/parameters/
   :template: autosummary/pydantic.rst

    Parameters  # noqa
    Control  # noqa
    KPoints  # noqa
"""  # noqa: D205, D400

from .hamiltonians import (
    DressedGrapheneParameters,
    GenericParameters,
    GrapheneParameters,
    HamiltonianParameters,
    OneBandParameters,
    ThreeBandParameters,
    TwoBandParameters,
)
from .main import Control, KPoints, Parameters

__all__ = [
    "Control",
    "DressedGrapheneParameters",
    "GenericParameters",
    "GrapheneParameters",
    "HamiltonianParameters",
    "KPoints",
    "OneBandParameters",
    "Parameters",
    "ThreeBandParameters",
    "TwoBandParameters",
]
