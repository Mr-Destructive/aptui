from textual.app import App, ComposeResult
from textual.containers import Container
from textual.reactive import var
from textual.widgets import Button, Header, Footer
from aptui.widgets.request_container import RequestContainer


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
            self.add_request_widget(RequestContainer(id="request"))

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Button("Add Request", id="add_req", variant="success")
        yield Header()
        yield Footer()
        yield Container(RequestContainer(id="request"), id="aptui")

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


def main():
    app = APTUI()
    app.run()


if __name__ == "__main__":
    main()
