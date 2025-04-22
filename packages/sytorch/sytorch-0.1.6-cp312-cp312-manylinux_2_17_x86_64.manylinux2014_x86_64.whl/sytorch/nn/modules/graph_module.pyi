import torch
import torch.fx
from .module import SymbolicModule as SymbolicModule
from _typeshed import Incomplete
from typing import Any

class SymbolicGraphModule(SymbolicModule, torch.fx.GraphModule):
    def __new__(cls, *args, **kwargs): ...
    def __getitem__(self, idx): ...
    training: Incomplete
    graph: Incomplete
    meta: dict[str, Any]
    def __init__(self, root: torch.nn.Module | dict[str, Any], graph: torch.fx.Graph, class_name: str = 'SymbolicGraphModule') -> None: ...
