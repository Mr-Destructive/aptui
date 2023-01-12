# APTUI - Application Programming Textual User Interface

An terminal interface for testing and working with APIs and web requests. It is(will be) like [Postman](https://www.postman.com/) or [Insomnia](https://insomnia.rest/) applications but in the terminal. Though it won't be a fully feldged application like those GUIs but it would serve the basic functionalities for testing APIs. 

API + TUI = APTUI

![APTUI base app](https://meetgor-cdn.pages.dev/aptui-dev-1.png)

## Development Progress

It's quite a fresh project and is in it's initial stage of development.

## Installation


- With Normal package installation:

```
pip install git+https://github.com/mr-destructive/aptui
aptui
```

- With pipx:

```
pipx run --spec git+https://github.com/mr-destructive/aptui aptui
```

### TODO

- Improve UI
- Allow expandable response text
- Fix and Improve Copy from Curl Feature
- Save and Load requests from previous session/file
- Tabulate different requests instead of scroll tree

### DONE

- Basic app structure
- Layout of the TUI
- REST API CRUD Requests
- GraphQL API GET requests

## Tech Stack

- Python
  - [Textual](https://pypi.org/project/textual/)
  - [Rich](https://pypi.org/project/rich/)
  - [Requests](https://pypi.org/project/requests/)
  - [Pyperclip](https://pypi.org/project/pyperclip/)
  - [Uncurl](https://github.com/spulec/uncurl)
  - [Requests-To-Curl](https://pypi.org/project/requests-to-curl/)

## Development Log


GET Request:

![APTUI GET Request](https://meetgor-cdn.pages.dev/aptui-dev-get.png)


POST Request:

![POST Request](https://meetgor-cdn.pages.dev/aptui-dev-post.png)

