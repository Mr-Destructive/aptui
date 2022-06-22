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
from .response import ResponseField


class InputURL(Widget):

    url: Reactive[RenderableType] = Reactive("")
    resp: Reactive[RenderableType] = Reactive("")

    def __init__(self, title: str):
        super().__init__(title)

        self.title = title
        self.name = title
        self.resp = ""

    def text(self) -> str:
        return self.url

    def on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            resp = requests.get(self.url)
            self.resp = resp.text

        elif event.key == "ctrl+h":
            self.url = self.url[:-1]
        elif event.key == "ctrl+v":
            self.url = pyperclip.paste()
        elif event.key == "ctrl+x":
            self.url = ""
        else:
            self.url += event.key

    def render(self) -> RenderableType:
        input_url = Align.left(Text(self.url))
        response_body = Align.right(Text(self.url))
        grid = Table.grid(expand=True)
        grid.add_row(f"URL: {self.url}")
        grid.add_row("\nResponse : ")
        grid.add_row(f"{self.resp}")

        return Panel(
            grid,
            title=self.title,
        )
