import pyperclip
import requests
from textual import events
from rich.panel import Panel
from textual.widget import Widget
from rich.text import Text
from rich.table import Table
from textual.reactive import Reactive
from rich.console import RenderableType
from rich.align import Align


class ResponseField(Widget):

    response: Reactive[RenderableType] = Reactive("")

    def __init__(self, title: str):
        super().__init__(title)

        self.title = title
        self.name = title
        self.resp = ""

    def text(self) -> str:
        return self.resp.text

    def render(self) -> RenderableType:
        response_body = Align.right(Text(self.resp))
        grid = Table(expand=True)
        grid.add_column("Response ", justify="center")

        return Panel(
            grid,
            title=f"{self.title}",
        )
