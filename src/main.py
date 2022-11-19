import json
import pyperclip
import requests
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.reactive import var
from textual.widgets import Button, Header, Footer, Input, Static

class Response(Static):
    """A widget to display Response""" 


class Request(Static):
    """A APTUI widget."""

    def get_response(self, url: str) -> str:
        resp = json.loads(requests.get(url).content).__str__()
        return resp

    def on_input_submitted(self, message: Input.Submitted) -> None:
        url = message.value
        resp = self.get_response(url)
        self.query_one("#response", Static).update(resp)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        if event.button.id == "send":
            url = self.query_one(Input).value 
            resp = self.get_response(url)
            self.query_one("#response", Static).update(resp)
            

        elif event.button.id == "import":
            curl = pyperclip.paste()
            resp = self.get_response(curl)
            self.query_one("#response", Static).update(resp)

    def compose(self) -> ComposeResult:
        """Create child widgets of a stopwatch."""
        yield Input(placeholder="URL", id="url")
        yield Button("Send", id="send", variant="success")
        yield Button("Import", id="import", variant="error")
        yield Response("Response",id="response")


class APTUI(App):
    """A Textual app to manage API Requests"""

    CSS_PATH = "aptui_styles.css"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"),
                ("q", "quit_app", "Quit"),
                ("r", "add_request", "Add"),
                ]
    content = var("0")

    def add_request_widget(self, req_widget:Request = Request()) -> None:
        self.query_one("#aptui").mount(req_widget)
        req_widget.scroll_visible()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Called when a button is pressed."""
        button_id = event.button.id
        if button_id == "add_req":
            self.add_request_widget(Request())
        assert button_id is not None

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Button("Add", id="add_req", variant="success")
        yield Header()
        yield Footer()
        yield Container(Request(),
                        id="aptui"
                        )

    def on_mount(self) -> None:
        self.styles.height = "auto"

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_quit_app(self) -> None:
        """An action to quit the app."""
        self.exit()

    def action_add_request(self) -> None:
        """An action to add a request"""
        self.add_request_widget(Request())


if __name__ == "__main__":
    app = APTUI()
    app.run()
