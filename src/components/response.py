import pyperclip
import requests
from textual import events
from rich.panel import Panel
from textual.widget import Widget
from rich.text import Text
from rich.table import Table
from rich.box import HEAVY
from textual.reactive import Reactive
from rich.console import RenderableType
from rich.align import Align


class ResponseField(Widget):

    response: Reactive[RenderableType] = Reactive("")

    def __init__(self, title: str, resp):
        super().__init__(title)

        self.title = title
        self.name = title
        self.resp = resp

    def on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            resp = requests.get(self.url, json={"query": self.body})
            print(resp.json())
            self.resp = resp.text

        elif event.key == "ctrl+h":
            self.url = self.url[:-1]
        elif event.key == "ctrl+v":
            self.url = pyperclip.paste()
        elif event.key == "ctrl+x":
            self.url = ""

    def text(self) -> str:
        return self.resp.text

    def render(self) -> RenderableType:
        response_body = Align.right(Text(self.resp))
        grid = Table(expand=True)
        grid.add_column("Response ", justify="center")
        grid.add_row(
            self.resp,
        )

        return Panel(
            grid,
            title=f"{self.title}",
            box=HEAVY,
        )
