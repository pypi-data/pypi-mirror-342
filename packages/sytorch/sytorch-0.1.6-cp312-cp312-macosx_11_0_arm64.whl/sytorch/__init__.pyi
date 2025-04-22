import torch
from . import attr as attr, evaluate as evaluate, fx as fx, nn, utils as utils
from ._einsum import einsum as einsum, transpose_and_broadcast as transpose_and_broadcast
from ._eps import epsilon as epsilon, get_epsilon as get_epsilon, set_epsilon as set_epsilon
from ._tensor import Box as Box, Domain as Domain, Point as Point, Solver, SymbolicTensor as SymbolicTensor, cat as cat, contract as contract, dense_delta_real_tensor as dense_delta_real_tensor, dense_real_tensor as dense_real_tensor, dense_tensor as dense_tensor, sparse_delta_real_tensor as sparse_delta_real_tensor, sparse_delta_tensor as sparse_delta_tensor, stack as stack, symbolic_tensor as symbolic_tensor
from ._types import EncodingScheme as EncodingScheme, StorageFormat as StorageFormat, domain as domain, stype, vtype as vtype
from .nn import enable_symbolic as enable_symbolic, is_symbolic_enabled as is_symbolic_enabled, no_symbolic as no_symbolic, set_symbolic_enabled as set_symbolic_enabled, within_no_symbolic_context as within_no_symbolic_context
from .utils import as_kwargs as as_kwargs, as_slice as as_slice, console as console, enable_runtime_guard as enable_runtime_guard, implement_for as implement_for, is_runtime_guard_enabled as is_runtime_guard_enabled, logger as logger, make_mask as make_mask, make_readonly as make_readonly, mask_at_dim as mask_at_dim, masked_block as masked_block, no_runtime_guard as no_runtime_guard, no_stderr as no_stderr, no_stdout as no_stdout, print as print, set_runtime_guard_enabled as set_runtime_guard_enabled, to_numpy as to_numpy
from _typeshed import Incomplete
from typing import TypeVar, overload

dist_name: Incomplete
__version__: Incomplete
ST = TypeVar('ST', bound=stype)
ModuleT = TypeVar('ModuleT', bound=torch.nn.Module)

@overload
def s(obj: torch.nn.ReLU, *, solver: Solver[ST]) -> nn.SymbolicReLU[ST]: ...
@overload
def s(obj: ModuleT, solver: Solver[ST]) -> nn.SymbolicModule[ModuleT, ST]: ...
def _(obj: torch.nn.Module, **kwargs): ...
