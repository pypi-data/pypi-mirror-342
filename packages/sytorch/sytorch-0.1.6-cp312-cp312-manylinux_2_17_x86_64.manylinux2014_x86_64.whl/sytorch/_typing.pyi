from sytorch import SymbolicTensor as SymbolicTensor
from typing import Protocol, TypeAlias

Shape: TypeAlias

class SupportsShape(Protocol):
    @property
    def shape(self) -> Shape: ...
