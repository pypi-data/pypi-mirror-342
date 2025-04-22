import sytorch as st
import torch
import torch.nn as nn
from ..._typing import Any as Any, Callable as Callable, Dict as Dict, Generator as Generator, Generic as Generic, Iterable as Iterable, Literal as Literal, Optional as Optional, Protocol as Protocol, Self as Self, Tuple as Tuple, TypeVar as TypeVar, Union as Union, cast as cast, overload as overload
from ...utils import logger as logger
from .._symbolic_mode import is_symbolic_enabled as is_symbolic_enabled, no_symbolic as no_symbolic
from ..parameter import EditableParameter as EditableParameter, SymbolicParameter as SymbolicParameter
from _typeshed import Incomplete
from sytorch import Solver as Solver, SymbolicTensor as SymbolicTensor
from sytorch._tensor import AnyConstant as AnyConstant

ST = TypeVar('ST', bound=st.stype)
ST2 = TypeVar('ST2', bound=st.stype)
GUROBI: Incomplete
ModuleT = TypeVar('ModuleT', bound=torch.nn.Module)
ModuleT2 = TypeVar('ModuleT2', bound=torch.nn.Module)
T = TypeVar('T')
TorchModuleT = TypeVar('T', bound=torch.nn.Module)

def to_editable(model: TorchModuleT, solver: Optional[ST] = None) -> SymbolicModule[TorchModuleT, ST]: ...

class SymbolicModule(nn.Module, Generic[ModuleT, ST]):
    @property
    def solver(self) -> st.Solver[ST]: ...
    @property
    def orig(self) -> ModuleT: ...
    def requires_edit_(self, requires_edit: bool = True, *, mask: Optional[torch.Tensor | st.utils.MaskSpec] = None, lb: Optional[AnyConstant] = None, ub: Optional[AnyConstant] = None): ...
    def copy(self, recursive: bool = False, copy_attr: bool = False) -> Self: ...
    def optimize(self, *args, **kwargs) -> Self | None: ...
    def update_(self) -> None: ...
    def param_delta(self): ...
