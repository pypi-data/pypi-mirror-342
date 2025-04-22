import sytorch as st
import torch
from typing import TypeVar, overload

__all__ = ['relu']

ST = TypeVar('ST', bound=st.stype)
VT = TypeVar('VT', bound=st.vtype)
FT = TypeVar('FT', bound=st.StorageFormat)
ET = TypeVar('ET', bound=st.EncodingScheme)

@overload
def relu(x: torch.Tensor) -> torch.Tensor: ...
@overload
def relu(x: st.SymbolicTensor[ST, REAL, FT, ET]) -> st.SymbolicTensor[ST, REAL, FT, ET]: ...
@overload
def relu(x: st.Point[st.SymbolicTensor[ST, REAL, FT, ET], APRNN]) -> st.Point[st.SymbolicTensor[ST, REAL, FT, ET], APRNN]: ...
@overload
def relu(x: st.Box[st.SymbolicTensor[ST, REAL, FT, ET], PREPARED]) -> st.Box[st.SymbolicTensor[ST, REAL, FT, ET], PREPARED]: ...
