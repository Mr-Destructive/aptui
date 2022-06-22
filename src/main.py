import sys
import requests
from textual.app import App
from textual.widget import Widget
from textual.widgets import Placeholder, Button, Header, Footer
from textual.reactive import Reactive
from textual_inputs import TextInput, IntegerInput
from rich.text import Text
from textual import events
from rich.console import RenderableType
from rich.align import Align
from rich.box import DOUBLE
from rich.panel import Panel
from rich.style import Style
from textual import events
from components import inputs, methods, response


class MainApp(App):
    async def on_load(self) -> None:
        await self.bind("q", "quit", "Quit")

    async def on_mount(self) -> None:
        header = Header(tall=False, style="white on dark_orange")
        footer = Footer()
        await self.view.dock(
            header,
            inputs.InputURL("URL"),
            response.ResponseField(
                "Response Body",
            ),
            Placeholder(name="APTUI"),
            footer,
            edge="top",
        )
        # await self.view.dock(
        #    edge="left",
        # )


MainApp.run(title="APTUI")
