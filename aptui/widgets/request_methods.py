from textual.app import ComposeResult
from textual.widgets import Static, Button

class RequestMethods(Static):
    def compose(self) -> ComposeResult:
        """Create child widgets of a request methods."""
        yield Button("GET", id="get")
        yield Button("POST", id="post")
        yield Button("PUT", id="put")
        yield Button("PATCH", id="patch")
        yield Button("DELETE", id="delete")

    def on_mount(self) -> None:
        self.styles.height = "auto"
