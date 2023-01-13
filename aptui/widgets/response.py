from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static


class Response(Static):
    """A widget to display Response"""

    def compose(self) -> ComposeResult:
        """Create child widgets of response"""
        #yield Container(
        #    Static("Response", id="response_text"),
        #    Static("Status Code", id="status_code"),
        #    id="resp_container",
        #)
        yield Static("Response", id="response_text")
        yield Static("Status Code", id="status_code")

    def on_mount(self) -> None:
        self.scroll_visible()
        # self.query_one("#response_text").styles.height = "auto"
        # self.query_one("#response_text").expand = True
