import sytorch as st
from ..parameter import SymbolicParameter
from torch import Tensor
from typing import TypeVar, overload

__all__ = ['linear']

ST = TypeVar('ST', bound=st.stype)
VT = TypeVar('VT', bound=st.vtype)
FT = TypeVar('FT', bound=st.StorageFormat)
ET = TypeVar('ET', bound=st.EncodingScheme)

@overload
def linear(input: Tensor, weight: Tensor, bias: Tensor | None = None) -> Tensor: ...
@overload
def linear(input: st.Point[st.SymbolicTensor[ST, REAL, FT, ET], APRNN] | Tensor, weight: SymbolicParameter[ST, REAL] | Tensor, bias: SymbolicParameter[ST, REAL] | Tensor | None = None) -> st.Point[st.SymbolicTensor[ST, REAL, FT, ET], APRNN]: ...
