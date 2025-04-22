import torch
from .._dispatch import DispatchKey as DispatchKey, DispatchResolver as DispatchResolver, Dispatcher as Dispatcher
from _typeshed import Incomplete
from torch.func import functional_call as functional_call, jacfwd as jacfwd, jacrev as jacrev, vmap as vmap
from typing import Callable

dispatcher: Incomplete

def batched_jacobian_iter(func: Callable, inputs: torch.Tensor[*N, I], batch_dims: int = 1, create_graph: bool = False, strict: bool = False, vectorize: bool = True, strategy: str = 'reverse-mode', device_compute: Incomplete | None = None, device_standby: Incomplete | None = None, dtype_compute: Incomplete | None = None, dtype_standby: Incomplete | None = None, expand: bool = True) -> torch.Tensor[*N, O, *N, I]: ...
