import curl
import json
import os
from pathlib import Path
import pyperclip
import random
import requests
import string
import uncurl
from pathlib import Path
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static, Input, Button, DirectoryTree, Label
from urllib.parse import urlparse

from widgets.response import Response
from widgets.request_headers import RequestHeader
from widgets.request_methods import RequestMethods


class Body(Static):
    def compose(self) -> ComposeResult:
        yield Input(placeholder="Body", id="body_inp")


class RequestContainer(Static):
    """A APTUI widget."""

    method_choice = "GET"
    method_list = ["GET", "POST", "PATCH", "PUT", "DELETE"]
    headers_dict = {}
    req_path = f".aptui/requests/"

    def save_request(self):
        url = self.query_one("#url").value
        body = self.query_one("#body_inp").value or {}
        headers = self.get_headers() or {}
        method = self.method_choice
        request_json = {
            "url": url,
            "method": method,
            "headers": headers,
            "body": body,
        }
        request_name = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=5)
        )
        name = f"request-{method.lower()}-{request_name}"
        Path(self.req_path).mkdir(parents=True, exist_ok=True)
        with open(f"{self.req_path}{name}.json", "w+") as f:
            json.dump(request_json, f)

    def load_request(self):
        dir_tree = DirectoryTree(self.req_path)
        self.query_one("#response_text").mount(dir_tree)
        files = os.listdir(self.req_path)
        with open(f"{self.req_path}{files[0]}", "r") as f:
            request_json = json.load(f)
        url = request_json["url"]
        method = request_json["method"]
        body = request_json["body"]
        headers = request_json["headers"]

        aptui = self.parent.query_one("#aptui")
        loaded_request = RequestContainer()
        aptui.mount(loaded_request)
        request_widget = self.parent.query("#request")
        for i in request_widget.results():
            request_widget = aptui.query("#request").last()
            request_widget.query_one("#url").value = url
            request_widget.method_choice = method

    def get_headers(self) -> dict:
        headers = self.query("#header")
        for header in headers:
            key = header.query_one("#key").value
            value = header.query_one("#value").value
            if key and value:
                self.headers_dict[key] = value
        return self.headers_dict

    def catch_response(self, resp: requests.Response) -> dict:
        try:
            return {"status_code": str(resp.status_code), "response": resp.text}
        except json.JSONDecodeError as e:
            return {"status_code": str(resp.status_code), "response": "ERROR"}

    def get_request(self, url: str) -> dict:
        urlp = urlparse(url)
        url_valid = all([urlp.scheme, urlp.netloc])
        if url and url_valid:
            resp = requests.get(url)
            if resp.status_code not in range(200, 227):
                return self.catch_response(resp)
            return {
                "status_code": str(resp.status_code),
                "response": resp.content.decode("ascii"),
            }
        else:
            return {
                "status_code": "000",
                "response": "Invalid URL",
            }

    def post_request(self, url: str, body: dict, headers: dict) -> dict:
        # resp = requests.post(url, data=body, headers=headers)
        headers = self.get_headers() or {}
        resp = requests.request("POST", url, headers=headers, json=body)
        if resp.status_code not in range(200, 227):
            return self.catch_response(resp)
        return {
            "status_code": str(resp.status_code),
            "response": resp.content.decode("ascii"),
        }

    def delete_request(self, url: str) -> dict:
        resp = requests.request("DELETE", url)
        if resp.status_code not in range(200, 227):
            return self.catch_response(resp)
        return {
            "status_code": str(resp.status_code),
            "response": resp.content.decode("ascii"),
        }

    def put_request(self, url: str, body: dict, headers: dict) -> dict:
        # resp = requests.post(url, data=body, headers=headers)
        headers = self.get_headers() or {}
        resp = requests.request("PUT", url, headers=headers, json=body)
        if resp.status_code not in range(200, 227):
            return self.catch_response(resp)
        return {
            "status_code": str(resp.status_code),
            "response": resp.content.decode("ascii"),
        }

    def patch_request(self, url: str, body: dict, headers: dict) -> dict:
        # resp = requests.post(url, data=body, headers=headers)
        headers = self.get_headers() or {}
        resp = requests.request("PATCH", url, headers=headers, json=body)
        if resp.status_code not in range(200, 227):
            return self.catch_response(resp)
        return {
            "status_code": str(resp.status_code),
            "response": resp.content.decode("ascii"),
        }

    def on_input_submitted(self, message: Input.Submitted) -> None:
        url = message.value
        if self.method_choice == "GET":
            resp = self.get_request(url)
        if self.method_choice == "POST":
            body = json.loads(self.query_one("#body_inp").value) or {}
            resp = self.post_request(url, body=body, headers={})
        elif self.method_choice == "PUT":
            body = json.loads(self.query_one("#body_inp").value) or {}
            resp = self.put_request(url, body=body, headers={})
        elif self.method_choice == "PATCH":
            body = json.loads(self.query_one("#body_inp").value) or {}
            resp = self.patch_request(url, body=body, headers={})
        elif self.method_choice == "DELETE":
            resp = self.delete_request(url)
        else:
            ...
            #resp = self.get_request(url)
        for i in self.method_list:
            button = self.query_one(f"#{i.lower()}")
            background_color = "#24292f"
            if i == self.method_choice:
                button.styles.background = "green"
            else:
                button.styles.background = background_color
        self.query_one("#response_text", Static).update(resp["response"])
        self.query_one("#status_code", Static).update(resp["status_code"])

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        button_id = event.button.id
        if button_id == "tocurl":
            url = self.query_one("#url").value
            body = self.query_one("#body_inp").value or {}
            method = self.method_choice
            urlp = urlparse(url)
            url_valid = all([urlp.scheme, urlp.netloc])
            if url and url_valid:
                if not body or button_id in ["DELETE", "GET"]:
                    request = requests.request(method, url)
                else:
                    body = json.loads(body)
                    request = requests.request(method, url, json=body, headers={})
                c = curl.parse(request, return_it=True)
                pyperclip.copy(c)

        if button_id == "send":
            for i in self.method_list:
                button = self.query_one(f"#{i.lower()}")
                background_color = "#24292f"
                if i == self.method_choice:
                    button.styles.background = "green"
                else:
                    button.styles.background = background_color
            url = self.query(Input).first().value
            if self.method_choice == "POST":
                body = self.query_one("#body_inp").value or {}
                urlp = urlparse(url)
                url_valid = all([urlp.scheme, urlp.netloc])
                if body and url_valid:
                    body = json.loads(body)
                    # headers = self.query(".header").first().value or {}
                    resp = self.post_request(
                        url, body=body, headers={}
                    )  # , headers=headers)
                    self.query_one("#response_text", Static).update(resp["response"])
                    self.query_one("#status_code", Static).update(resp["status_code"])
            elif self.method_choice == "DELETE":
                resp = self.delete_request(url=url)
                self.query_one("#response_text", Static).update(resp["response"])
                self.query_one("#status_code", Static).update(resp["status_code"])
            elif self.method_choice == "PUT":
                body = self.query_one("#body_inp").value or {}
                urlp = urlparse(url)
                url_valid = all([urlp.scheme, urlp.netloc])
                if body and url_valid:
                    body = json.loads(body)
                    resp = self.put_request(url=url, body=body, headers={})
                    self.query_one("#response_text", Static).update(resp["response"])
                    self.query_one("#status_code", Static).update(resp["status_code"])
            elif self.method_choice == "PATCH":
                body = self.query_one("#body_inp").value or {}
                urlp = urlparse(url)
                url_valid = all([urlp.scheme, urlp.netloc])
                if body and url_valid:
                    body = json.loads(body)
                resp = self.patch_request(url=url, body=body, headers={})
                self.query_one("#response_text", Static).update(resp["response"])
                self.query_one("#status_code", Static).update(resp["status_code"])
            else:
                url = self.query(Input).first().value
                resp = self.get_request(url)
                self.query_one("#response_text", Static).update(resp["response"])

        elif button_id == "post":
            self.method_choice = "POST"
        elif button_id == "get":
            self.method_choice = "GET"
        elif button_id == "delete":
            self.method_choice = "DELETE"
        elif button_id == "put":
            self.method_choice = "PUT"
        elif button_id == "patch":
            self.method_choice = "PATCH"

        elif button_id == "importcurl":
            curl_request = pyperclip.paste()
            req_widget = RequestContainer()
            self.parent.mount(req_widget)
            new_req = self.parent.query("#aptui").last()
            new_req.query_one("#response_text", Static).update(curl_request)
            new_req.scroll_visible()
            # try:
            parsed_curl = uncurl.parse_context(f"""{curl_request}""")
            # except Exception as e:
            url = parsed_curl.url
            method = parsed_curl.method.upper()
            parsed_headers = parsed_curl.headers.items()
            data = parsed_curl.data
            headers = {}
            for k, v in parsed_headers:
                headers[k] = v
            new_req.query_one("#url").value = url
            new_req.query_one("#body_inp").value = data or ""
            self.method_choice = method

        elif button_id == "add_req":
            headers = RequestHeader(id="headers")
            self.query_one("#reqheaders").mount(headers)
            headers.scroll_visible()

        elif button_id == "savereq":
            self.save_request()

        elif button_id == "loadreq":
            self.load_request()

        elif button_id == "add_head":
            header = RequestHeader(id="header")
            self.query_one("#headers").mount(header)

        elif button_id == "copyresp":
            response_text = str(self.query_one("#response_text").renderable)
            pyperclip.copy(response_text)

    def compose(self) -> ComposeResult:
        """Create child widgets of a API Request."""
        yield Input(placeholder="URL", id="url")
        yield Button("Send", id="send", variant="success")
        yield RequestMethods("Rquest Methods", id="methods", classes="body")
        yield Container(RequestHeader(), id="headers")
        yield Button("Add Header", id="add_head")
        yield Body(expand=True, id="body")
        yield Container(
            Button("Copy Curl", id="tocurl"),
            Button("Import", id="importcurl"),
            Button("Save", id="savereq"),
            Button("Load", id="loadreq"),
            Button("Copy Response", id="copyresp"),
            id="opts",
        )
        yield Response("Response", expand=True, id="response")

    def on_mount(self) -> None:
        self.styles.height = "auto"
