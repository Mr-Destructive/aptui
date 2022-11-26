import json
from typing import List
import pyperclip
import requests
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.reactive import var
from textual.widgets import Button, Header, Footer, Input, Static


class Response(Static):
    """A widget to display Response"""
    def compose(self) -> ComposeResult:
        """Create child widgets of response"""
        yield Static(id="response_text")
        yield Static(id="status_code")

    def on_mount(self) -> None:
        self.styles.height = "auto"

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
        yield Button("PUT", id="put")
        yield Button("PATCH", id="patch")
        yield Button("DELETE", id="delete")

    def on_mount(self) -> None:
        self.styles.height = "auto"


class RequestContainer(Static):
    """A APTUI widget."""

    method_choide = "GET"

    def catch_response(self, resp: requests.Response) -> dict:
        try:
            return {"status_code": str(resp.status_code), "response": resp.text}
        except json.JSONDecodeError as e:
            return {"status_code": str(resp.status_code), "response": "ERRO"}

    def get_request(self, url: str) -> dict:
        resp = requests.get(url)
        if resp.status_code not in range(200, 227):
            return self.catch_response(resp)
        return {"status_code": str(resp.status_code), "response": resp.content.decode("ascii")}

    def get_headers(self) -> dict:
        headers = self.query(".headers")
        for header in headers:
            kv_pair = header

        return {}

    def post_request(self, url: str, body: dict, headers: dict) -> dict:
        # resp = requests.post(url, data=body, headers=headers)
        resp = requests.request("POST", url, headers=headers, json=body)
        if resp.status_code not in range(200, 227):
            return self.catch_response(resp)
        return {"status_code": str(resp.status_code), "response": resp.content.decode("ascii")}

    def delete_request(self, url: str) -> dict:
        resp = requests.request("DELETE", url)
        if resp.status_code not in range(200, 227):
            return self.catch_response(resp)
        return {"status_code": str(resp.status_code), "response": resp.content.decode("ascii")}

    def on_input_submitted(self, message: Input.Submitted) -> None:
        url = message.value
        resp = self.get_request(url)
        self.query_one("#response_text", Static).update(resp["response"])
        self.query_one("#status_code", Static).update(resp["status_code"])

    def put_request(self, url: str, body: dict, headers: dict) -> dict:
        # resp = requests.post(url, data=body, headers=headers)
        resp = requests.request("PUT", url, headers=headers, json=body)
        if resp.status_code not in range(200, 227):
            return self.catch_response(resp)
        return {"status_code": str(resp.status_code), "response": resp.content.decode("ascii")}

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        button_id = event.button.id
        if button_id == "send":
            url = self.query(Input).first().value
            if self.method_choide == "POST":
                body = json.loads(self.query_one("#body_inp").value) or {}
                # headers = self.query(".header").first().value or {}
                resp = self.post_request(
                    url, body=body, headers={}
                )  # , headers=headers)
                self.query_one("#response_text", Static).update(resp["response"])
                self.query_one("#status_code", Static).update(resp["status_code"])
            elif self.method_choide == "DELETE":
                resp = self.delete_request(url=url)
                self.query_one("#response_text", Static).update(resp["response"])
                self.query_one("#status_code", Static).update(resp["status_code"])
            elif self.method_choide == "PUT":
                body = json.loads(self.query_one("#body_inp").value) or {}
                resp = self.put_request(url=url, body=body, headers={})
                self.query_one("#response_text", Static).update(resp["response"])
                self.query_one("#status_code", Static).update(resp["status_code"])
            else:
                url = self.query(Input).first().value
                resp = self.get_request(url)
                self.query_one("#response_text", Static).update(resp["response"])

        elif button_id == "post":
            self.method_choide = "POST"
        elif button_id == "get":
            self.method_choide = "GET"
        elif button_id == "delete":
            self.method_choide = "DELETE"
        elif button_id == "put":
            self.method_choide = "PUT"

        elif button_id == "import":
            curl = pyperclip.paste()
            resp = self.get_request(curl)
            self.query_one("#response", Static).update(resp)

        elif button_id == "add_req":
            headers = RequestHeader(id="headers")
            self.query_one("#reqheaders").mount(headers)
            headers.scroll_visible()

    def compose(self) -> ComposeResult:
        """Create child widgets of a API Request."""
        yield Input(placeholder="URL", id="url")
        yield Button("Send", id="send", variant="success")
        yield Button("Import", id="import", variant="error")
        yield RequestMethods("Rquest Methods", id="methods", classes="body")
        yield RequestHeader()
        yield Body(expand=True, id="body")
        yield Response("Response", expand=True, id="response")

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

    def add_request_widget(
        self, req_widget: RequestContainer = RequestContainer()
    ) -> None:
        self.query_one("#aptui").mount(req_widget)
        req_widget.scroll_visible()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Called when a button is pressed."""
        button_id = event.button.id
        if button_id == "add_req":
            self.add_request_widget(RequestContainer())

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Button("Add Request", id="add_req", variant="success")
        yield Header()
        yield Footer()
        yield Container(RequestContainer(), id="aptui")

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
        self.add_request_widget(RequestContainer())


if __name__ == "__main__":
    app = APTUI()
    app.run()
