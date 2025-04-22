import rich.status
from _typeshed import Incomplete
from rich.console import Console as Console, RenderableType as RenderableType
from rich.jupyter import JupyterMixin as JupyterMixin
from rich.style import StyleType as StyleType
from types import TracebackType as TracebackType

class Status(rich.status.Status):
    status: Incomplete
    spinner_style: Incomplete
    speed: Incomplete
    log_level: Incomplete
    def __init__(self, status: RenderableType, *, console: Console | None = None, spinner: str = 'dots', spinner_style: StyleType = 'status.spinner', speed: float = 1.0, refresh_per_second: float = 12.5, log_level=...) -> None: ...
    def stop(self) -> None: ...
