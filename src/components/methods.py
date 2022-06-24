from rich.panel import Panel
from textual.widget import Widget
from textual.widgets import Button
from rich.text import Text
from rich.table import Table
from rich.console import RenderableType
from rich.align import Align


class MethodOptions(Widget):
    def __init__(self, title: str):
        super().__init__(title)

        self.title = title
        self.name = title
        self.methods = ["GET", "POST", "UPDATE", "DELETE"]

    def on_click(self) -> None:
        print("clicked")

    def render(self) -> RenderableType:
        grid = Table(width=60)
        # grid.add_column(Button("Methods", style="white on black"))
        for method in self.methods:
            grid.add_column(
                Button(f"{method}", style="white on green"),
                width=50,
            )
        return Panel(
            grid,
            title=self.title,
        )
