import rich.spinner
from _typeshed import Incomplete
from rich.console import Console as Console, ConsoleOptions as ConsoleOptions, RenderResult as RenderResult, RenderableType as RenderableType
from rich.measure import Measurement as Measurement
from rich.style import StyleType as StyleType
from rich.text import Text

class Spinner(rich.spinner.Spinner):
    text: RenderableType | Text
    name: Incomplete
    frames: Incomplete
    interval: Incomplete
    start_time: float | None
    style: Incomplete
    speed: Incomplete
    frame_no_offset: float
    def __init__(self, name: str, text: RenderableType = '', *, style: StyleType | None = None, speed: float = 1.0) -> None: ...
    def render(self, time: float) -> RenderableType: ...
