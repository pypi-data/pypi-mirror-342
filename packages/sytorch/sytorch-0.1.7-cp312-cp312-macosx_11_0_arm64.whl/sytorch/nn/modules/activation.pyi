import sytorch as st
import torch
from ..functional.activation import relu as relu
from .module import SymbolicModule as SymbolicModule
from _typeshed import Incomplete
from sytorch.utils._dispatch import Dispatched as Dispatched, dispatch as dispatch, implement_for as implement_for
from typing import TypeAlias, TypeVar, overload

ST = TypeVar('ST', bound=st.stype)
VT = TypeVar('VT', bound=st.vtype)
REAL: Incomplete
FT = TypeVar('FT', bound=st.StorageFormat)
ET = TypeVar('ET', bound=st.EncodingScheme)
APRNN: TypeAlias
PREPARED: TypeAlias
ConstantTensor: Incomplete

class SymbolicReLU(SymbolicModule[torch.nn.ReLU, ST], torch.nn.ReLU):
    @overload
    def __call__(self, x: torch.Tensor) -> torch.Tensor: ...
    @overload
    def __call__(self, x: st.SymbolicTensor[ST, REAL, FT, ET]) -> st.SymbolicTensor[ST, REAL, FT, ET]: ...
    @overload
    def __call__(self, x: st.Point[st.SymbolicTensor[ST, REAL, FT, ET], APRNN]) -> st.Point[st.SymbolicTensor[ST, REAL, FT, ET], APRNN]: ...
    @overload
    def __call__(self, x: st.Box[st.SymbolicTensor[ST, REAL, FT, ET], PREPARED]) -> st.Box[st.SymbolicTensor[ST, REAL, FT, ET], PREPARED]: ...
    def forward(self, x): ...
