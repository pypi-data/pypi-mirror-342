# Copyright 2025 BDP Ecosystem Limited. All Rights Reserved.
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
# ==============================================================================

__version__ = "0.0.1"

from ._block_csr import BlockCSR
from ._block_ell import BlockELL
from ._coo import COO
from ._csr import CSR, CSC
from ._csrlb import CSR_LB, CSC_LB
from ._event import EventArray
from ._fixed_conn_num import FixedPostNumConn, FixedPreNumConn
from ._jitc_csr import JITC_CSR, JITC_CSC
from ._xla_custom_op import XLACustomKernel, defjvp
from ._xla_custom_op_numba import NumbaKernelGenerator, set_numba_environ
from ._xla_custom_op_pallas import PallasKernelGenerator
from ._xla_custom_op_warp import WarpKernelGenerator, dtype_to_warp_type

__all__ = [
    # events
    'EventArray',

    # data structures
    'COO',
    'CSR', 'CSC',
    'CSR_LB', 'CSC_LB',
    'JITC_CSR', 'JITC_CSC',
    'BlockCSR',
    'BlockELL',
    'FixedPreNumConn',
    'FixedPostNumConn',

    # kernels
    'XLACustomKernel', 'defjvp',
    'NumbaKernelGenerator', 'set_numba_environ',
    'WarpKernelGenerator',
    'PallasKernelGenerator',
    'dtype_to_warp_type',
]

# def __getattr(name):
#     """
#     Custom attribute lookup function for lazy-loading modules.
#
#     This function implements lazy loading for the 'nn' submodule. When the
#     'nn' attribute is accessed for the first time, this function dynamically
#     imports the module and returns it, avoiding unnecessary imports at startup.
#
#     Parameters
#     ----------
#     name : str
#         Name of the attribute being accessed.
#
#     Returns
#     -------
#     module
#         The requested module if it exists.
#
#     Raises
#     ------
#     AttributeError
#         If the requested attribute does not exist in the brainevent package.
#     """
#     if name == 'nn':
#         # Import the module directly from its actual location
#         # instead of from the brainevent package
#         import brainevent.nn as nn
#         return nn
#     raise AttributeError(f"brainevent has no attribute {name!r}")
#
#
# # Register the getattr function as the module's __getattr__ hook
# # This enables Python's attribute lookup mechanism to call our custom function
# # when an undefined attribute is accessed
# __getattr__ = __getattr
