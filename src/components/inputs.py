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
from .methods import MethodOptions


class InputURL(Widget):

    url: Reactive[RenderableType] = Reactive("")
    body: Reactive[RenderableType] = Reactive("")
    resp: Reactive[RenderableType] = Reactive("")

    def __init__(self, title: str):
        super().__init__(title)

        self.title = title
        self.name = title
        self.resp = ""
        self.body = ""

    def text(self) -> str:
        return self.url

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
        elif event.key == "ctrl+u":
            self.url += event.key
        elif event.key == "ctrl+p":
            self.body = pyperclip.paste()

    def render(self) -> RenderableType:

        method_option = Table()
        method_option.add_column("URL", no_wrap=True)
        method_option.add_column("Payload", no_wrap=True)
        method_option.add_column("Response", no_wrap=True)
        methods = [
            [f"URL: {self.url}\n", self.body, self.resp],
        ]
        for method in methods:
            method_option.add_row(*method)
            if method == methods[0]:
                method_option.add_row(MethodOptions(""))

        return Panel(
            method_option,
            title=self.title,
        )
