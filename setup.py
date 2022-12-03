import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = "0.0.1"
PACKAGE_NAME = "APTUI"
AUTHOR = "Meet Gor"
AUTHOR_EMAIL = "gormeet711@gmail.com"
URL = "https://github.com/Mr-Destructive/aptui"

DESCRIPTION = (
    "API Textual User Interface, Test APIs from the terminal."
)

INSTALL_REQUIRES = [
    "requests",
    "textual",
    "pyperclip",
    "uncurl",
    "requests-to-curl",
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
    entry_points={"console_scripts": ["aptui = src.main:main"]},
)
