from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static, Input

class RequestHeader(Static):
    def compose(self) -> ComposeResult:
        """Create child widgets of headers"""
        yield Container(
            Input(placeholder="key", id="key"),
            Input(placeholder="value", id="value"),
            id="header",
        )
