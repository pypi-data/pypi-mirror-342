import sytorch as st
import torch
from .module import SymbolicModule as SymbolicModule
from _typeshed import Incomplete
from sytorch.utils._dispatch import Dispatched as Dispatched, dispatch as dispatch, implement_for as implement_for
from typing import TypeAlias, TypeVar

ST = TypeVar('ST', bound=st.stype)
VT = TypeVar('VT', bound=st.vtype)
REAL: Incomplete
FT = TypeVar('FT', bound=st.StorageFormat)
ET = TypeVar('ET', bound=st.EncodingScheme)
APRNN: TypeAlias
PREPARED: TypeAlias
ConstantTensor: Incomplete

class SymbolicSequential(SymbolicModule[torch.nn.Sequential, ST], torch.nn.Sequential): ...
