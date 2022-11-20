import json
import pyperclip
import requests
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.reactive import var
from textual.widgets import Button, Header, Footer, Input, Static


class Response(Static):
    """A widget to display Response"""


class RequestHeader(Static):
    def compose(self) -> ComposeResult:
        """Create child widgets of headers"""
        yield Container(
            Input(placeholder="key", id="key"),
            Input(placeholder="value", id="value"),
            classes="header",
        )


class Body(Static):
    def compose(self) -> ComposeResult:
        yield Input(placeholder="Body", id="body_inp")


class RequestMethods(Static):
    def compose(self) -> ComposeResult:
        """Create child widgets of a request methods."""
        yield Button("GET", id="get")
        yield Button("POST", id="post")
        yield Button("PATCH", id="patch")
        yield Button("DELETE", id="delete")

    def on_mount(self) -> None:
        self.styles.height = "auto"


class Request(Static):
    """A APTUI widget."""

    def get_response(self, url: str) -> str:
        resp = json.loads(requests.get(url).content).__str__()
        return resp

    def post_request(self, url: str, body: dict, headers: dict) -> str:
        resp = requests.post(url, data=body, headers=headers).content
        return json.loads(resp).__str__()

    def on_input_submitted(self, message: Input.Submitted) -> None:
        url = message.value
        resp = self.get_response(url)
        self.query_one("#response", Static).update(resp)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        if event.button.id == "send":
            url = self.query(Input).first().value
            resp = self.get_response(url)
            self.query_one("#response", Static).update(resp)

        elif event.button.id == "post":
            url = self.query(Input).first().value
            body = self.query_one("#body_inp").value
            #'''
            body = {"option": "test 56", "is_correct": True}
            #'''
            # headers = self.query("#headers")value
            headers = {}
            resp = self.post_request(url, body=body, headers=headers)
            self.query_one("#response", Static).update(resp)

            headers = RequestHeader(id="headers")
            self.query_one("#reqheaders").mount(headers)
            headers.scroll_visible()

        elif event.button.id == "import":
            curl = pyperclip.paste()
            resp = self.get_response(curl)
            self.query_one("#response", Static).update(resp)

    def compose(self) -> ComposeResult:
        """Create child widgets of a API Request."""
        yield Input(placeholder="URL", id="url")
        yield Button("Send", id="send", variant="success")
        yield Button("Import", id="import", variant="error")
        yield RequestMethods("Rquest Methods", id="methods", classes="body")
        yield RequestHeader()
        yield Body(id="body")
        yield Response("Response", id="response")

    def on_mount(self) -> None:
        self.styles.height = "auto"


class APTUI(App):
    """A Textual app to manage API Requests"""

    CSS_PATH = "aptui_styles.css"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit_app", "Quit"),
        ("r", "add_request", "Add"),
    ]
    content = var("0")

    def add_request_widget(self, req_widget: Request = Request()) -> None:
        self.query_one("#aptui").mount(req_widget)
        req_widget.scroll_visible()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Called when a button is pressed."""
        button_id = event.button.id
        if button_id == "add_req":
            self.add_request_widget(Request())

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Button("Add", id="add_req", variant="success")
        yield Header()
        yield Footer()
        yield Container(Request(), id="aptui")

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
