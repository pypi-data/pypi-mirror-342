import sytorch as st
import torch
from .._tensor import AnyConstant, AsIs, BooleanTensor, Delta, Dense, EncodingScheme, Solver, Sparse, StorageFormat, SymbolicTensor
from .._typing import Literal, Optional, Tuple, TypeVar, overload
from sytorch.utils.array import MaskSpec
from typing import Generic

__all__ = ['SymbolicParameter']

L = Literal
ST = TypeVar('ST', bound=st.stype)
ST2 = TypeVar('ST2', bound=st.stype)
VT = TypeVar('VT', bound=st.vtype)
FormatT = TypeVar('FormatT', bound=StorageFormat, default=Dense)
ET = TypeVar('ET', bound=EncodingScheme)
RealT = TypeVar('RealT', bound=Real, default=Real)
SparseT = TypeVar('SparseT', bound=Sparse, default=Sparse)
DeltaT = TypeVar('DeltaT', bound=Delta, default=Delta)

class EditableParameter(torch.nn.Parameter, Generic[ST]):
    @property
    def __type_args__(self) -> Tuple[type[ST]]: ...
    @property
    def requires_edit(self) -> bool: ...
    @property
    def solver(self) -> Solver[ST]: ...
    @property
    def symbolic_data(self): ...
    def __new__(cls, param: torch.nn.Parameter, *, solver: Solver[ST]) -> EditableParameter: ...
    def requires_edit_(self, requires_edit: bool = True, *, mask: Optional[BooleanTensor | MaskSpec] = None, lb: Optional[AnyConstant] = None, ub: Optional[AnyConstant] = None) -> EditableParameter[ST]: ...
    def update_(self) -> None: ...

class SymbolicParameter(SymbolicTensor[ST, RealT, FormatT, DeltaT]):
    @overload
    def __init__(self, data: SymbolicTensor[ST, VT, Dense, AsIs], /, *, base: torch.Tensor, encoding: type[Delta] = ...) -> None: ...
    @overload
    def __init__(self, data: SymbolicTensor[ST, VT, Dense, AsIs], /, *, base: torch.Tensor, mask: BooleanTensor, encoding: type[Delta] = ...) -> None: ...
    def update_(self): ...
