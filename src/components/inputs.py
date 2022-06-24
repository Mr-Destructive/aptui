import pyperclip
import requests
from textual import events
from rich.panel import Panel
from textual.widget import Widget
from rich.text import Text
from rich.box import DOUBLE, HEAVY
from rich.table import Table
from textual.reactive import Reactive
from rich.console import RenderableType
from rich.align import Align
from .response import ResponseField
from .methods import MethodOptions


class Payload(Widget):

    body: Reactive[RenderableType] = Reactive("")

    def __init__(self, title: str, body):
        super().__init__(title)

        self.title = title
        self.name = title
        self.body = body

    def text(self) -> str:
        return self.body

    def on_key(self, event: events.Key) -> None:

        if event.key == "ctrl+h":
            self.body = self.body[:-1]
        elif event.key == "ctrl+v":
            self.body = pyperclip.paste()
        elif event.key == "ctrl+x":
            self.body = ""
        elif event.key == "ctrl+u":
            self.url += event.key
        elif event.key == "ctrl+p":
            self.body = pyperclip.paste()
        else:
            self.body += event.key

    def render(self) -> RenderableType:
        payload_body = Text()
        return Panel(
            payload_body,
            title=self.title,
        )


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
        self.headers = ""

    def text(self) -> str:
        return self.url

    def on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            resp = requests.get(self.url, json={"query": self.body})
            self.resp = resp.text
        if event.key == "ctrl+o":
            resp = requests.post(self.url, data=self.body, headers=self.headers)
            self.resp = resp.text
        if event.key == "ctrl+u":
            resp = requests.put(self.url, data=self.body, headers=self.headers)
            self.resp = resp.text
        if event.key == "ctrl+d":
            resp = requests.delete(self.url, data=self.body, headers=self.headers)
            if resp.status_code == 204:
                self.resp = "DELETED SUCCESSFULLY"
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
        elif event.key == "ctrl+a":
            self.headers = pyperclip.paste()
        else:
            self.url += event.key

    def render(self) -> RenderableType:

        method_option = Table(
            box=DOUBLE,
        )
        method_option.add_column(
            "URL",
        )
        # method_option.add_column("Payload", no_wrap=True)
        method_option.add_column("Payload", no_wrap=True)
        method_option.add_column("Headers", no_wrap=True)
        methods = [
            [f"URL: {self.url}\n", self.body, self.headers],  # self.resp],
        ]
        for method in methods:
            method_option.add_row(*method)
            if method == methods[0]:
                method_option.add_row(MethodOptions(""))

        # method_option.add_row("Response")  # no_wrap=True)
        method_option.add_row(ResponseField("", resp=self.resp))
        return Panel(
            method_option,
            title=self.title,
        )
