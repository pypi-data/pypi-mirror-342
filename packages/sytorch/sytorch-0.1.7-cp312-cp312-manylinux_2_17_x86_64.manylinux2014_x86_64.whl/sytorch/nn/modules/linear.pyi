import sytorch as st
import torch
from ..functional.linear import linear as linear
from .module import SymbolicModule as SymbolicModule
from _typeshed import Incomplete
from typing import TypeAlias, TypeVar

ST = TypeVar('ST', bound=st.stype)
VT = TypeVar('VT', bound=st.vtype)
REAL: Incomplete
FT = TypeVar('FT', bound=st.StorageFormat)
ET = TypeVar('ET', bound=st.EncodingScheme)
APRNN: TypeAlias
PREPARED: TypeAlias
ConstantTensor: Incomplete

class SymbolicLinear(SymbolicModule[torch.nn.Linear, ST], torch.nn.Linear):
    def forward(self, input): ...
