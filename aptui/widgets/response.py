from textual.app import App, ComposeResult
from textual.widgets import Static


class Response(Static):
    """A widget to display Response"""

    def compose(self) -> ComposeResult:
        """Create child widgets of response"""
        yield Static("Response", id="response_text")
        yield Static("Status Code", id="status_code")

    def on_mount(self) -> None:
        self.scroll_visible()
        self.styles.height = "auto"
