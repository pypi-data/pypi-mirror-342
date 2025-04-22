# This file is part of tad-libcint.
#
# SPDX-Identifier: Apache-2.0
# Copyright (C) 2024 Grimme Group
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
PyTorch-based Libcint Interface
===============================

Implementation of a PyTorch-based interface to the *libcint* high-performance
integral library. The interface supports automatic differentiation with custom
backward functions that also call the C backend for the derivatives.

Currently, only one-electron integrals are supported.
"""
import torch

from ._version import __version__
from .api import CGTO, CINT
from .interface import LibcintWrapper, int1e

__all__ = ["CINT", "CGTO", "LibcintWrapper", "int1e", "__version__"]
